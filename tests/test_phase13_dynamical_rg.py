"""Tests for phase13_dynamical_rg.py"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from phase13_dynamical_rg import *
from phase11_golden_substrate import KleinGoldenSubstrate, PHI


class TestDynamicalRG:
    @classmethod
    def setup_class(cls):
        cls.sub = KleinGoldenSubstrate(n=40, noise_std=0.02, gain=3.0, seed=3)
        cls.rows = run_dynamical_rg(cls.sub, n_epochs=10, ticks_per_epoch=40)

    def test_golden_adjacency_symmetric(self):
        adj = golden_adjacency(self.sub)
        assert np.allclose(adj.toarray(), adj.toarray().T)

    def test_effective_laplacian_has_entries(self):
        L = effective_laplacian(self.sub)
        assert L.nnz > 0

    def test_components_detected(self):
        for r in self.rows:
            assert r["n_coarse"] > 500  # many small golden components

    def test_d_eff_measured(self):
        valid = [r for r in self.rows if not np.isnan(r["D_eff"])]
        assert len(valid) >= 5

    def test_d_eff_bounded(self):
        for r in self.rows:
            if not np.isnan(r["D_eff"]):
                assert 0.8 < r["D_eff"] < 5.0

    def test_golden_fraction_stable(self):
        gs = [r["golden_frac"] for r in self.rows]
        assert abs(gs[-1] - gs[0]) < 0.05

    def test_substrate_evolves(self):
        assert self.sub.step_count > 0
