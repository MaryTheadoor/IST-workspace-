"""Tests for phase14_feedback.py"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from phase14_feedback import *
from phase1_klein_laplacian import PHI


class TestFeedback:
    @classmethod
    def setup_class(cls):
        cls.fa, cls.da = load_phase4_d_eff()
        cls.results = {}
        for f0 in [1.5, 4.0, 12.0]:
            f, D, G = integrate_feedback(f0, cls.fa, cls.da, 0.3, 0.02, 800)
            cls.results[f0] = (f, D, G)

    def test_d_eff_decreases_with_f(self):
        assert self.da[0] > self.da[-1]

    def test_converges_from_below(self):
        _, D, _ = self.results[1.5]
        assert abs(D[-1] - PHI) < 0.15

    def test_converges_from_above(self):
        _, D, _ = self.results[12.0]
        assert abs(D[-1] - PHI) < 0.15

    def test_golden_window_near_4_2(self):
        f, _, _ = self.results[4.0]
        assert abs(f[-1] - 4.2) < 0.3

    def test_g_exponent_approaches_one_over_phi(self):
        _, D, _ = self.results[4.0]
        assert abs(1/D[-1] - 1/PHI) < 0.05

    def test_d_eff_of_f_monotonic(self):
        vals = d_eff_of_f(np.linspace(1.2, 15, 30), self.fa, self.da)
        assert np.all(np.diff(vals) < 0)  # strictly decreasing
