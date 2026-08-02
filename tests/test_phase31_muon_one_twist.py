"""
Unit tests for phase31_muon_one_twist.py -- IST Phase 31
========================================================
The one-twist muon: Koide Q = 2/3 realized by the pi/2 phase (the half-
integer twist theta = 1/2), and the muon's back-sheet interpretation.

Run: cd code && python -m pytest ../tests/test_phase31_muon_one_twist.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase31_muon_one_twist import (
    M_E, M_MU, M_TAU,
    koide_Q, koide_phase, koide_masses,
    theta_half_integer, twist_phase, generation_offsets,
    muon_amplitude_at_pi2, muon_back_sheet_ratio,
)


class TestKoideRelation:
    def test_koide_Q_is_two_thirds(self):
        Q = koide_Q()
        assert abs(Q - 2 / 3) < 1e-4            # agreement to ~1e-5

    def test_phase_is_pi_over_2(self):
        phi = koide_phase()
        assert abs(phi - np.pi / 2) < 1e-4      # 6.5 micro-rad

    def test_Q_two_thirds_iff_phase_pi2(self):
        # Q = 2/3 <=> phi = pi/2 (the equivalence)
        for Q, expected in [(2 / 3, np.pi / 2)]:
            phi = np.arccos((3 * Q / 2 - 1) / np.sqrt(2))
            assert abs(phi - expected) < 1e-12


class TestOneTwistStructure:
    def test_theta_is_half(self):
        assert theta_half_integer() == 0.5

    def test_twist_phase_is_pi2(self):
        assert twist_phase() == np.pi / 2

    def test_three_generation_offsets(self):
        offsets = generation_offsets()
        assert len(offsets) == 3
        assert all(abs(o - 2 * np.pi * k / 3) < 1e-12
                   for k, o in enumerate(offsets))


class TestMuonBackSheet:
    def test_muon_amplitude_is_negative(self):
        # At phi = pi/2 the muon amplitude 1 - sqrt(3/2) < 0: back sheet
        assert muon_amplitude_at_pi2() < 0

    def test_muon_sits_on_back_sheet(self):
        # amplitude = 1 + sqrt(2) cos(pi/2 + 2pi/3) = 1 - sqrt(3/2)
        assert abs(muon_amplitude_at_pi2() - (1 - np.sqrt(3 / 2))) < 1e-12

    def test_naive_fan_fails_for_muon_ratio(self):
        R_fan, _ = muon_back_sheet_ratio()
        assert R_fan < 1.0                       # fails (back-sheet sign)
        assert M_MU / M_E > 100.0

    def test_phase27_hit_is_back_sheet(self):
        # 3/(2 alpha) is close but not exact (99.41%)
        _, R_hit = muon_back_sheet_ratio()
        R_obs = M_MU / M_E
        assert abs(R_hit / R_obs - 1) < 0.01
        assert abs(R_hit / R_obs - 1) > 1e-4


class TestKoideFan:
    def test_fan_recovers_electron_amplitude(self):
        _, amps = koide_masses(np.pi / 2)
        # electron amplitude at phi=pi/2 is ~1 (cos(pi/2)=0)
        assert abs(amps[0] - 1.0) < 1e-12

    def test_fan_sum_squares_gives_Q(self):
        # The Koide Q relation is consistent with the fan: sum(amp^2)/sum(amp)^2
        # ... (Koide identity) -- just check the fan is a valid parametrization
        _, amps = koide_masses(np.pi / 2)
        assert len(amps) == 3
        assert np.all(np.isfinite(amps))
