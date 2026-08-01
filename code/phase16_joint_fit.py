"""IST Phase 16 — Joint H(z)+Pantheon++DESI BAO fit (FIXED cosmology)"""
import csv, os, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase16_joint")
C_KM_S = 299792.458
R_D_FID = 147.09
ALPHA = 1/137.036
EPS_PRED = ALPHA / PHI**2  # associator prediction ~0.00278

# DESI DR1 BAO
DESI_BAO = [
    (0.51, 13.62, 0.25, 20.01, 0.36, -0.45),
    (0.71, 16.85, 0.33, 20.08, 0.46, -0.42),
    (0.93, 21.71, 0.61, 17.88, 0.63, -0.45),
    (1.32, 26.03, 0.67, 13.52, 1.01, -0.38),
    (1.49, 27.85, 1.39, 12.51, 2.79, -0.52),
]

def load_hz():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "hz_cosmic_chronometers.csv")
    z, H, sig = [], [], []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("#") or not line: continue
            p = line.split(","); z.append(float(p[0])); H.append(float(p[1])); sig.append(float(p[2]))
    return np.array(z), np.array(H), np.array(sig)

def load_pantheon():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "pantheon_plus.txt")
    z_cmb, mu, mu_err = [], [], []
    with open(path) as fh:
        header = fh.readline().split()
        iz = header.index("zCMB"); imu = header.index("MU_SH0ES")
        ierr = next(i for i, h in enumerate(header) if "MU_SH0ES" in h and "ERR" in h)
        for line in fh:
            if not line.strip(): continue
            p = line.split()
            if len(p) < max(iz, imu, ierr) + 1: continue
            z_cmb.append(float(p[iz])); mu.append(float(p[imu])); mu_err.append(float(p[ierr]))
    return np.array(z_cmb), np.array(mu), np.array(mu_err)

def cosmic_time(z, H0, Om):
    """Age of the universe at redshift z (Gyr), flat LCDM."""
    OL = 1 - Om
    return 2/(3*H0*np.sqrt(OL)/3.086e19*3.156e16) * \
        np.arcsinh(np.sqrt(OL/(Om*(1+z)**3))) * 3.156e16 / 1e9
# simpler: use H0 in km/s/Mpc, return in Gyr
# t = (977.8/H0) * integral_0^z dz/((1+z)E(z)) ... just compute numerically

def cosmic_time_Gyr(z, H0, Om):
    """t(z) in Gyr by numerical integration."""
    z_arr = np.atleast_1d(z)
    res = np.zeros_like(z_arr, dtype=float)
    for i, zi in enumerate(z_arr):
        zs = np.linspace(zi, 10, 200)  # integrate from z to infinity
        integrand = 1.0 / ((1+zs) * Ez(zs, Om))
        res[i] = 977.8 / H0 * np.trapezoid(integrand, zs)  # Gyr
    return float(res[0]) if len(res) == 1 else res
def Ez(z, Om): return np.sqrt(Om*(1+z)**3 + (1-Om))

def comoving(z, H0, Om):
    zs = np.linspace(0, z, 256)
    return C_KM_S / H0 * np.trapezoid(1.0/Ez(zs, Om), zs)

def Hz_lcdm(z, H0, Om): return H0 * Ez(z, Om)

def Hz_osc(z, H0, Om, eps0, Delta, beta=1/PHI):
    eps = eps0 * (1+z)**beta
    return _hz_osc(z, H0, Om, eps, Delta)

def Hz_osc_cosmic(z, H0, Om, eps0, Delta):
    """epsilon(z) = eps0 * (t0/t(z))^(1/phi) — physical plonk-tick scaling."""
    t0 = cosmic_time_Gyr(0, H0, Om)
    tz = cosmic_time_Gyr(z, H0, Om)
    tz = np.maximum(tz, 0.01)
    eps = eps0 * (t0 / tz) ** (1/PHI)
    return _hz_osc(z, H0, Om, eps, Delta)

def _hz_osc(z, H0, Om, eps, Delta):
    osc = 1 + eps * np.cos(2*np.pi*np.log(1+z)/Delta)
    return H0 * np.sqrt(Om*(1+z)**3 + (1-Om)*np.maximum(osc, 0.01))

