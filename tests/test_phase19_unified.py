"""Tests for phase19_unified.py"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from phase19_unified import UnifiedSubstrate, PHI


class TestUnified:
    @classmethod
    def setup_class(cls):
        cls.sub = UnifiedSubstrate(n_noise=80, sigma=0.6, seed=3)
        cls.rows = cls.sub.run_layers(n_layers=8, n_new=15)

    def test_d_eff_measured(self):
        valid = [r for r in self.rows if not np.isnan(r["D_eff"])]
        assert len(valid) >= 5

    def test_d_eff_bounded(self):
        for r in self.rows:
            if not np.isnan(r["D_eff"]):
                assert 1.5 < r["D_eff"] < 12

    def test_golden_fraction_increases(self):
        assert self.rows[-1]["golden_frac"] > self.rows[0]["golden_frac"]

    def test_d_eff_descends(self):
        # D_eff decreases as golden fraction increases (2D spatial model)
        ds = [r["D_eff"] for r in self.rows[1:] if not np.isnan(r["D_eff"])]
        if len(ds) >= 3:
            assert ds[-1] < ds[0]
