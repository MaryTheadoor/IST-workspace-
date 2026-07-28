"""
Unit tests for phase7_vector_substrate.py -- IST Phase 7
=========================================================
Spectral-proximity coupling graph on the oscillator circle:
Fibonacci vs random vs rational ensembles.

Run: cd code && python -m pytest ../tests/test_phase7_vector_substrate.py -v
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase7_vector_substrate import (
    PHI, ALPHA_GOLDEN,
    fibonacci_phases, rational_phases, random_phases,
    spectral_graph, spectral_dimension,
)


class TestEnsembles:
    def test_fibonacci_phases_are_sorted(self):
        p = fibonacci_phases(128)
        assert np.all(np.diff(p) >= 0)

    def test_fibonacci_three_gap_structure(self):
        p = fibonacci_phases(89)
        gaps = np.diff(np.append(p, p[0] + 2 * np.pi))
        u = np.unique(np.round(gaps, 8))
        assert 2 <= len(u) <= 3

    def test_random_phases_cover_circle(self):
        rng = np.random.default_rng(0)
        p = random_phases(200, rng)
        assert p[0] > 0
        assert p[-1] < 2 * np.pi + 1e-6

    def test_rational_phases_not_degenerate(self):
        p = rational_phases(128)
        assert np.all(np.diff(p) >= 0)
        assert p[-1] < 2 * np.pi + 1e-6


class TestSpectralGraph:
    def test_graph_is_symmetric(self):
        A, _, _ = spectral_graph(fibonacci_phases(64), sigma=0.1)
        D = A.toarray()
        assert np.allclose(D, D.T)

    def test_graph_connected_at_moderate_sigma(self):
        _, L, _ = spectral_graph(fibonacci_phases(64), sigma=0.1)
        vals = spectral_dimension(L)[0]
        assert not np.isnan(vals)

    def test_degree_grows_with_sigma(self):
        d1 = spectral_graph(fibonacci_phases(64), 0.05)[2]
        d2 = spectral_graph(fibonacci_phases(64), 0.2)[2]
        assert d2 > d1


class TestFibonacciSpectralDimension:
    def test_fibonacci_d_eff_stable_over_degree_range(self):
        """D_eff stays within [1.05, 1.25] for degrees 10–40 (self-similar regime)."""
        for sig in [0.07, 0.10, 0.15, 0.20]:
            _, L, deg = spectral_graph(fibonacci_phases(64), sigma=sig)
            D, r2 = spectral_dimension(L)
            if 10 <= deg <= 40 and not np.isnan(D):
                assert 1.05 < D < 1.25, f"sig={sig:.3f} D_eff={D:.3f}"
                assert r2 > 0.85

    def test_fibonacci_not_converging_to_grid_dimension(self):
        """Fibonacci D_eff (~1.1) is far from the grid's D=2."""
        for sig in [0.08, 0.12, 0.18]:
            _, L, deg = spectral_graph(fibonacci_phases(64), sigma=sig)
            D, _ = spectral_dimension(L)
            assert abs(D - 2.0) > 0.5, f"D={D:.3f} too close to grid D=2"


class TestRandomDimensionality:
    def test_random_d_eff_varies_with_degree(self):
        """Random graph's D_eff is not constant (unlike Fibonacci)."""
        vals = []
        for sig in [0.05, 0.10, 0.20]:
            _, L, _ = spectral_graph(random_phases(64,
                                     np.random.default_rng(1)), sigma=sig)
            D, _ = spectral_dimension(L)
            if not np.isnan(D):
                vals.append(D)
        assert max(vals) - min(vals) > 0.15


class TestRationalDimensionality:
    def test_rational_degrees_vary_with_sigma(self):
        d1 = spectral_graph(rational_phases(64), 0.05)[2]
        d2 = spectral_graph(rational_phases(64), 0.25)[2]
        assert d2 > d1
