"""
Unit tests for phase27_qm_ratio_validation.py -- IST Phase 27
==============================================================
Top-down QM-scale ratio validation. Tests the parameter-free predictions
(m_p/m_e = 6 pi^5), the geometric alpha identity, the neutron delta forms,
the muon candidate, and the Planck-anchored bottom-up cross-checks.

Run: cd code && python -m pytest ../tests/test_phase27_qm_ratio_validation.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from ist_toolkit_v2 import (
    ALPHA, M_PROTON, M_ELECTRON, M_NEUTRON, M_PLANCK,
)
from phase27_qm_ratio_validation import (
    PHI, M_MUON,
    m_p_over_m_e_6pi5, alpha_geometric,
    delta_n_naive, delta_n_half, delta_n_observed, running_phi_neutron,
    m_mu_over_m_e, m_mu_candidate_3_over_2alpha,
    proton_mass_planck, electron_mass_planck, neutron_mass_running_phi,
    residual_percent, accuracy_percent,
)


# ── Tier 1: parameter-free ────────────────────────────────────────────────────

class TestTier1ParameterFree:
    def test_m_p_over_m_e_is_6pi5(self):
        assert abs(m_p_over_m_e_6pi5() - 6.0 * np.pi ** 5) < 1e-12

    def test_m_p_over_m_e_matches_observation(self):
        pred = m_p_over_m_e_6pi5()
        obs = M_PROTON / M_ELECTRON
        assert accuracy_percent(pred, obs) > 99.9

    def test_alpha_geometric_is_identity(self):
        # alpha = r_e / lbar_C is exact by definition
        assert abs(alpha_geometric() / ALPHA - 1.0) < 1e-6


# ── Tier 2: minimally-parameterized ──────────────────────────────────────────

class TestTier2Neutron:
    def test_naive_delta_overshoots(self):
        # Plan's literal alpha/phi^2 overshoots the observed neutron excess
        assert delta_n_naive() / delta_n_observed() > 1.8

    def test_factor2_delta_lands_on_neutron(self):
        # alpha/(2 phi^2) reproduces m_n to better than 99.99%
        pred = M_PROTON * (1.0 + delta_n_half())
        assert accuracy_percent(pred, M_NEUTRON) > 99.99

    def test_running_phi_is_between_phi_and_phi2(self):
        pn = running_phi_neutron()
        assert PHI < pn < PHI ** 2

    def test_running_phi_reproduces_neutron_exactly(self):
        pred = neutron_mass_running_phi()
        assert abs(pred - M_NEUTRON) / M_NEUTRON < 1e-9


class TestTier2Muon:
    def test_muon_candidate_residual_reported_honestly(self):
        pred = m_mu_candidate_3_over_2alpha()
        obs = m_mu_over_m_e()
        # Candidate is within a few percent but is NOT claimed exact
        assert accuracy_percent(pred, obs) > 98.0
        assert abs(residual_percent(pred, obs)) > 0.1  # honest: not exact


# ── Tier 3: bottom-up Planck-anchored ────────────────────────────────────────

class TestTier3Planck:
    def test_proton_planck_accuracy(self):
        pred = proton_mass_planck()
        assert accuracy_percent(pred, M_PROTON) > 99.5

    def test_electron_planck_accuracy(self):
        pred = electron_mass_planck()
        assert accuracy_percent(pred, M_ELECTRON) > 99.5

    def test_planck_derived_ratios_consistent_with_6pi5(self):
        # Both Planck-anchored masses share M_P and alpha^-9, so their ratio
        # must equal 6 pi^5 independent of the normalization.
        ratio = proton_mass_planck() / electron_mass_planck()
        assert abs(ratio / m_p_over_m_e_6pi5() - 1.0) < 1e-9


# ── Scale reference frame ─────────────────────────────────────────────────────

class TestScaleReference:
    def test_qm_scale_anchors_present(self):
        # All anchors are measured QM-scale constants (CODATA 2018)
        assert M_ELECTRON > 0 and M_ELECTRON < 1.0e-3     # MeV-ish in GeV
        assert 0.9 < M_PROTON < 1.0
        assert 0.9 < M_NEUTRON < 1.0
        assert 0.09 < M_MUON < 0.12
