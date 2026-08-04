"""
Phase 59: Time-Crystal Dark Energy â€” Pre-Registered, Look-Elsewhere-Accounted Test
==================================================================================
Audits the Plan 11 log-periodic dark-energy modulation (a *plan*, never a
phase) against the 60-point H(z) compilation under two corrections Plan 11
never applied:

  1. PRE-REGISTERED anchors, stated before fitting:
       epsilon0 = alpha/phi^2 = 0.0027873   (master-equation coupling)
       Delta0   = ln(phi)     = 0.4812      (golden self-similarity period:
                                             cos(2pi/Delta*ln(1+z)) invariant
                                             under (1+z) -> phi*(1+z)  <=>
                                             Delta = ln(phi)/n, n=1 fundamental)
       Delta1   = phi = 1.6180              (secondary: one cycle per phi e-folds)

  2. LOOK-ELSEWHERE accounting for the free-Delta scan (Phase-54 philosophy,
     frequency-band trial count): the fitted Delta = 1.54 from Plan 11 sits
     near 3*ln(phi) = 1.4436 AND pi/2 = 1.5708 â€” the multi-candidate situation
     that trial factors exist for.

Tracks:
  H59a  strict amplitude anchor  : eps = eps0 fixed, fit (H0, Om, Delta, phi0)
  H59b  golden period anchor     : Delta = Delta0 fixed, fit (H0, Om, eps, phi0)
  H59c  free-Delta scan          : Delta in [0.3, 5.0], fit (H0, Om, eps, phi0),
                                   global significance with trial count
  H59d  cycle coverage + forecast: why Delta was unconstrained; precision needed
                                   for a 3-sigma detection of eps0 and of 0.136

Reuses the H(z) loader and the flat-LambdaCDM / log-periodic models from
Plan 11 (code/oscillatory_dark_energy.py).

References:
  - Berti et al. 2026 "Stratoverso": log-periodic structure growth vs DESI DR1/DR2
  - Sornette log-periodicity / Fibonacci self-similarity (Delta = ln(phi))
  - Phase 54 (trial-factor audit) philosophy
"""

import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats

sys.path.insert(0, os.path.dirname(__file__))
from oscillatory_dark_energy import (
    hz_lcdm,
    hz_osc_log,
    load_hz_data,
)

PHI = (1 + np.sqrt(5)) / 2
ALPHA = 1 / 137.035999084
EPS0 = ALPHA / PHI**2
DELTA0 = np.log(PHI)
DELTA1 = PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase59")
os.makedirs(OUT_DIR, exist_ok=True)

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(_REPO, "data", "hz_cosmic_chronometers.csv")

# Scan grid (pre-registered, not data-driven)
SCAN_MIN = 0.3
SCAN_MAX = 5.0
SCAN_STEPS = 200


def pre_registered_anchors():
    """Return the pre-registered anchors with their derivations."""
    return {
        "epsilon0": EPS0,
        "epsilon0_rationale": "alpha/phi^2 associator coupling, master equation "
                              "(unified_mass_analysis.py); note: old Plan 11 note "
                              "quoted 0.00239 (~14% low) - flagged as doc discrepancy",
        "Delta0": DELTA0,
        "Delta0_rationale": "ln(phi): golden self-similarity period, invariant under "
                            "(1+z) -> phi*(1+z)",
        "Delta1": DELTA1,
        "Delta1_rationale": "phi: one cycle per phi e-folds (secondary anchor)",
        "alpha": ALPHA,
        "phi": PHI,
    }


def fit_lcdm(z, H, sigma):
    """Flat LCDM fit; returns (chi2, popt, perr)."""
    popt, pcov = curve_fit(
        hz_lcdm, z, H, sigma=sigma, p0=[70.0, 0.3],
        bounds=([50, 0.1], [85, 0.5]), maxfev=10000,
    )
    pred = hz_lcdm(z, *popt)
    chi2 = np.sum(((H - pred) / sigma) ** 2)
    return chi2, popt, np.sqrt(np.diag(pcov))


