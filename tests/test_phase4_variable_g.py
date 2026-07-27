"""
Unit tests for phase4_variable_g.py -- IST Phase 4
===================================================
Compression spectrum (linearized Psi), slowest-mode fold latency, sheet/void
G_eff scaling, and nonlinear validation of the linear theory.

Run: cd code && python -m pytest ../tests/test_phase4_variable_g.py -v
"""

import sys
import os

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_klein_laplacian import PHI, build_klein_bottle_graph
from phase4_variable_g import (
    FoldedSubstrate, central_band, g_eff_normalized, fit_loglog_exponent,
    simulate_decay, fit_relaxation_time, crossing_time, run_scan,
    TARGET_EXPONENT, ZERO_TOL,
)

N_TEST = 32          # small grid for speed; spectra still analytic
N_BIG = 48           # for scaling trends


# ── Compression spectrum vs Phase 1 Laplacian ────────────────────────────────

class TestDecaySpectrum:
    def test_flat_klein_gamma_min_matches_analytic_gap(self):
        sub = FoldedSubstrate(N_TEST, twisted=True)
        analytic = 4 * np.sin(np.pi / (2 * N_TEST)) ** 2
        assert abs(sub.gamma_min() - analytic) < 1e-10

    def test_flat_spectrum_equals_laplacian_spectrum(self):
        # For f == 1 the generalized problem reduces to eig(L)
        sub = FoldedSubstrate(N_TEST, twisted=True)
        gammas = sub.decay_spectrum(k=6)
        lams = np.sort(np.linalg.eigvalsh(
            sub.graph.laplacian().toarray()))[:6]
        assert np.allclose(gammas, lams, atol=1e-8)

    def test_torus_zero_mode_gives_infinite_latency(self):
        # Constant section exists on the orientable control: gamma_min = 0
        sub = FoldedSubstrate(N_TEST, twisted=False)
        assert sub.gamma_min() < ZERO_TOL
        assert np.isinf(sub.tau_fold())

    def test_klein_latency_is_finite(self):
        sub = FoldedSubstrate(N_TEST, twisted=True)
        assert np.isfinite(sub.tau_fold())

    def test_mu_spectrum_relation(self):
        # Linearized Psi eigenvalues are mu_k = 1 - gamma_k/4
        sub = FoldedSubstrate(N_TEST, twisted=True)
        gammas = sub.decay_spectrum(k=5)
        mus = sub.mu_spectrum(k=5)
        assert np.allclose(mus, 1.0 - gammas / 4.0, atol=1e-12)
        assert np.all(mus < 1.0)  # all modes relax

    def test_uniform_fold_scales_gamma_exactly(self):
        # Uniform F = cI: L v = gamma c v => gamma = lambda / c
        c = 3.0
        flat = FoldedSubstrate(N_TEST, twisted=True, fold_factor=1.0)
        folded = FoldedSubstrate(N_TEST, twisted=True,
                                 band=(0, N_TEST), fold_factor=c)
        g_flat = flat.decay_spectrum(k=5)
        g_fold = folded.decay_spectrum(k=5)
        assert np.allclose(g_fold, g_flat / c, rtol=1e-6)

    def test_spectrum_is_real_and_nonnegative(self):
        sub = FoldedSubstrate(N_TEST, twisted=True,
                              band=central_band(N_TEST), fold_factor=8.0)
        gammas = sub.decay_spectrum(k=10)
        assert np.all(np.isreal(gammas))
        assert np.all(gammas > -1e-12)


# ── Slowest mode = gravitational time scale ──────────────────────────────────

