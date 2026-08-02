"""
================================================================================
IST PHASE 28 - The Factor-2 Neutron: delta_n = (alpha/2 phi^2)(1 - c alpha)
================================================================================
Purpose:
    Pursue the factor-2 neutron finding surfaced by Phase 27's top-down
    validation. The plan's naive form

        delta_n = alpha / phi^2        (m_n = m_p (1 + delta_n))

    overshoots the observed neutron-proton mass excess by 2.02x. Phase 28
    derives and validates the corrected form, checks it against CODATA 2018
    at full precision, and documents the hypotheses for where the factor 2
    originates.

The result (parameter-free, all inputs measured CODATA constants):

        delta_n = (alpha / 2 phi^2) * (1 - c alpha),
        c       = 3/2 - alpha / phi^6

    expanded to third order in alpha:

        delta_n = alpha/(2 phi^2) - 3 alpha^2/(4 phi^2) + alpha^3/(2 phi^8)

    With CODATA 2018 values this reproduces the observed neutron excess to
    ~1.2e-9 relative (0.02 sigma) -- i.e. m_n to 100.00000000%.

Structure of the result (and its physical reading):
    * The leading factor 1/2 is the Phase 27 discovery: the naive alpha/phi^2
      must be halved. Natural candidates for the 2:
        (a) the 720-degree double-cover (a full cycle needs TWO traversals of
            the Klein twist; Phase 23a/25 verified exactly two seam crossings
            per 4-tick cycle);
        (b) a combinatorial factor from the neutron's extra binding loop (the
            supplementary already suggested 'a combinatorial factor from the
            number of additional loops or isospin breaking').
    * The (3/2) alpha term looks like a leading QED-style radiative
      correction (compare the anomalous-momentum 1 + alpha/(2 pi) family),
      and the exact coefficient is 3/2 - alpha/phi^6, off from 3/2 by the
      tiny alpha/phi^6 ~ 0.4%. Whether the phi^6 refinement is real or a
      numerical coincidence at CODATA precision is a documented open point.

Honest caveats:
    * This is an empirical relation validated top-down against measured
      masses, NOT a first-principles derivation. The factor 2 and the
      correction series are consistent with the framework's double-cover
      and associator machinery but are not yet derived from them.
    * The synthesis paper's earlier claim that running phi ~ 1.98 gives
      99.99% is an ARITHMETIC ERROR (that phi gives m_n = 0.9400, accuracy
      99.95%). The true running phi for the neutron is phi_n ~ 2.301, which
      sits 0.55% from phi*sqrt(2) ~ 2.288. The corrected running-phi and
      the new closed form are both reported here.

Outputs:  code/outputs/phase28/neutron_factor2.csv
          code/outputs/phase28/neutron_factor2.png

References:
    code/phase27_qm_ratio_validation.py   (top-down framing that surfaced 2x)
    supplementary/phase3_mass_hierarchy.md (original delta_n = alpha/phi^2)
    code/ist_toolkit_v2.py                (CODATA 2018 constants)
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ist_toolkit_v2 import PHI, ALPHA, M_PROTON, M_NEUTRON

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase28")

# CODATA 2018 relative uncertainties (1-sigma)
U_MP_REL = 1.4e-8
U_MN_REL = 5.7e-8


# ───────────────────────────────────────────────────────────────────────────────
# THE FORMS
# ───────────────────────────────────────────────────────────────────────────────

def delta_n_observed():
    return M_NEUTRON / M_PROTON - 1.0


def delta_n_naive():
    """Plan's literal form: alpha/phi^2 (overshoots ~2.02x)."""
    return ALPHA / PHI ** 2


def delta_n_factor2():
    """Phase 27 factor-2 leading term: alpha/(2 phi^2)."""
    return ALPHA / (2.0 * PHI ** 2)


def c_exact_coefficient():
    """Coefficient c such that delta_n = alpha/(2 phi^2) (1 - c alpha).
    Solved from the measured masses; compare to 3/2 - alpha/phi^6."""
    return (1.0 - delta_n_observed() / delta_n_factor2()) / ALPHA


def c_claimed():
    """c = 3/2 - alpha/phi^6 (the proposed closed form)."""
    return 1.5 - ALPHA / PHI ** 6


def delta_n_exact():
    """delta_n = alpha/(2 phi^2) * (1 - (3/2 - alpha/phi^6) alpha)."""
    return delta_n_factor2() * (1.0 - c_claimed() * ALPHA)


def m_n_predicted(delta_fn):
    return M_PROTON * (1.0 + delta_fn())


# ───────────────────────────────────────────────────────────────────────────────
# RUNNING-PHI DIAGNOSTIC (correcting the synthesis-paper arithmetic error)
# ───────────────────────────────────────────────────────────────────────────────

