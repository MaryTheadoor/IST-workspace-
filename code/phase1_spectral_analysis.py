
"""
================================================================================
IST PHASE 1.2 - Spectral Gap Analysis: Does the Gap Ratio Converge to phi?
================================================================================
Purpose:
    Sweep the discrete Klein bottle graph family G_n at n = 8..128, compute
    the low-lying spectrum of the topological Laplacian, and test the
    roadmap's key claim: that the dominant spectral gap ratio r* converges
    to the golden ratio phi under self-similar refinement (n -> 2n).

    Gap ratios are computed between DISTINCT eigenvalue levels (exact
    degeneracies clustered), per the plan's r_k = (l_{k+1} - l_k)/(l_k - l_{k-1}).
    An untwisted torus control is run alongside. Numerical spectra are
    validated against the closed-form analytic spectrum.

Inputs:   none (grid sizes hardcoded per plan: 8, 16, 32, 64, 128)
Outputs:
    code/outputs/phase1/eigenvalue_convergence.csv  - per-level eigenvalues,
        gaps, ratios for Klein and torus at every n
    code/outputs/phase1/spectral_gaps.png           - 4-panel summary (300 DPI)
    stdout summary table

References:
    notes/IST_Research_Plan_Phases_1-5.md   (Phase 1.2)
    code/phase1_klein_laplacian.py          (graph + Laplacian + spectra)

Note: the plan specifies outputs/phase1/; we follow the repo convention
code/outputs/phase1/ (all existing simulation outputs live in code/outputs/).
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from phase1_klein_laplacian import (
    PHI, build_klein_bottle_graph, build_torus_graph,
    laplacian_spectrum, analytic_klein_eigenvalues,
    distinct_eigenvalues, gap_ratios,
)

SIZES = [8, 16, 32, 64, 128]
N_EIGEN = 45          # raw eigenvalues per solve (clusters -> ~25-30 distinct)
N_LEVELS = 25         # distinct levels kept for CSV / gap statistics
OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase1")


def analyze(n):
    """Run the spectrum + gap-ratio analysis for one grid size n x n."""
    rows = []
    for topology, build in [("klein", build_klein_bottle_graph),
                            ("torus", build_torus_graph)]:
        g = build(n, n)
        vals = laplacian_spectrum(g.laplacian(), N_EIGEN)
        distinct = distinct_eigenvalues(vals)[:N_LEVELS]
        gaps, ratios = gap_ratios(distinct)
        scale = (n / np.pi) ** 2
        for k, lam in enumerate(distinct):
            rows.append({
                "topology": topology,
                "n_meridians": n,
                "n_longitudes": n,
                "level": k,
                "eigenvalue": lam,
                "scaled_eigenvalue": lam * scale,
                "gap": gaps[k - 1] if k >= 1 else "",
                "ratio": ratios[k - 2] if k >= 2 else "",
            })

    # Solver validation against the closed-form Klein spectrum
    g = build_klein_bottle_graph(n, n)
    vals = laplacian_spectrum(g.laplacian(), 20)
    analytic = analytic_klein_eigenvalues(n, n, 400)
    max_err = max(np.min(np.abs(analytic - v)) for v in vals)

    klein = [r for r in rows if r["topology"] == "klein"]
    torus = [r for r in rows if r["topology"] == "torus"]
    klein_ratios = np.array([r["ratio"] for r in klein if r["ratio"] != ""])
    summary = {
        "n": n,
        "lambda_min_klein": klein[0]["eigenvalue"],
        "lambda_min_klein_scaled": klein[0]["scaled_eigenvalue"],
        "lambda_1_torus_scaled": torus[1]["scaled_eigenvalue"],
        "n_distinct": len(klein),
        "median_ratio": float(np.median(klein_ratios)),
        "geomean_ratio": float(np.exp(np.mean(np.log(klein_ratios)))),
        "frac_near_phi": float(np.mean(np.abs(klein_ratios - PHI) < 0.05 * PHI)),
        "max_analytic_err": max_err,
    }
    return rows, summary


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    all_rows, summaries = [], []
    for n in SIZES:
        rows, summary = analyze(n)
        all_rows.extend(rows)
        summaries.append(summary)
        print(f"n={n:4d}  N={n*n:6d}  l_min={summary['lambda_min_klein']:.6f} "
              f"(scaled {summary['lambda_min_klein_scaled']:.4f})  "
              f"distinct={summary['n_distinct']:2d}  "
              f"median r={summary['median_ratio']:.4f}  "
              f"geomean r={summary['geomean_ratio']:.4f}  "
              f"P(|r-phi|<5%)={summary['frac_near_phi']:.2f}  "
              f"err={summary['max_analytic_err']:.2e}")

    csv_path = os.path.join(OUT_DIR, "eigenvalue_convergence.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"\nWrote {csv_path}")

    make_figure(all_rows, summaries)
    print(f"phi = {PHI:.15f}")


def make_figure(all_rows, summaries):
    klein = {n: [r for r in all_rows
                 if r["topology"] == "klein" and r["n_meridians"] == n]
             for n in SIZES}
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    cmap = plt.get_cmap("viridis")
    colors = {n: cmap(i / (len(SIZES) - 1)) for i, n in enumerate(SIZES)}

    # A: scaled eigenvalue ladder -> universal integers 4p^2 + l^2
    ax = axes[0, 0]
    integers = [1, 4, 5, 8, 9, 13, 16, 17, 20, 25]
    for y in integers:
        ax.axhline(y, color="0.85", lw=0.8, zorder=0)
    for n in SIZES:
        rows = klein[n][:12]
        ax.plot([r["level"] for r in rows],
                [r["scaled_eigenvalue"] for r in rows],
                "o-", ms=4, lw=1, color=colors[n], label=f"n={n}")
    ax.set_xlabel("distinct level $k$")
    ax.set_ylabel(r"$\lambda_k \,(n/\pi)^2$")
    ax.set_title("A. Scaled spectral ladder $\\to$ integers $4p^2+\\ell^2$")
    ax.legend(fontsize=8)

    # B: gap-ratio distribution at the finest resolution
    ax = axes[0, 1]
    ratios = [r["ratio"] for r in klein[SIZES[-1]] if r["ratio"] != ""]
    ax.hist(ratios, bins=np.linspace(0, 4, 33), color="steelblue",
            edgecolor="white")
    ax.axvline(PHI, color="crimson", lw=2, label=f"$\\varphi$ = {PHI:.4f}")
    ax.axvline(np.median(ratios), color="k", ls="--",
               label=f"median = {np.median(ratios):.4f}")
    ax.set_xlabel(r"gap ratio $r_k = g_k/g_{k-1}$")
    ax.set_ylabel("count")
    ax.set_title(f"B. Gap-ratio distribution (n={SIZES[-1]}, "
                 f"{len(ratios)} ratios)")
    ax.legend(fontsize=8)

    # C: convergence test — statistics of r* vs refinement level
    ax = axes[1, 0]
    ns = [s["n"] for s in summaries]
    ax.axhline(PHI, color="crimson", lw=1.5, ls="-", label="$\\varphi$")
    ax.axhspan(PHI * 0.95, PHI * 1.05, color="crimson", alpha=0.12)
    ax.plot(ns, [s["median_ratio"] for s in summaries], "o-",
            label="median $r^*$")
    ax.plot(ns, [s["geomean_ratio"] for s in summaries], "s--",
            label="geomean $r^*$")
    ax.set_xscale("log", base=2)
    ax.set_xticks(ns, [str(n) for n in ns])
    ax.set_xlabel("grid size $n$")
    ax.set_ylabel("gap-ratio statistic")
    ax.set_title("C. Does $r^* \\to \\varphi$ under refinement?")
    ax.legend(fontsize=8)

    # D: ground state scaling — twist halves the meridian momentum
    ax = axes[1, 1]
    ax.plot(ns, [s["lambda_min_klein_scaled"] for s in summaries], "o-",
            color="crimson", label=r"Klein $\lambda_0 (n/\pi)^2 \to 1$")
    ax.plot(ns, [s["lambda_1_torus_scaled"] for s in summaries], "s--",
            color="steelblue", label=r"torus $\lambda_1 (n/\pi)^2 \to 4$")
    ax.axhline(1.0, color="crimson", lw=0.8, alpha=0.4)
    ax.axhline(4.0, color="steelblue", lw=0.8, alpha=0.4)
    ax.set_xscale("log", base=2)
    ax.set_xticks(ns, [str(n) for n in ns])
    ax.set_xlabel("grid size $n$")
    ax.set_ylabel(r"scaled eigenvalue")
    ax.set_title("D. Twist opens gap: $\\lambda_0 = 4\\sin^2(\\pi/2n) > 0$")
    ax.legend(fontsize=8)

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "spectral_gaps.png")
    fig.savefig(path, dpi=300)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
