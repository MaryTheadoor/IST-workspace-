"""Tests for Phase 70 - H-GRAV2: the attraction sign from linking-mode tension.
Verifies: (H70a) E_int = -kappa^2 c^2 G(d) factors as a Green's-function product;
(H70b) attraction (E_int<0, dE/dd>0, F<0); (H70c) pure geometry (no tension) does
not attract (the 2+1-D control); (H70d) the force profile is 1/d^2 in D=3 (and
1/d in D=2, 1/d^3 in D=4); (H70e) the verdict."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase70_grav_attraction_sign import (
    kappa_coupling, interaction_energy_continuum, lattice_greens_crosscheck,
    attraction_sign, geometry_control, dimension_profile,
)


# ───────────────────────────────────────────────────────────────────────────────
# H70a - GREEN'S-FUNCTION PRODUCT (CONTINUUM)
# ───────────────────────────────────────────────────────────────────────────────

def test_kappa_coupling_positive():
    """The master-equation linking tension is positive (a real coupling)."""
    kappa = kappa_coupling()
    assert kappa > 0


def test_interaction_energy_continuum_negative():
    """E_int(d) = -kappa^2 c^2 G(d) with G>0 gives E_int < 0 (binding)."""
    d, G, E = interaction_energy_continuum(np.array([1.0, 2.0, 3.0]))
    assert np.all(G > 0)
    assert np.all(E < 0)


def test_interaction_energy_decrements_with_distance():
    """|E_int| decreases with d (G ~ 1/d), so it's more binding at short range."""
    d, G, E = interaction_energy_continuum(np.array([1.0, 2.0, 3.0, 4.0]))
    mag = np.abs(E)
    for i in range(len(mag) - 1):
        assert mag[i] > mag[i + 1]


def test_interaction_energy_matches_inverse_d():
    """E_int(d) / E_int(d0) = d0/d exactly (the 1/d Green's function)."""
    d, G, E = interaction_energy_continuum(np.array([1.0, 2.0, 4.0]))
    assert abs(E[2] / E[0] - 1.0 / 4.0) < 1e-9
    assert abs(E[1] / E[0] - 1.0 / 2.0) < 1e-9


def test_lattice_crosscheck_runs():
    """The finite-lattice cross-check runs (and is documented as indicative)."""
    rows = lattice_greens_crosscheck(L=7)
    assert len(rows) >= 1
    assert "d" in rows[0]


# ───────────────────────────────────────────────────────────────────────────────
# H70b - ATTRACTION SIGN
# ───────────────────────────────────────────────────────────────────────────────

def test_all_distances_attract():
    """F < 0 (toward the other knot) at every sampled d."""
    rows = attraction_sign()
    assert all(r["attracts"] for r in rows)


def test_binding_energy_negative():
    """E_int < 0 (bound state) for all d."""
    rows = attraction_sign()
    assert all(r["E_int"] < 0 for r in rows)


def test_dedd_positive():
    """dE/dd > 0 (E becomes more negative as d shrinks)."""
    rows = attraction_sign()
    assert all(r["dEdd"] > 0 for r in rows)


def test_force_magnitude_inverse_square():
    """|F| ~ 1/d^2: F(d)/F(d0) = (d0/d)^2."""
    rows = attraction_sign()
    f1 = next(r["F"] for r in rows if r["d"] == 1.0)
    f4 = next(r["F"] for r in rows if r["d"] == 4.0)
    assert abs(f4 / f1 - 1.0 / 16.0) < 1e-9  # (1/4)^2


# ───────────────────────────────────────────────────────────────────────────────
# H70c - GEOMETRY CONTROL
# ───────────────────────────────────────────────────────────────────────────────

def test_tension_attracts():
    """With the coupling tension, the system attracts."""
    rows = geometry_control()
    assert rows[0]["attracts"]


def test_pure_geometry_no_attraction():
    """Pure geometry (kappa=0) gives zero interaction and NO attraction —
    the 2+1-D no-attraction control."""
    rows = geometry_control()
    pure = rows[1]
    assert not pure["attracts"]
    assert abs(pure["E_int"]) < 1e-15
    assert abs(pure["dEdd"]) < 1e-15


# ───────────────────────────────────────────────────────────────────────────────
# H70d - DIMENSION PROFILE
# ───────────────────────────────────────────────────────────────────────────────

def test_dim3_exponent_minus2():
    """In emergent 3D the force exponent is exactly -2 (inverse square)."""
    rows = dimension_profile()
    d3 = next(r for r in rows if r["dim"] == 3)
    assert abs(d3["force_exponent"] - d3["expected"]) < 0.05


def test_exponents_match_minus_D_minus_1():
    """The force exponent = -(D-1) exactly for D=2,3,4."""
    rows = dimension_profile()
    for r in rows:
        assert abs(r["force_exponent"] - r["expected"]) < 0.05
        assert r["expected"] == -(r["dim"] - 1)


def test_inverse_square_requires_dim3():
    """The inverse-square law (exponent -2) holds only for D=3, not D=2 or D=4."""
    rows = dimension_profile()
    d3 = next(r for r in rows if r["dim"] == 3)
    d2 = next(r for r in rows if r["dim"] == 2)
    d4 = next(r for r in rows if r["dim"] == 4)
    assert abs(d3["force_exponent"] + 2.0) < 0.05  # 3D -> -2
    assert abs(d2["force_exponent"] + 1.0) < 0.05  # 2D -> -1
    assert abs(d4["force_exponent"] + 3.0) < 0.05  # 4D -> -3
