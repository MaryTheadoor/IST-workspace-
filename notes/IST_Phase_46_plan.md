# IST Phase 46 — The Reference-Level Fix: Does Scheme-Dependence Re-Scope the Flavor Closure?

**Status:** COMPLETE (honest negative: the reference-level fix is REFUTED --
the alpha_s flavor closure is reference-irreducible; m_t 0.108 makes RMS worse,
free references still leave m_b/M_Z OUT, and QCD needs the OPPOSITE sign of
layer-base flattening, proving a power-law-vs-log shape mismatch)
**Predecessor:** Phase 43 (`code/phase43_flavor_closure_2loop.py`) — honest negative;
closure conflict localized to the m_b→M_Z running slope (+31.5% too steep under the
golden layer model). Phase 43 added an open question (sequencing note):
> "whether a *reference-level* fix — the scheme-dependence of the m_t = 0.090
> reference, vs 2-loop QCD running 0.108 — re-scopes the closure target."

**Postcondition:** Either a golden rule closes all four references under a legitimate
reference choice, or an honest, robustness-checked statement of why the closure
conflict is reference-irreducible.

---

## 1. The Phase 43 residual, restated

Principled golden model, upper convention (four references):

| model | m_tau | m_b | M_Z | m_t | RMS |
|---|---|---|---|---|---|
| principled phi^-(nf-3)/6 | -2.0% | +15.9% | -6.75% | -2.2% | 8.78% |
| b1 golden cast (k0+k1) | -4.2% | +0.7% | -42.1% | -75.8% | 43.4% |

The conflict is a running-slope mismatch in the m_b→M_Z segment (golden 1.747 vs QCD
1.328 layers, +31.5%). The open question: is this a real shape mismatch, or an
artifact of single-number references whose scheme/scale dependence is untested?

## 2. Preliminary findings (scoping run, `code/_scratch46*.py`)

These drive the phase design and are re-verified in code:

**(P1) The m_t reference fix makes it WORSE.** Substituting m_t = 0.108 (the 2-loop
QCD-running value) for the 0.090 convention raises principled RMS 8.78% → 12.70%,
with m_t going -2.2% → -18.5%. The golden model predicts alpha_s(173 GeV) ~ 0.088,
close to the 0.090 convention but 18% below the QCD-running value. The 0.090
reference was *masking* the m_t deficit, not causing the m_b/M_Z conflict.

**(P2) QCD-consistent reference set scores worse.** Scoring against the exact 2-loop
QCD running values {m_tau 0.3133, m_b 0.2236, M_Z 0.1180, m_t 0.1076} gives principled
RMS 12.10% (m_tau +3.2%, m_b +14.1%, M_Z -6.8%, m_t -18.2%). No reference choice
rescues m_b.

**(P3) Free references within credible ranges still fail.** Minimizing range-residual
over the single exponent a with ALL four references free in their REF_RANGES: best
a=0.110, but m_b (pred 0.258 vs [0.210, 0.240]) and M_Z (pred 0.114 vs [0.117, 0.119])
stay OUT. No single exponent can close m_b and M_Z together even at the friendliest
reference placement.

**(P4) Two-parameter decoupling still fails.** Two free exponents (a for nf<=5, b for
nf=6), refs free in ranges: best (a,b)=(0.110, 0.000) — m_b +7.4% over, M_Z -2.5%
under. The conflict is not an exponent-count artifact.

**(P5) Structural origin.** The layer-base multipliers REQUIRED to match 2-loop QCD
exactly are f(4)~phi^-2.65, f(5)~phi^-1.69, f(6)~phi^+0.82 (m_b→M_Z), f(6)~phi^+2.96
(M_Z→m_t) — a positive-exponent (flattening) high-scale structure, opposite to the
principled phi^-(nf-3)/6 (steepening). The golden layer model is a pure power law in
E; QCD running is ~1/ln E and flattens at high E. The m_b→M_Z slope conflict is the
signature of power-law vs logarithmic running — reference-independent.

## 3. Hypotheses to test (H46)

1. **H46a — The m_t reference-level fix (Phase 43's open question).** Substitute the
   QCD-running m_t = 0.108 for the 0.090 convention; re-score principled and best-exponent.
   Does the closure target re-scope? (Preliminary: NO — RMS worsens.)
2. **H46b — QCD-consistent reference set.** Score every golden model against the exact
   2-loop QCD running values at the four scales, not single-number PDG conventions.
   This is the "natural" reference frame for a running law. (Preliminary: worse.)
3. **H46c — Best-possible reference placement.** Minimize range-residual over the
   exponent a with all four references free in their credible ranges (REF_RANGES).
   Even at the friendliest placement, can a single golden exponent close all four?
   (Preliminary: NO — m_b, M_Z irreducible.)
4. **H46d — Two-parameter exponent decoupling.** Allow different golden exponents
   below/above the m_b threshold. Even with two free knobs, can the closure close?
   (Preliminary: NO.)
5. **H46e — Structural diagnosis.** Compute the required layer-base f(nf) profile to
   match 2-loop QCD exactly per segment, and the power-law-vs-log divergence as a
   function of E. State WHY the golden flavor running cannot reproduce QCD curvature,
   reference-independently.

## 4. Success criteria

- **Closure:** if some legitimate reference choice + single (or principled) golden
  rule closes all four < 5% with a sharp exponent basin (passing the
  golden_relation_checks frame), Phase 46 is a success and closes the Phase 43 open
  question positively.
- **Honest negative (expected):** if the reference-level fix is refuted, quantify the
  minimal range-residual at the best reference placement, show it is irreducible under
  single AND two-parameter rules, and give the structural reason (power-law golden
  running vs 1/ln E QCD running). This CLOSES the Phase 43 sequencing question with a
  definite answer: the closure is reference-irreducible.

## 5. Deliverables

- `code/phase46_reference_rescope.py` — H46a-e: m_t substitution, QCD-consistent
  scoring, free-reference minimization, two-exponent scan, required-f structural
  profile; CSV + figure.
- `tests/test_phase46_reference_rescope.py` — tests encoding H46a-e.
- `code/outputs/phase46/` — `reference_rescope.csv`, figures.
- Phase map + synthesis update (README.md, cross_phase_synthesis.md,
  synthesis_paper.md 8.1v, retrospective_cross_analysis.md, plan-file sequencing).

## 6. Reference data (same as Phases 42/43)

    thresholds (GeV): m_c = 1.27, m_b = 4.18, m_t = 173.0
    references:       m_tau 1.77686 -> 0.330 (range +-0.013)
                      m_b   4.18    -> 0.220 (world average, range [0.210, 0.240])
                      M_Z   91.1876 -> 0.118 (PDG, range +-0.001)
                      m_t   173.0   -> 0.090 (scheme-dependent, range [0.090, 0.108])
    QCD-consistent (2-loop MS-bar from alpha_s(M_Z)=0.118):
                      m_tau -> 0.3133, m_b -> 0.2236, M_Z -> 0.1180, m_t -> 0.1076
    constants: m_p = 0.938272, C = 1/phi^2, layer base phi^4

## 7. Sequencing

Phase 46 is the direct answer to the Phase 43 sequencing open question. After it the
standing open items remain: emergent-twist derivation; stable-knot -> SM multiplicity
mapping; and (if Phase 46 is a negative) the alpha_s flavor-closure line is closed as
reference-irreducible and the m_b/M_Z conflict is understood as power-law-vs-log
running, not a golden failure at the reference level.
