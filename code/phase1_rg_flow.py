
"""
================================================================================
IST PHASE 1.3 - Renormalization-Group Flow on the Graph Laplacian
================================================================================
Purpose:
    Implement block-spin (Galerkin) coarse-graining of the discrete Klein
    bottle / torus graph Laplacian, extract the effective spectral dimension
    D_eff at each scale from the low-energy density of states, and compare
    the observed RG trajectory to the Solis phenomenological beta function
    beta(D) = -(1/phi^2)(D - phi) used elsewhere in the IST toolkit.

Inputs:   none (start grid n_start = 128, block factor b = 2)
Outputs:
    code/outputs/phase1/rg_trajectory.csv   - per-level D_eff and beta
    code/outputs/phase1/rg_trajectory.png   - 4-panel summary (300 DPI)

References:
    notes/IST_Research_Plan_Phases_1-5.md   (Phase 1.3)
    code/phase1_klein_laplacian.py          (graph + Laplacian)
    code/ist_toolkit_v2.py                  (RGFlowSimulator beta function)
    main/ist_v5_3_topology_substrate.md     (Solis fixed-point reference)

Limitations:
      The 2x2 block-spin coarse-graining is a raster RG -- it assumes
      geometric locality of the raster grid and partitions it into
      uniform blocks. The correct RG for a vector-encoded substrate is
      spectral: project the Laplacian onto its low-energy eigenspace
      rather than onto spatial cells. See
      notes/discrete_substrate_not_raster.md.

Conventions:
    * RG time t = ln(mu_0 / mu) = level * ln b, with b = 2 for 2x2 blocking.
      t = 0 is the UV (fine grid), t increasing toward the IR (coarse grid).
    * D_eff is extracted from the low-energy Weyl fit
          N(lambda) ~ C lambda^{D_eff/2}
      over a sliding window of the sorted positive eigenvalues.
    * The coarse operator L' = P^T L P is the Galerkin projection with
      piecewise-constant prolongation P (2x2 blocks). It preserves the
      topological zero-mode structure: torus stays massless, Klein stays
      massive because no constant section exists on a twisted bundle.
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

from phase1_klein_laplacian import (
    PHI, build_klein_bottle_graph, build_torus_graph
)

BLOCK = 2
N_START = 128
N_LEVELS = 5          # 128 -> 64 -> 32 -> 16 -> 8
OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase1")


def block_prolongation(n_mer, n_lon):
    """Piecewise-constant prolongation P: N_fine x N_coarse.

    Each 2x2 block of fine vertices maps to one coarse vertex.
    Requires n_mer and n_lon to be even.
    """
    if n_mer % BLOCK or n_lon % BLOCK:
        raise ValueError("grid dimensions must be divisible by block size 2")
    N_fine = n_mer * n_lon
    n_cm, n_cl = n_mer // BLOCK, n_lon // BLOCK
    N_coarse = n_cm * n_cl

    rows, cols, data = [], [], []
    for j in range(n_mer):
        for i in range(n_lon):
            fine = j * n_lon + i
            coarse = (j // BLOCK) * n_cl + (i // BLOCK)
            rows.append(fine)
            cols.append(coarse)
            data.append(1.0)
    P = sp.csr_matrix((data, (rows, cols)), shape=(N_fine, N_coarse))
    return P, (n_cm, n_cl)


def coarsen_laplacian(L, n_mer, n_lon):
    """Galerkin coarse-graining: L' = P^T L P."""
    P, (n_cm, n_cl) = block_prolongation(n_mer, n_lon)
    Lc = P.T @ L @ P
    return Lc, n_cm, n_cl


