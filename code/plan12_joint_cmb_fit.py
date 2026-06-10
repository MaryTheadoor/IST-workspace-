"""
Plan 12 — Task 3: Joint Fit with Planck CMB Gaussian Priors
=============================================================
Combines the oscillatory log-periodic dark energy model with
Planck 2018 derived parameter constraints as Gaussian priors.

Uses the compressed likelihood approach: Planck chains give
posterior constraints on (H0, Omega_m, omega_b h^2) which we
use as Gaussian priors alongside H(z) data.

References:
  - Planck 2018 VI, A&A 641, A6 (2020): cosmological parameters
  - Plan 7 master equation, Plan 11 oscillatory model, Plan 12 spec
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize

os.makedirs("code/outputs", exist_ok=True)

PHI = (1 + np.sqrt(5)) / 2
ALPHA = 1 / 137.035999084
COUPLING = ALPHA / PHI**2

SHOES_H0 = 73.0
SHOES_H0_SIGMA = 1.0

PLANCK_H0 = 67.36
PLANCK_H0_SIGMA = 0.54
PLANCK_OM = 0.3153
PLANCK_OM_SIGMA = 0.0073
PLANCK_OB = 0.02236
PLANCK_OB_SIGMA = 0.00015


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
    z, H, sigma = np.array(z), np.array(H), np.array(sigma)
    sort = np.argsort(z)
    return z[sort], H[sort], sigma[sort]


def hz_osc_log(z, H0, Om_m, eps, Delta, phi):
    cos_arg = (2 * np.pi / Delta) * np.log(1 + z) + phi
    return H0 * np.sqrt(Om_m * (1 + z)**3 + (1 - Om_m) * (1 + eps * np.cos(cos_arg)))


def hz_osc_fixed(z, H0, Om_m, eps, phi):
    """Log-periodic with Delta = PHI fixed."""
    return hz_osc_log(z, H0, Om_m, eps, PHI, phi)


def total_chi2(params, z_hz, H_hz, sigma_hz):
    """Combined chi^2 from H(z) data + Planck Gaussian priors.

    params = [H0, Om_m, eps, Delta, phi, omega_b]
    """
    H0, Om_m, eps, Delta, phi, omega_b = params

    chi2_hz = np.sum(((H_hz - hz_osc_log(z_hz, H0, Om_m, eps, Delta, phi)) / sigma_hz)**2)

    chi2_cmb = 0.0
    chi2_cmb += ((omega_b - PLANCK_OB) / PLANCK_OB_SIGMA)**2
    chi2_cmb += ((Om_m - PLANCK_OM) / PLANCK_OM_SIGMA)**2
    chi2_cmb += ((H0 - PLANCK_H0) / PLANCK_H0_SIGMA)**2

    return chi2_hz + chi2_cmb


def fit_joint(z_hz, H_hz, sigma_hz, fixed_delta=False):
    n_data_hz = len(z_hz)
    n_data_cmb = 3
    n_free = 6
    if fixed_delta:
        n_free = 5

    p0 = [70.0, 0.30, 0.05, 1.54, 0.0, PLANCK_OB]
    bounds = [(60, 80), (0.15, 0.40), (0.0, 0.3), (0.5, 5.0),
              (-np.pi, np.pi), (0.021, 0.024)]
    if fixed_delta:
        p0[3] = PHI
        bounds[3] = (PHI - 1e-6, PHI + 1e-6)

    result = minimize(
        lambda p: total_chi2(p, z_hz, H_hz, sigma_hz),
        p0, method="L-BFGS-B", bounds=bounds,
        options={"maxiter": 10000, "ftol": 1e-8}
    )
    popt = result.x
    chi2_total = result.fun

    H0, Om_m, eps, Delta_use, phi_use, omega_b = popt
    chi2_hz = np.sum(((H_hz - hz_osc_log(z_hz, H0, Om_m, eps, Delta_use, phi_use)) / sigma_hz)**2)
    chi2_cmb = chi2_total - chi2_hz

    return popt, chi2_total, chi2_hz, chi2_cmb, n_free, n_data_hz + n_data_cmb


if __name__ == "__main__":
    print("=" * 72)
    print("  PLAN 12 — TASK 3: JOINT FIT (H(z) + PLANCK GAUSSIAN PRIORS)")
    print("=" * 72)
    print()

    z, H, sigma = load_hz_data()
    print(f"  H(z) data: {len(z)} points (z = {min(z):.3f} to {max(z):.3f})")
    print(f"  Planck priors: H0={PLANCK_H0}+/-{PLANCK_H0_SIGMA}, "
          f"Om={PLANCK_OM}+/-{PLANCK_OM_SIGMA}, ob={PLANCK_OB}+/-{PLANCK_OB_SIGMA}")
    print()

    # Model A
    print("  Fitting Model A: Free log-periodic + Planck priors...")
    popt_A, c2_A, c2hz_A, c2cmb_A, nfree_A, ndata_A = fit_joint(z, H, sigma)
    H0_A, Om_A, eps_A, Delta_A, phi_A, ob_A = popt_A
    dof_A = ndata_A - nfree_A
    tension_A = abs(H0_A - SHOES_H0) / SHOES_H0_SIGMA

    print(f"  H0       = {H0_A:.2f} km/s/Mpc")
    print(f"  Om_m     = {Om_A:.4f}")
    print(f"  eps      = {eps_A:.5f}")
    print(f"  Delta    = {Delta_A:.4f}")
    print(f"  phi_0    = {phi_A:.4f}")
    print(f"  omega_b  = {ob_A:.5f}")
    print(f"  chi^2_HZ = {c2hz_A:.1f}")
    print(f"  chi^2_CMB= {c2cmb_A:.1f}")
    print(f"  chi^2_tot= {c2_A:.1f} / {dof_A}")
    print(f"  Tension  = {tension_A:.1f} sigma")
    print()

    # Model B: Fixed Delta = phi
    print("  Fitting Model B: Delta=phi + Planck priors...")
    popt_B, c2_B, c2hz_B, c2cmb_B, nfree_B, ndata_B = fit_joint(z, H, sigma, fixed_delta=True)
    H0_B, Om_B, eps_B, _, phi_B, ob_B = popt_B
    dof_B = ndata_B - nfree_B
    dchi2_AB = c2_B - c2_A
    tension_B = abs(H0_B - SHOES_H0) / SHOES_H0_SIGMA

    print(f"  H0       = {H0_B:.2f} km/s/Mpc")
    print(f"  Om_m     = {Om_B:.4f}")
    print(f"  eps      = {eps_B:.5f}")
    print(f"  Delta    = PHI ({PHI:.4f}) [FIXED]")
    print(f"  phi_0    = {phi_B:.4f}")
    print(f"  omega_b  = {ob_B:.5f}")
    print(f"  chi^2_HZ = {c2hz_B:.1f}")
    print(f"  chi^2_CMB= {c2cmb_B:.1f}")
    print(f"  chi^2_tot= {c2_B:.1f} / {dof_B}")
    print(f"  Delta chi^2 vs free = {dchi2_AB:.2f}")
    print(f"  Tension  = {tension_B:.1f} sigma")
    print()

    # Summary
    print("=" * 72)
    print("  JOINT FIT SUMMARY (H(z) + Planck Gaussian Priors)")
    print("=" * 72)
    print(f"  {'Model':<30} {'H0':>8} {'Om_m':>8} {'chi2/dof':>10} {'Tension':>8} {'omega_b':>10}")
    print(f"  {'-'*72}")
    print(f"  {'Planck LCDM':<30} {PLANCK_H0:>8.2f} {PLANCK_OM:>8.4f} {'---':>10} {'---':>8} {PLANCK_OB:>10.5f}")
    print(f"  {'A. Free + CMB':<30} {H0_A:>8.2f} {Om_A:>8.4f} {f'{c2_A:.1f}/{dof_A}':>10} {f'{tension_A:.1f} sigma':>8} {ob_A:>10.5f}")
    print(f"  {'B. Delta=phi + CMB':<30} {H0_B:>8.2f} {Om_B:>8.4f} {f'{c2_B:.1f}/{dof_B}':>10} {f'{tension_B:.1f} sigma':>8} {ob_B:>10.5f}")
    print()
    print(f"  Om_m agreement: free={abs(Om_A-PLANCK_OM)/PLANCK_OM_SIGMA:.1f} sigma, "
          f"fixed={abs(Om_B-PLANCK_OM)/PLANCK_OM_SIGMA:.1f} sigma")
    print(f"  Delta chi^2 (fixed Delta=phi): {dchi2_AB:.2f} for 1 param removed")
    print()

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax = axes[0]
    z_smooth = np.linspace(0, 2.5, 200)
    ax.errorbar(z, H, yerr=sigma, fmt="o", color="black", ms=3, capsize=2, alpha=0.5, label="H(z) data")
    ax.plot(z_smooth, hz_osc_log(z_smooth, H0_A, Om_A, eps_A, Delta_A, phi_A), "k-", lw=1.5, label="A. Free + CMB")
    ax.plot(z_smooth, hz_osc_fixed(z_smooth, H0_B, Om_B, eps_B, phi_B), "r--", lw=1.5, label="B. Delta=phi + CMB")
    ax.axhline(y=SHOES_H0, color="orange", ls=":", lw=0.8, label=f"SH0ES H0={SHOES_H0}")
    ax.axhline(y=PLANCK_H0, color="green", ls=":", lw=0.8, label=f"Planck H0={PLANCK_H0}")
    ax.set_xlabel("Redshift z")
    ax.set_ylabel("H(z) [km/s/Mpc]")
    ax.legend(fontsize=7, loc="upper left")
    ax.set_title("Joint Fit: H(z) + Planck Gaussian Priors")
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    ax.axvline(x=PLANCK_OM, color="green", ls="-", lw=2, alpha=0.5, label="Planck LCDM")
    ax.axvspan(PLANCK_OM - PLANCK_OM_SIGMA, PLANCK_OM + PLANCK_OM_SIGMA, color="green", alpha=0.1)
    ax.axhline(y=SHOES_H0, color="orange", ls="-", lw=2, alpha=0.5, label=f"SH0ES H0={SHOES_H0}")
    ax.axhspan(SHOES_H0 - SHOES_H0_SIGMA, SHOES_H0 + SHOES_H0_SIGMA, color="orange", alpha=0.1)
    ax.errorbar([Om_A], [H0_A], xerr=0.005, yerr=1.0, fmt="o", color="black", ms=8, label=f"A. Free")
    ax.errorbar([Om_B], [H0_B], xerr=0.005, yerr=1.0, fmt="s", color="red", ms=8, label=f"B. Delta=phi")
    ax.set_xlabel("Omega_m")
    ax.set_ylabel("H0 [km/s/Mpc]")
    ax.set_title("Omega_m — H0 Joint Constraints")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.22, 0.40)
    ax.set_ylim(62, 78)

    plt.tight_layout()
    plt.savefig("code/outputs/plan12_cmb_constraints.png", dpi=150)
    plt.close(fig)

    with open("code/outputs/plan12_joint_fit.txt", "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("PLAN 12 — TASK 3: JOINT FIT (H(z) + PLANCK GAUSSIAN PRIORS)\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Model A (Free + CMB): H0={H0_A:.2f}, Om={Om_A:.4f}, ")
        f.write(f"eps={eps_A:.5f}, Delta={Delta_A:.4f}, ob={ob_A:.5f}\n")
        f.write(f"  chi^2_tot={c2_A:.1f} (HZ={c2hz_A:.1f} + CMB={c2cmb_A:.1f}) / {dof_A}\n\n")
        f.write(f"Model B (Delta=phi + CMB): H0={H0_B:.2f}, Om={Om_B:.4f}, ")
        f.write(f"eps={eps_B:.5f}, Delta=PHI={PHI:.4f}, ob={ob_B:.5f}\n")
        f.write(f"  chi^2_tot={c2_B:.1f} (HZ={c2hz_B:.1f} + CMB={c2cmb_B:.1f}) / {dof_B}\n\n")
        f.write(f"Delta chi^2 (B vs A) = {dchi2_AB:.2f} (1 param)\n")
        f.write(f"Om vs Planck: A={abs(Om_A-PLANCK_OM)/PLANCK_OM_SIGMA:.1f} sigma, "
                f"B={abs(Om_B-PLANCK_OM)/PLANCK_OM_SIGMA:.1f} sigma\n")
        f.write(f"H0 vs Planck: A={abs(H0_A-PLANCK_H0)/PLANCK_H0_SIGMA:.1f} sigma, "
                f"B={abs(H0_B-PLANCK_H0)/PLANCK_H0_SIGMA:.1f} sigma\n")
        f.write(f"Tension w/ SH0ES: A={tension_A:.1f} sigma, B={tension_B:.1f} sigma\n\n")
        f.write(f"N_inflation(B) = eps_B / {COUPLING:.6f} = {eps_B/COUPLING:.1f}\n")

    print("  Output files:")
    print("    code/outputs/plan12_cmb_constraints.png")
    print("    code/outputs/plan12_joint_fit.txt")
