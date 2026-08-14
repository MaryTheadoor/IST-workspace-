"""Tests for Phase 62 - the IXPE vacuum-birefringence gate (Stewart et al.
2026): the achiral vacuum (c2 = 0) survives structurally (E||B mode exactly
non-refractive), the c1 = alpha/phi^2 (52.3x QED) reading is in tension with
the observed 2-4 keV vacuum-resonance dip, and the gate verdict is recorded."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase62_ixpe_vb_gate import (
    ALPHA, C1_QED, C1_IST_RATIO, E_BAND, QED_C2_C1,
    achiral_mode_algebra, accumulated_phase, decoupling_radius,
    delta_n_surface, mode_index_shifts, on_shell_check, qed_canonical,
    registration_gate, verify_mode_algebra, vr_energy,
)


# ───────────────────────────────────────────────────────────────────────────────
# H62a - the mode algebra
# ───────────────────────────────────────────────────────────────────────────────

def test_h62a_derivation_matches_canonical_qed():
    # the exact quadratic expansion reproduces the canonical QED one-loop
    # indices (14/45, 8/45)(alpha^2/m^4) B^2 sin^2(theta) at all angles.
    for r in verify_mode_algebra(B_mag=1.0):
        assert r["derived_npar"] == pytest.approx(r["canonical_npar"], rel=1e-6)
        assert r["derived_nperp"] == pytest.approx(r["canonical_nperp"], rel=1e-6)
        assert r["ratio_derived"] == pytest.approx(QED_C2_C1, rel=1e-6)
        assert r["ratio_canonical"] == pytest.approx(QED_C2_C1, rel=1e-6)


def test_h62a_onshell_probe_invariant_vanishes():
    # internal consistency: a plane-wave probe has B_f^2 = E_f^2 exactly.
    for th in (0.2, 0.6, 1.0, 1.3):
        assert abs(on_shell_check(1.0, th)) < 1e-12


def test_h62a_decoupling_is_exact_by_invariant():
    # n(E||B) depends on c2 ONLY and n(E_|_B) on c1 ONLY: swapping the
    # couplings moves the two shifts independently.
    n_par, n_perp = mode_index_shifts(C1_QED, QED_C2_C1 * C1_QED, 1.0, 1.0)
    n_par0, n_perp0 = mode_index_shifts(C1_QED, 0.0, 1.0, 1.0)
    n_par1, n_perp1 = mode_index_shifts(0.0, QED_C2_C1 * C1_QED, 1.0, 1.0)
    # c2 -> 0 kills only the E||B shift; c1 -> 0 kills only the E_|_B shift
    assert n_par0 == pytest.approx(0.0, abs=1e-18)
    assert n_perp1 == pytest.approx(0.0, abs=1e-18)
    assert n_perp0 == pytest.approx(n_perp, rel=1e-12)
    assert n_par1 == pytest.approx(n_par, rel=1e-12)


def test_h62a_achiral_vacuum_epar_mode_is_exactly_nonrefractive():
    # c2 = 0 -> n(E||B) = 1 EXACTLY at all angles (the structural, normalization-
    # independent core of the c2/c1 = 0 prediction).
    for r in achiral_mode_algebra():
        assert r["n_par_is_one"] is True
        assert abs(r["n_par_minus_1"]) < 1e-15


def test_h62a_achiral_nperp_scales_with_c1():
    # n(E_|_B) - 1 = 16 c1 B^2 sin^2(theta): the surviving channel.
    for th in (0.4, 0.9, 1.3):
        n_par, n_perp = mode_index_shifts(C1_QED, 0.0, 1.0, th)
        assert n_perp == pytest.approx(16.0 * C1_QED * np.sin(th) ** 2,
                                       rel=1e-9)


# ───────────────────────────────────────────────────────────────────────────────
# H62b - the magnetar observable
# ───────────────────────────────────────────────────────────────────────────────

def test_h62b_qed_decoupling_lands_in_paper_band():
    # independent validation of the whole chain: the QED accumulated phase
    # puts the mode-decoupling radius inside the paper's own 30-300 R*
    # statement for 1E 1547.0-5408.
    r_qed = decoupling_radius(1.0, 1.0)
    assert 30.0 < r_qed < 300.0


def test_h62b_branch_ii_is_consistent():
    # c2 = 0 with c1 ~ QED: |Delta n| = (4/3) QED, sign-flipped; decoupling
    # and VR both inside the observed bands -> consistent with the IXPE data.
    dn = delta_n_surface(1.0, 0.0)
    dn_qed = delta_n_surface(1.0, 1.0)
    assert dn == pytest.approx(-(4.0 / 3.0) * dn_qed, rel=1e-9)
    assert dn < 0 < dn_qed                          # sign-flipped
    assert 30.0 < decoupling_radius(1.0, 0.0) < 300.0
    assert E_BAND[0] < vr_energy(1.0) < E_BAND[1]


def test_h62b_branch_i_is_in_tension():
    # c1 = 52.3x QED: the vacuum-resonance energy moves to ~0.4 keV, far from
    # the observed 2-4 keV dip, and the decoupling radius leaves the paper's
    # band -> the Phase 56 magnitude reading is gated off.
    vr = vr_energy(C1_IST_RATIO)
    assert not (E_BAND[0] < vr < E_BAND[1])
    assert vr < 1.0
    assert decoupling_radius(C1_IST_RATIO, 0.0) > 300.0
    # magnitude check: ~70x QED, sign-flipped
    dn = delta_n_surface(C1_IST_RATIO, 0.0)
    dn_qed = delta_n_surface(1.0, 1.0)
    assert dn == pytest.approx(-(4.0 / 3.0) * C1_IST_RATIO * dn_qed, rel=1e-6)


def test_h62b_accumulated_phase_is_saturated():
    # the accumulated VB phase is enormous (>> 1) for every branch: the
    # polarization modes are adiabatically locked -- the paper's core premise.
    for c1r, c2r in [(1.0, 1.0), (1.0, 0.0), (C1_IST_RATIO, 0.0)]:
        assert abs(accumulated_phase(c1r, c2r)) > 1e9


# ───────────────────────────────────────────────────────────────────────────────
# H62c/H62d - the gate
# ───────────────────────────────────────────────────────────────────────────────

def test_h62d_gate_table_verdicts():
    rows = registration_gate()
    by_model = {r["model"]: r for r in rows}
    qed = by_model["QED"]
    ii = by_model["IST branch (ii): c2=0, c1~QED"]
    i = by_model["IST branch (i): c2=0, c1=52.3x"]
    # QED and branch (ii) pass both anchors; branch (i) fails both
    assert qed["decoupling_in_30_300"] and qed["vr_in_2_4_keV"]
    assert ii["decoupling_in_30_300"] and ii["vr_in_2_4_keV"]
    assert not i["decoupling_in_30_300"] and not i["vr_in_2_4_keV"]
    # the structural discriminator: branch (ii) and (i) share c2 = 0
    assert ii["c2_ratio"] == 0.0 and i["c2_ratio"] == 0.0
    assert qed["c2_ratio"] == 1.0


def test_figure_written():
    out = os.path.join(os.path.dirname(__file__), "..", "code", "outputs",
                       "phase62", "ixpe_vb_gate.png")
    assert os.path.exists(out), "figure output missing"
