"""Tests for phase16_joint_fit.py"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from phase16_joint_fit import *


class TestLoaders:
    def test_hz_loaded(self):
        z, H, s = load_hz(); assert len(z) > 30
    def test_pantheon_loaded(self):
        z, mu, e = load_pantheon(); assert len(z) > 1000

class TestCosmology:
    def test_ez_at_z0(self): assert abs(Ez(0, 0.3) - 1.0) < 1e-9
    def test_comoving_positive(self):
        assert comoving(1.0, 70, 0.3) > 1000
    def test_mu_monotonic(self):
        zs = np.linspace(0.01, 2, 10)
        mu = mu_pred(zs, 70, 0.3); assert np.all(np.diff(mu) > 0)
    def test_hz_lcdm_at_z0(self):
        assert abs(Hz_lcdm(0, 70, 0.3) - 70) < 1

class TestJointFit:
    @classmethod
    def setup_class(cls):
        cls.zh, cls.Hd, cls.sh = load_hz()
        cls.zs, cls.mu_d, cls.mu_e = load_pantheon()
        r_l = minimize(lambda p: chi2_total(p, cls.zh, cls.Hd, cls.sh,
                         cls.zs, cls.mu_d, cls.mu_e, False),
                       [70, 0.3], method="Nelder-Mead", options={"maxiter": 500})
        cls.chi2_lcdm = r_l.fun
        r_o = minimize(lambda p: chi2_total(p, cls.zh, cls.Hd, cls.sh,
                         cls.zs, cls.mu_d, cls.mu_e, True),
                       [r_l.x[0], r_l.x[1], 0.1, 1.618, 0.618],
                       method="Nelder-Mead", options={"maxiter": 500})
        cls.chi2_osc = r_o.fun
        cls.dchi2 = cls.chi2_lcdm - cls.chi2_osc

    def test_lcdm_chi2_reasonable(self): assert self.chi2_lcdm > 500
    def test_osc_improves_fit(self): assert self.dchi2 > 10
    def test_dchi2_significant(self): assert self.dchi2 > 15
