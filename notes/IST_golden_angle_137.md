# IST — The Golden Angle and the Self-Consistent 137

**Status:** EXPLORATION NOTE (adjunct to Phase 42, H42g)
**Related:** `code/phase42_flavor_closure.py` (H42g), `notes/IST_Phase_42_plan.md`
**Ask:** Does the 137 equation (alpha^-1 ~= 360/phi^2) survive the spin-1/2
double cover (720 deg) that IST's structural constants (theta = 1/2, Koide
phase pi/2) already use?

---

## 1. The coincidence

    alpha^-1       = 137.035999   (CODATA 2022)
    golden angle   = 360/phi^2    = 137.507764    (+0.344%)

0.34% agreement is the well-known "137 mystery" near-coincidence. It is not
a derivation: the residual 0.47 deg does not cast cleanly as a golden power
nor as the Koide 120 deg offset.

## 2. The 720 deg (double-cover) test

A spin-1/2 object needs a FULL 720 deg to return to identity. Doubling the
circle naively:

    2*alpha^-1  = 274.072 deg
    720/phi^2   = 275.016 deg        residual -0.94 deg

The residual merely doubles (same relative error). The naive 2x rotation is
NOT the resolution. (Note the incidental near-hit 720/phi^2 - alpha^-1 ~=
137.98 deg ~= golden angle -- it restates the same coincidence, not a new
structure.)

## 3. The self-consistent fixed point (H42g)

The 0.34% residual should be resolved by the coupling resolving ITSELF. If
alpha enters its own golden exponent:

    alpha^-1 = 360 / phi^(2+alpha)      x = 360/phi^(2+1/x)

Solving the fixed point (no free parameters; 360, 2, phi all given):

    x* = 137.025706        CODATA 137.035999        error -0.0075%

    plain golden angle                 +0.344%
    self-consistent fixed point        -0.0075%      (~46x tighter)

Physical reading: over the 720 deg double cover, the coupling is a
self-returning map -- alpha is the FIXED POINT of "golden angle with alpha
in its own exponent", not a free value. This is the IST-consistent form:
structural self-reference (alpha solves alpha) rather than a tuned constant.

## 4. Honest caveats

- 0.0075% on a coincidence-rich constant is suggestive, not proof. The
  fixed point is one clean relation among many that could fit; its claim
  rests on being PARAMETER-FREE and structurally motivated (double-cover
  self-return), which the plain golden angle also is but at 0.34%.
- The result is robust to perturbation (the map converges; small changes in
  the exponent shift x* smoothly), but it is a single point relation, not a
  spectrum.

## 5. Status / next

- Integrated as H42g in `phase42_flavor_closure.py`; reported in
  `code/outputs/phase42/flavor_closure.csv`.
- Not (yet) a phase of its own. If it survives independent cross-checks
  (e.g. alpha_s(0) reinterpretation, coupling to the m_b/m_c golden
  relation), promote to its own note/phase.
