"""
Phase 60: Auditing the "4-sigma" Oscillatory-Dark-Energy Headline + the Amplitude Bridge
=========================================================================================
Track A -- the 4-sigma audit. Reproduces the paper's headline observable claim
(ist_v8_0 SS4.4: oscillatory DE preferred over LCDM at ~4sigma, Delta_chi2 =
22.1, in a joint fit to 60 H(z) + 1701 Pantheon+ SNe + DESI DR1 BAO) in clean
reproducible code, then applies the Phase-59 discipline:

  H60a  reproduce the joint fit (free epsilon0, Delta, beta)
  H60b  pre-registered strict fit: (eps0, Delta, beta) = (alpha/phi^2, ln phi,
        phi^3) and the v8-consistent (alpha/phi^2, ln phi, 1/phi) variant
  H60c  look-elsewhere accounting: Delta-profile over the log-redshift window,
        frequency-band trial count, global significance of the headline Delta_chi2

Track B -- the amplitude bridge. Phase 59's golden-period fit wants eps ~ 0.1;
the master equation gives eps0 = alpha/phi^2 = 0.002787 (~37x gap).

  H60d  does eps_eff(z) = eps0*(1+z)^beta with the derived beta = phi^3 (and the
        code's beta = 1/phi) bridge the gap at each dataset's characteristic z?

Model (as in phase16_joint_fit.py):
  H(z) = H0 sqrt[ Om(1+z)^3 + (1-Om) * max(1 + eps(z)*cos(2*pi*ln(1+z)/Delta), 0.01) ]
  eps(z) = eps0 * (1+z)^beta

Data: data/hz_cosmic_chronometers.csv (60), data/pantheon_plus.txt (1701),
      DESI DR1 BAO (5 bins, hard-coded as in phase16).
"""

import os
import csv

import numpy as np
from scipy.optimize import minimize
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PHI = (1 + np.sqrt(5)) / 2
ALPHA = 1 / 137.035999084
EPS0_DERIVED = ALPHA / PHI**2
DELTA0_DERIVED = np.log(PHI)
BETA0_DERIVED = PHI**3
BETA_INV_PHI = 1 / PHI
C_KM_S = 299792.458
R_D_FID = 147.09

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(_REPO, "data", "hz_cosmic_chronometers.csv")
PANTHEON_PATH = os.path.join(_REPO, "data", "pantheon_plus.txt")
OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase60")
os.makedirs(OUT_DIR, exist_ok=True)

# DESI DR1 BAO (z, D_M/r_d, sig_DM, D_H/r_d, sig_DH, corr) -- phase16 values
DESI_BAO = [
    (0.51, 13.62, 0.25, 20.01, 0.36, -0.45),
    (0.71, 16.85, 0.33, 20.08, 0.46, -0.42),
    (0.93, 21.71, 0.61, 17.88, 0.63, -0.45),
    (1.32, 26.03, 0.67, 13.52, 1.01, -0.38),
    (1.49, 27.85, 1.39, 12.51, 2.79, -0.52),
]

SCAN_MIN = 0.3
SCAN_MAX = 5.0
N_GRID = 40
N_INT = 500


def load_hz(path=DATA_PATH):
    z, H, sig = [], [], []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            p = line.split(",")
            z.append(float(p[0])); H.append(float(p[1])); sig.append(float(p[2]))
    z = np.array(z); H = np.array(H); sig = np.array(sig)
    o = np.argsort(z)
    return z[o], H[o], sig[o]


def load_pantheon(path=PANTHEON_PATH):
    z, mu, mu_err = [], [], []
    with open(path) as fh:
        header = fh.readline().split()
        iz = header.index("zCMB")
        imu = header.index("MU_SH0ES")
        ierr = next(i for i, h in enumerate(header)
                    if h == "MU_SH0ES_ERR_DIAG")
        for line in fh:
            if not line.strip():
                continue
            p = line.split()
            if len(p) < max(iz, imu, ierr) + 1:
                continue
            z.append(float(p[iz])); mu.append(float(p[imu]))
            mu_err.append(float(p[ierr]))
    z = np.array(z); mu = np.array(mu); mu_err = np.array(mu_err)
    o = np.argsort(z)
    return z[o], mu[o], mu_err[o]


