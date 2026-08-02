"""
Unit tests for phase34_baryon_ladder.py -- IST Phase 34
=======================================================
The baryon mass ladder in units of E = hbar c / 1 fm. Verifies the decuplet
equal-spacing rule (spacing = (3/4)E), Delta - N = (3/2)E (the f_Klein
factor), N = (19/4)E, and the honest octet (weaker) relations.

Run: cd code && python -m pytest ../tests/test_phase34_baryon_ladder.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase34_baryon_ladder import (
    E, P, N, LAM, SIG, XI, DELTA, SIG_STAR, XI_STAR, OMEGA,
    nucleon_mass_pred, delta_minus_n, decuplet_spacing, decuplet_mass,
    octet_relations,
)


class TestEnergyQuantum:
    def test_E_is_hbar_c_per_fm(self):
        # hbar c = 197.3269804 MeV fm; E at l = 1 fm
        assert abs(E - 197.3269804) < 1e-6


class TestDecupletLadder:
    def test_nucleon_is_19_quarters_E(self):
        pred = nucleon_mass_pred()
        assert abs(pred / ((P + N) / 2) - 1) < 0.01        # 0.17%

    def test_delta_minus_N_is_3_over_2_E(self):
        # the f_Klein = 3/2 factor
        assert abs(delta_minus_n() - 1.5 * E) < 1e-9
        assert abs((DELTA - (P + N) / 2) / delta_minus_n() - 1) < 0.02

    def test_decuplet_spacing_is_3_quarters_E(self):
        assert abs(decuplet_spacing() - 0.75 * E) < 1e-9
        d_obs = (SIG_STAR - DELTA + XI_STAR - SIG_STAR
                 + OMEGA - XI_STAR) / 3.0
        assert abs(d_obs / decuplet_spacing() - 1) < 0.02

    def test_all_decuplet_masses(self):
        # m(S) = Delta + S d for S = 0,1,2,3
        for S, m in [(0, DELTA), (1, SIG_STAR), (2, XI_STAR), (3, OMEGA)]:
            pred = decuplet_mass(S)
            assert abs(pred / m - 1) < 0.01


class TestOctetHonest:
    def test_lambda_minus_N_consistent(self):
        o = octet_relations()
        assert abs(o["Lam_minus_N"] / o["pred_LamN"] - 1) < 0.02

    def test_xi_minus_N_consistent(self):
        o = octet_relations()
        assert abs(o["Xi_minus_N"] / o["pred_XiN"] - 1) < 0.05

    def test_octet_internal_splitting_not_clean(self):
        # Sig-Lam and Xi-Sig are not on the clean E-ladder (honest)
        sig_lam = SIG - LAM
        xi_sig = XI - SIG
        assert sig_lam > 0 and xi_sig > 0
        # and they are not equal to each other (no equal spacing in octet)
        assert abs(sig_lam - xi_sig) > 20.0


class TestSelfConsistency:
    def test_delta_consistent_with_ladder(self):
        # Delta = N + (3/2)E should be close to the anchor 1232
        pred_delta = nucleon_mass_pred() + delta_minus_n()
        assert abs(pred_delta / DELTA - 1) < 0.02
