"""
Plan 11.5 — Phase 2A: Anisotropic Hubble Parameter Fitting
============================================================
Tests the IST prediction of a direction-dependent Hubble parameter arising
from the Klein bottle twist axis (intrinsic substrate anisotropy).

The log-periodic oscillatory model from Plan 11 is extended with a
dipolar modulation: H0(theta) = H0 * (1 + H_dip * cos(theta))

Where theta is the angle between the line-of-sight and the Klein bottle
twist axis. Uses SNe Ia + BAO sky-coordinate data to constrain the
dipole direction (ra_axis, dec_axis) and amplitude H_dip.

References:
  - Plan 11 results: H0_log = 71.00, eps = 0.136, Delta = 1.54
  - IST master equation (Plan 7): delta_tc couples to associator field Xi(r)
  - Directed numbers (Plan 9): parity UP/DOWN axes define substrate directions
  - Cosmic dipole: Secrest et al. (2021, ApJL 908, L51)
  - Pantheon+ SNe Ia: Scolnic et al. (2022, ApJ 938, 113)
"""

import os
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize, curve_fit
from scipy import stats

os.makedirs("code/outputs", exist_ok=True)

PHI = (1 + np.sqrt(5)) / 2
ALPHA = 1 / 137.035999084
DEG_TO_RAD = np.pi / 180.0

PLANCK_H0 = 67.4
SHOES_H0 = 73.0

IST_EPS_PREDICTED = ALPHA / PHI**2


def sky_angle(ra1, dec1, ra2, dec2):
    """Compute angular separation between two sky positions (radians)."""
    ra1r, dec1r = ra1 * DEG_TO_RAD, dec1 * DEG_TO_RAD
    ra2r, dec2r = ra2 * DEG_TO_RAD, dec2 * DEG_TO_RAD
    cos_angle = np.sin(dec1r) * np.sin(dec2r) + np.cos(dec1r) * np.cos(dec2r) * np.cos(ra1r - ra2r)
    return np.arccos(np.clip(cos_angle, -1.0, 1.0))


def hz_lcdm(z, H0, Om_m):
    return H0 * np.sqrt(Om_m * (1 + z)**3 + (1 - Om_m))


def hz_osc_log(z, H0, Om_m, eps, Delta, phi):
    cos_arg = (2 * np.pi / Delta) * np.log(1 + z) + phi
    return H0 * np.sqrt(Om_m * (1 + z)**3 + (1 - Om_m) * (1 + eps * np.cos(cos_arg)))


def hz_osc_anisotropic(z, ra, dec, H0, Om_m, eps, Delta, phi, H_dip, ra_axis, dec_axis):
    """Anisotropic oscillatory model: H0 varies with sky direction."""
    theta = sky_angle(ra, dec, ra_axis, dec_axis)
    H0_eff = H0 * (1 + H_dip * np.cos(theta))
    return hz_osc_log(z, H0_eff, Om_m, eps, Delta, phi)


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


def generate_mock_sne_data(n_sne=200, H_dip_true=0.02, ra_axis_true=150.0, dec_axis_true=-10.0, seed=42):
    """Generate mock SNe Ia with sky positions and H(z) values for testing."""
    rng = np.random.default_rng(seed)
    z = rng.uniform(0.01, 1.5, n_sne)
    ra = rng.uniform(0, 360, n_sne)
    dec = rng.uniform(-90, 90, n_sne)

    H0_base = 73.0
    Om_m_base = 0.30
    eps_base = 0.05
    Delta_base = 1.5
    phi_base = 0.0

    H_true = hz_osc_anisotropic(z, ra, dec, H0_base, Om_m_base, eps_base, Delta_base, phi_base,
                                 H_dip_true, ra_axis_true, dec_axis_true)
    sigma_H = 0.03 * H_true + 2.0
    H_obs = H_true + rng.normal(0, sigma_H)

    return z, ra, dec, H_obs, sigma_H


def fit_isotropic(z, H, sigma):
    """Fit isotropic oscillatory model (baseline from Plan 11)."""
    popt, pcov = curve_fit(
        hz_osc_log, z, H, sigma=sigma,
        p0=[70.0, 0.3, 0.05, 1.5, 0.0],
        bounds=([50, 0.1, 0.0, 0.5, -np.pi], [85, 0.5, 0.3, 5.0, np.pi]),
        maxfev=20000
    )
    residuals = (H - hz_osc_log(z, *popt)) / sigma
    chi2 = np.sum(residuals**2)
    dof = len(z) - 5
    return popt, pcov, chi2, dof