def hz_osc(z, H0, Om, eps0, Delta, beta):
    eps = eps0 * (1 + z) ** beta
    osc = 1 + eps * np.cos(2 * np.pi * np.log(1 + z) / Delta)
    return H0 * np.sqrt(Om * (1 + z) ** 3 + (1 - Om) * np.maximum(osc, 0.01))


def ez(z, Om):
    return np.sqrt(Om * (1 + z) ** 3 + (1 - Om))


def bao_chi2(H0, Om):
    total = 0.0
    for ze, DM_o, dDM, DH_o, dDH, rc in DESI_BAO:
        zs = np.linspace(0, ze, 128)
        chi = C_KM_S / H0 * np.trapezoid(1.0 / ez(zs, Om), zs)
        Hz = H0 * ez(ze, Om)
        DM_p = chi / R_D_FID
        DH_p = C_KM_S / Hz / R_D_FID
        cov = np.array([[dDM ** 2, rc * dDM * dDH], [rc * dDM * dDH, dDH ** 2]])
        diff = np.array([DM_p - DM_o, DH_p - DH_o])
        total += diff @ np.linalg.inv(cov) @ diff
    return total


def sne_chi2(z_sne, mu, mu_err, H0, Om, eps0, Delta, beta, zgrid):
    hz = hz_osc(zgrid, H0, Om, eps0, Delta, beta)
    inv = 1.0 / np.maximum(hz, 0.1)
    chi_int = np.concatenate(
        ([0.0], np.cumsum(0.5 * (inv[:-1] + inv[1:]) * np.diff(zgrid))))
    chi = np.interp(z_sne, zgrid, chi_int)
    dl = np.maximum((1 + z_sne) * C_KM_S * chi, 0.1)
    mu_p = 5 * np.log10(dl * 1e6 / 10)
    return float(np.sum(((mu_p - mu) / mu_err) ** 2))


def chi2_joint(params, z_hz, H, sig, z_sne, mu, mu_err, zgrid, model,
               fixed=None):
    """Joint H(z)+SNe+BAO chi2. model: 'lcdm' | 'free' | 'prereg'."""
    if model == "lcdm":
        H0, Om = params
        eps0, Delta, beta = 0.0, DELTA0_DERIVED, 0.0
        hz_pred = H0 * ez(z_hz, Om)
    elif model in ("free", "free_nosign"):
        H0, Om, eps0, Delta, beta = params
        hz_pred = hz_osc(z_hz, H0, Om, eps0, Delta, beta)
    else:  # prereg
        H0, Om = params
        eps0, Delta, beta = fixed
        hz_pred = hz_osc(z_hz, H0, Om, eps0, Delta, beta)
    chi2 = np.sum(((hz_pred - H) / sig) ** 2)
    chi2 += sne_chi2(z_sne, mu, mu_err, H0, Om, eps0, Delta, beta, zgrid)
    chi2 += bao_chi2(H0, Om)
    return float(chi2)


def fit_joint(z_hz, H, sig, z_sne, mu, mu_err, zgrid, model, x0, fixed=None,
              maxiter=1200, ranges=None):
    if ranges is None:
        if model == "lcdm":
            ranges = [(50, 85), (0.1, 0.6)]
        elif model == "free":
            ranges = [(50, 85), (0.1, 0.6), (0.0, 0.3), (SCAN_MIN, SCAN_MAX),
                      (-2.0, 10.0)]
        elif model == "free_nosign":
            ranges = [(50, 85), (0.1, 0.6), (-0.3, 0.3), (SCAN_MIN, SCAN_MAX),
                      (-2.0, 10.0)]
        else:
            ranges = [(50, 85), (0.1, 0.6)]
    ranges = list(ranges)

    def obj(p):
        pen = 0.0
        for (lo, hi), x in zip(ranges, p):
            if x < lo or x > hi:
                return 1e12 + pen
            if x < lo:
                pen += (lo - x) ** 2
            elif x > hi:
                pen += (x - hi) ** 2
        c = chi2_joint(p, z_hz, H, sig, z_sne, mu, mu_err, zgrid, model,
                       fixed=fixed)
        return c if np.isfinite(c) else 1e12

    res = minimize(obj, x0, method="Nelder-Mead",
                   options={"maxiter": maxiter})
    return res


