"""
Unit tests for phase46_reference_rescope.py -- IST Phase 46
============================================================
Tests the five hypotheses (H46a-e): the m_t reference substitution, the
QCD-consistent reference set, the best-possible free-reference placement,
the two-parameter exponent decoupling, and the structural (power-law vs log)
diagnosis. Encodes the honest-negative finding: the alpha_s flavor closure is
reference-irreducible -- the m_t scheme fix makes it WORSE, and no reference
choice or exponent set closes m_b/M_Z.

Run: cd code && python -m pytest ../tests/test_phase46_reference_rescope.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase46_reference_rescope import (
    PDG_REFS, QCD_REFS, REF_RANGES,
    errors_mt,
    errors_qcd,
    f_principled,
    f_scan,
    free_reference_resid,
    range_residual_free,
    required_f_per_segment,
)
from phase43_flavor_closure_2loop import f_b1_cast, rms


class TestH46aMtReferenceFix:
    def test_0108_worsens_rms(self):
        # substituting the QCD-running m_t=0.108 raises principled RMS (8.78->12.70)
        r90 = rms(errors_mt(f_principled, 0.090, True))
        r108 = rms(errors_mt(f_principled, 0.108, True))
        assert r108 > r90 + 2.0

    def test_baseline_reproduced(self):
        # m_t=0.090 recovers the Phase 43 baseline RMS 8.78
        r = rms(errors_mt(f_principled, 0.090, True))
        assert abs(r - 8.78) < 0.05

    def test_mt_residual_worsens_at_qcd_value(self):
        e = errors_mt(f_principled, 0.108, True)
        assert abs(e["m_t"]) > 15.0


class TestH46bQcdConsistent:
    def test_qcd_mt_far_from_090(self):
        # the QCD-consistent m_t is ~0.108, far from the 0.090 convention
        assert abs(QCD_REFS["m_t"] / 0.090 - 1.0) > 0.10

    def test_qcd_scoring_worse_than_pdg(self):
        # scoring against QCD-consistent refs is worse than PDG single numbers
        r_pdg = rms(errors_mt(f_principled, 0.090, True))
        r_qcd = rms(errors_qcd(f_principled, True))
        assert r_qcd > r_pdg

    def test_qcd_mb_irreducible(self):
        # even the friendliest reference frame leaves m_b > 10% off
        e = errors_qcd(f_principled, True)
        assert abs(e["m_b"]) > 10.0


class TestH46cFreeReferences:
    def test_no_single_exponent_closes_mb_mz(self):
        # over the full a-scan with ALL refs free, m_b and M_Z stay OUT
        as_ = np.linspace(0.0, 0.6, 601)
        results = [free_reference_resid(lambda nf, a=a: f_scan(nf, a)) for a in as_]
        best = min(results, key=lambda x: x[0])
        pred, rr = best[1], best[2]
        assert pred["m_b"] > REF_RANGES["m_b"][1]
        assert pred["M_Z"] < REF_RANGES["M_Z"][0]

    def test_free_reference_best_residual_finite(self):
        # the friendliest placement still leaves a > 3% range residual
        as_ = np.linspace(0.0, 0.6, 601)
        best = min((free_reference_resid(lambda nf, a=a: f_scan(nf, a))[0] for a in as_))
        assert best * 100.0 > 3.0

    def test_one_sixth_not_optimal_under_free_refs(self):
        # the principled 1/6 is not the free-reference optimum (best ~0.110)
        r16 = free_reference_resid(lambda nf: f_scan(nf, 1.0 / 6.0))[0]
        as_ = np.linspace(0.0, 0.6, 601)
        best = min((free_reference_resid(lambda nf, a=a: f_scan(nf, a))[0] for a in as_))
        assert best < r16


class TestH46dTwoExponent:
    def test_two_knobs_do_not_close(self):
        # even with two free exponents the range residual stays ~3.9%
        from phase46_reference_rescope import f_two
        best = (1e9, None)
        for a in np.linspace(0.0, 0.6, 241):
            for b in np.linspace(0.0, 0.6, 241):
                resid, pred, _ = free_reference_resid(lambda nf, a=a, b=b: f_two(nf, a, b))
                if resid < best[0]:
                    best = (resid, pred)
        assert best[0] * 100.0 > 3.0
        rr = range_residual_free(best[1])
        assert rr["m_b"] > 0.05

    def test_two_exponent_optimum_at_zero_high(self):
        # the best high-scale exponent is ~0 (no nf=6 correction helps)
        from phase46_reference_rescope import f_two
        best = (1e9, (0.0, 1.0))
        for a in np.linspace(0.0, 0.3, 121):
            for b in np.linspace(0.0, 0.3, 121):
                resid, _, _ = free_reference_resid(lambda nf, a=a, b=b: f_two(nf, a, b))
                if resid < best[0]:
                    best = (resid, (a, b))
        assert best[1][1] < 0.05


class TestH46eStructural:
    def test_required_f_sign_flip_at_high_scale(self):
        # the required layer-base exponent flips sign above m_b: steepening
        # below (negative k) vs flattening above (positive k)
        rows = required_f_per_segment()
        k_below = [r for r in rows if float(r["lo"]) < 4.18]
        k_above = [r for r in rows if float(r["lo"]) >= 4.18]
        assert all(float(r["k_req"]) < 0 for r in k_below)
        assert all(float(r["k_req"]) > 0 for r in k_above)

    def test_required_f_mbz_opposite_to_principled(self):
        # principled f(6)=phi^-0.5 steepens; QCD needs phi^+0.82 flattening
        rows = required_f_per_segment()
        mbz = [r for r in rows if r["lo"] == "4.180"][0]
        assert float(mbz["k_req"]) > 0.7
        assert float(mbz["k_req"]) < 1.0

    def test_principled_never_close_to_qcd_profile(self):
        # every segment's required f deviates from the principled golden cast
        rows = required_f_per_segment()
        principled = {nf: f_principled(nf) for nf in (4, 5, 6)}
        for r in rows:
            lo = float(r["lo"])
            nf = 4 if lo < 1.27 else (5 if lo < 4.18 else 6)
            assert abs(float(r["f_req"]) / principled[nf] - 1.0) > 0.2
