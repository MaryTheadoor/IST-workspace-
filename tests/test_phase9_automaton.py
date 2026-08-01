"""
Unit tests for phase9_game_of_life_substrate.py -- IST Phase 9
===============================================================
Golden-filter Conway automaton: golden fraction increase,
entropy decrease, population stabilisation.

Run: cd code && python -m pytest ../tests/test_phase9_automaton.py -v
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase9_game_of_life_substrate import ISTAutomaton


class TestAutomaton:
    @classmethod
    def setup_class(cls):
        cls.a = ISTAutomaton(n=40, alive_frac=0.34, seed=3)
        cls.rows = cls.a.run(n_steps=200)

    def test_golden_fraction_increases(self):
        init = self.rows[0]["golden_fraction"]
        final = self.rows[-1]["golden_fraction"]
        assert final > init * 1.1, f"golden frac {init:.3f} -> {final:.3f}"

    def test_entropy_decreases(self):
        init = self.rows[0]["entropy"]
        final = self.rows[-1]["entropy"]
        assert final < init, f"entropy {init:.3f} -> {final:.3f}"

    def test_population_stabilises(self):
        last10 = [r["live_count"] for r in self.rows[-10:]]
        assert np.std(last10) / max(np.mean(last10), 1) < 0.10

    def test_structures_exist(self):
        assert self.rows[-1]["structures"] > 0

    def test_population_does_not_explode(self):
        for r in self.rows:
            assert r["live_count"] < self.a.N * 0.9

    def test_population_does_not_collapse(self):
        assert self.rows[-1]["live_count"] > 0

    def test_golden_fraction_bounded(self):
        for r in self.rows:
            assert 0 <= r["golden_fraction"] <= 1.0
