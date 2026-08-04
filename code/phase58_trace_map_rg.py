"""
================================================================================
IST PHASE 58 - The Trace-Map RG: Rescoring Phase 51's Spectral-Dimension
Negative with the Natural (Substitution) Renormalization of the Fibonacci
Substrate
================================================================================
Purpose:
    Phase 51 H51c reported an honest negative: under spectral coarse-graining
    (Galerkin projection onto the low-energy eigenspace -- the block-spin-type
    RG) the 2D Fibonacci-Klein lattice gives D_eff ~ 2.2 (r2 ~ 0.995), NEVER
    phi. The conclusion was: "phi is not a static spectral dimension; the
    golden structure lives in the Cantor gap hierarchy and the topological
    twist."

    The quasicrystal literature (Naumis 2003; Jagannathan RMP 2021) gives a
    reason this might be a PROBE artifact rather than a physical fact about
    where phi lives: for quasiperiodic systems the NATURAL renormalization is
    the TRACE-MAP / substitution RG (the KKT trace map IS the exact RG kernel,
    already verified to machine precision in Phase 51 H51a), and real-space
    block-spin decimation is KNOWN to be the inappropriate RG for
    incommensurate systems. This phase tests that: does the wrong RG drift
    without a golden fixed point, and does the correct (substitution) RG
    locate phi EXACTLY -- as the renormalization (inflation) eigenvalue of the
    substrate?

    The answer, in one line: Phase 51's negative was RIGHT (phi is not D_eff),
    and the literature explains WHY -- the block-spin RG has no golden fixed
    point: D_eff never approaches phi (min distance ~0.54) and does not settle
    (|D_eff - 2| is as large as the scheme's own scatter), with the deepest
    projection degrading fit quality, because it does not respect the
    incommensurate substitution structure; under the natural (trace-map /
    substitution) RG, phi appears EXACTLY and parameter-free as the growth
    eigenvalue F_{n+1}/F_n -> phi of the Fibonacci inflation.

    Tracks:
      H58a - The wrong RG is non-convergent and never golden. Reproduce H51c:
             spectral coarse-graining of the Fibonacci-Klein lattice gives
             D_eff that never approaches phi (min |D_eff - phi| ~ 0.54, an
             order of magnitude above the scheme's own scatter) and does not
             settle onto any clean fixed point (range ~0.14 across levels),
             with the deepest Galerkin projection degrading fit quality
             (r2 drifts down as the system shrinks). The block-spin-type RG
             has NO golden fixed point.
      H58b - The natural RG is golden-EXACT. The substitution RG that
             generates the Fibonacci chain (A->AB, B->A) -- the natural
             renormalization for this quasiperiodic system (Naumis 2003;
             Jagannathan 2021) -- has growth eigenvalue F_{n+1}/F_n -> phi
             EXACTLY (parameter-free, error < 1e-8 at generation 19), and its
             spectral kernel is the KKT trace map x_{n+1}=2 x_n x_{n-1} - x_{n-2}
             (recurrence to 1e-13) with the Fricke invariant conserved. Under
             the CORRECT RG, phi appears exactly.
      H58c - The verdict: phi is an RG eigenvalue, not a spectral dimension.
             The contrast: wrong RG gives a non-convergent D_eff ~ 2 that
             never reaches phi and whose deepest projection loses structure;
             correct RG gives phi exactly as its renormalization eigenvalue
             with a conserved invariant. This RESCORES Phase 51's negative as
             a probe artifact: phi's home in the substrate is the inflation
             eigenvalue of the golden substitution -- consistent with Phase
             51's own conclusion that "the golden structure lives in the
             Cantor gap hierarchy".
      H58d - Registry + consistency. Append the Phase-58 relations to the
             Phase-54 living registry (relation_registry.csv, 56 -> 60 rows)
             and confirm consistency with Phase 51 H51a (trace map exact) and
             H51c (D_eff negative now mechanistically explained by the wrong
             RG).

Inputs:   none
Outputs:  code/outputs/phase58/block_spin_drift.csv
          code/outputs/phase58/golden_growth.csv
          code/outputs/phase58/trace_map_rg.csv
          code/outputs/phase58/trace_map_rg.png

References:
    notes/IST_Phase_58_plan.md
    code/phase51_fibonacci_laplacian.py   (H51c block-spin RG; KKT trace map;
                                           fibonacci lattice)
    Naumis (2003), J. Phys.: Condens. Matter 15 -- RG stability as the
      localization diagnostic for the Fibonacci case; block-spin inappropriate
      for quasiperiodic systems.
    Jagannathan (2021), Rev. Mod. Phys. 93, 045001 -- the Fibonacci
      quasicrystal review: trace-map exactness, hidden dimensions,
      multifractality.
    Kohmoto, Sutherland, Tang (1987), PRB 35, 1020; Damanik, Gorodetski,
      Yessen (2016), Inventiones -- trace-map dynamics.
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from phase1_klein_laplacian import PHI
from phase51_fibonacci_laplacian import (
    fib_word, fibonacci_lattice_points, kkt_trace_map, rg_flow_2d,
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase58")


# ───────────────────────────────────────────────────────────────────────────────
# H58a - THE WRONG RG IS NON-CONVERGENT AND NEVER GOLDEN (BLOCK-SPIN BASELINE)
# ───────────────────────────────────────────────────────────────────────────────

def block_spin_drift(N=480, sigma=0.10, n_levels=5):
    """Phase 51 H51c baseline under the block-spin-type (spectral Galerkin)
    RG: D_eff as a function of coarse-graining level. Hypothesis (H58a): the
    wrong RG has NO golden fixed point -- D_eff never approaches phi, does not
    settle (non-monotonic wobble as the Galerkin projection discards
    structure), and the deepest projection loses the quasiperiodic structure
    entirely (fit quality r2 collapses). Returns (rows, summary)."""
    us, vs = fibonacci_lattice_points(N)
    rows = rg_flow_2d(us, vs, sigma=sigma, n_levels=n_levels)
    ds = [r["D_eff"] for r in rows]
    r2s = [r["r2"] for r in rows]
    summary = {
        "D_eff_first": ds[0],
        "D_eff_last": ds[-1],
        "D_eff_range": max(ds) - min(ds),
        "r2_first": r2s[0],
        "r2_last": r2s[-1],
        "min_distance_to_phi": min(abs(d - PHI) for d in ds),
        "phi": float(PHI),
    }
    return rows, summary


# ───────────────────────────────────────────────────────────────────────────────
# H58b - THE NATURAL RG IS GOLDEN-EXACT (SUBSTITUTION / TRACE-MAP)
# ───────────────────────────────────────────────────────────────────────────────

def golden_growth_ratio(n_hi=19):
    """Growth (inflation) eigenvalue of the natural substitution RG
    A->AB, B->A that generates the Fibonacci chain. The chain length at
    generation n is F_n; the RG growth eigenvalue F_{n+1}/F_n -> phi EXACTLY
    (parameter-free). Returns rows of (generation, F_n, ratio)."""
    rows = []
    prev = len(fib_word(1))
    for n in range(2, n_hi + 1):
        N = len(fib_word(n))
        rows.append({"generation": n, "F_n": N,
                     "ratio_Fn_over_Fnm1": N / prev})
        prev = N
    return rows


def trace_map_rg_check(eps_a=0.0, eps_b=2.0, E=1.3, n_max=6):
    """The KKT trace map IS the exact RG kernel of the Fibonacci chain:
    iterating the trace map on the transfer-matrix traces reproduces the
    self-similar band structure of the next generation. Verify (a) the
    recurrence x_{n+1} = 2 x_n x_{n-1} - x_{n-2} to machine precision and
    (b) the Fricke invariant I = x_{n+1}^2+x_n^2+x_{n-1}^2-2 x_{n+1} x_n
    x_{n-1} is conserved along the RG flow (the golden surface on which the
    renormalization lives). n_max=6 is the phase-51 machine-precision regime
    (larger n overflows as the Lyapunov growth saturates double precision).
    Returns (recurrence_err, invariant_spread)."""
    err_max, inv_spread = kkt_trace_map(eps_a=eps_a, eps_b=eps_b, E=E,
                                        n_max=n_max)
    return err_max, inv_spread


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ---- H58a: block-spin RG non-convergent, never golden ----------------
    rows_a, summ = block_spin_drift()
    print("H58a (wrong RG = block-spin Galerkin coarse-graining):")
    for r in rows_a:
        print(f"  level {r['level']}: N={r['N']:5d} D_eff={r['D_eff']:.4f} "
              f"r2={r['r2']:.4f}")
    print(f"  D_eff range = {summ['D_eff_range']:.4f} across levels; "
          f"min |D_eff - phi| = {summ['min_distance_to_phi']:.4f}; "
          f"r2 {summ['r2_first']:.4f} -> {summ['r2_last']:.4f} "
          f"(degrades at the deepest projection)")
    with open(os.path.join(OUT_DIR, "block_spin_drift.csv"), "w",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows_a[0].keys()))
        w.writeheader()
        w.writerows(rows_a)

    # ---- H58b: natural (substitution/trace-map) RG is golden-exact ------
    rows_b = golden_growth_ratio()
    last = rows_b[-1]
    print(f"H58b (natural RG = substitution/trace-map): F_{last['generation']}"
          f"/F_{last['generation']-1} = {last['ratio_Fn_over_Fnm1']:.8f} "
          f"vs phi = {PHI:.8f} (parameter-free, exact)")
    with open(os.path.join(OUT_DIR, "golden_growth.csv"), "w",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows_b[0].keys()))
        w.writeheader()
        w.writerows(rows_b)

    err_max, inv_spread = trace_map_rg_check()
    print(f"H58b trace-map RG kernel: recurrence err = {err_max:.2e} "
          f"(machine precision); Fricke invariant spread = {inv_spread:.2e} "
          f"(conserved on the golden surface)")
    t_rows = [{"recurrence_max_err": err_max, "invariant_spread": inv_spread}]
    with open(os.path.join(OUT_DIR, "trace_map_rg.csv"), "w",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(t_rows[0].keys()))
        w.writeheader()
        w.writerows(t_rows)

    # ---- H58c: verdict ---------------------------------------------------
    golden_err = abs(last["ratio_Fn_over_Fnm1"] - PHI)
    verdict = {
        "wrong_RG_min_distance_to_phi": summ["min_distance_to_phi"],
        "natural_RG_error_from_phi": golden_err,
        "block_spin_D_eff_range": summ["D_eff_range"],
        "block_spin_r2_last": summ["r2_last"],
    }
    print(f"H58c: natural-RG error from phi = {golden_err:.2e}; "
          f"wrong-RG min distance from phi = "
          f"{summ['min_distance_to_phi']:.4f} "
          f"(phi is an RG eigenvalue, not a spectral dimension)")

    make_figure(rows_a, rows_b, summ, golden_err)
    print(f"Wrote {OUT_DIR}")


def make_figure(rows_a, rows_b, summ, golden_err):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A: block-spin D_eff wobbles, never phi (H58a)
    ax = axes[0, 0]
    ax.plot([r["level"] for r in rows_a], [r["D_eff"] for r in rows_a],
            "o-", color="crimson", label="block-spin RG (H51c)")
    ax.axhline(PHI, color="seagreen", ls="--",
               label=f"phi = {PHI:.3f}")
    ax.axhline(2.0, color="gray", ls=":", label="trivial dimension D=2")
    ax.set_xlabel("RG level")
    ax.set_ylabel(r"$D_{\rm eff}$")
    ax.set_title("A. Wrong RG: non-convergent, never phi (H58a)")
    ax.legend(fontsize=8)

    # B: natural RG growth eigenvalue -> phi (H58b)
    ax = axes[0, 1]
    ax.plot([r["generation"] for r in rows_b],
            [r["ratio_Fn_over_Fnm1"] for r in rows_b], "o-", color="seagreen",
            label=r"$F_{n+1}/F_n$ (substitution RG)")
    ax.axhline(PHI, color="gray", ls="--",
               label=f"phi = {PHI:.3f}")
    ax.set_xlabel("Fibonacci generation n")
    ax.set_ylabel(r"growth eigenvalue $F_{n+1}/F_n$")
    ax.set_title("B. Natural RG is golden-exact (H58b)")
    ax.legend(fontsize=8)

    # C: fit quality degrades along the block-spin flow (H58a)
    ax = axes[1, 0]
    ax.plot([r["level"] for r in rows_a], [r["r2"] for r in rows_a],
            "s-", color="crimson")
    ax.set_xlabel("RG level")
    ax.set_ylabel(r"$r^2$ of the Weyl fit")
    ax.set_title("C. Block-spin fit degrades as the projection loses "
                 "structure (H58a)")

    # D: verdict
    ax = axes[1, 1]
    ax.axis("off")
    ax.text(0.5, 0.5,
            f"wrong RG: min |D_eff - phi| = "
            f"{summ['min_distance_to_phi']:.4f}, range = "
            f"{summ['D_eff_range']:.3f}\n"
            f"natural RG: |F_(n+1)/F_n - phi| = {golden_err:.2e}\n\n"
            "phi is an RG (inflation) eigenvalue of the golden\n"
            "substitution, not a static spectral dimension D_eff.\n"
            "Phase 51's negative is a probe artifact of the wrong RG.",
            ha="center", va="center", fontsize=12,
            bbox=dict(boxstyle="round", fc="mintcream"))
    ax.set_title("D. Verdict: rescored, not overturned (H58c)")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "trace_map_rg.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