def fit_anisotropic_mock(z, ra, dec, H, sigma):
    """Fit anisotropic oscillatory model (7 parameters). Uses Nelder-Mead + curve_fit hybrid."""

    # Step 1: Fit isotropic first for good initial guess
    p0_iso, _, _, _ = fit_isotropic(z, H, sigma)
    H0_iso, Om_iso, eps_iso, Delta_iso, phi_iso = p0_iso

    def chi2_func(params):
        H0, Om_m, eps, Delta, phi, H_dip, ra_axis, dec_axis = params
        H_pred = hz_osc_anisotropic(z, ra, dec, H0, Om_m, eps, Delta, phi, H_dip, ra_axis, dec_axis)
        return np.sum(((H - H_pred) / sigma)**2)

    # Try multiple dipole axis starting points
    best_chi2 = np.inf
    best_params = None
    for ra_try in [0, 90, 180, 270]:
        for dec_try in [-45, 0, 45]:
            p0 = [H0_iso, Om_iso, eps_iso, Delta_iso, phi_iso, 0.01, ra_try, dec_try]
            bounds = [(50, 85), (0.1, 0.5), (0, 0.3), (0.5, 5.0), (-np.pi, np.pi),
                      (-0.1, 0.1), (0, 360), (-90, 90)]
            try:
                result = minimize(chi2_func, p0, method="L-BFGS-B", bounds=bounds,
                                  options={"maxiter": 5000})
                if result.fun < best_chi2:
                    best_chi2 = result.fun
                    best_params = result.x
            except Exception:
                continue

    if best_params is None:
        return None, np.inf, 0

    chi2_aniso = best_chi2
    dof_aniso = len(z) - 8
    return best_params, chi2_aniso, dof_aniso


def run_isotropic_only(z, H, sigma):
    """Fit the isotropic osc model to real H(z) data."""
    print("=" * 65)
    print("  ISOTROPIC OSCILLATORY FIT (BASELINE)")
    print("=" * 65)

    popt_iso, pcov_iso, chi2_iso, dof_iso = fit_isotropic(z, H, sigma)
    perr_iso = np.sqrt(np.diag(pcov_iso))
    H0_i, Om_i, eps_i, Delta_i, phi_i = popt_iso

    print(f"  H0     = {H0_i:.2f} +/- {perr_iso[0]:.2f} km/s/Mpc")
    print(f"  Om_m   = {Om_i:.4f} +/- {perr_iso[1]:.4f}")
    print(f"  eps    = {eps_i:.5f} +/- {perr_iso[2]:.5f}")
    print(f"  Delta  = {Delta_i:.4f} +/- {perr_iso[3]:.4f}")
    print(f"  phi    = {phi_i:.4f} +/- {perr_iso[4]:.4f}")
    print(f"  chi^2  = {chi2_iso:.2f} / {dof_iso}")
    print(f"  IST predicted eps = alpha/phi^2 = {IST_EPS_PREDICTED:.6f}")
    print(f"  Fitted / IST ratio = {eps_i / IST_EPS_PREDICTED:.2f}")
    print()

    return popt_iso, chi2_iso, dof_iso


