"""Tests for phase16_dimensions.py"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from phase16_dimensions import *


class TestDimSubstrate:
    def test_adjacency_degree(self):
        for d in [2, 3, 4]:
            A = build_d_dim_periodic(4, d)
            deg = np.asarray(A.sum(axis=1)).ravel()
            assert np.all(deg == 2 * d)

    def test_adjacency_symmetric(self):
        A = build_d_dim_periodic(5, 3)
        assert np.allclose(A.toarray(), A.toarray().T)

    def test_d_dim_laplacian_psd(self):
        L = d_dim_laplacian(4, 3)
        vals = np.linalg.eigvalsh(L.toarray())
        assert vals.min() > -1e-10


class TestDimScan:
    @classmethod
    def setup_class(cls):
        cls.rows = []
        for d, n, ticks in [(2, 8, 100), (3, 6, 100), (4, 5, 100)]:
            D, coh, amp = run_d_dim_simulation(n, d, n_ticks=ticks)
            cls.rows.append({"dim": d, "D_eff": D, "coherence": coh,
                             "amplification": amp})

    def test_d_eff_measured(self):
        for r in self.rows:
            assert not np.isnan(r["D_eff"])

    def test_d_eff_peak_at_3(self):
        vals = [r["D_eff"] for r in self.rows]
        assert vals[1] > vals[0]  # 3D > 2D

    def test_amplification_finite(self):
        for r in self.rows:
            assert 0 < r["amplification"] < 3
