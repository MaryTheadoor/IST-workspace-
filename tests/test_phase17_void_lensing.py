"""Tests for phase17_void_lensing.py"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from phase17_void_lensing import *
from phase1_klein_laplacian import PHI

class TestVoidShear:
    def test_pinned_suppresses_gr(self):
        th = np.linspace(10, 100, 8)
        gp = void_shear(th, 0.8, 2.0, 30.0, -0.8, PHI)
        gg = void_shear(th, 0.8, 2.0, 30.0, -0.8, None)
        assert np.min(gp) > np.min(gg)  # less negative = suppressed
    def test_pinned_vs_phase4_near(self):
        th = np.linspace(5, 120, 12)
        gp = void_shear(th, 0.8, 2.0, 30.0, -0.8, PHI)
        g4 = void_shear(th, 0.8, 2.0, 30.0, -0.8, D_PHASE4)
        assert np.max(np.abs(gp - g4)/np.max(np.abs(gp))) < 0.05
    def test_sigma_crit_sensible(self):
        sc = sigma_crit(0.8, 2.0)
        assert 1e14 < sc < 1e16
    def test_suppression_positive(self):
        th = np.linspace(5, 120, 10)
        gp = void_shear(th, 0.8, 2.0, 30.0, -0.8, PHI)
        gg = void_shear(th, 0.8, 2.0, 30.0, -0.8, None)
        assert np.sum(np.abs(gp)) < np.sum(np.abs(gg))
