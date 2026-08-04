"""
Unit tests for phase49_proton_electron_ratio.py -- IST Phase 49
===============================================================
Tests the rigorous topological derivation of the 6pi^5 factor
in the proton/electron mass ratio.

Run: cd code && python -m pytest ../tests/test_phase49_proton_electron_ratio.py -v
"""

import os
import sys
import math
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase49_proton_electron_ratio import (
    sphere_volume,
    su_n_volume,
    M_P_MEV,
    M_E_MEV,
    OBSERVED_RATIO
)

class TestH49aTopologicalVolumes:
    def test_sphere_volumes_exact(self):
        # Vol(S^3) = 2pi^2
        assert np.isclose(sphere_volume(3), 2 * math.pi**2)
        # Vol(S^5) = pi^3
        assert np.isclose(sphere_volume(5), math.pi**3)
        
    def test_su_n_volumes_exact(self):
        # Vol(SU(2)) = Vol(S^3) = 2pi^2
        assert np.isclose(su_n_volume(2), 2 * math.pi**2)
        # Vol(SU(3)) = Vol(S^3) * Vol(S^5) = 2pi^5
        assert np.isclose(su_n_volume(3), 2 * math.pi**5)

class TestH49bMassRatioIdentity:
    def test_six_pi_five_matches_su3_formula(self):
        # 6pi^5 should be exactly 3 * Vol(SU(3))
        formula = 3 * su_n_volume(3)
        six_pi_five = 6 * math.pi**5
        assert np.isclose(formula, six_pi_five)
        
    def test_derived_ratio_matches_codata(self):
        derived = 3 * su_n_volume(3)
        # Verify it matches 99.9981%
        accuracy = 1.0 - abs(derived / OBSERVED_RATIO - 1.0)
        assert accuracy > 0.99998

class TestH49cAnomalyCancellation:
    def test_only_nc_3_matches_observed(self):
        for nc in [1, 2, 4, 5]:
            derived = nc * su_n_volume(3)
            error = abs(derived / OBSERVED_RATIO - 1.0)
            assert error > 0.3  # > 30% error for any other N_c
