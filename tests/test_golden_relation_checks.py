"""
Unit tests for golden_relation_checks.py -- IST robustness methodology
========================================================================
Encodes the four robustness checks (uniqueness, base-specificity,
unit-invariance, exponent-freedom) learned from the Phase 42 H42g
cross-analysis, applied to the H42g fixed point and the flavor closure.

Honest finding these tests lock in: H42g's 0.0075% agreement is REAL as a
fixed point but does NOT survive the methodology checks -- it is non-unique
(two roots), unit-fragile (deg vs rad), base-unspecific (0.09% band of
bases), and exponent-free (14 k values fit). The flavor closure likewise
prefers a base 0.99% above phi.

Run: cd code && python -m pytest ../tests/test_golden_relation_checks.py -v
"""

import os
import sys

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from golden_relation_checks import base_specificity, fixed_point_roots, unit_robustness
from phase42_flavor_closure import REFS, THRESH, M_P, ALPHA_INV_CODATA, PHI


def h42g_fixed_point(circle=360.0, base=PHI, exponent=2.0):
    x = 137.0
    for _ in range(200):
        x = circle / base ** (exponent + 1.0 / x)
    return x


class TestUniqueness:
    def test_h42g_has_two_roots(self):
        # G1: the equation x = 360/phi^(2+1/x) has TWO roots
        roots = fixed_point_roots(lambda x: 360.0 / PHI ** (2.0 + 1.0 / x),
                                  lo=1e-2, hi=300.0)
        assert len(roots) == 2
        assert any(r < 1.0 for r in roots)       # the spurious root ~0.06
        assert any(abs(r - 137.0) < 1.0 for r in roots)  # the physical root

    def test_physical_root_near_codata(self):
        roots = fixed_point_roots(lambda x: 360.0 / PHI ** (2.0 + 1.0 / x),
                                  lo=1e-2, hi=300.0)
        phys = max(roots)
        assert abs(phys / ALPHA_INV_CODATA - 1) < 0.001


class TestBaseSpecificity:
    def test_h42g_base_basin_wide(self):
        # G2: any base in a ~0.09% band fits <0.1% -- phi NOT uniquely selected
        def err(b):
            return abs(h42g_fixed_point(base=b) / ALPHA_INV_CODATA - 1.0)
        res = base_specificity(err, PHI, threshold=1e-3,
                               lo=1.55, hi=1.70, n=4001)
        assert res["width"] > 1e-3          # basin is a BAND, not a spike
        assert res["b_star_inside"]          # phi inside, but so is the band
        assert res["min_error_b"] != PHI     # the BEST base is not phi

    def test_h42g_min_error_better_than_phi(self):
        def err(b):
            return abs(h42g_fixed_point(base=b) / ALPHA_INV_CODATA - 1.0)
        res = base_specificity(err, PHI, threshold=1e-3,
                               lo=1.55, hi=1.70, n=4001)
        # a nearby base fits BETTER than phi -> phi is not special
        assert res["min_error"] < res["b_star_error"]


class TestUnitInvariance:
    def test_h42g_unit_fragile(self):
        # G3: degrees -> 137, radians -> 1.85. NOT unit-invariant.
        deg = h42g_fixed_point(circle=360.0)
        rad = h42g_fixed_point(circle=2 * np.pi)
        assert abs(deg / ALPHA_INV_CODATA - 1) < 0.001   # deg works
        assert rad < 5.0                                  # rad does NOT


class TestExponentFreedom:
    def test_h42g_many_exponents_fit(self):
        # G4: 14 exponents in [1.5,2.5] reach <0.01% with some base
        def phys_root(b, k):
            try:
                return brentq(lambda x: x - 360.0 / b ** (k + 1.0 / x), 100, 200)
            except Exception:
                return None
        hits = 0
        for k in np.linspace(1.5, 2.5, 41):
            best = 1e9
            for b in np.linspace(1.55, 1.70, 601):
                r = phys_root(b, k)
                if r is not None:
                    best = min(best, abs(r / ALPHA_INV_CODATA - 1.0))
            if best < 1e-4:
                hits += 1
        assert hits >= 5


class TestFlavorClosure:
    def test_flavor_closure_prefers_base_above_phi(self):
        # G5: the principled flavor closure's optimal base is ~1.634,
        # 0.99% ABOVE phi -- even the strong-closure claim does not
        # uniquely select phi.
        def alpha_s(E, f, B):
            a = 1.0 / B ** 2
            prev = M_P
            for t, nf in THRESH:
                if E <= t:
                    break
                a *= B ** (-np.log(t / prev) / np.log(B ** 4 * f(nf, B)))
                prev = t
            if E > prev:
                nf = sum(1 for t, _ in THRESH if t <= E) + 3
                a *= B ** (-np.log(E / prev) / np.log(B ** 4 * f(nf, B)))
            return a

        def f_prin(nf, B):
            return B ** (-(nf - 3) / 6.0)

        def rms(b):
            errs = {nm: 100.0 * (alpha_s(E, f_prin, b) / ref - 1.0)
                    for nm, E, ref in REFS}
            return np.sqrt(np.mean([v ** 2 for v in errs.values()]))

        bs = np.linspace(1.55, 1.72, 2001)
        i = np.array([rms(b) for b in bs]).argmin()
        assert bs[i] > PHI
