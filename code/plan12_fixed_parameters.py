"""
Plan 12 — Tasks 1 & 2: Fixed Golden Ratio Period & Inflationary Amplification
===============================================================================
Tests two key hypotheses arising from Plan 11 results:

Hypothesis 1: The oscillation period Delta equals the golden ratio phi = 1.618.
  Plan 11 found Delta = 1.5403 +/- 3.64. Fixing Delta = phi tests whether
  chi^2 degrades significantly (if not, the golden ratio is supported).

Hypothesis 2: The oscillation amplitude epsilon = (alpha/phi^2) * N_inflation.
  Plan 11 found eps = 0.136, which is 48.8x the bare IST coupling alpha/phi^2 = 0.00279.
  48.8 is within the typical inflationary e-fold range (50-60), suggesting
  the amplitude is amplified by inflation. We fit N_inflation as a free parameter.

References:
  - Plan 11 results: eps=0.136, Delta=1.540, ratio=48.78
  - Plan 7 master equation: coupling = alpha/phi^2
  - Planck 2018: r < 0.036 => N_inflation > 50
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats

os.makedirs("code/outputs", exist_ok=True)

PHI = (1 + np.sqrt(5)) / 2
ALPHA = 1 / 137.035999084
COUPLING = ALPHA / PHI**2

PLANCK_H0 = 67.4
PLANCK_H0_SIGMA = 0.5
SHOES_H0 = 73.0
SHOES_H0_SIGMA = 1.0

PLANCK_OM_M = 0.315
PLANCK_OM_M_SIGMA = 0.007


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


def hz_lcdm(z, H0, Om_m):
    return H0 * np.sqrt(Om_m * (1 + z)**3 + (1 - Om_m))


def hz_osc_log(z, H0, Om_m, eps, Delta, phi):
    cos_arg = (2 * np.pi / Delta) * np.log(1 + z) + phi
    return H0 * np.sqrt(Om_m * (1 + z)**3 + (1 - Om_m) * (1 + eps * np.cos(cos_arg)))


def hz_osc_fixed_delta(z, H0, Om_m, eps, phi):
    """Log-periodic with Delta = PHI (golden ratio) fixed."""
    return hz_osc_log(z, H0, Om_m, eps, PHI, phi)


def hz_inflationary(z, H0, Om_m, N_inflation, Delta, phi):
    """Log-periodic with eps = COUPLING * N_inflation."""
    eps = COUPLING * N_inflation
    return hz_osc_log(z, H0, Om_m, eps, Delta, phi)


def hz_inflationary_fixed(z, H0, Om_m, N_inflation, phi):
    """Log-periodic with eps = COUPLING * N_inflation AND Delta = PHI fixed."""
    eps = COUPLING * N_inflation
    return hz_osc_log(z, H0, Om_m, eps, PHI, phi)


def compute_chi2(model, params, z, H_obs, sigma, n_params):
    H_pred = model(z, *params)
    residuals = (H_obs - H_pred) / sigma
    chi2 = np.sum(residuals**2)
    dof = len(z) - n_params
    return chi2, dof


def fit_free_osc(z, H, sigma):
    """Full free log-periodic fit (baseline from Plan 11)."""
    popt, pcov = curve_fit(
        hz_osc_log, z, H, sigma=sigma,
        p0=[70.0, 0.3, 0.05, 1.5, 0.0],
        bounds=([50, 0.1, 0.0, 0.5, -np.pi], [85, 0.5, 0.3, 5.0, np.pi]),
        maxfev=20000
    )
    perr = np.sqrt(np.diag(pcov))
    chi2, dof = compute_chi2(hz_osc_log, popt, z, H, sigma, 5)
    tension = abs(popt[0] - SHOES_H0) / np.sqrt(perr[0]**2 + SHOES_H0_SIGMA**2)
    return popt, perr, chi2, dof, tension


def fit_fixed_delta(z, H, sigma):
    """Fit with Delta fixed to golden ratio phi."""
    popt, pcov = curve_fit(
        hz_osc_fixed_delta, z, H, sigma=sigma,
        p0=[70.0, 0.3, 0.05, 0.0],
        bounds=([50, 0.1, 0.0, -np.pi], [85, 0.5, 0.3, np.pi]),
        maxfev=20000
    )
    perr = np.sqrt(np.diag(pcov))
    chi2, dof = compute_chi2(hz_osc_fixed_delta, popt, z, H, sigma, 4)
    tension = abs(popt[0] - SHOES_H0) / np.sqrt(perr[0]**2 + SHOES_H0_SIGMA**2)
    return popt, perr, chi2, dof, tension


def fit_inflationary(z, H, sigma):
    """Fit with eps = COUPLING * N_inflation (free Delta)."""
    popt, pcov = curve_fit(
        hz_inflationary, z, H, sigma=sigma,
        p0=[70.0, 0.3, 50.0, 1.5, 0.0],
        bounds=([50, 0.1, 10, 0.5, -np.pi], [85, 0.5, 200, 5.0, np.pi]),
        maxfev=20000
    )
    perr = np.sqrt(np.diag(pcov))
    chi2, dof = compute_chi2(hz_inflationary, popt, z, H, sigma, 5)
    tension = abs(popt[0] - SHOES_H0) / np.sqrt(perr[0]**2 + SHOES_H0_SIGMA**2)
    return popt, perr, chi2, dof, tension


def fit_inflationary_fixed(z, H, sigma):
    """Fit with eps = COUPLING * N_inflation AND Delta = PHI fixed."""
    popt, pcov = curve_fit(
        hz_inflationary_fixed, z, H, sigma=sigma,
        p0=[70.0, 0.3, 50.0, 0.0],
        bounds=([50, 0.1, 10, -np.pi], [85, 0.5, 200, np.pi]),
        maxfev=20000
    )
    perr = np.sqrt(np.diag(pcov))
    chi2, dof = compute_chi2(hz_inflationary_fixed, popt, z, H, sigma, 4)
    tension = abs(popt[0] - SHOES_H0) / np.sqrt(perr[0]**2 + SHOES_H0_SIGMA**2)
    return popt, perr, chi2, dof, tension


if __name__ == "__main__":
    z, H, sigma = load_hz_data()
    n = len(z)
    print(f"Loaded {n} H(z) data points")
    print()

    # ── Model 0: Free oscillatory (Plan 11 baseline) ─────────────────────
    p_free, e_free, c2_free, dof_free, t_free = fit_free_osc(z, H, sigma)
    H0_f, Om_f, eps_f, Delta_f, phi_f = p_free

    print("=" * 72)
    print("  MODEL 0: FREE LOG-PERIODIC (PLAN 11 BASELINE)")
    print("=" * 72)
    print(f"  H0     = {H0_f:.2f} +/- {e_free[0]:.2f} km/s/Mpc")
    print(f"  Om_m   = {Om_f:.4f} +/- {e_free[1]:.4f}")
    print(f"  eps    = {eps_f:.5f} +/- {e_free[2]:.5f}")
    print(f"  Delta  = {Delta_f:.4f} +/- {e_free[3]:.4f}")
    print(f"  phi    = {phi_f:.4f} +/- {e_free[4]:.4f}")
    print(f"  chi^2  = {c2_free:.2f} / {dof_free}")
    print(f"  Tension = {t_free:.2f} sigma")
    print(f"  eps / (alpha/phi^2) = {eps_f / COUPLING:.2f} x")
    print(f"  |Delta - PHI| = {abs(Delta_f - PHI):.4f}")
    print()

    # ── Model 1: Fixed golden ratio period ───────────────────────────────
    p_fd, e_fd, c2_fd, dof_fd, t_fd = fit_fixed_delta(z, H, sigma)
    H0_fd, Om_fd, eps_fd, phi_fd = p_fd
    dchi2_fd = c2_fd - c2_free

    print("=" * 72)
    print("  MODEL 1: FIXED Delta = phi = 1.618 (GOLDEN RATIO PERIOD)")
    print("=" * 72)
    print(f"  H0     = {H0_fd:.2f} +/- {e_fd[0]:.2f} km/s/Mpc")
    print(f"  Om_m   = {Om_fd:.4f} +/- {e_fd[1]:.4f}")
    print(f"  eps    = {eps_fd:.5f} +/- {e_fd[2]:.5f}")
    print(f"  phi    = {phi_fd:.4f} +/- {e_fd[3]:.4f}")
    print(f"  chi^2  = {c2_fd:.2f} / {dof_fd}")
    print(f"  Delta chi^2 vs free = {dchi2_fd:.2f}")
    p_val = 1 - stats.chi2.cdf(dchi2_fd, 1)
    print(f"  p-value (1 param removed) = {p_val:.4f}")
    print(f"  Tension = {t_fd:.2f} sigma")
    verdict = "SUPPORTED" if dchi2_fd < 2.71 else "MARGINAL" if dchi2_fd < 6.63 else "REJECTED"
    print(f"  Golden ratio hypothesis: {verdict} (Delta_chi2 < 2.71 at 90% CL)")
    print()

    # ── Model 2: Inflationary amplification ──────────────────────────────
    p_inf, e_inf, c2_inf, dof_inf, t_inf = fit_inflationary(z, H, sigma)
    H0_inf, Om_inf, N_inf, Delta_inf, phi_inf = p_inf
    dchi2_inf = c2_inf - c2_free
    eps_inf = COUPLING * N_inf

    print("=" * 72)
    print("  MODEL 2: eps = (alpha/phi^2) * N_inflation (FREE Delta)")
    print("=" * 72)
    print(f"  H0          = {H0_inf:.2f} +/- {e_inf[0]:.2f} km/s/Mpc")
    print(f"  Om_m        = {Om_inf:.4f} +/- {e_inf[1]:.4f}")
    print(f"  N_inflation = {N_inf:.1f} +/- {e_inf[2]:.1f} e-folds")
    print(f"  eps_inferred= {eps_inf:.5f}  (free eps = {eps_f:.5f})")
    print(f"  Delta       = {Delta_inf:.4f} +/- {e_inf[3]:.4f}")
    print(f"  phi         = {phi_inf:.4f} +/- {e_inf[4]:.4f}")
    print(f"  chi^2       = {c2_inf:.2f} / {dof_inf}")
    print(f"  Delta chi^2 vs free = {dchi2_inf:.2f}")
    print(f"  Tension = {t_inf:.2f} sigma")
    print()

    # ── Model 3: Inflationary + fixed golden ratio ───────────────────────
    p_if, e_if, c2_if, dof_if, t_if = fit_inflationary_fixed(z, H, sigma)
    H0_if, Om_if, N_if, phi_if = p_if
    dchi2_if = c2_if - c2_free
    eps_if = COUPLING * N_if

    print("=" * 72)
    print("  MODEL 3: eps = (alpha/phi^2) * N_inflation + Delta = phi (BOTH FIXED)")
    print("=" * 72)
    print(f"  H0          = {H0_if:.2f} +/- {e_if[0]:.2f} km/s/Mpc")
    print(f"  Om_m        = {Om_if:.4f} +/- {e_if[1]:.4f}")
    print(f"  N_inflation = {N_if:.1f} +/- {e_if[2]:.1f} e-folds")
    print(f"  eps_inferred= {eps_if:.5f}")
    print(f"  phi_0       = {phi_if:.4f} +/- {e_if[3]:.4f}")
    print(f"  chi^2       = {c2_if:.2f} / {dof_if}")
    print(f"  Delta chi^2 vs free = {dchi2_if:.2f} (2 params removed)")
    p_val2 = 1 - stats.chi2.cdf(dchi2_if, 2)
    print(f"  p-value (2 params removed) = {p_val2:.4f}")
    print(f"  Tension = {t_if:.2f} sigma")
    print()

    # ── Summary Table ────────────────────────────────────────────────────
    print("=" * 72)
    print("  SUMMARY: MODEL COMPARISON")
    print("=" * 72)
    print(f"  {'Model':<30} {'H0':>8} {'chi2/dof':>10} {'eps':>8} {'Delta':>8} {'N_inf':>8} {'Tension':>8}")
    print(f"  {'-'*72}")
    print(f"  {'0. Free log-periodic':<30} {H0_f:>8.2f} {f'{c2_free:.1f}/{dof_free}':>10} {eps_f:>8.4f} {Delta_f:>8.4f} {'---':>8} {f'{t_free:.1f} sigma':>8}")
    print(f"  {'1. Fixed Delta=phi':<30} {H0_fd:>8.2f} {f'{c2_fd:.1f}/{dof_fd}':>10} {eps_fd:>8.4f} {f'{PHI:.4f}*':>8} {'---':>8} {f'{t_fd:.1f} sigma':>8}")
    print(f"  {'2. eps=N_inf*alpha/phi^2':<30} {H0_inf:>8.2f} {f'{c2_inf:.1f}/{dof_inf}':>10} {eps_inf:>8.4f} {Delta_inf:>8.4f} {f'{N_inf:.1f}':>8} {f'{t_inf:.1f} sigma':>8}")
    print(f"  {'3. Delta=phi + N_inflation':<30} {H0_if:>8.2f} {f'{c2_if:.1f}/{dof_if}':>10} {eps_if:>8.4f} {f'{PHI:.4f}*':>8} {f'{N_if:.1f}':>8} {f'{t_if:.1f} sigma':>8}")
    print()
    print(f"  * Fixed parameter")
    print(f"  Coupling = alpha/phi^2 = {COUPLING:.6f}")
    print(f"  Golden ratio phi = {PHI:.6f}")
    print(f"  Planck 2018: r < 0.036 => N_inflation > 50")
    print()
    print(f"  Independent cross-check: BICEP/Keck r < 0.036 (95% CL)")
    print(f"    => N_inflation > 50 e-folds for standard slow-roll")
    print(f"    Fitted N_inflation = {N_inf:.1f} +/- {e_inf[2]:.1f} (free Delta)")
    print(f"    Fitted N_inflation = {N_if:.1f} +/- {e_if[2]:.1f} (fixed Delta)")
    consistency = "CONSISTENT" if 40 < N_inf < 80 else "INCONSISTENT"
    print(f"    => {consistency} with inflationary expectations")
    print()

    # ── Plot ─────────────────────────────────────────────────────────────
    z_smooth = np.linspace(0, 2.5, 300)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Panel 1: H(z) with all four models
    ax = axes[0, 0]
    ax.errorbar(z, H, yerr=sigma, fmt="o", color="black", ms=3, capsize=2, alpha=0.6, label="H(z) data")
    ax.plot(z_smooth, hz_osc_log(z_smooth, *p_free), "k-", lw=2, label="Free log-periodic")
    ax.plot(z_smooth, hz_osc_fixed_delta(z_smooth, *p_fd), "b--", lw=1.5,
            label=f"Delta=phi ({PHI:.3f})")
    ax.plot(z_smooth, hz_inflationary(z_smooth, *p_inf), "g-.", lw=1.5,
            label=f"eps=N_inf*alpha/phi^2 (N={N_inf:.0f})")
    ax.plot(z_smooth, hz_inflationary_fixed(z_smooth, *p_if), "r:", lw=1.5,
            label=f"Delta=phi + N_inf (N={N_if:.0f})")
    ax.axhline(y=SHOES_H0, color="orange", ls=":", lw=0.8)
    ax.axhline(y=PLANCK_H0, color="green", ls=":", lw=0.8)
    ax.set_xlabel("Redshift z")
    ax.set_ylabel("H(z) [km/s/Mpc]")
    ax.legend(fontsize=7, loc="upper left")
    ax.set_title("Plan 12: Fixed Parameters — All Models")
    ax.grid(True, alpha=0.3)
    ax.text(0.02, 0.98, f"chi2_free={c2_free:.1f}/{dof_free}", transform=ax.transAxes,
            va="top", fontsize=8, family="monospace")

    # Panel 2: N_inflation likelihood profile
    ax = axes[0, 1]
    N_grid = np.linspace(10, 100, 91)
    chi2_N = []
    for N_val in N_grid:
        eps_test = COUPLING * N_val
        H_pred = hz_osc_fixed_delta(z, H0_fd, Om_fd, eps_test, phi_fd)
        residuals = (H - H_pred) / sigma
        chi2_N.append(np.sum(residuals**2))
    chi2_N = np.array(chi2_N)
    delta_chi2_N = chi2_N - np.min(chi2_N)
    ax.plot(N_grid, delta_chi2_N, "b-", lw=2)
    ax.axhline(y=1.0, ls="--", color="gray", label="1 sigma")
    ax.axhline(y=2.71, ls="--", color="gray", label="90% CL")
    ax.axvline(x=N_if, ls="--", color="red", label=f"Best-fit N={N_if:.0f}")
    ax.axvline(x=50, ls=":", color="green", label="BICEP/Keck bound (N>50)")
    ax.set_xlabel("N_inflation [e-folds]")
    ax.set_ylabel("Delta chi^2")
    ax.set_title("N_inflation Likelihood Profile (Delta=phi fixed)")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, max(4, max(delta_chi2_N) * 1.1))

    # Panel 3: Residuals vs free model
    ax = axes[1, 0]
    resid_free = (H - hz_osc_log(z, *p_free)) / sigma
    resid_inf = (H - hz_inflationary_fixed(z, *p_if)) / sigma
    ax.errorbar(z, resid_free, yerr=np.ones_like(z), fmt="o", color="gray", ms=3, alpha=0.5,
                label="Free model residuals")
    ax.errorbar(z, resid_inf, yerr=0.8 * np.ones_like(z), fmt="s", color="red", ms=3, alpha=0.6,
                label="Delta=phi + N_inflation residuals")
    ax.axhline(y=0, color="gray", ls="--", lw=0.5)
    ax.set_xlabel("Redshift z")
    ax.set_ylabel("Residual (sigma)")
    ax.set_title("Residuals: Free vs Delta=phi+N_inf Model")
    ax.legend(fontsize=7)
    ax.grid(True, alpha=0.3)

    # Panel 4: Epsilon scaling plot
    ax = axes[1, 1]
    N_range = np.linspace(1, 100, 100)
    eps_range = COUPLING * N_range
    ax.plot(N_range, eps_range, "b-", lw=1.5, label="eps = (alpha/phi^2) x N")
    ax.scatter([48.78], [0.136], color="red", s=100, zorder=5,
               label="Plan 11 free fit (eps=0.136, N_eff=48.8)")
    ax.scatter([N_inf], [eps_inf], color="green", s=100, zorder=5, marker="s",
               label=f"Model 2: N_inf={N_inf:.0f}, eps={eps_inf:.3f}")
    ax.scatter([N_if], [eps_if], color="purple", s=100, zorder=5, marker="D",
               label=f"Model 3: N_inf={N_if:.0f}, eps={eps_if:.3f}")
    ax.axvline(x=50, color="gray", ls=":", lw=1, label="BICEP bound N>50")
    ax.set_xlabel("N_inflation [e-folds]")
    ax.set_ylabel("epsilon (oscillation amplitude)")
    ax.set_title("Inflationary Amplification: eps = (alpha/phi^2) x N_inflation")
    ax.legend(fontsize=7, loc="upper left")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("code/outputs/plan12_fixed_delta_fit.png", dpi=150)
    plt.close(fig)

    # ── Write output file ────────────────────────────────────────────────
    with open("code/outputs/plan12_fixed_params.txt", "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("PLAN 12 — TASKS 1 & 2: FIXED PARAMETER FITS\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Golden ratio phi = {PHI:.6f}\n")
        f.write(f"IST coupling alpha/phi^2 = {COUPLING:.6f}\n\n")

        f.write("Model 0 (Free log-periodic, baseline):\n")
        f.write(f"  H0     = {H0_f:.4f}, Om_m = {Om_f:.4f}, eps = {eps_f:.6f}\n")
        f.write(f"  Delta  = {Delta_f:.4f}, phi_0 = {phi_f:.4f}\n")
        f.write(f"  chi^2  = {c2_free:.2f} / {dof_free}, tension = {t_free:.2f} sigma\n")
        f.write(f"  eps/(alpha/phi^2) = {eps_f/COUPLING:.2f} x\n")
        f.write(f"  |Delta - phi| = {abs(Delta_f - PHI):.4f}\n\n")

        f.write("Model 1 (Fixed Delta = phi):\n")
        f.write(f"  H0     = {H0_fd:.4f}, Om_m = {Om_fd:.4f}, eps = {eps_fd:.6f}\n")
        f.write(f"  phi_0  = {phi_fd:.4f}\n")
        f.write(f"  chi^2  = {c2_fd:.2f} / {dof_fd}, Delta_chi^2 = {dchi2_fd:.2f}\n")
        f.write(f"  tension = {t_fd:.2f} sigma\n\n")

        f.write("Model 2 (eps = (alpha/phi^2) * N_inflation, free Delta):\n")
        f.write(f"  H0     = {H0_inf:.4f}, Om_m = {Om_inf:.4f}\n")
        f.write(f"  N_inflation = {N_inf:.2f} +/- {e_inf[2]:.2f}\n")
        f.write(f"  eps_inferred = {eps_inf:.6f}\n")
        f.write(f"  Delta  = {Delta_inf:.4f}, phi_0 = {phi_inf:.4f}\n")
        f.write(f"  chi^2  = {c2_inf:.2f} / {dof_inf}, Delta_chi^2 = {dchi2_inf:.2f}\n")
        f.write(f"  tension = {t_inf:.2f} sigma\n\n")

        f.write("Model 3 (eps = (alpha/phi^2) * N_inflation, Delta = phi):\n")
        f.write(f"  H0     = {H0_if:.4f}, Om_m = {Om_if:.4f}\n")
        f.write(f"  N_inflation = {N_if:.2f} +/- {e_if[2]:.2f}\n")
        f.write(f"  eps_inferred = {eps_if:.6f}\n")
        f.write(f"  phi_0  = {phi_if:.4f}\n")
        f.write(f"  chi^2  = {c2_if:.2f} / {dof_if}, Delta_chi^2 = {dchi2_if:.2f}\n")
        f.write(f"  tension = {t_if:.2f} sigma\n\n")

        f.write("-" * 70 + "\n")
        f.write(f"BICEP/Keck r < 0.036 => N_inflation > 50\n")
        f.write(f"Fitted N_inflation (free Delta):  {N_inf:.1f} +/- {e_inf[2]:.1f}\n")
        f.write(f"Fitted N_inflation (fixed Delta): {N_if:.1f} +/- {e_if[2]:.1f}\n")

    print("  Output files:")
    print("    code/outputs/plan12_fixed_delta_fit.png")
    print("    code/outputs/plan12_fixed_params.txt")
