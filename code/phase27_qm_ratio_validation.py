"""
================================================================================
IST PHASE 27 - Top-Down QM-Scale Ratio Validation
================================================================================
Purpose:
    Validate IST's quantitative predictions at the QUANTUM-MECHANICAL scale,
    working TOP-DOWN: take the measured QM-scale constants (CODATA masses,
    fine-structure constant, Compton/classical radii) as given anchors and
    ask whether the substrate topology predicts their RATIOS -- rather than
    building bottom-up from the Planck scale and hoping to land on a mass.

    This follows the project's standing guidance: ground validation in
    existing observational measurements when possible; the framework is a
    work in progress and specific variables may turn out different from
    their initially suggested values; prefer ratio tests that cancel the
    uncertain absolute normalization.

Scale reference frame:
    Validation is carried out at the QM scale (Compton wavelengths, lepton
    and nucleon masses in GeV, the fine-structure constant). The Planck
    mass is used ONLY for the flagged bottom-up cross-checks, where it is
    the least-secure input (M_P carries the G-normalization).

Test tiers (strongest first):
    Tier 1 - parameter-free (no free parameters; ratios that cancel alpha
             and phi entirely):
        m_p / m_e  =  6 pi^5           (from the two mass formulas; alpha
                                        and phi^2 cancel)     ~ 0.0019%
        alpha      =  r_e / lbar_C     (geometric identity; consistency
                                        check, exact by definition)
    Tier 2 - minimally-parameterized (one candidate form each, reported
             honestly when the naive form fails):
        m_n / m_p  =  1 + delta_n,
             delta_n = alpha/phi^2     (plan's naive form; overshoots ~2x)
             delta_n = alpha/(2 phi^2) (factor-2 candidate; ~1.1% off)
             best-fit delta_n and the implied running phi_n are reported
             so the discrepancy is quantified, not hidden.
        m_mu / m_e =  3/(2 alpha)      (candidate; ~0.6% off -- reported as
             a search hit, NOT a claimed derivation)
    Tier 3 - bottom-up Planck-anchored (carry M_P normalization and the
             alpha^-9 sensitivity; the least secure):
        proton   :  M_P/m_p = (2/phi^2) alpha^-9
        electron :  M_P/m_e = (12 pi^5/phi^2) alpha^-9
        neutron  :  running-phi form  m_n = m_p (1 + alpha/phi_n^2)

Outputs:  code/outputs/phase27/qm_ratio_validation.csv
          code/outputs/phase27/qm_ratio_validation.png

References:
    code/ist_toolkit_v2.py               (CODATA 2018 constants)
    code/phase3_mass_spectrum.py         (original mass formulas)
    code/alpha_s_fix.py                  (running-phi neutron)
    notes/open_questions.md              (muon/tau open question)
    notes/IST v6.2 temporal holonomy.md  (scale-refinement discussion)
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ist_toolkit_v2 import (
    PHI, ALPHA, ALPHA_INV, M_PLANCK, M_PROTON, M_ELECTRON, M_NEUTRON,
    R_E_CLASSICAL, LAMBDA_BAR_C_E,
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase27")

# Muon mass, CODATA 2018 (GeV/c^2) -- not in ist_toolkit_v2
M_MUON = 0.1056583755


# ───────────────────────────────────────────────────────────────────────────────
# TIER 1 - PARAMETER-FREE RATIOS
# ───────────────────────────────────────────────────────────────────────────────

def m_p_over_m_e_6pi5():
    """From M_P/m_p = (2/phi^2) alpha^-9 and M_P/m_e = (12pi^5/phi^2) alpha^-9
    the ratio cancels BOTH alpha and phi^2:
        m_p / m_e = (12 pi^5 / 2) = 6 pi^5.
    This is IST's strongest top-down prediction: no free parameters at all.
    """
    return 6.0 * np.pi ** 5


def alpha_geometric():
    """alpha = r_e / lbar_C. This is exact BY DEFINITION of the classical
    radius (r_e = alpha * lbar_C), so it is a consistency identity, not an
    independent prediction. Included to document the geometric link."""
    return R_E_CLASSICAL / LAMBDA_BAR_C_E


# ───────────────────────────────────────────────────────────────────────────────
# TIER 2 - MINIMALLY-PARAMETERIZED FORMS
# ───────────────────────────────────────────────────────────────────────────────

def delta_n_naive():
    """Plan's literal form: delta_n = alpha / phi^2."""
    return ALPHA / PHI ** 2