def _fit_osc_fixed(z, H, sigma, fixed, fixed_val, p0):
    """Fit hz_osc_log with one parameter frozen.

    fixed: 'eps' or 'Delta'; fixed_val: the frozen value.
    Returns (chi2, popt_full, perr_full) where popt_full has the frozen
    parameter in its canonical slot [H0, Om, eps, Delta, phi0].
    """
    model = hz_osc_log

    def wrapper(x, H0, Om, other, phi0):
        params = [H0, Om, 0.0, 0.0, phi0]
        if fixed == "eps":
            params[2] = fixed_val
            params[3] = other
        else:
            params[3] = fixed_val
            params[2] = other
        return model(x, *params)

    p0_wrap = [p0[0], p0[1], p0[3] if fixed == "eps" else p0[2], p0[4]]
    lower = [50, 0.1, SCAN_MIN if fixed == "eps" else 0.0]
    upper = [85, 0.5, SCAN_MAX if fixed == "eps" else 0.3]
    lower.append(-np.pi)
    upper.append(np.pi)
    popt_w, pcov_w = curve_fit(
        wrapper, z, H, sigma=sigma, p0=p0_wrap,
        bounds=(lower, upper), maxfev=20000,
    )
    H0, Om, other, phi0 = popt_w
    full = [H0, Om, 0.0, 0.0, phi0]
    if fixed == "eps":
        full[2] = fixed_val
        full[3] = other
    else:
        full[3] = fixed_val
        full[2] = other
    chi2 = np.sum(((H - model(z, *full)) / sigma) ** 2)
    perr = [0.0] * 5
    perr_w = np.sqrt(np.diag(pcov_w))
    perr[0], perr[1], perr[4] = perr_w[0], perr_w[1], perr_w[3]
    perr[3 if fixed == "eps" else 2] = perr_w[2]
    return chi2, np.array(full), np.array(perr)


def h59a_strict_amplitude(z, H, sigma, lcdm_chi2):
    """Fix eps = eps0 (master-equation amplitude); fit H0, Om, Delta, phi0."""
    chi2, popt, perr = _fit_osc_fixed(
        z, H, sigma, "eps", EPS0, [70.0, 0.3, 0.1, 1.5, 0.0])
    return {
        "chi2": chi2,
        "delta_chi2_vs_lcdm": lcdm_chi2 - chi2,
        "popt": popt,
        "perr": perr,
        "eps_fixed": EPS0,
    }


def h59b_golden_period(z, H, sigma, lcdm_chi2):
    """Fix Delta = Delta0 = ln(phi); fit H0, Om, eps, phi0."""
    chi2, popt, perr = _fit_osc_fixed(
        z, H, sigma, "Delta", DELTA0, [70.0, 0.3, 0.1, 1.5, 0.0])
    return {
        "chi2": chi2,
        "delta_chi2_vs_lcdm": lcdm_chi2 - chi2,
        "popt": popt,
        "perr": perr,
        "Delta_fixed": DELTA0,
    }


def scan_delta(z, H, sigma, lcdm_chi2):
    """Scan Delta over the pre-registered grid; fit (H0, Om, eps, phi0) each.

    Returns dict with grid, dchi2 array, best index, best Delta, and the
    local p-value of the best (2 extra dof: eps, phi0; Delta frozen per point).
    """
    grid = np.linspace(SCAN_MIN, SCAN_MAX, SCAN_STEPS)
    dchi2 = np.empty_like(grid)
    popt_best = None
    best_i = 0
    for i, Delta in enumerate(grid):
        chi2, popt, _ = _fit_osc_fixed(z, H, sigma, "Delta", Delta,
                                       [70.0, 0.3, 0.1, 1.5, 0.0])
        dchi2[i] = lcdm_chi2 - chi2
        if dchi2[i] > dchi2[best_i]:
            best_i = i
            popt_best = popt
    p_local = stats.chi2.sf(dchi2[best_i], df=2)
    return {
        "grid": grid,
        "dchi2": dchi2,
        "best_index": int(best_i),
        "best_Delta": float(grid[best_i]),
        "best_dchi2": float(dchi2[best_i]),
        "p_local": float(p_local),
        "popt_best": popt_best,
    }


def effective_trials(delta_grid, ln1pz_max):
    """Independent frequency-band trials over the log-redshift window.

    Frequencies f = 1/Delta; a window of length L in ln(1+z) resolves
    frequency bands of width ~1/L. N_ind = (f_max - f_min) * L.
    """
    f_max = 1.0 / delta_grid.min()
    f_min = 1.0 / delta_grid.max()
    n = max(1, int(round((f_max - f_min) * ln1pz_max)))
    return n


