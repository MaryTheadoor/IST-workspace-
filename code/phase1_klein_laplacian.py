
"""
================================================================================
IST PHASE 1.1 - Discrete Klein Bottle Graph & Topological Laplacian
================================================================================
Purpose:
    Construct the discrete substrate graph G_n of Information Substrate
    Theory: a finite 4-regular cellulation of the Klein bottle whose edges
    carry twists t_ij in {+1, -1} encoding non-orientability, together with
    its twisted (topological) graph Laplacian. Provides the topology checks
    required by the roadmap: Euler characteristic, orientability, and twist
    holonomy of the self-intersection (seam) cycle.

Inputs:
    n_meridians   - grid points along the twisted (meridian) direction
    n_longitudes  - grid points along the untwisted (longitude) direction

Outputs:
    SubstrateGraph (adjacency A, twist T, signed adjacency W, faces, coords),
    positive Laplacian L = D - T*J*A, topology checks, numerical spectra via
    shift-invert Lanczos, and closed-form analytic spectra for validation.

References:
    notes/IST_Research_Plan_Phases_1-5.md   (Phase 1.1)
    main/ist_v5_3_topology_substrate.md     (substrate, twist, plonk units)

Conventions:
    * The plan writes the Laplacian as L_plan = T*J*A - D. We return the
      conventional positive Laplacian L = D - T*J*A = -L_plan so the spectrum
      is nonnegative with lambda_0 the ground state (Laplace-Beltrami
      convention). Gap sequences are identical under this overall sign flip.
    * Vertex id v = j*n_longitudes + i, with i the longitude index
      (periodic) and j the meridian index (twisted periodic).
    * Twist assignment: every edge has t = +1 except the n_longitudes seam
      edges (i, n_mer-1) <-> ((-i) mod n_lon, 0), which carry t = -1.
      This is a flat Z_2 connection: holonomy -1 around the meridian
      (orientation-reversing cycle), +1 around every contractible
      plaquette and around the longitude.
    * Analytic spectrum (derivation: separate variables s(i,j) =
      exp(i*kappa*i) * exp(i*theta*j); the seam imposes s(i, m) = -s(-i, 0),
      forcing theta = pi*l/n_mer - half-integer-spacing boundary condition):
          lambda(p, l) = 4 - 2 cos(2*pi*p / n_lon) - 2 cos(pi*l / n_mer)
      with p in Z_{n_lon}, l in Z_{2*n_mer}, and paired standing-wave
      constraints. The smallest eigenvalue is 4 sin^2(pi / (2 n_mer)) > 0:
      the twist removes the zero mode (no globally constant section exists
      on a non-orientable bundle).
================================================================================
"""

from collections import deque

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

PHI = (1 + np.sqrt(5)) / 2  # Golden ratio ~ 1.618033988749895


# ───────────────────────────────────────────────────────────────────────────────
# GRAPH CONSTRUCTION
# ───────────────────────────────────────────────────────────────────────────────

