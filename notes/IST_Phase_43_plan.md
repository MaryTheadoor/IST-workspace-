# IST Phase 43 — The m_b Anomaly and the 2-Loop Golden Closure

**Status:** COMPLETE (honest negative; conflict localized to the m_b→M_Z slope)
**Predecessor:** Phase 42 (`code/phase42_flavor_closure.py`) — principled upper
RMS 8.78%, conflict isolated to m_b (+15.9%) and M_Z (-6.75%)
**Postcondition:** A principled golden rule closing all four references, or a
systematic, robustness-checked statement of why the residual is irreducible.
(Result: the latter — no single golden rule closes all four; the m_b→M_Z
segment runs +31.5% too steep under the golden layer model.)

---

## 1. The Phase 42 residual, restated

Upper-convention results (four references):

| model | m_tau | m_b | M_Z | m_t | RMS |
|---|---|---|---|---|---|
| principled phi^-(nf-3)/6 | -2.0% | +15.9% | -6.75% | -2.2% | 8.78% |
| best single exponent a=0.150 | -1.9% | +16.3% | -5.7% | -0.4% | 8.70% |

The closure conflict is a **running-slope mismatch**: m_b must come DOWN and
M_Z must go UP, i.e. the model's running between m_b and M_Z is too steep.
m_tau and m_t are essentially closed.

## 2. Three gaps in the current testing (found in review)

**(A) H42d was never tested.** `phase42_flavor_closure.py` computes
`f_b1(nf) = PHI^(-(k0 + 0.0*k1))` -- the 2-loop b1 term is dead code
(`0.0 * k1 == 0`). The CSV row "b1 golden cast" is bit-identical to "exact b0
ratios". The n_f^2 curvature hypothesis was documented but never evaluated.

**(B) No full-curve comparison.** Scoring uses only 4 reference points. We have
never compared the golden-layer alpha_s(E) against the exact 2-loop QCD
running curve between thresholds. That comparison distinguishes a *local m_b
issue* from a *systematic running-shape mismatch*.

**(C) No reference-systematics audit.** m_b = 0.220, m_t = 0.090,
m_tau = 0.330 are single-convention values (scheme/scale-dependent, PDG world
averages carry quoted uncertainties). The residual is scored against one
number each, not the credible range.

## 3. Hypotheses to test (H43)

1. **H43a -- Fold in the real b1 (2-loop) golden cast.** Implement the 2-loop
   golden-layer base properly: cast the combined (b0, b1) structure as golden
   powers and re-run all four references. Physical intuition says a positive
   b1 *steepens* running (wrong direction for both residuals) -- test it, and
   report the sign/direction honestly rather than assuming.
2. **H43b -- Full-curve 2-loop QCD comparison.** Integrate the standard 2-loop
   QCD RGE (b0, b1, MS-bar) and overlay the golden-layer curve across
   [m_p, M_Z]. Measure the shape mismatch (max deviation, where it peaks).
   This tells us whether the residual is a local threshold issue or a global
   golden-vs-QCD running discrepancy.
3. **H43c -- Reference-systematics audit.** Establish the credible range for
   each reference from PDG quoted values and scheme conventions (e.g.
   m_tau alpha_s ~ 0.331 +- 0.013; m_b world average; m_t scheme-dependence).
   Re-score the golden model against the *ranges*, and report which residuals
   shrink under legitimate reference choice.
4. **H43d -- Robustness of the exponent basin (G4 applied to the closure).**
   Scan the exponent a around the principled 1/6 and the best-fit 0.150.
   Measure the RMS basin width: is the golden exponent sharp (claim) or flat
   (weak claim)? Apply the golden_relation_checks.py frame to the flavor
   closure itself, the way H42g was checked.
5. **H43e -- Low-scale (m_tau) re-anchoring.** Phase 38 nailed m_tau (1.3%)
   with identity running and M_Z at 3.1%. Re-anchor the golden-layer model so
   the m_tau->M_Z layer count matches 2-loop QCD exactly, and treat m_b/m_t
   as consistency checks. Contrasts with the failed H42e high-scale (M_Z)
   anchor (m_tau -87.8%) and may reveal the natural anchor scale.

## 4. Success criteria

- **Closure:** one golden rule (single derived exponent, or a principled b1
  combination) fits all four references to < 5% each, with the exponent basin
  sharp AND phi/1/6 at its minimum (passes H43d).
- **Honest negative:** if m_b remains irreducible, quantify the minimal RMS,
  identify why (b0-vs-b1 curvature, step-boundary placement, or reference
  systematics), and state it as the golden-vs-QCD divergence point -- the
  Phase 37-style outcome.
- **Methodology either way:** the closure claim itself gets the
  golden_relation_checks treatment (basin sharpness, parameter count).

## 5. Deliverables

- `code/phase43_flavor_closure_2loop.py` -- b1 cast, full-curve QCD RGE,
  systematics ranges, exponent-basin scan, low-scale anchor; CSV + figure.
- `tests/test_phase43_flavor_closure.py` -- tests encoding H43a-e.
- `code/outputs/phase43/` -- `flavor_closure_2loop.csv`, figures.
- Phase map + synthesis update (README.md, cross_phase_synthesis.md,
  synthesis_paper.md 8.1s, retrospective_cross_analysis.md).

## 6. Reference data (same as Phases 38-39, plus PDG uncertainties)

    thresholds (GeV): m_c = 1.27, m_b = 4.18, m_t = 173.0
    references:       m_tau 1.77686 -> 0.330 (+-0.013)
                      m_b   4.18    -> 0.220 (world average)
                      M_Z   91.1876 -> 0.118 (PDG)
                      m_t   173.0   -> 0.090 (scheme-dependent)
    constants: m_p = 0.938272, C = 1/phi^2, layer base phi^4

## 7. Sequencing

Phase 43 is complete. The standing open items remain: BAO sound-horizon test of
Phase 36's crystallization; baryon octet Lambda-Sigma mixing; stable-knot -> SM
multiplicity mapping. (Phase 43 added one: whether a *reference-level* fix — the
scheme-dependence of the m_t = 0.090 reference, vs 2-loop QCD running 0.108 —
re-scopes the closure target.)
