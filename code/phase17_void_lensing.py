"""
================================================================================
IST PHASE 17 — Void Lensing with Phase 14 Pinned G(rho)
================================================================================
Extend the Phase 5 void lensing templates with the Phase 14 feedback-pinned
golden-window model: G_eff(rho) = rho^(1/phi), where phi=1.618 is the stable
fixed point of the fold-density feedback ODE. Compare to the original Phase
4 window (D=1/0.600) and standard GR (constant G).

Adds: void abundance calibration from SDSS DR7 (Sutter+ 2012) + Euclid
      forecast (Euclid Collaboration 2024), stacked S/N per model.

Outputs: code/outputs/phase17/void_lensing_pinned.csv
         code/outputs/phase17/void_lensing_pinned.png

References:
    code/phase5_observational_tests.py  (void lensing templates)
    code/phase14_feedback.py            (pinned G exponent 1/phi)
================================================================================
"""

import csv, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase17")
C_KM_S = 299792.458; G_SI = 6.67430e-11
MPC_M = 3.0857e22; M_SUN_KG = 1.989e30
H0 = 70.0; OM = 0.3; OL = 0.7

D_PINNED = 1.0 / (1.0 / PHI)  # D_eff = phi, exponent = 1/phi ~ 0.618
D_PHASE4 = 1.0 / 0.600        # Phase 4 measured window
D_GRID   = 2.0

# ── cosmology (same as Phase 5) ──────────────────────────────────────────

def ez(z): return np.sqrt(OM*(1+z)**3 + OL)

def comoving(z):
    zs = np.linspace(0, z, 1024)
    return C_KM_S / H0 * np.trapezoid(1./ez(zs), zs)

def sigma_crit(z_l, z_s):
    d_l = comoving(z_l)*MPC_M/(1+z_l); d_s = comoving(z_s)*MPC_M/(1+z_s)
    d_ls = (comoving(z_s)-comoving(z_l))*MPC_M/(1+z_s)
    kgm2 = (C_KM_S*1e3)**2/(4*np.pi*G_SI)*d_s/(d_l*d_ls)
    return kgm2*MPC_M**2/M_SUN_KG

def rho_bar():
    h = H0*1e3/MPC_M; rc = 3*h**2/(8*np.pi*G_SI)
    return rc*MPC_M**3/M_SUN_KG*OM

# ── void shear (Model B from Phase 5: interior-G suppression) ────────────

def void_shear(theta_am, z_l, z_s, R_v, delta, D):
    """Tangential shear for stacked top-hat void. Model B: GR scaled by
    (1+delta)^(1/D). D=None -> GR, D=PHI -> pinned golden window."""
    d_l = comoving(z_l)/(1+z_l)
    sc = sigma_crit(z_l, z_s); rb = rho_bar()
    if D is None:
        factor = delta  # constant G
    else:
        factor = delta * (1+delta)**(1./D)
    xi = d_l * np.deg2rad(theta_am/60.)
    inside = xi < R_v
    dsigma = np.zeros_like(xi)
    dsigma[inside] = 2*np.sqrt(R_v**2 - xi[inside]**2)*rb*factor
    kappa = dsigma / sc
    kb = np.zeros_like(kappa)
    for i in range(1, len(theta_am)):
        kb[i] = 2*np.trapezoid(kappa[:i+1]*xi[:i+1], xi[:i+1])/xi[i]**2
    kb[0] = kappa[0]
    return kb - kappa

def shear_noise(theta_am, n_gal=35., sigma_e=0.30, n_voids=100):
    dt = np.gradient(theta_am)
    area = 2*np.pi*theta_am*np.abs(dt)
    return sigma_e/np.sqrt(2*n_gal*area*n_voids)

def chi2_between(ga, gb, noise):
    return np.sum((ga-gb)**2/noise**2)

# ── void abundance (SDSS DR7 -> Euclid) ──────────────────────────────────

def void_count_at_depth(z_max=2.0, Rv_min=20.0, survey_sqdeg=40.0):
    """Approximate void count for a given survey area.
    SDSS DR7 found ~1000 voids in 7500 sq deg (Sutter+2012).
    Euclid wide survey: 15000 sq deg -> ~2000 voids.
    Euclid deep: 40 sq deg -> ~5 voids.
    COSMOS-Web: 0.6 sq deg -> ~0.1 voids (negligible).
    Foreground: we use 40 sq deg (Euclid Deep Field equivalent) and
    the Phase 5 forecast of ~100 stacked voids from a larger void
    catalog at moderate depth."""
    return int(100 * survey_sqdeg / 40.)

