"""
Unit tests for phase10_gpu_substrate.py -- IST Phase 10
========================================================
2D Klein bottle vector substrate: doubly-stochastic coupling,
cross-component directed-number dynamics, twist correlation.

Run: cd code && python -m pytest ../tests/test_phase10_substrate.py -v
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase10_gpu_substrate import KleinVectorSubstrate


class TestVectorSubstrate:
    @classmethod
    def setup_class(cls):
        cls.sub = KleinVectorSubstrate(n=48, noise_std=0.01, gain=1.4, seed=3)
        cls.rows = cls.sub.run(n_steps=400)

    def test_subcritical_decays(self):
        sub = KleinVectorSubstrate(n=32, noise_std=0.01, gain=0.5, seed=1)
        r = sub.run(n_steps=200)
        # with gain < 1, signal should decay
        assert r[-1]["total_info"] < r[0]["total_info"]

    def test_supercritical_grows(self):
        sub = KleinVectorSubstrate(n=32, noise_std=0.01, gain=1.3, seed=1)
        r = sub.run(n_steps=200)
        assert r[-1]["total_info"] > r[0]["total_info"]

    def test_state_has_three_channels(self):
        assert self.sub.state.shape == (48, 48, 3)

    def test_twist_correlation_is_nonzero(self):
        # the Klein twist creates a non-trivial boundary correlation
        assert abs(self.rows[-1]["twist_corr"]) > 0.1

    def test_information_stabilizes(self):
        last10 = [r["total_info"] for r in self.rows[-10:]]
        assert np.std(last10) / max(np.mean(last10), 1) < 0.05

    def test_pattern_count_is_one(self):
        # field is everywhere active (no isolated dead zones)
        assert self.rows[-1]["patterns"] == 1

    def test_tanh_bounded(self):
        # amplitudes are bounded by tanh
        amp = np.sqrt(np.sum(self.sub.state ** 2, axis=-1))
        assert amp.max() < 2.0  # sqrt(3) ~ 1.732
        assert amp.min() >= 0

    def test_cross_component_exists(self):
        # up and down channels should differ (competition creates asymmetry)
        up = self.sub.state[:, :, 0]
        dn = self.sub.state[:, :, 1]
        # they shouldn't be identical everywhere
        assert np.max(np.abs(up - dn)) > 0.01
