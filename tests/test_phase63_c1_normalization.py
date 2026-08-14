"""Tests for Phase 63 - the c1 normalization resolution: the IXPE VR band
selects M_assoc ~ [1.1, 1.6] MeV, the phi^2 m_e reading sits inside it with
R = 52.33/phi^8 = 1.114, and the 52.3x enhancement stays gated."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_klein_laplacian import PHI
from phase63_c1_normalization import (
    E_BAND, M_E, R_52,
    candidate_scales, ixpe_implied_band, phi2_reading, ratio_R, vr_energy_keV,
)


# ───────────────────────────────────────────────────────────────────────────────
# H63a - the normalization map
# ───────────────────────────────────────────────────────────────────────────────

def test_h63a_map_reproduces_52x_branch():
    # M = m_e is the excluded Phase-62 branch (i): R = 52.3, E_VR = 0.41 keV.
    assert ratio_R(M_E) == pytest.approx(R_52, rel=1e-6)
    assert vr_energy_keV(R_52) == pytest.approx(0.415, abs=0.01)


def test_h63a_map_is_quartic_in_mass():
    assert ratio_R(2 * M_E) == pytest.approx(R_52 / 16.0, rel=1e-9)
    assert ratio_R(0.5 * M_E) == pytest.approx(R_52 * 16.0, rel=1e-9)


# ───────────────────────────────────────────────────────────────────────────────
# H63b - the IXPE-implied band
# ───────────────────────────────────────────────────────────────────────────────

def test_h63b_band_inversion():
    band = ixpe_implied_band()
    # E_VR = 3/sqrt(R) in [2,4] -> R in [9/16, 9/4]
    assert band["R_lo"] == pytest.approx(9.0 / 16.0, rel=1e-12)
    assert band["R_hi"] == pytest.approx(9.0 / 4.0, rel=1e-12)
    # M_assoc in [1.12, 1.59] MeV
    assert 1.0 < band["M_lo_MeV"] < 1.2
    assert 1.5 < band["M_hi_MeV"] < 1.7
    assert band["M_lo_MeV"] < band["M_hi_MeV"]


def test_h63b_band_contains_phi2_me_and_np_diff():
    band = ixpe_implied_band()
    assert band["M_lo_MeV"] < PHI ** 2 * M_E < band["M_hi_MeV"]
    assert band["M_lo_MeV"] < 1.29333236 < band["M_hi_MeV"]


# ───────────────────────────────────────────────────────────────────────────────
# H63c - the candidate-scale table
# ───────────────────────────────────────────────────────────────────────────────

def test_h63c_candidates_scored_against_band():
    by_name = {r["candidate"]: r for r in candidate_scales()}
    # in band: the two MeV-scale candidates
    assert by_name["phi^2 m_e"]["in_2_4_keV_band"] is True
    assert by_name["m_n - m_p"]["in_2_4_keV_band"] is True
    # out: the QED loop itself (the gated branch), pair threshold, muon mean,
    # pion scale
    for name in ["m_e", "2 m_e", "sqrt(m_e m_mu)", "m_pi0"]:
        assert by_name[name]["in_2_4_keV_band"] is False, name
    # the QED loop reproduces the Phase-62 branch (i) number
    assert by_name["m_e"]["E_VR_keV"] == pytest.approx(0.41, abs=0.01)


# ───────────────────────────────────────────────────────────────────────────────
# H63d - the phi^2 reading
# ───────────────────────────────────────────────────────────────────────────────

def test_h63d_phi2_reading_inside_all_bands():
    ph = phi2_reading()
    assert ph["R"] == pytest.approx(R_52 / PHI ** 8, rel=1e-9)
    assert 1.0 < ph["R"] < 1.3
    assert E_BAND[0] < ph["E_VR_keV"] < E_BAND[1]
    assert ph["delta_n_ratio_vs_QED"] == pytest.approx(
        (4.0 / 3.0) * ph["R"], rel=1e-9)
    assert 30.0 < ph["decoupling_Rstar"] < 300.0
    assert ph["E_VR_in_band"] and ph["decoupling_in_30_300"]
    assert ph["R_close_to_unity"]


def test_h63d_phi2_scale_definition():
    # M_assoc = phi^2 m_e exactly (the pre-registered reading)
    assert phi2_reading()["M_assoc_MeV"] == pytest.approx(
        PHI ** 2 * M_E, rel=1e-9)


def test_h63d_52x_branch_stays_gated():
    # the Phase-56 magnitude reading (M = m_e) remains far outside the band:
    # E_VR = 0.41 keV, not 2-4 keV.
    assert not (E_BAND[0] < vr_energy_keV(ratio_R(M_E)) < E_BAND[1])


def test_figure_written():
    out = os.path.join(os.path.dirname(__file__), "..", "code", "outputs",
                       "phase63", "c1_normalization.png")
    assert os.path.exists(out), "figure output missing"
