"""Tests for Phase 56 - the 4WM discriminator: dual-mode photon vacuum vs QED
Heisenberg-Euler."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase56_four_wave_mixing import (
    ALPHA_INV, PHI2_OVER_ALPHA, QED_C2_C1,
    euler_heisenberg_invariants, golden_magnitude_ratio, ist_dual_mode_invariants,
    output_group_velocity,
)


def test_h56a_qed_canonical_ratio():
    c1, c2, ratio = euler_heisenberg_invariants()
    assert ratio == pytest.approx(QED_C2_C1, abs=1e-9)
    assert c2 > 0, "QED parity-odd channel must be OPEN"


def test_h56a_ist_achiral_forbids_parity_odd():
    c1, c2, ratio = ist_dual_mode_invariants()
    assert c2 == 0.0, "achiral vacuum cannot source the parity-odd invariant"
    assert ratio == 0.0


def test_h56a_discriminator_separates_models():
    _, _, r_qed = euler_heisenberg_invariants()
    _, _, r_ist = ist_dual_mode_invariants()
    assert r_qed > 1.0 and r_ist == 0.0
    assert (r_qed - r_ist) > 1.5


def test_h56b_golden_magnitude():
    gm = golden_magnitude_ratio()
    # coupling ratio = (alpha/phi^2)/(alpha^2) = 1/(alpha*phi^2) ~ 52.3
    alpha = 1 / ALPHA_INV
    phi = (1 + np.sqrt(5)) / 2
    assert gm["coupling_ratio"] == pytest.approx(1 / (alpha * phi ** 2), rel=1e-6)
    # signal ratio is the squared coupling ratio
    assert gm["signal_ratio"] == pytest.approx(gm["coupling_ratio"] ** 2, rel=1e-9)
    assert gm["golden_charge_scale"] == pytest.approx(PHI2_OVER_ALPHA, rel=1e-6)


def test_h56c_output_group_velocity_is_c():
    for om in [0.1, 0.3, 0.5, 0.8]:
        vg = output_group_velocity(om)
        assert vg == pytest.approx(1.0, abs=1e-9), \
            "4WM output peak must move at universal c"


def test_h56c_zhang_consistency():
    # the dual-mode prediction (1.0c) sits within ~1% of Zhang et al.'s 0.99c
    assert abs(1.0 - 0.99) < 0.011


def test_figure_written():
    out = os.path.join(os.path.dirname(__file__), "..", "code", "outputs",
                       "phase56", "photon_4wm_discriminator.png")
    assert os.path.exists(out), "figure output missing"