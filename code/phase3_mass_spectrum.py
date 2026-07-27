
"""
================================================================================
IST PHASE 3 - Mass Ratios from Phase-Space Volume
================================================================================
Purpose:
    Extend the IST mass formulas to the electron, neutron, and neutrino, and
    derive the strong coupling alpha_s from the associator magnitude. The proton
    and electron formulas are already high-accuracy empirical relations; here
    we test the neutron extension and explore the associator-driven alpha_s
    running and neutrino tunneling hypotheses.

Inputs:   none (CODATA constants imported from ist_toolkit_v2)
Outputs:
    code/outputs/phase3/mass_predictions.csv   - mass and coupling predictions
    code/outputs/phase3/mass_hierarchy.png     - 3-panel summary (300 DPI)

References:
    notes/IST_Research_Plan_Phases_1-5.md   (Phase 3)
    main/ist_v5_3_topology_substrate.md     (?3.6 proton/electron mass)
    notes/beta_function_derivation.md       (associator magnitude 1/phi^2)
    notes/master_equation_derivation.md     (master equation, associator term)

Conventions:
    * Mass ratios use M_P (Planck mass) as the reference.
    * Neutron formula: we test the plan's literal ratio form and the
      physically clearer m_n = m_p (1 + delta_n) with delta_n ~ alpha/phi^2.
    * alpha_s(E) is modeled as C phi^{-n(E)} with n(E) = log(E_ref/E)/log(b).
      C defaults to the associator fixed-point magnitude 1/phi^2, and can be
      re-normalized to match alpha_s(M_Z).
    * Neutrino mass: m_nu = M_Planck * P_tunnel (in eV if M_Planck is in eV).
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ist_toolkit_v2 import (
    PHI, ALPHA, ALPHA_INV, M_PLANCK, M_PROTON, M_ELECTRON, M_NEUTRON
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase3")

# Reference alpha_s values for comparison (approximate)
ALPHA_S_REF = {
    "M_Z (91.2 GeV)": (91.1876e9, 0.118),
    "m_tau (1.78 GeV)": (1.77686e9, 0.33),
    "m_b (4.18 GeV)": (4.18e9, 0.22),
    "m_t (173 GeV)": (173e9, 0.09),
}

# Neutrino scale (order-of-magnitude individual mass)
M_NU_OBSERVED_EV = 0.05


def proton_ratio():
    """M_P / m_p = (2/phi^2) alpha^{-9}."""
    return (2.0 / PHI ** 2) * (ALPHA ** (-9))


def electron_ratio():
    """M_P / m_e = (12pi^5/phi^2) alpha^{-9}."""
    return (12.0 * np.pi ** 5 / PHI ** 2) * (ALPHA ** (-9))


def neutron_ratio_plan_literal(delta_n=None):
    """Plan literal: M_P/m_n = (2/phi^2) alpha^{-9} (1 + delta_n)."""
    if delta_n is None:
        delta_n = ALPHA / PHI ** 2
    return proton_ratio() * (1.0 + delta_n)


def neutron_from_proton(delta_n=None):
    """Physically clearer: m_n = m_p (1 + delta_n)."""
    if delta_n is None:
        delta_n = ALPHA / PHI ** 2
    m_p_pred = predicted_mass(proton_ratio())
    return m_p_pred * (1.0 + delta_n)


def predicted_mass(ratio):
    return M_PLANCK / ratio


def accuracy_percent(pred, obs):
    return 100.0 * (1.0 - abs(pred - obs) / obs)


def best_delta_n_for_neutron():
    """Solve m_n = m_p (1 + delta) for the observed neutron mass."""
    m_p_pred = predicted_mass(proton_ratio())
    return M_NEUTRON / m_p_pred - 1.0


# -- Strong coupling from associator ------------------------------------------

def associator_magnitude_fixed_point():
    """Associator |[q1,q2,q3]| at the golden-ratio fixed point."""
    return 1.0 / PHI ** 2


def alpha_s_associator(E_GeV, E_ref_GeV=91.1876, alpha_s_ref=0.118,
                       step_base=2.0, use_fixed_point=False):
    """alpha_s(E) = C phi^{-n(E)} with n(E) = log(E_ref/E)/log(step_base).

    If use_fixed_point is True, C = 1/phi^2 (topological prediction).
    Otherwise C is normalized so that alpha_s(E_ref) = alpha_s_ref.
    """
    # n(E) increases with energy: many fractal layers probed at high E,
    # so the associator averages to zero (asymptotic freedom).
    n = np.log(E_GeV / E_ref_GeV) / np.log(step_base)
    if use_fixed_point:
        C = 1.0 / PHI ** 2
    else:
        C = alpha_s_ref  # because n(E_ref) = 0
    return C * (PHI ** (-n))


# -- Neutrino tunneling -------------------------------------------------------

def M_planck_eV():
    return M_PLANCK * 1.0e9


def neutrino_mass_eV(P_tunnel):
    """m_nu = M_Planck * P_tunnel (M_Planck in eV)."""
    return M_planck_eV() * P_tunnel


def required_tunneling_probability(m_nu_eV=M_NU_OBSERVED_EV):
    return m_nu_eV / M_planck_eV()


# -- Main driver --------------------------------------------------------------

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    rows = []

    # Proton
    rp = proton_ratio()
    mp_pred = predicted_mass(rp)
    rows.append({
        "quantity": "proton",
        "observed_GeV": M_PROTON,
        "predicted_GeV": mp_pred,
        "ratio_observed": M_PLANCK / M_PROTON,
        "ratio_predicted": rp,
        "accuracy_percent": accuracy_percent(mp_pred, M_PROTON),
    })

    # Electron
    re = electron_ratio()
    me_pred = predicted_mass(re)
    rows.append({
        "quantity": "electron",
        "observed_GeV": M_ELECTRON,
        "predicted_GeV": me_pred,
        "ratio_observed": M_PLANCK / M_ELECTRON,
        "ratio_predicted": re,
        "accuracy_percent": accuracy_percent(me_pred, M_ELECTRON),
    })

    # Neutron ? plan literal
    rn_lit = neutron_ratio_plan_literal()
    mn_lit = predicted_mass(rn_lit)
    rows.append({
        "quantity": "neutron_plan_literal",
        "observed_GeV": M_NEUTRON,
        "predicted_GeV": mn_lit,
        "ratio_observed": M_PLANCK / M_NEUTRON,
        "ratio_predicted": rn_lit,
        "accuracy_percent": accuracy_percent(mn_lit, M_NEUTRON),
    })

    # Neutron ? m_n = m_p (1 + delta)
    rn_alt = M_PLANCK / neutron_from_proton()
    mn_alt = neutron_from_proton()
    rows.append({
        "quantity": "neutron_mn_eq_mp_times_factor",
        "observed_GeV": M_NEUTRON,
        "predicted_GeV": mn_alt,
        "ratio_observed": M_PLANCK / M_NEUTRON,
        "ratio_predicted": rn_alt,
        "accuracy_percent": accuracy_percent(mn_alt, M_NEUTRON),
    })

    # Best-fit delta_n
    delta_best = best_delta_n_for_neutron()
    mn_best = neutron_from_proton(delta_best)
    rows.append({
        "quantity": "neutron_best_fit_delta",
        "observed_GeV": M_NEUTRON,
        "predicted_GeV": mn_best,
        "ratio_observed": M_PLANCK / M_NEUTRON,
        "ratio_predicted": M_PLANCK / mn_best,
        "accuracy_percent": accuracy_percent(mn_best, M_NEUTRON),
    })

    csv_path = os.path.join(OUT_DIR, "mass_predictions.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {csv_path}")

    print("\nMass predictions:")
    for r in rows:
        print(f"  {r['quantity']:30s} obs={r['observed_GeV']:.9f} "
              f"pred={r['predicted_GeV']:.9f}  acc={r['accuracy_percent']:.4f}%")

    print("\nNeutron delta analysis:")
    print(f"  delta_n from plan (alpha/phi^2)        = {ALPHA/PHI**2:.6f}")
    print(f"  Best-fit delta_n (m_n = m_p(1+delta))  = {delta_best:.6f}")
    print(f"  Ratio best/plan                        = {delta_best / (ALPHA/PHI**2):.3f}")

    # alpha_s running
    print("\nalpha_s running (associator model, fitted at M_Z):")
    energies = np.logspace(0, 11, 200)  # 1 GeV to 1e11 GeV
    alpha_s_fitted = [alpha_s_associator(E) for E in energies]
    alpha_s_fixed = [alpha_s_associator(E, use_fixed_point=True) for E in energies]

    for name, (E, val) in ALPHA_S_REF.items():
        pred_fitted = alpha_s_associator(E / 1e9)
        pred_fixed = alpha_s_associator(E / 1e9, use_fixed_point=True)
        print(f"  {name:20s} ref={val:.3f}  fitted={pred_fitted:.3f}  fixed-point={pred_fixed:.3f}")

    # Neutrino tunneling
    P_req = required_tunneling_probability()
    P_naive = ALPHA / PHI ** 2
    print(f"\nNeutrino tunneling:")
    print(f"  M_Planck = {M_planck_eV():.3e} eV")
    print(f"  Required P_tunnel for m_nu = {M_NU_OBSERVED_EV} eV: {P_req:.3e}")
    print(f"  Naive P_tunnel ~ alpha/phi^2 = {P_naive:.3e}")
    print(f"  Suppression factor needed: {P_req / P_naive:.3e}")

    make_figure(rows, energies, alpha_s_fitted, alpha_s_fixed, P_req, P_naive)


def make_figure(rows, energies, alpha_s_fitted, alpha_s_fixed, P_req, P_naive):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # A: mass predictions
    ax = axes[0]
    labels = ["proton", "electron", "neutron\n(m_n=m_p(1+delta))"]
    obs = [M_PROTON, M_ELECTRON, M_NEUTRON]
    pred = [rows[0]["predicted_GeV"], rows[1]["predicted_GeV"], rows[3]["predicted_GeV"]]
    x = np.arange(len(labels))
    width = 0.35
    ax.bar(x - width / 2, obs, width, label="observed", color="steelblue")
    ax.bar(x + width / 2, pred, width, label="predicted", color="crimson")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("mass (GeV)")
    ax.set_yscale("log")
    ax.set_title("A. Mass predictions")
    ax.legend(fontsize=8)

    # B: alpha_s running
    ax = axes[1]
    ax.loglog(energies, alpha_s_fitted, "-", color="crimson",
              label=r"associator, fitted to $\alpha_s(M_Z)$")
    ax.loglog(energies, alpha_s_fixed, "--", color="gray",
              label=r"associator, fixed point $C=1/\varphi^2$")
    for name, (E, val) in ALPHA_S_REF.items():
        ax.plot(E / 1e9, val, "o", ms=6, label=f"ref: {name}")
    ax.set_xlabel(r"energy $E$ (GeV)")
    ax.set_ylabel(r"$\alpha_s(E)$")
    ax.set_title("B. Strong coupling from associator")
    ax.legend(fontsize=7)

    # C: neutrino mass vs tunneling probability
    ax = axes[2]
    P_vals = np.logspace(-35, -25, 200)
    m_nu = neutrino_mass_eV(P_vals)
    ax.loglog(P_vals, m_nu, "-", color="steelblue")
    ax.axhline(M_NU_OBSERVED_EV, color="crimson", ls="--",
               label=f"observed scale ~{M_NU_OBSERVED_EV} eV")
    ax.axvline(P_req, color="crimson", ls=":",
               label=f"required $P_{{tunnel}} = {P_req:.1e}$")
    ax.axvline(P_naive, color="gray", ls=":",
               label=r"naive $P \sim \alpha/\varphi^2$")
    ax.set_xlabel(r"tunneling probability $P_{tunnel}$")
    ax.set_ylabel(r"$m_\nu$ (eV)")
    ax.set_title("C. Neutrino mass from topological tunneling")
    ax.legend(fontsize=7)

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "mass_hierarchy.png")
    fig.savefig(path, dpi=300)
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
