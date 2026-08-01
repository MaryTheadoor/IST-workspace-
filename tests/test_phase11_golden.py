"""
Unit tests for phase11_golden_substrate.py -- IST Phase 11
===========================================================
Golden-filtered Klein vector substrate: per-edge coupling weights,
golden attractor, pattern fragmentation.

Run: cd code && python -m pytest ../tests/test_phase11_golden.py -v
"""

import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from phase11_golden_substrate import KleinGoldenSubstrate, ALPHA_GOLDEN
from phase1_klein_laplacian import PHI


class TestGoldenWeights:
    def test_golden_weight_is_1_for_golden_separation(self):
        sub = KleinGoldenSubstrate(n=16)
        d = 2 * np.pi * ALPHA_GOLDEN
        assert sub._gold_weight(np.array([d]))[0] == 1.0

    def test_default_weight_is_0_3(self):
        sub = KleinGoldenSubstrate(n=16)
        assert sub._gold_weight(np.array([0.5]))[0] == 0.3

    def test_rational_weight_is_0(self):
        sub = KleinGoldenSubstrate(n=16)
        assert sub._gold_weight(np.array([np.pi]))[0] == 0.0

    def test_phase_diff_wraps(self):
        sub = KleinGoldenSubstrate(n=16)
        d = sub._phase_diff(0.1, 2 * np.pi - 0.05)
        assert np.abs(d - 0.15) < 1e-6


class TestSubstrateDynamics:
    @classmethod
    def setup_class(cls):
        cls.sub = KleinGoldenSubstrate(n=40, noise_std=0.02, gain=3.0, seed=5)
        cls.rows = cls.sub.run(n_steps=300)

    def test_state_has_three_channels(self):
        assert self.sub.state.shape == (40, 40, 3)

    def test_total_info_is_finite(self):
        assert np.isfinite(self.rows[-1]["total_info"])

    def test_golden_fraction_bounded(self):
        for r in self.rows:
            assert 0 <= r["golden_frac"] <= 1.0

    def test_entropy_bounded(self):
        for r in self.rows:
            assert 0 < r["entropy"] < 20

    def test_pattern_count_positive(self):
        assert self.rows[-1]["patterns"] > 0

    def test_phase_range_is_circle(self):
        p = self.sub.phase
        assert p.min() >= 0
        assert p.max() <= 2 * np.pi + 1e-9

    def test_tanh_bounds_state(self):
        amp = np.sqrt(np.sum(self.sub.state ** 2, axis=-1))
        assert amp.max() < 2.0
