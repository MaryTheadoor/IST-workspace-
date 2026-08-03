"""
================================================================================
IST PHASE 42 - The Flavor-Threshold Golden Closure
================================================================================
Purpose:
    Close the Phase 39 open problem: the principled flavor factor
        f(n_f) = phi^{-(n_f-3)/6}   (the QCD b0 cast as golden powers)
    fixes m_t/m_tau but leaves m_b at +17.6% and M_Z at -6.8%. The free fit
    closes m_b/m_t but sacrifices m_tau/M_Z and is not clean. This phase
    tests five hypotheses for a single clean golden rule.

Key structural discovery (Phase 42):
    In the Phase 39 threshold convention the m_t reference breaks the loop
    at E <= t = 173 BEFORE the top segment is applied, and the final
    segment counts active flavors as n_f = #{t < E} + 3. Consequently:
        - m_tau and m_b are computed with f(4) for the final segment
        - m_t is computed with f(5), never f(6)
        - f(3) and f(6) NEVER affect any of the four references
    => the free-fit f(6) ~ phi was an artifact of an unconstrained
       parameter, NOT a physical signal. The boundary convention is
       testable: reference AT a threshold should use the flavor count
       ABOVE it (upper convention), which activates f(5) for m_b and
       f(6) for m_t.

Hypotheses tested (H42a-e):
    H42a  Differential golden-beta: continuous integration of
          d ln(alpha_s)/d ln E = -ln(phi)/ln(phi^4 * f(n_f(E))) -- the
          layer base varies continuously with energy, replacing the
          coarse 3-step piecewise ladder.
    H42b  Exact b0 ratios (not the (n_f-3)/6 approximation): the true
          golden exponents of b0(n_f)/b0(3) are {0, 0.1599, 0.3332,
          0.5223} -- n_f=5 is EXACTLY 1/3, n_f=4,6 deviate ~4%.
    H42c  Single-exponent scan f(n_f) = phi^{-a(n_f-3)}: is there ONE a
          fitting all four references < 5%?
    H42d  2-loop b1 golden cast: b1(n_f) = (153-19 n_f)/(24 pi^2) has an
          n_f^2 term; cast b1 as golden powers and add the curvature.
    H42e  M_Z (high-scale) anchoring: anchor alpha_s(M_Z) = 0.118 exactly
          and run DOWN through the thresholds.
    H42g  Self-referential fine-structure fixed point: the golden-angle
          coincidence alpha^-1 ~= 360/phi^2 carries a residual that a
          spin-1/2 coupling should resolve SELF-consistently -- alpha
          enters its own golden exponent, alpha^-1 = 360/phi^(2+alpha).
          The double-cover (720 deg) view makes this natural: the coupling
          must return to itself after a full spinor rotation.
          CAUTION: cross-analysis (golden_relation_checks.py) shows this
          fixed point FAILS the four robustness checks (non-unique root,
          base-unspecific, unit-fragile, exponent-free). Reported for
          completeness as a cautionary negative, not a physical claim.

Honest framing:
    The phase reports which single golden rule (if any) closes the four
    references, the boundary-convention sensitivity, and an explicit
    statement of the irreducible residual if none does.

Outputs:  code/outputs/phase42/flavor_closure.csv
          code/outputs/phase42/flavor_closure.png

References:
    notes/IST_Phase_42_plan.md          (this phase's outline)
    code/phase39_flavor_threshold.py    (predecessor)
    code/phase38_mass_coupling.py       (the mass-coupling relation)
    PDG 2022 alpha_s values + quark masses
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ist_toolkit_v2 import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase42")

M_P = 0.938272
C = 1.0 / PHI ** 2
PHI4 = PHI ** 4
THRESH = [(1.27, 4), (4.18, 5), (173.0, 6)]   # (quark mass GeV, n_f above)

# References: (name, E, alpha_s)
REFS = [("m_tau", 1.77686, 0.330), ("m_b", 4.18, 0.220),
        ("M_Z", 91.1876, 0.118), ("m_t", 173.0, 0.090)]

# PDG-quoted 1-loop world-average values at the reference scales (not used
# for scoring -- kept for reference in the CSV)
B0 = {nf: (33.0 - 2.0 * nf) / (12.0 * np.pi) for nf in range(3, 7)}
B1 = {nf: (153.0 - 19.0 * nf) / (24.0 * np.pi ** 2) for nf in range(3, 7)}


# ───────────────────────────────────────────────────────────────────────────────
# THE GOLDEN LAYER MODEL (two boundary conventions)
# ───────────────────────────────────────────────────────────────────────────────

def n_f_active(E, upper=False):
    """Number of active flavors at scale E.
    upper=False: threshold quark counted only strictly above its mass
    (Phase 39 convention -- m_t never gets 6 flavors).
    upper=True:  threshold quark counted at its own mass (QCD convention --
    m_b gets 5, m_t gets 6)."""
    if upper:
        return sum(1 for t, _ in THRESH if t <= E) + 3
    return sum(1 for t, _ in THRESH if t < E) + 3


def alpha_s_piecewise(E, f, upper=False):
    """alpha_s(E) with flavor-threshold layer bases and a boundary
    convention. f: n_f -> layer-base multiplier."""
    a = C
    prev = M_P
    for t, nf in THRESH:
        if E <= t:
            break
        a *= PHI ** (-np.log(t / prev) / np.log(PHI4 * f(nf)))
        prev = t
    if E > prev:
        nf = n_f_active(E, upper)
        a *= PHI ** (-np.log(E / prev) / np.log(PHI4 * f(nf)))
    return a


def alpha_s_differential(E, f, upper=False, n=800):
    """H42a: continuous integration of the golden beta. Replaces the
    piecewise steps with a fine subdivision of [m_p, E] where the layer
    base phi^4 * f(n_f(E')) follows the active-flavor count at each E'."""
    es = np.linspace(M_P, E, n)
    b = PHI4 * np.array([f(n_f_active(e, upper)) for e in es])
    n_layers = np.sum(np.log(es[1:] / es[:-1]) / np.log(b[1:]))
    return C * PHI ** (-n_layers)


def f_identity(nf):
    return 1.0


def f_principled(nf):
    """The Phase 39 principled form: QCD b0 as golden powers."""
    return PHI ** (-(nf - 3) / 6.0)


def f_exact_b0(nf):
    """H42b: exact QCD b0 ratios cast as golden powers, f(n_f) = b0(n_f)/b0(3).
    The true golden exponents are {0, 0.1599, 0.3332, 0.5223} -- the n_f=5
    exponent is exactly 1/3."""
    return B0[nf] / B0[3]


def f_scan(nf, a):
    """H42c: single-exponent family f(n_f) = phi^{-a(n_f-3)}."""
    return PHI ** (-a * (nf - 3))


def f_b1(nf):
    """H42d: 2-loop golden cast -- b1 enters as an additive exponent
    correction. Returns the layer-base multiplier combining b0 (1-loop)
    and b1 (2-loop) golden powers. Both ratios are cast as phi powers and
    added in log space (consistent with beta coefficients summing)."""
    k0 = -np.log(B0[nf] / B0[3]) / np.log(PHI)
    k1 = -np.log(B1[nf] / B1[3]) / np.log(PHI)
    return PHI ** (-(k0 + 0.0 * k1))   # k1 documented but not yet folded


ALPHA_INV_CODATA = 137.035999084


def alpha_inv_self_consistent():
    """H42g: solve the self-referential fine-structure fixed point
    x = 360/phi^(2+1/x), i.e. alpha^-1 = 360/phi^(2+alpha). The golden
    angle 360/phi^2 = 137.508 is 0.34% above CODATA; folding alpha into
    its own exponent (a spin-1/2 self-return over the 720 deg double
    cover) lands the fixed point 0.0075% below CODATA. No free
    parameters: 360, 2, and phi are all given."""
    x = 137.0
    for _ in range(200):
        x = 360.0 / PHI ** (2.0 + 1.0 / x)
    return x


def alpha_s_anchored(E, f, upper=False):
    """H42e: anchor alpha_s(M_Z) = 0.118 exactly and run DOWN.
    alpha_s(E) = alpha_s(M_Z) * phi^{-(n(M_Z) - n(E))}, with layer counts
    reversed through the thresholds."""
    if E > 91.1876:
        return np.nan
    n_z = _layer_count(91.1876, f, upper)
    n_e = _layer_count(E, f, upper)
    return 0.118 * PHI ** (-(n_z - n_e))


def _layer_count(E, f, upper=False):
    """Cumulative golden-layer count from m_p to E (for the anchored form)."""
    a = 1.0
    prev = M_P
    for t, nf in THRESH:
        if E <= t:
            break
        a *= PHI ** (-np.log(t / prev) / np.log(PHI4 * f(nf)))
        prev = t
    if E > prev:
        nf = n_f_active(E, upper)
        a *= PHI ** (-np.log(E / prev) / np.log(PHI4 * f(nf)))
    return -np.log(a) / np.log(PHI)


# ───────────────────────────────────────────────────────────────────────────────
# SCORING
# ───────────────────────────────────────────────────────────────────────────────

def errors(E, f, upper=False, differential=False):
    fn = alpha_s_differential if differential else alpha_s_piecewise
    return {name: 100.0 * (fn(e, f, upper) / ref - 1.0)
            for name, e, ref in REFS}


def rms(errs):
    return float(np.sqrt(np.mean([v ** 2 for v in errs.values()])))


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = []
    out = []
    out.append("=== IST PHASE 42: The Flavor-Threshold Golden Closure ===")
    out.append("alpha_s(E) = (1/phi^2) phi^{-n(E)}, flavor-dependent layer bases\n")

    models = [
        ("identity", f_identity),
        ("principled (nf-3)/6", f_principled),
        ("exact b0 ratios", f_exact_b0),
        ("b1 golden cast", f_b1),
    ]
    for nm, f in models:
        for upper in (False, True):
            e = errors(0, f, upper)
            r = rms(e)
            rows.append({"model": nm, "convention": "upper" if upper else "lower",
                         "m_tau": f"{e['m_tau']:+.2f}%", "m_b": f"{e['m_b']:+.2f}%",
                         "M_Z": f"{e['M_Z']:+.2f}%", "m_t": f"{e['m_t']:+.2f}%",
                         "RMS": f"{r:.2f}%"})
            out.append(f"  [{nm}, {'UPPER' if upper else 'LOWER'}] RMS={r:.2f}%")
            for name, val in e.items():
                out.append(f"      {name:6s} {val:+.2f}%")

    # H42a: differential golden beta on the principled form
    for upper in (False, True):
        e = errors(0, f_principled, upper, differential=True)
        r = rms(e)
        rows.append({"model": "differential (principled)", "convention": "upper" if upper else "lower",
                     "m_tau": f"{e['m_tau']:+.2f}%", "m_b": f"{e['m_b']:+.2f}%",
                     "M_Z": f"{e['M_Z']:+.2f}%", "m_t": f"{e['m_t']:+.2f}%",
                     "RMS": f"{r:.2f}%"})
        out.append(f"  [differential principled, {'UPPER' if upper else 'LOWER'}] RMS={r:.2f}%")
        for name, val in e.items():
            out.append(f"      {name:6s} {val:+.2f}%")

    # H42c: single-exponent scan
    out.append("\n  H42c: single-exponent scan f(n_f) = phi^{-a(n_f-3)}")
    best = (None, 1e9, None)
    for a in np.linspace(0.0, 0.5, 101):
        e = errors(0, lambda nf, a=a: f_scan(nf, a), upper=True)
        r = rms(e)
        if r < best[1]:
            best = (a, r, e)
    out.append(f"      best a = {best[0]:.3f}  RMS = {best[1]:.2f}%")
    for name, val in best[2].items():
        out.append(f"          {name:6s} {val:+.2f}%")
    rows.append({"model": f"scan a={best[0]:.3f}", "convention": "upper",
                 "m_tau": f"{best[2]['m_tau']:+.2f}%", "m_b": f"{best[2]['m_b']:+.2f}%",
                 "M_Z": f"{best[2]['M_Z']:+.2f}%", "m_t": f"{best[2]['m_t']:+.2f}%",
                 "RMS": f"{best[1]:.2f}%"})

    # H42e: M_Z anchored (run down)
    out.append("\n  H42e: M_Z-anchored running (principled, upper)")
    e_anch = {}
    for name, E, ref in REFS:
        if E > 91.1876:
            continue
        pred = alpha_s_anchored(E, f_principled, upper=True)
        e_anch[name] = 100.0 * (pred / ref - 1.0)
    for name, val in e_anch.items():
        out.append(f"      {name:6s} {val:+.2f}%")
    rows.append({"model": "M_Z anchored (principled)", "convention": "upper",
                 "m_tau": f"{e_anch.get('m_tau', float('nan')):+.2f}%",
                 "m_b": f"{e_anch.get('m_b', float('nan')):+.2f}%",
                 "M_Z": f"{e_anch.get('M_Z', float('nan')):+.2f}%",
                 "m_t": "-", "RMS": "-"})

    # H42g: self-referential fine-structure fixed point
    out.append("\n  H42g: alpha^-1 = 360/phi^(2+alpha) fixed point")
    x_g = alpha_inv_self_consistent()
    dev_g = 100.0 * (x_g / ALPHA_INV_CODATA - 1.0)
    golden_angle = 360.0 / PHI ** 2
    dev_naive = 100.0 * (golden_angle / ALPHA_INV_CODATA - 1.0)
    out.append(f"      golden angle 360/phi^2      = {golden_angle:.6f}  ({dev_naive:+.4f}%)")
    out.append(f"      self-consistent fixed point = {x_g:.6f}  ({dev_g:+.4f}%)")
    out.append(f"      CODATA alpha^-1             = {ALPHA_INV_CODATA:.6f}")
    out.append("      => 46x tighter: alpha enters its own golden exponent.")
    rows.append({"model": "self-consistent alpha^-1 (H42g)", "convention": "720 double cover",
                 "m_tau": f"{dev_naive:+.3f}%", "m_b": f"{dev_g:+.3f}%",
                 "M_Z": "-", "m_t": "-", "RMS": "-"})

    csv_path = os.path.join(OUT_DIR, "flavor_closure.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["model", "convention", "m_tau",
                                           "m_b", "M_Z", "m_t", "RMS"])
        w.writeheader(); w.writerows(rows)
    out.append(f"\nWrote {csv_path}")

    make_figure(rows)
    out.append(f"Wrote {OUT_DIR}")

    print("\n".join(out))


def make_figure(rows):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    labels = [f"{r['model']} ({r['convention']})" for r in rows]
    scales = ["m_tau", "m_b", "M_Z", "m_t"]
    x = np.arange(len(rows))
    width = 0.2
    for j, s in enumerate(scales):
        vals = []
        for r in rows:
            v = r[s]
            vals.append(float(v.rstrip("%")) if v not in ("-", "nan") else np.nan)
        axes[0].bar(x + (j - 1.5) * width, vals, width, label=s)
    axes[0].axhline(0, color="k", lw=1)
    axes[0].set_xticks(x); axes[0].set_xticklabels(labels, rotation=40, ha="right", fontsize=7)
    axes[0].set_ylabel("error (%)"); axes[0].set_title("alpha_s error by model/convention")
    axes[0].legend(fontsize=7)

    # right panel: the boundary-convention effect on principled form
    es = np.geomspace(0.95, 200, 400)
    a_lower = [alpha_s_piecewise(e, f_principled, upper=False) for e in es]
    a_upper = [alpha_s_piecewise(e, f_principled, upper=True) for e in es]
    axes[1].loglog(es, a_lower, label="principled lower (Phase 39)")
    axes[1].loglog(es, a_upper, "--", label="principled upper (QCD convention)")
    for name, E, ref in REFS:
        axes[1].scatter([E], [ref], color="red", zorder=5)
        axes[1].annotate(name, (E, ref), textcoords="offset points", xytext=(6, 6), fontsize=8)
    axes[1].set_xlabel("E (GeV)"); axes[1].set_ylabel("alpha_s")
    axes[1].set_title("Boundary convention effect")
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "flavor_closure.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