class SubstrateGraph:
    """Discrete substrate graph: twisted torus (Klein bottle) or plain torus.

    Attributes
    ----------
    A : csr_matrix      Unsigned adjacency (0/1).
    T : csr_matrix      Twist matrix (+/-1 on edges, zero elsewhere).
    W : csr_matrix      Signed adjacency W = T hadamard A (J = 1).
    faces : list[list[int]]
        Plaquette boundaries as ordered vertex cycles (for orientability
        and Euler characteristic).
    coords : (N, 2) int array   Grid coordinates (i, j) per vertex id.
    n_meridians, n_longitudes : int
    twisted : bool      True -> Klein bottle, False -> torus control.
    seam_edges : list[(int, int)]   The distinguished self-intersection locus.
    """

    def __init__(self, n_meridians, n_longitudes, twisted=True):
        if n_meridians < 3 or n_longitudes < 3:
            raise ValueError("grid dimensions must be >= 3")
        self.n_meridians = n_meridians
        self.n_longitudes = n_longitudes
        self.twisted = twisted

        m, n = n_meridians, n_longitudes

        def vid(i, j):
            return (j % m) * n + (i % n)

        # Edges: (u, v, twist). Longitude edges and interior meridian edges
        # are untwisted; the seam row closes with the glide reflection.
        edges = []
        for j in range(m):
            for i in range(n):
                edges.append((vid(i, j), vid(i + 1, j), +1))
                if j < m - 1:
                    edges.append((vid(i, j), vid(i, j + 1), +1))
                elif twisted:
                    edges.append((vid(i, m - 1), vid(-i, 0), -1))
                else:
                    edges.append((vid(i, m - 1), vid(i, 0), +1))

        # Plaquettes as ordered cycles, following the seam identification.
        faces = []
        for j in range(m):
            for i in range(n):
                if j < m - 1:
                    faces.append([vid(i, j), vid(i + 1, j),
                                  vid(i + 1, j + 1), vid(i, j + 1)])
                elif twisted:
                    faces.append([vid(i, m - 1), vid(i + 1, m - 1),
                                  vid(-(i + 1), 0), vid(-i, 0)])
                else:
                    faces.append([vid(i, m - 1), vid(i + 1, m - 1),
                                  vid(i + 1, 0), vid(i, 0)])

        N = m * n
        rows = [e[0] for e in edges] + [e[1] for e in edges]
        cols = [e[1] for e in edges] + [e[0] for e in edges]
        sgn = [e[2] for e in edges] * 2
        self.W = sp.csr_matrix((sgn, (rows, cols)), shape=(N, N))
        self.T = self.W.copy()
        self.A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N))
        self.faces = faces
        self.coords = np.array([(i, j) for j in range(m) for i in range(n)])
        self.seam_edges = ([(vid(i, m - 1), vid(-i, 0)) for i in range(n)]
                           if twisted else [])
        self._twist_lookup = {(min(u, v), max(u, v)): t for u, v, t in edges}

    # ── Laplacian ────────────────────────────────────────────────────────────

    def laplacian(self, J=None):
        """Positive topological Laplacian L = D - T*J*A of this graph."""
        return topological_laplacian(self.A, self.T, J)

    # ── Topology checks ──────────────────────────────────────────────────────

    def euler_characteristic(self):
        """chi = V - E + F, computed from the actual cellulation."""
        V = self.A.shape[0]
        E = self.A.nnz // 2
        F = len(self.faces)
        return V - E + F

    def is_orientable(self):
        """Try to assign consistent face orientations by BFS.

        Two faces sharing an edge must traverse it in opposite directions.
        If they traverse it the same way, one face's orientation must flip.
        A contradiction around any dual cycle means non-orientable.
        """
        incidence = {}
        for f_idx, face in enumerate(self.faces):
            for a in range(len(face)):
                u, v = face[a], face[(a + 1) % len(face)]
                key = (min(u, v), max(u, v))
                direction = +1 if (u, v) == key else -1
                incidence.setdefault(key, []).append((f_idx, direction))

        adj = {f: [] for f in range(len(self.faces))}
        for occ in incidence.values():
            if len(occ) != 2:
                return False  # not a closed-surface cellulation
            (f1, d1), (f2, d2) = occ
            relation = -1 if d1 == d2 else +1
            adj[f1].append((f2, relation))
            adj[f2].append((f1, relation))

        sign = {}
        for start in range(len(self.faces)):
            if start in sign:
                continue
            sign[start] = +1
            queue = deque([start])
            while queue:
                f = queue.popleft()
                for g, rel in adj[f]:
                    want = rel * sign[f]
                    if g in sign:
                        if sign[g] != want:
                            return False
                    else:
                        sign[g] = want
                        queue.append(g)
        return True

    # ── Twist holonomy ───────────────────────────────────────────────────────

    def walk_twist_product(self, walk):
        """Product of edge twists along a closed walk (list of vertex ids)."""
        product = +1
        for a in range(len(walk) - 1):
            u, v = walk[a], walk[a + 1]
            product *= self._twist_lookup[(min(u, v), max(u, v))]
        return product

    def meridian_walk(self, i0=0):
        """Closed walk around the twisted direction at longitude i0."""
        n, m = self.n_longitudes, self.n_meridians
        return [j * n + (i0 % n) for j in range(m)] + [(-i0) % n]

    def longitude_walk(self, j0=0):
        """Closed walk around the untwisted direction at meridian j0."""
        n = self.n_longitudes
        return [j0 * n + i for i in range(n)] + [j0 * n]


