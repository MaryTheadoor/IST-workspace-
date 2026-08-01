"""
================================================================================
IST Phase 18 — DES Y6 BAO Distance Scale Test
================================================================================
Fit the BAO peak position in the DES Y6 angular correlation function
(acf) data across 6 redshift bins. Extract D_A(z)/r_d and compare to
both LCDM and the IST oscillatory DE model (Phase 16).

The BAO scale: theta_BAO = r_d / D_A(z). IST modifies H(z) -> D_A(z)
-> predicted theta_BAO. dchi2 vs LCDM tests the oscillatory model.

Input:  data/bao/DESY6BAO_datavectors/acf/acf_data_bin*.dat
Output: code/outputs/phase18_bao/bao_fit.csv
        code/outputs/phase18_bao/bao_distance.png
================================================================================
"""
import os, csv, glob, time
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase18_bao")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "bao",
                        "DESY6BAO_datavectors", "acf")
C_KM_S = 299792.458
R_D_FID = 147.09  # Mpc


def ez(z, Om): return np.sqrt(Om*(1+z)**3 + (1-Om))

def D_A(z, H0, Om):
    """Angular diameter distance in Mpc."""
    chi = comoving(z, H0, Om)
    return chi / (1 + z)

def comoving(z, H0, Om):
    zs = np.linspace(0, z, 256)
    return C_KM_S / H0 * np.trapezoid(1./ez(zs, Om), zs)

def D_A_osc(z, H0, Om, eps0, Delta, beta=1/PHI):
    """D_A with the IST oscillatory H(z)."""
    zs = np.linspace(0, z, 256)
    eps_z = eps0 * (1 + zs) ** beta
    osc = 1 + eps_z * np.cos(2*np.pi*np.log(1+zs)/Delta)
    Hz = H0 * np.sqrt(Om*(1+zs)**3 + (1-Om)*np.maximum(osc, 0.01))
    chi = C_KM_S * np.trapezoid(1./np.maximum(Hz, 0.1), zs)
    return chi / (1 + z)


def gaussian_peak(theta, A, th0, sigma, B, C):
    """w(theta) = A*exp(-(theta-th0)^2/(2*sigma^2)) + B + C*theta."""
    return (A * np.exp(-(theta - th0)**2 / (2*sigma**2))
            + B + C * theta)


# DES Y6 redshift bins from the data release paper (approximate z_eff)
Z_BINS = {1: 0.30, 2: 0.45, 3: 0.60, 4: 0.75, 5: 0.90, 6: 1.10}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    # LCDM fiducial: H0=70, Om=0.3
    # IST oscillatory: from Phase 16 best fit
    H0_ist, Om_ist, eps_ist, Del_ist, beta_ist = 71.4, 0.283, 0.063, 2.206, 1/PHI

    rows = []
    plt.figure(figsize=(12, 8))

    for bin_id in range(1, 7):
        fname = os.path.join(DATA_DIR, f"acf_data_bin{bin_id}.dat")
        data = np.loadtxt(fname)
        theta = data[:, 0] * 180/np.pi  # rad -> deg
        w_obs = data[:, 1]
        w_err = data[:, 2]

        # Restrict to BAO range: 0.5-5 degrees
        mask = (theta > 0.5) & (theta < 5.0) & (w_err > 0)
        th_fit = theta[mask]; w_fit = w_obs[mask]; we_fit = w_err[mask]

        if len(th_fit) < 5:
            continue

        # Initial guess for BAO peak
        th0_guess = th_fit[np.argmax(w_fit)]
        try:
            popt, pcov = curve_fit(gaussian_peak, th_fit, w_fit,
                                p0=[max(w_fit)*0.5, th0_guess, 0.3, 0, 0],
                                sigma=we_fit, maxfev=2000)
            th_bao = abs(popt[1])
            th_err = np.sqrt(pcov[1,1]) if pcov.shape[0] > 1 else 0.1
        except:
            popt = [max(w_fit)*0.5, th0_guess, 0.3, 0, 0]
            th_bao = th0_guess; th_err = 0.5

        z_eff = Z_BINS[bin_id]
        # LCDM prediction
        DA_lcdm = D_A(z_eff, 70, 0.3)
        th_lcdm = R_D_FID / DA_lcdm * 180/np.pi

        # IST prediction
        DA_ist = D_A_osc(z_eff, H0_ist, Om_ist, eps_ist, Del_ist, beta_ist)
        th_ist = R_D_FID / DA_ist * 180/np.pi

        rows.append({"bin": bin_id, "z_eff": z_eff,
                     "theta_BAO_deg": th_bao, "theta_err": th_err,
                     "theta_LCDM": th_lcdm, "theta_IST": th_ist,
                     "DA_measured": R_D_FID / (th_bao * np.pi/180),
                     "DA_LCDM": DA_lcdm, "DA_IST": DA_ist})

        # Plot
        ax = plt.subplot(2, 3, bin_id)
        ax.errorbar(theta, w_obs, w_err, fmt="o", ms=2, color="k")
        th_plot = np.linspace(0.5, 5, 100)
        ax.plot(th_plot, gaussian_peak(th_plot, *popt), "-", color="crimson")
        ax.axvline(th_bao, color="crimson", ls="--")
        ax.axvline(th_lcdm, color="steelblue", ls=":")
        ax.set_title(f"Bin {bin_id} (z~{z_eff})")

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "bao_distance.png"), dpi=300)
    plt.close()

    with open(os.path.join(OUT_DIR, "bao_fit.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    print("Bin  z_eff  theta_BAO  theta_LCDM  theta_IST  chi2_LCDM  chi2_IST")
    chi2_l, chi2_i = 0, 0
    for r in rows:
        dl = (r["theta_BAO_deg"] - r["theta_LCDM"]) / r["theta_err"]
        di = (r["theta_BAO_deg"] - r["theta_IST"]) / r["theta_err"]
        chi2_l += dl**2; chi2_i += di**2
        print(f"  {r['bin']}   {r['z_eff']:.2f}   {r['theta_BAO_deg']:.3f}    "
              f"{r['theta_LCDM']:.3f}       {r['theta_IST']:.3f}      "
              f"{dl:6.2f}     {di:6.2f}")
    print(f"Total chi2: LCDM={chi2_l:.1f}, IST={chi2_i:.1f}, "
          f"dchi2={chi2_l-chi2_i:.1f}")

    print(f"Wrote {OUT_DIR}")


if __name__ == "__main__":
    main()
