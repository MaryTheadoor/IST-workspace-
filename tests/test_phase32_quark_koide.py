"""
Unit tests for phase32_quark_koide.py -- IST Phase 32
=====================================================
Quark-sector Koide test. Verifies: leptons at Q=2/3 (pi/2 phase), heavy
(c,b,t) consistent with 2/3 within pole-mass systematics, light/up/down
generations broken. The honest falsification mapping.

Run: cd code && python -m pytest ../tests/test_phase32_quark_koide.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase32_quark_koide import (
    M_U, M_D, M_S, M_C, M_B, M_T,
    koide_Q, koide_phase, triplet,
)


def koide(m):
    return koide_Q(m)


class TestCore:
    def test_leptons_at_two_thirds(self):
        Q = koide([0.51099895000, 105.6583755, 1776.86])
        assert abs(Q - 2 / 3) < 1e-4

    def test_phase_pi2_equivalence(self):
        assert abs(koide_phase(2 / 3) - np.pi / 2) < 1e-12


class TestHeavyTriplet:
    def test_cbt_consistent_with_two_thirds(self):
        # (c,b,t) Q = 0.6696, +0.45% -- within ~1% pole-mass systematics
        t = triplet("heavy (c,b,t)", [M_C, M_B, M_T])
        assert abs(t["pct_from_2_3"]) < 1.0        # consistent, not sharp

    def test_cbt_phase_near_pi2(self):
        t = triplet("heavy (c,b,t)", [M_C, M_B, M_T])
        assert abs(t["phase_dev_deg"]) < 2.0       # ~89.8 deg


class TestBrokenTriplets:
    def test_light_triplet_broken(self):
        t = triplet("light (u,d,s)", [M_U, M_D, M_S])
        assert abs(t["pct_from_2_3"]) > 5.0        # -15%

    def test_uptype_broken(self):
        t = triplet("up-type (u,c,t)", [M_U, M_C, M_T])
        assert abs(t["pct_from_2_3"]) > 10.0       # +27%

    def test_downtype_broken(self):
        t = triplet("down-type (d,s,b)", [M_D, M_S, M_B])
        assert abs(t["pct_from_2_3"]) > 5.0        # +9.7%


class TestMapping:
    def test_exactly_one_koide_valid_quark_generation(self):
        # Among the quark triplets, only (c,b,t) is consistent with 2/3
        heavy = triplet("heavy", [M_C, M_B, M_T])
        light = triplet("light", [M_U, M_D, M_S])
        up = triplet("up", [M_U, M_C, M_T])
        down = triplet("down", [M_D, M_S, M_B])
        assert abs(heavy["pct_from_2_3"]) < 1.0
        assert abs(light["pct_from_2_3"]) > 5.0
        assert abs(up["pct_from_2_3"]) > 5.0
        assert abs(down["pct_from_2_3"]) > 5.0

    def test_heavy_deviation_within_pole_mass_uncertainty(self):
        # 2/3 is just outside the pole-mass band (0.34-0.59% above 2/3),
        # so the heavy triplet is CONSISTENT, not confirmed. Verify the
        # deviation is < 1% (the nominal pole-mass systematic scale).
        t = triplet("heavy (c,b,t)", [M_C, M_B, M_T])
        assert abs(t["pct_from_2_3"]) < 1.0
