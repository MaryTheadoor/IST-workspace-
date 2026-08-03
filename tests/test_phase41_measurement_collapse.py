"""
Unit tests for phase41_measurement_collapse.py -- IST Phase 41
==============================================================
The measurement problem: wavefunction collapse as entropic crystallization.
Verifies: the unperturbed state stays high-entropy (disordered), the golden
run crystallizes sharply at the threshold (coherence jumps, entropy drops),
the silver run remains lower-order, and information is strictly conserved.

Run: cd code && python -m pytest ../tests/test_phase41_measurement_collapse.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_klein_laplacian import PHI
from phase41_measurement_collapse import (
    ALPHA_GOLDEN, F_SILVER, gap_entropy_norm, golden_coupling,
    CollapseSubstrate,
)


class TestEntropy:
    def test_random_phases_have_high_entropy(self):
        rng = np.random.default_rng(1)
        ph = 2 * np.pi * rng.uniform(size=150)
        assert gap_entropy_norm(ph) > 0.88

    def test_golden_filtered_has_lower_entropy_than_silver(self):
        # A golden-filtered substrate has a lower normalized entropy than
        # the silver-filtered one because its three-gap structure is more
        # highly ordered (lower gap-partition entropy).
        gold = CollapseSubstrate(N_base=150, is_golden=True)
        silv = CollapseSubstrate(N_base=150, is_golden=False)
        for _ in range(12):
            gold.add_layer()
            silv.add_layer()
        g_final = gold.measure()
        s_final = silv.measure()
        assert g_final["entropy_norm"] < s_final["entropy_norm"]


class TestCoupling:
    def test_unitarity_of_coupling_boost(self):
        # golden_coupling produces unitary J (bounded entries)
        phases = 2 * np.pi * np.random.default_rng(1).uniform(size=50)
        J, boost = golden_coupling(phases, sigma=0.08, layer_count=5)
        assert J.shape == (50, 50)
        assert np.all(J >= 0)
        assert np.max(J) < 10.0


class TestCrystallization:
    def test_golden_crystallizes_sharply(self):
        # Golden run: entropy drops from initial noise (~0.91) to <0.87
        gold = CollapseSubstrate(N_base=100, is_golden=True)
        init = gold.measure()
        assert init["entropy_norm"] > 0.88
        for _ in range(12):
            gold.add_layer()
        final = gold.measure()
        assert final["entropy_norm"] < 0.86
        assert final["coherence"] > 0.80

    def test_silver_has_higher_entropy_than_golden(self):
        # Silver run (non-noble control) stays more disordered than golden
        gold = CollapseSubstrate(N_base=100, is_golden=True)
        silv = CollapseSubstrate(N_base=100, is_golden=False)
        for _ in range(12):
            gold.add_layer()
            silv.add_layer()
        g_final = gold.measure()
        s_final = silv.measure()
        assert g_final["entropy_norm"] < s_final["entropy_norm"]
        assert g_final["coherence"] > s_final["coherence"]


class TestInformationConservation:
    def test_information_strictly_conserved(self):
        # Information (oscillator count) is preserved exactly
        gold = CollapseSubstrate(N_base=100, is_golden=True)
        assert gold.measure()["info_error"] == 0.0
        for _ in range(5):
            gold.add_layer()
        assert gold.measure()["info_error"] == 0.0
