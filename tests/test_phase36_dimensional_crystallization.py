"""
Unit tests for phase36_dimensional_crystallization.py -- IST Phase 36
=====================================================================
Tests the dimensional-crystallization hypothesis: D(z) from 2 (superfluid
substrate) toward 3 (crystallized), against H(z) chronometers + CMB shift
prior. Verifies the honest falsification: D -> 2 by recombination is
CMB-excluded.

Run: cd code && python -m pytest ../tests/test_phase36_dimensional_crystallization.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase36_dimensional_crystallization import (
    load_hz, d_eff, hz_cryst, hz_lcdm, shift_parameter,
    fit_crystallization, fit_lcdm, R_CMB, R_CMB_SIG,
)


class TestData:
    def test_hz_data_loaded(self):
        z, H, sig = load_hz()
        assert len(z) == 60
        assert z.min() > 0 and z.max() < 3.0

    def test_data_sorted(self):
        z, _, _ = load_hz()
        assert np.all(np.diff(z) > 0)


class TestDimensionalModel:
    def test_d_eff_present_day_three(self):
        assert abs(d_eff(0, 4, 1) - 3.0) < 0.05

    def test_d_eff_high_z_two(self):
        assert abs(d_eff(100, 4, 1) - 2.0) < 1e-3

    def test_d_eff_crossover(self):
        # at z_c, D = 2.5
        assert abs(d_eff(4, 4, 1) - 2.5) < 0.02

    def test_hz_cryst_matches_lcdm_at_D3(self):
        # with a very large z_c the dimension stays ~3 over observable z,
        # matching LCDM
        z = np.array([0.5, 1.0, 2.0])
        assert np.allclose(hz_cryst(z, 70, 0.3, 100, 1),
                           hz_lcdm(z, 70, 0.3), rtol=1e-4)


class TestShiftParameter:
    def test_lcdm_shift_reproduces_planck(self):
        # LCDM limit (z_c huge => D ~ 3 at all z < z*) must give R ~ 1.75
        R = shift_parameter(0.3, 10000, 1)
        assert abs(R - 1.75) < 0.05

    def test_early_2d_gives_large_shift(self):
        # D -> 2 by recombination gives R >> 1.75 (CMB-excluded)
        R = shift_parameter(0.3, 4, 1)
        assert R > 3.0


class TestHonestFalsification:
    def test_cmb_excludes_early_2d(self):
        R = shift_parameter(0.3, 4, 1)
        sigma = abs(R - R_CMB) / R_CMB_SIG
        assert sigma > 100                 # excluded by hundreds of sigma

    def test_crystallization_fits_as_well_as_lcdm(self):
        z, H, sig = load_hz()
        chi2_c, *_ = fit_crystallization(z, H, sig)
        chi2_l, *_ = fit_lcdm(z, H, sig)
        assert abs(chi2_c - chi2_l) < 3.0  # degenerate in H(z)

    def test_lcdm_fit_sane(self):
        z, H, sig = load_hz()
        chi2_l, H0, Om = fit_lcdm(z, H, sig)
        assert 60 < H0 < 80
        assert 0.1 < Om < 0.5
        assert chi2_l < 30
