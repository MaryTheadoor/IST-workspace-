"""Tests for Phase 58 - the trace-map RG: rescoring Phase 51's spectral-
dimension negative with the natural (substitution) renormalization of the
Fibonacci substrate."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_klein_laplacian import PHI
from phase58_trace_map_rg import (
    block_spin_drift, golden_growth_ratio, trace_map_rg_check,
)


def test_h58a_block_spin_never_reaches_phi():
    _rows, summ = block_spin_drift()
    # D_eff must stay far from phi across the whole RG flow
    assert summ["min_distance_to_phi"] > 0.4, \
        "block-spin D_eff must never approach phi"


def test_h58a_block_spin_not_convergent():
    _rows, summ = block_spin_drift()
    # a clean fixed point would show tiny scatter; the wrong RG does not settle
    assert summ["D_eff_range"] > 0.05


def test_h58a_deepest_projection_degrades_fit():
    _rows, summ = block_spin_drift()
    assert summ["r2_last"] <= summ["r2_first"] + 1e-12, \
        "fit quality must not improve as the projection shrinks the system"


def test_h58b_golden_growth_eigenvalue_exact():
    rows = golden_growth_ratio()
    # the natural (substitution) RG growth eigenvalue converges to phi exactly
    assert rows[-1]["ratio_Fn_over_Fnm1"] == pytest.approx(PHI, rel=1e-6)
    assert abs(rows[-1]["ratio_Fn_over_Fnm1"] - PHI) < 1e-6


def test_h58b_growth_monotone_convergent():
    rows = golden_growth_ratio()
    errs = [abs(r["ratio_Fn_over_Fnm1"] - PHI) for r in rows]
    assert errs[-1] < errs[0], "must converge to phi with generation"


def test_h58b_trace_map_is_exact_rg_kernel():
    err_max, inv_spread = trace_map_rg_check()
    assert err_max < 1e-9, f"trace-map recurrence must be machine-precision, got {err_max:.2e}"
    assert inv_spread < 1e-6, f"Fricke invariant must be conserved, spread {inv_spread:.2e}"


def test_h58c_natural_rg_beats_wrong_rg():
    _rows_a, summ = block_spin_drift()
    rows_b = golden_growth_ratio()
    golden_err = abs(rows_b[-1]["ratio_Fn_over_Fnm1"] - PHI)
    # the correct RG locates phi exactly (1e-8) while the wrong RG misses by 0.54
    assert golden_err < 1e-6
    assert golden_err < summ["min_distance_to_phi"] / 1e5


def test_figure_written():
    out = os.path.join(os.path.dirname(__file__), "..", "code", "outputs",
                       "phase58", "trace_map_rg.png")
    assert os.path.exists(out), "figure output missing"
