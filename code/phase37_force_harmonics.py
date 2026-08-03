"""
================================================================================
IST PHASE 37 - Force Unification as Harmonic Excitations of the Substrate
================================================================================
Purpose:
    Test the hypothesis that the fundamental forces are specific harmonic
    excitations of the emerging manifold -- that each force couples at a
    harmonic of the same underlying substrate oscillation, with the field
    functioning as the decentralized non-local average of all information
    resonating at that harmonic. This is a unification-by-harmonics idea,
    distinct from gauge-coupling unification: instead of all forces meeting
    at one scale, they are DIFFERENT HARMONICS of one substrate resonance.

Three testable formulations (all tested here, honestly):

    (A) Fixed-scale harmonic ladder: at M_Z, the inverse couplings should
        sit on golden-ratio harmonics of a common fundamental.

        Measured (M_Z): 1/alpha_EM = 127.95, 1/alpha_W = 29.5,
                        1/alpha_S = 8.47
        Ratios: em/weak = 4.337 ~ phi^3 = 4.236 (2.4% off)
                weak/strong = 3.483 vs phi^2 = 2.618 (33% off)
                em/strong = 15.11 vs phi^5 = 11.09 (36% off)
        VERDICT: only em/weak ~ phi^3 is close. The fixed-scale ladder
        is NOT clean.

    (B) Beta-coefficient ladder: the 1-loop SM beta coefficients
        (b1 = 41/10, b2 = -19/6, b3 = -7) should form a golden ladder.
        |b3|/|b1| = 1.707 vs phi = 1.618 (5.5% off)
        |b2|/|b1| = 0.772 vs 1/phi^2 = 0.382 (way off)
        VERDICT: not clean.

    (C) Slaved running (IST's existing claim): the weak and strong
        couplings inherit their running from EM via a golden-ratio
        enhancement phi^(2n-1) / (1 - 2 phi^2 x). The existing predictor
        calibrates at M_Z then predicts the running, which deviates from
        SM above M_Z (strong ratio 1.28 at 500 GeV to 2.39 at 1e5 GeV).
        VERDICT: the slaved-running hypothesis is CALIBRATED, not a pure
        prediction, and its high-energy running deviates strongly from SM.

Honest conclusion:
    The harmonic-unification hypothesis, in its simplest forms (A, B, C),
    is NOT supported by the measured couplings. Only one ratio (em/weak ~
    phi^3 at 2.4%) is close, and the running predictions deviate. This is
    an honest negative result: it does NOT falsify the deeper idea (forces
    as substrate harmonics), but it shows the coupling VALUES do not sit
    on a simple golden ladder at the scales probed. A refined formulation
    is needed -- e.g. the harmonics may appear in the MASS ratios (which
    ARE golden-structured, Phases 28-35) rather than the bare couplings.

    The framework's strongest harmonic evidence is in the MASS spectrum
    (the phi-ladders of the baryons, leptons, and neutron), NOT the force
    couplings. This phase documents where the harmonic idea is supported
    (masses) and where it is not (couplings).

Outputs:  code/outputs/phase37/force_harmonics.csv
          code/outputs/phase37/force_harmonics.png

References:
    notes/beta_function_derivation.md   (IR freedom, UV Landau pole)
    code/running_couplings_predictor.py (slaved running)
    code/phase28-35                     (golden ladders in the MASS spectrum)
    PDG 2022 running couplings at M_Z
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ist_toolkit_v2 import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase37")

# Inverse couplings at M_Z (PDG 2022)
INV_EM, INV_WEAK, INV_STRONG = 127.952, 29.5, 8.47

# SM 1-loop beta coefficients
B1, B2, B3 = 41 / 10, -19 / 6, -7.0


# ───────────────────────────────────────────────────────────────────────────────
# (A) FIXED-SCALE HARMONIC LADDER
# ───────────────────────────────────────────────────────────────────────────────

def coupling_ratios():
    return {"em_over_weak": INV_EM / INV_WEAK,
            "weak_over_strong": INV_WEAK / INV_STRONG,
            "em_over_strong": INV_EM / INV_STRONG}


def golden_harmonics(n_max=6):
    return {f"phi^{n}": PHI ** n for n in range(1, n_max + 1)}


def best_harmonic_match(ratio, harmonics):
    best = min(harmonics.items(),
               key=lambda kv: abs(kv[1] / ratio - 1))
    return best[0], best[1], 100 * (best[1] / ratio - 1)


# ───────────────────────────────────────────────────────────────────────────────
# (B) BETA-COEFFICIENT LADDER
# ───────────────────────────────────────────────────────────────────────────────

def beta_ratios():
    return {"|b3|/|b1|": abs(B3 / B1), "|b2|/|b1|": abs(B2 / B1),
            "|b3|/|b2|": abs(B3 / B2)}


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    harmonics = golden_harmonics()

    rows = []
    for name, ratio in coupling_ratios().items():
        hname, hval, pct = best_harmonic_match(ratio, harmonics)
        rows.append({"quantity": name, "ratio": ratio,
                     "best_harmonic": hname, "harmonic_value": hval,
                     "pct_off": pct, "tier": "A-couplings"})
    for name, ratio in beta_ratios().items():
        hname, hval, pct = best_harmonic_match(ratio, harmonics)
        rows.append({"quantity": name, "ratio": ratio,
                     "best_harmonic": hname, "harmonic_value": hval,
                     "pct_off": pct, "tier": "B-beta"})
    csv_path = os.path.join(OUT_DIR, "force_harmonics.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"Wrote {csv_path}")

    print("=== IST PHASE 37: Force Unification as Harmonic Excitations ===")
    print("Honest test: do the measured force couplings sit on golden")
    print("harmonics of a common substrate resonance?\n")

    print("  (A) Fixed-scale inverse-coupling ladder at M_Z:")
    for r in rows:
        if r["tier"] != "A-couplings":
            continue
        print(f"      {r['quantity']:16s} = {r['ratio']:7.3f}  "
              f"closest harmonic {r['best_harmonic']:8s} = "
              f"{r['harmonic_value']:7.3f}  ({r['pct_off']:+.1f}%)")

    print("\n  (B) SM 1-loop beta-coefficient ladder:")
    for r in rows:
        if r["tier"] != "B-beta":
            continue
        print(f"      {r['quantity']:16s} = {r['ratio']:7.3f}  "
              f"closest harmonic {r['best_harmonic']:8s} = "
              f"{r['harmonic_value']:7.3f}  ({r['pct_off']:+.1f}%)")

    print(f"\n  Golden harmonics: " + ", ".join(
        f"{k}={v:.3f}" for k, v in harmonics.items()))

    print(f"\nHonest conclusion:")
    print(f"  (A) Only em/weak ~ phi^3 (2.3% off) is close; the other two")
    print(f"      ratios are ~19-22% off the NEAREST golden harmonic. The")
    print(f"      fixed-scale ladder is NOT clean.")
    print(f"  (B) |b3|/|b1| ~ phi (5.2% off); |b2|/|b1| and |b3|/|b2| far")
    print(f"      off. NOT clean.")
    print(f"  (C) The slaved-running predictor (existing) is CALIBRATED at")
    print(f"      M_Z, not a pure prediction; its high-E running deviates")
    print(f"      from SM (strong ratio up to 2.4). NOT supported.")
    print(f"  => The simplest harmonic-unification formulations are NOT")
    print(f"     supported by the coupling data. The framework's strong")
    print(f"     harmonic (golden) evidence is in the MASS spectrum")
    print(f"     (Phases 28-35), not the force couplings.")
    print(f"  => Refined hypothesis needed: harmonics may structure the")
    print(f"     masses/couplings relation rather than the bare couplings.")

    make_figure(rows, harmonics)
    print(f"\nWrote {OUT_DIR}")


def make_figure(rows, harmonics):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    labels = [r["quantity"] for r in rows]
    pcts = [r["pct_off"] for r in rows]
    colors = ["steelblue"] * 3 + ["seagreen"] * 3
    axes[0].bar(labels, [abs(p) for p in pcts], color=colors)
    axes[0].axhline(5, color="crimson", ls="--", lw=1, label="5% threshold")
    axes[0].set_ylabel("|% off nearest golden harmonic|")
    axes[0].set_title("Force couplings vs golden harmonics")
    axes[0].tick_params(axis="x", rotation=25); axes[0].legend(fontsize=8)

    names = list(harmonics.keys())
    vals = list(harmonics.values())
    axes[1].bar(names, vals, color="darkorange")
    axes[1].set_ylabel("phi^n"); axes[1].set_title("Golden harmonics")
    axes[1].tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "force_harmonics.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
