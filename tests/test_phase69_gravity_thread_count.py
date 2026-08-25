"""Tests for Phase 69 - gravity from thread-counting: the 1/r^2 law.
Verifies: (H69a) mass ~ thread count (exactly linear); (H69b) conserved flux
gives 1/r^2 (not exponential); (H69c) Newton's constant assembles from the
substrate; (H69d) the force exponent tracks the dimension; (H69e) the
reconciliation of the two IST gravity mechanisms."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_klein_laplacian import PHI
from phase69_gravity_thread_count import (
    thread_count, thread_count_table, golden_angle_directions,
    conserve_flux_on_shells, flux_exponent, newton_constant_formula,
    required_substrate_length, newton_constant_audit, reconciliation,
)


# ───────────────────────────────────────────────────────────────────────────────
# H69a - MASS ~ THREAD COUNT
# ───────────────────────────────────────────────────────────────────────────────

def test_thread_count_exactly_linear():
    """N(M)/M is constant across masses (exactly linear, no free exponent)."""
    rows = thread_count_table([0.51099895, 0.938272, 93.0, 1000.0])
    ratios = [r["N_over_M"] for r in rows]
    # all ratios equal to machine precision
    assert np.allclose(ratios, ratios[0], rtol=1e-10)


def test_thread_count_scales_with_mass():
    """More mass -> more threads (monotone)."""
    rows = thread_count_table([0.5, 5.0, 50.0])
    counts = [r["thread_count"] for r in rows]
    assert counts[0] < counts[1] < counts[2]


def test_thread_count_doubling():
    """Doubling mass roughly doubles the thread count (linear)."""
    n1 = thread_count(1.0)
    n2 = thread_count(2.0)
    assert abs(n2 / n1 - 2.0) < 1e-10


# ───────────────────────────────────────────────────────────────────────────────
# H69b - CONSERVED FLUX GIVES 1/r^2
# ───────────────────────────────────────────────────────────────────────────────

def test_golden_angle_directions_normalized():
    """The golden-angle thread directions are unit vectors."""
    dirs = golden_angle_directions(200)
    norms = np.linalg.norm(dirs, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-10)


def test_flux_conserved_every_shell():
    """Conservation: every shell passes ALL threads (no dissipation)."""
    rows = conserve_flux_on_shells(N_threads=1000, n_dir=500, dim=3)
    for r in rows:
        assert r["threads_passing"] == 1000  # conserved, no dissipation


def test_flux_density_slope_3d():
    """The flux-density log-log slope for dim=3 is -2 (1/r^2), not exponential."""
    rows = conserve_flux_on_shells(N_threads=1000, n_dir=500, dim=3)
    r = np.array([x["radius"] for x in rows])
    d = np.array([x["density"] for x in rows])
    slope, _ = np.polyfit(np.log(r), np.log(d), 1)
    assert abs(slope + 2.0) < 0.01


def test_flux_density_is_proportional_to_1_over_r2():
    """Each shell's density ~ r^(1-D) up to the constant N/(4 pi) (i.e. density
    is proportional to 1/r^2, the functional form is exact)."""
    rows = conserve_flux_on_shells(N_threads=1000, n_dir=500, dim=3)
    # density * r^2 should be constant = N/(4 pi) at every shell
    for x in rows:
        assert abs(x["density"] * x["radius"] ** 2 - 1000.0 / (4 * np.pi)) < 1e-6


# ───────────────────────────────────────────────────────────────────────────────
# H69c - NEWTON'S CONSTANT FROM THE SUBSTRATE
# ───────────────────────────────────────────────────────────────────────────────

def test_newton_constant_formula_verifies():
    """G = kappa c^2 L^2/(16 pi^3 hbar^2) reproduces the measured G for the
    required L (self-consistency check)."""
    nc = newton_constant_audit()
    assert abs(nc["G_verification_ratio"] - 1.0) < 1e-3


def test_required_substrate_length_finite():
    """The required substrate length to match G is finite and positive."""
    L_req, L_planck = required_substrate_length(kappa=1.0)
    assert np.isfinite(L_req) and L_req > 0
    assert np.isfinite(L_planck)


def test_newton_constant_planck_is_not_g():
    """Honest negative: the Planck-length identification is WRONG (off by many
    orders) -- G is not the Planck tension."""
    nc = newton_constant_audit()
    # G at the Planck length is dramatically off from the measured G
    assert abs(np.log10(nc["G_planck_length_m3_kg1_s2"] / nc["G_measured_m3_kg1_s2"])) > 10


# ───────────────────────────────────────────────────────────────────────────────
# H69d - EXPONENT TRACKS THE DIMENSION
# ───────────────────────────────────────────────────────────────────────────────

def test_exponent_dim3_is_minus2():
    """Inverse-square: exponent = -2 in D=3."""
    assert abs(flux_exponent(3) + 2.0) < 0.01


def test_exponent_strands_attribute():
    """Exponent = -(D-1): -1 for D=2, -2 for D=3, -3 for D=4."""
    for dim, expected in [(2, -1), (3, -2), (4, -3)]:
        assert abs(flux_exponent(dim) - expected) < 0.01


def test_inverse_square_requires_dim3():
    """The inverse-square law REQUIRES D=3 (not 2 or 4)."""
    assert abs(flux_exponent(2) + 2.0) > 0.1  # D=2 gives -1, not -2
    assert abs(flux_exponent(4) + 2.0) > 0.1  # D=4 gives -3, not -2


# ───────────────────────────────────────────────────────────────────────────────
# H69e - THE RECONCILIATION
# ───────────────────────────────────────────────────────────────────────────────

def test_reconciliation_has_two_mechanisms():
    """The reconciliation presents both IST gravity mechanisms."""
    rows = reconciliation()
    assert len(rows) == 2


def test_reconciliation_differs_in_range():
    """The two mechanisms differ: one short-range (Gaussian), one long-range (1/r²)."""
    rows = reconciliation()
    assert rows[0]["range"] != rows[1]["range"]
    assert "exponential" in rows[0]["long_range_tail"]
    assert "1/r^2" in rows[1]["long_range_tail"]
