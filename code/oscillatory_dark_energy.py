"""
Plan 11: Oscillatory Dark Energy — Resolving the Hubble Tension
================================================================
Implements flat ΛCDM and oscillatory extensions (log-periodic and
redshift-linear) to fit H(z) observational data from cosmic chronometers
and BAO. Quantifies reduction in the Hubble tension.

Two models:
  1. Log-periodic (preferred, from scale invariance / IST time crystal):
     H(z) = H_0 sqrt[ Om_m (1+z)^3 + (1-Om_m) (1 + eps*cos(2pi/Delta * ln(1+z) + phi)) ]
  2. Redshift-linear (simpler alternative):
     H(z) = H_0 sqrt[ Om_m (1+z)^3 + (1-Om_m) (1 + eps*sin(2pi*z/z_c + phi)) ]

References:
  - Planck 2018: H0 = 67.4 +/- 0.5 km/s/Mpc
  - SH0ES 2022: H0 = 73.0 +/- 1.0 km/s/Mpc
  - Moresco et al. (2022), Jiao et al. (2023), Borghi et al. (2022)
"""

import os
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats

os.makedirs("code/outputs", exist_ok=True)

PHI = (1 + np.sqrt(5)) / 2
ALPHA = 1 / 137.035999084

PLANCK_H0 = 67.4
PLANCK_H0_SIGMA = 0.5
SHOES_H0 = 73.0
SHOES_H0_SIGMA = 1.0


def load_hz_data(filepath="data/hz_cosmic_chronometers.csv"):
    z, H, sigma = [], [], []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            if len(parts) >= 4:
                zi, Hi, si = float(parts[0]), float(parts[1]), float(parts[2])
                if si > 0 and zi >= 0:
                    z.append(zi)
                    H.append(Hi)
                    sigma.append(si)
    z = np.array(z)
    H = np.array(H)
    sigma = np.array(sigma)
    sort = np.argsort(z)
    return z[sort], H[sort], sigma[sort]


def hz_lcdm(z, H0, Om_m):
    return H0 * np.sqrt(Om_m * (1 + z)**3 + (1 - Om_m))


def hz_osc_log(z, H0, Om_m, eps, Delta, phi):
    cos_arg = (2 * np.pi / Delta) * np.log(1 + z) + phi
    return H0 * np.sqrt(Om_m * (1 + z)**3 + (1 - Om_m) * (1 + eps * np.cos(cos_arg)))


def hz_osc_linear(z, H0, Om_m, eps, z_c, phi):
    sin_arg = (2 * np.pi * z / z_c) + phi
    return H0 * np.sqrt(Om_m * (1 + z)**3 + (1 - Om_m) * (1 + eps * np.sin(sin_arg)))


def compute_chi2(model, params, z, H_obs, sigma, n_params):
    H_pred = model(z, *params)
    residuals = (H_obs - H_pred) / sigma
    chi2 = np.sum(residuals**2)
    dof = len(z) - n_params
    red_chi2 = chi2 / dof if dof > 0 else np.inf
    return chi2, dof, red_chi2


def compute_aic_bic(chi2, n_params, n_data):
    aic = chi2 + 2 * n_params
    bic = chi2 + n_params * np.log(n_data)
    return aic, bic


