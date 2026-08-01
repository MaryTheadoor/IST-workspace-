"""IST Phase 16 — Joint H(z)+Pantheon++DESI BAO fit (FIXED cosmology)"""
import csv, os, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase16_joint")
C_KM_S = 299792.458
R_D_FID = 147.09

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

# ---- cosmology ----
def Ez(z, Om): return np.sqrt(Om*(1+z)**3 + (1-Om))

def comoving(z, H0, Om):
    zs = np.linspace(0, z, 256)
    return C_KM_S / H0 * np.trapezoid(1.0/Ez(zs, Om), zs)

def Hz_lcdm(z, H0, Om): return H0 * Ez(z, Om)

def Hz_osc(z, H0, Om, eps0, Delta, beta=1/PHI):
    eps = eps0 * (1+z)**beta
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
def chi2_total(params, z_hz, H, sig, z_sne, mu, mu_err, osc):
    H0, Om = params[0], params[1]
    eps0, Delta, beta = params[2:] if osc else (0, PHI, 0)
    # H(z)
    hz_pred = Hz_osc(z_hz, H0, Om, eps0, Delta, beta) if osc else Hz_lcdm(z_hz, H0, Om)
    chi2_hz = np.sum(((hz_pred - H)/sig)**2)
    # SNe
    mu_p = mu_pred(z_sne, H0, Om, eps0, Delta, beta, oscillatory=osc)
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

# ---- main ----
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    zh, Hd, sh = load_hz()
    zs, mu_d, mu_e = load_pantheon()
    print(f"Data: {len(zh)} H(z), {len(zs)} SNe, {len(DESI_BAO)} BAO")

    # LCDM
    r_l = minimize(lambda p: chi2_total(p, zh, Hd, sh, zs, mu_d, mu_e, False),
                   [70, 0.3], method="Nelder-Mead", options={"maxiter": 3000})
    c2_l, (H0l, Oml) = r_l.fun, r_l.x
    print(f"LCDM: H0={H0l:.1f}, Om={Oml:.3f}, chi2={c2_l:.0f}")

    # Oscillatory fixed beta=1/phi
    r_f = minimize(lambda p: chi2_total(p, zh, Hd, sh, zs, mu_d, mu_e, True),
                   [H0l, Oml, 0.1, PHI, 1/PHI], method="Nelder-Mead",
                   options={"maxiter": 3000})
    Hf, Omf, ef, Df, bf = r_f.x
    d2f = c2_l - r_f.fun
    print(f"Osc(beta=1/phi): H0={Hf:.1f}, Om={Omf:.3f}, eps={ef:.3f}, "
          f"D={Df:.3f}, chi2={r_f.fun:.0f}, dchi2={d2f:.1f}")

    # Oscillatory free beta
    r_ff = minimize(lambda p: chi2_total(p, zh, Hd, sh, zs, mu_d, mu_e, True),
                    [H0l, Oml, ef, Df, bf], method="Nelder-Mead",
                    options={"maxiter": 3000})
    Hff, Omff, eff, Dff, bff = r_ff.x
    d2ff = c2_l - r_ff.fun
    print(f"Osc(free): H0={Hff:.1f}, Om={Omff:.3f}, eps={eff:.3f}, "
          f"D={Dff:.3f}, beta={bff:.3f}, chi2={r_ff.fun:.0f}, dchi2={d2ff:.1f}")

    # save
    with open(os.path.join(OUT_DIR, "joint_fit_results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model","H0","Om","eps0","Delta","beta","chi2","dchi2"])
        w.writerow(["LCDM", H0l, Oml, 0, 0, 0, c2_l, 0])
        w.writerow(["osc_fixed", Hf, Omf, ef, Df, bf, r_f.fun, d2f])
        w.writerow(["osc_free", Hff, Omff, eff, Dff, bff, r_ff.fun, d2ff])

    make_fig(zh, Hd, sh, zs, mu_d, mu_e, (H0l, Oml), (Hf, Omf, ef, Df, bf))
    print(f"Wrote {OUT_DIR}")

def make_fig(zh, Hd, sh, zs, mu_d, mu_e, pl, po):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    zz = np.linspace(0.01, 2.5, 200)
    ax = axes[0,0]
    ax.errorbar(zh, Hd, sh, fmt="o", ms=3, color="k")
    ax.plot(zz, Hz_lcdm(zz, *pl), "-", color="steelblue", lw=1.5, label="LCDM")
    ax.plot(zz, Hz_osc(zz, *po), "-", color="crimson", lw=1.5, label="IST")
    ax.set_xlabel("z"); ax.set_ylabel("H(z)"); ax.set_title("A. H(z) fit"); ax.legend(fontsize=8)

    ax = axes[0,1]
    mu_l = mu_pred(zs, *pl); mu_o = mu_pred(zs, *po, oscillatory=True)
    ax.errorbar(zs, mu_d-mu_l, mu_e, fmt=".", ms=1, color="steelblue", alpha=0.3)
    ax.errorbar(zs, mu_d-mu_o, mu_e, fmt=".", ms=1, color="crimson", alpha=0.3)
    ax.axhline(0, color="k", ls=":"); ax.set_xlabel("z"); ax.set_ylabel("mu residual")
    ax.set_title("B. SNe residuals"); ax.legend(["LCDM","IST"], fontsize=8)

    ax = axes[1,0]
    eps_z = abs(po[2])*(1+zz)**po[4]
    ax.plot(zz, eps_z, "-", color="crimson", lw=2)
    ax.set_xlabel("z"); ax.set_ylabel("eps(z)"); ax.set_title(f"C. eps(z) beta={po[4]:.3f}")

    ax = axes[1,1]
    ax.errorbar(zh, Hd, sh, fmt="o", ms=3, color="k")
    ax.plot(zz, Hz_osc(zz, *po), "-", color="crimson", lw=1.5)
    ax.set_xscale("log"); ax.set_xlabel("z"); ax.set_ylabel("H(z)")
    ax.set_title("D. H(z) log scale")

    fig.tight_layout(); fig.savefig(os.path.join(OUT_DIR, "joint_fit.png"), dpi=300); plt.close(fig)

if __name__ == "__main__":
    main()
