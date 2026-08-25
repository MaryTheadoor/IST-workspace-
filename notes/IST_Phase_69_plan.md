# IST Phase 69 Plan — Gravity from Thread-Counting: The 1/r² Law

**Origin.** The queue's remaining big derivation (status memo item 3). The
existing gravity note (`notes/gravity_from_dimensional_collapse.md`) uses a
*dimensional-collapse* mechanism with a Gaussian kernel and explicitly
**resolves** that it does NOT reproduce 1/r² ("IST does not reproduce 1/r²;
predicts exponential cutoff"). This phase attacks the *other*, unstarted
approach: derive the **inverse-square law from counting stretched lattice
threads**. The two mechanisms are different, not contradictory — this phase
shows they agree at short range and that thread-counting supplies the
infinite-range inverse-square sector the dimensional-collapse note lacks.

**The derivation (three ingredients, each already established in the repo).**

1. **Mass ∝ thread count.** `notes/emc2_in_IST.md`: a knot of mass M freezes
   I_topo = Mcℓ/(2πℏ) information threads; E = mc² = I_topo·(2πℏc/ℓ). So a mass
   *emits* N ∝ M threads. This is a derived identity, not an assumption.

2. **Thread conservation (no cutoff).** Phase 65: the zero point makes
   information conservation exact (Ω_inv∘Ω = identity, |λ|=1, closed cycle).
   Threads are not dissipated as they traverse — so flux is conserved and the
   interaction is **infinite-range**, in exact contrast to the Gaussian kernel
   of the dimensional-collapse note (which is why that note got an exponential
   cutoff).

3. **D = 3 shell spreading.** Phase 68: D_eff crosses 3 at three stacked sheets
   and asymptotes to 2φ ≈ 3.236 — the emergent spatial dimension is 3. Threads
   spreading isotropically over a 3-shell have area 4πr², so flux density ∝ 1/r².

Combining: force between masses M, m = (thread tension τ) × (thread flux
density at the target) ∝ (τ) × (M·m)/(4πr²). Therefore

  **F = G·M·m/r² with G = τ/(4π),**

where τ is the per-thread tension (energy per thread per unit length) —
dimensionally fixed by the substrate scale. The **exponent −2 is derived**,
not assumed: it is the emergent-projected statement that thread flux is
conserved across the 3-shell. It depends on D_eff = 3, so the inverse-square
law is itself cross-validating evidence for Phase 68's dimensional selection.

**Hypotheses (pre-registered before compute):**

- **H69a — mass ∝ thread count.** The number of threads frozen into a knot is
  exactly linear in M (from the emc² formula): N(M) = Mcℓ/(2πℏ), an exact
  proportionality with no free exponent.
- **H69b — conserved flux gives 1/r² (not exponential).** A discrete lattice
  emitting N ∝ M threads from a source and counting them on concentric shells
  (distributed by the golden-angle spiral — the IST anti-resonant isotropic
  distribution, Phase 6) gives a flux density falling as **r^(1−D)**, i.e. a
  fitted log-log slope of **−2** for D=3, with zero exponential tail. This
  supersedes the dimensional-collapse note's "no infinite-range tail" resolve.
- **H69c — Newton's constant from the substrate.** F = τ·N(M)·N(m)/(S_D(r)·ℏc)
  assembling to G·Mm/r² with **G = τ/(4π)**; G is mass-independent (a function
  of geometry + thread tension only). If the plonk scale ℓ ≈ ℓ_P, G matches the
  measured value to O(1); the honest gap is fixing ℓ from first principles.
- **H69d — exponent tracks the dimension.** The force exponent is exactly
  −(D−1): for D=2 it is −1, for D=4 it is −3. Therefore an inverse-square law
  *requires* the substrate to stack to exactly D=3 — a cross-validation of
  Phase 68 (and a falsification of the Phase-68 naive-axis 4D overshoot, which
  would give 1/r³).
- **H69e — the reconciliation.** A side-by-side of the two IST gravity
  mechanisms: dimensional-collapse (Gaussian, short-range, exponential cutoff)
  vs thread-counting (conserved flux, long-range, 1/r²). They agree at short
  range and the thread-counting sector supplies the Newtonian infinite-range
  tail. Verdict: IST does have an inverse-square Newtonian sector (the
  dimensional-collapse note's RESOLVED claim is revised).

**Honest framing.** The exponent and the G-structure are the new content; the
absolute normalization of G still requires fixing the substrate scale ℓ (the
same gap the dimensional-collapse note flagged as Open Question #3). H69c's
O(1) matching is a plausibility check, not a first-principles derivation of G's
magnitude. H69e is a framework-level reconciliation, and it revises a prior
"RESOLVED" claim in the dimensional-collapse note — a deliberate, documented
supersession. The derivation is no longer a restatement of Gauss's law because
the conservation (Phase 65) and dimensionality (Phase 68) that make the
exponent exact are both *derived results of the substrate*, not inputs.

**Deliverables:** `code/phase69_gravity_thread_count.py`,
`tests/test_phase69_gravity_thread_count.py`, outputs under
`code/outputs/phase69/`, this plan file.

**Independent cross-validation.** The parallel-agent note
`IST_gravity_as_latency_gradient.md` (added 2026-08-26) independently converges
on the same thread-counting → 1/r² skeleton in D = 3 (its §2.3 and H-GRAV1
"count thread crossings through shells of radius r; fit against 1/r²" is
exactly the H69b count-don't-inject prescription). Its honest caveats are the
correct framing of the open remainder: H-GRAV2 (the attraction SIGN is NOT
automatic — the 2+1-D no-attraction theorem is the canonical way the picture
dies) and H-GRAV3 (a full METRIC with g_tt AND g_ij, not just a force law) are
deliberately OUT OF SCOPE for this derivation, which establishes the static
inverse-square skeleton only.

**References:**
- `notes/gravity_from_dimensional_collapse.md` (the mechanism to supersede)
- `notes/emc2_in_IST.md` (mass ∝ thread count)
- `code/phase65_signature_duality.py` (thread/zero-point conservation)
- `code/phase68_sheet_stacking.py` (D_eff = 3)
- `code/phase6_phi_attractor.py` (golden-angle anti-resonant distribution)
- `IST_gravity_as_latency_gradient.md` (parallel-agent cross-validation; H-GRAV1)
