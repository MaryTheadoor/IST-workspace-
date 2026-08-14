"""Tests for Phase 64 - neutrino classification: the strand rule's next test.
Single open strand -> parity 0.446 -> fermion (consistent with observation);
lightness = open-strand non-closure; the Phase-3 tunneling gap re-anchored."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase64_neutrino_classification import (
    ELECTRON_TWIST, NAIVE_COUPLING, SIZES,
    closure_contrast, dual_strand_parity, neutrino_parity,
    tunneling_reanchor,
)


# ───────────────────────────────────────────────────────────────────────────────
# H64a - the parity test
# ───────────────────────────────────────────────────────────────────────────────

def test_h64a_open_strand_is_fermionic():
    # the single open strand's parity-inversion is the lattice twist fraction
    # 0.446 (electron value): the neutrino's required fermionic classification
    for N in SIZES:
        frac, n_cross = neutrino_parity(N)
        assert frac == pytest.approx(ELECTRON_TWIST, abs=0.002), \
            f"open strand must be fermionic, N={N} frac={frac}"
        assert n_cross > 0


def test_h64a_dual_strand_alternative_excluded():
    # the bosonic reading gives 0.000: excluded by the observed statistics
    for N in SIZES:
        assert dual_strand_parity(N) == 0.0
        assert neutrino_parity(N)[0] > 0.4


# ───────────────────────────────────────────────────────────────────────────────
# H64b - the closure test
# ───────────────────────────────────────────────────────────────────────────────

def test_h64b_closure_separates_fermions():
    cc = closure_contrast()
    assert cc["closure_separates_fermions"] is True
    # electron: closed knot, stable fraction consistent with ~1/34 (Phase 52
    # ensemble band 3.13% +/- 0.48% at 0.0444 -- the honest single-run value)
    assert 0.01 < cc["electron_closed_stable_fraction"] < 0.10
    assert cc["neutrino_open_fraction"] > 0.9
    # the neutrino (open strand) never phase-returns
    assert cc["open_strand_stability"] == 0.0


# ───────────────────────────────────────────────────────────────────────────────
# H64c - the tunneling re-anchor
# ───────────────────────────────────────────────────────────────────────────────

def test_h64c_gap_is_reanchored():
    tr = tunneling_reanchor()
    assert tr["required_P_tunnel"] == pytest.approx(4.1e-30, rel=0.05)
    assert tr["naive_alpha_over_phi2"] == pytest.approx(NAIVE_COUPLING, rel=1e-9)
    assert tr["measured_seam_crossing_frac"] == pytest.approx(
        ELECTRON_TWIST, abs=0.01)
    # the 27-order gap persists: classification does not depend on closing it
    assert tr["gap_required_vs_naive"] < 1e-20
    assert tr["gap_reanchored_not_closed"] is True


def test_figure_written():
    out = os.path.join(os.path.dirname(__file__), "..", "code", "outputs",
                       "phase64", "neutrino_classification.png")
    assert os.path.exists(out), "figure output missing"
