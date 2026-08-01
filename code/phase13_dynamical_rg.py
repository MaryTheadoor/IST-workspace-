"""
================================================================================
IST PHASE 13 - Dynamical RG: Golden-Cluster Blocking Under Temporal Evolution
================================================================================
Purpose:
    Replace static blocking (Phase 12) with emergent blocking: the Phase 11
    golden-filtered substrate evolves in time. At each RG epoch, golden-
    connected components (cells linked by edges with weight > 0.5) become
    coarse vertices. The Galerkin projection from the current effective
    Laplacian gives D_eff at that epoch. The RG flow is dynamical -- the
    golden attractor creates, merges, and splits clusters in real time.

    Hypothesis: as golden clusters crystallize under the temporal attractor,
    D_eff should converge toward a stable value (potentially phi) reflecting
    the golden-filtered connectivity structure.

Inputs:   none (uses Phase 11 KleinGoldenSubstrate)
Outputs:  code/outputs/phase13/dynamical_rg.csv
          code/outputs/phase13/dynamical_rg.png

References:
    code/phase11_golden_substrate.py   (golden-filtered Klein substrate)
    code/phase12_fibonacci_rg.py       (static RG baseline)
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components

from phase1_klein_laplacian import PHI
from phase7_vector_substrate import spectral_dimension
from phase11_golden_substrate import KleinGoldenSubstrate

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase13")


# ───────────────────────────────────────────────────────────────────────────────
# GOLDEN ADJACENCY & EFFECTIVE LAPLACIAN
# ───────────────────────────────────────────────────────────────────────────────

def golden_adjacency(sub):
    """Sparse binary adjacency of edges with golden weight > 0.5."""
    w_up, w_dn, w_r, w_l = sub._edge_weights()
    n = sub.n
    N = n * n
    rows, cols = [], []

    def idx(i, j):
        return j * n + i

    for j in range(n):
        for i in range(n):
            u = idx(i, j)
            if w_r[j, i] > 0.5:
                rows.append(u); cols.append(idx((i + 1) % n, j))
            if w_l[j, i] > 0.5:
                rows.append(u); cols.append(idx((i - 1) % n, j))
            if j < n - 1 and w_up[j, i] > 0.5:
                rows.append(u); cols.append(idx(i, j + 1))
            if j > 0 and w_dn[j, i] > 0.5:
                rows.append(u); cols.append(idx(i, j - 1))
            # twist seam
            if j == n - 1 and w_up[j, i] > 0.5:
                rows.append(u); cols.append(idx(n - 1 - i, 0))
            if j == 0 and w_dn[j, i] > 0.5:
                rows.append(u); cols.append(idx(n - 1 - i, n - 1))

    data = np.ones(len(rows))
    A = sp.csr_matrix((data, (rows, cols)), shape=(N, N))
    return A + A.T  # symmetrize


def effective_laplacian(sub):
    """Signed coupling matrix from current golden-filtered weights."""
    w_up, w_dn, w_r, w_l = sub._edge_weights()
    n = sub.n
    N = n * n
    rows, cols, vals = [], [], []

    def idx(i, j):
        return j * n + i

    g = sub.gain / 4.0
    for j in range(n):
        for i in range(n):
            u = idx(i, j)
            # right (periodic, +1)
            rows.append(u); cols.append(idx((i+1)%n, j)); vals.append(g*w_r[j,i])
            # left (periodic, +1)
            rows.append(u); cols.append(idx((i-1)%n, j)); vals.append(g*w_l[j,i])
            # up interior (+1)
            if j < n - 1:
                rows.append(u); cols.append(idx(i, j+1)); vals.append(g*w_up[j,i])
            # down interior (+1)
            if j > 0:
                rows.append(u); cols.append(idx(i, j-1)); vals.append(g*w_dn[j,i])
            # twist: bottom -> top, sign -1
            if j == n - 1:
                rows.append(u); cols.append(idx(n-1-i, 0))
                vals.append(-g * w_up[j, i])
            # twist: top -> bottom, sign -1
            if j == 0:
                rows.append(u); cols.append(idx(n-1-i, n-1))
                vals.append(-g * w_dn[j, i])

    W = sp.csr_matrix((vals, (rows, cols)), shape=(N, N))
    D = np.asarray(np.abs(W).sum(axis=1)).ravel()
    return sp.diags(D) - W


# ───────────────────────────────────────────────────────────────────────────────
# DYNAMICAL RG
# ───────────────────────────────────────────────────────────────────────────────

def dynamical_rg_epoch(sub):
    """Compute components from golden edges, build coarse Laplacian,
    measure D_eff. Returns metrics dict."""
    adj = golden_adjacency(sub)
    n_comp, labels = connected_components(adj, directed=False)

    N = sub.n * sub.n
    if n_comp <= 1 or n_comp >= N - 1:
        return {"n_coarse": n_comp, "D_eff": np.nan}

    # prolongation from label assignment
    P = sp.csr_matrix((np.ones(N), (np.arange(N), labels)),
                      shape=(N, n_comp))
    col_norm = np.sqrt(np.asarray(P.power(2).sum(axis=0)).ravel() + 1e-12)
    P = P @ sp.diags(1.0 / col_norm)

    L = effective_laplacian(sub)
    Lc = P.T @ L @ P
    D, r2 = spectral_dimension(Lc,
                               k=min(30, int(n_comp * 0.8) - 2))
    return {"n_coarse": n_comp, "D_eff": D, "r2": r2}


def run_dynamical_rg(sub, n_epochs=12, ticks_per_epoch=80):
    """Evolve substrate, measure D_eff at each epoch."""
    rows = []
    for epoch in range(n_epochs):
        sub.run(ticks_per_epoch, record_every=ticks_per_epoch + 1)
        meta = dynamical_rg_epoch(sub)
        meta["epoch"] = epoch + 1
        meta["total_tick"] = sub.step_count
        meta["golden_frac"] = sub.golden_fraction()
        rows.append(meta)
    return rows


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    sub = KleinGoldenSubstrate(n=64, noise_std=0.02, gain=3.0, seed=5)
    rows = run_dynamical_rg(sub, n_epochs=15, ticks_per_epoch=60)

    with open(os.path.join(OUT_DIR, "dynamical_rg.csv"), "w",
              newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("epoch  tick   n_coarse  golden_frac  D_eff")
    for r in rows:
        d = f"{r['D_eff']:.3f}" if not np.isnan(r["D_eff"]) else "nan"
        print(f"{r['epoch']:5d}  {r['total_tick']:5d}  {r['n_coarse']:8d}  "
              f"{r['golden_frac']:10.3f}  {d}")

    make_figure(rows)
    print(f"Wrote {OUT_DIR}")


def make_figure(rows):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    eps = [r["epoch"] for r in rows]
    Ds = [r["D_eff"] if not np.isnan(r["D_eff"]) else np.nan for r in rows]
    ns = [r["n_coarse"] for r in rows]
    gs = [r["golden_frac"] for r in rows]

    ax = axes[0, 0]
    ax.plot(eps, Ds, "o-", color="seagreen", lw=2, label=r"$D_{\rm eff}$")
    ax.axhline(PHI, color="crimson", ls="--", label=r"$\varphi$")
    ax.set_xlabel("RG epoch")
    ax.set_ylabel(r"$D_{\rm eff}$")
    ax.set_title("A. Dynamical RG: D_eff vs epoch")
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    ax.plot(eps, ns, "s-", color="steelblue", label="n_coarse")
    ax.set_xlabel("RG epoch")
    ax.set_ylabel("coarse vertices")
    ax.set_title("B. Golden-component count")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    ax.plot(eps, gs, "o-", color="crimson", lw=2, label="golden frac")
    ax.set_xlabel("RG epoch")
    ax.set_ylabel("fraction")
    ax.set_title("C. Golden edge fraction")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    valid = [(e, d) for e, d in zip(eps, Ds) if not np.isnan(d)]
    if valid:
        xe, ye = zip(*valid)
        ax.semilogy(xe, [abs(y - PHI) for y in ye], "o-",
                    color="crimson", lw=2, label=r"$|D_{\rm eff} - \varphi|$")
    ax.set_xlabel("RG epoch")
    ax.set_ylabel(r"$|D_{\rm eff} - \varphi|$")
    ax.set_title("D. Convergence toward phi")
    ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "dynamical_rg.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
