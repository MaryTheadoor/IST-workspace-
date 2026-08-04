"""
Unit tests for phase53_heavy_flavor_octet.py -- IST Phase 53
=====================================================================
Tests the honest negative: the Phase 45 golden partition of the light
octet does NOT extend to the charmed/bottom SU(3) analog triplets.
Encodes H53a (charm fails), H53b (bottom fails, ordering inverted),
and the light-octet anchor still passing.

Run: cd code && python -m pytest ../tests/test_phase53_heavy_flavor_octet.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase53_heavy_flavor_octet import (
    PHI, INV_PHI2,
    LAM_C, SIG_C, XI_C, LAM_B, SIG_B, XI_B,
    flavor_splits, flavor_gaps, ordering,
)


class TestLightAnchor:
    def test_light_split_is_golden(self):
        # the Phase 45 anchor must still pass inside this module's frame
        s, _, t = flavor_splits()["light"]
        assert abs(t - INV_PHI2) < 1e-12
        assert abs(s / t - 1) < 0.002

    def test_light_gap_is_golden(self):
        g, _, t = flavor_gaps()["light"]
        assert abs(t - PHI) < 1e-12
        assert abs(g / t - 1) < 0.002


class TestCharmNegative:
    def test_charm_split_far_off_golden(self):
        s, ss, t = flavor_splits()["charm"]
        assert abs(t - INV_PHI2) < 1e-12
        # >100% off the golden target
        assert abs(s / t - 1) > 1.0
        # and off by many sigma (not an uncertainty artifact)
        assert abs(s - t) / ss > 50

    def test_charm_gap_far_off_golden(self):
        g, gs, t = flavor_gaps()["charm"]
        assert abs(t - PHI) < 1e-12
        assert abs(g / t - 1) > 0.5
        assert abs(g - t) / gs > 50

    def test_charm_ordering_normal(self):
        # Lambda_c < Sigma_c < Xi_c holds, so the failure is not an ordering artifact
        assert LAM_C < SIG_C < XI_C
        assert "INVERTED" not in ordering("charm")


class TestBottomNegative:
    def test_bottom_split_far_off_golden(self):
        s, ss, t = flavor_splits()["bottom"]
        assert abs(s / t - 1) > 1.5
        assert abs(s - t) / ss > 50

    def test_bottom_gap_negative(self):
        # the Xi_b - Sigma_b gap is NEGATIVE (Sigma_b above Xi_b)
        g, _, t = flavor_gaps()["bottom"]
        assert g < 0
        assert abs(g / t - 1) > 1.0

    def test_bottom_ordering_inverted(self):
        # Lambda_b < Xi_b < Sigma_b -- the SU(3) hierarchy flips in bottom
        assert LAM_B < XI_B < SIG_B
        assert "INVERTED" in ordering("bottom")


class TestInterpretation:
    def test_only_light_obeys(self):
        for fl in ("light", "charm", "bottom"):
            s, ss, st = flavor_splits()[fl]
            g, gs, gt = flavor_gaps()[fl]
            obeys = abs(s / st - 1) < 0.002 and abs(g / gt - 1) < 0.002
            assert obeys == (fl == "light")

    def test_mass_ratios_self_consistent(self):
        # internal consistency: split and gap derive from the same masses
        s_c, _, _ = flavor_splits()["charm"]
        g_c, _, _ = flavor_gaps()["charm"]
        assert abs(s_c - (SIG_C - LAM_C) / (XI_C - LAM_C)) < 1e-12
        assert abs(g_c - (XI_C - SIG_C) / (SIG_C - LAM_C)) < 1e-12
