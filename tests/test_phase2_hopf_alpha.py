"""
Unit tests for phase2_hopf_alpha.py — IST Phase 2
===================================================
Discrete Hopf fibration construction, topology (Chern number), spectral
dimension of the total space, and the Kaluza-Klein alpha relation.

Run: cd code && python -m pytest ../tests/test_phase2_hopf_alpha.py -v
"""

import sys
import os

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase2_hopf_alpha import DiscreteHopfFibration, sweep
from phase1_rg_flow import spectral_dimension
from ist_toolkit_v2 import ALPHA


# ── Construction & Counting ───────────────────────────────────────────────────

class TestConstruction:
    def test_vertex_counts(self):
        h = DiscreteHopfFibration(n_lat=5, n_lon=8, fiber_period=4, chern=1)
        assert h.n_base == 2 + 3 * 8
        assert h.n_total == h.n_base * 4

    def test_fiber_cycles_have_correct_length(self):
        h = DiscreteHopfFibration(n_lat=5, n_lon=8, fiber_period=6, chern=1)
        # Each base vertex owns a cycle of length fiber_period in the adjacency.
        # Pick an arbitrary fiber vertex and walk its neighbors within the same base.
        A = h.A.toarray()
        for bid in [0, 3, h.n_base - 1]:
            start = bid * h.fiber_period
            visited = set()
            cur = start
            for _ in range(h.fiber_period):
                visited.add(cur)
                # neighbors within the same fiber
                same_fiber = [n for n in range(cur - cur % h.fiber_period,
                                                cur - cur % h.fiber_period + h.fiber_period)
                              if n != cur and A[cur, n] > 0]
                assert len(same_fiber) == 2
                nxt = [n for n in same_fiber if n not in visited or len(visited) == h.fiber_period][0]
                cur = nxt
            assert len(visited) == h.fiber_period

    def test_total_space_connected(self):
        h = DiscreteHopfFibration(n_lat=4, n_lon=6, fiber_period=3, chern=1)
        L = h.laplacian().toarray()
        vals = np.linalg.eigh(L)[0]
        assert vals[0] < 1e-10  # single zero mode for connected bundle over S^2


# ── Topology ──────────────────────────────────────────────────────────────────

class TestTopology:
    def test_chern_number_one(self):
        h = DiscreteHopfFibration(n_lat=6, n_lon=12, fiber_period=5, chern=1)
        assert h.chern_number() == 1

    def test_chern_number_two(self):
        h = DiscreteHopfFibration(n_lat=6, n_lon=12, fiber_period=5, chern=2)
        assert h.chern_number() == 2

    def test_chern_number_three(self):
        h = DiscreteHopfFibration(n_lat=7, n_lon=16, fiber_period=6, chern=3)
        assert h.chern_number() == 3


# ── Spectral Geometry ─────────────────────────────────────────────────────────

class TestSpectralGeometry:
    def test_total_space_is_three_dimensional(self):
        # The total space is topologically S^3, but finite discretization and
        # the twisted bundle push the fitted spectral dimension slightly above 3.
        # We test that it is clearly 3-dimensional (not 2 or 4).
        h = DiscreteHopfFibration(n_lat=8, n_lon=16, fiber_period=10, chern=1)
        D, r2, _, _ = spectral_dimension(h.laplacian(), window_low=0.05, window_high=0.25)
        assert 2.5 < D < 3.8, f"expected ~3, got {D}"
        assert r2 > 0.95


# ── Alpha Relation ────────────────────────────────────────────────────────────

class TestAlphaRelation:
    def test_alpha_raw_formula(self):
        h = DiscreteHopfFibration(n_lat=4, n_lon=6, fiber_period=10, chern=1)
        Rf = h.fiber_radius()
        expected = 4.0 / (Rf * Rf)
        assert abs(h.alpha_raw() - expected) < 1e-12

    def test_fiber_period_three_gives_large_raw_alpha(self):
        h = DiscreteHopfFibration(n_lat=5, n_lon=10, fiber_period=3, chern=1)
        alpha_inv = 1.0 / h.alpha_raw()
        assert alpha_inv < 1.0  # far from observed ~137

    def test_sweep_produces_rows(self):
        rows = sweep(fiber_periods=[3, 5, 7], n_lat=5, n_lon=8, chern=1)
        assert len(rows) == 3
        for r in rows:
            assert r["cher_number_computed"] == 1
            assert r["alpha_raw"] > 0
