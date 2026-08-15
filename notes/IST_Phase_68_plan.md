# IST Phase 68 Plan — The Sheet-Stacking Automaton: D_eff Crossing 3 and the Stopping Rule

**Origin.** The sheet-stacking automaton is the dynamical model of the coherence
threshold that Phase 67's honest negative pointed at: the thread/sheet/strand
factorization does not come from the zero-point dynamics (P0, pre-mereological)
but must emerge above the coherence threshold (P2–P3, crystallized regime).
Phase 66 supplied the suppression factor: each stacking level costs ψ² = 1/φ².
This phase builds the automaton that stacks sheets, measures D_eff(N), and tests
whether the stacking stops at 3 spatial dimensions — closing OQ1 (the stopping
rule) and the coherence-threshold gap from Phase 67.

**The analytic prediction (pre-registered).** If each stacked sheet contributes
D_n = 2·ψ²ⁿ to the effective dimension (the base sheet is 2D; each additional
sheet contributes its 2D surface weighted by the ψ²ⁿ stacking suppression),

  D_eff(N) = Σ_{n=0}^{N-1} 2·ψ²ⁿ = 2·(1 − ψ²ᴺ)/(1 − ψ²)

As N → ∞: D_eff(∞) = 2/(1 − 1/φ²) = 2φ²/(φ² − 1) = 2φ²/φ = 2φ ≈ 3.236.
At N = 3: D_eff(3) = 2(1 + 1/φ² + 1/φ⁴) = 2(1 + ψ² + ψ⁴) ≈ 3.056.

So D_eff crosses 3 at level 3 and asymptotes to 2φ ≈ 3.236. The stopping rule
has two parts: (1) each additional level is suppressed by 1/φ² (the dynamical
slowdown from Phase 66), and (2) level 4 is topologically unstable (knots unknot
in 4D — §4 of the dimensional-emergence note). The combination: D_eff crosses 3
at level 3, and the topological instability at 4D prevents further stable stacking.

**The P3′ locus reading.** The automaton must be built with observer-relative
stacking — no naive global stacking axis. In the P3′ reading (dimensional-
emergence note), the zero point is a locus, not an axis; sheets stack in every/
any direction relative to the observer's Hilbert space. The automaton tests
this: a naive-axis model (stack along one fixed direction) vs a locus model
(stack isotropically, each new sheet oriented by the local coherence structure).
If the locus model gives D_eff crossing 3 and the naive-axis model doesn't,
that's a falsifiable contrast selecting the P3′ reading.

**Hypotheses (pre-registered before compute):**

- **H68a — the D_eff curve.** D_eff(N) = 2·(1 − ψ²ᴺ)/(1 − ψ²) crosses 3 at
  N = 3 and asymptotes to 2φ ≈ 3.236. The level-by-level values: D_eff(1) = 2,
  D_eff(2) ≈ 2.764, D_eff(3) ≈ 3.056, D_eff(4) ≈ 3.168, D_eff(∞) ≈ 3.236.
- **H68b — the stacking automaton (locus model).** A dynamical sheet-stacking
  simulation calibrated on Phase 13 (D_eff → φ for a single sheet under golden-
  connected RG) and Phase 14 (fold feedback pinning to the golden window) reproduces
  the H68a curve: D_eff crosses 3 at 3 stacked sheets. Each new sheet is oriented
  by the local coherence structure (P3′ locus reading), not a fixed axis.
- **H68c — the naive-axis contrast.** The naive-axis model (stack along one
  fixed direction) gives a different D_eff curve — either overshooting 3 (no
  stopping rule) or undershooting (no crossing). The contrast falsifies the
  naive-axis reading and selects the P3′ locus model.
- **H68d — the topological instability at level 4.** At level 4, the stacked
  structure is topologically unstable: the knot stability (Phase 52's 0.044 band)
  drops to ~0 (knots unknot in 4D). The stacking automaton should show a
  stability collapse at N = 4 — the second half of the stopping rule.
- **H68e — OQ1 closed.** The stopping rule, stated dynamically: (1) each
  additional stacking level is suppressed by 1/φ² (Phase 66's ψ²), making
  D_eff converge to 2φ ≈ 3.236; (2) level 4 is topologically unstable (knot
  stability collapses); together these select 3 spatial dimensions. The full
  dynamical statement closes OQ1.

**Honest framing.** H68a is analytic (exact from Phase 66's ψ²). H68b is the
genuinely risky test: the mapping from the analytic suppression to a dynamical
simulation involves design choices (the sheet orientation rule, the coherence
criterion). The P3′ locus reading makes the model non-trivial — the "isotropic
stacking" implementation is a design choice made in the open. H68d depends on
whether the Phase 52 knot-stability computation extends naturally to 4 stacked
sheets; if the stability measure doesn't collapse at N = 4, the topological
instability argument needs revision. Either outcome is informative.

**Deliverables:** `code/phase68_sheet_stacking.py`,
`tests/test_phase68_sheet_stacking.py`, outputs under `code/outputs/phase68/`,
this plan file; if confirmed, OQ1's status changes from open to closed, and the
coherence-threshold gap from Phase 67 is addressed.

**References:**
- `notes/IST_Phase_68_plan.md` (this plan)
- `code/phase66_associator_derivation.py` (ψ² = 1/φ², the suppression factor)
- `code/phase67_quantum_mereology.py` (the coherence-threshold gap)
- `code/phase13_dynamical_rg.py` (D_eff → φ for single sheet)
- `code/phase14_feedback.py` (fold feedback to golden window)
- `code/phase52_sm_partition_cycle.py` (knot stability 0.044)
- `notes/IST_dimensional_emergence.md` (P3′ locus, §4 knot stability, OQ1, §9)
- `notes/IST_phi8_caution.md` (the layer-11 coherence-threshold trap)
