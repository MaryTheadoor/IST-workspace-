"""
Unit tests for phase50_light_quark_partition.py -- IST Phase 50
================================================================
Tests the honest negative: the bare light quarks do NOT obey the
Golden Partition that organizes the Baryon Octet bound states.

Run: cd code && python -m pytest ../tests/test_phase50_light_quark_partition.py -v
"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase50_light_quark_partition import (
    M_U, M_D, M_S, PHI,
    M_LAMBDA, M_SIGMA, M_XI,
)

class TestOctetReference:
    def test_octet_golden_partition_still_holds(self):
        # The baryon octet bound-state partition (Phase 45) is the reference
        split = (M_SIGMA - M_LAMBDA) / (M_XI - M_LAMBDA)
        assert abs(split - 1 / PHI**2) / (1 / PHI**2) < 0.01

class TestH50aBareQuarkPartition:
    def test_light_quarks_do_not_obey_golden_partition(self):
        # The bare quark gap ratio must NOT match 1/phi^2
        split = (M_D - M_U) / (M_S - M_U)
        assert abs(split - 1 / PHI**2) > 0.2  # >20% away

    def test_quark_split_is_small(self):
        # The d quark barely splits u->s (2.7%), unlike the hyperons (38%)
        split = (M_D - M_U) / (M_S - M_U)
        assert split < 0.1

class TestH50bRGInvariance:
    def test_split_is_scale_invariant(self):
        # Running all light quarks by the same factor leaves the ratio identical
        for factor in [1.0, 1.3, 1.54, 2.0]:
            s1 = (M_D - M_U) / (M_S - M_U)
            s2 = (M_D*factor - M_U*factor) / (M_S*factor - M_U*factor)
            assert np.isclose(s1, s2)

class TestH50cKoideSpace:
    def test_koide_space_also_fails(self):
        # The partition fails in sqrt(mass) space too
        sq_split = (np.sqrt(M_D) - np.sqrt(M_U)) / (np.sqrt(M_S) - np.sqrt(M_U))
        assert abs(sq_split - 1 / PHI**2) > 0.2
