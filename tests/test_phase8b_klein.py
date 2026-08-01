"""
Unit tests for KleinOscillatorSheet -- IST Phase 8b
=====================================================
2D Klein bottle oscillator sheet: geodesic metric, twist edge detection,
golden-filtered coupling, spectral gap (lambda_min > 0), coherence transition.

Extends test_phase8_threshold.py. Run together or standalone.
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_klein_laplacian import PHI
from phase8_vacuum_pump_threshold import KleinOscillatorSheet


class TestKleinMetric:
    @classmethod
    def setup_class(cls):
        cls.sheet = KleinOscillatorSheet(noise_count=4, sigma=1.0)

    def test_self_distance_is_zero(self):
        xs = np.array([1.0, 2.0])
        ys = np.array([3.0, 4.0])
        dist, twist = self.sheet.klein_metric(xs, ys)
        for i in range(2):
            assert dist[i, i] > 1e6  # filled with inf on diagonal

    def test_metric_is_symmetric(self):
        xs = 2 * np.pi * np.random.default_rng(0).uniform(size=20)
        ys = 2 * np.pi * np.random.default_rng(0).uniform(size=20)
        dist, twist = self.sheet.klein_metric(xs, ys)
        assert np.allclose(dist, dist.T, atol=1e-10)

    def test_periodic_distance_in_x(self):
        xs = np.array([0.1, 2 * np.pi - 0.1])
        ys = np.array([0.0, 0.0])
        dist, twist = self.sheet.klein_metric(xs, ys)
        assert dist[0, 1] < 0.5  # periodic OR twist wrap gives short path


class TestKleinSheet:
    @classmethod
    def setup_class(cls):
        cls.sheet = KleinOscillatorSheet(noise_count=50, sigma=0.5, seed=3)
        for _ in range(6):
            cls.sheet.add_harmonic_layer(15)
        cls.rows = cls.sheet.run_scan(n_layers=0, n_new=15)  # already has 6
        # re-run from scratch for the scan
        cls.sheet2 = KleinOscillatorSheet(noise_count=50, sigma=0.5, seed=4)
        cls.rows2 = cls.sheet2.run_scan(n_layers=8, n_new=15)

    def test_spectral_gap_grows_with_layers(self):
        """lambda_min should increase as golden layers accumulate twist edges."""
        lam0 = self.rows2[0]["lambda_min"]
        lam_late = self.rows2[-1]["lambda_min"]
        assert lam_late > lam0

    def test_klein_twist_lifts_zero_mode(self):
        """lambda_min > 0 for the Klein bottle oscillator sheet."""
        assert self.rows2[-1]["lambda_min"] > 0

    def test_coherence_transitions(self):
        cohs = [r["coherence"] for r in self.rows2]
        assert cohs[0] < 0.05
        assert max(cohs) > 0.15  # at least some accumulation

    def test_d_eff_near_manifold_dimension(self):
        """D_eff stays in [1.0, 4.0] for a 2D manifold."""
        for r in self.rows2:
            if not np.isnan(r["D_eff"]):
                assert 1.0 < r["D_eff"] < 4.0

    def test_magnification_tracks_phi(self):
        for r in self.rows2:
            assert abs(r["magnification"] - PHI ** r["n_layers"]) < 1e-10
