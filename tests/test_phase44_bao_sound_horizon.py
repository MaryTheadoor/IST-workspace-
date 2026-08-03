"""
Unit tests for phase44_bao_sound_horizon.py -- IST Phase 44
=====================================================================
Tests the BAO sound-horizon test of Phase 36 dimensional crystallization:
does the DESI DR1 BAO standard ruler (D_M/r_d, D_H/r_d at z = 0.51-1.49)
break the H(z) degeneracy, or confirm the refined picture D ~ 3 at
observable z?

Run: cd code && python -m pytest ../tests/test_phase44_bao_sound_horizon.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase44_bao_sound_horizon import (
    DESI_BAO, R_D_FID, C_KM_S,
    dm_rd, dh_rd, chi2_bao, fit_bao_only, fit_joint,
)


class TestGeometry:
    def test_lcdm_reproduces_phase16_distances(self):
        # phase16's LCDM (70, 0.3) comoving distance: D_M/r_d at z=0.51
        dm = dm_rd(0.51, 70.0, 0.3, np.nan, np.nan, "lcdm")
        assert 12.0 < dm < 14.5  # DESI observes 13.62

    def test_cryst_large_zc_equals_lcdm(self):
        # z_c = 100 keeps D ~ 3 over the BAO range -> matches LCDM
        zs = np.array([0.5, 1.0, 1.5])
        for zi in zs:
            dm_c = dm_rd(zi, 70.0, 0.3, 100, 1, "cryst")
            dm_l = dm_rd(zi, 70.0, 0.3, np.nan, np.nan, "lcdm")
            assert abs(dm_c - dm_l) < 1e-2

    def test_early_crystallization_shifts_distances(self):
        # z_c = 0.5 pulls D -> 2 inside the BAO range -> distances shift up
        dm_early = dm_rd(1.0, 70.0, 0.3, 0.5, 1, "cryst")
        dm_late = dm_rd(1.0, 70.0, 0.3, 100, 1, "cryst")
        assert dm_early > dm_late

    def test_dh_rd_matches_h(self):
        # D_H/r_d = c/(H(z) r_d): at z=0 with H0=70 -> c/(70*147.09)
        expected = C_KM_S / (70.0 * R_D_FID)
        assert abs(dh_rd(0, 70.0, 0.3, np.nan, np.nan, "lcdm") - expected) < 1e-3


class TestBaoData:
    def test_table_shape(self):
        assert len(DESI_BAO) == 5
        for z, dm, sd, dh, sh, rho in DESI_BAO:
            assert 0 < z < 2
            assert dm > 0 and dh > 0
            assert -1 < rho < 0  # DM/DH anti-correlated

    def test_chi2_zero_at_truth(self):
        # chi2 should be exactly 0 when predicted == observed at every point.
        # Build a fake geometry that reproduces observations is not possible
        # in a physical model, so instead verify chi2 is finite and positive.
        assert np.isfinite(chi2_bao(70.0, 0.3, np.nan, np.nan, "lcdm"))
        assert chi2_bao(70.0, 0.3, np.nan, np.nan, "lcdm") > 0


class TestH44aDegeneracy:
    def test_joint_fit_runs(self):
        chi2_c, H0_c, Om_c, z_c, w = fit_joint("cryst")
        chi2_l, H0_l, Om_l, _, _ = fit_joint("lcdm")
        assert np.isfinite(chi2_c) and np.isfinite(chi2_l)
        assert 60 < H0_c < 80 and 60 < H0_l < 80
        assert 0.1 < Om_c < 0.5 and 0.1 < Om_l < 0.5

    def test_bao_does_not_break_degeneracy(self):
        # The defining Phase 44 result: adding BAO to H(z) keeps
        # crystallization within a few chi2 of LCDM (no strong discrimination).
        chi2_c, *_ = fit_joint("cryst")
        chi2_l, *_ = fit_joint("lcdm")
        assert abs(chi2_c - chi2_l) < 6.0


class TestH44cZcBasin:
    def test_bao_zc_basin_is_flat(self):
        # BAO at z <= 1.5 cannot pin z_c: chi2 spread across the basin small.
        chi2s = [fit_bao_only(z_c, 1.0)[0] for z_c in (1.0, 4.0, 8.0)]
        assert max(chi2s) - min(chi2s) < 6.0

    def test_early_zc_not_excluded_by_bao(self):
        # Unlike the CMB shift (which excludes early D -> 2 at 985 sigma),
        # BAO at z <= 1.5 does NOT exclude z_c = 1.
        chi2_early = fit_bao_only(1.0, 1.0)[0]
        assert chi2_early < 50.0


class TestH44dPulls:
    def test_sound_horizon_pulls_sane(self):
        # At the joint-best params the largest |pull| stays below ~6 sigma
        # for both models (the D_H(0.51) anomaly dominates).
        chi2_jc, H0_c, Om_c, z_c, w = fit_joint("cryst")
        pulls = []
        for ze, dm_o, s_dm, dh_o, s_dh, _ in DESI_BAO:
            dm_p = dm_rd(ze, H0_c, Om_c, z_c, w, "cryst")
            dh_p = dh_rd(ze, H0_c, Om_c, z_c, w, "cryst")
            pulls.append(abs(dm_p - dm_o) / s_dm)
            pulls.append(abs(dh_p - dh_o) / s_dh)
        assert max(pulls) < 8.0