def run_audit():
    z_hz, H, sig = load_hz()
    z_sne, mu, mu_err = load_pantheon()
    zgrid = np.linspace(0.0, max(z_hz.max(), z_sne.max()) * 1.02, N_INT)

    out = {}

    # ---- H60a: LCDM baseline + free oscillatory fit ----
    r = fit_joint(z_hz, H, sig, z_sne, mu, mu_err, zgrid, "lcdm",
                  [70.0, 0.3])
    chi2_lcdm, H0_l, Om_l = r.fun, r.x[0], r.x[1]

    r = fit_joint(z_hz, H, sig, z_sne, mu, mu_err, zgrid, "free",
                  [H0_l, Om_l, 0.05, DELTA0_DERIVED, BETA_INV_PHI])
    chi2_free, (H0_f, Om_f, eps0_f, Delta_f, beta_f) = r.fun, r.x

    out["lcdm"] = {"H0": H0_l, "Om": Om_l, "chi2": chi2_lcdm, "dchi2": 0.0}
    out["free"] = {"H0": H0_f, "Om": Om_f, "eps0": eps0_f, "Delta": Delta_f,
                   "beta": beta_f, "chi2": chi2_free,
                   "dchi2": chi2_lcdm - chi2_free}
    p_local_free = stats.chi2.sf(chi2_lcdm - chi2_free, df=3)
    out["free"]["p_local_3dof"] = p_local_free

    # H60a-bis: same free fit but allowing the UNPHYSICAL sign of eps0
    # (eps0 < 0 == a free phase pi, an unacknowledged extra dof)
    r = fit_joint(z_hz, H, sig, z_sne, mu, mu_err, zgrid, "free_nosign",
                  [H0_l, Om_l, -0.05, DELTA0_DERIVED, BETA_INV_PHI])
    chi2_ns, (H0_ns, Om_ns, eps0_ns, Delta_ns, beta_ns) = r.fun, r.x
    out["free_nosign"] = {"H0": H0_ns, "Om": Om_ns, "eps0": eps0_ns,
                          "Delta": Delta_ns, "beta": beta_ns,
                          "chi2": chi2_ns, "dchi2": chi2_lcdm - chi2_ns,
                          "p_local_3dof": float(stats.chi2.sf(
                              chi2_lcdm - chi2_ns, df=3))}
    out["free_nosign"]["eps0_sign"] = int(np.sign(eps0_ns))

    # ---- H60b: pre-registered strict fits ----
    for name, (e0, d0, b0) in [
        ("prereg_phi3", (EPS0_DERIVED, DELTA0_DERIVED, BETA0_DERIVED)),
        ("prereg_invphi", (EPS0_DERIVED, DELTA0_DERIVED, BETA_INV_PHI)),
    ]:
        r = fit_joint(z_hz, H, sig, z_sne, mu, mu_err, zgrid, "prereg",
                      [H0_l, Om_l], fixed=(e0, d0, b0))
        out[name] = {"H0": r.x[0], "Om": r.x[1], "eps0": e0, "Delta": d0,
                     "beta": b0, "chi2": r.fun, "dchi2": chi2_lcdm - r.fun}

    # ---- H60c: Delta-profile with refits (look-elsewhere on the period) ----
    dgrid = np.linspace(SCAN_MIN, SCAN_MAX, N_GRID)
    prof = []
    best_d, best_c2 = dgrid[0], np.inf
    for D in dgrid:
        # at fixed Delta, fit (H0, Om, eps0, beta): 2 dof over LCDM
        r = fit_joint(z_hz, H, sig, z_sne, mu, mu_err, zgrid, "free",
                      [H0_f, Om_f, eps0_f, D, beta_f], maxiter=700)
        prof.append((D, r.fun))
        if r.fun < best_c2:
            best_c2, best_d = r.fun, D
    prof = np.array(prof)
    dchi2_prof = chi2_lcdm - prof[:, 1]
    best_dchi2 = float(dchi2_prof.max())
    p_local_d = float(stats.chi2.sf(best_dchi2, df=2))
    ln1pz_max = np.log(1 + z_hz.max())
    n_trials = max(1, int(round((1 / SCAN_MIN - 1 / SCAN_MAX) * ln1pz_max)))
    p_global_d = 1.0 - (1.0 - p_local_d) ** n_trials
    out["delta_profile"] = {"grid": dgrid, "prof": prof,
                            "dchi2": dchi2_prof,
                            "best_Delta": best_d, "best_dchi2": best_dchi2,
                            "p_local": p_local_d, "trials": n_trials,
                            "p_global": p_global_d}

    # no-sign (anti-phase) Delta-profile: where the "4-sigma" actually lived
    prof_ns = []
    best_dn, best_c2n = dgrid[0], np.inf
    for D in dgrid:
        r = fit_joint(z_hz, H, sig, z_sne, mu, mu_err, zgrid, "free_nosign",
                      [H0_l, Om_l, -0.05, D, BETA_INV_PHI], maxiter=700)
        prof_ns.append((D, r.fun))
        if r.fun < best_c2n:
            best_c2n, best_dn = r.fun, D
    prof_ns = np.array(prof_ns)
    dchi2_ns = chi2_lcdm - prof_ns[:, 1]
    out["delta_profile_nosign"] = {
        "grid": dgrid, "prof": prof_ns, "dchi2": dchi2_ns,
        "best_Delta": best_dn, "best_dchi2": float(dchi2_ns.max()),
        "p_local": float(stats.chi2.sf(dchi2_ns.max(), df=2)),
        "trials": n_trials,
        "p_global": 1.0 - (1.0 - float(stats.chi2.sf(dchi2_ns.max(), df=2)))
        ** n_trials}

    # ---- beta profile at best free-fit params (shape dimension) ----
    bg = np.geomspace(0.1, 10.0, 25)
    bprof = []
    for b in bg:
        c2 = chi2_joint([H0_f, Om_f, eps0_f, Delta_f, b], z_hz, H, sig,
                        z_sne, mu, mu_err, zgrid, "free")
        bprof.append((b, c2))
    bprof = np.array(bprof)
    out["beta_profile"] = {"grid": bg, "chi2": bprof[:, 1],
                           "dchi2": chi2_lcdm - bprof[:, 1],
                           "best_beta": bg[np.argmin(bprof[:, 1])],
                           "best_chi2": float(bprof[:, 1].min())}

    # ---- H60d: the amplitude bridge ----
    zb_hz = float(np.average(z_hz, weights=1.0 / sig))
    zb_sne = float(np.average(z_sne, weights=1.0 / mu_err))
    eps_eff = {}
    for label, zbar in [("hz", zb_hz), ("sne", zb_sne)]:
        eps_eff[label] = {
            "zbar": zbar,
            "eps_eff_phi3": EPS0_DERIVED * (1 + zbar) ** BETA0_DERIVED,
            "eps_eff_invphi": EPS0_DERIVED * (1 + zbar) ** BETA_INV_PHI,
            "eps_eff_fitted": eps0_f * (1 + zbar) ** beta_f,
        }
    eps_eff["phase59_eps"] = 0.1064
    out["amplitude_bridge"] = eps_eff

    write_outputs(out, z_hz, H, sig, z_sne, mu, mu_err, zgrid)
    return out