def global_significance(p_local, trials):
    """Sidak-corrected global p for `trials` independent local trials."""
    return 1.0 - (1.0 - p_local) ** trials


def cycle_coverage(ln1pz_max, delta):
    """Number of oscillation cycles spanned by the data at period Delta."""
    return ln1pz_max / delta


def forecast_precision(z, H, sigma, eps_target, delta_target, target_dchi2=9.0):
    """Precision factor needed for a ~3-sigma detection.

    Fits the fixed-(eps_target, Delta_target) model vs LCDM and returns the
    factor by which all sigma must be scaled down (sigma/f) so that
    delta_chi2 = target_dchi2.  delta_chi2 scales as 1/sigma^2.
    """
    model = hz_osc_log

    def wrapper(x, H0, Om, phi0):
        return model(x, H0, Om, eps_target, delta_target, phi0)

    popt_w, _ = curve_fit(
        wrapper, z, H, sigma=sigma, p0=[70.0, 0.3, 0.0],
        bounds=([50, 0.1, -np.pi], [85, 0.5, np.pi]), maxfev=20000,
    )
    chi2_target = np.sum(
        ((H - model(z, popt_w[0], popt_w[1], eps_target, delta_target,
                    popt_w[2])) / sigma) ** 2)
    lcdm_chi2, _, _ = fit_lcdm(z, H, sigma)
    dchi2_now = lcdm_chi2 - chi2_target
    if dchi2_now <= 0:
        return float("inf")
    return float(np.sqrt(target_dchi2 / dchi2_now))


def run_full():
    z, H, sigma = load_hz_data(DATA_PATH)
    ln1pz_max = np.log(1 + z.max())
    lcdm_chi2, lcdm_popt, _ = fit_lcdm(z, H, sigma)

    a = pre_registered_anchors()
    r59a = h59a_strict_amplitude(z, H, sigma, lcdm_chi2)
    r59b = h59b_golden_period(z, H, sigma, lcdm_chi2)
    r59c = scan_delta(z, H, sigma, lcdm_chi2)
    trials = effective_trials(r59c["grid"], ln1pz_max)
    p_global = global_significance(r59c["p_local"], trials)

    cycles_0 = cycle_coverage(ln1pz_max, a["Delta0"])
    cycles_fit = cycle_coverage(ln1pz_max, r59c["best_Delta"])

    f_eps0 = forecast_precision(z, H, sigma, a["epsilon0"], a["Delta0"])
    f_0136 = forecast_precision(z, H, sigma, 0.136, a["Delta0"])
    f_0136_fit = forecast_precision(z, H, sigma, 0.136, r59c["best_Delta"])

    summary = {
        "n_data": int(len(z)),
        "zmax": float(z.max()),
        "ln1pz_max": float(ln1pz_max),
        "lcdm_chi2": float(lcdm_chi2),
        "lcdm_H0": float(lcdm_popt[0]),
        "lcdm_Om": float(lcdm_popt[1]),
        "epsilon0": float(a["epsilon0"]),
        "Delta0": float(a["Delta0"]),
        "Delta1": float(a["Delta1"]),
        "h59a_chi2": float(r59a["chi2"]),
        "h59a_dchi2": float(r59a["delta_chi2_vs_lcdm"]),
        "h59b_chi2": float(r59b["chi2"]),
        "h59b_dchi2": float(r59b["delta_chi2_vs_lcdm"]),
        "h59b_eps_best": float(r59b["popt"][2]),
        "h59b_eps_err": float(r59b["perr"][2]),
        "h59c_best_Delta": float(r59c["best_Delta"]),
        "h59c_best_dchi2": float(r59c["best_dchi2"]),
        "h59c_p_local": float(r59c["p_local"]),
        "h59c_trials": int(trials),
        "h59c_p_global": float(p_global),
        "cycles_golden": float(cycles_0),
        "cycles_best": float(cycles_fit),
        "3lnphi": float(3 * np.log(PHI)),
        "pi_over_2": float(np.pi / 2),
        "f_eps0_detection": float(f_eps0),
        "f_0136_detection": float(f_0136),
        "f_0136_bestDelta_detection": float(f_0136_fit),
    }

    write_outputs(z, H, sigma, r59a, r59b, r59c, summary)
    return summary


