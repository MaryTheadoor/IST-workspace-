"""
================================================================================
IST PHASE 16 — Dimensional Amplification: 3D as Critical Dimension?
================================================================================
Test whether 3D is the "critical dimension" where the vacuum pump's
constructive interference peaks. Extend the Phase 10 vector substrate
to 2D, 3D, 4D, and 5D hypercubic grids with periodic boundaries.
Each cell couples to its 2*d nearest neighbours. The tanh nonlinearity
with gain and noise drives the field. We measure D_eff, spatial
coherence, and amplification per dimension.

Hypothesis (from Plan 12): 3D shows maximum amplification before 4D+
over-saturates and the field collapses toward uniformity.

Inputs:   none
Outputs:  code/outputs/phase16/dim_scan.csv
          code/outputs/phase16/dim_amplification.png
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

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase16")


# ───────────────────────────────────────────────────────────────────────────────
# D-DIMENSIONAL VECTOR SUBSTRATE
# ───────────────────────────────────────────────────────────────────────────────

def build_d_dim_periodic(n, d):
    """Sparse adjacency for d-dim periodic hypercube, side n, degree 2d."""
    N = n ** d
    rows, cols = [], []
    for dim in range(d):
        stride = n ** dim
        block = stride * n  # stride * n = n^{dim+1}
        for i in range(N):
            pos = (i // stride) % n
            if pos < n - 1:
                jp = i + stride
            else:
                jp = i - (n - 1) * stride
            if pos > 0:
                jm = i - stride
            else:
                jm = i + (n - 1) * stride
            rows.extend([i, i])
            cols.extend([jp, jm])
    data = np.ones(len(rows))
    return sp.csr_matrix((data, (rows, cols)), shape=(N, N))


def d_dim_laplacian(n, d):
    """L = D - A for the d-dim periodic hypercube."""
    A = build_d_dim_periodic(n, d)
    D = np.asarray(A.sum(axis=1)).ravel()
    return sp.diags(D) - A


def spectral_dimension(L, k=30):
    """D_eff from low-energy Weyl fit."""
    N = L.shape[0]
    k = min(k, N - 2)
    try:
        vals = spla.eigsh(L, k=k, sigma=-1e-4, which="LM", tol=1e-8,
                          return_eigenvectors=False)
    except spla.ArpackError:
        return np.nan
    vals = np.sort(vals[vals > 1e-10])
    if len(vals) < 8:
        return np.nan
    imin = max(1, int(0.05 * len(vals)))
    imax = max(imin + 5, int(0.4 * len(vals)))
    lam, cnt = vals[imin:imax], np.arange(imin + 1, imax + 1)
    slope, _ = np.polyfit(np.log(lam), np.log(cnt), 1)
    return 2 * slope


def run_d_dim_simulation(n, d, gain=None, noise_std=0.02, n_ticks=400):
    """Run the vector substrate in d dimensions. Returns D_eff (static
    Laplacian), coherence, and amplification (field std after tanh)."""
    if gain is None:
        gain = 2.0 * d * 1.15  # barely supercritical ~ 2.3*d, total ~2.3d/2d=1.15 per neighbor
    N = n ** d
    A = build_d_dim_periodic(n, d)
    deg = 2.0 * d
    rng = np.random.default_rng(d * 7)
    s = rng.random((N, 3)) * 0.5

    for t in range(n_ticks):
        h = (A @ s) / deg
        s = np.tanh(gain * h + noise_std * rng.standard_normal((N, 3)))

    # static Laplacian dimension
    D_vec = np.asarray(A.sum(axis=1)).ravel()
    L = sp.diags(D_vec) - A
    D = spectral_dimension(L, k=min(30, N - 2))
    # field metrics
    amp = np.sqrt(np.sum(s ** 2, axis=1))
    coherence = 1.0 - amp.std() / (amp.mean() + 1e-9)
    amplification = amp.mean()
    return D, coherence, amplification


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = []
    configs = [(2, 12, 1000), (3, 10, 1000), (4, 8, 800), (5, 7, 500)]
    for d, n, ticks in configs:
        D, coh, amp = run_d_dim_simulation(n, d, n_ticks=ticks,
                                            noise_std=0.05)
        rows.append({"dim": d, "N": n**d,
                     "D_eff": D, "coherence": coh, "amplification": amp})
        print(f"dim={d} N={n**d:6d} D_eff={D:.3f} coh={coh:.3f} amp={amp:.2f}")

    with open(os.path.join(OUT_DIR, "dim_scan.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nD_eff: {[r['D_eff'] for r in rows]}")
    print(f"Coherence: {[r['coherence'] for r in rows]}")

    make_figure(rows)
    print(f"Wrote {OUT_DIR}")


def make_figure(rows):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    dims = [r["dim"] for r in rows]

    ax = axes[0]
    ax.plot(dims, [r["D_eff"] for r in rows], "o-", color="seagreen",
            lw=2, ms=8)
    ax.set_xlabel("spatial dimension")
    ax.set_ylabel(r"$D_{\rm eff}$")
    ax.set_title("A. Spectral dimension vs spatial dim")
    ax.set_xticks(dims)

    ax = axes[1]
    ax.plot(dims, [r["coherence"] for r in rows], "s-", color="crimson",
            lw=2, ms=8)
    ax.set_xlabel("spatial dimension")
    ax.set_ylabel("coherence")
    ax.set_title("B. Field coherence vs dimension")
    ax.set_xticks(dims)

    ax = axes[2]
    ax.plot(dims, [r["amplification"] for r in rows], "D-", color="steelblue",
            lw=2, ms=8)
    ax.set_xlabel("spatial dimension")
    ax.set_ylabel("amplification")
    ax.set_title("C. Amplification vs dimension")
    ax.set_xticks(dims)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "dim_amplification.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