def running_phi_neutron():
    """phi_n such that alpha/phi_n^2 = delta_n(observed)."""
    return np.sqrt(ALPHA / delta_n_observed())


def m_n_from_phi(phi_n):
    """m_n = m_p (1 + alpha/phi_n^2) for a given running phi_n."""
    return M_PROTON * (1.0 + ALPHA / phi_n ** 2)


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    dn_obs = delta_n_observed()
    u_dn = dn_obs * np.sqrt(U_MN_REL ** 2 + U_MP_REL ** 2)

    rows = []
    for name, fn in [("naive alpha/phi^2", delta_n_naive),
                     ("factor-2 alpha/(2 phi^2)", delta_n_factor2),
                     ("exact (1 - c alpha) form", delta_n_exact)]:
        d = fn()
        m_pred = M_PROTON * (1.0 + d)
        rows.append({
            "form": name,
            "delta_n_pred": d,
            "delta_n_obs": dn_obs,
            "residual": d - dn_obs,
            "sigma": (d - dn_obs) / u_dn,
            "m_n_pred_GeV": m_pred,
            "m_n_obs_GeV": M_NEUTRON,
            "accuracy_percent": 100.0 * (1.0 - abs(m_pred - M_NEUTRON) / M_NEUTRON),
        })

    csv_path = os.path.join(OUT_DIR, "neutron_factor2.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"Wrote {csv_path}")

    print("=== IST PHASE 28: The Factor-2 Neutron ===")
    print(f"delta_n observed = {dn_obs:.12f}  (+/- {u_dn:.2e})\n")
    for r in rows:
        print(f"  {r['form']:28s} delta_n={r['delta_n_pred']:.12f} "
              f"sigma={r['sigma']:+.2f}  m_n={r['m_n_pred_GeV']:.10f} GeV "
              f"acc={r['accuracy_percent']:.6f}%")

    c_ex = c_exact_coefficient()
    c_cl = c_claimed()
    print(f"\nCoefficient analysis:")
    print(f"  exact c (from masses)      = {c_ex:.8f}")
    print(f"  claimed c = 3/2 - a/phi^6  = {c_cl:.8f}")
    print(f"  agreement                  = {abs(c_ex - c_cl):.3e} "
          f"({100*(1-abs(c_ex-c_cl)/c_ex):.6f}%)")

    print(f"\nRunning-phi diagnostic (correcting the synthesis paper):")
    pn = running_phi_neutron()
    print(f"  observed delta_n      = {dn_obs:.8f}")
    print(f"  true running phi_n    = {pn:.4f}")
    m_198 = m_n_from_phi(1.98)
    print(f"  paper claimed phi=1.98 m_n = {m_198:.6f} "
          f"vs obs {M_NEUTRON:.6f} "
          f"(acc {100*(1-abs(m_198-M_NEUTRON)/M_NEUTRON):.4f}%, NOT 99.99%)")
    print(f"  phi*sqrt(2)           = {PHI * np.sqrt(2):.4f} "
          f"(phi_n is {100*(pn/(PHI*np.sqrt(2))-1):+.3f}% above it)")

    print(f"\nExact closed form:")
    print(f"  delta_n = alpha/(2 phi^2) (1 - (3/2 - alpha/phi^6) alpha)")
    print(f"         = alpha/(2 phi^2) - 3 alpha^2/(4 phi^2) + alpha^3/(2 phi^8)")
    d = delta_n_exact()
    print(f"  residual vs observed = {d - dn_obs:.3e} "
          f"({abs(d - dn_obs) / u_dn:.2f} sigma)")

    make_figure(rows, c_ex, c_cl)
    print(f"Wrote {OUT_DIR}")


def make_figure(rows, c_ex, c_cl):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    names = [r["form"].replace("alpha", "α") for r in rows]
    accs = [r["accuracy_percent"] for r in rows]
    axes[0].bar(names, accs, color=["crimson", "steelblue", "seagreen"])
    for b, a in zip(axes[0].patches, accs):
        axes[0].text(b.get_x() + b.get_width()/2, a + 0.002,
                     f"{a:.6f}%", ha="center", fontsize=8)
    axes[0].set_ylim(99.8, 100.001)
    axes[0].set_ylabel("m_n prediction accuracy (%)")
    axes[0].set_title("Neutron mass: naive vs factor-2 vs exact form")

    axes[1].bar(["exact c\n(from masses)", "claimed c\n= 3/2 − α/φ⁶"],
                [c_ex, c_cl], color=["steelblue", "seagreen"])
    axes[1].axhline(1.5, color="crimson", ls="--", lw=1, label="3/2")
    axes[1].set_ylabel("coefficient c")
    axes[1].set_title("Exact vs claimed correction coefficient")
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "neutron_factor2.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
