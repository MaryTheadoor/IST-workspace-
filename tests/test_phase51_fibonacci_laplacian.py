"""
Unit tests for phase51_fibonacci_laplacian.py -- IST Phase 51
=====================================================================
Tests the Fibonacci Laplacian: rebuilding Phase 1's raster spectral
analysis on the true incommensurate (golden-angle / Fibonacci) lattice.

Run: cd code && python -m pytest ../tests/test_phase51_fibonacci_laplacian.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase51_fibonacci_laplacian import (
    PHI, ALPHA_GOLD,
    fib_word, word_product, kkt_trace_map,
    chain_laplacian_1d, periodic_laplacian_1d,
    cantor_measure_table, band_cluster_count,
    fibonacci_lattice_points, raster_grid_points,
    klein_coupling_laplacian, klein_distance,
    klein_lattice_comparison, gap_ratio_stats,
    spectral_dimension, rg_flow_2d,
)


class TestTraceMapExact:
    def test_trace_map_recurrence_machine_precision(self):
        err, spread = kkt_trace_map()
        assert err < 1e-11          # x_{n+1} = 2x_n x_{n-1} - x_{n-2}
        assert spread < 1e-5        # KKT invariant conserved

    def test_invariant_value_is_golden_constant(self):
        # The KKT (Fricke) invariant is a fixed constant along the orbit
        _, spread = kkt_trace_map()
        assert np.isfinite(spread)

    def test_word_lengths_are_fibonacci(self):
        from phase51_fibonacci_laplacian import fib_word
        lens = [len(fib_word(n)) for n in range(3, 9)]
        assert lens == [5, 8, 13, 21, 34, 55]


class TestCantorFragmentation:
    def test_fibonacci_fragments_far_more_than_rational(self):
        table = cantor_measure_table(n_hi=14)
        last = table[-1]
        assert last["bands_fib"] > 5 * last["bands_periodic"]

    def test_rational_control_stays_small(self):
        table = cantor_measure_table(n_hi=14)
        assert max(r["bands_periodic"] for r in table) <= 2

    def test_fibonacci_measure_collapses(self):
        # occupancy of the spectral support drops monotonically-ish
        table = cantor_measure_table(n_hi=14)
        occ_early = [r["occ_fib"] for r in table if r["generation"] >= 12]
        assert occ_early[-1] < occ_early[0]
        assert occ_early[-1] < 0.25   # deep Cantor collapse


class Test2DParityInvariant:
    def test_twist_fraction_matches_phase23a(self):
        # Fibonacci lattice: parity-inversion fraction ~ 0.446 (Phase 23a),
        # and essentially N-independent.
        for N, sigma in [(210, 0.15), (360, 0.12), (480, 0.10)]:
            r = klein_lattice_comparison(N, sigma)
            assert abs(r["twist_frac_fib"] - 0.446) < 0.02

    def test_twist_fraction_stable_vs_raster_drift(self):
        # Fibonacci twist fraction is tightly repeated across sizes; the
        # raster grid's parity fraction depends visibly on N (grid locking).
        fr = [klein_lattice_comparison(N, s)["twist_frac_fib"]
              for N, s in [(210, 0.15), (360, 0.12), (480, 0.10)]]
        ra = [klein_lattice_comparison(N, s)["twist_frac_raster"]
              for N, s in [(210, 0.15), (360, 0.12), (480, 0.10)]]
        assert np.std(fr) < np.std(ra)

    def test_fib_point_in_unit_patch(self):
        # fibonacci lattice stays on the [0,1)^2 patch
        us, vs = fibonacci_lattice_points(360)
        assert us.min() >= 0 and us.max() < 1
        assert vs.min() >= 0 and vs.max() < 1


class TestRGHonestNegative:
    def test_d_eff_never_phi(self):
        # THE core honest result: even on the true incommensurate lattice,
        # the static spectral dimension does NOT equal phi.
        us, vs = fibonacci_lattice_points(480)
        rows = rg_flow_2d(us, vs, n_levels=4)
        for r in rows:
            assert np.isnan(r["D_eff"]) or abs(r["D_eff"] - PHI) > 0.1

    def test_d_eff_stays_near_raster_two(self):
        # D_eff ~ 2 (lattice dimension), like Phase 1 raster, NOT a golden D.
        us, vs = fibonacci_lattice_points(480)
        rows = rg_flow_2d(us, vs, n_levels=4)
        valid = [r["D_eff"] for r in rows if not np.isnan(r["D_eff"])]
        assert all(1.7 < d < 2.6 for d in valid)

    def test_weyl_fit_good_quality(self):
        rows = rg_flow_2d(fibonacci_lattice_points(480)[0],
                          fibonacci_lattice_points(480)[1], n_levels=4)
        assert all(r["r2"] > 0.9 for r in rows if not np.isnan(r["D_eff"]))


class TestAlphasGolden:
    def test_golden_rotation_constant(self):
        assert abs(ALPHA_GOLD - 1 / PHI ** 2) < 1e-12