def write_outputs(out, z_hz, H, sig, z_sne, mu, mu_err, zgrid):
    dpn = out["delta_profile_nosign"]
    csv_path = os.path.join(OUT_DIR, "joint_fit_audit.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["model", "H0", "Om", "eps0", "Delta", "beta", "chi2",
                    "dchi2_vs_lcdm"])
        for name in ["lcdm", "free", "free_nosign", "prereg_phi3",
                     "prereg_invphi"]:
            v = out[name]
            w.writerow([name, v.get("H0", 0), v.get("Om", 0),
                        v.get("eps0", 0), v.get("Delta", 0),
                        v.get("beta", 0), v["chi2"], v["dchi2"]])

    dp = out["delta_profile"]
    with open(os.path.join(OUT_DIR, "delta_profile.csv"), "w", encoding="utf-8") as f:
        f.write("Delta,dchi2_vs_lcdm\n")
        for D, c in zip(dp["grid"], dp["dchi2"]):
            f.write(f"{D:.6f},{c:.6f}\n")

    dpn = out["delta_profile_nosign"]
    with open(os.path.join(OUT_DIR, "delta_profile_nosign.csv"), "w",
              encoding="utf-8") as f:
        f.write("Delta,dchi2_vs_lcdm\n")
        for D, c in zip(dpn["grid"], dpn["dchi2"]):
            f.write(f"{D:.6f},{c:.6f}\n")

    bp = out["beta_profile"]
    with open(os.path.join(OUT_DIR, "beta_profile.csv"), "w", encoding="utf-8") as f:
        f.write("beta,chi2,dchi2_vs_lcdm\n")
        for b, c, d in zip(bp["grid"], bp["chi2"], bp["dchi2"]):
            f.write(f"{b:.6f},{c:.6f},{d:.6f}\n")

    ab = out["amplitude_bridge"]
    with open(os.path.join(OUT_DIR, "amplitude_bridge.csv"), "w", encoding="utf-8") as f:
        f.write("dataset,zbar,eps_eff_phi3,eps_eff_invphi,eps_eff_fitted\n")
        for label in ["hz", "sne"]:
            e = ab[label]
            f.write(f"{label},{e['zbar']:.4f},{e['eps_eff_phi3']:.6f},"
                    f"{e['eps_eff_invphi']:.6f},{e['eps_eff_fitted']:.6f}\n")

    txt = os.path.join(OUT_DIR, "audit_summary.txt")
    with open(txt, "w", encoding="utf-8") as f:
        w = f.write
        w("=" * 70 + "\n")
        w("PHASE 60 - AUDIT OF THE '4-SIGMA' OSCILLATORY-DE HEADLINE\n")
        w("+ amplitude bridge (Phase 59 eps ~ 0.1 vs alpha/phi^2)\n")
        w("=" * 70 + "\n\n")
        l = out["lcdm"]; fr = out["free"]
        w(f"LCDM : chi2 = {l['chi2']:.1f}, H0 = {l['H0']:.2f}, Om = {l['Om']:.3f}\n")
        w(f"FREE : chi2 = {fr['chi2']:.1f}, dchi2 = {fr['dchi2']:+.1f} "
          f"(claim: +22.1)\n")
        w(f"       H0 = {fr['H0']:.2f} (claim 71.4), eps0 = {fr['eps0']:.5f}, "
          f"Delta = {fr['Delta']:.3f}, beta = {fr['beta']:.3f} (claim ~4.16)\n")
        w(f"       local p (3 dof) = {fr['p_local_3dof']:.4f}\n")
        ns = out["free_nosign"]
        w(f"FREE_NOSIGN (eps0 sign free = hidden phase): chi2 = {ns['chi2']:.1f}, "
          f"dchi2 = {ns['dchi2']:+.1f}\n")
        w(f"       H0 = {ns['H0']:.2f}, eps0 = {ns['eps0']:.5f} "
          f"(sign {ns['eps0_sign']:+d}), Delta = {ns['Delta']:.3f}, "
          f"beta = {ns['beta']:.3f}\n\n")
        for name in ["prereg_phi3", "prereg_invphi"]:
            v = out[name]
            w(f"{name}: chi2 = {v['chi2']:.1f}, dchi2 = {v['dchi2']:+.2f} "
              f"(eps0={v['eps0']:.5f}, Delta={v['Delta']:.4f}, "
              f"beta={v['beta']:.3f})\n")
        w("\nH60c - LOOK-ELSEWHERE (Delta-profile over joint data)\n")
        w("-" * 70 + "\n")
        w(f"  best Delta = {dp['best_Delta']:.3f}, "
          f"best dchi2 = {dp['best_dchi2']:+.2f}\n")
        w(f"  local p (2 dof) = {dp['p_local']:.4f}, trials = {dp['trials']}, "
          f"GLOBAL p = {dp['p_global']:.4f}\n")
        w(f"  no-sign (anti-phase) profile: best Delta = "
          f"{dpn['best_Delta']:.3f}, best dchi2 = {dpn['best_dchi2']:+.2f}, "
          f"GLOBAL p = {dpn['p_global']:.4f}\n\n")
        w("  beta profile: best beta = "
          f"{bp['best_beta']:.2f}, chi2 = {bp['best_chi2']:.1f}, "
          f"dchi2_vs_free = {bp['best_chi2']-fr['chi2']:+.1f}\n\n")
        w("H60d - AMPLITUDE BRIDGE\n")
        w("-" * 70 + "\n")
        for label in ["hz", "sne"]:
            e = ab[label]
            w(f"  {label}: zbar = {e['zbar']:.3f} | eps_eff(phi^3) = "
              f"{e['eps_eff_phi3']:.5f} | eps_eff(1/phi) = "
              f"{e['eps_eff_invphi']:.5f} | fitted = {e['eps_eff_fitted']:.5f}\n")
        w(f"  Phase 59 golden-period eps = {ab['phase59_eps']:.4f}; "
          f"master-equation eps0 = {EPS0_DERIVED:.5f} "
          f"(gap x{ab['phase59_eps'] / EPS0_DERIVED:.1f})\n")
        w("\nInterpretation in notes/IST_Phase_60_plan.md and paper 8.1ai.\n")

    # plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    zz = np.linspace(0.01, 2.6, 300)
    ax = axes[0, 0]
    ax.errorbar(z_hz, H, yerr=sig, fmt="o", ms=3, color="k", label="H(z)")
    ax.plot(zz, hz_osc(zz, l["H0"], l["Om"], 0.0, DELTA0_DERIVED, 0.0),
            "b-", lw=1.5, label="LCDM")
    ax.plot(zz, hz_osc(zz, fr["H0"], fr["Om"], fr["eps0"], fr["Delta"],
                       fr["beta"]), "r--", lw=1.5, label="free oscillatory")
    ax.set_xlabel("z"); ax.set_ylabel("H(z)"); ax.legend(fontsize=8)
    ax.set_title("A. H(z)")
    ax.grid(True, alpha=0.3)

    ax = axes[0, 1]
    ax.plot(dp["grid"], dp["dchi2"], "k-", lw=1.2, label="physical (eps0>=0)")
    ax.plot(dpn["grid"], dpn["dchi2"], "r--", lw=1.0, alpha=0.7,
            label="nosign (eps0 free)")
    ax.axvline(DELTA0_DERIVED, ls=":", lw=1, color="g", label="Delta=ln phi")
    ax.axvline(fr["Delta"], ls=":", lw=1, color="purple", label="best free Delta")
    ax.set_xlabel("Delta"); ax.set_ylabel("dchi2 vs LCDM")
    ax.set_title("B. Delta profile (joint)")
    ax.legend(fontsize=7); ax.grid(True, alpha=0.3)

    ax = axes[1, 0]
    ax.plot(bp["grid"], bp["dchi2"], "s-", lw=1.2, ms=3)
    ax.axvline(BETA0_DERIVED, ls=":", lw=1, color="g", label="beta=phi^3")
    ax.axvline(BETA_INV_PHI, ls=":", lw=1, color="orange", label="beta=1/phi")
    ax.set_xscale("log")
    ax.set_xlabel("beta"); ax.set_ylabel("dchi2 vs LCDM")
    ax.set_title("C. Beta profile (at free best)")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    ax = axes[1, 1]
    models = ["lcdm", "free", "free_nosign", "prereg_phi3", "prereg_invphi"]
    names = ["LCDM", "free (eps0>=0)", "free (eps0 sign free)", "prereg phi^3",
             "prereg 1/phi"]
    vals = [out[m]["dchi2"] for m in models]
    ax.barh(names, vals,
            color=["gray", "seagreen", "crimson", "steelblue", "orange"])
    ax.set_xlabel("dchi2 vs LCDM"); ax.set_title("D. Model comparison")
    ax.axvline(0, color="k", lw=0.8)
    ax.grid(True, alpha=0.3, axis="x")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "joint_fit_audit.png"), dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    out = run_audit()
    print("=" * 70)
    for name in ["lcdm", "free", "free_nosign", "prereg_phi3", "prereg_invphi"]:
        v = out[name]
        print(f"  {name:16s} chi2={v['chi2']:.1f} dchi2={v['dchi2']:+.1f} "
              f"H0={v['H0']:.1f} eps0={v.get('eps0', 0):.4f}")
    dp = out["delta_profile"]; dpn = out["delta_profile_nosign"]
    print(f"  H60c PHYSICAL:  best Delta={dp['best_Delta']:.3f} dchi2={dp['best_dchi2']:+.2f} "
          f"GLOBAL p={dp['p_global']:.4f}")
    print(f"  H60c NOSIGN:    best Delta={dpn['best_Delta']:.3f} dchi2={dpn['best_dchi2']:+.2f} "
          f"GLOBAL p={dpn['p_global']:.4f}")
    for label in ["hz", "sne"]:
        e = out["amplitude_bridge"][label]
        print(f"  H60d {label}: zbar={e['zbar']:.3f} eps_eff(phi^3)="
              f"{e['eps_eff_phi3']:.5f} fitted={e['eps_eff_fitted']:.5f}")
    print("=" * 70)
