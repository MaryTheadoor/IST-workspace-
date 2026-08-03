"""
===============================================================================
IST GOLDEN-RELATION ROBUSTNESS CHECKS
===============================================================================
Methodology learned from the Phase 42 H42g double-cover cross-analysis.

A golden relation is only a claim if it survives four robustness checks.
These encode the honest lesson of H42g (alpha^-1 = 360/phi^(2+alpha)):
its fixed point landed 0.0075% from CODATA -- 46x tighter than the plain
golden angle -- but cross-analysis showed the "tightness" was partly an
artifact of four unexamined degrees of freedom:

  G1. FIXED-POINT UNIQUENESS: does x = g(x) have ONE physical root?
      (H42g has TWO: 0.0625 and 137.03 -- the equation alone does not
      select the physical root; the iteration initial guess did.)
  G2. BASE SPECIFICITY: does the base (phi) sit in a SHARP basin, or do
      nearby bases fit just as well? (H42g: any base in a 0.09% band
      gives <0.1% error -- phi is NOT uniquely selected.)
  G3. UNIT INVARIANCE: does the relation survive a degrees<->radians
      rescale? (H42g: deg -> fixed point 137; rad -> 1.85. The relation
      is unit-fragile, i.e. it depends on the arbitrary choice of 360.)
  G4. EXPONENT FREEDOM: if a parameter k appears in the exponent, how
      many k values give a comparable fit with some base? (H42g: 14
      exponents in [1.5,2.5] reach <0.01% -- two knobs (b,k) can be
      tuned, which devalues a "no free parameters" claim.)

Use these checks on ANY proposed golden relation BEFORE reporting its
agreement as physical. A claim that passes is one where the fixed point
is unique, the base basin is narrow AND phi sits at its minimum, the
relation is (or is explicitly convention-bound about) unit scaling, and
the number of tunable knobs is honestly counted.

Run: cd code && python -m pytest ../tests/test_golden_relation_checks.py -v
===============================================================================
"""

import numpy as np


def fixed_point_roots(g, lo, hi, n=100000):
    """All roots of x = g(x) in [lo, hi] (sign changes of x - g(x)).
    Returns the list of root locations. For a physical claim you want
    EXACTLY ONE root in the physically allowed region."""
    xs = np.linspace(lo, hi, n)
    diffs = xs - np.array([g(x) for x in xs])
    roots = []
    for i in range(n - 1):
        if diffs[i] == 0.0:
            roots.append(float(xs[i]))
        elif diffs[i] * diffs[i + 1] < 0.0:
            a, b = xs[i], xs[i + 1]
            for _ in range(60):
                m = 0.5 * (a + b)
                if (m - g(m)) * (a - g(a)) < 0.0:
                    b = m
                else:
                    a = m
            roots.append(float(0.5 * (a + b)))
    return roots


def base_specificity(error_fn, b_star, threshold, lo=1.2, hi=2.0, n=4001):
    """Width of the base basin where |error(b)| < threshold, and whether
    b_star sits at (or below) the basin minimum.

    error_fn(b) -> relative error as a fraction (e.g. 0.001 = 0.1%).
    Returns dict: width, basin_lo, basin_hi, b_star_inside,
                  min_error, min_error_b, margin.
    margin = (basin half-width)/width ... larger margin = sharper claim.
    A narrow width with b_star NOT inside = the base is not golden."""
    bs = np.linspace(lo, hi, n)
    errs = np.array([abs(error_fn(b)) for b in bs])
    inside = bs[errs < threshold]
    if inside.size == 0:
        return {"width": np.nan, "basin_lo": np.nan, "basin_hi": np.nan,
                "b_star_inside": False, "min_error": float(errs.min()),
                "min_error_b": float(bs[errs.argmin()]),
                "b_star_error": float(error_fn(b_star))}
    i = errs.argmin()
    return {"width": inside[-1] - inside[0], "basin_lo": inside[0],
            "basin_hi": inside[-1], "b_star_inside": inside[0] < b_star < inside[-1],
            "min_error": float(errs[i]), "min_error_b": float(bs[i]),
            "b_star_error": float(error_fn(b_star))}


def unit_robustness(fixed_point_fn, reference, scale):
    """Degrees<->radians robustness. fixed_point_fn(circle) computes the
    fixed point for a given full-circle measure (360 deg or 2*pi rad).
    Returns (deg_error, rad_error) as fractions."""
    return (abs(fixed_point_fn(scale[0]) / reference - 1.0),
            abs(fixed_point_fn(scale[1]) / reference - 1.0))
