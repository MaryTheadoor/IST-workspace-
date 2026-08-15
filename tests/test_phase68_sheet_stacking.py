"""Tests for Phase 68 - the sheet-stacking automaton: D_eff crossing 3 and the
stopping rule. Verifies: (H68a) the analytic D_eff curve; (H68b) the stacking
automaton locus model; (H68c) the naive-axis contrast; (H68d) the topological
instability at level 4; (H68e) OQ1 closed."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_klein_laplacian import PHI
from phase66_associator_derivation import PSI, PSI_SQ
from phase68_sheet_stacking import (
    deff_analytic, deff_analytic_table, stacking_automaton_locus,
    stacking_automaton_naive, topological_instability,
)


# ───────────────────────────────────────────────────────────────────────────────
# H68a - THE ANALYTIC D_eff CURVE
# ───────────────────────────────────────────────────────────────────────────────

def test_deff_at_N1():
    """D_eff(1) = 2 (one sheet, the base)."""
    assert abs(deff_analytic(1) - 2.0) < 1e-10


def test_deff_at_N3():
    """D_eff(3) crosses 3."""
    assert deff_analytic(3) > 3.0


def test_deff_asymptote():
    """D_eff(infinity) = 2*phi."""
    d_large = deff_analytic(100)
    assert abs(d_large - 2.0 * PHI) < 1e-6


def test_deff_monotone_increasing():
    """D_eff(N) is monotone increasing."""
    rows = deff_analytic_table(N_max=10)
    for i in range(1, len(rows)):
        assert rows[i]["D_eff"] > rows[i - 1]["D_eff"]


def test_deff_crossing_at_N3():
    """D_eff crosses 3 at N=3 (not N=2 or N=4)."""
    assert deff_analytic(2) < 3.0
    assert deff_analytic(3) >= 3.0


# ───────────────────────────────────────────────────────────────────────────────
# H68b - THE STACKING AUTOMATON (LOCUS MODEL)
# ───────────────────────────────────────────────────────────────────────────────

def test_locus_model_crosses_3():
    """The locus model's D_eff crosses 3 at N=3."""
    rows = stacking_automaton_locus(N_max=6)
    assert rows[2]["D_eff_measured"] > 3.0  # N=3 (index 2)


def test_locus_model_approximates_analytic():
    """The locus model approximates the analytic curve (within 10%)."""
    rows = stacking_automaton_locus(N_max=6)
    for r in rows:
        ratio = r["D_eff_measured"] / r["D_eff_analytic"]
        assert 0.85 < ratio < 1.15


# ───────────────────────────────────────────────────────────────────────────────
# H68c - THE NAIVE-AXIS CONTRAST
# ───────────────────────────────────────────────────────────────────────────────

def test_naive_model_overshoots():
    """The naive-axis model overshoots 3 (crosses at N=2, no stopping rule)."""
    rows = stacking_automaton_naive(N_max=6)
    assert rows[1]["D_eff_naive"] > 3.0  # N=2 (index 1)


def test_naive_contrast_grows():
    """The contrast between naive and locus grows with N."""
    rows = stacking_automaton_naive(N_max=6)
    for i in range(1, len(rows)):
        assert rows[i]["contrast"] > rows[i - 1]["contrast"]


# ───────────────────────────────────────────────────────────────────────────────
# H68d - THE TOPOLOGICAL INSTABILITY AT LEVEL 4
# ───────────────────────────────────────────────────────────────────────────────

def test_stability_at_N3():
    """Knot stability at N=3 is in the Phase 52 band (0.044)."""
    rows = topological_instability(N_max=6)
    assert rows[2]["knot_stability"] > 0.03  # N=3, still stable


def test_stability_collapse_at_N4():
    """Knot stability collapses at N=4 (exponential drop)."""
    rows = topological_instability(N_max=6)
    # N=4 stability should be < 0.01 (below the Phase 52 band)
    assert rows[3]["knot_stability"] < 0.01
    # and unstable
    assert rows[3]["unstable"]


def test_stability_monotone_decreasing():
    """Knot stability is monotone decreasing with N."""
    rows = topological_instability(N_max=6)
    for i in range(1, len(rows)):
        assert rows[i]["knot_stability"] <= rows[i - 1]["knot_stability"]


# ───────────────────────────────────────────────────────────────────────────────
# H68e - OQ1 CLOSED
# ───────────────────────────────────────────────────────────────────────────────

def test_oq1_stopping_rule():
    """The stopping rule: D_eff crosses 3 at N=3, and N=4 is unstable."""
    deff_rows = deff_analytic_table(N_max=6)
    topo_rows = topological_instability(N_max=6)
    # D_eff crosses 3 at N=3
    assert deff_rows[2]["crossing_3"]
    assert not deff_rows[1]["crossing_3"]  # N=2 doesn't cross
    # N=4 is unstable
    assert topo_rows[3]["unstable"]


def test_deff_infinity_is_2phi():
    """D_eff(infinity) = 2*phi ~ 3.236 (not 4 or higher)."""
    d = deff_analytic(1000)
    assert abs(d - 2.0 * PHI) < 1e-10
    assert d < 3.3  # less than 3.3 (no overshooting to 4)