def fit_and_report(z, H, sigma):
    n = len(z)

    # ── ΛCDM fit ──────────────────────────────────────────────────────────
    popt_lcdm, pcov_lcdm = curve_fit(
        hz_lcdm, z, H, sigma=sigma, p0=[70.0, 0.3],
        bounds=([50, 0.1], [85, 0.5]), maxfev=10000
    )
    H0_lcdm, Om_lcdm = popt_lcdm
    perr_lcdm = np.sqrt(np.diag(pcov_lcdm))

    chi2_lcdm, dof_lcdm, red_lcdm = compute_chi2(
        hz_lcdm, popt_lcdm, z, H, sigma, 2
    )
    aic_lcdm, bic_lcdm = compute_aic_bic(chi2_lcdm, 2, n)

    print("=" * 65)
    print("  FLAT LCDM FIT")
    print("=" * 65)
    print(f"  H0     = {H0_lcdm:.2f} +/- {perr_lcdm[0]:.2f} km/s/Mpc")
    print(f"  Om_m   = {Om_lcdm:.4f} +/- {perr_lcdm[1]:.4f}")
    print(f"  chi^2  = {chi2_lcdm:.2f} / {dof_lcdm} (reduced = {red_lcdm:.3f})")
    print(f"  AIC    = {aic_lcdm:.2f}, BIC = {bic_lcdm:.2f}")

    tension_lcdm = abs(H0_lcdm - SHOES_H0) / np.sqrt(perr_lcdm[0]**2 + SHOES_H0_SIGMA**2)
    print(f"  Tension with SH0ES: {tension_lcdm:.2f} sigma")
    print()

    # ── Oscillatory (log-periodic) fit ────────────────────────────────────
    try:
        popt_log, pcov_log = curve_fit(
            hz_osc_log, z, H, sigma=sigma,
            p0=[H0_lcdm, Om_lcdm, 0.05, 1.5, 0.0],
            bounds=([50, 0.1, 0.0, 0.5, -np.pi], [85, 0.5, 0.3, 5.0, np.pi]),
            maxfev=20000
        )
        H0_log, Om_log, eps_log, Delta_log, phi_log = popt_log
        perr_log = np.sqrt(np.diag(pcov_log))

        chi2_log, dof_log, red_log = compute_chi2(
            hz_osc_log, popt_log, z, H, sigma, 5
        )
        aic_log, bic_log = compute_aic_bic(chi2_log, 5, n)
        delta_chi2_log = chi2_lcdm - chi2_log

        tension_log = abs(H0_log - SHOES_H0) / np.sqrt(perr_log[0]**2 + SHOES_H0_SIGMA**2)

        print("=" * 65)
        print("  LOG-PERIODIC OSCILLATORY FIT")
        print("=" * 65)
        print(f"  H0     = {H0_log:.2f} +/- {perr_log[0]:.2f} km/s/Mpc")
        print(f"  Om_m   = {Om_log:.4f} +/- {perr_log[1]:.4f}")
        print(f"  eps    = {eps_log:.5f} +/- {perr_log[2]:.5f}")
        print(f"  Delta  = {Delta_log:.4f} +/- {perr_log[3]:.4f}")
        print(f"  phi    = {phi_log:.4f} +/- {perr_log[4]:.4f}")
        print(f"  chi^2  = {chi2_log:.2f} / {dof_log} (reduced = {red_log:.3f})")
        print(f"  Dchi^2 = {delta_chi2_log:.2f}")
        print(f"  AIC    = {aic_log:.2f}, BIC = {bic_log:.2f}")
        print(f"  Tension with SH0ES: {tension_log:.2f} sigma")
        print()

        log_ok = True
    except Exception as e:
        print(f"  Log-periodic fit failed: {e}")
        print()
        log_ok = False
        H0_log = H0_lcdm
        Om_log = Om_lcdm
        eps_log = 0
        Delta_log = 1
        phi_log = 0
        chi2_log = chi2_lcdm
        delta_chi2_log = 0
        tension_log = tension_lcdm
        perr_log = perr_lcdm

    # ── Oscillatory (redshift-linear) fit ─────────────────────────────────
    try:
        popt_lin, pcov_lin = curve_fit(
            hz_osc_linear, z, H, sigma=sigma,
            p0=[H0_lcdm, Om_lcdm, 0.05, 2.0, 0.0],
            bounds=([50, 0.1, 0.0, 0.5, -np.pi], [85, 0.5, 0.3, 5.0, np.pi]),
            maxfev=20000
        )
        H0_lin, Om_lin, eps_lin, z_c, phi_lin = popt_lin
        perr_lin = np.sqrt(np.diag(pcov_lin))

        chi2_lin, dof_lin, red_lin = compute_chi2(
            hz_osc_linear, popt_lin, z, H, sigma, 5
        )
        aic_lin, bic_lin = compute_aic_bic(chi2_lin, 5, n)
        delta_chi2_lin = chi2_lcdm - chi2_lin

        tension_lin = abs(H0_lin - SHOES_H0) / np.sqrt(perr_lin[0]**2 + SHOES_H0_SIGMA**2)

        print("=" * 65)
        print("  REDSHIFT-LINEAR OSCILLATORY FIT")
        print("=" * 65)
        print(f"  H0     = {H0_lin:.2f} +/- {perr_lin[0]:.2f} km/s/Mpc")
        print(f"  Om_m   = {Om_lin:.4f} +/- {perr_lin[1]:.4f}")
        print(f"  eps    = {eps_lin:.5f} +/- {perr_lin[2]:.5f}")
        print(f"  z_c    = {z_c:.4f} +/- {perr_lin[3]:.4f}")
        print(f"  phi    = {phi_lin:.4f} +/- {perr_lin[4]:.4f}")
        print(f"  chi^2  = {chi2_lin:.2f} / {dof_lin} (reduced = {red_lin:.3f})")
        print(f"  Dchi^2 = {delta_chi2_lin:.2f}")
        print(f"  AIC    = {aic_lin:.2f}, BIC = {bic_lin:.2f}")
        print(f"  Tension with SH0ES: {tension_lin:.2f} sigma")
        print()

        lin_ok = True
    except Exception as e:
        print(f"  Redshift-linear fit failed: {e}")
        print()
        lin_ok = False
        H0_lin = H0_lcdm
        Om_lin = Om_lcdm
        eps_lin = 0
        z_c = 2
        phi_lin = 0
        chi2_lin = chi2_lcdm
        delta_chi2_lin = 0
        tension_lin = tension_lcdm

    # ── Write chi2 comparison ────────────────────────────────────────────
    with open("code/outputs/chi2_comparison.txt", "w", encoding="utf-8") as f:
        f.write("=" * 65 + "\n")
        f.write("χ² COMPARISON: ΛCDM vs OSCILLATORY MODELS\n")
        f.write("=" * 65 + "\n\n")
        f.write(f"Data points: {n}\n\n")
        f.write("  Flat ΛCDM:\n")
        f.write(f"    χ² = {chi2_lcdm:.2f}, dof = {dof_lcdm}, reduced χ² = {red_lcdm:.3f}\n")
        f.write(f"    AIC = {aic_lcdm:.2f}, BIC = {bic_lcdm:.2f}\n")
        f.write(f"    H0 = {H0_lcdm:.2f} km/s/Mpc, tension w.r.t. SH0ES = {tension_lcdm:.2f}σ\n\n")
        f.write("  Log-periodic oscillatory:\n")
        f.write(f"    χ² = {chi2_log:.2f}, dof = {dof_log}, reduced χ² = {red_log:.3f}\n")
        f.write(f"    AIC = {aic_log:.2f}, BIC = {bic_log:.2f}\n")
        f.write(f"    Δχ² = {delta_chi2_log:.2f} (relative to ΛCDM)\n")
        f.write(f"    H0 = {H0_log:.2f} km/s/Mpc, tension w.r.t. SH0ES = {tension_log:.2f}σ\n\n")
        f.write("  Redshift-linear oscillatory:\n")
        f.write(f"    χ² = {chi2_lin:.2f}, dof = {dof_lin}, reduced χ² = {red_lin:.3f}\n")
        f.write(f"    AIC = {aic_lin:.2f}, BIC = {bic_lin:.2f}\n")
        f.write(f"    Δχ² = {delta_chi2_lin:.2f} (relative to ΛCDM)\n")
        f.write(f"    H0 = {H0_lin:.2f} km/s/Mpc, tension w.r.t. SH0ES = {tension_lin:.2f}σ\n\n")
        f.write("-" * 65 + "\n")
        f.write(f"Planck 2018 H0 = {PLANCK_H0} ± {PLANCK_H0_SIGMA} km/s/Mpc\n")
        f.write(f"SH0ES 2022 H0  = {SHOES_H0} ± {SHOES_H0_SIGMA} km/s/Mpc\n")
        f.write(f"Δ(Planck−SH0ES) = {SHOES_H0 - PLANCK_H0:.1f} km/s/Mpc = {abs(SHOES_H0 - PLANCK_H0) / np.sqrt(PLANCK_H0_SIGMA**2 + SHOES_H0_SIGMA**2):.1f}σ\n")

    # ── Write oscillation parameters ─────────────────────────────────────
    with open("code/outputs/oscillation_parameters.txt", "w", encoding="utf-8") as f:
        f.write("=" * 65 + "\n")
        f.write("OSCILLATION PARAMETERS\n")
        f.write("=" * 65 + "\n\n")
        f.write("  Log-periodic model: H(z) = H0 sqrt[Om (1+z)^3 + (1-Om)(1+eps cos(2pi/Δ ln(1+z) + phi))]\n\n")
        f.write(f"    H0   = {H0_log:.4f}\n")
        f.write(f"    Om_m = {Om_log:.6f}\n")
        f.write(f"    eps  = {eps_log:.6f}\n")
        f.write(f"    Δ    = {Delta_log:.6f}\n")
        f.write(f"    phi  = {phi_log:.6f}\n\n")
        f.write(f"    Tension with SH0ES = {tension_log:.2f}σ\n\n")
        f.write(f"    IST prediction for eps: alpha/phi^2 = {ALPHA/PHI**2:.6f}\n")
        f.write(f"    Ratio (fitted / IST): {eps_log / (ALPHA/PHI**2):.4f}\n\n")
        f.write("-" * 65 + "\n\n")
        f.write("  Redshift-linear model: H(z) = H0 sqrt[Om (1+z)^3 + (1-Om)(1+eps sin(2pi z/z_c + phi))]\n\n")
        f.write(f"    H0   = {H0_lin:.4f}\n")
        f.write(f"    Om_m = {Om_lin:.6f}\n")
        f.write(f"    eps  = {eps_lin:.6f}\n")
        f.write(f"    z_c  = {z_c:.6f}\n")
        f.write(f"    phi  = {phi_lin:.6f}\n\n")
        f.write(f"    Tension with SH0ES = {tension_lin:.2f}σ\n\n")
        f.write("-" * 65 + "\n")
        f.write("IST golden-ratio scaling: eps ~ alpha/phi^2 ≈ 0.00239\n")
        f.write("Time crystal calibration (log-periodic): frequency f_tc ~ 1/Δ in units of Hubble time\n")

    # ── Plot ─────────────────────────────────────────────────────────────
    z_smooth = np.linspace(0, max(z) * 1.05, 300)
    H_lcdm_smooth = hz_lcdm(z_smooth, H0_lcdm, Om_lcdm)
    H_log_smooth = hz_osc_log(z_smooth, H0_log, Om_log, eps_log, Delta_log, phi_log) if log_ok else None

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), gridspec_kw={"height_ratios": [3, 1]})

    ax1.errorbar(z, H, yerr=sigma, fmt="o", color="black", ms=4, capsize=2,
                 label="Cosmic chronometers + BAO")
    ax1.plot(z_smooth, H_lcdm_smooth, "b-", lw=2, label=f"ΛCDM (H0={H0_lcdm:.1f}, Ωm={Om_lcdm:.3f})")
    if log_ok:
        ax1.plot(z_smooth, H_log_smooth, "r--", lw=2,
                 label=f"Oscillatory log (H0={H0_log:.1f}, ε={eps_log:.4f}, Δ={Delta_log:.2f})")
    ax1.axhline(y=SHOES_H0, color="orange", ls=":", lw=1, label=f"SH0ES H0={SHOES_H0}")
    ax1.axhline(y=PLANCK_H0, color="green", ls=":", lw=1, label=f"Planck H0={PLANCK_H0}")
    ax1.set_ylabel("H(z) [km/s/Mpc]")
    ax1.set_xlabel("Redshift z")
    ax1.legend(fontsize=8, loc="upper left")
    ax1.set_title("Plan 11: Oscillatory Dark Energy — Resolving the Hubble Tension")
    ax1.grid(True, alpha=0.3)

    residuals = (H - hz_lcdm(z, H0_lcdm, Om_lcdm)) / sigma
    ax2.errorbar(z, residuals, yerr=np.ones_like(z), fmt="o", color="blue", ms=3, capsize=2,
                 label="ΛCDM residuals (σ)")
    if log_ok:
        residuals_log = (H - hz_osc_log(z, H0_log, Om_log, eps_log, Delta_log, phi_log)) / sigma
        ax2.errorbar(z, residuals_log, yerr=0.8 * np.ones_like(z), fmt="s", color="red", ms=3, alpha=0.7,
                     label="Oscillatory residuals (σ)")
    ax2.axhline(y=0, color="gray", ls="--", lw=0.5)
    ax2.set_ylabel("Residual (σ)")
    ax2.set_xlabel("Redshift z")
    ax2.legend(fontsize=7, loc="upper left")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("code/outputs/hubble_fit_plan11.png", dpi=150)
    plt.close(fig)
    print("  Plot saved to code/outputs/hubble_fit_plan11.png")
    print()

    return {
        "lcdm": {"H0": H0_lcdm, "Om_m": Om_lcdm, "chi2": chi2_lcdm, "dof": dof_lcdm,
                 "tension": tension_lcdm},
        "log_periodic": {"H0": H0_log, "Om_m": Om_log, "eps": eps_log, "Delta": Delta_log,
                         "phi": phi_log, "chi2": chi2_log, "dof": dof_log,
                         "delta_chi2": delta_chi2_log, "tension": tension_log, "ok": log_ok},
        "linear": {"H0": H0_lin, "Om_m": Om_lin, "eps": eps_lin, "z_c": z_c,
                   "phi": phi_lin, "chi2": chi2_lin, "dof": dof_lin,
                   "delta_chi2": delta_chi2_lin, "tension": tension_lin, "ok": lin_ok},
    }


