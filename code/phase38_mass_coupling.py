"""
================================================================================
IST PHASE 38 - The Mass-Coupling Relation (Insight B): Couplings as Slaved
Running Between Golden Mass Harmonics
================================================================================
Purpose:
    Test the retrospective Insight B: the substrate's golden harmonics
    structure the MASS spectrum, and the force couplings are the 'slaved
    running' between those mass harmonics. Concretely, the coupling at a
    scale E is set by the golden-layer count from the proton mass, with a
    per-force normalization.

The mass->coupling relation (from Phase 15, generalized):

    alpha_i(E) = C_i * phi^{-n(E)},   n(E) = ln(E / m_p) / ln(phi^4)

    where n(E) counts golden-ratio layers between m_p and scale E, and C_i
    is a per-force normalization. This is the mechanism: the mass spectrum
    defines the layer count, and the coupling follows.

Tested here:

    (A) The strong coupling follows the relation with C = 1/phi^2 (the
        associator fixed-point magnitude):
            alpha_s(M_Z)  = 0.1217 vs 0.118  (3.1%)
            alpha_s(m_tau)= 0.3256 vs 0.330  (1.3%)
            alpha_s(m_b)  = 0.2629 vs 0.220  (19.5%)
            alpha_s(m_t)  = 0.1037 vs 0.090  (15.2%)
        VERDICT: works at M_Z (3%) and m_tau (1.3%); the b/t errors are the
        known active-flavor threshold issue (Phase 15 noted 15-20%).

    (B) The per-force normalizations C_i at M_Z, written as
        C_i = alpha * phi^{k_i}:
            k_em    = 2.520   (alpha = 1/137.036)
            k_weak  = 5.569
            k_strong= 8.161
        The ladder gaps are 3.05 and 2.59 -- NOT uniform. If the forces were
        clean golden harmonics, the gaps would be equal.
        VERDICT: partial signal; the k_i rise with force strength, but the
        gaps are not clean golden steps.

    (C) The total golden span from alpha to alpha_s at M_Z:
            ln(alpha_s/alpha)/ln(phi) = 5.641
        em->strong spans ~5.6 golden powers. The em->weak and weak->strong
        sub-spans are 3.05 and 2.59 -- near phi^2-related but not exact.

Honest conclusion:
    The MASS->COUPLING MECHANISM is supported for the strong force: the
    golden-layer count from the proton mass reproduces alpha_s at M_Z and
    m_tau to 1-3%, with the associator magnitude 1/phi^2 as the natural
    normalization. This is the concrete content of Insight B.
    The per-force normalization LADDER is only partial: the C_i rise with
    force strength but the gaps (2.6-3.0) are not clean golden steps. The
    clean statement is the strong-coupling mass->coupling relation; the
    unified three-force ladder remains open (consistent with Phase 37's
    finding that the couplings themselves are not golden-laddered).

Outputs:  code/outputs/phase38/mass_coupling.csv
          code/outputs/phase38/mass_coupling.png

References:
    notes/retrospective_cross_analysis.md  (Insight B)
    code/alpha_s_fix.py                    (phi^4 layer-counting)
    code/phase15_running_phi.py
    PDG 2022 running couplings at M_Z
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ist_toolkit_v2 import PHI, ALPHA

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase38")

M_P = 0.938272        # proton mass (GeV)
PHI4 = PHI ** 4
C_ASSOC = 1.0 / PHI ** 2    # associator fixed-point magnitude

# Couplings at M_Z (PDG 2022)
ALPHA_EM_MZ, ALPHA_W_MZ, ALPHA_S_MZ = 1 / 127.952, 1 / 29.5, 0.118


# ───────────────────────────────────────────────────────────────────────────────
# THE MASS -> COUPLING RELATION
# ───────────────────────────────────────────────────────────────────────────────

def n_layers(E_GeV):
    """Golden layers between the proton mass and scale E."""
    return np.log(E_GeV / M_P) / np.log(PHI4)


def alpha_s_from_layers(E_GeV, C=C_ASSOC):
    """alpha_s(E) = C * phi^{-n(E)}."""
    return C * PHI ** (-n_layers(E_GeV))


def c_normalization(alpha_at_E, E_GeV):
    """The per-force normalization C_i such that alpha_i(E) = C_i phi^{-n(E)}.
    C_i = alpha_i(E) * phi^{n(E)}."""
    return alpha_at_E * PHI ** n_layers(E_GeV)


def k_golden_power(C):
    """Write C = alpha * phi^k; return k."""
    return np.log(C / ALPHA) / np.log(PHI)


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    M_Z = 91.1876

    # (A) strong coupling via golden layers
    rows = []
    for name, E, ref in [("M_Z", 91.1876, 0.118), ("m_tau", 1.77686, 0.33),
                         ("m_b", 4.18, 0.22), ("m_t", 173.0, 0.09)]:
        pred = alpha_s_from_layers(E)
        rows.append({"test": "A-strong", "scale": name, "E_GeV": E,
                     "predicted": pred, "observed": ref,
                     "pct_err": 100 * (pred / ref - 1)})

    # (B) per-force normalization ladder at M_Z
    for name, a_val in [("em", 1 / 127.952), ("weak", 1 / 29.5),
                        ("strong", 0.118)]:
        C = c_normalization(a_val, M_Z)
        k = k_golden_power(C)
        rows.append({"test": "B-ladder", "scale": name, "E_GeV": M_Z,
                     "predicted": C, "observed": np.nan,
                     "pct_err": np.nan, "k": k})
    csv_path = os.path.join(OUT_DIR, "mass_coupling.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["test", "scale", "E_GeV",
                                           "predicted", "observed", "pct_err",
                                           "k"])
        w.writeheader(); w.writerows(rows)
    print(f"Wrote {csv_path}")

    print("=== IST PHASE 38: The Mass-Coupling Relation (Insight B) ===")
    print("Couplings as slaved running between golden mass harmonics\n")
    print("  (A) alpha_s(E) = (1/phi^2) phi^{-n(E)}, n = ln(E/m_p)/ln(phi^4):")
    for r in rows:
        if r["test"] != "A-strong":
            continue
        print(f"      {r['scale']:7s} E={r['E_GeV']:8.2f} pred={r['predicted']:.4f} "
              f"ref={r['observed']:.3f} err={r['pct_err']:+.1f}%")

    print("\n  (B) per-force normalization C_i = alpha * phi^k at M_Z:")
    for r in rows:
        if r["test"] != "B-ladder":
            continue
        print(f"      {r['scale']:7s} C={r['predicted']:.5f}  k={r['k']:.3f}")

    ks = [r["k"] for r in rows if r["test"] == "B-ladder"]
    print(f"      ladder gaps: {ks[1]-ks[0]:.2f}, {ks[2]-ks[1]:.2f} "
          f"(NOT uniform)")

    span = np.log(ALPHA_S_MZ / ALPHA_EM_MZ) / np.log(PHI)
    print(f"\n  (C) total golden span alpha->alpha_s at M_Z = {span:.3f}")
    print(f"      em->strong spans ~{span:.1f} golden powers.")

    print(f"\nHonest conclusion:")
    print(f"  The MASS->COUPLING mechanism is SUPPORTED for the strong force:")
    print(f"  golden-layer count from m_p reproduces alpha_s at M_Z (3.1%) and")
    print(f"  m_tau (1.3%), with the associator magnitude 1/phi^2 as the")
    print(f"  natural normalization. This is the concrete content of Insight B.")
    print(f"  The per-force normalization LADDER is PARTIAL: C_i rise with")
    print(f"  force strength (k: 2.5, 5.6, 8.2) but the gaps (2.6-3.0) are not")
    print(f"  clean golden steps. The clean statement is the strong-coupling")
    print(f"  mass->coupling relation; the unified three-force ladder remains")
    print(f"  open (consistent with Phase 37).")

    make_figure(rows)
    print(f"\nWrote {OUT_DIR}")


def make_figure(rows):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    a = [r for r in rows if r["test"] == "A-strong"]
    names = [r["scale"] for r in a]
    pred = [r["predicted"] for r in a]
    obs = [r["observed"] for r in a]
    x = np.arange(len(names))
    axes[0].bar(x - 0.2, pred, 0.4, color="steelblue", label="predicted")
    axes[0].bar(x + 0.2, obs, 0.4, color="seagreen", label="observed")
    axes[0].set_xticks(x); axes[0].set_xticklabels(names)
    axes[0].set_ylabel("alpha_s"); axes[0].set_title("Strong coupling via golden layers")
    axes[0].legend(fontsize=8)

    b = [r for r in rows if r["test"] == "B-ladder"]
    axes[1].bar([r["scale"] for r in b], [r["k"] for r in b],
                color="darkorange")
    axes[1].set_ylabel("k (golden power above alpha)")
    axes[1].set_title("Per-force normalization ladder (C_i = alpha phi^k)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "mass_coupling.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
