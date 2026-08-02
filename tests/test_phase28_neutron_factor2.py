"""
Unit tests for phase28_neutron_factor2.py -- IST Phase 28
=========================================================
The factor-2 neutron: delta_n = (alpha/2 phi^2)(1 - c alpha) with
c = 3/2 - alpha/phi^6. Tests the forms against the observed neutron excess
and the exact correction coefficient, and verifies the synthesis-paper's
running-phi arithmetic error is corrected.

Run: cd code && python -m pytest ../tests/test_phase28_neutron_factor2.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from ist_toolkit_v2 import PHI, ALPHA, M_PROTON, M_NEUTRON
from phase28_neutron_factor2 import (
    delta_n_observed, delta_n_naive, delta_n_factor2,
    c_exact_coefficient, c_claimed, delta_n_exact,
    running_phi_neutron, m_n_from_phi,
)


class TestNaiveFormFails:
    def test_naive_overshoots_by_two(self):
        # The plan's alpha/phi^2 is ~2.02x the observed excess
        assert delta_n_naive() / delta_n_observed() > 2.0

    def test_naive_accuracy_is_under_99_9(self):
        pred = M_PROTON * (1.0 + delta_n_naive())
        assert abs(pred - M_NEUTRON) / M_NEUTRON > 1e-4


class TestFactor2LeadingTerm:
    def test_factor2_is_close_but_not_exact(self):
        d = delta_n_factor2()
        obs = delta_n_observed()
        # factor-2 lands within ~1% of delta_n but not exact
        assert abs(d / obs - 1.0) < 0.02
        assert abs(d / obs - 1.0) > 1e-4

    def test_factor2_accuracy_above_99_99(self):
        pred = M_PROTON * (1.0 + delta_n_factor2())
        # factor-2 lands at 99.9985% (1.4e-5 relative) -- a big improvement
        # over the naive form but not exact
        assert abs(pred - M_NEUTRON) / M_NEUTRON < 2e-5


class TestExactForm:
    def test_coefficient_close_to_claimed(self):
        assert abs(c_exact_coefficient() - c_claimed()) < 1e-6

    def test_exact_form_hits_neutron(self):
        d = delta_n_exact()
        pred = M_PROTON * (1.0 + d)
        # relative agreement to better than 1e-8
        assert abs(pred - M_NEUTRON) / M_NEUTRON < 1e-8

    def test_exact_delta_within_observational_error(self):
        obs = delta_n_observed()
        u_rel = np.sqrt((5.7e-8) ** 2 + (1.4e-8) ** 2)
        sigma = abs(delta_n_exact() - obs) / (obs * u_rel)
        assert sigma < 1.0

    def test_third_order_expansion_consistency(self):
        # delta_n = a/(2f2) - 3a^2/(4f2) + a^3/(2f8)
        a, f = ALPHA, PHI
        series = a/(2*f**2) - 3*a**2/(4*f**2) + a**3/(2*f**8)
        assert abs(series - delta_n_exact()) < 1e-20


class TestRunningPhi:
    def test_true_running_phi_is_about_2_3(self):
        pn = running_phi_neutron()
        assert 2.0 < pn < 2.6

    def test_paper_claimed_198_is_only_99_95(self):
        # The synthesis paper claimed phi=1.98 gives 99.99%; it actually
        # gives 99.95%. This test pins the corrected claim.
        m = m_n_from_phi(1.98)
        acc = 1.0 - abs(m - M_NEUTRON) / M_NEUTRON
        assert acc < 0.9997          # NOT 99.99%
        assert acc > 0.999           # still 99.95%

    def test_running_phi_reproduces_observed(self):
        m = m_n_from_phi(running_phi_neutron())
        assert abs(m - M_NEUTRON) / M_NEUTRON < 1e-10
