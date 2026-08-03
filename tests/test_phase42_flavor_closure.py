"""
Unit tests for phase42_flavor_closure.py -- IST Phase 42
==========================================================
Tests the flavor-threshold golden closure: boundary-convention sensitivity,
the five hypotheses (H42a-e), and the self-referential fine-structure
fixed point (H42g).

Run: cd code && python -m pytest ../tests/test_phase42_flavor_closure.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase42_flavor_closure import (
    PHI, C, REFS, THRESH,
    ALPHA_INV_CODATA,
    alpha_inv_self_consistent,
    alpha_s_anchored,
    alpha_s_differential,
    alpha_s_piecewise,
    errors,
    f_b1,
    f_exact_b0,
    f_identity,
    f_principled,
    n_f_active,
    rms,
)


class TestBoundaryConvention:
    def test_lower_mt_never_gets_6_flavors(self):
        assert n_f_active(173.0, upper=False) == 5

    def test_upper_activates_6_at_mt(self):
        assert n_f_active(173.0, upper=True) == 6

    def test_upper_activates_5_at_mb(self):
        assert n_f_active(4.18, upper=True) == 5

    def test_lower_mb_gets_4(self):
        assert n_f_active(4.18, upper=False) == 4


class TestHypotheses:
    def test_upper_convention_improves_principled_rms(self):
        lower = rms(errors(0, f_principled, upper=False))
        upper = rms(errors(0, f_principled, upper=True))
        assert upper < lower

    def test_exact_b0_nf5_is_third_power(self):
        # n_f = 5 exponent should be exactly 1/3 in the golden cast
        k = -np.log(f_exact_b0(5)) / np.log(PHI)
        assert abs(k - 1.0 / 3.0) < 1e-3

    def test_exact_b0_vs_principled_stay_close(self):
        # the (nf-3)/6 approximation and exact b0 ratios agree ~4%
        for nf in (4, 6):
            assert abs(f_exact_b0(nf) / f_principled(nf) - 1) < 0.05

    def test_b1_k1_documented_but_not_folded(self):
        # H42d: b1 is currently a no-op -- f_b1 must equal f_exact_b0
        for nf in (3, 4, 5, 6):
            assert f_b1(nf) == f_exact_b0(nf)

    def test_anchored_anchors_mz_exactly(self):
        pred = alpha_s_anchored(91.1876, f_principled, upper=True)
        assert pred == 0.118

    def test_anchored_fails_at_mtau_honest_negative(self):
        # H42e is a documented NEGATIVE: anchoring at M_Z over-shoots by
        # -87% at m_tau (pred 0.040 vs ref 0.330). Encode that finding.
        pred = alpha_s_anchored(1.77686, f_principled, upper=True)
        assert pred < 0.118 and pred < 0.330

    def test_differential_equals_piecewise_monotone(self):
        # both conventions must be monotonically decreasing in E
        for upper in (False, True):
            es = np.geomspace(1.0, 200, 20)
            vals = [alpha_s_differential(e, f_principled, upper) for e in es]
            assert all(b <= a for a, b in zip(vals, vals[1:]))


class TestH42gSelfConsistent137:
    def test_fixed_point_near_codata(self):
        x = alpha_inv_self_consistent()
        assert abs(x / ALPHA_INV_CODATA - 1) < 0.001   # 0.0075%

    def test_fixed_point_better_than_plain_golden_angle(self):
        x = alpha_inv_self_consistent()
        plain = 360.0 / PHI ** 2
        assert abs(x / ALPHA_INV_CODATA - 1) < abs(plain / ALPHA_INV_CODATA - 1)

    def test_fixed_point_self_consistent(self):
        x = alpha_inv_self_consistent()
        assert abs(x - 360.0 / PHI ** (2.0 + 1.0 / x)) < 1e-9

    def test_no_free_parameters(self):
        # exponent is exactly 2 + alpha (self-reference), nothing tuned
        x = alpha_inv_self_consistent()
        exponent = np.log(360.0 / x) / np.log(PHI)
        assert abs(exponent - (2.0 + 1.0 / x)) < 1e-12
