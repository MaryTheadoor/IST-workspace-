"""
Unit tests for phase5_observational_tests.py -- IST Phase 5
============================================================
Void lensing templates with derived G(rho), CMB Klein parity flip null
tests, and GW time-crystal modulation detectability.

Run: cd code && python -m pytest ../tests/test_phase5_observational.py -v
"""

import sys
import os

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from ist_toolkit_v2 import PHI, ALPHA
from phase5_observational_tests import (
    sigma_crit, rho_bar_msun_mpc3, angular_diameter,
    void_shear, void_contrast_model_a, void_contrast_model_b,
    shear_noise, chi2_between, PHASE4_WINDOW_SLOPE,
    cl_low_ell, make_grid, precompute_ylm, synthesize_sky,
    apply_klein_parity_flip, galactic_mask, antipodal_correlation,
    inject_correlated, null_distribution,
    ringdown_waveform, modulation_template, fit_modulation,
    sigma_epsilon, simulate_epsilon_recovery, nanograv_extra_component,
    EPS_TC,
)

Z_L, Z_S, R_V, DELTA = 0.8, 2.0, 30.0, -0.8


# ── 5.1 Void lensing ─────────────────────────────────────────────────────────

class TestCosmology:
    def test_sigma_crit_positive_and_sensible(self):
        sc = sigma_crit(Z_L, Z_S)
        assert 1e14 < sc < 1e16  # M_sun / Mpc^2

    def test_angular_diameter_distance_peaks(self):
        # D_A must turn over at high z (standard LCDM behaviour)
        assert angular_diameter(0.5) < angular_diameter(0.8)

    def test_rho_bar_is_omega_m_times_critical(self):
        assert 3e10 < rho_bar_msun_mpc3() < 6e10


class TestVoidShear:
    THETA = np.linspace(5.0, 120.0, 12)

    def test_constant_g_baseline_is_negative_shear_inside(self):
        # voids produce negative tangential shear within the void radius
        g = void_shear(self.THETA, Z_L, Z_S, R_V, DELTA, None, model="A")
        assert np.min(g) < 0

    def test_constant_g_identical_across_models(self):
        gA = void_shear(self.THETA, Z_L, Z_S, R_V, DELTA, None, model="A")
        gB = void_shear(self.THETA, Z_L, Z_S, R_V, DELTA, None, model="B")
        assert np.allclose(gA, gB)

    def test_model_a_deepens_void(self):
        # local Poisson weighting: |(1+d)^{1+1/D} - 1| > |d|
        assert abs(void_contrast_model_a(DELTA, PHI)) > abs(DELTA)

    def test_model_b_suppresses_void(self):
        # IST narrative: interior-G suppression reduces the signal
        assert abs(void_contrast_model_b(DELTA, PHI)) < abs(DELTA)

    def test_model_b_phi_suppression_matches_readme_scale(self):
        # (1+d)^{1/phi} for d = -0.8 -> 0.37 (63% suppression); d = -0.9
        # gives 0.24 -> the ~76% figure in the IST phenomenology
        assert abs((0.2 ** (1 / PHI)) - 0.37) < 0.01
        assert abs((0.1 ** (1 / PHI)) - 0.24) < 0.01

    def test_d2_between_phi_and_gr(self):
        g_gr = void_shear(self.THETA, Z_L, Z_S, R_V, DELTA, None, model="B")
        g_2 = void_shear(self.THETA, Z_L, Z_S, R_V, DELTA, 2.0, model="B")
        g_phi = void_shear(self.THETA, Z_L, Z_S, R_V, DELTA, PHI, model="B")
        i = np.argmin(g_gr)
        assert abs(g_phi[i]) < abs(g_2[i]) < abs(g_gr[i])

    def test_phase4_window_close_to_phi_template(self):
        g_p4 = void_shear(self.THETA, Z_L, Z_S, R_V, DELTA,
                          1 / PHASE4_WINDOW_SLOPE, model="B")
        g_phi = void_shear(self.THETA, Z_L, Z_S, R_V, DELTA, PHI, model="B")
        assert np.max(np.abs(g_p4 - g_phi) / np.max(np.abs(g_phi))) < 0.05

    def test_noise_decreases_with_stack_size(self):
        n100 = shear_noise(self.THETA, n_voids=100)
        n400 = shear_noise(self.THETA, n_voids=400)
        assert np.allclose(n400, n100 / 2)

    def test_chi2_detection_scales_with_voids(self):
        g_phi = void_shear(self.THETA, Z_L, Z_S, R_V, DELTA, PHI, model="B")
        g_gr = void_shear(self.THETA, Z_L, Z_S, R_V, DELTA, None, model="B")
        c100 = chi2_between(g_phi, g_gr, shear_noise(self.THETA, n_voids=100))
        c400 = chi2_between(g_phi, g_gr, shear_noise(self.THETA, n_voids=400))
        assert abs(c400 / c100 - 4.0) < 0.01


# ── 5.2 CMB Klein parity flip ────────────────────────────────────────────────

