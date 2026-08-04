"""Tests for Phase 57 - the single- vs dual-strand discriminator: is the
dual-mode geometry of the photon forced?"""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase57_singlestrand_discriminator import (
    ELECTRON_TWIST, SIZES,
    bare_single_strand_spread, dual_mode_compactness, dual_mode_twist_fraction,
    helicity_mode_count, shared_speed, single_strand_twist_fraction,
)


def test_h57a_speed_is_degenerate():
    # BOTH a single strand and the dual mode translate at universal c:
    # speed alone never discriminates a photon from a fermion.
    assert shared_speed() == pytest.approx(1.0, abs=1e-9)


def test_h57a_single_strand_is_chiral_like_electron():
    # A single strand threading the Klein seam has the COMPUTED parity-
    # inversion 0.446, numerically identical to the electron knot.
    for N in SIZES:
        frac, n_cross = single_strand_twist_fraction(N)
        assert frac == pytest.approx(ELECTRON_TWIST, abs=0.002), \
            f"single strand must be electron-like, N={N} frac={frac}"
        assert n_cross > 0, "single strand must actually cross the seam"


def test_h57a_dual_mode_is_achiral():
    for N in SIZES:
        assert dual_mode_twist_fraction(N) == 0.0, \
            "dual-mode photon must be achiral (0.000)"


def test_h57a_parity_separates_models():
    # the discriminator: parity-inversion 0.446 (single) vs 0.000 (dual)
    # despite the SHARED speed.
    for N in SIZES:
        single = single_strand_twist_fraction(N)[0]
        dual = dual_mode_twist_fraction(N)
        assert (single - dual) > 0.4
        assert single > 3 * dual + 0.4


def test_h57b_two_polarizations_need_two_strands():
    n_single, n_dual = helicity_mode_count()
    assert n_single == 1, "a single strand carries one helicity mode"
    assert n_dual == 2, "the photon carries two helicity modes (E_+, E_-)"
    assert n_dual == n_single + 1


def test_h57c_bare_single_strand_disperses():
    c = bare_single_strand_spread(T=200)
    assert c[0] == pytest.approx(1.0, abs=1e-9)
    assert c[-1] < 0.2, f"bare single strand must spread, ended at {c[-1]:.4f}"
    # overall collapse: the concentration integrated over the tail is a small
    # fraction of the peak (a spreading wave, not a bound compound).
    assert c[len(c) // 2] < 0.5
    assert np.mean(c[-10:]) < 0.1


def test_h57c_dual_mode_stays_bound():
    comp = dual_mode_compactness(T=200)
    assert comp[0] == pytest.approx(1.0, abs=1e-9)
    assert abs(comp[-1] - 1.0) < 1e-6, \
        "dual-mode compound must stay compact (rung-bound, non-dispersing)"


def test_h57c_contrast_single_vs_dual():
    c = bare_single_strand_spread(T=200)
    comp = dual_mode_compactness(T=200)
    # the discriminator: the bare strand's concentration collapses while the
    # rung-bound compound's stays at 1.
    assert (1.0 - c[-1]) > 10 * (1.0 - comp[-1])


def test_figure_written():
    out = os.path.join(os.path.dirname(__file__), "..", "code", "outputs",
                       "phase57", "singlestrand_discriminator.png")
    assert os.path.exists(out), "figure output missing"