def rg_flow_laplacians(n_start=N_START, n_levels=N_LEVELS, twisted=True):
    """Generate a sequence of Laplacians under repeated 2x2 blocking.

    Returns a list of dicts with keys: level, n_mer, n_lon, N, L, scale.
    """
    build = build_klein_bottle_graph if twisted else build_torus_graph
    n = n_start
    levels = []
    L = build(n, n).laplacian()
    for level in range(n_levels):
        levels.append({
            "level": level,
            "n_mer": n,
            "n_lon": n,
            "N": n * n,
            "L": L,
            "scale": BLOCK ** level,          # length-scale factor
        })
        if level == n_levels - 1:
            break
        L, n, _ = coarsen_laplacian(L, n, n)
    return levels


def smallest_eigenvalues(L, k):
    """Return sorted smallest k positive eigenvalues of symmetric L."""
    N = L.shape[0]
    k = min(k, N - 2)
    if N <= 1000:
        vals = np.linalg.eigh(L.toarray())[0]
    else:
        vals = spla.eigsh(L, k=k, sigma=-1e-6, which="LM", tol=1e-12,
                          return_eigenvectors=False)
    vals = np.sort(vals)
    return vals[vals > 1e-10]  # drop zero modes (torus)


def spectral_dimension(L, window_low=0.05, window_high=0.5, k=200):
    """Fit D_eff from low-energy Weyl law N(lambda) ~ C lambda^{D_eff/2}.

    Uses eigenvalues window_low .. window_high of the available positive
    spectrum. Returns D_eff, R^2 of the log-log fit, and the fitted slope.
    """
    vals = smallest_eigenvalues(L, k)
    if len(vals) < 20:
        # For very small graphs use the full positive spectrum
        i_min = 1
        i_max = len(vals)
    else:
        i_min = max(1, int(window_low * len(vals)))
        i_max = max(i_min + 5, int(window_high * len(vals)))

    lam = vals[i_min:i_max]
    N = np.arange(i_min + 1, i_max + 1)  # counting index, 1-based
    x = np.log(lam)
    y = np.log(N)
    slope, intercept = np.polyfit(x, y, 1)
    y_fit = slope * x + intercept
    ss_res = np.sum((y - y_fit) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return 2.0 * slope, r2, slope, intercept


def solis_beta(D):
    """Phenomenological beta function beta(D) = -(1/phi^2)(D - phi)."""
    return -(1.0 / PHI ** 2) * (D - PHI)


def solis_flow(D0, t):
    """Analytic solution of dD/dt = solis_beta(D)."""
    return PHI + (D0 - PHI) * np.exp(-t / PHI ** 2)


def estimate_beta(Ds):
    """Finite-difference beta from observed D sequence.

    dt = ln(BLOCK) between 2x2 blocking steps.
    """
    dt = np.log(BLOCK)
    beta = np.diff(Ds) / dt
    D_mid = 0.5 * (Ds[:-1] + Ds[1:])
    return D_mid, beta


def run(twisted=True):
    """Execute the RG flow analysis for one topology."""
    levels = rg_flow_laplacians(twisted=twisted)
    name = "klein" if twisted else "torus"
    rows = []
    Ds = []
    for lvl in levels:
        D, r2, slope, intercept = spectral_dimension(lvl["L"])
        Ds.append(D)
        rows.append({
            "topology": name,
            "level": lvl["level"],
            "n": lvl["n_mer"],
            "N": lvl["N"],
            "t": lvl["level"] * np.log(BLOCK),
            "D_eff": D,
            "r2": r2,
            "weyl_slope": slope,
        })

    D_mid, beta_obs = estimate_beta(np.array(Ds))
    for i, row in enumerate(rows):
        row["beta_obs"] = beta_obs[i] if i < len(beta_obs) else ""
    return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    all_rows = run(twisted=True) + run(twisted=False)
    csv_path = os.path.join(OUT_DIR, "rg_trajectory.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"Wrote {csv_path}")

    # Print summary tables
    for topology in ["klein", "torus"]:
        rows = [r for r in all_rows if r["topology"] == topology]
        Ds = np.array([r["D_eff"] for r in rows])
        ts = np.array([r["t"] for r in rows])
        D_mid, beta_obs = estimate_beta(Ds)
        print(f"\n{topology.upper()} RG flow:")
        print(f"  level |   n  |     N |    t   | D_eff |   R^2  | beta_obs")
        for i, r in enumerate(rows):
            b = beta_obs[i] if i < len(beta_obs) else np.nan
            print(f"    {r['level']:2d}  | {r['n']:4d} | {r['N']:5d} | "
                  f"{r['t']:.4f} | {r['D_eff']:.4f} | {r['r2']:.4f} | {b:+.4f}")

    make_figure(all_rows)


def make_figure(all_rows):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    for topology, color in [("klein", "crimson"), ("torus", "steelblue")]:
        rows = [r for r in all_rows if r["topology"] == topology]
        ts = np.array([r["t"] for r in rows])
        Ds = np.array([r["D_eff"] for r in rows])
        label = "Klein bottle" if topology == "klein" else "Torus control"

        # A: D_eff vs RG time + Solis prediction from observed UV
        ax = axes[0, 0]
        ax.plot(ts, Ds, "o-", color=color, label=label)
        t_fine = np.linspace(0, ts.max(), 200)
        ax.plot(t_fine, solis_flow(Ds[0], t_fine), "--", color=color,
                alpha=0.6, label=f"Solis fit ({topology})")
        ax.axhline(PHI, color="k", ls=":", lw=1.2, label=f"$\\varphi$" if topology == "klein" else "")

        # B: observed beta vs D + Solis line
        ax = axes[0, 1]
        D_mid, beta_obs = estimate_beta(Ds)
        ax.plot(D_mid, beta_obs, "o-", color=color, label=label)

        # C: residual D - phi
        ax = axes[1, 0]
        ax.semilogy(ts, np.abs(Ds - PHI), "o-", color=color, label=label)

        # D: Weyl scaling at the finest level only
        ax = axes[1, 1]
        if topology == "klein":
            L0 = rg_flow_laplacians(twisted=True, n_levels=1)[0]["L"]
            vals = smallest_eigenvalues(L0, 200)
            i_min, i_max = int(0.05 * len(vals)), int(0.5 * len(vals))
            lam, N = vals[i_min:i_max], np.arange(i_min + 1, i_max + 1)
            ax.loglog(lam, N, "o", ms=3, color=color, label="Klein n=128")
            slope, intercept = np.polyfit(np.log(lam), np.log(N), 1)
            ax.loglog(lam, np.exp(intercept) * lam ** slope, "-",
                      color=color, label=f"fit D={2*slope:.3f}")

    ax = axes[0, 0]
    ax.set_xlabel(r"RG time $t = \ln(\mu_0/\mu)$")
    ax.set_ylabel(r"effective dimension $D_{\rm eff}$")
    ax.set_title("A. RG flow of spectral dimension")
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    D_grid = np.linspace(1.0, 3.0, 200)
    ax.plot(D_grid, solis_beta(D_grid), "k--", label=r"Solis: $\beta(D)=-(D-\varphi)/\varphi^2$")
    ax.axvline(PHI, color="k", ls=":", alpha=0.5)
    ax.axhline(0, color="k", ls="-", alpha=0.3)
    ax.set_xlabel(r"$D$")
    ax.set_ylabel(r"$\beta(D)$")
    ax.set_title("B. Observed beta function vs Solis target")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    ax.set_xlabel(r"RG time $t$")
    ax.set_ylabel(r"$|D_{\rm eff} - \varphi|$")
    ax.set_title("C. Distance to golden-ratio fixed point")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    ax.set_xlabel(r"eigenvalue $\lambda$")
    ax.set_ylabel(r"counting function $N(\lambda)$")
    ax.set_title("D. Low-energy Weyl scaling (finest Klein grid)")
    ax.legend(fontsize=8)

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "rg_trajectory.png")
    fig.savefig(path, dpi=300)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