def delta_n_half():
    """Factor-2 candidate: delta_n = alpha / (2 phi^2)."""
    return ALPHA / (2.0 * PHI ** 2)


def delta_n_observed():
    """m_n/m_p - 1 from measured masses (the target the forms must hit)."""
    return M_NEUTRON / M_PROTON - 1.0


def running_phi_neutron():
    """phi_n that makes alpha/phi_n^2 reproduce the observed neutron excess."""
    return np.sqrt(ALPHA / delta_n_observed())


def m_mu_over_m_e():
    return M_MUON / M_ELECTRON


def m_mu_candidate_3_over_2alpha():
    """m_mu/m_e ~ 3/(2 alpha). Reported as a search hit with honest residual,
    not a derived prediction (muon/tau is an open question in the plan)."""
    return 1.5 / ALPHA


# ───────────────────────────────────────────────────────────────────────────────
# TIER 3 - BOTTOM-UP PLANCK-ANCHORED (least secure)
# ───────────────────────────────────────────────────────────────────────────────

def proton_mass_planck():
    """m_p = M_P / ((2/phi^2) alpha^-9)."""
    return M_PLANCK / ((2.0 / PHI ** 2) * ALPHA ** (-9))


def electron_mass_planck():
    """m_e = M_P / ((12 pi^5/phi^2) alpha^-9)."""
    return M_PLANCK / ((12.0 * np.pi ** 5 / PHI ** 2) * ALPHA ** (-9))


def neutron_mass_running_phi(phi_n=None):
    """m_n = m_p (1 + alpha/phi_n^2). With the best-fit running phi_n this
    reproduces the neutron exactly by construction; with phi_n = phi (the
    plan's literal) it overshoots ~2x in delta_n."""
    if phi_n is None:
        phi_n = running_phi_neutron()
    return M_PROTON * (1.0 + ALPHA / phi_n ** 2)


# ───────────────────────────────────────────────────────────────────────────────
# REPORTING HELPERS
# ───────────────────────────────────────────────────────────────────────────────

def residual_percent(pred, obs):
    return 100.0 * (pred - obs) / obs


