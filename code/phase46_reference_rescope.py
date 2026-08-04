"""
================================================================================
IST PHASE 46 - The Reference-Level Fix: Does Scheme-Dependence Re-Scope the
Flavor Closure?
================================================================================
Predecessor (Phase 43, code/phase43_flavor_closure_2loop.py):
    Honest negative: the alpha_s flavor closure is NOT closed. The conflict is
    localized to the m_b->M_Z running slope (golden 1.747 vs QCD 1.328 layers,
    +31.5% too steep). Phase 43 added an open question (sequencing note):
    whether the scheme-dependence of the m_t = 0.090 reference (vs 2-loop QCD
    running 0.108) re-scopes the closure target.

Phase 46 answers that question. It tests whether ANY legitimate reference
choice (scheme-dependent m_t, QCD-consistent running values, or free references
within credible ranges) lets a golden rule close all four references.

Hypotheses tested (H46a-e):
    H46a  The m_t reference fix. Substitute the QCD-running m_t = 0.108 for
          the 0.090 convention; re-score principled and best-exponent. Does
          the closure target re-scope? (Result: NO - RMS worsens 8.78->12.70%.)
    H46b  QCD-consistent reference set. Score every golden model against the
          exact 2-loop QCD running values at the four scales, not single-number
          PDG conventions - the "natural" reference frame for a running law.
          (Result: worse - principled RMS 12.10%.)
    H46c  Best-possible reference placement. Minimize range-residual over the
          exponent a with ALL four references free in their credible ranges.
          Can a single golden exponent close all four? (Result: NO - m_b, M_Z
          irreducible even at the friendliest placement.)
    H46d  Two-parameter exponent decoupling. Different golden exponents below
          and above the m_b threshold. Even with two free knobs, does the
          closure close? (Result: NO.)
    H46e  Structural diagnosis. The layer-base multipliers REQUIRED to match
          2-loop QCD exactly per segment. Shows golden running is a power law
          in E while QCD running is ~1/ln E (flattening at high E) - the
          m_b/M_Z conflict is reference-independent.

Success criteria:
    Closure: a legitimate reference choice + single golden rule closes all
    four < 5% with a sharp exponent basin (golden_relation_checks frame).
    Otherwise: a quantified statement that the closure is reference-irreducible
    and the m_b/M_Z conflict is power-law-vs-log running, not a reference
    artifact.

Outputs:  code/outputs/phase46/reference_rescope.csv
          code/outputs/phase46/reference_rescope.png

References:
    notes/IST_Phase_46_plan.md          (this phase's outline)
    code/phase43_flavor_closure_2loop.py (2-loop QCD RGE, ref ranges)
    code/phase42_flavor_closure.py      (piecewise golden-layer machinery)
    code/golden_relation_checks.py      (robustness frame)
    PDG 2022 alpha_s values + quark masses
===============================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from phase42_flavor_closure import (
    M_P, PHI4, THRESH, alpha_s_piecewise,
)
from phase43_flavor_closure_2loop import (
    PHI, REFS, REF_RANGES, alpha_s_qcd_2loop, f_b1_cast, f_exact_b0, f_principled,
    f_scan, qcd_layer_count, rms,
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase46")

QCD_REFS = {name: alpha_s_qcd_2loop(E) for name, E, _ in REFS}
PDG_REFS = {name: ref for name, _, ref in REFS}

# principled golden exponents of f(nf)=phi^-(nf-3)/6, for the structural contrast
PRINCIPLED_F = {nf: PHI ** (-(nf - 3) / 6.0) for nf in (4, 5, 6)}


# ───────────────────────────────────────────────────────────────────────────────
# SCORING AGAINST DIFFERENT REFERENCE SETS
# ───────────────────────────────────────────────────────────────────────────────

def errors_mt(f, mt_ref, upper=True):
    """H46a: percent error with the m_t reference replaced by mt_ref."""
    refs = dict(PDG_REFS)
    refs["m_t"] = mt_ref
    return {name: 100.0 * (alpha_s_piecewise(E, f, upper) / refs[name] - 1.0)
            for name, E, _ in REFS}


def errors_qcd(f, upper=True):
    """H46b: percent error against the exact 2-loop QCD running values."""
    return {name: 100.0 * (alpha_s_piecewise(E, f, upper) / QCD_REFS[name] - 1.0)
            for name, E, _ in REFS}


def range_residual_free(pred):
    """H46c: nearest-approach residual of PREDICTED values to the credible
    ranges. Zero inside; otherwise signed overshoot of the near boundary."""
    out = {}
    for name, E, _ in REFS:
        lo, hi = REF_RANGES[name]
        p = pred[name]
        if p < lo:
            out[name] = (lo - p) / lo
        elif p > hi:
            out[name] = (p - hi) / hi
        else:
            out[name] = 0.0
    return out


def free_reference_resid(f):
    """RMS of the range residuals for a given layer-base function f(nf)."""
    pred = {name: alpha_s_piecewise(E, f, upper=True) for name, E, _ in REFS}
    rr = range_residual_free(pred)
    return float(np.sqrt(np.mean([v ** 2 for v in rr.values()]))), pred, rr


def f_two(nf, a, b):
    """H46d: two-exponent family - a for nf<=5, b for nf=6."""
    return PHI ** (-(a if nf <= 5 else b) * (nf - 3))


def required_f_per_segment():
    """H46e: the layer-base multiplier f REQUIRED to make the golden layer count
    match 2-loop QCD exactly in each segment, and its golden exponent k."""
    segs = [(M_P, 1.27), (1.27, 4.18), (4.18, 91.1876), (91.1876, 173.0)]
    base_plain = PHI ** 4
    rows = []
    for lo, hi in segs:
        q = qcd_layer_count(lo, hi)
        f_req = (hi / lo) ** (1.0 / q) / base_plain
        k_req = float(np.log(f_req) / np.log(PHI))
        rows.append({"lo": f"{lo:.3f}", "hi": f"{hi:.3f}", "qcd_layers": f"{q:.3f}",
                     "f_req": f"{f_req:.4f}", "k_req": f"{k_req:+.4f}"})
    return rows


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = []
    out = []
    out.append("=== IST PHASE 46: The Reference-Level Fix ===")
    out.append("Does scheme-dependence (m_t 0.090 vs QCD 0.108) re-scope the flavor closure?")

    # ---- H46a: m_t reference fix ----
    out.append("\nH46a: m_t reference substitution (0.090 -> 0.108 QCD running)")
    e90 = errors_mt(f_principled, 0.090, True)
    e108 = errors_mt(f_principled, 0.108, True)
    out.append(f"  m_t=0.090: m_tau {e90['m_tau']:+.2f}%  m_b {e90['m_b']:+.2f}%  "
               f"M_Z {e90['M_Z']:+.2f}%  m_t {e90['m_t']:+.2f}%  RMS={rms(e90):.2f}%")
    out.append(f"  m_t=0.108: m_tau {e108['m_tau']:+.2f}%  m_b {e108['m_b']:+.2f}%  "
               f"M_Z {e108['M_Z']:+.2f}%  m_t {e108['m_t']:+.2f}%  RMS={rms(e108):.2f}%")
    out.append("  => the 0.090 convention was MASKING the m_t deficit; 0.108 makes the "
               "golden closure WORSE (RMS 8.78 -> 12.70). The reference fix does NOT "
               "re-scope the target.")
    rows.append({"hyp": "H46a", "model": "principled, m_t=0.090",
                 "m_tau": f"{e90['m_tau']:+.2f}%", "m_b": f"{e90['m_b']:+.2f}%",
                 "M_Z": f"{e90['M_Z']:+.2f}%", "m_t": f"{e90['m_t']:+.2f}%",
                 "note": f"RMS={rms(e90):.2f}% (baseline)"})
    rows.append({"hyp": "H46a", "model": "principled, m_t=0.108",
                 "m_tau": f"{e108['m_tau']:+.2f}%", "m_b": f"{e108['m_b']:+.2f}%",
                 "M_Z": f"{e108['M_Z']:+.2f}%", "m_t": f"{e108['m_t']:+.2f}%",
                 "note": "reference fix FAILS (RMS worsens)"})

    # ---- H46b: QCD-consistent reference set ----
    out.append("\nH46b: score against the exact 2-loop QCD running values")
    for nm, f in [("principled", f_principled), ("exact b0", f_exact_b0),
                  ("b1 cast", f_b1_cast),
                  ("scan best a=0.148", lambda nf: f_scan(nf, 0.148))]:
        e = errors_qcd(f, True)
        out.append(f"  [{nm:18s}] m_tau {e['m_tau']:+.2f}%  m_b {e['m_b']:+.2f}%  "
                   f"M_Z {e['M_Z']:+.2f}%  m_t {e['m_t']:+.2f}%  RMS={rms(e):.2f}%")
        rows.append({"hyp": "H46b", "model": nm + " (QCD-consistent)",
                     "m_tau": f"{e['m_tau']:+.2f}%", "m_b": f"{e['m_b']:+.2f}%",
                     "M_Z": f"{e['M_Z']:+.2f}%", "m_t": f"{e['m_t']:+.2f}%",
                     "note": f"RMS={rms(e):.2f}%"})

    # ---- H46c: best-possible reference placement ----
    out.append("\nH46c: single exponent, ALL references free in their credible ranges")
    best = (1e9, None, None)
    for a in np.linspace(0.0, 0.6, 601):
        resid, pred, _ = free_reference_resid(lambda nf, a=a: f_scan(nf, a))
        if resid < best[0]:
            best = (resid, a, pred)
    a_best, pred = best[1], best[2]
    rr = range_residual_free(pred)
    out.append(f"  best a={a_best:.3f}  range-resid RMS={best[0]*100:.2f}%")
    for name, E, _ in REFS:
        p = pred[name]
        lo, hi = REF_RANGES[name]
        if lo <= p <= hi:
            state = "IN"
        else:
            over = 100.0 * (p - hi) / hi if p > hi else 100.0 * (lo - p) / lo
            state = f"OUT ({over:+.1f}%)"
        out.append(f"      {name:6s} pred={p:.4f}  range=[{lo:.4f},{hi:.4f}]  {state}")
    rows.append({"hyp": "H46c", "model": f"free-ref single-exp (a={a_best:.3f})",
                 "m_tau": f"{pred['m_tau']:.4f}", "m_b": f"{pred['m_b']:.4f}",
                 "M_Z": f"{pred['M_Z']:.4f}", "m_t": f"{pred['m_t']:.4f}",
                 "note": "m_b, M_Z OUT even with free references"})

    # ---- H46d: two-parameter exponent decoupling ----
    out.append("\nH46d: two exponents (a for nf<=5, b for nf=6), refs free in ranges")
    best2 = (1e9, None, None)
    for a in np.linspace(0.0, 0.6, 241):
        for b in np.linspace(0.0, 0.6, 241):
            resid, pred, _ = free_reference_resid(lambda nf, a=a, b=b: f_two(nf, a, b))
            if resid < best2[0]:
                best2 = (resid, (a, b), pred)
    a2, b2, pred2 = best2[1][0], best2[1][1], best2[2]
    rr2 = range_residual_free(pred2)
    out.append(f"  best (a,b)=({a2:.3f},{b2:.3f})  range-resid RMS={best2[0]*100:.2f}%")
    for name, E, _ in REFS:
        p = pred2[name]
        lo, hi = REF_RANGES[name]
        state = "IN" if lo <= p <= hi else "OUT"
        out.append(f"      {name:6s} pred={p:.4f}  range=[{lo:.4f},{hi:.4f}]  {state}")
    rows.append({"hyp": "H46d", "model": f"two-exp (a={a2:.3f},b={b2:.3f})",
                 "m_tau": f"{pred2['m_tau']:.4f}", "m_b": f"{pred2['m_b']:.4f}",
                 "M_Z": f"{pred2['M_Z']:.4f}", "m_t": f"{pred2['m_t']:.4f}",
                 "note": "two free knobs still do not close m_b/M_Z"})

    # ---- H46e: structural diagnosis ----
    out.append("\nH46e: required layer-base to match 2-loop QCD exactly (per segment)")
    for row in required_f_per_segment():
        out.append(f"  segment {row['lo']:>8}->{row['hi']:<9} qcd_layers={row['qcd_layers']:>6}  "
                   f"f_req={row['f_req']}  phi^k={row['k_req']}")
    out.append("  vs principled f(nf)=phi^-(nf-3)/6:")
    for nf in (4, 5, 6):
        out.append(f"      f({nf}) = {PRINCIPLED_F[nf]:.4f}  (phi^-{(nf-3)/6:+.3f})")
    out.append("  => the m_b->M_Z segment needs f ~ phi^+0.82 (FLATTENING), opposite to the")
    out.append("     principled steepening phi^-0.5. Golden running is a power law in E;")
    out.append("     QCD running is ~1/ln E, flattening at high E. The m_b/M_Z conflict is")
    out.append("     REFERENCE-INDEPENDENT: a shape mismatch, not a reference artifact.")

    csv_path = os.path.join(OUT_DIR, "reference_rescope.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["hyp", "model", "m_tau", "m_b", "M_Z", "m_t", "note"])
        w.writeheader()
        w.writerows(rows)
    out.append(f"\nWrote {csv_path}")

    make_figure(best[1], best2[1], required_f_per_segment())
    out.append(f"Wrote {OUT_DIR}")

    print("\n".join(out))


def make_figure(a_free, ab_two, seg_rows):
    """Three panels: reference-fix impact, exponent-basin residual under free
    references, and the required-f structural profile."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # panel 1: m_t substitution effect on principled RMS
    mts = np.linspace(0.085, 0.112, 60)
    rms_curve = [rms(errors_mt(f_principled, mt, True)) for mt in mts]
    axes[0].plot(mts, rms_curve)
    axes[0].axvline(0.090, color="gray", ls=":", label="0.090 convention")
    axes[0].axvline(0.108, color="gray", ls="--", label="0.108 QCD running")
    axes[0].set_xlabel("m_t reference value (alpha_s)"); axes[0].set_ylabel("principled RMS (%)")
    axes[0].set_title("H46a: m_t reference fix worsens closure")
    axes[0].legend(fontsize=8)

    # panel 2: exponent basin under free references (H46c)
    as_ = np.linspace(0.0, 0.6, 601)
    resid_curve = [free_reference_resid(lambda nf, a=a: f_scan(nf, a))[0] for a in as_]
    axes[1].plot(as_, np.array(resid_curve) * 100.0)
    axes[1].axvline(1.0 / 6.0, color="gray", ls=":", label="1/6")
    axes[1].axvline(a_free, color="tab:red", ls="--", label=f"best a={a_free:.3f}")
    axes[1].set_xlabel("exponent a"); axes[1].set_ylabel("free-reference range-resid RMS (%)")
    axes[1].set_title("H46c: no single exponent closes free refs")
    axes[1].legend(fontsize=8)

    # panel 3: required-f structural profile (H46e)
    k_reqs = [float(r["k_req"]) for r in seg_rows]
    k_princ = [-(nf - 3) / 6.0 for nf in (4, 5, 6)]
    axes[2].plot(range(len(k_reqs)), k_reqs, "o-", label="required phi^k (QCD match)")
    axes[2].plot(range(len(k_princ)), k_princ, "s--", label="principled phi^k")
    axes[2].axhline(0, color="k", lw=0.6)
    axes[2].set_xticks(range(len(k_reqs)))
    axes[2].set_xticklabels([f"{r['lo']}->{r['hi']}" for r in seg_rows], rotation=25, fontsize=7)
    axes[2].set_ylabel("golden exponent k"); axes[2].set_xlabel("segment")
    axes[2].set_title("H46e: required f(nf) vs principled (sign flip at high E)")
    axes[2].legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "reference_rescope.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()