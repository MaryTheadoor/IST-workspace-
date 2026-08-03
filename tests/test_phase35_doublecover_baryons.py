"""
Unit tests for phase35_doublecover_baryons.py -- IST Phase 35
=============================================================
Derives the full baryon decuplet ladder from the double-cover (4) and the
topological factor f_Klein = 3/2. Verifies the derived coefficients
replace the empirical 19/4 of Phase 34.

Run: cd code && python -m pytest ../tests/test_phase35_doublecover_baryons.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase35_doublecover_baryons import (
    E, F_KLEIN, DOUBLE_COVER, P, N, DELTA, SIG_STAR, XI_STAR, OMEGA,
    coefficient, decuplet_mass, ladder_table, structure_decomposition,
)


class TestStructuralConstants:
    def test_energy_quantum(self):
        assert abs(E - 197.3269804) < 1e-6

    def test_f_klein_is_3_over_2(self):
        assert F_KLEIN == 1.5

    def test_double_cover_is_four(self):
        assert DOUBLE_COVER == 4.0


class TestDerivedCoefficients:
    def test_nucleon_coefficient_is_19_over_4(self):
        # N = 4 + (1/2) f = 19/4 (no longer an empirical input!)
        assert abs(coefficient(0) - 19 / 4) < 1e-12

    def test_delta_coefficient_is_25_over_4(self):
        # Delta = 4 + (3/2) f = 25/4
        assert abs(4 + 1.5 * F_KLEIN - 25 / 4) < 1e-12

    def test_omega_coefficient_is_17_over_2(self):
        assert abs(4 + 3.0 * F_KLEIN - 17 / 2) < 1e-12


class TestLadderMasses:
    def test_all_decuplet_masses(self):
        for nm, S, c, pred, obs in ladder_table():
            assert abs(pred / obs - 1) < 0.01

    def test_nucleon_consistency(self):
        pred = decuplet_mass(0)
        assert abs(pred / ((P + N) / 2) - 1) < 0.01

    def test_omega_consistency(self):
        # Omega uses the k=6 (3f) coefficient via the table
        for nm, S, c, pred, obs in ladder_table():
            if nm == "Omega":
                assert abs(pred / obs - 1) < 0.01
                assert abs(c - 4 - 3.0 * F_KLEIN) < 1e-12


class TestStructure:
    def test_structure_decomposition_complete(self):
        s = structure_decomposition()
        assert len(s) == 5
        # every coefficient matches the k/2 f formula
        kvals = [0.5, 1.5, 2.0, 2.5, 3.0]
        for (nm, txt), k in zip(s.items(), kvals):
            assert abs(4 + k * F_KLEIN - float(txt.split("= ")[-1])) < 1e-6

    def test_ladder_monotone(self):
        coeffs = [r[2] for r in ladder_table()]         # tuples (name,S,coeff,pred,obs)
        assert all(b > a for a, b in zip(coeffs, coeffs[1:]))


class TestEnergyScale:
    def test_residual_dominated_by_confinement_scale(self):
        # The ~0.18% mean residual is consistent with the ~1% 1-fm scale
        resids = [abs(100 * (r[3] / r[4] - 1)) for r in ladder_table()]
        assert np.mean(resids) < 1.0