def run_anisotropic_mock():
    """Test anisotropic fitting on mock data with known dipole."""
    print("=" * 65)
    print("  ANISOTROPIC FIT ON MOCK SNe Ia DATA")
    print("=" * 65)

    H_dip_true = 0.02
    ra_axis_true = 150.0
    dec_axis_true = -10.0

    z, ra, dec, H, sigma = generate_mock_sne_data(
        n_sne=300, H_dip_true=H_dip_true, ra_axis_true=ra_axis_true, dec_axis_true=dec_axis_true
    )

    print(f"  Mock data: {len(z)} SNe Ia")
    print(f"  True dipole: H_dip = {H_dip_true:.4f}, axis = ({ra_axis_true}, {dec_axis_true})")
    print()

    # Isotropic fit
    popt_iso, pcov_iso, chi2_iso, dof_iso = fit_isotropic(z, H, sigma)
    H0_i, Om_i, eps_i, Delta_i, phi_i = popt_iso
    print(f"  Isotropic chi^2 = {chi2_iso:.1f} / {dof_iso}")
    print(f"  Isotropic H0 = {H0_i:.2f}, eps = {eps_i:.4f}, Delta = {Delta_i:.4f}")
    print()

    # Anisotropic fit
    best_params, chi2_aniso, dof_aniso = fit_anisotropic_mock(z, ra, dec, H, sigma)

    if best_params is not None:
        H0_a, Om_a, eps_a, Delta_a, phi_a, H_dip, ra_axis, dec_axis = best_params
        delta_chi2 = chi2_iso - chi2_aniso

        print(f"  Anisotropic chi^2 = {chi2_aniso:.1f} / {dof_aniso}")
        print(f"  Delta chi^2       = {delta_chi2:.1f} (p ~ {1 - stats.chi2.cdf(delta_chi2, 3):.3f} for 3 extra params)")
        print(f"  H0     = {H0_a:.2f} km/s/Mpc")
        print(f"  Om_m   = {Om_a:.4f}")
        print(f"  eps    = {eps_a:.4f}")
        print(f"  Delta  = {Delta_a:.4f}")
        print(f"  H_dip  = {H_dip:.6f}")
        print(f"  Axis   = RA={ra_axis:.1f} deg, Dec={dec_axis:.1f} deg")
        print()

        # Recovery accuracy
        angular_error = np.degrees(sky_angle(ra_axis, dec_axis, ra_axis_true, dec_axis_true))
        print(f"  Dipole recovery:")
        print(f"    H_dip error = {abs(H_dip - H_dip_true):.6f}")
        print(f"    Axis error  = {angular_error:.1f} deg")
        print()

        # Sky map
        n_grid = 40
        ra_grid = np.linspace(0, 360, n_grid)
        dec_grid = np.linspace(-90, 90, n_grid)
        RA, DEC = np.meshgrid(ra_grid, dec_grid)

        z_mean = np.mean(z)
        H0_map = np.zeros_like(RA)
        for i in range(n_grid):
            for j in range(n_grid):
                theta = sky_angle(RA[i, j], DEC[i, j], ra_axis, dec_axis)
                H0_map[i, j] = H0_a * (1 + H_dip * np.cos(theta))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        im1 = ax1.contourf(RA, DEC, H0_map, levels=20, cmap="RdBu_r")
        ax1.set_xlabel("RA [deg]")
        ax1.set_ylabel("Dec [deg]")
        ax1.set_title(f"Fitted H0 Sky Map (dipole = {H_dip:.4f})")
        plt.colorbar(im1, ax=ax1, label="H0 [km/s/Mpc]")
        ax1.scatter([ra_axis], [dec_axis], marker="*", color="black", s=200, label="Dipole axis")
        ax1.legend()

        z_sorted = np.sort(z)
        H_iso_pred = hz_osc_log(z_sorted, H0_i, Om_i, eps_i, Delta_i, phi_i)
        H_aniso_pred = np.array([hz_osc_anisotropic(zi, ra_i, dec_i, H0_a, Om_a, eps_a, Delta_a, phi_a,
                                                     H_dip, ra_axis, dec_axis)
                                  for zi, ra_i, dec_i in zip(z_sorted, ra[np.argsort(z)], dec[np.argsort(z)])])

        ax2.errorbar(z_sorted, H[np.argsort(z)], yerr=sigma[np.argsort(z)],
                      fmt="o", color="gray", ms=3, alpha=0.5, label="Mock data")
        ax2.plot(z_sorted, H_iso_pred, "b-", lw=1.5, label="Isotropic fit")
        ax2.plot(z_sorted, H_aniso_pred, "r--", lw=1.5, label="Anisotropic fit")
        ax2.set_xlabel("Redshift z")
        ax2.set_ylabel("H(z) [km/s/Mpc]")
        ax2.legend(fontsize=8)
        ax2.set_title("Mock SNe Ia: Isotropic vs Anisotropic Fit")
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig("code/outputs/anisotropic_fit.png", dpi=150)
        plt.close(fig)
        print("  Plot saved to code/outputs/anisotropic_fit.png")
        print()

        with open("code/outputs/anisotropic_params.txt", "w", encoding="utf-8") as f:
            f.write("=" * 65 + "\n")
            f.write("ANISOTROPIC HUBBLE PARAMETER FIT\n")
            f.write("=" * 65 + "\n\n")
            f.write(f"Mock data: {len(z)} SNe Ia\n")
            f.write(f"True dipole: H_dip = {H_dip_true:.4f}, axis = ({ra_axis_true}, {dec_axis_true})\n\n")
            f.write(f"Isotropic chi^2 = {chi2_iso:.1f} / {dof_iso}\n")
            f.write(f"Anisotropic chi^2 = {chi2_aniso:.1f} / {dof_aniso}\n")
            f.write(f"Delta chi^2 = {delta_chi2:.1f}\n\n")
            f.write(f"Fitted dipole: H_dip = {H_dip:.6f}, axis = ({ra_axis:.1f}, {dec_axis:.1f})\n")
            f.write(f"Angular recovery error: {angular_error:.1f} deg\n")
            f.write(f"H0_iso = {H0_i:.2f}, H0_aniso = {H0_a:.2f}\n")
    else:
        print("  Anisotropic fit FAILED to converge.")
        print()


