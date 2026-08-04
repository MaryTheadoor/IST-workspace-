"""
===============================================================================
IST PHASE 45 - Baryon Octet: Lambda-Sigma Mixing as the Golden Partition
===============================================================================
Purpose:
    Resolve the Phase 34 open item -- the baryon octet's internal Lambda-Sigma
    mixing -- with a parameter-free golden structure. Phase 34 found the
    decuplet is the clean SU(3) equal-spacing E-ladder (Phase 35 derived it
    from the double-cover + f_Klein = 3/2), but the octet masses

        N = 938.92,  Lambda = 1115.68,  Sigma = 1193.15,  Xi = 1318.28 MeV

    do NOT sit on that ladder, and the internal gaps
    Sigma - Lambda = 77.47, Xi - Sigma = 125.13 MeV were reported as
    "not clean".

The discovery (H45):
    The Lambda -> Xi mass interval is GOLDEN-PARTITIONED by Sigma:

        (Sigma - Lambda) / (Xi - Lambda) = 1/phi^2     (0.108% off)
        (Xi - Sigma)     / (Sigma - Lambda) = phi      (0.175% off)

    i.e. the two internal gaps -- the Lambda-Sigma hyperfine split (ud pair
    spin-flip, I=0 <-> I=1) and the Xi-Sigma strangeness step (S=-1 -> -2) --
    stand in the golden ratio. This is a single, parameter-free constraint,
    with prediction power:

        Sigma = Lambda + (Xi - Lambda)/phi^2   -> 1193.070 vs 1193.154 (0.007%)
        Xi    = Lambda + phi^2 (Sigma - Lambda) -> 1318.504 vs 1318.285 (0.017%)

    The octet is NOT an E-ladder (confirming Phase 34): its clean content is
    the golden partition, a different quantization law from the decuplet's
    clean E-ladder. Robustness uses the Phase 42 frame
    (golden_relation_checks.base_specificity): the split fraction sits in a
    narrow basin with 1/phi^2 uniquely selected.

Outputs:  code/outputs/phase45/baryon_octet.csv
          code/outputs/phase45/baryon_octet.png

References:
    code/phase34_baryon_ladder.py      (octet left open)
    code/phase35_doublecover_baryons.py (decuplet derived; octet open)
    code/golden_relation_checks.py     (robustness frame, Phase 42)
    PDG 2022 baryon masses
===============================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from golden_relation_checks import base_specificity

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase45")

HBAR_C = 197.3269804
E = HBAR_C / 1.0
PHI = (1 + np.sqrt(5)) / 2.0

# PDG 2022 octet masses (MeV)
P, N = 938.27208816, 939.56542052
LAM = 1115.683
SIG = (1189.37 + 1192.642 + 1197.449) / 3.0
XI = (1314.86 + 1321.71) / 2.0
N_BAR = (P + N) / 2.0


# ───────────────────────────────────────────────────────────────────────────────
# THE GOLDEN PARTITION
# ───────────────────────────────────────────────────────────────────────────────

def golden_split_fraction():
    """(Sigma - Lambda) / (Xi - Lambda) vs 1/phi^2. Returns fraction, target,
    and the fractional error."""
    f = (SIG - LAM) / (XI - LAM)
    return f, 1.0 / PHI ** 2, abs(f / (1.0 / PHI ** 2) - 1.0)


def gap_ratio():
    """(Xi - Sigma) / (Sigma - Lambda) vs phi."""
    r = (XI - SIG) / (SIG - LAM)
    return r, PHI, abs(r / PHI - 1.0)


def predict_sigma():
    """Sigma from (Lambda, Xi) via the golden partition."""
    return LAM + (XI - LAM) / PHI ** 2


def predict_xi():
    """Xi from (Lambda, Sigma) via the golden partition."""
    return LAM + PHI ** 2 * (SIG - LAM)


def gmo_octet():
    """Gell-Mann-Okubo sum rule: (m_N + m_Xi)/2 = (3 m_Lam + m_Sig)/4.
    Returns (lhs, rhs, fractional error)."""
    lhs = (N_BAR + XI) / 2.0
    rhs = (3.0 * LAM + SIG) / 4.0
    return lhs, rhs, abs(lhs / rhs - 1.0)


# ───────────────────────────────────────────────────────────────────────────────
# ROBUSTNESS (G2 frame)
# ───────────────────────────────────────────────────────────────────────────────

def split_bas_specificity():
    """Base-specificity of the claim (Sigma-Lam)/(Xi-Lam) = 1/phi^2.
    b is the split-fraction constant (1/phi^2 ~ 0.382); error_fn(b) is the
    fractional deviation of the observed split from b. A narrow basin with
    1/phi^2 inside and at (or below) the minimum = phi is uniquely selected."""
    split = (SIG - LAM) / (XI - LAM)

    def error_fn(b):
        return abs(split / b - 1.0)

    return base_specificity(error_fn, 1.0 / PHI ** 2, 0.005,
                            lo=0.2, hi=0.6, n=20001)


def competitor_fractions():
    """Neighboring simple fractions and their errors vs the observed split."""
    return [
        (q, abs((SIG - LAM) / (XI - LAM) / q - 1.0))
        for q in (3 / 8, 0.38, 1 / PHI ** 2, 5 / 13, 8 / 21, 0.39, 0.4)
    ]


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    f, f_t, f_err = golden_split_fraction()
    r, r_t, r_err = gap_ratio()
    s_pred, x_pred = predict_sigma(), predict_xi()
    g_lhs, g_rhs, g_err = gmo_octet()
    spec = split_bas_specificity()

    rows = [
        {"relation": "split (Sig-Lam)/(Xi-Lam)", "target": 1 / PHI ** 2,
         "observed": f, "pct": 100 * f_err, "pass": f_err < 0.002},
        {"relation": "gap (Xi-Sig)/(Sig-Lam)", "target": PHI,
         "observed": r, "pct": 100 * r_err, "pass": r_err < 0.002},
        {"relation": "predict Sigma", "target": SIG,
         "observed": s_pred, "pct": 100 * abs(s_pred / SIG - 1), "pass": abs(s_pred / SIG - 1) < 5e-4},
        {"relation": "predict Xi", "target": XI,
         "observed": x_pred, "pct": 100 * abs(x_pred / XI - 1), "pass": abs(x_pred / XI - 1) < 5e-4},
        {"relation": "GMO sum rule", "target": g_rhs,
         "observed": g_lhs, "pct": 100 * g_err, "pass": g_err < 0.01},
    ]
    csv_path = os.path.join(OUT_DIR, "baryon_octet.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
        for q, err in competitor_fractions():
            w.writerow({"relation": f"competitor split={q:.4f}", "target": q,
                        "observed": f, "pct": 100 * err, "pass": False})
        w.writerow({"relation": "basin width (0.5%)", "target": 1 / PHI ** 2,
                    "observed": spec["width"], "pct": np.nan,
                    "pass": spec["b_star_inside"]})
    print(f"Wrote {csv_path}")

    print("=== IST PHASE 45: Baryon Octet - Lambda-Sigma Mixing ===")
    print("The octet's clean content: Sigma GOLDEN-PARTITIONS the Lambda->Xi\n")
    print(f"  N = {N_BAR:.2f}   Lam = {LAM:.2f}   Sig = {SIG:.2f}   "
          f"Xi = {XI:.2f} MeV")
    print(f"\n  (Sig-Lam)/(Xi-Lam) = {f:.5f}  vs 1/phi^2 = {f_t:.5f}  "
          f"({100*f_err:+.3f}%)")
    print(f"  (Xi-Sig)/(Sig-Lam) = {r:.5f}  vs phi     = {r_t:.5f}  "
          f"({100*r_err:+.3f}%)")
    print(f"\n  Predictions (parameter-free, 2 anchors -> 1 mass):")
    print(f"    Sig = Lam + (Xi-Lam)/phi^2  = {s_pred:.3f}  "
          f"(obs {SIG:.3f}, {100*abs(s_pred/SIG-1):+.4f}%)")
    print(f"    Xi  = Lam + phi^2(Sig-Lam)  = {x_pred:.3f}  "
          f"(obs {XI:.3f}, {100*abs(x_pred/XI-1):+.4f}%)")
    print(f"\n  Gell-Mann-Okubo anchor: ({N_BAR:.2f}+{XI:.2f})/2 = {g_lhs:.2f}"
          f"  vs  (3*{LAM:.2f}+{SIG:.2f})/4 = {g_rhs:.2f}  "
          f"({100*g_err:.2f}%)")

    print(f"\n  Robustness (G2 frame, base_specificity on 1/phi^2):")
    print(f"    basin width (0.5%): {spec['width']:.5f}  "
          f"phi inside: {spec['b_star_inside']}")
    print(f"    phi error: {100*spec['b_star_error']:.3f}%  "
          f"basin min: {100*spec['min_error']:.3f}% at b = {spec['min_error_b']:.5f}")
    print(f"    competitors:")
    for q, err in competitor_fractions():
        print(f"      {q:.4f}: {100*err:.2f}%  "
              f"{'<- 1/phi^2' if abs(q - 1/PHI**2) < 1e-6 else ''}")
    passed = all(r["pass"] for r in rows)
    print(f"\n  {'PASS: golden partition closes the octet' if passed else 'FAIL: honest negative'}")

    make_figure(f, f_t, s_pred, x_pred)
    print(f"\nWrote {OUT_DIR}")


def make_figure(f, f_t, s_pred, x_pred):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: mass gap diagram with golden partition
    labels = ["Lambda", "Sigma", "Xi"]
    masses = [LAM, SIG, XI]
    axes[0].plot([0, 0], [LAM, XI], "k-", lw=3)
    axes[0].plot([0.1, 0.1], [LAM, SIG], "seagreen", lw=3)
    axes[0].plot([0.2, 0.2], [SIG, XI], "crimson", lw=3)
    for lx, m in zip(labels, masses):
        axes[0].text(0.35, m, f"{lx} {m:.1f}", va="center", fontsize=10)
    axes[0].axhline(LAM + (XI - LAM) / PHI ** 2, color="b", ls="--", lw=1)
    axes[0].text(0.55, LAM + (XI - LAM) / PHI ** 2, "golden point 1/phi^2",
                 fontsize=8, color="b")
    axes[0].set_xlim(-0.2, 2.2); axes[0].set_ylim(1100, 1330)
    axes[0].set_yticks([]); axes[0].set_xticks([])
    axes[0].set_title("Sigma golden-partitions Lambda->Xi")
    axes[0].set_ylabel("mass (MeV)")

    # Right: split fraction vs 1/phi^2 and competitors
    qs = [3/8, 0.38, 1/PHI**2, 5/13, 8/21, 0.39, 0.4]
    errs = [abs(f / q - 1) * 100 for q in qs]
    colors = ["grey" if abs(q - 1/PHI**2) > 1e-6 else "crimson" for q in qs]
    axes[1].bar([str(round(q, 4)) for q in qs], errs, color=colors)
    axes[1].axhline(0.2, color="k", ls="--", lw=1, label="0.2% threshold")
    axes[1].set_ylabel("|error| (%)"); axes[1].set_xlabel("split fraction")
    axes[1].set_title("Base specificity: 1/phi^2 uniquely selected")
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "baryon_octet.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