def accuracy_percent(pred, obs):
    return 100.0 * (1.0 - abs(pred - obs) / obs)


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = []

    # ── Tier 1: parameter-free ──────────────────────────────────────────
    pred = m_p_over_m_e_6pi5()
    obs = M_PROTON / M_ELECTRON
    rows.append({
        "tier": "1", "quantity": "m_p/m_e = 6 pi^5 (parameter-free)",
        "predicted": pred, "observed": obs,
        "residual_percent": residual_percent(pred, obs),
        "accuracy_percent": accuracy_percent(pred, obs),
        "note": "alpha and phi^2 cancel; no free parameters",
    })

    pred_a = alpha_geometric()
    rows.append({
        "tier": "1", "quantity": "alpha = r_e/lbar_C (geometric identity)",
        "predicted": pred_a, "observed": ALPHA,
        "residual_percent": residual_percent(pred_a, ALPHA),
        "accuracy_percent": accuracy_percent(pred_a, ALPHA),
        "note": "exact by definition (consistency check)",
    })

    # ── Tier 2: minimally-parameterized ────────────────────────────────
    dn_obs = delta_n_observed()
    for name, dn in [("delta_n = alpha/phi^2 (plan)", delta_n_naive()),
                     ("delta_n = alpha/(2 phi^2) (factor-2)", delta_n_half())]:
        pred_mn = M_PROTON * (1.0 + dn)
        rows.append({
            "tier": "2", "quantity": f"m_n from {name}",
            "predicted": pred_mn, "observed": M_NEUTRON,
            "residual_percent": residual_percent(pred_mn, M_NEUTRON),
            "accuracy_percent": accuracy_percent(pred_mn, M_NEUTRON),
            "note": f"delta_n={dn:.6f} vs observed {dn_obs:.6f}",
        })

    pred_mu = m_mu_candidate_3_over_2alpha()
    obs_mu = m_mu_over_m_e()
    rows.append({
        "tier": "2", "quantity": "m_mu/m_e ~ 3/(2 alpha) (search hit)",
        "predicted": pred_mu, "observed": obs_mu,
        "residual_percent": residual_percent(pred_mu, obs_mu),
        "accuracy_percent": accuracy_percent(pred_mu, obs_mu),
        "note": "open question; reported as a candidate, not a derivation",
    })

    # ── Tier 3: bottom-up Planck-anchored ───────────────────────────────
    pred_p = proton_mass_planck()
    rows.append({
        "tier": "3", "quantity": "m_p from (2/phi^2) alpha^-9 (Planck)",
        "predicted": pred_p, "observed": M_PROTON,
        "residual_percent": residual_percent(pred_p, M_PROTON),
        "accuracy_percent": accuracy_percent(pred_p, M_PROTON),
        "note": "carries M_P normalization and alpha^-9 sensitivity",
    })
    pred_e = electron_mass_planck()
    rows.append({
        "tier": "3", "quantity": "m_e from (12pi^5/phi^2) alpha^-9 (Planck)",
        "predicted": pred_e, "observed": M_ELECTRON,
        "residual_percent": residual_percent(pred_e, M_ELECTRON),
        "accuracy_percent": accuracy_percent(pred_e, M_ELECTRON),
        "note": "carries M_P normalization and alpha^-9 sensitivity",
    })

    csv_path = os.path.join(OUT_DIR, "qm_ratio_validation.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"Wrote {csv_path}")

    print("\n=== IST PHASE 27: Top-Down QM-Scale Ratio Validation ===")
    print("Scale reference frame: QM scale (CODATA 2018 masses, alpha, radii).")
    print("Approach: top-down; measured QM constants are anchors, ratios are")
    print("the predicted observables; M_P used only in flagged bottom-up checks.\n")
    for r in rows:
        print(f"  [{r['tier']}] {r['quantity']:45s} "
              f"pred={r['predicted']:.6g} obs={r['observed']:.6g} "
              f"acc={r['accuracy_percent']:.4f}%  ({r['note']})")

    print(f"\nNeutron running-phi diagnostic:")
    print(f"  observed delta_n         = {delta_n_observed():.6f}")
    print(f"  naive alpha/phi^2        = {delta_n_naive():.6f} "
          f"(overshoots {delta_n_naive()/delta_n_observed():.2f}x)")
    print(f"  factor-2 alpha/(2phi^2)  = {delta_n_half():.6f}")
    print(f"  implied running phi_n    = {running_phi_neutron():.4f} "
          f"(phi={PHI:.4f}, phi^2={PHI**2:.4f})")
    print(f"  running-phi m_n          = {neutron_mass_running_phi():.6f} GeV "
          f"(obs {M_NEUTRON:.6f})")

    make_figure(rows)
    print(f"Wrote {OUT_DIR}")


def make_figure(rows):
    fig, ax = plt.subplots(figsize=(10, 6))
    names = [r["quantity"].split(" = ")[0].split(" (")[0] for r in rows]
    accs = [r["accuracy_percent"] for r in rows]
    colors = {"1": "seagreen", "2": "steelblue", "3": "darkorange"}
    bars = ax.bar(names, accs, color=[colors[r["tier"]] for r in rows])
    for b, r in zip(bars, rows):
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.3,
                f"{r['accuracy_percent']:.3f}%", ha="center", fontsize=8)
    ax.axhline(99.0, color="crimson", ls="--", lw=1)
    ax.set_ylabel("prediction accuracy (%)")
    ax.set_title("Phase 27: top-down QM-scale ratio validation "
                 "(green=Tier1 param-free, blue=Tier2, orange=Tier3 Planck)")
    ax.set_ylim(0, 102)
    plt.xticks(rotation=30, ha="right", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "qm_ratio_validation.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