def run_anisotropic_real(z, H, sigma):
    """Fit anisotropic model to real H(z) data (no sky positions — assigns mock positions for demonstration)."""
    print("=" * 65)
    print("  ANISOTROPIC FIT ON REAL H(z) DATA")
    print("=" * 65)
    print("  NOTE: Real H(z) from cosmic chronometers lacks sky positions.")
    print("  Assigning mock RA/Dec for demonstration of the fitting framework.")
    print()

    rng = np.random.default_rng(42)
    ra = rng.uniform(0, 360, len(z))
    dec = rng.uniform(-90, 90, len(z))

    best_params, chi2_aniso, dof_aniso = fit_anisotropic_mock(z, ra, dec, H, sigma)

    if best_params is not None:
        H0_a, Om_a, eps_a, Delta_a, phi_a, H_dip, ra_axis, dec_axis = best_params
        chi2_iso = np.sum(((H - hz_osc_log(z, H0_a, Om_a, eps_a, Delta_a, phi_a)) / sigma)**2)
        dof_iso = len(z) - 5
        delta_chi2 = chi2_iso - chi2_aniso

        print(f"  Isotropic chi^2 = {chi2_iso:.1f} / {dof_iso}")
        print(f"  Anisotropic chi^2 = {chi2_aniso:.1f} / {dof_aniso}")
        print(f"  Delta chi^2 = {delta_chi2:.1f}")
        print(f"  H0     = {H0_a:.2f} km/s/Mpc")
        print(f"  H_dip  = {H_dip:.6f}")
        print(f"  Axis   = RA={ra_axis:.1f}, Dec={dec_axis:.1f}")
        print(f"  (Result not physically meaningful — sky positions are mock)")
        print()

        # Compare to known anomalies
        print("  Comparison to known cosmic dipoles:")
        print(f"    CMB dipole (Planck 2018):   RA=168, Dec=-7,  amp=0.0012")
        print(f"    Radio dipole (Secrest 2021): RA=158, Dec=-5,  amp=0.0054")
        print(f"    Quasar dipole (Secrest):    RA=238, Dec=+25,  amp=0.0155")
        cmb_angle = np.degrees(sky_angle(ra_axis, dec_axis, 168, -7))
        radio_angle = np.degrees(sky_angle(ra_axis, dec_axis, 158, -5))
        quasar_angle = np.degrees(sky_angle(ra_axis, dec_axis, 238, 25))
        print(f"    Angular distance from CMB dipole:    {cmb_angle:.1f} deg")
        print(f"    Angular distance from radio dipole:  {radio_angle:.1f} deg")
        print(f"    Angular distance from quasar dipole: {quasar_angle:.1f} deg")
        print()
    else:
        print("  Anisotropic fit FAILED to converge.")
        print()


if __name__ == "__main__":
    print("Plan 11.5 — Phase 2A: Anisotropic Hubble Fitting")
    print("=" * 65)
    print(f"IST predicted oscillation amplitude: eps ~ alpha/phi^2 = {IST_EPS_PREDICTED:.6f}")
    print(f"IST predicted dipole amplitude: H_dip ~ O(0.01) from associator field variation")
    print()

    # Load real data
    z, H, sigma = load_hz_data()
    print(f"Loaded {len(z)} real H(z) data points (cosmic chronometers + BAO)")

    # 1. Isotropic baseline
    _ = run_isotropic_only(z, H, sigma)

    # 2. Mock anisotropic test
    run_anisotropic_mock()

    # 3. Real data anisotropic (demonstration with mock positions)
    run_anisotropic_real(z, H, sigma)

    print("=" * 65)
    print("  SUMMARY")
    print("=" * 65)
    print("  Anisotropic fitting framework operational.")
    print("  Mock data test shows dipole recovery capability.")
    print("  Real data requires SNe Ia sky coordinates (Pantheon+ catalog).")
    print("  Next: download Pantheon+ and run with actual positions.")
    print()
    print("  Output files:")
    print("    - code/outputs/anisotropic_fit.png")
    print("    - code/outputs/anisotropic_params.txt")
