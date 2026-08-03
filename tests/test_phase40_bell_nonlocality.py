"""
Unit tests for phase40_bell_nonlocality.py -- IST Phase 40
==========================================================
The Bell non-locality mechanism: shared substrate as the singlet. Verifies
the singlet correlation violates CHSH (E=-cos -> Tsirelson), local hidden
variable models cannot (<= 2), and the substrate is signal-local.

Run: cd code && python -m pytest ../tests/test_phase40_bell_nonlocality.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase40_bell_nonlocality import (
    singlet_correlation, chsh_singlet, chsh_local_hidden_variable,
    substrate_singlet_pair, chsh_from_substrate_pairs,
    signal_locality_check, count_twist_adjacent_euclid_far,
)


class TestSingletCorrelation:
    def test_singlet_is_anticorrelated(self):
        assert abs(singlet_correlation(0, 0) + 1) < 1e-9     # E(0,0) = -1
        assert abs(singlet_correlation(0, np.pi / 2)) < 1e-9  # E(0,pi/2)=0

    def test_singlet_violates_chsh(self):
        S = chsh_singlet()
        assert abs(abs(S) - 2 * np.sqrt(2)) < 1e-9          # Tsirelson


class TestLHV:
    def test_lhv_cannot_exceed_two(self):
        S = chsh_local_hidden_variable()
        assert abs(S) <= 2.0 + 1e-6                          # Bell bound

    def test_lhv_strictly_less_than_singlet(self):
        assert abs(chsh_local_hidden_variable()) < abs(chsh_singlet())


class TestSubstrateSinglet:
    def test_singlet_pair_is_anticorrelated(self):
        rng = np.random.default_rng(1)
        lA, lB = substrate_singlet_pair(rng)
        assert abs((lB - lA) % (2 * np.pi) - np.pi) < 1e-9   # pi apart


class TestSignalLocality:
    def test_marginals_independent_of_bob_setting(self):
        m1, m2 = signal_locality_check()
        assert abs(m1 - m2) < 0.05                           # signal-local

    def test_marginal_is_half(self):
        # A's outcome is ~50/50 regardless of Bob (no signaling)
        m1, m2 = signal_locality_check()
        assert 0.4 < m1 < 0.6
        assert 0.4 < m2 < 0.6


class TestSubstrateGeometry:
    def test_twist_adjacent_euclid_far_pairs_exist(self):
        n, kd, ed = count_twist_adjacent_euclid_far()
        assert n > 100
        assert ed > kd

    def test_geometry_separates_substrate_from_projection(self):
        # euclid-far pairs have mean euclid distance >> klein distance
        n, kd, ed = count_twist_adjacent_euclid_far()
        assert ed / kd > 3.0
