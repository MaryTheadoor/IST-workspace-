"""
Unit tests for phase38_mass_coupling.py -- IST Phase 38
=======================================================
Tests the mass->coupling relation (Insight B): couplings as slaved running
between golden mass harmonics. Verifies the strong-coupling mass->coupling
relation works, and the per-force ladder is partial (honest).

Run: cd code && python -m pytest ../tests/test_phase38_mass_coupling.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from ist_toolkit_v2 import PHI, ALPHA
from phase38_mass_coupling import (
    M_P, PHI4, C_ASSOC, ALPHA_EM_MZ, ALPHA_W_MZ, ALPHA_S_MZ,
    n_layers, alpha_s_from_layers, c_normalization, k_golden_power,
)


class TestLayers:
    def test_n_layers_zero_at_proton(self):
        assert abs(n_layers(M_P)) < 1e-9

    def test_n_layers_increases_with_E(self):
        assert n_layers(91.1876) > n_layers(1.0)


class TestStrongMassCoupling:
    def test_alpha_s_at_MZ_within_5pct(self):
        pred = alpha_s_from_layers(91.1876)
        assert abs(pred / 0.118 - 1) < 0.05

    def test_alpha_s_at_mtau_within_5pct(self):
        pred = alpha_s_from_layers(1.77686)
        assert abs(pred / 0.33 - 1) < 0.05

    def test_uses_associator_normalization(self):
        # C = 1/phi^2 by default
        assert abs(C_ASSOC - 1 / PHI ** 2) < 1e-12

    def test_alpha_s_decreases_with_energy(self):
        assert alpha_s_from_layers(173.0) < alpha_s_from_layers(4.18)


class TestNormalizationLadder:
    def test_c_strong_near_associator(self):
        # C_s = 0.3705 vs 1/phi^2 = 0.3820 (within 4%)
        C_s = c_normalization(ALPHA_S_MZ, 91.1876)
        assert abs(C_s / (1 / PHI ** 2) - 1) < 0.04

    def test_k_increases_with_force_strength(self):
        C_em = c_normalization(ALPHA_EM_MZ, 91.1876)
        C_w = c_normalization(ALPHA_W_MZ, 91.1876)
        C_s = c_normalization(ALPHA_S_MZ, 91.1876)
        k_em, k_w, k_s = (k_golden_power(C) for C in (C_em, C_w, C_s))
        assert k_em < k_w < k_s

    def test_ladder_gaps_not_uniform(self):
        # honest: the gaps (2.6, 3.0) are not equal golden steps
        Cs = [c_normalization(a, 91.1876)
              for a in (ALPHA_EM_MZ, ALPHA_W_MZ, ALPHA_S_MZ)]
        ks = [k_golden_power(C) for C in Cs]
        gaps = [ks[1] - ks[0], ks[2] - ks[1]]
        assert abs(gaps[0] - gaps[1]) > 0.2    # not uniform


class TestGoldenSpan:
    def test_total_span_alpha_to_alpha_s(self):
        span = np.log(ALPHA_S_MZ / ALPHA_EM_MZ) / np.log(PHI)
        assert 5.0 < span < 6.5
