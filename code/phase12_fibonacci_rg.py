"""
================================================================================
IST PHASE 12 - Fibonacci RG: Self-Similar Decimation on the Golden Circle
================================================================================
Purpose:
    Test whether Fibonacci-scaled blocking on the golden-rotation-order
    (GRO) circle preserves spectral self-similarity under RG. The base
    graph is the Phase 7 spectral-proximity coupling on the GRO circle
    (D_eff ~ 1.1). Three blocking schemes are compared:
      * Fibonacci: GRO-consecutive blocks with phi-scaled sizes
      * Uniform: GRO-consecutive blocks with equal sizes
      * Random: random blocks (same number)

    The Fibonacci blocking should produce a coarse graph whose D_eff
    matches the fine graph (self-similar), while uniform/random blocking
    should drift — confirming that Fibonacci-preserved gap structure is
    the key to a stable RG attractor.

Inputs:   none
Outputs:  code/outputs/phase12/rg_fibonacci_comparison.csv
          code/outputs/phase12/rg_fibonacci.png

References:
    IST_Project_Implementation_Plan.md (Priority 3)
    code/phase7_vector_substrate.py (spectral-proximity graph)
    code/phase1_rg_flow.py          (2x2 RG baseline)
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
from phase7_vector_substrate import spectral_dimension

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase12")
ALPHA_GOLDEN = 1.0 / PHI ** 2


# ───────────────────────────────────────────────────────────────────────────────
# SPECTRAL-PROXIMITY GRAPH ON THE GRO CIRCLE
# ───────────────────────────────────────────────────────────────────────────────

def gro_phases(N):
    return 2 * np.pi * ((np.arange(N) * ALPHA_GOLDEN) % 1.0)


def gro_coupling(N, sigma=0.03):
    """Binary adjacency for the GRO circle: 1 if d < sigma else 0."""
    p = gro_phases(N)
    dmat = np.minimum(np.abs(p[:, None] - p[None, :]),
                      2 * np.pi - np.abs(p[:, None] - p[None, :]))
    J = (dmat < sigma).astype(float)
    np.fill_diagonal(J, 0.0)
    return J


def gro_laplacian(N, sigma=0.03):
    """Symmetric PSD Laplacian D - J for the GRO circle graph."""
    J = gro_coupling(N, sigma)
    D = np.asarray(J.sum(axis=1))
    return sp.diags(D) - sp.csr_matrix(J)


# ───────────────────────────────────────────────────────────────────────────────
# BLOCKING SCHEMES
# ───────────────────────────────────────────────────────────────────────────────

def fibonacci_blocking(N, n_coarse):
    """Two-size Fibonacci blocking: blocks of size a and b where a/b ~ phi,
    both close to N/n_coarse. The alternating sizes create Fibonacci-gap
    structure at the current RG scale without block-size explosion."""
    avg = N / n_coarse
    a = int(np.ceil(avg * PHI / (1 + PHI) * 2))  # ~ avg * 1.24
    b = max(round(a / PHI), 1)                    # ~ avg * 0.76
    # solve a*x + b*(n_coarse - x) == N
    x = (N - b * n_coarse) / (a - b)
    if x < 0 or x > n_coarse:
        a = max(round(avg * 1.3), 1)
        b = max(round(avg * 0.7), 1)
        x = (N - b * n_coarse) / (a - b)
        if x < 0 or x > n_coarse:
            # fallback: equal sizes with slight variation
            a, b = max(round(avg) + 1, 1), max(round(avg), 1)
            x = (N - b * n_coarse) / (a - b) if a != b else 0
    x = int(np.clip(round(x), 0, n_coarse))
    sizes = [a] * x + [b] * (n_coarse - x)
    sizes = np.maximum(sizes, 1)
    # adjust to exact sum
    while sum(sizes) > N:
        sizes[np.argmax(sizes)] -= 1
    while sum(sizes) < N:
        sizes[np.argmin(sizes)] += 1

    indices = np.arange(N)
    rows, cols, data = [], [], []
    idx = 0
    for b_idx, s in enumerate(sizes):
        for j in range(s):
            rows.append(indices[idx + j])
            cols.append(b_idx)
            data.append(1.0)
        idx += s
    P = sp.csr_matrix((data, (rows, cols)), shape=(N, n_coarse))
    col_norm = np.sqrt(np.asarray(P.power(2).sum(axis=0)).ravel() + 1e-12)
    return P @ sp.diags(1.0 / col_norm)


def uniform_blocking(N, n_coarse):
    """GRO-consecutive equal-size blocks."""
    base = N // n_coarse
    rem = N % n_coarse
    indices = np.arange(N)
    rows, cols, data = [], [], []
    idx = 0
    for b in range(n_coarse):
        sz = base + (1 if b < rem else 0)
        for j in range(sz):
            rows.append(indices[idx + j])
            cols.append(b)
            data.append(1.0)
        idx += sz
    P = sp.csr_matrix((data, (rows, cols)), shape=(N, n_coarse))
    col_norm = np.sqrt(np.asarray(P.power(2).sum(axis=0)).ravel() + 1e-12)
    return P @ sp.diags(1.0 / col_norm)


def random_blocking(N, n_coarse, seed=1):
    """Random block assignment (same n_coarse)."""
    rng = np.random.default_rng(seed)
    assignment = rng.choice(n_coarse, N)
    rows = np.arange(N)
    cols = assignment
    data = np.ones(N)
    P = sp.csr_matrix((data, (rows, cols)), shape=(N, n_coarse))
    col_norm = np.sqrt(np.asarray(P.power(2).sum(axis=0)).ravel() + 1e-12)
    return P @ sp.diags(1.0 / col_norm)


# ───────────────────────────────────────────────────────────────────────────────
# RG FLOW
# ───────────────────────────────────────────────────────────────────────────────

def run_scheme(L_0, N_0, scheme, n_levels=6, coarsen_factor=3):
    rows = []
    L = L_0.tocsr()
    N = N_0
    for level in range(n_levels + 1):
        D, _ = spectral_dimension(L, k=min(40, N - 2))
        rows.append({"scheme": scheme, "level": level, "N": N, "D_eff": D})
        if level == n_levels or N < coarsen_factor * 3:
            break
        n_c = max(round(N / coarsen_factor), 6)
        if scheme == "Fibonacci":
            P = fibonacci_blocking(N, n_c)
        elif scheme == "Uniform":
            P = uniform_blocking(N, n_c)
        else:
            P = random_blocking(N, n_c, seed=level)
        L = P.T @ L @ P
        N = n_c
    return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    N_start = 800
    L_0 = gro_laplacian(N_start, sigma=0.03)

    all_rows = []
    for scheme in ["Fibonacci", "Uniform", "Random"]:
        rows = run_scheme(L_0, N_start, scheme, n_levels=5)
        all_rows.extend(rows)
        valid = [r["D_eff"] for r in rows
                 if r["D_eff"] is not None and not np.isnan(float(r["D_eff"]))]
        print(f"{scheme:12s}: D_eff = {[round(d, 3) for d in valid]}")

    with open(os.path.join(OUT_DIR, "rg_fibonacci_comparison.csv"), "w",
              newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)

    make_figure(all_rows)
    print(f"Wrote {OUT_DIR}")


def make_figure(all_rows):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    colors = {"Fibonacci": "seagreen", "Uniform": "steelblue", "Random": "gray"}
    for scheme, ax, title in [
            ("Fibonacci", axes[0], "A. D_eff vs RG level"),
            ("Fibonacci", axes[1], "B. D_eff vs system size")]:
        for s in ["Fibonacci", "Uniform", "Random"]:
            pts = [(r["level"], r["D_eff"]) for r in all_rows
                   if r["scheme"] == s and not np.isnan(r["D_eff"])]
            if pts:
                xs, ys = zip(*pts)
                ax.plot(xs, ys, "o-", color=colors[s], label=s, lw=2)
        ax.axhline(PHI, color="crimson", ls="--", label=r"$\varphi$")
        ax.axhline(1.10, color="gray", ls=":", label="D ~ 1.1 (Phase 7)")
        ax.legend(fontsize=9)

    axes[0].set_xlabel("RG level")
    axes[0].set_ylabel(r"$D_{\rm eff}$")
    axes[1].set_xlabel("system size N")
    axes[1].set_ylabel(r"$D_{\rm eff}$")
    axes[1].set_xscale("log")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "rg_fibonacci.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
