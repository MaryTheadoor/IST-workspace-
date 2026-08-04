"""
Unit tests for phase45_baryon_octet.py -- IST Phase 45
=====================================================================
Tests the baryon octet Lambda-Sigma mixing as a golden partition: Sigma
splits the Lambda->Xi mass interval at 1/phi^2, closing the Phase 34 open
item. Encodes H45a-e (golden split, parameter-free prediction, GMO anchor,
robustness, decuplet contrast).

Run: cd code && python -m pytest ../tests/test_phase45_baryon_octet.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase45_baryon_octet import (
    PHI, LAM, SIG, XI, N_BAR,
    golden_split_fraction, gap_ratio, predict_sigma, predict_xi,
    gmo_octet, split_bas_specificity,
)


class TestGoldenSplit:
    def test_split_fraction_is_inverse_phi_squared(self):
        f, f_t, err = golden_split_fraction()
        assert abs(f_t - 1 / PHI ** 2) < 1e-12
        assert err < 0.002          # within 0.2%

    def test_gap_ratio_is_phi(self):
        r, r_t, err = gap_ratio()
        assert abs(r_t - PHI) < 1e-12
        assert err < 0.002          # within 0.2%

    def test_split_numeric(self):
        f, *_ = golden_split_fraction()
        assert 0.38 < f < 0.385


class TestPredictions:
    def test_sigma_predicted_from_lambda_xi(self):
        pred = predict_sigma()
        assert abs(pred / SIG - 1) < 5e-4      # 0.05%

    def test_xi_predicted_from_lambda_sigma(self):
        pred = predict_xi()
        assert abs(pred / XI - 1) < 5e-4       # 0.05%

    def test_prediction_consistency(self):
        # both predictions must be consistent with the observed masses
        assert abs(predict_sigma() - SIG) < 1.0
        assert abs(predict_xi() - XI) < 1.0


class TestGmoAnchor:
    def test_gmo_sum_rule(self):
        lhs, rhs, err = gmo_octet()
        assert err < 0.01            # 1%
        assert abs(lhs - rhs) < 10.0


class TestRobustness:
    def test_phi_in_basin(self):
        spec = split_bas_specificity()
        assert spec["b_star_inside"]

    def test_basin_is_narrow(self):
        # a 0.5% basin narrower than 0.01 in split-fraction units
        spec = split_bas_specificity()
        assert spec["width"] < 0.01

    def test_phi_uniquely_best_among_simple_fractions(self):
        # 1/phi^2 must beat 3/8, 0.38, 5/13, 8/21, 0.39, 0.4
        f = (SIG - LAM) / (XI - LAM)
        errs = [abs(f / (1 / PHI ** 2) - 1)]
        for q in (3 / 8, 0.38, 5 / 13, 8 / 21, 0.39, 0.4):
            errs.append(abs(f / q - 1))
        assert errs[0] == min(errs)


class TestOctetNotELadder:
    def test_octet_off_the_decuplet_ladder(self):
        # Phase 34 honest negative: octet coefficients are NOT
        # 4 + (2S+1)/2 * f_Klein for the decuplet's f = 3/2
        E = 197.3269804
        f_klein = 1.5
        coeffs = [N_BAR / E, LAM / E, SIG / E, XI / E]
        # decuplet ladder coefficients for S = 0..2: 19/4, 25/4, 7
        ladder = [4 + (2 * s + 1) / 2 * f_klein for s in range(3)]
        # N is on the ladder (19/4); Lam/Sig/Xi are not
        assert abs(coeffs[0] - ladder[0]) < 0.01
        assert all(abs(c - l) > 0.1 for c in coeffs[1:] for l in ladder)
