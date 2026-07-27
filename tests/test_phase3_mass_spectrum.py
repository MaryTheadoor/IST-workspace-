"""
Unit tests for phase3_mass_spectrum.py -- IST Phase 3
======================================================
Mass hierarchy predictions (proton, electron, neutron), strong coupling from
the associator, and neutrino tunneling mass estimates.

Run: cd code && python -m pytest ../tests/test_phase3_mass_spectrum.py -v
"""

import sys
import os

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase3_mass_spectrum import (
    proton_ratio, electron_ratio, neutron_ratio_plan_literal,
    neutron_from_proton, best_delta_n_for_neutron,
    predicted_mass, accuracy_percent,
    associator_magnitude_fixed_point, alpha_s_associator,
    neutrino_mass_eV, required_tunneling_probability,
    M_planck_eV,
)
from ist_toolkit_v2 import M_PLANCK, M_PROTON, M_ELECTRON, M_NEUTRON, ALPHA, PHI


# ── Mass Formulas ─────────────────────────────────────────────────────────────

class TestMassFormulas:
    def test_proton_accuracy(self):
        pred = predicted_mass(proton_ratio())
        assert accuracy_percent(pred, M_PROTON) > 99.9

    def test_electron_accuracy(self):
        pred = predicted_mass(electron_ratio())
        assert accuracy_percent(pred, M_ELECTRON) > 99.9

    def test_electron_to_proton_ratio(self):
        # m_p / m_e = 6 pi^5 in the IST formula
        ratio_pred = electron_ratio() / proton_ratio()
        assert abs(ratio_pred - 6 * np.pi ** 5) < 1e-9

    def test_neutron_from_proton_with_plan_delta(self):
        pred = neutron_from_proton(ALPHA / PHI ** 2)
        assert accuracy_percent(pred, M_NEUTRON) > 99.8

    def test_neutron_best_fit_delta_is_positive(self):
        delta = best_delta_n_for_neutron()
        assert 0 < delta < ALPHA / PHI ** 2

    def test_neutron_plan_literal_has_wrong_sign(self):
        # The literal plan form predicts a neutron lighter than the proton,
        # which is incorrect. We document this as a sign tension.
        pred = predicted_mass(neutron_ratio_plan_literal())
        assert pred < M_PROTON


# ── Strong Coupling from Associator ───────────────────────────────────────────

class TestStrongCoupling:
    def test_associator_fixed_point_magnitude(self):
        assert abs(associator_magnitude_fixed_point() - 1.0 / PHI ** 2) < 1e-12

    def test_alpha_s_decreases_with_energy(self):
        # Asymptotic freedom: alpha_s drops as energy increases above M_Z
        low = alpha_s_associator(100.0)
        high = alpha_s_associator(10000.0)
        assert high < low

    def test_alpha_s_fitted_at_reference(self):
        assert abs(alpha_s_associator(91.1876) - 0.118) < 1e-12

    def test_fixed_point_exceeds_observed_at_mz(self):
        # The topological fixed-point normalization gives alpha_s(M_Z) ~ 0.38,
        # about 3x larger than observed -- a tension to document.
        assert alpha_s_associator(91.1876, use_fixed_point=True) > 0.3


# ── Neutrino Tunneling ────────────────────────────────────────────────────────

class TestNeutrinoTunneling:
    def test_mass_scales_linearly_with_probability(self):
        assert abs(neutrino_mass_eV(1e-30) - 1e-30 * M_planck_eV()) < 1e-12

    def test_required_probability_is_extremely_small(self):
        P_req = required_tunneling_probability()
        assert P_req < 1e-25
        assert P_req < ALPHA / PHI ** 2

    def test_required_probability_reproduces_observed_scale(self):
        P_req = required_tunneling_probability(0.05)
        assert abs(neutrino_mass_eV(P_req) - 0.05) < 1e-15