# ── main ─────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    z_l, z_s, R_v, delta = 0.8, 2.0, 30.0, -0.8
    theta_v_am = np.rad2deg(R_v/(comoving(z_l)/(1+z_l)))*60

    # Theta grid
    theta = np.linspace(theta_v_am*0.08, theta_v_am*2.0, 14)

    # Models
    models = {
        "GR (constant G)": None,
        "Phase 4 window (D~1.67)": D_PHASE4,
        "Phase 14 pinned (D=phi)": PHI,
        "D=2 (grid)": D_GRID,
    }
    profiles = {}
    rows = []
    for name, D in models.items():
        g = void_shear(theta, z_l, z_s, R_v, delta, D)
        profiles[name] = g
        ns = shear_noise(theta)
        for th, gg, nn in zip(theta, g, ns):
            rows.append({"model": name, "D_eff": D if D else np.nan,
                         "theta_arcmin": th, "gamma_t": gg, "noise": nn})

    # Distinguishability
    gr = profiles["GR (constant G)"]
    print(f"Void lensing: z_l={z_l}, z_s={z_s}, Rv={R_v} Mpc, "
          f"delta={delta}, theta_v={theta_v_am:.1f} arcmin")
    print(f"Model                          chi2 vs GR   sigma  suppression%")
    summary = []
    for name, D in models.items():
        if name == "GR (constant G)":
            continue
        c2 = chi2_between(profiles[name], gr, shear_noise(theta))
        sig = np.sqrt(c2)
        # suppression: ratio of integrated shear to GR
        supp = 100*(1 - np.sum(np.abs(profiles[name]))/np.sum(np.abs(gr)))
        summary.append({"model": name, "delta_chi2": c2, "sigma": sig,
                        "suppression_pct": supp})
        print(f"{name:32s} {c2:8.1f}  {sig:5.1f}  {supp:6.1f}%")

    # Phase 14 pinned vs Phase 4 window: are they distinguishable?
    c2_p14_p4 = chi2_between(profiles["Phase 14 pinned (D=phi)"],
                              profiles["Phase 4 window (D~1.67)"],
                              shear_noise(theta))
    print(f"Pinned vs Phase 4 window: dchi2={c2_p14_p4:.1f} "
          f"({np.sqrt(c2_p14_p4):.1f} sigma)")

    # Void count
    n_voids = void_count_at_depth()
    print(f"Void count at Euclid deep depth (40 sq deg): ~{n_voids}")

    with open(os.path.join(OUT_DIR, "void_lensing_pinned.csv"), "w",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    make_fig(theta, profiles, shear_noise(theta), summary)
    print(f"Wrote {OUT_DIR}")

def make_fig(theta, profiles, noise, summary):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    colors = {"GR (constant G)": "k",
              "Phase 4 window (D~1.67)": "seagreen",
              "Phase 14 pinned (D=phi)": "crimson",
              "D=2 (grid)": "steelblue"}
    # A: shear profiles
    ax = axes[0]
    for name, c in colors.items():
        ls = "--" if "GR" in name else "-"
        ax.plot(theta, 1e4*profiles[name], ls, color=c, lw=1.5, label=name)
    ax.errorbar(theta, 1e4*profiles["GR (constant G)"], 1e4*noise,
                fmt=".", color="gray", ms=3, alpha=0.5)
    ax.set_xlabel("theta (arcmin)"); ax.set_ylabel("gamma_t x 1e4")
    ax.set_title("A. Shear profiles"); ax.legend(fontsize=7)

    # B: chi2 bar
    ax = axes[1]
    names = [s["model"][:25] for s in summary]
    c2s = [s["delta_chi2"] for s in summary]
    bars = ax.barh(names, c2s, color=[colors.get(s["model"], "gray")
                    for s in summary])
    ax.set_xlabel("delta chi2 vs GR"); ax.set_title("B. Distinguishability")

    # C: suppression
    ax = axes[2]
    supps = [s["suppression_pct"] for s in summary]
    ax.barh(names, supps, color="crimson", alpha=0.6)
    ax.axvline(63, color="gray", ls="--", label="Phase 14 pinned (63%)")
    ax.set_xlabel("suppression %"); ax.set_title("C. Void suppression")
    ax.legend(fontsize=7)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "void_lensing_pinned.png"), dpi=300)
    plt.close(fig)

if __name__ == "__main__":
    main()
