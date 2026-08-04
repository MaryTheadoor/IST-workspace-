"""
Unit tests for phase48_sm_fibonacci_mapping.py -- IST Phase 48
==============================================================
Tests the combinatorial mapping of SM multiplicities to the Fibonacci sequence.

Run: cd code && python -m pytest ../tests/test_phase48_sm_fibonacci_mapping.py -v
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase48_sm_fibonacci_mapping import generate_fibonacci, SM_MAPPING, load_phase24_data

class TestH48aFibonacciMapping:
    def test_fibonacci_sequence_generation(self):
        fibs = generate_fibonacci(9)
        assert fibs == [1, 1, 2, 3, 5, 8, 13, 21, 34]
        
    def test_all_sm_mappings_are_valid(self):
        fibs = generate_fibonacci(9)
        for label, desc, check_fn in SM_MAPPING:
            assert check_fn(fibs), f"Mapping failed for {label}: {desc}"

class TestH48bKnotFraction:
    def test_1_34_is_within_one_sigma_of_empirical_mean(self):
        df = load_phase24_data()
        if df is not None:
            empirical_fractions = df["stable_mean"] / df["N"]
            mean_emp = empirical_fractions.mean()
            std_emp = empirical_fractions.std()
            theoretical_frac = 1.0 / 34.0
            
            assert abs(theoretical_frac - mean_emp) < std_emp

class TestH48cGoldenRatio:
    def test_boson_fermion_ratio_approximates_phi(self):
        fibs = generate_fibonacci(9)
        ratio = fibs[6] / fibs[5]  # F_7 / F_6
        assert ratio == 13 / 8
        assert abs(ratio - 1.618034) < 0.01
