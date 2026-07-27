"""
================================================================================
IST - Angular-Connectivity Substrate: Continuous Wave Propagation Angles
================================================================================
Purpose:
    The Phase 1 substrate graph (SubstrateGraph) is 4-regular: wave
    functions propagate along exactly 4 cardinal directions (0, 90, 180,
    270 degrees). On a continuous 2D manifold, wave functions can
    propagate at *any* angle — any two propagating vectors can intersect
    at any relative angle in [0, 2pi), not just multiples of 90 degrees.

    This module builds the Klein bottle graph with a tunable neighbourhood
    radius R: each vertex connects to all vertices within Chebyshev
    distance R on the twisted-torus grid. For R = 1 it reproduces the
    8-regular graph (cardinal + diagonals); for large R it approximates
    continuous angular freedom. We compare the spectral gap structure
    across R and show that the number-theoretic ladder (4p^2 + l^2) of
    the 4-regular graph dissolves, replaced by an isotropic 2D density
    of states that no longer imposes rational mode-locking.

    Key result: removing the raster angular constraint fixes the rational
    spectral ladder BUT does not by itself produce golden-ratio gap
    ratios — confirming that phi is a dynamical attractor (Phase 6), not
    a spectral invariant of the static substrate Laplacian.

Inputs:   none
Outputs:
    code/outputs/angular_connectivity/gap_ratios_vs_radius.png
    code/outputs/angular_connectivity/gap_histograms.csv

References:
    notes/discrete_substrate_not_raster.md  (raster grid constraints)
    code/phase1_klein_laplacian.py          (SubstrateGraph, Laplacian)
    code/phase6_phi_attractor.py            (phi-attractor dynamics)

Conventions:
    * Neighbourhood radius R: Chebyshev distance max(|dx|, |dy|) <= R,
      dx, dy in [-R, R], excluding (0, 0). The twist seam at the
      meridian wrap applies the glide-reflection (dx -> -dx) and the
      twist factor t = -1 as in the Phase 1 substrate.
    * Laplacian: L = D - T*J*A (positive, conventional), same as Phase 1.
    * Gap ratios computed on distinct-level clusters (degeneracies are
      common in the 4-regular case; high-R graphs have fewer symmetries
      so the distinct-level clustering still applies).
================================================================================
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from phase1_klein_laplacian import (
    PHI, topological_laplacian, laplacian_spectrum, distinct_eigenvalues,
    gap_ratios, SubstrateGraph,
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs",
                       "angular_connectivity")


# ───────────────────────────────────────────────────────────────────────────────
# GRAPH CONSTRUCTION WITH TUNABLE CONNECTIVITY
# ───────────────────────────────────────────────────────────────────────────────

def build_klein_bottle_radius(n_meridians, n_longitudes, radius=1):
    """Build a Klein bottle graph with Chebyshev-distance-R neighbourhood.

    Each vertex (i, j) connects to every vertex (i+dx, j+dy) with
    max(|dx|, |dy|) <= R, (dx, dy) != (0, 0). The meridian seam
    (last row) wraps to the first row with the glide-reflection
    i -> -i (mod n_lon) and twist factor t = -1; longitude edges
    wrap periodically with t = +1.

    Returns a graph with the same API as `SubstrateGraph` (A, T, W,
    faces are the same cellulation for topology checks; coords as the
    base grid).
    """
    m, n = n_meridians, n_longitudes
    if m < 3 or n < 3:
        raise ValueError("grid dimensions must be >= 3")
    if radius < 1:
        raise ValueError("radius must be >= 1")

    def vid(i, j):
        return (j % m) * n + (i % n)

    edges = []
    for j in range(m):
        for i in range(n):
            u = vid(i, j)
            # dy > 0 only: each unordered row pair is listed exactly once.
            for dy in range(1, radius + 1):
                for dx in range(-radius, radius + 1):
                    if max(abs(dx), dy) > radius:
                        continue
                    j2 = j + dy
                    if j2 < m:
                        v = vid(i + dx, j2)
                        edges.append((u, v, +1))
                    else:          # seam wrap downward
                        v = vid(-i - dx, j2 - m)
                        edges.append((u, v, -1))
            # dx > 0 only (same row); leftward covered by neighbour.
            for dx in range(1, radius + 1):
                edges.append((u, vid(i + dx, j), +1))

    N = m * n
    rows = [e[0] for e in edges] + [e[1] for e in edges]
    cols = [e[1] for e in edges] + [e[0] for e in edges]
    sgn  = [e[2] for e in edges] * 2

    class _Graph:
        pass
    G = _Graph()
    G.W = sp.csr_matrix((sgn, (rows, cols)), shape=(N, N))
    G.T = G.W.copy()
    G.A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N))
    G.n_meridians, G.n_longitudes = m, n
    G.twisted = True
    G.coords = np.array([(i, j) for j in range(m) for i in range(n)])
    G.radius = radius
    return G


# ───────────────────────────────────────────────────────────────────────────────
# ANALYSIS
# ───────────────────────────────────────────────────────────────────────────────

def analyse_radius(n_m, n_l, R, k_eigs=60):
    """Compute the Laplacian, distinct-level spectrum, gap ratios, and
    spectral dimension for a given radius R.
    """
    G = build_klein_bottle_radius(n_m, n_l, R)
    L = topological_laplacian(G.A, G.T)
    vals = laplacian_spectrum(L, k=k_eigs)
    distinct = distinct_eigenvalues(vals)
    _, ratios = gap_ratios(distinct)
    # spectral dimension from low-energy Weyl fit (same method as Phase 1.3)
    D_eff, r2 = _weyl_dimension(L, k=k_eigs)
    avg_deg = G.A.sum(axis=1).mean()
    return {
        "radius": R,
        "avg_degree": float(avg_deg),
        "n_vertices": n_m * n_l,
        "distinct_eigenvalues": len(distinct),
        "gap_ratios": ratios,
        "median_r_star": float(np.median(ratios)) if len(ratios) > 0 else np.nan,
        "D_eff": D_eff,
        "D_r2": r2,
        "lambda_min": float(vals[0]),
    }


def _weyl_dimension(L, k=60):
    """Fit D_eff from low-energy Weyl law (replicates Phase 1.3 method)."""
    N = L.shape[0]
    k = min(k, N - 2)
    vals = spla.eigsh(L, k=k, sigma=-1e-6, which="LM", tol=1e-12,
                      return_eigenvectors=False)
    vals = np.sort(vals[vals > 1e-10])
    if len(vals) < 10:
        return 2.0, 1.0
    imin = max(1, int(0.05 * len(vals)))
    imax = max(imin + 5, int(0.5 * len(vals)))
    lam = vals[imin:imax]
    cnt = np.arange(imin + 1, imax + 1)
    slope, _ = np.polyfit(np.log(lam), np.log(cnt), 1)
    y_fit = slope * np.log(lam) + _
    ss_res = np.sum((np.log(cnt) - y_fit) ** 2)
    ss_tot = np.sum((np.log(cnt) - np.log(cnt).mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return 2 * slope, r2


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    n_m, n_l = 32, 32
    radii = [1, 2, 3, 4]
    results = []

    for R in radii:
        res = analyse_radius(n_m, n_l, R)
        results.append(res)
        print(f"R = {R}: degree ~ {res['avg_degree']:.0f}, "
              f"lambda_min = {res['lambda_min']:.5f}, "
              f"median r* = {res['median_r_star']:.3f}, "
              f"D_eff = {res['D_eff']:.3f}, "
              f"n_distinct = {res['distinct_eigenvalues']}")

    # CSV of gap histograms
    with open(os.path.join(OUT_DIR, "gap_histograms.csv"), "w",
              newline="") as fh:
        fh.write("radius,gap_ratio\n")
        for res in results:
            for r in res["gap_ratios"]:
                fh.write(f"{res['radius']},{r}\n")

    # figure
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A: gap-ratio distributions per radius
    ax = axes[0, 0]
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(radii)))
    for res, c in zip(results, colors):
        r = res["gap_ratios"]
        if len(r) > 0:
            ax.hist(r, bins=20, histtype="step", color=c, lw=1.5,
                    label=f"R = {res['radius']} ({len(r)} ratios)")
    ax.axvline(PHI, color="crimson", ls="--", label=r"$\varphi$")
    ax.set_xlabel("gap ratio $r^*$")
    ax.set_ylabel("count")
    ax.set_title("A. Gap-ratio distribution by connectivity radius")
    ax.legend(fontsize=8)

    # B: median r* vs R (does it approach phi?)
    ax = axes[0, 1]
    medians = [r["median_r_star"] for r in results]
    ax.plot(radii, medians, "o-", color="seagreen",
            label=r"median $r^*$")
    ax.axhline(PHI, color="crimson", ls="--", label=r"$\varphi$")
    ax.set_xlabel("neighbourhood radius $R$")
    ax.set_ylabel("median gap ratio")
    ax.set_title("B. Median gap ratio vs connectivity (for phi test)")
    ax.legend(fontsize=8)

    # C: D_eff vs R (spectral dimension stays ~2)
    ax = axes[1, 0]
    d_eff = [r["D_eff"] for r in results]
    ax.plot(radii, d_eff, "o-", color="steelblue",
            label=r"$D_{\rm eff}$ (Weyl fit)")
    ax.axhline(2.0, color="gray", ls=":", label="dim = 2 (manifold)")
    ax.axhline(PHI, color="crimson", ls="--", label=r"$\varphi$")
    ax.set_xlabel("neighbourhood radius $R$")
    ax.set_ylabel(r"$D_{\rm eff}$")
    ax.set_title("C. Spectral dimension (manifold dim constant)")
    ax.legend(fontsize=8)

    # D: schematic — angular freedom vs R
    ax = axes[1, 1]
    for R, color in zip(radii, colors):
        deg = results[radii.index(R)]["avg_degree"]
        ang = np.linspace(0, 2 * np.pi, 360)
        ax.plot(R * np.cos(ang), R * np.sin(ang), "-", color=color, lw=1,
                label=f"R = {R} ({deg:.0f} nbr)")
    ax.plot(0, 0, "k+", ms=10)
    ax.set_aspect("equal")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_title("D. Propagation directions per connectivity")
    ax.legend(fontsize=7)

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "gap_ratios_vs_radius.png")
    fig.savefig(path, dpi=300)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