def mu_pred(z, H0, Om, eps0=0, Delta=PHI, beta=0, oscillatory=False):
    z = np.atleast_1d(z)
    res = np.zeros_like(z, dtype=float)
    for i, zi in enumerate(z):
        zs = np.linspace(0, zi, 128)
        if oscillatory:
            Hz = Hz_osc(zs, H0, Om, eps0, Delta, beta)
        else:
            Hz = Hz_lcdm(zs, H0, Om)
        Hz = np.maximum(Hz, 0.1)
        chi = C_KM_S * np.trapezoid(1.0/Hz, zs)
        res[i] = 5 * np.log10(max((1+zi)*chi, 0.1) * 1e6 / 10)
    return float(res[0]) if len(res) == 1 else res

# ---- chi^2 ----
def chi2_total(params, z_hz, H, sig, z_sne, mu, mu_err, model="lcdm"):
    """model: 'lcdm', 'powerlaw', 'cosmic', 'fixed_eps'"""
    if model == "lcdm":
        H0, Om = params
        hz_pred = Hz_lcdm(z_hz, H0, Om)
    elif model == "fixed_eps":
        H0, Om, Delta = params
        eps0 = EPS_PRED; beta = 1/PHI
        hz_pred = Hz_osc(z_hz, H0, Om, eps0, Delta, beta)
    elif model == "cosmic":
        H0, Om, eps0, Delta = params
        hz_pred = Hz_osc_cosmic(z_hz, H0, Om, eps0, Delta)
    else:  # powerlaw
        H0, Om, eps0, Delta, beta = params
        hz_pred = Hz_osc(z_hz, H0, Om, eps0, Delta, beta)
    chi2_hz = np.sum(((hz_pred - H)/sig)**2)
    if model == "lcdm":
        mu_p = mu_pred(z_sne, H0, Om)
    elif model == "fixed_eps":
        mu_p = mu_pred(z_sne, H0, Om, EPS_PRED, Delta, 1/PHI, oscillatory=True)
    elif model == "cosmic":
        mu_p = mu_pred(z_sne, H0, Om, eps0, Delta, 0, oscillatory=True)
        # mu_pred expects beta param — use Hz_osc_cosmic instead
        mu_p = mu_pred_cosmic(z_sne, H0, Om, eps0, Delta)
    else:
        mu_p = mu_pred(z_sne, H0, Om, eps0, Delta, beta, oscillatory=True)
    chi2_sne = np.sum(((mu_p - mu)/mu_err)**2)
    # BAO
    chi2_bao = 0.0
    for ze, DM_o, dDM, DH_o, dDH, rc in DESI_BAO:
        chi = comoving(ze, H0, Om)
        Hz_val = Hz_lcdm(ze, H0, Om)
        DM_p = chi / R_D_FID
        DH_p = C_KM_S / Hz_val / R_D_FID
        cov = np.array([[dDM**2, rc*dDM*dDH],[rc*dDM*dDH, dDH**2]])
        diff = np.array([DM_p-DM_o, DH_p-DH_o])
        chi2_bao += diff @ np.linalg.inv(cov) @ diff
    return chi2_hz + chi2_sne + chi2_bao


def mu_pred_cosmic(z, H0, Om, eps0, Delta):
    z = np.atleast_1d(z)
    res = np.zeros_like(z, dtype=float)
    for i, zi in enumerate(z):
        zs = np.linspace(0, zi, 128)
        Hz = Hz_osc_cosmic(zs, H0, Om, eps0, Delta)
        Hz = np.maximum(Hz, 0.1)
        chi = C_KM_S * np.trapezoid(1.0/Hz, zs)
        res[i] = 5 * np.log10(max((1+zi)*chi, 0.1) * 1e6 / 10)
    return float(res[0]) if len(res) == 1 else res

