"""
Unit tests for phase54_look_elsewhere.py -- IST Phase 54
=====================================================================
Tests the global look-elsewhere accounting: the registry of all tested
relations (with outcomes and rejection reasons) and the trial-factor
analysis of the headline hits. Encodes H54a (registry is complete enough to
answer the referee's count question) and H54b (the octet golden partition
sits in the golden-Fibonacci family -- 13/34 fits ~16x tighter than 1/phi^2
-- refining, not negating, Phase 45).

Run: cd code && python -m pytest ../tests/test_phase54_look_elsewhere.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase54_look_elsewhere import (
    PHI, REGISTRY, simple_constant_pool, trial_factor,
    headline_trial_factors, registry_stats,
)


class TestRegistry:
    def test_registry_populated(self):
        stats = registry_stats()
        assert stats["total"] >= 40          # enough to answer the referee's count
        assert "NEGATIVE" in stats["counts"]
        assert "SUPPORTED" in stats["counts"]
        assert "DERIVED" in stats["counts"]

    def test_every_entry_has_outcome_and_reason(self):
        for r in REGISTRY:
            assert r["outcome"]
            assert r["reason"]
            assert r["relation"]

    def test_demoted_entries_present(self):
        # the H42g and phi8 demotions must be in the registry (honest accounting)
        demoted = [r for r in REGISTRY if r["outcome"] == "DEMOTED"]
        assert len(demoted) >= 2

    def test_heavy_flavor_negatives_present(self):
        # Phase 53's charm/bottom negatives must be registered
        neg = [r for r in REGISTRY if r["phase"] == 53]
        assert len(neg) >= 2
        assert all(r["outcome"] == "NEGATIVE" for r in neg)


class TestTrialFactorEngine:
    def test_pool_well_populated(self):
        pool = simple_constant_pool()
        assert len(pool) > 1500

    def test_six_pi_five_is_unique(self):
        h = headline_trial_factors()[0]
        assert h["name"].startswith("m_p/m_e")
        assert h["n_match"] == 1
        assert h["closest_label"] == "6*pi^5"

    def test_one_over_34_unique(self):
        h = headline_trial_factors()[3]
        assert h["n_match"] == 1
        assert h["closest_label"] == "1/34"

    def test_koide_two_thirds_is_closest(self):
        h = headline_trial_factors()[1]
        assert h["closest_label"] == "2/3"
        assert h["closest_err"] < 1e-6


class TestOctetFamilyFinding:
    def test_split_numeric(self):
        r = (1193.154 - 1115.683) / (1318.285 - 1115.683)
        assert 0.382 < r < 0.383

    def test_fib_convergent_fits_tighter_than_inv_phi2(self):
        # the look-elsewhere finding: 13/34 ~= F7/F9 fits tighter than 1/phi^2
        r = (1193.154 - 1115.683) / (1318.285 - 1115.683)
        assert abs(r / (13 / 34) - 1) < abs(r / (1 / PHI ** 2) - 1)
        assert abs(r / (13 / 34) - 1) < 1e-3   # 13/34 inside 0.1%
        assert abs(r / (1 / PHI ** 2) - 1) < 2e-3  # 1/phi^2 inside 0.2% bar too

    def test_octet_split_multi_match_documented(self):
        # the octet hit is family-degenerate: several pool members match.
        h = headline_trial_factors()[2]
        assert h["name"].startswith("octet")
        assert h["n_match"] >= 2
        assert h["closest_label"] == "13/34"

    def test_phi2_still_in_family(self):
        # 1/phi^2 remains a member of the matching set (the family's limit)
        h = headline_trial_factors()[2]
        assert "phi^-2" in h["match_labels"]


class TestTrialFactorSemantics:
    def test_no_match_outside_tol_reports_closest(self):
        res = trial_factor(0.3823785879046932, 1e-6, simple_constant_pool())
        assert res["n_match"] == 0
        assert res["closest_label"]
