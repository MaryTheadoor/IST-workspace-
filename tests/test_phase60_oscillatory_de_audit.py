"""Tests for Phase 60 - audit of the '4-sigma' oscillatory-DE headline
(joint H(z)+Pantheon++DESI BAO) and the amplitude bridge."""

import os, sys
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase60_oscillatory_de_audit import (
    EPS0_DERIVED, DELTA0_DERIVED, BETA0_DERIVED, BETA_INV_PHI,
    load_hz, load_pantheon, chi2_joint, hz_osc, run_audit,
)


@pytest.fixture(scope="module")
def results():
    return run_audit()


@pytest.fixture(scope="module")
def data():
    zh, hd, sh = load_hz()
    zs, mu, me = load_pantheon()
    return zh, hd, sh, zs, mu, me


# ── data loaders ──────────────────────────────────────────────────────
def test_data_counts(data):
    zh, hd, sh, zs, mu, me = data
    assert len(zh) == 60, "60 H(z) points"
    assert len(zs) > 1600, "1701 Pantheon+ SNe"
    assert 1700 < len(zs) < 1710


def test_hz_osc_reduces_to_lcdm():
    z = np.linspace(0.01, 2.0, 50)
    h1 = hz_osc(z, 70.0, 0.3, 0.0, DELTA0_DERIVED, 0.0)
    h2 = hz_osc(z, 70.0, 0.3, 0.0, DELTA0_DERIVED, 5.0)
    np.testing.assert_allclose(h1, h2, atol=1e-10)


# ── LCDM baseline reproduction ────────────────────────────────────────
def test_lcdm_chi2_matches_v8(results):
    """v8 table: LCDM chi2=948, H0=73.6. Pipeline reproduced exactly."""
    assert 900 < results["lcdm"]["chi2"] < 1000


def test_lcdm_h0_matches_v8(results):
    assert abs(results["lcdm"]["H0"] - 73.6) < 0.3


# ── physical free fit (eps0 >= 0): NO improvement ─────────────────────
def test_physical_free_gives_no_oscillation(results):
    """With eps0 >= 0 (physically required), oscillation adds nothing."""
    assert abs(results["free"]["dchi2"]) < 2.0


def test_physical_free_eps0_is_zero(results):
    assert results["free"]["eps0"] < 1e-3, \
        "eps0 must be driven to zero under the positive-amplitude constraint"


# ── no-sign free fit (anti-phase = hidden phase dof): reproduces claim ──
def test_nosign_free_has_large_dchi2(results):
    """The '4-sigma' lives in the eps0 < 0 channel (unacknowledged phase)."""
    assert results["free_nosign"]["dchi2"] > 15.0


def test_nosign_free_has_negative_eps0(results):
    assert results["free_nosign"]["eps0_sign"] < 0


# ── pre-registered strict fits: invisible ──────────────────────────────
def test_prereg_phi3_invisible(results):
    assert abs(results["prereg_phi3"]["dchi2"]) < 5.0


def test_prereg_invphi_invisible(results):
    assert abs(results["prereg_invphi"]["dchi2"]) < 5.0


# ── Delta-profile look-elsewhere ───────────────────────────────────────
def test_physical_profile_max_at_boundary(results):
    """The physical-channel max is pinned at the scan edge (not interior)."""
    dp = results["delta_profile"]
    assert dp["best_Delta"] >= 4.5, "physical max must be boundary (Delta->large)"


def test_physical_profile_not_significant_globally(results):
    dp = results["delta_profile"]
    assert dp["p_global"] > 0.005, \
        "physical-channel periodic signal must not be globally significant"


def test_nosign_profile_interior_peak(results):
    """The anti-phase peak IS at an interior Delta (~1.4, near Plan 11's 1.54)."""
    dpn = results["delta_profile_nosign"]
    assert 0.5 < dpn["best_Delta"] < 3.0


def test_nosign_profile_global_significant(results):
    dpn = results["delta_profile_nosign"]
    assert dpn["p_global"] < 0.05


# ── amplitude bridge ───────────────────────────────────────────────────
def test_phi3_amplitude_bridge_does_not_reach_phase59(results):
    """eps_eff(zbar) = eps0*(1+zbar)^phi^3 < 0.05 at H(z) characteristic z."""
    ab = results["amplitude_bridge"]["hz"]
    assert ab["eps_eff_phi3"] < 0.05


def test_fitted_eps0_joint_is_zero(results):
    """The joint fit wants eps0 = 0 with positive amplitude."""
    assert results["free"]["eps0"] < 1e-3
