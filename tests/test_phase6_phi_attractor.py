"""
Unit tests for phase6_phi_attractor.py -- IST Phase 6
======================================================
The phi-attractor hypothesis: golden ratio as a dynamical attractor of
the substrate's harmonic self-interaction (phyllotaxis mechanism), with
scale-dependent best-approach, plus the golden window in the Phase 4
fold scan.

Run: cd code && python -m pytest ../tests/test_phase6_phi_attractor.py -v
"""

import sys
import os

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_klein_laplacian import PHI
from phase6_phi_attractor import (
    ALPHA_GOLDEN, GOLDEN_ANGLE_DEG,
    orbit_gaps, gap_rigidity, rigidity_profile, three_gap_sizes,
    rigidity_matrix, fibonacci_rationals,
    atela_gole_energy, simulate_growth,
    load_phase4_scan, d_eff_profile, golden_crossing,
)


# ── 6.1 Anti-resonance selection ─────────────────────────────────────────────

class TestAntiResonance:
    def test_golden_rigidity_floor_is_one_over_phi2(self):
        r_min, n_coll = rigidity_profile(ALPHA_GOLDEN, 300)
        assert abs(r_min - 1 / PHI ** 2) < 1e-9
        assert n_coll == 301  # never collapses within 300 generations

    def test_rational_collapses_at_denominator(self):
        _, n_coll = rigidity_profile(0.25, 300)   # 1/4
        assert n_coll == 5

    def test_rational_collapse_ordering(self):
        # smaller denominators collapse earlier
        _, n5 = rigidity_profile(1 / 5, 300)
        _, n7 = rigidity_profile(2 / 7, 300)
        assert n5 < n7

    def test_golden_beats_silver_ratio(self):
        r_gold, _ = rigidity_profile(ALPHA_GOLDEN, 300)
        r_silver, _ = rigidity_profile(np.sqrt(2) - 1, 300)
        assert r_gold > r_silver

    def test_transcendental_non_noble_dips_low(self):
        r_e, _ = rigidity_profile(np.e - 2, 300)
        assert r_e < 0.2

    def test_three_gap_theorem_golden_two_sizes(self):
        # at a Fibonacci generation, the golden partition has exactly two
        # gap sizes in ratio phi
        sizes = three_gap_sizes(ALPHA_GOLDEN, 89)
        assert len(sizes) == 2
        assert abs(sizes[-1] / sizes[0] - PHI) < 1e-6

    def test_three_gap_theorem_holds_generally(self):
        sizes = three_gap_sizes(np.sqrt(2) - 1, 50)
        assert len(sizes) <= 3


# ── 6.2a Persistence: rationals peel off at their denominators ────────────────

class TestPersistence:
    def test_golden_rigidity_bounded_for_all_generations(self):
        R = rigidity_matrix([ALPHA_GOLDEN], 233)[0]
        assert np.all(R >= 1 / PHI ** 2 - 1e-9)

    def test_fibonacci_rationals_collapse_at_denominator_plus_one(self):
        for k, ratio, denom in fibonacci_rationals(k_min=4, k_max=8):
            R = rigidity_matrix([ratio], denom + 2)[0]
            assert R[denom - 1] < 1e-9      # generation denom + 1
            assert np.all(R[:denom - 2] > 0)  # alive until then

    def test_fibonacci_ratios_approach_golden(self):
        ratios = [r for _, r, _ in fibonacci_rationals(k_min=3, k_max=12)]
        devs = [abs(r - (1 - ALPHA_GOLDEN)) for r in ratios]  # mirror 1/phi
        assert devs[-1] < devs[0]
        assert devs[-1] < 1e-3


# ── 6.2b Atela-Gole variational lattice ───────────────────────────────────────

class TestAtelaGole:
    def test_golden_beats_rationals_near_close_packing(self):
        for g in [0.90, 0.94, 0.96]:
            e_gold = atela_gole_energy(g, ALPHA_GOLDEN)
            assert e_gold < atela_gole_energy(g, 0.4)
            assert e_gold < atela_gole_energy(g, 0.5)

    def test_golden_basin_deepens_toward_close_packing(self):
        # the energy advantage of golden over rational grows as g -> 1
        ratio_90 = atela_gole_energy(0.90, ALPHA_GOLDEN) / \
                   atela_gole_energy(0.90, 0.4)
        ratio_96 = atela_gole_energy(0.96, ALPHA_GOLDEN) / \
                   atela_gole_energy(0.96, 0.4)
        assert ratio_96 < ratio_90


# ── 6.2c Repulsive growth: noble attractor ────────────────────────────────────

class TestGrowth:
    @classmethod
    def setup_class(cls):
        cls.div, cls.config = simulate_growth(
            n_injections=120, v0=0.02, v0_final=0.002, mu=1.0, soft=1.0,
            steps_per_injection=40, r_max=40.0)

    def test_converges_to_noble_family_window(self):
        tail = self.div[-30:]
        # the ODE settles in a noble-family basin (golden or a neighboring
        # branch of the bifurcation tree), not at a rational angle
        assert 130.0 < np.mean(tail) < 165.0

    def test_convergence_is_tight(self):
        assert np.std(self.div[-30:]) < 3.0

    def test_lattice_is_nonempty(self):
        assert len(self.config) >= 15


# ── 6.3 Golden window in the Phase 4 fold scan ────────────────────────────────

class TestGoldenWindow:
    def test_d_eff_crosses_phi_once(self):
        fs, gs = load_phase4_scan()
        _, _, d_eff = d_eff_profile(fs, gs)
        signs = np.sign(d_eff - PHI)
        crossings = np.sum(signs[:-1] * signs[1:] < 0)
        assert crossings == 1

    def test_crossing_in_physical_window(self):
        fs, gs = load_phase4_scan()
        f_cross = golden_crossing(fs, gs)
        assert 3.0 < f_cross < 6.0

    def test_suppression_at_crossing_matches_ist_phenomenology(self):
        fs, gs = load_phase4_scan()
        f_cross = golden_crossing(fs, gs)
        suppression = 100 * (1 - 1 / f_cross)
        assert abs(suppression - 76.0) < 3.0

    def test_d_eff_descends(self):
        fs, gs = load_phase4_scan()
        _, _, d_eff = d_eff_profile(fs, gs)
        assert d_eff[0] > d_eff[-1]
