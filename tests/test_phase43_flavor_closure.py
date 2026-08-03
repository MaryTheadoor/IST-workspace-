"""
Unit tests for phase43_flavor_closure_2loop.py -- IST Phase 43
================================================================
Tests the five hypotheses (H43a-e): the real 2-loop b1 golden cast,
the full-curve 2-loop QCD RGE overlay, the reference-systematics audit,
the exponent-basin robustness (G4 frame), and the low-scale (m_tau)
re-anchoring. Encodes the honest-negative findings.

Run: cd code && python -m pytest ../tests/test_phase43_flavor_closure.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase43_flavor_closure_2loop import (
    PHI, REFS, REF_RANGES,
    alpha_s_low_anchor,
    alpha_s_qcd_2loop,
    b_golden_exponents,
    errors,
    f_b1_cast,
    f_exact_b0,
    f_principled,
    f_scan,
    qcd_layer_count,
    range_residual,
    rms,
)


class TestH43aRealB1Cast:
    def test_k1_positive_all_flavors(self):
        # b1 steepens running: k1 > 0 for every threshold flavor
        for nf in (4, 5, 6):
            _, k1 = b_golden_exponents(nf)
            assert k1 > 0

    def test_b1_cast_differs_from_b0_only(self):
        # the DEAD CODE of H42d is gone: b0-only and b0+b1 must differ
        for nf in (4, 5, 6):
            assert f_b1_cast(nf) != f_exact_b0(nf)

    def test_b1_cast_closes_mb(self):
        # the headline finding: folding b1 in pulls m_b from +15.9% to <5%
        e = errors(f_b1_cast, upper=True)
        assert abs(e["m_b"]) < 5.0
        assert abs(errors(f_exact_b0, upper=True)["m_b"]) > 10.0

    def test_b1_cast_destroys_high_scale(self):
        # ...but over-corrects M_Z and m_t (honest negative)
        e = errors(f_b1_cast, upper=True)
        assert abs(e["M_Z"]) > 20.0
        assert abs(e["m_t"]) > 40.0

    def test_principled_rms_unchanged_baseline(self):
        # Phase 42 baseline reproduced
        r = rms(errors(f_principled, upper=True))
        assert abs(r - 8.78) < 0.05


class TestH43bFullCurveQCD:
    def test_qcd_mz_is_anchor(self):
        assert abs(alpha_s_qcd_2loop(91.1876) - 0.118) < 1e-3

    def test_qcd_running_monotone_downward(self):
        assert alpha_s_qcd_2loop(1.77686) > alpha_s_qcd_2loop(4.18)
        assert alpha_s_qcd_2loop(4.18) > alpha_s_qcd_2loop(91.1876)
        assert alpha_s_qcd_2loop(91.1876) > alpha_s_qcd_2loop(173.0)

    def test_qcd_targets_reference_ranges(self):
        # 2-loop QCD running (no 3-loop / threshold matching) tracks the
        # credible ranges. Naive running lands m_tau just below the PDG
        # band (3-loop + matching raise it to ~0.330) -- encode that honestly.
        q = {name: alpha_s_qcd_2loop(E) for name, E, _ in REFS}
        for name, (lo, hi) in REF_RANGES.items():
            assert q[name] <= hi * 1.05
        assert q["m_b"] >= REF_RANGES["m_b"][0]
        assert REF_RANGES["m_t"][0] <= q["m_t"] <= REF_RANGES["m_t"][1]

    def test_qcd_mtau_slightly_below_pdg_range(self):
        # naive 2-loop running gives alpha_s(m_tau) ~0.313, just under the
        # PDG 0.330+-0.013 band (needs 3-loop + matching)
        q = alpha_s_qcd_2loop(1.77686)
        assert q < REF_RANGES["m_tau"][0]

    def test_mt_reference_scheme_dependent(self):
        # the m_t reference 0.090 is far from 2-loop QCD running (~0.108)
        q = alpha_s_qcd_2loop(173.0)
        assert abs(q / 0.090 - 1.0) > 0.10

    def test_qcd_layer_count_positive(self):
        assert qcd_layer_count(1.77686, 91.1876) > 0

    def test_mb_to_mz_slope_conflict_is_large(self):
        # the irreducible conflict lives in the m_b -> M_Z segment
        golden = layer_count_at(91.1876) - layer_count_at(4.18)
        qcd = qcd_layer_count(4.18, 91.1876)
        assert abs(golden / qcd - 1.0) > 0.20


def layer_count_at(E):
    """Golden layer count from m_p to E (mirrors phase43 helper)."""
    from phase43_flavor_closure_2loop import C, layer_count
    return layer_count(E, f_principled, upper=True)


class TestH43cSystematics:
    def test_range_residual_zero_inside(self):
        # errors within the credible range score zero
        fake = {"m_tau": 0.0, "m_b": 0.0, "M_Z": 0.0, "m_t": 0.0}
        rr = range_residual(fake)
        assert all(v == 0.0 for v in rr.values())

    def test_mb_residual_survives_range_audit(self):
        # even against the world-average spread m_b stays outside
        rr = range_residual(errors(f_principled, upper=True))
        assert rr["m_b"] > 5.0

    def test_mz_residual_survives_range_audit(self):
        rr = range_residual(errors(f_principled, upper=True))
        assert abs(rr["M_Z"]) > 5.0


class TestH43dExponentBasin:
    def test_one_sixth_inside_basin(self):
        # the principled exponent 1/6 sits inside the RMS<10% basin
        from golden_relation_checks import base_specificity
        basin = base_specificity(
            lambda a: rms(errors(lambda nf, a=a: f_scan(nf, a), upper=True)) / 100.0,
            b_star=1.0 / 6.0, threshold=0.10, lo=0.0, hi=0.40, n=401)
        assert basin["b_star_inside"]

    def test_basin_minima_not_at_one_sixth(self):
        # honest: the basin minimum is NOT exactly 1/6 (best a ~0.148)
        from golden_relation_checks import base_specificity
        basin = base_specificity(
            lambda a: rms(errors(lambda nf, a=a: f_scan(nf, a), upper=True)) / 100.0,
            b_star=1.0 / 6.0, threshold=0.10, lo=0.0, hi=0.40, n=401)
        assert abs(basin["min_error_b"] - 1.0 / 6.0) > 0.01

    def test_basin_width_finite_and_narrow(self):
        from golden_relation_checks import base_specificity
        basin = base_specificity(
            lambda a: rms(errors(lambda nf, a=a: f_scan(nf, a), upper=True)) / 100.0,
            b_star=1.0 / 6.0, threshold=0.10, lo=0.0, hi=0.40, n=401)
        assert 0.05 < basin["width"] < 0.30


class TestH43eLowScaleAnchor:
    def test_mtau_anchor_closes_mt(self):
        e = low_anchor_errors()
        assert abs(e["m_t"]) < 1.0

    def test_mtau_anchor_mb_worsens(self):
        e = low_anchor_errors()
        assert abs(e["m_b"]) > 15.0

    def test_mtau_anchor_improves_mz_over_baseline(self):
        e = low_anchor_errors()
        assert abs(e["M_Z"]) < abs(errors(f_principled, upper=True)["M_Z"])


def low_anchor_errors():
    out = {}
    for name, E, ref in REFS:
        if name == "m_tau":
            continue
        pred = alpha_s_low_anchor(E, f_principled, upper=True)
        out[name] = 100.0 * (pred / ref - 1.0)
    return out