def write_outputs(z, H, sigma, r59a, r59b, r59c, s):
    # delta scan csv
    scan_path = os.path.join(OUT_DIR, "delta_scan.csv")
    with open(scan_path, "w", encoding="utf-8") as f:
        f.write("Delta,dchi2_vs_lcdm\n")
        for d, c in zip(r59c["grid"], r59c["dchi2"]):
            f.write(f"{d:.6f},{c:.6f}\n")

    # anchors and fits csv
    fits_path = os.path.join(OUT_DIR, "anchors_and_fits.csv")
    with open(fits_path, "w", encoding="utf-8") as f:
        f.write("quantity,value\n")
        rows = [
            ("epsilon0_alpha_phi2", s["epsilon0"]),
            ("Delta0_ln_phi", s["Delta0"]),
            ("Delta1_phi", s["Delta1"]),
            ("lcdm_chi2", s["lcdm_chi2"]),
            ("lcdm_H0", s["lcdm_H0"]),
            ("lcdm_Om", s["lcdm_Om"]),
            ("h59a_chi2_eps_fixed", s["h59a_chi2"]),
            ("h59a_dchi2_vs_lcdm", s["h59a_dchi2"]),
            ("h59b_chi2_Delta_golden", s["h59b_chi2"]),
            ("h59b_dchi2_vs_lcdm", s["h59b_dchi2"]),
            ("h59b_eps_best", s["h59b_eps_best"]),
            ("h59b_eps_err", s["h59b_eps_err"]),
            ("h59c_best_Delta", s["h59c_best_Delta"]),
            ("h59c_best_dchi2", s["h59c_best_dchi2"]),
            ("h59c_p_local", s["h59c_p_local"]),
            ("h59c_trials", s["h59c_trials"]),
            ("h59c_p_global", s["h59c_p_global"]),
            ("cycles_golden", s["cycles_golden"]),
            ("cycles_best", s["cycles_best"]),
            ("3lnphi", s["3lnphi"]),
            ("pi_over_2", s["pi_over_2"]),
            ("f_eps0_detection", s["f_eps0_detection"]),
            ("f_0136_detection", s["f_0136_detection"]),
            ("f_0136_bestDelta_detection", s["f_0136_bestDelta_detection"]),
        ]
        for k, v in rows:
            f.write(f"{k},{v:.6g}\n")

    # summary text
    txt = os.path.join(OUT_DIR, "lookelsewhere_summary.txt")
    with open(txt, "w", encoding="utf-8") as f:
        w = f.write
        w("=" * 70 + "\n")
        w("PHASE 59 - PRE-REGISTERED, LOOK-ELSEWHERE-ACCOUNTED TEST\n")
        w("Time-crystal dark energy (Plan 11 audit)\n")
        w("=" * 70 + "\n\n")
        w(f"Data: {s['n_data']} H(z) points, zmax = {s['zmax']}, "
          f"ln(1+zmax) = {s['ln1pz_max']:.4f}\n\n")
        w(f"LCDM baseline: chi2 = {s['lcdm_chi2']:.2f}, "
          f"H0 = {s['lcdm_H0']:.2f}, Om = {s['lcdm_Om']:.3f}\n\n")
        w("PRE-REGISTERED ANCHORS (before fitting)\n")
        w("-" * 70 + "\n")
        w(f"  eps0 = alpha/phi^2  = {s['epsilon0']:.7f}  "
          f"(master-equation coupling)\n")
        w(f"  Delta0 = ln(phi)    = {s['Delta0']:.6f}  "
          f"(golden self-similarity period)\n")
        w(f"  Delta1 = phi        = {s['Delta1']:.6f}  "
          f"(secondary anchor)\n\n")
        w("H59a - STRICT AMPLITUDE ANCHOR (eps = eps0 fixed)\n")
        w("-" * 70 + "\n")
        w(f"  chi2 = {s['h59a_chi2']:.2f}, "
          f"Delta_chi2 vs LCDM = {s['h59a_dchi2']:+.3f}\n\n")
        w("H59b - GOLDEN PERIOD ANCHOR (Delta = ln phi fixed)\n")
        w("-" * 70 + "\n")
        w(f"  chi2 = {s['h59b_chi2']:.2f}, "
          f"Delta_chi2 vs LCDM = {s['h59b_dchi2']:+.3f}\n")
        w(f"  fitted eps at golden period = {s['h59b_eps_best']:.4f} "
          f"+- {s['h59b_eps_err']:.4f}\n")
        w(f"  cycles spanned by data at Delta0: {s['cycles_golden']:.2f}\n\n")
        w("H59c - FREE-DELTA SCAN WITH LOOK-ELSEWHERE ACCOUNTING\n")
        w("-" * 70 + "\n")
        w(f"  best Delta = {s['h59c_best_Delta']:.4f}, "
          f"Delta_chi2 = {s['h59c_best_dchi2']:.3f}\n")
        w(f"  local p (2 dof) = {s['h59c_p_local']:.4f}, "
          f"trials = {s['h59c_trials']}, "
          f"GLOBAL p = {s['h59c_p_global']:.4f}\n")
        w(f"  cycles spanned by data at best Delta: {s['cycles_best']:.2f}\n")
        w(f"  best Delta vs candidates: 3*ln(phi) = {s['3lnphi']:.4f}, "
          f"pi/2 = {s['pi_over_2']:.4f}\n\n")
        w("H59d - CYCLE COVERAGE + DETECTION FORECAST\n")
        w("-" * 70 + "\n")
        w(f"  precision factor needed for 3-sigma detection (dchi2=9):\n")
        w(f"    of eps0=alpha/phi^2 at Delta0      : {s['f_eps0_detection']:.1f}x "
          f"smaller errors\n")
        w(f"    of eps=0.136 at Delta0             : {s['f_0136_detection']:.1f}x\n")
        w(f"    of eps=0.136 at best Delta         : {s['f_0136_bestDelta_detection']:.1f}x\n\n")
        w("VERDICT\n")
        w("-" * 70 + "\n")
        w("Interpretation is drawn from the numbers above and stated in\n")
        w("notes/IST_Phase_59_plan.md and main/synthesis_paper.md 8.1ah.\n")

    # plot
    z_s = np.linspace(0, z.max() * 1.02, 300)
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(9, 9), gridspec_kw={"height_ratios": [3, 1]})
    ax1.errorbar(z, H, yerr=sigma, fmt="o", ms=3, color="black",
                 capsize=2, label="H(z) chronometers")
    lcdm_chi2, lcdm_popt, _ = fit_lcdm(z, H, sigma)
    ax1.plot(z_s, hz_lcdm(z_s, *lcdm_popt), "b-", lw=2,
             label=f"LCDM (H0={lcdm_popt[0]:.1f}, Om={lcdm_popt[1]:.3f})")
    if r59b["popt"] is not None:
        ax1.plot(z_s, hz_osc_log(z_s, *r59b["popt"]), "r--", lw=2,
                 label=f"golden period Delta=ln phi (eps={r59b['popt'][2]:.4f})")
    if r59c["popt_best"] is not None:
        ax1.plot(z_s, hz_osc_log(z_s, *r59c["popt_best"]), "g:", lw=1.5,
                 label=f"best free Delta={r59c['best_Delta']:.2f}")
    ax1.set_ylabel("H(z) [km/s/Mpc]")
    ax1.set_xlabel("z")
    ax1.set_title("Phase 59: Pre-registered, look-elsewhere-accounted test of "
                  "time-crystal dark energy")
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax2.plot(r59c["grid"], r59c["dchi2"], "k-", lw=1)
    ax2.axhline(0, color="gray", ls="--", lw=0.5)
    for cand, lab in [(DELTA0, "ln(phi)"), (3 * np.log(PHI), "3ln(phi)"),
                      (np.pi / 2, "pi/2")]:
        ax2.axvline(cand, ls=":", lw=1, alpha=0.6, label=lab)
    ax2.set_xlabel("Delta (log-periodic period in ln(1+z))")
    ax2.set_ylabel("Delta_chi2 vs LCDM")
    ax2.set_title(f"H59c free-Delta scan (global p = {s['h59c_p_global']:.4f})")
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "delta_scan.png"), dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    s = run_full()
    print("=" * 70)
    for k, v in s.items():
        print(f"  {k} = {v:.6g}" if isinstance(v, float) else f"  {k} = {v}")
    print("=" * 70)
    print(f"  outputs -> {OUT_DIR}")