class TestFoldLatency:
    def test_tau_increases_with_fold_factor(self):
        taus = []
        for f in [1.0, 2.0, 4.0, 8.0]:
            sub = FoldedSubstrate(N_TEST, twisted=True,
                                  band=central_band(N_TEST), fold_factor=f)
            taus.append(sub.tau_fold())
        assert all(b > a for a, b in zip(taus, taus[1:]))

    def test_tau_scales_linearly_for_large_fold(self):
        # Asymptotic regime: the slowest mode localizes in the band and
        # gamma_min ~ lambda_band / f, so tau ~ f (measured slope -> 1).
        f1, f2 = 12.0, 16.0
        s1 = FoldedSubstrate(N_BIG, twisted=True, band=central_band(N_BIG),
                             fold_factor=f1)
        s2 = FoldedSubstrate(N_BIG, twisted=True, band=central_band(N_BIG),
                             fold_factor=f2)
        slope = fit_loglog_exponent([f1, f2], [s1.tau_fold(), s2.tau_fold()])
        assert 0.8 < slope <= 1.05

    def test_g_eff_normalized_to_void(self):
        rows = run_scan(N_TEST, fold_scan=[1.0, 2.0, 4.0])
        g = [r["g_eff_norm"] for r in rows]
        assert abs(g[0] - 1.0) < 1e-12
        assert all(v > 1.0 for v in g[1:])

    def test_sheet_latency_exceeds_void_latency(self):
        sub = FoldedSubstrate(N_TEST, twisted=True,
                              band=central_band(N_TEST), fold_factor=4.0)
        assert sub.regional_tau(sub.band_mask()) > \
               sub.regional_tau(sub.void_window())

    def test_regional_tau_scales_with_fold(self):
        # Equal-size windows: Dirichlet gamma ~ lambda_patch / f
        s1 = FoldedSubstrate(N_TEST, twisted=True,
                             band=central_band(N_TEST), fold_factor=1.0)
        s4 = FoldedSubstrate(N_TEST, twisted=True,
                             band=central_band(N_TEST), fold_factor=4.0)
        ratio = s4.regional_tau(s4.band_mask()) / \
                s1.regional_tau(s1.band_mask())
        assert abs(ratio - 4.0) < 0.2

    def test_measured_exponent_is_super_d2_target_window(self):
        # Document where the local substrate lands between the D = 2
        # prediction (0.5) and the asymptotic linear regime (1.0); it does
        # not reproduce the IST target 1/phi on this finite scan.
        rows = run_scan(N_BIG)
        slope = fit_loglog_exponent([r["fold_factor"] for r in rows],
                                    [r["g_eff_norm"] for r in rows])
        assert 0.5 < slope < 1.0
        assert abs(slope - TARGET_EXPONENT) > 0.05  # honest tension


# ── Nonlinear Psi validation ─────────────────────────────────────────────────

class TestNonlinearPsi:
    def test_equilibrium_is_fixed_point(self):
        sub = FoldedSubstrate(N_TEST, twisted=True,
                              band=central_band(N_TEST), fold_factor=4.0)
        s0 = np.zeros(N_TEST * N_TEST)
        assert np.allclose(sub.psi_step(s0), s0)

    def test_map_is_bounded(self):
        sub = FoldedSubstrate(N_TEST, twisted=True,
                              band=central_band(N_TEST), fold_factor=4.0)
        s = np.full(N_TEST * N_TEST, 1e6)
        for _ in range(10):
            s = sub.psi_step(s)
        assert np.all(np.abs(s) < 1e6)

    def test_nonlinear_decay_matches_linear_tau(self):
        sub = FoldedSubstrate(N_TEST, twisted=True,
                              band=central_band(N_TEST), fold_factor=4.0)
        _, vecs = sub.decay_spectrum(k=1, return_eigenvectors=True)
        v_slow = vecs[:, 0] / np.sqrt(sub.fold)
        v_slow = v_slow / np.linalg.norm(v_slow)
        rng = np.random.default_rng(7)
        amps = simulate_decay(sub, rng.normal(size=N_TEST * N_TEST), 4000,
                              projector=v_slow)
        tau_num = fit_relaxation_time(np.arange(4000), amps, frac_start=0.3)
        assert abs(tau_num - sub.tau_fold()) / sub.tau_fold() < 0.05

    def test_crossing_time_increases_with_fold(self):
        times = []
        for f in [1.0, 4.0, 16.0]:
            sub = FoldedSubstrate(N_TEST, twisted=True,
                                  band=central_band(N_TEST), fold_factor=f)
            times.append(crossing_time(sub, n_steps=20000))
        assert all(np.isfinite(times))
        assert times[0] < times[1] < times[2]


# ── Utilities ────────────────────────────────────────────────────────────────

class TestUtilities:
    def test_fit_loglog_recovers_power_law(self):
        rho = np.linspace(1, 20, 50)
        assert abs(fit_loglog_exponent(rho, rho ** 0.618) - 0.618) < 1e-10

    def test_g_eff_normalized(self):
        g = g_eff_normalized([1.0, 2.0, 4.0], [10.0, 25.0, 40.0])
        assert np.allclose(g, [1.0, 2.5, 4.0])

    def test_central_band_geometry(self):
        j0, j1 = central_band(N_TEST)
        assert (j0, j1) == (N_TEST // 2 - 4, N_TEST // 2 + 4)
