"""
Unit tests for phase33_master_equation_correction.py -- IST Phase 33
====================================================================
Generalized master equation: the associator term carries the twist
dependence (Xi_eff = theta, c = f - alpha/phi^6). Verifies the
generalization reduces to the original for orientable systems and fixes
the neutron, plus the electron factor-2 audit.

Run: cd code && python -m pytest ../tests/test_phase33_master_equation_correction.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from ist_toolkit_v2 import PHI, ALPHA, M_PLANCK, M_PROTON, M_ELECTRON, M_NEUTRON
from phase33_master_equation_correction import (
    xi_effective, c_radiative, f_topological, associator_term,
    delta_n_generalized, delta_n_observed, master_equation_orientable,
    electron_12pi5_decomposition, electron_ratio, proton_ratio,
    accuracy_percent,
)


class TestGeneralizedMasterEquation:
    def test_orientable_reduction(self):
        # theta=0: Xi_eff=1, f=1, c=0 => original (alpha/phi^2) Xi
        assert xi_effective(0.0) == 1.0
        assert f_topological(0.0) == 1.0
        assert c_radiative(1.0, theta=0.0) == 0.0
        assert abs(associator_term(ALPHA/PHI**2, 0.0)
                   - master_equation_orientable()) < 1e-15

    def test_non_orientable_theta_half(self):
        assert xi_effective(0.5) == 0.5
        assert f_topological(0.5) == 1.5
        assert abs(c_radiative(1.5, theta=0.5)
                   - (1.5 - ALPHA/PHI**6)) < 1e-15


class TestNeutronFixed:
    def test_generalized_neutron_at_codata(self):
        d = delta_n_generalized()
        pred = M_PROTON * (1.0 + d)
        assert abs(pred - M_NEUTRON) / M_NEUTRON < 1e-8

    def test_delta_within_observational_error(self):
        obs = delta_n_observed()
        u_rel = np.sqrt((5.7e-8)**2 + (1.4e-8)**2)
        sigma = abs(delta_n_generalized() - obs) / (obs * u_rel)
        assert sigma < 1.0


class TestOrientablePreserved:
    def test_proton_unchanged(self):
        pred = M_PLANCK / proton_ratio()
        assert accuracy_percent(pred, M_PROTON) > 99.9

    def test_electron_unchanged(self):
        pred = M_PLANCK / electron_ratio()
        assert accuracy_percent(pred, M_ELECTRON) > 99.9


class TestElectronFactor2Audit:
    def test_12pi5_decomposition(self):
        dec = electron_12pi5_decomposition()
        assert abs(dec["total"] - 12 * np.pi ** 5) < 1e-9
        assert dec["two"] * dec["six"] * dec["pi5"] == dec["total"]

    def test_electron_ratio_uses_12pi5(self):
        assert abs(electron_ratio() / ((12*np.pi**5/PHI**2)*ALPHA**(-9)) - 1) < 1e-12


class TestAssociatorTermContinuity:
    def test_term_continuous_in_theta(self):
        # The associator term is smooth in theta: at theta=0 it equals the
        # original (alpha/phi^2) Xi, and decreases to 0 at theta=1 (fully
        # twisted, no single-valued charge). The neutron sits at theta=1/2.
        t0 = associator_term(ALPHA/PHI**2, 0.0)
        t05 = associator_term(ALPHA/PHI**2, 0.5)
        t1 = associator_term(ALPHA/PHI**2, 1.0)
        assert t0 > t05 > t1                 # decreasing with twist
        assert abs(t0 - ALPHA/PHI**2) < 1e-15   # reduces at orientable
        assert abs(t1) < 1e-15               # vanishes fully twisted