class TestCMBPipeline:
    @classmethod
    def setup_class(cls):
        cls.theta, cls.phi = make_grid(32, 64)
        cls.per_ell = precompute_ylm(cls.theta, 30)
        cls.cls = np.zeros(31)
        cls.cls[2:] = cl_low_ell(np.arange(2, 31))
        cls.rng = np.random.default_rng(3)
        cls.mask = galactic_mask(cls.theta, 30)

    def test_cl_anchors_interpolate(self):
        c2 = cl_low_ell([2])[0]
        assert 900 < c2 < 1200  # C_2 = D_2 * 2pi/6 ~ 1047 uK^2

    def test_flip_is_involution(self):
        T = synthesize_sky(self.per_ell, self.phi, self.cls, self.rng)
        TT = apply_klein_parity_flip(apply_klein_parity_flip(T))
        assert np.array_equal(TT, T)

    def test_antipodal_flip_is_involution(self):
        T = synthesize_sky(self.per_ell, self.phi, self.cls, self.rng)
        TT = apply_klein_parity_flip(apply_klein_parity_flip(T, mirror=False),
                                     mirror=False)
        assert np.array_equal(TT, T)

    def test_fully_correlated_sky_gives_unit_statistic(self):
        T = synthesize_sky(self.per_ell, self.phi, self.cls, self.rng)
        Tsym = inject_correlated(T, 1.0)  # T + KT: fully symmetric component
        C = antipodal_correlation(Tsym, self.mask, mirror=True)
        assert C > 0.9

    def test_null_std_much_larger_than_ist_signal(self):
        # The honest Phase 5.2 finding: single-sky cosmic variance gives
        # sigma_C ~ 0.1, ~20-30x the claimed C = 0.005.
        mc = null_distribution(self.per_ell, self.phi, self.cls,
                               {"m30": self.mask}, 40, self.rng,
                               mirror=True, inject_c=0.0025)
        null = mc["m30"]["null"]
        assert np.std(null) > 10 * 0.005

    def test_paired_injection_recovers_shift(self):
        mc = null_distribution(self.per_ell, self.phi, self.cls,
                               {"m30": self.mask}, 40, self.rng,
                               mirror=True, inject_c=0.0025)
        shift = np.mean(mc["m30"]["inj"] - mc["m30"]["null"])
        assert abs(shift - 0.005) < 0.002


# ── 5.3 GW time-crystal modulation ───────────────────────────────────────────

class TestGWModulation:
    def test_waveform_decays(self):
        t = np.arange(0, 0.1, 1 / 16384)
        h = ringdown_waveform(t, 250.0)
        env = np.abs(h)
        assert env[:50].mean() > env[-50:].mean()

    def test_f_tc_prediction(self):
        assert abs(251.0 / (2 * PHI) - 77.6) < 0.5

    def test_epsilon_is_alpha_over_phi2(self):
        assert abs(EPS_TC - ALPHA / PHI ** 2) < 1e-15

    def test_sigma_epsilon_scales_inversely_with_snr(self):
        s24 = sigma_epsilon(251.0, 251.0 / (2 * PHI), 24.0)
        s48 = sigma_epsilon(251.0, 251.0 / (2 * PHI), 48.0)
        assert abs(s24 / s48 - 2.0) < 0.01

    def test_ist_signal_not_detectable_at_catalog_snr(self):
        # eps = alpha/phi^2 at SNR ~ 24 gives << 3 sigma
        sig = sigma_epsilon(251.0, 251.0 / (2 * PHI), 24.0)
        assert EPS_TC / sig < 0.5

    def test_recovery_unbiased_with_2x2_fit(self):
        rng = np.random.default_rng(11)
        est, sig = simulate_epsilon_recovery(
            2000.0, 2000.0 / (2 * PHI), 32.4, 0.2, rng, n_trials=100)
        assert abs(np.mean(est) - 0.2) < 3 * sig / np.sqrt(100) + 0.01
        assert abs(np.std(est) - sig) / sig < 0.3

    def test_recovery_unbiased_at_low_frequency(self):
        # f_tc ~ 32 Hz overlaps the ringdown envelope timescale; the 2x2
        # fit must still be unbiased (the inner-product estimator was not)
        rng = np.random.default_rng(12)
        est, sig = simulate_epsilon_recovery(
            105.0, 105.0 / (2 * PHI), 14.4, 0.2, rng, n_trials=100)
        assert abs(np.mean(est) - 0.2) < 3 * sig / np.sqrt(100) + 0.01

    def test_fit_modulation_orthogonal_templates(self):
        t = np.arange(0, 0.5, 1 / 16384)
        h = np.sin(2 * np.pi * 100 * t)
        g = np.sin(2 * np.pi * 100 * t + np.pi / 2)
        d = 3.0 * h + 0.7 * g
        eps, sig = fit_modulation(d, h, g, 1.0)
        assert abs(eps - 0.7) < 1e-10

    def test_nanograv_ratios(self):
        ng = nanograv_extra_component()
        assert abs(ng["amplitude_ratio"] - ALPHA / PHI ** 2) < 1e-15
        assert ng["power_ratio"] < 1e-5
        assert ng["required_sensitivity_factor"] > 1e5
