
"""
================================================================================
IST PHASE 5 - Observational Validation & Falsification Pipeline
================================================================================
Purpose:
    End-to-end observational tests of the IST predictions developed in
    Plans 6-12 and Phases 1-4, with a falsification summary:

    5.1 Void lensing templates with the Phase 4 derived G(rho):
        tangential shear profiles of a stacked top-hat void for constant G,
        D = 2, D = phi, and the Phase 4 measured window slope (0.600),
        under two mappings from G(rho) to the lensing signal, with
        distinguishability at COSMOS-Web/Euclid depth.

    5.2 CMB antipodal (Klein parity flip) re-analysis:
        implements apply_klein_parity_flip() and the antipodal correlation
        statistic, builds the LambdaCDM Monte Carlo null distribution from
        synthetic Planck-like skies, and tests recovery of an injected
        C = 0.005 signal under multiple galactic masks. (No Planck maps are
        stored locally; this pipeline is validated on synthetic skies and
        is ready to be pointed at real maps.)

    5.3 GW time-crystal modulation:
        per GWTC-3 event, computes the detectability of the Plan 10/12
        ringdown modulation at f_tc = f_rd/(2 phi) with amplitude
        eps = alpha/phi^2, verified by synthetic injection/recovery, and
        the NANOGrav SGWB extra-component ratio A_extra/A_obs.

Inputs:   none (GW catalog from code/data_fetch/fetch_ligo.py)
Outputs:
    code/outputs/phase5/lensing_shear.csv
    code/outputs/phase5/cmb_antipodal_summary.csv
    code/outputs/phase5/gw_modulation.csv
    code/outputs/phase5/lensing_templates.png
    code/outputs/phase5/cmb_null.png
    code/outputs/phase5/gw_modulation.png
    code/outputs/phase5/falsification_summary.pdf

References:
    notes/IST_Research_Plan_Phases_1-5.md   (Phase 5)
    main/ist_v5_3_topology_substrate.md     (sec. 3.5 G scaling, CMB parity)
    code/phase4_variable_g.py               (measured G_eff(rho) exponents)
    code/data_fetch/fetch_ligo.py           (GWTC-3 + NANOGrav + IST preds)
    analysis/empirical_assessment_ist_v3_0.md (C ~ 0.005 claim, void pred)

Conventions:
    * Lensing model A (local Poisson): kappa sourced by the G-weighted
      density contrast, DeltaSigma_G = 2 sqrt(R_v^2 - xi^2) rho_bar
      [(1+delta)^{1+1/D} - 1]. Model B (interior-G suppression, the IST
      phenomenology narrative): the GR signal is uniformly scaled by
      (1+delta)^{1/D}. Both are reported; the sign of the deviation from
      GR differs, which is flagged as an open modeling question.
    * CMB skies: Gaussian realizations on an equiangular (theta, phi) grid
      from a low-ell anchor-point interpolation of the Planck 2018 TT
      spectrum (ell <= 60; the antipodal statistic is large-scale).
    * Klein parity flip: (theta, phi) -> (pi - theta, pi - phi)
      (orientation-reversing antipodal identification). Plain antipodal
      (theta, phi) -> (pi - theta, phi + pi) is run as a control.
    * GW significance: eps_hat = <d, g>/<g, g> with g = dh/deps|_0;
      white noise normalized so the ringdown SNR equals the catalog SNR.
================================================================================
"""

import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from scipy.special import gammaln, lpmv

