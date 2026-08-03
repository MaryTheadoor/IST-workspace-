"""
================================================================================
IST PHASE 43 - The m_b Anomaly and the 2-Loop Golden Closure
================================================================================
Predecessor (Phase 42, code/phase42_flavor_closure.py):
    Upper-convention principled residual: m_tau -2.0%, m_b +15.9%,
    M_Z -6.75%, m_t -2.2%, RMS 8.78%. Best single exponent a=0.150: 8.70%.
    The closure conflict is a running-slope mismatch: m_b must come DOWN
    and M_Z must go UP, i.e. the golden running between m_b and M_Z is
    too steep.

Three gaps closed here (review findings):
    (A) H42d's 2-loop b1 term was DEAD CODE (f_b1 used 0.0*k1). Phase 43
        folds the real b1 golden cast and reports the sign honestly.
    (B) Scoring used only 4 points. Phase 43 overlays the full golden-layer
        curve against the exact 2-loop QCD running over [m_p, M_Z] and
        measures where the shape mismatch peaks.
    (C) References were single numbers. Phase 43 audits credible ranges
        (PDG uncertainties + scheme dependence) and re-scores against them.

Hypotheses tested (H43a-e):
    H43a  Real b1 golden cast: f(n_f) = phi^{-(k0 + k1)}, k0/k1 = golden
          exponents of b0(n_f)/b0(3), b1(n_f)/b1(3). k1 > 0 for all n_f
          (b1 *steepens* running), so physical intuition says the wrong
          direction for the m_b/M_Z conflict -- test it and report sign.
    H43b  Full-curve 2-loop QCD RGE comparison. Integrate the MS-bar RGE
          d a_s/d ln E = -b0 a_s^2 - b1 a_s^3 (a_s = alpha_s/pi) from
          alpha_s(M_Z)=0.118 across the thresholds and overlay the golden
          layer curve. Report max deviation and its location.
    H43c  Reference-systematics audit. m_tau 0.330+-0.013, m_b world
          average range, M_Z 0.118+-0.001, m_t 0.090 scheme-dependent
          (2-loop QCD running gives 0.108). Re-score against the ranges.
    H43d  Exponent-basin robustness (G4 applied to the closure). Scan the
          exponent a, measure the RMS basin width, and check whether the
          principled 1/6 and the best-fit 0.150 sit in a sharp basin.
    H43e  Low-scale (m_tau) re-anchoring. Anchor alpha_s(m_tau)=0.330
          exactly, run UP, and treat m_b/M_Z/m_t as consistency checks.
          Contrasts with the failed H42e high-scale (M_Z) anchor.

Success criteria:
    Closure: one golden rule closing all four references < 5% each with a
    sharp exponent basin. Otherwise: an honest, quantified statement of the
    irreducible residual and its cause (b0-vs-b1 curvature, boundary
    placement, or reference systematics).

Outputs:  code/outputs/phase43/flavor_closure_2loop.csv
          code/outputs/phase43/flavor_closure_2loop.png

References:
    notes/IST_Phase_43_plan.md          (this phase's outline)
    code/phase42_flavor_closure.py      (predecessor: piecewise machinery)
    code/golden_relation_checks.py      (G1-G4 robustness frame; H43d)
    PDG 2022 alpha_s values + quark masses
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numba import njit

from golden_relation_checks import base_specificity
from phase42_flavor_closure import (
    B0, B1, C, PHI, REFS, THRESH,
    alpha_s_piecewise,
    f_exact_b0,
    f_principled,
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase43")

# References: (name, E, alpha_s) -- same as Phase 38/39/42
REFS = [("m_tau", 1.77686, 0.330), ("m_b", 4.18, 0.220),
        ("M_Z", 91.1876, 0.118), ("m_t", 173.0, 0.090)]

# H43c: credible reference ranges (PDG quoted uncertainties + scheme spread)
REF_RANGES = {
    "m_tau": (0.330 - 0.013, 0.330 + 0.013),
    "m_b": (0.210, 0.240),        # world-average spread, lattice/PDG
    "M_Z": (0.117, 0.119),        # PDG 2022 0.118 +- 0.001
    "m_t": (0.090, 0.108),        # 0.090 scheme convention vs QCD running 0.108
}


# ───────────────────────────────────────────────────────────────────────────────
# H43a: REAL 2-LOOP b1 GOLDEN CAST
# ───────────────────────────────────────────────────────────────────────────────

def b_golden_exponents(nf):
    """Golden exponents of the (b0, b1) ratios: k_i = -ln(b_i(n_f)/b_i(3))/ln(phi).
    Returns (k0, k1)."""
    k0 = -np.log(B0[nf] / B0[3]) / np.log(PHI)
    k1 = -np.log(B1[nf] / B1[3]) / np.log(PHI)
    return k0, k1


def f_b1_cast(nf):
    """H43a: the REAL b1 golden cast -- b1 folded in, not dead code.
    f(n_f) = phi^{-(k0 + k1)}. Both coefficients enter the layer base."""
    k0, k1 = b_golden_exponents(nf)
    return PHI ** (-(k0 + k1))


# ───────────────────────────────────────────────────────────────────────────────
# H43b: 2-LOOP QCD RGE (MS-BAR)
# ───────────────────────────────────────────────────────────────────────────────

_QCD_GRID = np.geomspace(0.9, 300.0, 60000)


@njit(cache=True)
def _qcd_integrate_jit(es, lnmu, iz, out):
    """numba-compiled 2-loop MS-bar running: d alpha_s/d ln E =
    -(33-2n_f)alpha_s^2/(6pi) - (153-19n_f)alpha_s^3/(12pi^2), flavor
    count from the scale. Integrates downward from M_Z to 0.9 GeV and
    upward to 300 GeV in place on `out`."""
    a = 0.1180
    for i in range(iz, 0, -1):
        e = es[i]
        nf = 6 if e >= 173.0 else (5 if e >= 4.18 else (4 if e >= 1.27 else 3))
        dln = lnmu[i - 1] - lnmu[i]
        a += dln * (-(33.0 - 2.0 * nf) / (6.0 * np.pi) * a ** 2
                    - (153.0 - 19.0 * nf) / (12.0 * np.pi ** 2) * a ** 3)
        out[i - 1] = a
    a = 0.1180
    for i in range(iz, len(lnmu) - 1):
        e = es[i]
        nf = 6 if e >= 173.0 else (5 if e >= 4.18 else (4 if e >= 1.27 else 3))
        dln = lnmu[i + 1] - lnmu[i]
        a += dln * (-(33.0 - 2.0 * nf) / (6.0 * np.pi) * a ** 2
                    - (153.0 - 19.0 * nf) / (12.0 * np.pi ** 2) * a ** 3)
        out[i + 1] = a
    return out


def _qcd_integrate():
    """2-loop MS-bar running from alpha_s(M_Z)=0.118 across the thresholds,
    integrated once (numba-JIT compiled for speed)."""
    lnmu = np.log(_QCD_GRID)
    iz = np.searchsorted(_QCD_GRID, 91.1876)
    out = np.empty_like(lnmu)
    out[iz] = 0.1180
    return _qcd_integrate_jit(_QCD_GRID, lnmu, iz, out)


_QCD_CURVE = _qcd_integrate()


def alpha_s_qcd_2loop(E):
    """2-loop MS-bar alpha_s(E) from alpha_s(M_Z)=0.118, interpolated on the
    precomputed QCD running curve."""
    return float(np.interp(E, _QCD_GRID, _QCD_CURVE))


def qcd_layer_count(E1, E2):
    """Layer count between E1 and E2 in the exact 2-loop QCD running:
    ln(alpha(E1)/alpha(E2))/ln(phi)."""
    return np.log(alpha_s_qcd_2loop(E1) / alpha_s_qcd_2loop(E2)) / np.log(PHI)


# ───────────────────────────────────────────────────────────────────────────────
# SCORING
# ───────────────────────────────────────────────────────────────────────────────

def errors(f, upper=True):
    """Percent error of the piecewise model at each of the four references."""
    return {name: 100.0 * (alpha_s_piecewise(e, f, upper) / ref - 1.0)
            for name, e, ref in REFS}


def rms(errs):
    return float(np.sqrt(np.mean([v ** 2 for v in errs.values()])))


def range_residual(errs):
    """H43c: closest-approach residual to the credible reference ranges.
    Zero inside the range; otherwise the signed overshoot relative to the
    near boundary, in percent of the reference value."""
    out = {}
    ref_by_name = {name: ref for name, _, ref in REFS}
    for name, v in errs.items():
        lo, hi = REF_RANGES[name]
        ref = ref_by_name[name]
        if lo <= ref * (1.0 + v / 100.0) <= hi:
            out[name] = 0.0
        else:
            pred = ref * (1.0 + v / 100.0)
            d = pred - hi if pred > hi else pred - lo
            out[name] = 100.0 * d / ref
    return out


def f_scan(nf, a):
    """Single-exponent family f(n_f) = phi^{-a(n_f-3)} (H43d / H42c)."""
    return PHI ** (-a * (nf - 3))


# ───────────────────────────────────────────────────────────────────────────────
# H43e: LOW-SCALE (m_tau) RE-ANCHORING
# ───────────────────────────────────────────────────────────────────────────────

def layer_count(E, f, upper=True):
    """Cumulative golden layer count from m_p to E (n such that
    alpha_s(E) = C * phi^{-n})."""
    return -np.log(alpha_s_piecewise(E, f, upper) / C) / np.log(PHI)


def alpha_s_low_anchor(E, f, upper=True):
    """H43e: anchor alpha_s(m_tau) = 0.330 exactly and run UP.
    alpha_s(E) = 0.330 * phi^{-(n(E) - n(m_tau))}."""
    n_tau = layer_count(1.77686, f, upper)
    return 0.330 * PHI ** (-(layer_count(E, f, upper) - n_tau))


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = []
    out = []
    out.append("=== IST PHASE 43: The m_b Anomaly and the 2-Loop Golden Closure ===")
    out.append("alpha_s(E) = (1/phi^2) phi^{-n(E)}, flavor-dependent layer bases\n")

    # ---- H43a: real b1 golden cast ----
    out.append("H43a: real b1 golden cast f(n_f) = phi^{-(k0 + k1)}")
    for nf in (4, 5, 6):
        k0, k1 = b_golden_exponents(nf)
        out.append(f"    n_f={nf}: k0={k0:+.4f}  k1={k1:+.4f}  "
                   f"(b1 steepens running: k1>0)")
    for nm, f in [("b0-only (k0)", f_exact_b0), ("b1 golden cast (k0+k1)", f_b1_cast)]:
        e = errors(f, upper=True)
        r = rms(e)
        rows.append({"model": nm, "convention": "upper", "m_tau": f"{e['m_tau']:+.2f}%",
                     "m_b": f"{e['m_b']:+.2f}%", "M_Z": f"{e['M_Z']:+.2f}%",
                     "m_t": f"{e['m_t']:+.2f}%", "RMS": f"{r:.2f}%"})
        out.append(f"  [{nm}, upper] RMS={r:.2f}%")
        for name, val in e.items():
            out.append(f"      {name:6s} {val:+.2f}%")
    out.append("    => folding b1 in CLOSES m_b (+15.95% -> +0.75%): the m_b residual "
               "IS the 2-loop curvature. But the b1 golden cast over-corrects the "
               "high scale (M_Z -42%, m_t -76%): the fixed-layer golden structure "
               "cannot reproduce the energy-dependent b1 curvature of QCD. "
               "b0-only and b0+b1 bracket the conflict; neither closes all four.\n")

    # ---- H43b: full-curve 2-loop QCD comparison ----
    out.append("H43b: full-curve 2-loop QCD RGE (MS-bar) vs golden layer curve")
    qcd_refs = {name: alpha_s_qcd_2loop(E) for name, E, _ in REFS}
    out.append("    2-loop QCD targets (from alpha_s(M_Z)=0.118):")
    for name, E, ref in REFS:
        q = qcd_refs[name]
        out.append(f"      {name:6s} {ref:<6.3f} -> QCD {q:.4f}  ({100.0 * (q / ref - 1.0):+.1f}% vs ref)")
    es = np.geomspace(0.95, 91.1876, 300)
    golden_curve = [alpha_s_piecewise(e, f_principled, upper=True) for e in es]
    qcd_curve = [alpha_s_qcd_2loop(e) for e in es]
    dev = np.array([abs(g / q - 1.0) for g, q in zip(golden_curve, qcd_curve)])
    imax = int(np.argmax(dev))
    out.append(f"    max |golden/QCD - 1| = {dev.max() * 100:.2f}% at E = {es[imax]:.2f} GeV")
    mid = int(np.argmin(np.abs(es - 10.0)))
    out.append(f"    |golden/QCD - 1| at 10 GeV = {dev[mid] * 100:.2f}%")
    qcd_layers = qcd_layer_count(1.77686, 91.1876)
    golden_layers = layer_count(91.1876, f_principled, upper=True) - \
        layer_count(1.77686, f_principled, upper=True)
    out.append(f"    layer count m_tau->M_Z: golden {golden_layers:.3f} vs QCD {qcd_layers:.3f} "
               f"(golden runs {100.0 * (golden_layers / qcd_layers - 1):+.1f}% too steep)")
    g_seg = layer_count(91.1876, f_principled, upper=True) - \
        layer_count(4.18, f_principled, upper=True)
    q_seg = qcd_layer_count(4.18, 91.1876)
    out.append(f"    m_b->M_Z segment: golden {g_seg:.3f} vs QCD {q_seg:.3f} layers "
               f"({100.0 * (g_seg / q_seg - 1):+.1f}% -- THE slope-conflict segment)\n")
    rows.append({"model": "2-loop QCD target alpha_s(m_t)", "convention": "QCD running",
                 "m_tau": f"{qcd_refs['m_tau']:.4f}", "m_b": f"{qcd_refs['m_b']:.4f}",
                 "M_Z": f"{qcd_refs['M_Z']:.4f}", "m_t": f"{qcd_refs['m_t']:.4f}", "RMS": "-"})

    # ---- H43c: reference-systematics audit ----
    out.append("H43c: reference-systematics audit (closest-approach to credible ranges)")
    for nm, f in [("principled (nf-3)/6", f_principled), ("b1 cast (k0+k1)", f_b1_cast)]:
        e = errors(f, upper=True)
        rr = range_residual(e)
        out.append(f"  [{nm}] raw: " + "  ".join(f"{k} {v:+.1f}%" for k, v in e.items()))
        out.append(f"      range-residual: " + "  ".join(f"{k} {v:+.1f}%" for k, v in rr.items()))
        rows.append({"model": nm + " (range audit)", "convention": "upper",
                     "m_tau": f"{rr['m_tau']:+.2f}%", "m_b": f"{rr['m_b']:+.2f}%",
                     "M_Z": f"{rr['M_Z']:+.2f}%", "m_t": f"{rr['m_t']:+.2f}%",
                     "RMS": f"{rms(rr):.2f}%"})

    # ---- H43d: exponent-basin robustness (G4) ----
    out.append("\nH43d: exponent-basin robustness (G4 frame on the closure)")
    as_ = np.linspace(0.0, 0.40, 401)
    rms_a = np.array([rms(errors(lambda nf, a=a: f_scan(nf, a), upper=True)) for a in as_])
    basin = base_specificity(
        lambda a: rms(errors(lambda nf, a=a: f_scan(nf, a), upper=True)) / 100.0,
        b_star=1.0 / 6.0, threshold=0.10, lo=0.0, hi=0.40, n=401)
    out.append(f"    basin width (RMS<10%): {basin['width']:.3f}  "
               f"[{basin['basin_lo']:.3f}, {basin['basin_hi']:.3f}]")
    out.append(f"    1/6 inside basin: {basin['b_star_inside']}; "
               f"RMS(1/6)={rms(errors(lambda nf: f_scan(nf, 1.0 / 6.0), upper=True)):.2f}%")
    out.append(f"    min RMS {basin['min_error'] * 100:.2f}% at a = {basin['min_error_b']:.3f}")
    rows.append({"model": f"exponent basin (min a={basin['min_error_b']:.3f})",
                 "convention": f"width {basin['width']:.3f}",
                 "m_tau": f"{basin['min_error'] * 100:.2f}%", "m_b": "-",
                 "M_Z": "-", "m_t": "-", "RMS": f"{basin['min_error'] * 100:.2f}%"})

    # ---- H43e: low-scale (m_tau) re-anchoring ----
    out.append("\nH43e: low-scale (m_tau) re-anchoring, principled upper")
    e_low = {}
    for name, E, ref in REFS:
        if name == "m_tau":
            continue
        pred = alpha_s_low_anchor(E, f_principled, upper=True)
        e_low[name] = 100.0 * (pred / ref - 1.0)
    for name, val in e_low.items():
        out.append(f"      {name:6s} {val:+.2f}%")
    rows.append({"model": "low-scale anchor (m_tau, principled)", "convention": "upper",
                 "m_tau": "0.00%", "m_b": f"{e_low['m_b']:+.2f}%",
                 "M_Z": f"{e_low['M_Z']:+.2f}%", "m_t": f"{e_low['m_t']:+.2f}%",
                 "RMS": f"{rms(e_low):.2f}%"})

    csv_path = os.path.join(OUT_DIR, "flavor_closure_2loop.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["model", "convention", "m_tau",
                                           "m_b", "M_Z", "m_t", "RMS"])
        w.writeheader()
        w.writerows(rows)
    out.append(f"\nWrote {csv_path}")

    make_figures(es, golden_curve, qcd_curve, as_, rms_a, dev)
    out.append(f"Wrote {OUT_DIR}")

    print("\n".join(out))


def make_figures(es, golden_curve, qcd_curve, as_, rms_a, dev):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # panel 1: full-curve overlay
    axes[0].loglog(es, golden_curve, label="golden layer (principled, upper)")
    axes[0].loglog(es, qcd_curve, "--", label="2-loop QCD RGE (MS-bar)")
    for name, E, ref in REFS:
        axes[0].scatter([E], [ref], color="red", zorder=5)
        axes[0].annotate(name, (E, ref), textcoords="offset points",
                         xytext=(6, 6), fontsize=8)
    axes[0].set_xlabel("E (GeV)"); axes[0].set_ylabel("alpha_s")
    axes[0].set_title("Golden layer vs 2-loop QCD")
    axes[0].legend(fontsize=8)

    # panel 2: relative deviation
    axes[1].semilogx(es, dev * 100.0)
    axes[1].axhline(0, color="k", lw=0.5)
    axes[1].set_xlabel("E (GeV)"); axes[1].set_ylabel("|golden/QCD - 1| (%)")
    axes[1].set_title("Shape mismatch vs E")
    for t, _ in THRESH:
        axes[1].axvline(t, color="gray", lw=0.6, ls=":")

    # panel 3: exponent basin
    axes[2].plot(as_, rms_a * 100.0)
    axes[2].axvline(1.0 / 6.0, color="gray", ls=":", label="1/6")
    axes[2].axvline(0.150, color="gray", ls="--", label="Phase 42 best")
    axes[2].set_xlabel("exponent a"); axes[2].set_ylabel("RMS (%)")
    axes[2].set_title("Exponent basin (RMS)")
    axes[2].legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "flavor_closure_2loop.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
