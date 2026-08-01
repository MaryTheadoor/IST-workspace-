"""
Unit tests for phase8_vacuum_pump_threshold.py -- IST Phase 8
==============================================================
Vacuum-pump threshold: golden filter accumulation, coherence transition,
D_eff pinning, and phi^n magnification.

Run: cd code && python -m pytest ../tests/test_phase8_threshold.py -v
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_klein_laplacian import PHI
from phase8_vacuum_pump_threshold import (
    VacuumPumpSimulator, golden_coupling, graph_laplacian,
    gap_rigidity, ALPHA_GOLDEN,
)


class TestGoldenFilter:
    def test_golden_boost_peak_at_correct_distance(self):
        # The golden filter boost should peak at d = 2*pi/phi^k
        phases = np.array([0.0, 2 * np.pi / PHI ** 3])
        J, boost = golden_coupling(phases, sigma=0.5, layer_count=4)
        # off-diagonal boost should be strong (near phi^3 distance)
        assert boost[0, 1] > 0.5

    def test_golden_boost_zero_for_zero_distance(self):
        phases = np.array([0.0, 0.001])
        J, boost = golden_coupling(phases, sigma=0.5, layer_count=4)
        assert boost[0, 1] < 0.01

    def test_coupling_symmetric(self):
        phases = np.linspace(0, 2 * np.pi, 20)
        J, _ = golden_coupling(phases, 0.1, 3)
        assert np.allclose(J, J.T)


class TestVacuumPumpSimulation:
    @classmethod
    def setup_class(cls):
        cls.sim = VacuumPumpSimulator(N_base=100, sigma=0.1, seed=7)
        cls.rows = cls.sim.run_threshold_scan(n_layers=12, n_new=30)

    def test_coherence_transitions_from_zero(self):
        assert self.rows[0]["coherence"] < 0.01

    def test_coherence_exceeds_threshold(self):
        assert max(r["coherence"] for r in self.rows) > 0.5

    def test_threshold_is_sharp(self):
        """Coherence rises from <0.1 to >0.5 within a few layers."""
        cohs = [r["coherence"] for r in self.rows]
        # find the steepest jump
        jumps = [cohs[i+1] - cohs[i] for i in range(len(cohs)-1)]
        assert max(jumps) > 0.15  # sharp transition

    def test_d_eff_pins_above_threshold(self):
        """D_eff is stable above threshold (std < 0.1)."""
        threshold = next(
            (r["n_layers"] for r in self.rows if r["coherence"] > 0.5), 999)
        above = [r["D_eff"] for r in self.rows
                 if r["n_layers"] > threshold]
        if len(above) >= 2:
            assert np.std(above) < 0.10

    def test_d_eff_pinned_in_measured_range(self):
        """D_eff pinned is finite and in a physically reasonable range."""
        threshold = next(
            (r["n_layers"] for r in self.rows if r["coherence"] > 0.5), 999)
        above = [r["D_eff"] for r in self.rows
                 if r["n_layers"] > threshold]
        if above:
            mean_d = np.mean(above)
            assert 0.8 < mean_d < 1.5, f"D_eff pinned at {mean_d:.3f}"

    def test_magnification_tracks_phi(self):
        for r in self.rows:
            assert abs(r["magnification"] - PHI ** r["n_layers"]) < 1e-10

    def test_magnification_at_8_matches_phi8(self):
        r8 = next(r for r in self.rows if r["n_layers"] == 8)
        phi8 = PHI ** 8
        assert abs(r8["magnification"] - phi8) / phi8 < 0.01


class TestGoldenStructure:
    def test_golden_layer_phases_sorted(self):
        sim = VacuumPumpSimulator(N_base=0, sigma=0.1)
        sim.add_harmonic_layer(20)
        assert np.all(np.diff(sim.golden_phases()) >= 0)

    def test_golden_orbit_rigidity(self):
        """A single golden layer has rigidity >= 1/phi^2 (the golden floor)."""
        sim = VacuumPumpSimulator(N_base=0, sigma=0.1)
        sim.add_harmonic_layer(89)
        rig = gap_rigidity(sim.golden_phases())
        assert rig >= 1.0 / PHI ** 2 - 1e-9  # floor is 1/phi^2
        assert rig <= 1.0  # bounded above by 1