from ist_toolkit_v2 import PHI, ALPHA

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "data_fetch"))
from fetch_ligo import (
    get_gwtc3_events, get_nanograv_sgwb, compute_ist_gw_predictions
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase5")

# ───────────────────────────────────────────────────────────────────────────────
# SHARED COSMOLOGY
# ───────────────────────────────────────────────────────────────────────────────

H0_KM_S_MPC = 70.0
OMEGA_M = 0.3
OMEGA_L = 0.7
C_KM_S = 299792.458
G_SI = 6.67430e-11
MPC_M = 3.0857e22
M_SUN_KG = 1.989e30

PHASE4_WINDOW_SLOPE = 0.600   # measured d log G / d log rho, Phase 4 scan


def e_z(z):
    return np.sqrt(OMEGA_M * (1 + z) ** 3 + OMEGA_L)


def comoving_distance(z, n_steps=2048):
    """Line-of-sight comoving distance chi(z) in Mpc (flat LambdaCDM)."""
    zs = np.linspace(0, z, n_steps)
    return (C_KM_S / H0_KM_S_MPC) * np.trapezoid(1.0 / e_z(zs), zs)


def angular_diameter(z_l, z_s=None):
    """Angular diameter distance to z_l, or between z_l and z_s, in Mpc."""
    if z_s is None:
        return comoving_distance(z_l) / (1 + z_l)
    return (comoving_distance(z_s) - comoving_distance(z_l)) / (1 + z_s)


def sigma_crit(z_l, z_s):
    """Critical surface density in M_sun / Mpc^2."""
    d_l = angular_diameter(z_l) * MPC_M
    d_s = angular_diameter(z_s) * MPC_M
    d_ls = angular_diameter(z_l, z_s) * MPC_M
    kg_per_m2 = (C_KM_S * 1e3) ** 2 / (4 * np.pi * G_SI) * d_s / (d_l * d_ls)
    return kg_per_m2 * MPC_M ** 2 / M_SUN_KG


def rho_bar_msun_mpc3():
    """Mean matter density of the universe in M_sun / Mpc^3."""
    h0_s = H0_KM_S_MPC * 1e3 / MPC_M
    rho_crit = 3 * h0_s ** 2 / (8 * np.pi * G_SI)      # kg / m^3
    return rho_crit * MPC_M ** 3 / M_SUN_KG * OMEGA_M


# ───────────────────────────────────────────────────────────────────────────────
# 5.1 VOID LENSING TEMPLATES
# ───────────────────────────────────────────────────────────────────────────────

def g_weight_factor(rho_ratio, D):
    """G_eff/G_N = rho_ratio^{1/D}; D=None gives constant G."""
    if D is None:
        return np.ones_like(np.atleast_1d(rho_ratio))
    return np.atleast_1d(rho_ratio) ** (1.0 / D)


def void_contrast_model_a(delta, D):
    """Model A (local Poisson): G-weighted density contrast, in units rho_bar.

    (1+delta)^{1+1/D} - 1 ; reduces to delta for constant G.
    """
    if D is None:
        return delta
    return (1 + delta) ** (1 + 1.0 / D) - 1.0


def void_contrast_model_b(delta, D):
    """Model B (interior-G suppression): GR contrast scaled by (1+delta)^{1/D}."""
    if D is None:
        return delta
    return delta * (1 + delta) ** (1.0 / D)


def void_shear(theta_arcmin, z_l, z_s, R_v, delta, D, model="A"):
    """Tangential shear profile of a stacked top-hat void.

    DeltaSigma(xi) = 2 sqrt(R_v^2 - xi^2) * rho_bar * contrast for xi < R_v.
    kappa(theta) = DeltaSigma(D_l theta) / Sigma_crit,
    gamma_t(theta) = kappa_bar(<theta) - kappa(theta).
    """
    d_l = angular_diameter(z_l)
    sc = sigma_crit(z_l, z_s)
    rho_bar = rho_bar_msun_mpc3()
    contrast = (void_contrast_model_a if model == "A"
                else void_contrast_model_b)(delta, D)

    xi = d_l * np.deg2rad(theta_arcmin / 60.0)          # Mpc
    inside = xi < R_v
    dsigma = np.zeros_like(xi)
    dsigma[inside] = (2 * np.sqrt(R_v ** 2 - xi[inside] ** 2)
                      * rho_bar * contrast)
    kappa = dsigma / sc

    # mean kappa inside theta via trapezoid on the theta grid
    kappa_bar = np.zeros_like(kappa)
    for i in range(1, len(theta_arcmin)):
        area = np.trapezoid(kappa[:i + 1] * xi[:i + 1], xi[:i + 1])
        kappa_bar[i] = 2 * area / xi[i] ** 2
    kappa_bar[0] = kappa[0]
    return kappa_bar - kappa


def shear_noise(theta_arcmin, n_gal=35.0, sigma_e=0.30, n_voids=100,
                dtheta_arcmin=None):
    """Per-bin tangential-shear noise for n_voids stacked voids.

    sigma_gamma = sigma_e / sqrt(2 * n_gal * A_bin * n_voids).
    """
    if dtheta_arcmin is None:
        dtheta_arcmin = np.gradient(theta_arcmin)
    area = 2 * np.pi * theta_arcmin * np.abs(dtheta_arcmin)   # arcmin^2
    return sigma_e / np.sqrt(2 * n_gal * area * n_voids)


def chi2_between(profile_a, profile_b, noise):
    return np.sum((profile_a - profile_b) ** 2 / noise ** 2)


# ───────────────────────────────────────────────────────────────────────────────
# 5.2 CMB KLEIN PARITY FLIP
# ───────────────────────────────────────────────────────────────────────────────

# Planck 2018-ish low-ell TT anchors: D_ell = ell(ell+1) C_ell / (2 pi) [uK^2]
CL_ANCHORS = {
    2: 1000.0, 3: 950.0, 5: 880.0, 8: 820.0, 12: 850.0,
    20: 1050.0, 30: 1250.0, 45: 1650.0, 60: 2100.0,
}


def cl_low_ell(ell):
    """Log-log interpolation of the anchor TT spectrum; returns C_ell [uK^2]."""
    ell = np.atleast_1d(np.asarray(ell, dtype=float))
    e0 = np.array(sorted(CL_ANCHORS))
    d0 = np.array([CL_ANCHORS[int(e)] for e in e0])
    log_d = np.interp(np.log(ell), np.log(e0), np.log(d0))
    d_ell = np.exp(log_d)
    return d_ell * 2 * np.pi / (ell * (ell + 1))


def make_grid(n_theta, n_phi):
    """Cell-centered equiangular grid avoiding the poles."""
    theta = np.pi * (np.arange(n_theta) + 0.5) / n_theta
    phi = 2 * np.pi * np.arange(n_phi) / n_phi
    return theta, phi


def precompute_ylm(theta, l_max):
    """Normalized Legendre factors N_ellm * P_ellm(cos theta) for m >= 0.

    Returns a list per ell of (m_values, array shape (l+1, n_theta)).
    """
    cost = np.cos(theta)
    per_ell = []
    for l in range(l_max + 1):
        ms = np.arange(l + 1)
        P = np.array([lpmv(m, l, cost) for m in ms])
        norm = np.sqrt((2 * l + 1) / (4 * np.pi)
                       * np.exp(gammaln(l - ms + 1) - gammaln(l + ms + 1)))
        per_ell.append((ms, norm[:, None] * P))
    return per_ell


def synthesize_sky(per_ell, phi, cls_uK, rng):
    """Gaussian LambdaCDM sky T(theta, phi) from precomputed Y_lm factors."""
    n_theta = len(per_ell[0][1][0])
    n_phi = len(phi)
    T = np.zeros((n_theta, n_phi))
    for l, (ms, nP) in enumerate(per_ell):
        if l < 2 or cls_uK[l] <= 0:
            continue
        a0 = np.sqrt(cls_uK[l]) * rng.normal()
        T += a0 * nP[0][:, None]
        for m in ms[1:]:
            a = np.sqrt(cls_uK[l] / 2) * (rng.normal() + 1j * rng.normal())
            T += 2 * np.real(a * nP[m][:, None] * np.exp(1j * m * phi)[None, :])
    return T


def apply_klein_parity_flip(T, mirror=True):
    """Klein-transformed sky: (theta, phi) -> (pi - theta, pi - phi).

    flipud maps theta -> pi - theta (exact on the cell-centered grid);
    the phi index maps k -> n_phi/2 - k (mirror=True, orientation
    reversing) or k -> n_phi/2 + k (mirror=False, plain antipodal).
    """
    n_phi = T.shape[1]
    k = np.arange(n_phi)
    shift = (n_phi // 2 - k) % n_phi if mirror else (k + n_phi // 2) % n_phi
    return np.flipud(T)[:, shift]


def galactic_mask(theta, b_min_deg):
    """Keep pixels with |b| >= b_min (treating theta as galactic colatitude)."""
    b = 90.0 - np.rad2deg(theta)
    return (np.abs(b) >= b_min_deg).astype(float)


def antipodal_correlation(T, mask, mirror=True):
    """C = <T . KT>_w / <T^2>_w over the masked sky."""
    w = mask[:, None]
    num = np.sum(w * T * apply_klein_parity_flip(T, mirror=mirror))
    den = np.sum(w * T ** 2)
    return num / den


def null_distribution(per_ell, phi, cls_uK, masks, n_mc, rng, mirror=True,
                      inject_c=None):
    """Monte Carlo of the antipodal statistic under LambdaCDM.

    Returns per mask: the null values C(T), and — when inject_c is given —
    the paired injected values C((T + c KT)/sqrt(1+c^2)) computed on the
    same skies, so the recovery shift is measured without doubling the
    cosmic variance.
    """
    out = {name: {"null": np.empty(n_mc), "inj": np.empty(n_mc)}
           for name in masks}
    for i in range(n_mc):
        T = synthesize_sky(per_ell, phi, cls_uK, rng)
        Ti = inject_correlated(T, inject_c, mirror=mirror) \
            if inject_c is not None else None
        for name, mask in masks.items():
            out[name]["null"][i] = antipodal_correlation(T, mask, mirror=mirror)
            if Ti is not None:
                out[name]["inj"][i] = antipodal_correlation(Ti, mask,
                                                            mirror=mirror)
    return out


def inject_correlated(T, c, mirror=True):
    """Sky with an enforced Klein-correlated component: (T + c KT)/sqrt(1+c^2)."""
    return (T + c * apply_klein_parity_flip(T, mirror=mirror)) / np.sqrt(1 + c ** 2)


# ───────────────────────────────────────────────────────────────────────────────
# 5.3 GW TIME-CRYSTAL MODULATION
# ───────────────────────────────────────────────────────────────────────────────

Q_FACTOR = 10.0           # ringdown quality factor (l = m = 2)
DT = 1.0 / 16384.0        # LIGO sample interval
EPS_TC = ALPHA / PHI ** 2  # IST modulation amplitude ~ 2.78e-3


def ringdown_waveform(t, f_rd, epsilon=0.0, f_tc=None):
    """Damped sinusoid with optional multiplicative time-crystal modulation.

    tau_d = Q / (pi f_rd); h = A e^{-t/tau} sin(2 pi f_rd t)
                                (1 + eps sin(2 pi f_tc t)).
    """
    tau = Q_FACTOR / (np.pi * f_rd)
    h = np.exp(-t / tau) * np.sin(2 * np.pi * f_rd * t)
    if epsilon:
        h = h * (1 + epsilon * np.sin(2 * np.pi * f_tc * t))
    return h


def modulation_template(t, f_rd, f_tc):
    """g = dh/deps|_0 = h_0(t) sin(2 pi f_tc t)."""
    tau = Q_FACTOR / (np.pi * f_rd)
    return (np.exp(-t / tau) * np.sin(2 * np.pi * f_rd * t)
            * np.sin(2 * np.pi * f_tc * t))


def fit_modulation(d, h, g, sigma_n):
    """Two-template matched filter: fit d = a*h + eps*g + noise.

    Solves the 2x2 normal equations exactly, so non-orthogonality of h and
    g (leakage of the unmodulated ringdown into the modulation template)
    does not bias eps. Returns (eps_hat, sigma_eps).
    """
    mhh, mhg, mgg = np.sum(h * h), np.sum(h * g), np.sum(g * g)
    det = mhh * mgg - mhg ** 2
    b_h, b_g = np.sum(d * h), np.sum(d * g)
    eps_hat = (mhh * b_g - mhg * b_h) / det
    sigma_eps = sigma_n * np.sqrt(mhh / det)
    return eps_hat, sigma_eps


def sigma_epsilon(f_rd, f_tc, snr, duration_factor=8.0):
    """White-noise uncertainty on the modulation amplitude.

    sigma_n is fixed by requiring the ringdown SNR to equal the catalog
    value: sum h^2 / sigma_n^2 = snr^2. The 2x2 matched filter accounts
    for h/g non-orthogonality.
    """
    tau = Q_FACTOR / (np.pi * f_rd)
    t = np.arange(0, duration_factor * tau, DT)
    h = ringdown_waveform(t, f_rd)
    g = modulation_template(t, f_rd, f_tc)
    sigma_n = np.sqrt(np.sum(h ** 2)) / snr
    return fit_modulation(np.zeros_like(h), h, g, sigma_n)[1]


def simulate_epsilon_recovery(f_rd, f_tc, snr, epsilon, rng, n_trials=200):
    """Inject epsilon into noisy ringdowns and recover via the 2x2 fit."""
    tau = Q_FACTOR / (np.pi * f_rd)
    t = np.arange(0, 8 * tau, DT)
    h = ringdown_waveform(t, f_rd)
    g = modulation_template(t, f_rd, f_tc)
    sigma_n = np.sqrt(np.sum(h ** 2)) / snr
    sig_eps = sigma_epsilon(f_rd, f_tc, snr)
    est = np.empty(n_trials)
    for i in range(n_trials):
        d = h * (1 + epsilon * np.sin(2 * np.pi * f_tc * t)) \
            + sigma_n * rng.normal(size=len(t))
        est[i] = fit_modulation(d, h, g, sigma_n)[0]
    return est, sig_eps


def nanograv_extra_component():
    """IST SGWB extra component: amplitude ratio alpha/phi^2, and the
    cross-power ratio (alpha/phi^2)^2 that PTA sensitivity must reach."""
    amp = ALPHA / PHI ** 2
    return {"amplitude_ratio": amp, "power_ratio": amp ** 2,
            "required_sensitivity_factor": 1.0 / amp ** 2}


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER
# ───────────────────────────────────────────────────────────────────────────────

def run_lensing():
    """5.1: void shear templates + COSMOS-Web/Euclid distinguishability."""
    z_l, z_s, R_v, delta = 0.8, 2.0, 30.0, -0.8
    theta_v_arcmin = np.rad2deg(R_v / angular_diameter(z_l)) * 60
    theta = np.linspace(theta_v_arcmin * 0.08, theta_v_arcmin * 2.0, 14)
    noise = shear_noise(theta, n_voids=100)

    models = {
        "constant G (GR)": None,
        "D = 2 (Phase 1.3)": 2.0,
        "D = phi (IST)": PHI,
        "D = 1/0.600 (Phase 4)": 1.0 / PHASE4_WINDOW_SLOPE,
    }
    rows, profiles = [], {}
    for model in ["A", "B"]:
        for name, D in models.items():
            g = void_shear(theta, z_l, z_s, R_v, delta, D, model=model)
            profiles[(model, name)] = g
            for th, gg, nn in zip(theta, g, noise):
                rows.append({"model": model, "template": name,
                             "theta_arcmin": th, "gamma_t": gg, "noise": nn})

    summary = []
    for model in ["A", "B"]:
        ref = profiles[(model, "constant G (GR)")]
        for name, D in list(models.items())[1:]:
            chi2 = chi2_between(profiles[(model, name)], ref, noise)
            summary.append({"model": model, "comparison": f"{name} vs GR",
                            "delta_chi2": chi2,
                            "significance_sigma": np.sqrt(chi2)})
    for name in list(models.keys())[1:]:
        chi2 = chi2_between(profiles[("A", name)], profiles[("B", name)], noise)
        summary.append({"model": "A vs B", "comparison": name,
                        "delta_chi2": chi2,
                        "significance_sigma": np.sqrt(chi2)})

    print("5.1 Void lensing (z_l = 0.8, z_s = 2.0, R_v = 30 Mpc, delta = -0.8):")
    print(f"  void angular radius = {theta_v_arcmin:.1f} arcmin; "
          f"100 stacked voids, n_gal = 35/arcmin^2")
    for s in summary:
        print(f"  model {s['model']:5s} {s['comparison']:28s} "
              f"dChi2 = {s['delta_chi2']:9.1f} ({s['significance_sigma']:.1f} sigma)")
    return theta, noise, profiles, summary, rows


def run_cmb(n_mc=200, l_max=60, n_theta=64, n_phi=128, seed=1234):
    """5.2: Klein parity flip null tests + injection recovery."""
    theta, phi = make_grid(n_theta, n_phi)
    per_ell = precompute_ylm(theta, l_max)
    cls_uK = np.zeros(l_max + 1)
    cls_uK[2:] = cl_low_ell(np.arange(2, l_max + 1))
    masks = {f"|b|>{b}": galactic_mask(theta, b) for b in (20, 30, 40)}
    rng = np.random.default_rng(seed)

    print(f"5.2 CMB antipodal statistic (l_max = {l_max}, "
          f"grid {n_theta}x{n_phi}, {n_mc} MC skies per case):")
    results = {}
    c_target, c_amp = 0.005, 0.0025   # injected shift ~ 2c = C
    for mirror, label in [(True, "klein"), (False, "antipodal")]:
        mc = null_distribution(per_ell, phi, cls_uK, masks, n_mc, rng,
                               mirror=mirror, inject_c=c_amp)
        results[label] = mc
        for name in masks:
            null = mc[name]["null"]
            shift = np.mean(mc[name]["inj"] - null)
            n_mean, n_std = np.mean(null), np.std(null)
            sig = shift / n_std
            print(f"  {label:9s} {name}: null = {n_mean:+.5f} +/- {n_std:.5f}, "
                  f"paired recovery shift = {shift:+.5f} -> {sig:.3f} sigma")
    return results


def run_gw():
    """5.3: GWTC-3 modulation detectability + NANOGrav ratio."""
    events, nanograv = compute_ist_gw_predictions(
        get_gwtc3_events(), get_nanograv_sgwb())
    rows = []
    print("5.3 GW time-crystal modulation (eps = alpha/phi^2 = "
          f"{EPS_TC:.2e}):")
    rng = np.random.default_rng(11)
    for e in events:
        # Plan 10/12 prediction: f_tc = f_rd / (2 phi) from the *measured*
        # catalog ringdown frequency (not the GR-mass-derived one).
        f_rd, snr = e["f_ringdown_Hz"], e["SNR"]
        f_tc = f_rd / (2 * PHI)
        sig_eps = sigma_epsilon(f_rd, f_tc, snr)
        significance = EPS_TC / sig_eps
        req_snr = 3.0 * snr / significance      # for a 3-sigma detection
        rows.append({
            "event": e["name"], "f_rd_Hz": f_rd, "f_tc_Hz": f_tc,
            "snr": snr, "sigma_eps": sig_eps,
            "detection_sigma": significance, "required_snr_3sigma": req_snr,
        })
        print(f"  {e['name']:10s} f_rd = {f_rd:6.0f} Hz  f_tc = {f_tc:6.1f} Hz  "
              f"SNR = {snr:5.1f} -> {significance:.3f} sigma "
              f"(needs SNR ~ {req_snr:.0f})")

    # injection/recovery cross-check on the highest-SNR event, boosted eps
    e0 = max(events, key=lambda e: e["SNR"])
    f_rd0, f_tc0 = e0["f_ringdown_Hz"], e0["f_ringdown_Hz"] / (2 * PHI)
    est, sig_eps = simulate_epsilon_recovery(
        f_rd0, f_tc0, e0["SNR"], epsilon=0.2, rng=rng)
    print(f"  injection check ({e0['name']}, eps = 0.2): "
          f"recovered {np.mean(est):.3f} +/- {np.std(est):.3f} "
          f"(analytic sigma {sig_eps:.3f})")

    ng = nanograv_extra_component()
    print(f"  NANOGrav: A_extra/A_obs = {ng['amplitude_ratio']:.2%}, "
          f"power ratio {ng['power_ratio']:.1e} "
          f"(needs ~{ng['required_sensitivity_factor']:.0e}x sensitivity)")
    return rows, ng, e0["name"], np.mean(est), np.std(est), sig_eps


# ───────────────────────────────────────────────────────────────────────────────
# FIGURES & REPORT FILES
# ───────────────────────────────────────────────────────────────────────────────

def make_figures(theta, noise, profiles, lensing_summary, cmb_results, gw_rows):
    figs = []

    # ── 5.1 lensing ──────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    colors = {"constant G (GR)": "k", "D = 2 (Phase 1.3)": "steelblue",
              "D = phi (IST)": "crimson", "D = 1/0.600 (Phase 4)": "seagreen"}
    for model, ax, title in [("A", axes[0], "A. Model A: local Poisson"),
                             ("B", axes[1], "B. Model B: interior-G suppression")]:
        for name, color in colors.items():
            g = profiles[(model, name)]
            ls = "--" if name == "constant G (GR)" else "-"
            ax.plot(theta, 1e4 * g, ls, color=color, lw=1.5, label=name)
        ax.errorbar(theta, 1e4 * profiles[(model, "constant G (GR)")],
                    1e4 * noise, fmt=".", color="gray", ms=4, alpha=0.6)
        ax.set_xlabel(r"angular radius $\theta$ (arcmin)")
        ax.set_ylabel(r"$\gamma_t \times 10^{4}$")
        ax.set_title(title)
        ax.legend(fontsize=7)
    fig.tight_layout()
    figs.append(("lensing_templates", fig))

    # ── 5.2 CMB nulls ────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for ax, (label, mc), title in [
            (axes[0], list(cmb_results.items())[0], "A. Klein flip (mirrored)"),
            (axes[1], list(cmb_results.items())[1], "B. Plain antipodal (control)")]:
        for name, color in zip(mc, ["steelblue", "seagreen", "crimson"]):
            ax.hist(mc[name]["null"], bins=25, histtype="step", color=color,
                    lw=1.5, label=f"{name} null")
            ax.axvline(np.mean(mc[name]["inj"] - mc[name]["null"])
                       + np.mean(mc[name]["null"]),
                       color=color, ls="--", label=f"{name} + 0.005 signal")
        ax.set_xlabel(r"antipodal correlation $C$")
        ax.set_ylabel("MC count")
        ax.set_title(title)
        ax.legend(fontsize=7)
    fig.tight_layout()
    figs.append(("cmb_null", fig))

    # ── 5.3 GW ───────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))
    names = [r["event"] for r in gw_rows]
    det = [r["detection_sigma"] for r in gw_rows]
    ax.bar(names, det, color="steelblue")
    ax.axhline(3.0, color="crimson", ls="--", label=r"3$\sigma$ threshold")
    ax.set_ylabel(r"detection significance ($\sigma$)")
    ax.set_title(r"Time-crystal modulation $\varepsilon = \alpha/\varphi^2$ "
                 "in GWTC-3 ringdowns")
    ax.legend(fontsize=8)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    fig.tight_layout()
    figs.append(("gw_modulation", fig))

    return figs


