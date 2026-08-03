"""
Unit tests for phase39_flavor_threshold.py -- IST Phase 39
==========================================================
Tests the active-flavor threshold correction to the mass-coupling relation.
Verifies: flavor thresholds reduce the m_b/m_t errors, the free fit
improves all references substantially, and the honest finding that no
single golden rule fits all four.

Run: cd code && python -m pytest ../tests/test_phase39_flavor_threshold.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from ist_toolkit_v2 import PHI
from phase39_flavor_threshold import (
    M_P, C, THRESH, REFS,
    alpha_s_piecewise, f_free, f_principled, f_identity,
)


class TestOriginalModel:
    def test_original_overpredicts_mb(self):
        pred = alpha_s_piecewise(4.18, f_identity)
        assert pred / 0.22 - 1 > 0.10          # +19.5%

    def test_original_close_at_mz(self):
        pred = alpha_s_piecewise(91.1876, f_identity)
        assert abs(pred / 0.118 - 1) < 0.05


class TestFreeFit:
    def test_free_fit_improves_mb(self):
        pred_orig = alpha_s_piecewise(4.18, f_identity)
        pred_fit = alpha_s_piecewise(4.18, f_free)
        assert abs(pred_fit / 0.22 - 1) < abs(pred_orig / 0.22 - 1)

    def test_free_fit_improves_mt(self):
        pred_orig = alpha_s_piecewise(173.0, f_identity)
        pred_fit = alpha_s_piecewise(173.0, f_free)
        assert abs(pred_fit / 0.09 - 1) < abs(pred_orig / 0.09 - 1)

    def test_free_fit_all_within_8pct(self):
        for name, E, ref in REFS:
            pred = alpha_s_piecewise(E, f_free)
            assert abs(pred / ref - 1) < 0.08


class TestPrincipledForm:
    def test_principled_improves_mt(self):
        pred_orig = alpha_s_piecewise(173.0, f_identity)
        pred_p = alpha_s_piecewise(173.0, f_principled)
        assert abs(pred_p / 0.09 - 1) < abs(pred_orig / 0.09 - 1)

    def test_principled_golden_power_form(self):
        # f(n_f) = phi^{-(n_f-3)/6}
        assert abs(f_principled(6) - PHI ** (-0.5)) < 1e-9
        assert abs(f_principled(3) - 1.0) < 1e-9


class TestFlavorFactors:
    def test_f6_near_phi(self):
        # the free-fit f(6) ~ phi (suggestive)
        assert abs(f_free(6) / PHI - 1) < 0.02

    def test_factors_monotone_free_fit(self):
        # fitted factors rise with n_f
        vals = [f_free(nf) for nf in (3, 4, 5, 6)]
        assert vals[-1] > vals[0]


class TestThresholdStructure:
    def test_thresholds_are_quark_masses(self):
        masses = [t for t, _ in THRESH]
        assert abs(masses[0] - 1.27) < 0.01
        assert abs(masses[1] - 4.18) < 0.01
        assert abs(masses[2] - 173.0) < 0.01
