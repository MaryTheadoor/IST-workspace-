"""
Unit tests for phase29_factor2_derivation.py -- IST Phase 29
============================================================
Derives the factor-2 neutron correction from the half-integer Klein meridian
quantization. Tests each link in the derivation chain.

Run: cd code && python -m pytest ../tests/test_phase29_factor2_derivation.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from ist_toolkit_v2 import PHI, ALPHA, M_PROTON, M_NEUTRON
from phase29_factor2_derivation import (
    klein_meridian_momentum_half_integer, klein_spectrum_odd_l,
    flat_holonomy_is_minus_I, two_seam_crossings_per_cycle,
    xi_effective, delta_n_leading_derived, c_radiative,
    delta_n_full_derived, delta_n_observed,
)


class TestHalfIntegerQuantization:
    def test_meridian_momentum_is_halved(self):
        kq, tq, ratio = klein_meridian_momentum_half_integer()
        assert ratio == 0.5                     # pi vs 2*pi

    def test_klein_numeric_matches_analytic_odd_l(self):
        # The lowest numeric Klein eigenvalue must be the odd-l (l=1) mode.
        # (Higher modes pick up standing-wave pairing so we check the ground
        # state, which is the structural claim of half-integer quantization.)
        n = 48
        num, _ = klein_spectrum_odd_l(n=n, k=4)
        odd_l_min = 4 - 2*np.cos(2*np.pi*0/n) - 2*np.cos(np.pi*1/n)
        assert abs(num[0] - odd_l_min) < 1e-6
        assert abs(num[1] - odd_l_min) < 1e-6     # degenerate pair

    def test_klein_gap_is_the_odd_l_mode(self):
        # lambda_min = 4 - 2cos(2pi*0/n) - 2cos(pi*1/n) = 2 - 2cos(pi/n)
        # (p=0, l=1; the l=0 and even-l modes are excluded by the seam)
        n = 48
        an_min = 2 - 2*np.cos(np.pi/n)
        num, an = klein_spectrum_odd_l(n=n, k=1)
        assert abs(num[0] - an_min) < 1e-6
        assert abs(an_min - 4*np.sin(np.pi/(2*n))**2) < 1e-12


class TestDoubleCover:
    def test_flat_holonomy_is_exact_minus_I(self):
        assert flat_holonomy_is_minus_I(n=48) < 1e-12

    def test_exactly_two_seam_crossings(self):
        assert two_seam_crossings_per_cycle() == [1, 3]


class TestXiEffective:
    def test_xi_effective_is_half(self):
        assert xi_effective() == 0.5

    def test_leading_delta_is_alpha_over_2phi2(self):
        assert abs(delta_n_leading_derived() - ALPHA/(2*PHI**2)) < 1e-15


class TestFullForm:
    def test_radiative_coefficient_close_to_3_2(self):
        assert abs(c_radiative() - 1.5) < 1e-3   # tiny alpha/phi^6 refinement

    def test_full_form_hits_neutron(self):
        d = delta_n_full_derived()
        pred = M_PROTON * (1.0 + d)
        assert abs(pred - M_NEUTRON) / M_NEUTRON < 1e-8

    def test_full_form_within_observational_error(self):
        obs = delta_n_observed()
        u_rel = np.sqrt((5.7e-8)**2 + (1.4e-8)**2)
        sigma = abs(delta_n_full_derived() - obs) / (obs * u_rel)
        assert sigma < 1.0

    def test_derived_leading_beats_naive(self):
        naive = ALPHA / PHI ** 2
        led = delta_n_leading_derived()
        obs = delta_n_observed()
        # derived leading is ~2x closer than naive
        assert abs(led - obs) < abs(naive - obs) / 2.0