def build_klein_bottle_graph(n_meridians, n_longitudes):
    """Build discrete Klein bottle as twisted torus graph.

    Returns the graph bundle: sparse adjacency A, twist matrix T, signed
    adjacency W = T hadamard A, vertex coordinates, plaquette faces, and
    the seam (self-intersection) edge set.
    """
    return SubstrateGraph(n_meridians, n_longitudes, twisted=True)


def build_torus_graph(n_meridians, n_longitudes):
    """Untwisted control: same grid with trivial (orientable) closure."""
    return SubstrateGraph(n_meridians, n_longitudes, twisted=False)


def topological_laplacian(A, T, J=None):
    """Positive topological Laplacian L = D - T*J*A.

    The plan defines L_plan = T*J*A - D; we return L = -L_plan so the
    spectrum is nonnegative with the ground state first. J defaults to
    uniform unit coupling. Degrees d_i = sum_j (J*A)_ij (unsigned weights),
    which keeps L positive semidefinite.
    """
    W = A.multiply(T) if J is None else A.multiply(T).multiply(J)
    weights = A if J is None else A.multiply(J)
    degrees = np.asarray(weights.sum(axis=1)).ravel()
    return sp.diags(degrees) - W


# ───────────────────────────────────────────────────────────────────────────────
# SPECTRA
# ───────────────────────────────────────────────────────────────────────────────

def laplacian_spectrum(L, k=40, sigma=-1e-6):
    """Smallest k eigenvalues of the (sparse, PSD) Laplacian.

    Shift-invert at a small negative sigma: L - sigma*I is positive definite
    even for the torus control (which has an exact zero mode), and Lanczos
    converges quickly on the bottom of the spectrum.
    """
    k = min(k, L.shape[0] - 2)
    vals = spla.eigsh(L, k=k, sigma=sigma, which="LM", tol=1e-12,
                      return_eigenvectors=False)
    return np.sort(vals)


def analytic_klein_eigenvalues(n_meridians, n_longitudes, count):
    """Closed-form Klein bottle eigenvalues: 4 - 2cos(2 pi p/n) - 2cos(pi l/m)."""
    p = np.arange(n_longitudes)
    ell = np.arange(2 * n_meridians)
    lam = (4 - 2 * np.cos(2 * np.pi * p[:, None] / n_longitudes)
              - 2 * np.cos(np.pi * ell[None, :] / n_meridians))
    return np.sort(lam.ravel())[:count]


def analytic_torus_eigenvalues(n_meridians, n_longitudes, count):
    """Closed-form torus eigenvalues: 4 - 2cos(2 pi p/n) - 2cos(2 pi q/m)."""
    p = np.arange(n_longitudes)
    q = np.arange(n_meridians)
    lam = (4 - 2 * np.cos(2 * np.pi * p[:, None] / n_longitudes)
              - 2 * np.cos(2 * np.pi * q[None, :] / n_meridians))
    return np.sort(lam.ravel())[:count]


def distinct_eigenvalues(vals, atol=1e-8, rtol=1e-6):
    """Cluster a sorted eigenvalue array into distinct levels.

    Exact degeneracies (e.g. cos-symmetry partners) come back from Lanczos
    within ~1e-10 of each other; clustering collapses them so gap ratios
    are computed between genuine distinct levels rather than across
    numerical-zero gaps.
    """
    clusters = []
    for v in vals:
        if clusters and abs(v - clusters[-1][-1]) <= atol + rtol * abs(v):
            clusters[-1].append(v)
        else:
            clusters.append([v])
    return np.array([np.mean(c) for c in clusters])


def gap_ratios(distinct):
    """Gaps g_k = d_{k+1} - d_k and ratios r_k = g_k / g_{k-1} of a distinct
    level sequence (the plan's r_k = (l_{k+1} - l_k)/(l_k - l_{k-1}))."""
    gaps = np.diff(distinct)
    ratios = gaps[1:] / gaps[:-1]
    return gaps, ratios
