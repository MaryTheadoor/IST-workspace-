"""Tests for Phase 59 - the pre-registered, look-elsewhere-accounted test of
the Plan 11 time-crystal dark-energy modulation."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase59_timecrystal_lookelsewhere import (
    EPS0, DELTA0, DELTA1, DATA_PATH,
    cycle_coverage, effective_trials, forecast_precision,
    global_significance, h59a_strict_amplitude, h59b_golden_period,
    scan_delta, pre_registered_anchors,
)
from oscillatory_dark_energy import load_hz_data


@pytest.fixture(scope="module")
def data():
    z, H, sigma = load_hz_data(DATA_PATH)
    return z, H, sigma


def test_anchors_exact():
    a = pre_registered_anchors()
    assert abs(a["epsilon0"] - 1 / 137.035999084 / ((1 + np.sqrt(5)) / 2) ** 2) < 1e-12
    assert abs(a["Delta0"] - np.log((1 + np.sqrt(5)) / 2)) < 1e-12
    assert abs(a["Delta1"] - (1 + np.sqrt(5)) / 2) < 1e-12


def test_h59a_strict_amplitude_anchor():
    z, H, sigma = load_hz_data(DATA_PATH)
    r = h59a_strict_amplitude(z, H, sigma, 22.88)
    # the master-equation amplitude is far below chronometer noise:
    # the improvement over LCDM must be negligible (< 1.0 in chi2)
    assert r["delta_chi2_vs_lcdm"] < 1.0, \
        "alpha/phi^2 amplitude must be invisible in H(z) data"
    assert abs(r["eps_fixed"] - EPS0) < 1e-12


def test_h59b_golden_period_anchor_well_constrained():
    z, H, sigma = load_hz_data(DATA_PATH)
    r = h59b_golden_period(z, H, sigma, 22.88)
    # at Delta0 the data span 2.5 cycles, so eps must be estimable
    assert 0.0 <= r["popt"][2] <= 0.4
    # a modest model must never be much worse than LCDM at 2 extra dof
    assert r["delta_chi2_vs_lcdm"] > -3.0


def test_h59c_scan_finds_nonzero_improvement():
    z, H, sigma = load_hz_data(DATA_PATH)
    r = scan_delta(z, H, sigma, 22.88)
    # the scan must stay inside the pre-registered grid and improve over LCDM
    assert r["grid"].min() <= r["best_Delta"] <= r["grid"].max()
    assert r["best_dchi2"] > 0.0


def test_h59c_not_significant_after_lookelsewhere():
    z, H, sigma = load_hz_data(DATA_PATH)
    r = scan_delta(z, H, sigma, 22.88)
    trials = effective_trials(r["grid"], np.log(1 + 2.36))
    p_global = global_significance(r["p_local"], trials)
    # the free-Delta oscillation must NOT be a robust detection after the
    # trial-factor penalty (Plan 11's "tension cut" was a free-fit artifact)
    assert p_global > 0.05, "free-Delta signal must be insignificant globally"


def test_h59c_look_elsewhere_promotes_local_p():
    r = {"p_local": 0.05}
    p_global = global_significance(r["p_local"], trials=10)
    assert p_global > r["p_local"] and p_global < 1.0


def test_effective_trials_counting():
    grid = np.linspace(0.3, 5.0, 200)
    n = effective_trials(grid, np.log(1 + 2.36))
    # frequency band = window length in ln(1+z) ~ 1.21; (fmax-fmin)=3.13 -> ~3.8
    assert 1 <= n <= 12


def test_cycle_coverage_golden_vs_fitted():
    L = np.log(1 + 2.36)
    assert cycle_coverage(L, DELTA0) > 2.0, "golden period spans >2 cycles"
    assert cycle_coverage(L, 1.54) < 1.0, "fitted period spans <1 cycle"


def test_forecast_monotonic_in_target_eps():
    z, H, sigma = load_hz_data(DATA_PATH)
    f_small = forecast_precision(z, H, sigma, EPS0, DELTA0)
    f_large = forecast_precision(z, H, sigma, 0.136, DELTA0)
    # a larger amplitude needs less precision to detect
    assert f_small > f_large > 0
