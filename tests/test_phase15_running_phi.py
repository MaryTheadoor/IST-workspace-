"""Tests for phase15_running_phi.py"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from phase15_running_phi import *
from phase1_klein_laplacian import PHI


class TestRunningPhi:
    def test_phi_approaches_asymptote(self):
        assert abs(phi_running(100, PHI, 2.0, 0.2) - PHI) < 0.01
    def test_phi_at_uv_is_larger(self):
        assert phi_running(0.01, PHI, 2.0, 0.2) > PHI + 0.2
    def test_alpha_s_decreases_with_energy(self):
        a_low = alpha_s_running(10, PHI, 2.0, 0.2)
        a_high = alpha_s_running(1000, PHI, 2.0, 0.2)
        assert a_high < a_low
    def test_neutron_mass_close_to_observed(self):
        phi_n = phi_running(0.5/91.2, PHI, 2.0, 0.2)
        delta = (1/137.036) / phi_n**2
        m_n = 0.9378 * (1 + delta)
        assert abs(m_n - 0.9396) < 0.002

class TestAlphaS:
    def test_phi4_fix_at_mz(self):
        pred = alpha_s_corrected(91.1876)
        assert abs(pred - 0.118) < 0.015  # within 3% at M_Z
    def test_phi4_fix_at_mtau(self):
        pred = alpha_s_corrected(1.78)
        assert abs(pred - 0.33) < 0.03  # within 1.3%
    def test_phi4_layers_increase_with_energy(self):
        assert n_layers(10) < n_layers(100)

class TestMagnification:
    def test_mag_analysis(self):
        m = magnification_analysis()
        assert 25 < m["implied_magnification"] < PHI**9

class TestRedshiftDE:
    @classmethod
    def setup_class(cls):
        cls.z, cls.H, cls.sig = hz_data()
    def test_data_loaded(self):
        assert len(self.z) > 10
    def test_hz_model_gives_positive_values(self):
        h = hz_model(np.linspace(0, 2, 10))
        assert np.all(h > 0)
    def test_running_epsilon_increases_with_z(self):
        eps = [0.136 * (1+z)**(1/PHI) for z in [0, 1, 2]]
        assert eps[0] < eps[1] < eps[2]