# ---- main ----
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    zh, Hd, sh = load_hz()
    zs, mu_d, mu_e = load_pantheon()
    print(f"Data: {len(zh)} H(z), {len(zs)} SNe, {len(DESI_BAO)} BAO")

    results = {}
    # ── A: LCDM ─────────────────────────────────────────────────
    r = minimize(lambda p: chi2_total(p, zh, Hd, sh, zs, mu_d, mu_e, "lcdm"),
                 [70, 0.3], method="Nelder-Mead", options={"maxiter": 800})
    results["LCDM"] = {"H0": r.x[0], "Om": r.x[1], "chi2": r.fun, "dchi2": 0}
    print(f"LCDM: H0={r.x[0]:.1f}, Om={r.x[1]:.3f}, chi2={r.fun:.0f}")

    # ── B: Power-law, beta = 1/phi ──────────────────────────────
    r = minimize(lambda p: chi2_total(p, zh, Hd, sh, zs, mu_d, mu_e, "powerlaw"),
                 [results["LCDM"]["H0"], results["LCDM"]["Om"], 0.1, PHI, 1/PHI],
                 method="Nelder-Mead", options={"maxiter": 800})
    Hf, Omf, ef, Df, bf = r.x
    d2 = results["LCDM"]["chi2"] - r.fun
    results["powerlaw_beta_fixed"] = {"H0": Hf, "Om": Omf, "eps0": ef,
        "Delta": Df, "beta": bf, "chi2": r.fun, "dchi2": d2}
    print(f"Power-law beta=1/phi: H0={Hf:.1f} Om={Omf:.3f} "
          f"eps0={ef:.3f} D={Df:.3f} chi2={r.fun:.0f} dchi2={d2:.1f}")

    # ── C: Power-law, free beta ─────────────────────────────────
    r = minimize(lambda p: chi2_total(p, zh, Hd, sh, zs, mu_d, mu_e, "powerlaw"),
                 [Hf, Omf, ef, Df, bf], method="Nelder-Mead",
                 options={"maxiter": 800})
    Hff, Omff, eff, Dff, bff = r.x
    d2f = results["LCDM"]["chi2"] - r.fun
    results["powerlaw_beta_free"] = {"H0": Hff, "Om": Omff, "eps0": eff,
        "Delta": Dff, "beta": bff, "chi2": r.fun, "dchi2": d2f}
    print(f"Power-law free: H0={Hff:.1f} Om={Omff:.3f} "
          f"eps0={eff:.3f} D={Dff:.3f} beta={bff:.3f} "
          f"chi2={r.fun:.0f} dchi2={d2f:.1f}")

    # ── D: Fixed eps0 = alpha/phi^2 ─────────────────────────────
    print(f"Theoretical eps0 = alpha/phi^2 = {EPS_PRED:.4f}")
    r = minimize(lambda p: chi2_total(p, zh, Hd, sh, zs, mu_d, mu_e, "fixed_eps"),
                 [Hf, Omf, Df], method="Nelder-Mead",
                 options={"maxiter": 800})
    Hx, Omx, Dx = r.x
    d2x = results["LCDM"]["chi2"] - r.fun
    results["fixed_eps0"] = {"H0": Hx, "Om": Omx, "eps0": EPS_PRED,
        "Delta": Dx, "chi2": r.fun, "dchi2": d2x}
    print(f"Fixed eps0: H0={Hx:.1f} Om={Omx:.3f} "
          f"D={Dx:.3f} chi2={r.fun:.0f} dchi2={d2x:.1f}")

    # ── E: Beta profile — lightweight grid over beta, fix other params ─
    betas = np.geomspace(0.1, 10, 20)
    beta_scan = []
    fix_params = [Hf, Omf, ef, Df]
    for bv in betas:
        c2 = chi2_total([Hf, Omf, ef, Df, bv], zh, Hd, sh, zs, mu_d, mu_e, "powerlaw")
        beta_scan.append((bv, c2))
    best_b = min(beta_scan, key=lambda x: x[1])
    c2_phi = next(c for b, c in beta_scan if abs(b - 1/PHI) < 0.1)
    print(f"Beta scan (fixed H0,Om,eps,D): best={best_b[0]:.2f} chi2={best_b[1]:.0f}")
    print(f"  beta=1/phi chi2={c2_phi:.0f}, dchi2={c2_phi - best_b[1]:.1f}")

    # save
    with open(os.path.join(OUT_DIR, "joint_fit_results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model","H0","Om","eps0","Delta","beta","chi2","dchi2"])
        for name, vals in results.items():
            if name == "cosmic_time": continue  # skip until faster
            w.writerow([name, vals.get("H0",0), vals.get("Om",0),
                       vals.get("eps0",0), vals.get("Delta",0),
                       vals.get("beta",0), vals["chi2"], vals["dchi2"]])
    with open(os.path.join(OUT_DIR, "beta_scan.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["beta","chi2"])
        w.writerows(beta_scan)

    make_fig(zh, Hd, sh, zs, mu_d, mu_e, results, beta_scan)
    print(f"Wrote {OUT_DIR}")

def make_fig(zh, Hd, sh, zs, mu_d, mu_e, results, beta_scan):
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    zz = np.linspace(0.01, 2.5, 200)

    pl = (results["LCDM"]["H0"], results["LCDM"]["Om"])
    po = (results["powerlaw_beta_fixed"]["H0"],
          results["powerlaw_beta_fixed"]["Om"],
          results["powerlaw_beta_fixed"]["eps0"],
          results["powerlaw_beta_fixed"]["Delta"],
          results["powerlaw_beta_fixed"]["beta"])

    ax = axes[0,0]
    ax.errorbar(zh, Hd, sh, fmt="o", ms=3, color="k", label="H(z)")
    ax.plot(zz, Hz_lcdm(zz, *pl), "-", color="steelblue", lw=1.5, label="LCDM")
    ax.plot(zz, Hz_osc(zz, *po), "-", color="crimson", lw=1.5, label="IST")
    ax.set_xlabel("z"); ax.set_ylabel("H(z)"); ax.legend(fontsize=8)
    ax.set_title("A. H(z) fit")

    ax = axes[0,1]
    # beta profile likelihood
    bs, cs = zip(*beta_scan)
    c_min = min(cs)
    dchi2s = [c - c_min for c in cs]
    ax.plot(bs, dchi2s, "o-", color="crimson", lw=2, ms=4)
    ax.axhline(1.0, color="gray", ls="--", label="1-sigma")
    ax.axhline(4.0, color="gray", ls=":", label="2-sigma")
    ax.axvline(1/PHI, color="seagreen", ls="--", label="beta=1/phi")
    ax.set_xlabel(r"$\beta$"); ax.set_ylabel(r"$\Delta\chi^2$")
    ax.set_title("B. Beta profile likelihood")
    ax.legend(fontsize=8)

    ax = axes[1,0]
    # model comparison bar chart
    models = list(results.keys())
    dchi2s = [results[m]["dchi2"] for m in models]
    colors_bar = ["gray" if m == "LCDM" else "crimson" if "powerlaw" in m
                  else "seagreen" if "cosmic" in m else "steelblue"
                  for m in models]
    ax.barh(models, dchi2s, color=colors_bar)
    ax.set_xlabel(r"$\Delta\chi^2$ vs LCDM")
    ax.set_title("C. Model comparison (dchi2 vs LCDM)")

    ax = axes[1,1]
    eps_vals = [results[m].get("eps0", 0) for m in models if "eps0" in results[m]]
    eps_labels = [m for m in models if "eps0" in results[m]]
    ax.barh(eps_labels, eps_vals, color=["crimson","crimson","seagreen","steelblue"])
    ax.axvline(EPS_PRED, color="gray", ls="--", label=f"pred={EPS_PRED:.4f}")
    ax.set_xlabel(r"$\epsilon_0$"); ax.set_title("D. Present-day amplitude")
    ax.legend(fontsize=8)

    fig.tight_layout(); fig.savefig(os.path.join(OUT_DIR, "joint_fit.png"), dpi=300)
    plt.close(fig)

if __name__ == "__main__":
    main()


def run_dimensional_test():
    """Test beta = phi^d for d=1,2,3,4; confirm d=3 gives best fit."""
    zh, Hd, sh = load_hz()
    zs, mu_d, mu_e = load_pantheon()
    dim_results = []
    for d in [1, 2, 3, 4]:
        beta = PHI ** d
        r = minimize(lambda p: chi2_total(
            [p[0], p[1], p[2], p[3], beta], zh, Hd, sh, zs, mu_d, mu_e,
            "powerlaw"),
            [71, 0.28, 0.06, 2.2], method="Nelder-Mead",
            options={"maxiter": 300})
        dim_results.append((d, beta, r.fun, r.x))
    best = min(dim_results, key=lambda x: x[2])
    for d, beta, c2, x in dim_results:
        lbl = " <<< BEST" if d == best[0] else ""
        print(f"d={d} beta=phi^{d}={beta:.3f} chi2={c2:.0f} "
              f"dchi2_vs_best={c2-best[2]:.1f}{lbl}")
    return dim_results
