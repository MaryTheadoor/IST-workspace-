"""Tests for Phase 65 - the signature duality: the runtime instantiates the
elliptic zero point (closed Omega cycle, period-2 parity) against the
hyperbolic temporal axis (open substitution growth, eigenvalue phi)."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_klein_laplacian import PHI
from phase65_signature_duality import (
    duality_table, omega_cycle_check, parity_circle_check,
    temporal_growth_check,
)


# ───────────────────────────────────────────────────────────────────────────────
# H65a - the Omega cycle is exactly closed (elliptic)
# ───────────────────────────────────────────────────────────────────────────────

def test_h65a_omega_cycle_exactly_closed():
    amps, drift, conserved = omega_cycle_check()
    assert conserved is True
    assert drift < 1e-12, f"Omega cycle must not drift, got {drift:.2e}"
    # bounded: every amplitude equals the initial one
    assert all(a == pytest.approx(4.76, abs=1e-12) for a in amps)


def test_h65a_memory_and_parity_restored():
    # Omega_inv(Omega(x)) restores parity and memory exactly (the compression-
    # expansion cycle is the identity map: |return eigenvalue| = 1)
    _, _, conserved = omega_cycle_check(n_cycles=20)
    assert conserved


# ───────────────────────────────────────────────────────────────────────────────
# H65b - the parity circle is period-2
# ───────────────────────────────────────────────────────────────────────────────

def test_h65b_parity_flip_twice_is_identity():
    pc = parity_circle_check()
    assert pc["flip_twice_is_identity"] is True


def test_h65b_meridian_period_2():
    pc = parity_circle_check()
    assert pc["W"] == pytest.approx(-1.0)
    assert pc["W_squared"] == pytest.approx(1.0)
    assert pc["theta"] == pytest.approx(0.5)
    assert pc["period_2"] is True


# ───────────────────────────────────────────────────────────────────────────────
# H65c - the temporal axis is open (hyperbolic)
# ───────────────────────────────────────────────────────────────────────────────

def test_h65c_substitution_growth_is_phi():
    tg = temporal_growth_check()
    assert tg["converged_ratio"] == pytest.approx(PHI, rel=1e-6)
    assert tg["error_vs_phi"] < 1e-7
    assert tg["open_no_return"] is True
    assert tg["chain_length_growth"][-1] == pytest.approx(
        tg["chain_length_growth"][-2] * PHI, rel=1e-6)


# ───────────────────────────────────────────────────────────────────────────────
# H65d - the duality table
# ───────────────────────────────────────────────────────────────────────────────

def test_h65d_duality_contrast_is_exact():
    _, _, conserved = omega_cycle_check()
    pc = parity_circle_check()
    tg = temporal_growth_check()
    table = duality_table(conserved, pc["period_2"], tg["converged_ratio"])
    by_structure = {r["structure"]: r for r in table}
    # zero point + parity: closed, zero growth (elliptic)
    zp = by_structure["zero point (Omega cycle)"]
    par = by_structure["parity (seam meridian)"]
    tm = by_structure["time (substitution RG)"]
    assert zp["closed"] and par["closed"] and not tm["closed"]
    assert zp["growth"] == 0.0 and par["growth"] == 0.0
    assert tm["growth"] == pytest.approx(PHI, rel=1e-6)
    # the contrast: unit-modulus/closed vs phi/open, no intermediate values
    assert tm["growth"] > 1.0


def test_figure_written():
    out = os.path.join(os.path.dirname(__file__), "..", "code", "outputs",
                       "phase65", "signature_duality.png")
    assert os.path.exists(out), "figure output missing"