def write_pdf(path, figs, summary_lines):
    """Multi-page falsification summary: text page + the three figures."""
    with PdfPages(path) as pdf:
        fig = plt.figure(figsize=(8.5, 11))
        fig.text(0.08, 0.95, "IST Phase 5 - Falsification Summary",
                 fontsize=16, weight="bold")
        fig.text(0.08, 0.90, "\n".join(summary_lines), fontsize=9,
                 family="monospace", va="top")
        pdf.savefig(fig)
        plt.close(fig)
        for _, f in figs:
            pdf.savefig(f)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    theta, noise, profiles, lensing_summary, lensing_rows = run_lensing()
    with open(os.path.join(OUT_DIR, "lensing_shear.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(lensing_rows[0].keys()))
        writer.writeheader()
        writer.writerows(lensing_rows)
    print(f"Wrote {os.path.join(OUT_DIR, 'lensing_shear.csv')}\n")

    cmb_results = run_cmb()
    cmb_rows = []
    for label, mc in cmb_results.items():
        for name, d in mc.items():
            null = d["null"]
            shift = float(np.mean(d["inj"] - null))
            cmb_rows.append({
                "flip": label, "mask": name,
                "null_mean": np.mean(null), "null_std": np.std(null),
                "recovery_shift": shift,
                "shift_over_injected": shift / 0.005,
                "detection_sigma": shift / np.std(null),
            })
    with open(os.path.join(OUT_DIR, "cmb_antipodal_summary.csv"), "w",
              newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(cmb_rows[0].keys()))
        writer.writeheader()
        writer.writerows(cmb_rows)
    print(f"Wrote {os.path.join(OUT_DIR, 'cmb_antipodal_summary.csv')}\n")

    gw_rows, ng, inj_event, inj_mean, inj_std, inj_sig = run_gw()
    with open(os.path.join(OUT_DIR, "gw_modulation.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(gw_rows[0].keys()))
        writer.writeheader()
        writer.writerows(gw_rows)
    print(f"Wrote {os.path.join(OUT_DIR, 'gw_modulation.csv')}\n")

    figs = make_figures(theta, noise, profiles, lensing_summary,
                        cmb_results, gw_rows)
    for name, fig in figs:
        fig.savefig(os.path.join(OUT_DIR, f"{name}.png"), dpi=300)
        print(f"Wrote {os.path.join(OUT_DIR, name + '.png')}")

    # ── falsification summary ────────────────────────────────────────────
    best_cmb = max(cmb_rows, key=lambda r: r["detection_sigma"])
    cmb_null_max = max(abs(r["null_std"]) for r in cmb_rows)
    best_gw = max(gw_rows, key=lambda r: r["detection_sigma"])
    summary_lines = [
        "PREDICTION                              TARGET            RESULT                VERDICT",
        "-" * 92,
    ]
    for s in lensing_summary:
        verdict = ("DISTINGUISHABLE" if s["significance_sigma"] >= 3
                   else "not distinguishable")
        summary_lines.append(
            f"void lensing [{s['model']:5s}] {s['comparison']:24s} "
            f"{s['significance_sigma']:7.1f} sigma       {verdict}")
    summary_lines += [
        "-" * 92,
        f"CMB antipodal C = 0.005 (synthetic)   recovery shift    "
        f"{best_cmb['detection_sigma']:7.3f} sigma       NOT recoverable: null "
        f"sigma ~ {cmb_null_max:.2f} is ~{cmb_null_max/0.005:.0f}x the signal",
        f"GW ringdown modulation eps = a/phi^2  best event        "
        f"{best_gw['detection_sigma']:7.3f} sigma       NOT detectable "
        f"({best_gw['event']}, needs SNR ~ {best_gw['required_snr_3sigma']:.0f})",
        f"NANOGrav extra SGWB component         A/A_obs = 0.28%   "
        f"power ratio {ng['power_ratio']:.1e}   below sensitivity "
        f"(needs ~{ng['required_sensitivity_factor']:.0e}x)",
        "-" * 92,
        "Notes:",
        "* Lensing models A and B deviate from GR in OPPOSITE directions; the",
        "  correct mapping from G(rho) to the lensing signal is an open item",
        "  for the IST field-equation derivation.",
        "* CMB: the paired injection IS recovered exactly (shift/0.005 = "
        f"{best_cmb['shift_over_injected']:.2f}); the statistic works, but",
        "  single-sky cosmic variance swamps the claimed signal. The original",
        "  C ~ 0.005 measurement is consistent with LCDM noise.",
        "* GW eps injection/recovery cross-check: "
        f"{inj_event}, eps = 0.2 -> {inj_mean:.3f} +/- {inj_std:.3f} "
        f"(analytic {inj_sig:.3f}).",
    ]
    for line in summary_lines:
        print(line)
    write_pdf(os.path.join(OUT_DIR, "falsification_summary.pdf"),
              figs, summary_lines)
    print(f"Wrote {os.path.join(OUT_DIR, 'falsification_summary.pdf')}")


if __name__ == "__main__":
    main()
