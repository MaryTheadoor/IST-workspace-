# IST Phase 42 — The Flavor-Threshold Golden Closure

**Status:** PLAN (outline for implementation)
**Predecessor:** Phase 39 (`code/phase39_flavor_threshold.py`) — threshold mechanism confirmed, clean closure open
**Postcondition:** A single principled golden rule for the active-flavor running, or an honest statement of why none exists.

---

## 1. The Problem (Phase 39 baseline)

The mass-coupling relation (Phase 38, Insight B),

    alpha_s(E) = (1/phi^2) phi^{-n(E)},   n(E) = ln(E/m_p)/ln(phi^4)

reproduces alpha_s at M_Z (3.1%) and m_tau (1.3%) but over-predicts at
m_b (+19.5%) and m_t (+15.2%). The cause: the model runs too fast above
each quark-mass threshold, whereas QCD's running slows as more flavors
become active (b0 = (33-2 n_f)/(12 pi) decreases).

Phase 39's piecewise fix multiplies the golden layer base by a per-flavor
factor f(n_f) between thresholds:

    a *= PHI^(-ln(seg)/ln(PHI^4 * f(n_f)))

Results (four references: m_tau, m_b, M_Z, m_t):

| model | m_tau | m_b | M_Z | m_t |
|---|---|---|---|---|
| original (no thresholds) | -1.3% | +19.5% | +3.1% | +15.2% |
| free 4-param fit f={0.64,0.58,0.91,1.64} | -7.4% | +3.0% | -5.7% | +4.5% |
| principled phi^{-(nf-3)/6} | -2.0% | +17.6% | -6.8% | +2.7% |

The principled form (the QCD b0 cast as golden powers) fixes m_t/m_tau but
leaves m_b at +17.6% and pushes M_Z to -6.8%. The free fit fixes m_b/m_t
but sacrifices m_tau/M_Z, and its f-values are not clean.

## 2. Why the Principled Form Fails — Two Structural Issues

**(A) Coarse piecewise steps vs continuous running.** The current model
changes the layer base in 3 discrete steps (at m_c, m_b, m_t). QCD's
running is continuous in E. A differential (golden-beta) formulation —
d ln(alpha_s)/d ln E = -ln(phi)/ln(phi^4 * f(n_f(E))) — replaces the
steps with a continuous integration and may remove the m_b/M_Z residuals
that come from where the step boundaries sit relative to the references.

**(B) The b0 golden cast is approximate, not exact.** phi^{-(nf-3)/6}
gives golden exponents {1/6, 1/3, 1/2} for n_f = {4,5,6}. The exact QCD
ratios b0(n_f)/b0(3) = {(33-8)/(33-6), 23/27, 21/27} = {0.926, 0.852,
0.778} have true golden exponents {-ln(b0/b0_3)/ln(phi)} =
{0.160, 0.333, 0.520}. n_f=5 is EXACT; n_f=4,6 are ~4% off. Test whether
the exact ratios (not the (nf-3)/6 approximation) close the residual.

## 3. Hypotheses to Test (H42)

1. **H42a — Differential golden-beta closure.** Integrate
   d ln(alpha_s)/d ln E = -ln(phi)/ln(phi^4 * f(n_f(E))) continuously
   from m_p to M_Z with threshold-dependent f(n_f). Compare the FULL
   predicted alpha_s(E) curve to the QCD 1-loop reference curve (not
   just 4 points). If the continuous form with f(nf)=phi^{-(nf-3)/6}
   closes m_b/M_Z, the coarse stepping was the residual source.

2. **H42b — Exact b0 ratios.** Use f(n_f) = b0(n_f)/b0(3) exactly
   (= {1, 25/27, 23/27, 21/27}) in the differential form. Test whether
   the exact QCD golden-cast (whose exponents are {0, 0.160, 0.333,
   0.520}, n_f=5 exact to 1/3) removes the residuals.

3. **H42c — Single-exponent scan.** Parametrize f(n_f) = phi^{-a(nf-3)}
   and scan a in [0, 0.5]. Is there ONE a that fits all four references
   within their uncertainties? Report the best a and its deviation from
   the principled a = 1/6.

4. **H42d — 2-loop (b1) golden cast.** QCD's b1 = (153-19 n_f)/(24 pi^2)
   has an n_f^2 term. Cast b1 as golden powers too and check whether the
   n_f^2 curvature closes the m_b residual that a pure b0 form cannot.

5. **H42e — Anchor consistency.** Anchor the golden model EXACTLY at
   M_Z (alpha_s = 0.118) and run DOWN through the thresholds. Check
   m_tau/m_b/m_t against their references. (Phase 39 anchored at m_p; a
   high-scale anchor is the QCD convention and may be more natural.)

6. **H42g — Self-referential fine-structure fixed point.** The golden
   angle 360/phi^2 = 137.5078 sits 0.34% above CODATA alpha^-1 =
   137.035999. The residual should be resolved SELF-consistently: a
   spin-1/2 coupling must return to itself over the 720 deg double
   cover, so alpha enters its own golden exponent,
   alpha^-1 = 360/phi^(2+alpha). Solving the fixed point x =
   360/phi^(2+1/x) gives x = 137.0257 -- 0.0075% below CODATA, ~46x
   tighter than the plain golden angle, with no free parameters (360, 2,
   phi are all given).

## 4. Success Criteria

- **Closure:** one golden rule (H42a/b with a single parameter) fits
  all four references to < 5% each, with the best-fit a within ~10% of
  the principled a = 1/6, OR the exact b0 ratios close m_b to < 5%.
- **Honest negative:** if no single rule closes all four, quantify the
  minimum achievable residual and identify WHICH reference is
  irreducible (likely m_b) and why (b0 vs b1 curvature, step boundary
  placement, or reference-systematics).
- **Refinement either way:** if closed, the mass-coupling relation gains
  a principled, parameter-free flavor dependence (golden cast of QCD
  b0). If not, the negative is as informative as Phase 37's: it locates
  where golden-layer running and QCD running genuinely diverge.

## 5. Deliverables

- `code/phase42_flavor_closure.py` — differential golden beta,
  full-curve comparison, exact-b0 cast, single-exponent scan, 2-loop
  b1 test, M_Z anchor test; CSV + figure outputs.
- `tests/test_phase42_flavor_closure.py` — tests encoding H42a-e, H42g.
- `code/outputs/phase42/` — `flavor_closure.csv`, `flavor_closure.png`.
- Phase map row added to `README.md`, `main/cross_phase_synthesis.md`,
  `main/synthesis_paper.md` (8.1r), and `notes/retrospective_cross_analysis.md`.

## 6. Reference Data (PDG 2022, same as Phases 38-39)

    thresholds (quark masses, GeV): m_c = 1.27, m_b = 4.18, m_t = 173.0
    references (scale, alpha_s):    m_tau 1.77686 -> 0.330
                                    m_b   4.18    -> 0.220
                                    M_Z   91.1876 -> 0.118
                                    m_t   173.0   -> 0.090
    constants: m_p = 0.938272, C = 1/phi^2, layer base phi^4

## 7. Sequencing

Phase 42 is the immediate next phase. After it: the Phase 36 follow-up
(BAO sound-horizon test of dimensional crystallization -- COMPLETE as Phase 44:
an honest negative that confirms D ~ 3 at observable z; the ruler adds no
discriminating power at z <= 1.5), then the
remaining open items (baryon octet Lambda-Sigma mixing -- COMPLETE as Phase 45:
a golden partition of the Lambda->Xi interval by Sigma; emergent-twist
derivation) as budget allows.
