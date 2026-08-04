"""Tests for Phase 55 - the photon as a dual-mode wave function propagating
across both sides of the manifold."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase55_photon_compound import (
    KAPPA,
    ELECTRON_TWIST,
    carried_energy,
    dual_mode_omega,
    gapless_branch_count,
    group_velocity,
    photon_twist_fraction,
    propagate_dual_mode,
)


def test_h55a_group_velocity_independent_of_omega_0():
    vgs = [group_velocity(KAPPA, om, 0.5) for om in [0.0, 0.1, 0.3, 0.5, 0.8, 1.2]]
    spread = max(vgs) - min(vgs)
    assert spread < 1e-9, f"v_g should be dispersion-free, spread={spread}"


def test_h55a_dual_mode_lockstep_no_slip():
    slip, _ = propagate_dual_mode(0.5, 0.5, T=200)
    assert slip[-1] < 1e-6, "rung tie across the zero point must stay pinned"
    assert slip[-1] == slip.mean()


def test_h55a_packet_nondispersing():
    slip, comp = propagate_dual_mode(0.3, 0.5, T=200)
    assert abs(comp[-1] - comp[-5]) < 1e-6, "packet must not disperse"


def test_h55b_photon_achiral_zero_parity_inversion():
    for N in [210, 360, 480]:
        frac, _ = photon_twist_fraction(N)
        assert frac == 0.0, "photon must be achiral (parity-inversion 0.000)"
        assert ELECTRON_TWIST > 0.4, "electron knot reference must be 0.446"


def test_h55c_energy_linear_in_omega_0():
    Es = [carried_energy(om, 0.5) for om in [0.1, 0.2, 0.3, 0.4, 0.5]]
    diffs = np.diff(Es)
    assert all(abs(d - diffs[0]) < 1e-6 for d in diffs), \
        f"E=h*nu must be linear in omega_0, diffs={diffs}"


def test_h55c_massless_vg_constant_as_energy_added():
    vgs = [group_velocity(KAPPA, om, 0.5) for om in [0.1, 0.2, 0.3, 0.4, 0.5]]
    assert max(vgs) - min(vgs) < 1e-9, "v_g must stay constant (massless)"


def test_h55d_single_gapless_species():
    n, modes = gapless_branch_count(0.5)
    assert modes == 2, "two helicity modes"
    assert n == 1, f"single gapless branch (F_2=1), got {n}"


def test_figure_written():
    out = os.path.join(os.path.dirname(__file__), "..", "code", "outputs",
                       "phase55", "photon_dual_mode.png")
    assert os.path.exists(out), "figure output missing"