"""
Unit tests for phase37_force_harmonics.py -- IST Phase 37
=========================================================
Honest test of force unification as harmonic excitations. Verifies the
three formulations (fixed-scale ladder, beta-coefficient ladder, slaved
running) and the honest negative result: the couplings do NOT sit on a
clean golden harmonic ladder.

Run: cd code && python -m pytest ../tests/test_phase37_force_harmonics.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from ist_toolkit_v2 import PHI
from phase37_force_harmonics import (
    INV_EM, INV_WEAK, INV_STRONG, B1, B2, B3,
    coupling_ratios, golden_harmonics, best_harmonic_match, beta_ratios,
)


class TestCouplingRatios:
    def test_ratios_computed(self):
        r = coupling_ratios()
        assert abs(r["em_over_weak"] - INV_EM / INV_WEAK) < 1e-9
        assert abs(r["em_over_strong"] - INV_EM / INV_STRONG) < 1e-9


class TestGoldenHarmonics:
    def test_harmonics_values(self):
        h = golden_harmonics(6)
        assert abs(h["phi^1"] - PHI) < 1e-12
        assert abs(h["phi^2"] - PHI ** 2) < 1e-12
        assert abs(h["phi^6"] - PHI ** 6) < 1e-9


class TestBestMatch:
    def test_match_finds_nearest(self):
        h = golden_harmonics(6)
        name, val, pct = best_harmonic_match(PHI ** 2, h)
        assert name == "phi^2"
        assert abs(pct) < 1e-9


class TestHonestNegative:
    def test_em_weak_close_to_phi3(self):
        # the ONE ratio that is close
        r = coupling_ratios()
        assert abs(r["em_over_weak"] / PHI ** 3 - 1) < 0.05

    def test_weak_strong_not_harmonic(self):
        # weak/strong is far from any golden harmonic
        r = coupling_ratios()
        h = golden_harmonics(6)
        name, val, pct = best_harmonic_match(r["weak_over_strong"], h)
        assert abs(pct) > 10.0

    def test_beta_ladder_not_clean(self):
        # |b3|/|b1| ~ phi is within 6%, but the others are far
        b = beta_ratios()
        assert abs(b["|b3|/|b1|"] / PHI - 1) < 0.06
        h = golden_harmonics(6)
        name, val, pct = best_harmonic_match(b["|b2|/|b1|"], h)
        assert abs(pct) > 50.0

    def test_no_clean_ladder_overall(self):
        # across all coupling ratios, most are >5% from a harmonic
        r = coupling_ratios()
        h = golden_harmonics(6)
        near = 0
        for ratio in r.values():
            _, _, pct = best_harmonic_match(ratio, h)
            if abs(pct) < 5.0:
                near += 1
        assert near < 3            # not all ratios are near-harmonic
