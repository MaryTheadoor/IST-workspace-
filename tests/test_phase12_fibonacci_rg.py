"""Tests for phase12_fibonacci_rg.py"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from phase12_fibonacci_rg import *


class TestGRO:
    def test_phases_on_circle(self):
        p = gro_phases(100)
        assert 0 <= p.min() and p.max() <= 2 * np.pi + 1e-9
    def test_coupling_symmetric(self):
        J = gro_coupling(50, 0.03); assert np.allclose(J, J.T)
    def test_laplacian_psd(self):
        L = gro_laplacian(50, 0.03)
        v = np.linalg.eigvalsh(L.toarray()); assert v.min() > -1e-10


class TestBlocking:
    def test_blocks_cover_all(self):
        for f in [fibonacci_blocking, uniform_blocking, random_blocking]:
            P = f(100, 30); assert P.nnz == 100
    def test_fib_variable_sizes(self):
        P = fibonacci_blocking(200, 50)
        s = np.asarray(P.sum(axis=0)).ravel(); assert s.max() > s.min()


class TestRGFlow:
    @classmethod
    def setup_class(cls):
        L0 = gro_laplacian(200, sigma=0.06)
        cls.fib = run_scheme(L0, 200, "Fibonacci", n_levels=2, coarsen_factor=3)
        cls.uni = run_scheme(L0, 200, "Uniform", n_levels=2, coarsen_factor=3)

    def test_d_eff_measured(self):
        for r in self.fib:
            if r["N"] >= 20: assert not np.isnan(r["D_eff"])

    def test_d_eff_bounded(self):
        for r in self.fib + self.uni:
            if not np.isnan(r["D_eff"]): assert 0.5 < r["D_eff"] < 8
