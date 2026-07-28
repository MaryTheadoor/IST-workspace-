"""
================================================================================
IST PHASE 7 - Vector Substrate: Spectral-Proximity Coupling Graph
================================================================================
Purpose:
    Implement the vector-encoded substrate: a population of N oscillators on
    the spectral circle whose pairwise coupling is determined by their
    angular proximity (weighted by the Phase 6 anti-resonance principle:
    Fibonacci gap structures suppress resonant triples, minimizing
    associator-mediated volume creation). The coupling graph emerges FROM
    the oscillator dispositions, not from a pre-assigned raster grid.

    Three ensembles are compared:
      * Random: uniformly distributed phases (disordered)
      * Rational (1/5): phase-locked on the circle, repeating every 5
      * Fibonacci (golden): phases following the golden rotation 1/phi^2,
        with the three-gap self-similar structure

    For each ensemble, the average degree is varied via the coupling range
    sigma, and the effective spectral dimension D_eff of the Laplacian is
    measured. If the golden rotation selects anti-resonant clustering,
    the Fibonacci graph should have a spectral dimension that differs
    systematically from both random and rational graphs.

Inputs:   none
Outputs:
    code/outputs/phase7/d_eff_comparison.csv
    code/outputs/phase7/sigma_scan.csv
    code/outputs/phase7/spatial_vs_spectral.png

References:
    notes/discrete_substrate_not_raster.md  (raster constraints)
    code/phase6_phi_attractor.py            (circle anti-resonance)
    code/phase1_klein_laplacian.py          (baseline D_eff = 2)

Conventions:
    * Spectral proximity coupling: J_ij = exp(-d_ij^2 / (2 sigma^2)),
      d_ij = angular distance on [0, 2pi).
    * Laplacian: L = D - J (unsigned, weighted, no twist).
    * Effective degree d_eff = (1/N) sum_i sum_j I(J_ij > tol).
    * D_eff from low-energy Weyl fit (same method as Phase 1.3).
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase7")
ALPHA_GOLDEN = 1.0 / PHI ** 2


# ───────────────────────────────────────────────────────────────────────────────
# OSCILLATOR ENSEMBLES
# ───────────────────────────────────────────────────────────────────────────────

def fibonacci_phases(N):
    """Phases ordered by the golden rotation orbit alpha = 1/phi^2,
    in increasing order on the circle (three-gap partition)."""
    raw = np.sort(np.array([(k * ALPHA_GOLDEN) % 1.0 for k in range(N)]))
    return 2 * np.pi * raw


def rational_phases(N, alpha=0.2):
    """Phases from a rational rotation with substantial spread so the
    graph is not a union of 5 disconnected cliques (finite plonk
    resolution prevents exact phase coincidence)."""
    raw = np.sort(((np.arange(N) * alpha) + 0.04 * np.sin(np.arange(N) * 73.0)) % 1.0)
    return 2 * np.pi * raw


def random_phases(N, rng):
    """IID uniform on the circle."""
    return 2 * np.pi * np.sort(rng.uniform(size=N))


# ───────────────────────────────────────────────────────────────────────────────
# SPECTRAL-PROXIMITY COUPLING GRAPH
# ───────────────────────────────────────────────────────────────────────────────

def spectral_graph(phases, sigma, tol=1e-4):
    """Weighted coupling graph from Gaussian spectral proximity.

    J_ij = exp(-d(phase_i, phase_j)^2 / (2 sigma^2)).
    Returns: adjacency A (csr), Laplacian L, effective degree d_eff.
    """
    N = len(phases)
    ph = np.asarray(phases)
    dmat = np.abs(ph[:, None] - ph[None, :])
    dmat = np.minimum(dmat, 2 * np.pi - dmat)
    J = np.exp(-dmat ** 2 / (2 * sigma ** 2))
    np.fill_diagonal(J, 0.0)
    J[J < tol] = 0.0
    A = sp.csr_matrix(J)
    D_vec = np.asarray(A.sum(axis=1)).ravel()
    L = sp.diags(D_vec) - A
    d_eff = (A.nnz / N)
    return A, L, d_eff


def spectral_dimension(L, k=60):
    """D_eff from low-energy Weyl fit. Returns NaN on poorly conditioned fits."""
    N = L.shape[0]
    k = min(k, N - 2)
    try:
        vals = spla.eigsh(L, k=k, sigma=-0.01, which="LM", tol=1e-8,
                          return_eigenvectors=False)
    except spla.ArpackError:
        return np.nan, 0.0
    vals = np.sort(vals[vals > 1e-10])
    if len(vals) < 10:
        return np.nan, 0.0
    imin = max(1, int(0.05 * len(vals)))
    imax = max(imin + 5, int(min(0.5 * len(vals), 3 * imin)))
    lam, cnt = vals[imin:imax], np.arange(imin + 1, imax + 1)
    slope, _ = np.polyfit(np.log(lam), np.log(cnt), 1)
    y_fit = slope * np.log(lam) + _
    ss_res = np.sum((np.log(cnt) - y_fit) ** 2)
    ss_tot = np.sum((np.log(cnt) - np.log(cnt).mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    if r2 < 0.5:
        return np.nan, r2
    return 2 * slope, r2


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    N = 128
    sigmas = np.geomspace(0.04, 0.50, 14)
    rng = np.random.default_rng(42)

    ensembles = {
        "Fibonacci (golden)": fibonacci_phases(N),
        "Rational (1/5)": rational_phases(N, 0.2),
        "Random": random_phases(N, rng),
    }

    rows = []
    for name, phases in ensembles.items():
        for sig in sigmas:
            A, L, d_eff = spectral_graph(phases, sig)
            D, r2 = spectral_dimension(L)
            rows.append({
                "ensemble": name, "N": N, "sigma": sig,
                "avg_degree": d_eff, "D_eff": D, "r2": r2,
            })
            print(f"{name:25s} sigma={sig:.4f}  deg={d_eff:5.1f}  "
                  f"D_eff = {D:.3f}  (r2={r2:.3f})")

    with open(os.path.join(OUT_DIR, "sigma_scan.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    make_figure(rows, ensembles)


def make_figure(rows, ensembles):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    colors = {"Fibonacci (golden)": "seagreen", "Rational (1/5)": "crimson",
              "Random": "steelblue"}

    # A: D_eff vs degree
    ax = axes[0, 0]
    for name in ensembles:
        pts = [(r["avg_degree"], r["D_eff"]) for r in rows
               if r["ensemble"] == name]
        ds, ds_eff = zip(*sorted(pts))
        ax.plot(ds, ds_eff, "o-", color=colors[name], label=name)
    ax.axhline(PHI, color="gray", ls="--", label=r"$\varphi$ = 1.618")
    ax.axhline(2.0, color="gray", ls=":", label="grid D = 2")
    ax.axhline(1.0, color="gray", ls=":", label="S^1 (1D manifold)")
    ax.set_xlabel("average degree")
    ax.set_ylabel(r"$D_{\rm eff}$")
    ax.set_title(f"A. Spectral dimension vs connectivity (N = {ensembles['Fibonacci (golden)'].size})")
    ax.legend(fontsize=8)

    # B: |D_eff - phi| vs degree
    ax = axes[0, 1]
    for name in ensembles:
        pts = [(r["avg_degree"], r["D_eff"]) for r in rows
               if r["ensemble"] == name]
        ds, ds_eff = zip(*sorted(pts))
        ax.semilogy(ds, np.abs(np.array(ds_eff) - PHI), "o-",
                    color=colors[name], label=name)
    ax.set_xlabel("average degree")
    ax.set_ylabel(r"$|D_{\rm eff} - \varphi|$")
    ax.set_title("B. Distance from golden dimension")
    ax.legend(fontsize=8)

    # C: adjacency matrix images (degree ~ 20)
    ax = axes[1, 0]
    ax.set_visible(False)
    target_deg = 20.0
    for idx, (name, phases) in enumerate(ensembles.items()):
        sig_cands = np.geomspace(0.04, 0.50, 30)
        sig = min(sig_cands, key=lambda s:
                  abs(spectral_graph(phases, s)[2] - target_deg))
        A_, _, _ = spectral_graph(phases, sig)
        J = A_.toarray()
        ax_ins = fig.add_axes([0.08 + idx * 0.30, 0.06, 0.26, 0.35])
        ax_ins.imshow(J > 0, cmap="gray_r", aspect="equal", interpolation="none")
        ax_ins.set_title(f"{name.split()[0]} (deg~{int(A_.nnz/len(phases))})",
                         fontsize=8)
        ax_ins.set_xticks([])
        ax_ins.set_yticks([])

    # D: oscillator disposition on circle (first 50)
    ax = axes[1, 1]
    for name, phases in ensembles.items():
        ang = np.sort(phases[:50])
        ax.scatter(np.cos(ang), np.sin(ang), s=20, color=colors[name],
                   alpha=0.7, label=name)
    ax.set_aspect("equal")
    ax.set_title("D. Oscillator phases on the spectral circle")
    ax.legend(fontsize=8, loc="upper right")
    ax.set_xlabel("cos theta")
    ax.set_ylabel("sin theta")

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "vector_substrate.png")
    fig.savefig(path, dpi=300)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
