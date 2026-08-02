"""
Unit tests for phase30_radiative_term.py -- IST Phase 30
========================================================
Derives the radiative (3/2)alpha correction from the same half-integer twist
theta = 1/2 that produced the leading factor-2 (Phase 29). Tests the
'unified derivation' claim.

Run: cd code && python -m pytest ../tests/test_phase30_radiative_term.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from ist_toolkit_v2 import PHI, ALPHA, M_PROTON, M_NEUTRON
from phase30_radiative_term import (
    theta_half_integer, f_klein_topological, xi_effective,
    delta_n_leading, triple_golden_suppression, c_radiative,
    delta_n_full, delta_n_observed, c_exact_from_masses,
)


class TestHalfIntegerTwist:
    def test_theta_is_half(self):
        assert theta_half_integer() == 0.5

    def test_f_klein_is_3_over_2(self):
        # f = 1 + |theta| = 1 + 1/2 = 3/2
        assert f_klein_topological() == 1.5


class TestUnifiedDerivation:
    def test_same_twist_gives_both_factors(self):
        # the 1/2 leading (Xi_eff = theta) and the 3/2 radiative (f = 1+theta)
        assert xi_effective() == theta_half_integer()
        assert f_klein_topological() == 1.0 + theta_half_integer()

    def test_leading_is_alpha_over_2phi2(self):
        assert abs(delta_n_leading() - ALPHA/(2*PHI**2)) < 1e-15


class TestTripleGoldenSuppression:
    def test_triple_suppression_is_1_over_phi6(self):
        # associator is a triple product; 3 pairings each 1/phi^2
        assert abs(triple_golden_suppression() - 1.0/PHI**6) < 1e-15

    def test_equals_cubed_pair_suppression(self):
        assert abs(triple_golden_suppression() - (1.0/PHI**2)**3) < 1e-15


class TestRadiativeCoefficient:
    def test_c_claims_fklein_minus_alpha_phi6(self):
        assert abs(c_radiative() - (1.5 - ALPHA/PHI**6)) < 1e-15

    def test_c_matches_exact_to_1e6(self):
        assert abs(c_radiative() - c_exact_from_masses()) < 1e-6


class TestFullForm:
    def test_full_delta_hits_neutron(self):
        d = delta_n_full()
        pred = M_PROTON * (1.0 + d)
        assert abs(pred - M_NEUTRON) / M_NEUTRON < 1e-8

    def test_full_form_within_observational_error(self):
        obs = delta_n_observed()
        u_rel = np.sqrt((5.7e-8)**2 + (1.4e-8)**2)
        sigma = abs(delta_n_full() - obs) / (obs * u_rel)
        assert sigma < 1.0

    def test_leading_term_needs_radiative_correction(self):
        # Without the radiative correction the leading term is 1.1% off
        obs = delta_n_observed()
        rel = abs(delta_n_leading() - obs) / obs
        assert 0.005 < rel < 0.02
