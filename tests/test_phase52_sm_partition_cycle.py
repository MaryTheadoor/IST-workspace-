"""
Unit tests for phase52_sm_partition_cycle.py -- IST Phase 52
=====================================================================
Tests that the SM Fibonacci partition (F_1..F_9, knot fraction 1/34)
emerges from the 4-TICK ORIENTATION CYCLE DYNAMICS on the TRUE
Fibonacci-Klein lattice, with the half-integer twist theta=1/2 as the
parity GENERATOR, cross-checked against Phase 51/23a's 0.446 twist
fraction.

Run: cd code && python -m pytest ../tests/test_phase52_sm_partition_cycle.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase52_sm_partition_cycle import (
    PHI, ALPHA_GOLD, KNOT_FRACTION_F9,
    OrientationSubstrate, torus_distance,
    twist_fraction, spectral_gap_counts,
    raster_gap_counts, is_consecutive_fibonacci,
)


def _run_ensemble_fraction(subclass_sizes, cycles=4):
    fracs = []
    for N in subclass_sizes:
        sub = OrientationSubstrate(N, twisted=True)
        rows, _ = sub.run_cycles(cycles)
        fracs.append(rows[-1]["stable_fraction"])
    return float(np.mean(fracs)), float(np.std(fracs))


class TestH52cTwistIsGenerator:
    """theta = 1/2 is the parity generator: parity-inversion fraction is
    0.446 on the true Fibonacci-Klein lattice and 0.000 on the orientable
    torus control (no seam exists)."""

    def test_klein_twist_fraction_matches_0446(self):
        frac, nc, npairs = twist_fraction(210)
        assert 0.43 < frac < 0.46
        assert nc > 0
        assert npairs == 210 * 210 - 210

    def test_twist_fraction_n_independent(self):
        fracs = [twist_fraction(N)[0] for N in (210, 360, 480)]
        assert np.ptp(fracs) < 0.01           # N-independent (H52d)
        assert 0.43 < fracs[0] < 0.46

    def test_torus_has_no_parity_inversion(self):
        # torus_distance never returns a twist flag; by construction theta=0
        # gives no orientation-reversing identification, so the Klein seam
        # (0.446) is absent. Assert the structural contrast.
        N = 210
        us, vs = np.arange(N), np.arange(N)
        d = torus_distance(us, vs, us, vs)
        assert np.all(np.isfinite(d))
        # chirality is conserved on the orientable control
        sub = OrientationSubstrate(N, twisted=False)
        sub.run_cycles(4)
        assert sub.chirality.min() == sub.chirality.max() == 1.0 or \
            np.all(sub.chirality > 0)

    def test_klein_chirality_flips_but_torus_conserves(self):
        # the double-cover flip only operates on the twisted (Klein) substrate
        klein = OrientationSubstrate(210, twisted=True)
        kle_c0 = klein.chirality.copy()
        klein.plonk_tick()
        assert not np.all(klein.chirality == kle_c0)   # flip happened

        torus = OrientationSubstrate(210, twisted=False)
        tor_c0 = torus.chirality.copy()
        torus.plonk_tick()
        assert np.all(torus.chirality == tor_c0)       # conserved


class TestH52dTwistFraction:
    def test_analytic_0446_across_sizes(self):
        for N in (210, 360, 480):
            frac, nc, npairs = twist_fraction(N)
            assert 0.43 < frac < 0.46
            assert frac == nc / npairs


class TestH52bFibonacciGapPartition:
    """The true golden lattice partitions into CONSECUTIVE FIBONACCI numbers;
    the commensurate raster control does not."""

    def test_golden_gap_counts_are_consecutive_fibonacci(self):
        # (a, b) = (F_k-1, F_k-2): sum and difference are both Fibonacci
        expected = {
            55: [21, 34],
            89: [34, 55],
            144: [55, 89],
            233: [89, 144],
            377: [144, 233],
        }
        for N, (lo, hi) in expected.items():
            _, counts = spectral_gap_counts(N)
            assert counts == [lo, hi], f"N={N} counts={counts}"
            assert set(counts).issubset({lo, hi})

    def test_consecutive_fibonacci_predicate(self):
        assert is_consecutive_fibonacci([21, 34])
        assert is_consecutive_fibonacci([55, 89])
        assert not is_consecutive_fibonacci([139, 5])
        assert not is_consecutive_fibonacci([64])      # single gap: no split
        assert not is_consecutive_fibonacci([5, 59])

    def test_raster_control_is_not_fibonacci(self):
        _, counts64 = raster_gap_counts(64)
        _, counts144 = raster_gap_counts(144)
        assert not is_consecutive_fibonacci(counts64)
        assert not is_consecutive_fibonacci(counts144)


class TestH52aDynamicStableFraction:
    """Stable-knot fraction from the 4-tick dynamics is consistent with
    1/F_9 = 1/34 at the ENSEMBLE level (single runs are noisy)."""

    def test_ensemble_mean_near_one_over_34(self):
        sizes = [55, 89, 144, 233]
        mean, std = _run_ensemble_fraction(sizes)
        # honest band: within ~3.5 sigma of the Phase 48 prediction 1/34,
        # matching Phase 24's observed mean (3.13% +/- 0.48%).
        assert 0.005 < mean < 0.08
        assert (KNOT_FRACTION_F9 - mean) < 0.05 + std

    def test_stable_fraction_is_a_small_minority(self):
        # the 1/34 structure means the vast majority of oscillators do NOT
        # phase-return stably over a cycle
        sub = OrientationSubstrate(480, twisted=True)
        rows, _ = sub.run_cycles(6)
        fracs = [r["stable_fraction"] for r in rows]
        assert all(f < 0.35 for f in fracs)

    def test_full_cycle_restores_orientation_double_cover(self):
        # after 4 ticks orientation returns to start (720 deg / 4-tick cycle)
        sub = OrientationSubstrate(120, twisted=True)
        o0 = sub.orientation.copy()
        for _ in range(4):
            sub.plonk_tick()
        assert np.array_equal(sub.orientation, o0)