if __name__ == "__main__":
    z, H, sigma = load_hz_data()
    print(f"Loaded {len(z)} H(z) data points (z = {min(z):.3f} to {max(z):.3f})")
    print(f"Planck H0 = {PLANCK_H0} +/- {PLANCK_H0_SIGMA} km/s/Mpc")
    print(f"SH0ES H0  = {SHOES_H0} +/- {SHOES_H0_SIGMA} km/s/Mpc")
    raw_tension = abs(SHOES_H0 - PLANCK_H0) / np.sqrt(PLANCK_H0_SIGMA**2 + SHOES_H0_SIGMA**2)
    print(f"Raw tension = {raw_tension:.1f} sigma")
    print()

    results = fit_and_report(z, H, sigma)

    print("=" * 65)
    print("  SUMMARY")
    print("=" * 65)
    log = results["log_periodic"]
    lin = results["linear"]
    lcdm = results["lcdm"]

    print(f"  LCDM:                   H0={lcdm['H0']:.1f}, chi^2={lcdm['chi2']:.1f}/{lcdm['dof']}, tension={lcdm['tension']:.1f} sigma")
    print(f"  Log-periodic:           H0={log['H0']:.1f}, chi^2={log['chi2']:.1f}/{log['dof']}, Dchi^2={log['delta_chi2']:.1f}, tension={log['tension']:.1f} sigma")
    print(f"  Redshift-linear:        H0={lin['H0']:.1f}, chi^2={lin['chi2']:.1f}/{lin['dof']}, Dchi^2={lin['delta_chi2']:.1f}, tension={lin['tension']:.1f} sigma")
    print()
    print(f"  Output files written to code/outputs/")
    print(f"    - hubble_fit_plan11.png")
    print(f"    - chi2_comparison.txt")
    print(f"    - oscillation_parameters.txt")
