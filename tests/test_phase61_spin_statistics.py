"""Tests for Phase 61 - spin-statistics from seam braiding (Z2 exchange
holonomy): the exchange phase is the substrate holonomy; the exchange operator
algebra reproduces Pauli exclusion; the Z2 holonomy collapses the braid phase
to exactly +/-1 (no anyons in the emergent 3D substrate)."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase61_spin_statistics import (
    ELECTRON_TWIST, GRIDS, SIZES,
    _anyonic_P, anyonic_contrast, exchange_operator, exchange_phase,
    meridian_wilson_loop, pair_twist_naive, pauli_algebra,
    temporal_cycle_phase, wilson_loop_set,
)


# ───────────────────────────────────────────────────────────────────────────────
# H61a - the exchange phase is the substrate holonomy
# ───────────────────────────────────────────────────────────────────────────────

def test_h61a_meridian_wilson_loop_is_minus_one():
    # the Z2 meridian holonomy W = -1 is grid-independent on the Klein graph
    # (Phase 47 H47b, re-derived on the true discrete substrate), and +1 on
    # the orientable torus control (no seam).
    for (nm, nl) in GRIDS:
        Wk, sk = meridian_wilson_loop(nm, nl, twisted=True)
        Wt, st = meridian_wilson_loop(nm, nl, twisted=False)
        assert Wk == pytest.approx(-1.0), "Klein meridian holonomy must be -1"
        assert Wt == pytest.approx(+1.0), "torus meridian holonomy must be +1"
        assert sk == 1, "the fundamental meridian crosses the seam exactly once"
        assert st == 0


def test_h61a_temporal_cycle_single_strand_is_fermionic():
    # single-strand (seam-threading) excitation: the 4-tick SU(2) cycle is
    # exactly -I (Phase 25 flat-limit fermionic sign) -> exchange phase -1.
    chi, tr = temporal_cycle_phase("single", twisted=True)
    assert tr == pytest.approx(-1.0, abs=1e-12), "cycle must be exactly -I"
    assert chi == pytest.approx(-1.0)


def test_h61a_temporal_cycle_dual_strand_is_bosonic():
    # dual-strand (achiral, rung-bound) compound: no seam crossings, the cycle
    # is +I -> exchange phase +1.
    chi, tr = temporal_cycle_phase("dual", twisted=True)
    assert tr == pytest.approx(+1.0, abs=1e-12), "cycle must be exactly +I"
    assert chi == pytest.approx(+1.0)


def test_h61a_torus_has_no_fermions():
    # without the twist (torus control, W = +1) BOTH strand types exchange
    # with phase +1: there are no fermions without the non-orientable seam.
    for strand in ["single", "dual"]:
        chi, _ = temporal_cycle_phase(strand, twisted=False)
        assert chi == pytest.approx(+1.0), \
            f"{strand}-strand on torus must be bosonic"


def test_h61a_exchange_phase_consistent_with_holonomy():
    chi_s, W = exchange_phase("single", twisted=True)
    chi_d, _ = exchange_phase("dual", twisted=True)
    assert W == pytest.approx(-1.0)
    assert chi_s == pytest.approx(-1.0), "single-strand -> fermion"
    assert chi_d == pytest.approx(+1.0), "dual-strand -> boson"


# ───────────────────────────────────────────────────────────────────────────────
# H61b - the exchange operator algebra (Pauli exclusion)
# ───────────────────────────────────────────────────────────────────────────────

def test_h61b_double_exchange_is_identity():
    # P^2 = I: the braid double-exchange is the identity -> the statistics is
    # a +-1 (permutation-group) representation, the emergent-3D collapse
    # (sigma = sigma^-1) -- no anyons.
    for chi in [-1.0, 1.0]:
        r = pauli_algebra(N=16, chi=chi)
        assert r["P2_deviation"] < 1e-12, \
            f"P^2 must be exactly I for chi={chi:+.0f}"


def test_h61b_fermion_double_occupancy_annihilated():
    # two identical fermions in the same state: (1 + P)|i,i> = 0 -- the
    # forbidden configuration is annihilated by the topology.
    r = pauli_algebra(N=16, chi=-1.0)
    assert r["diag_sym_norm"] < 1e-12, \
        "(1+P)|i,i> must vanish for fermions (exclusion)"
    assert r["fermion_excluded"] is True
    # the symmetric (double-occupancy) combination is NOT the physical state
    # for the fermion: the antisymmetric subspace is the physical one.
    assert r["eig_minus"] > 0


def test_h61b_boson_double_occupancy_allowed():
    # two identical bosons in the same state: (1 - P)|i,i> = 0 (the
    # antisymmetric combination vanishes) while the symmetric one survives.
    r = pauli_algebra(N=16, chi=+1.0)
    assert r["diag_asym_norm"] < 1e-12, \
        "(1-P)|i,i> must vanish for bosons (occupancy allowed)"
    assert r["boson_allowed"] is True
    assert r["diag_sym_norm"] > 3.9, \
        "the symmetric double-occupancy state must survive (|1+1|^2 = 4)"


def test_h61b_mixed_species_no_exclusion():
    # different particles (distinct species labels) suffer no statistics
    # constraint: (1 + P)|f,b> != 0.
    for chi in [-1.0, 1.0]:
        r = pauli_algebra(N=16, chi=chi)
        assert r["mixed_norm"] > 1.9, \
            "mixed-species state must survive both statistics"


# ───────────────────────────────────────────────────────────────────────────────
# H61c - the anyon collapse is the Z2 holonomy
# ───────────────────────────────────────────────────────────────────────────────

def test_h61c_holonomy_group_is_z2():
    # the flat seam connection's holonomy group is exactly {+1, -1} on the
    # Klein (all Wilson loops are +/-1) and {+1} on the torus: the braid phase
    # is quantized to +/-1 before the emergent-3D question arises.
    hol_k, hol_t = wilson_loop_set()
    assert hol_k == {-1, 1}, f"Klein holonomy group must be Z2, got {hol_k}"
    assert hol_t == {1}, f"torus holonomy group must be trivial, got {hol_t}"


def test_h61c_z2_phase_gives_clean_exclusion():
    r = anyonic_contrast(N=16, theta=np.pi)
    assert r["is_plus_minus_one"] is True
    assert r["P2_eq_anyonic"] < 1e-12
    assert r["double_occupancy_survival"] < 1e-12


def test_h61c_continuous_holonomy_is_anyonic():
    # a continuous U(1) holonomy (theta != pi) breaks the collapse: P^2 != I
    # and the double-occupancy state survives -> genuine anyons, no clean
    # exclusion. The Z2 value theta = pi is the unique point where the phase
    # group collapses to +-1.
    for theta in [2 * np.pi / 5, 0.6]:
        r = anyonic_contrast(N=16, theta=theta)
        assert r["is_plus_minus_one"] is False
        assert r["P2_eq_anyonic"] > 1.0
        assert r["double_occupancy_survival"] > 2.0
    # the Z2 point is isolated: no neighborhood of pi stays at +-1
    r_pi = anyonic_contrast(N=16, theta=np.pi)
    r_off = anyonic_contrast(N=16, theta=np.pi - 0.1)
    assert r_pi["is_plus_minus_one"] and not r_off["is_plus_minus_one"]


def test_h61c_naive_pair_twist_is_not_a_statistics():
    # honest guard: the exchange phase is NOT the random-pair geodesic twist
    # flag. The pair flag takes BOTH values with the 0.446 mixture (H52c), so
    # chi_pair varies pair-to-pair -- not the constant +-1 of a statistics.
    # The statistics is the LOOP holonomy (W = -1), a global invariant.
    for N in SIZES:
        g = pair_twist_naive(N)
        assert g["twist_fraction"] == pytest.approx(ELECTRON_TWIST, abs=0.01)
        assert g["naive_chi_unique"] == 2, \
            "the naive pair flag must take both +1 and -1"
        assert g["naive_chi_std"] > 0.4, \
            "the naive pair flag must be pair-dependent (not constant)"


def test_figure_written():
    out = os.path.join(os.path.dirname(__file__), "..", "code", "outputs",
                       "phase61", "spin_statistics.png")
    assert os.path.exists(out), "figure output missing"
