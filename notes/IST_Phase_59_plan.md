# IST Phase 59 Plan — Time-Crystal Dark Energy: Pre-Registered, Look-Elsewhere-Accounted Test

**Origin (literature-grounded).** The user's literature sweep
(`Downloads/Kimi_Agent_IST paper sourses/ist_lit/`) returned the time-crystal
front: **Berti et al. 2026 ("Stratoverso")** is already running *log-periodic*
modulations of structure growth against **DESI DR1 full-shape + DESI DR2** with
Bayesian MCMC, claiming to address the H0/S8 tensions; Hewitt (2025) finds
putative GW echoes at prime-number intervals; Panagis (Unified Field Continuity)
reports log-periodic features in the low-redshift Hubble diagram. The arena for
an oscillatory dark-energy signal has therefore moved from the 60-point H(z)
compilation to DESI-era full-shape data — which IST does not yet analyze. This
phase is the honest precondition: **does the time-crystal modulation that Plan
11 claimed (a *plan*, never a phase) actually survive its own data, under a
pre-registered prediction and a look-elsewhere accounting?**

**What Plan 11 actually reported.** `code/oscillatory_dark_energy.py` fitted a
log-periodic ΛCDM extension
H(z) = H0·√[Ωm(1+z)³ + (1−Ωm)(1 + ε·cos(2π/Δ·ln(1+z) + φ0))]
to 60 H(z) points (z ≤ 2.36): Δχ² = 3.38, tension with SH0ES cut 1.94σ → 0.29σ,
**fitted** Δ = 1.54, ε = 0.136. The note itself flagged Δχ² < 6, AIC favoring
ΛCDM, and ε being ~57× the derived α/φ² anchor. Plan 11 was a *fitting*
exercise: **no parameter was pre-registered, and no look-elsewhere accounting
was applied to the free-period search.** Phase 59 fixes both.

**Pre-registration (stated before any fit in this phase):**

1. **Amplitude anchor** ε0 = α/φ² = **0.0027873** — the associator coupling in
   the IST master equation M = (f/2π)·I_topo + (α/φ²)·Ξ + δ_tc
   (`code/unified_mass_analysis.py`). *Note:* the old Plan 11 note's "0.00239"
   is a ~14% documentation discrepancy vs the exact α/φ² — flagged, not
   silently reused.
2. **Period anchor** Δ0 = ln(φ) = **0.4812** — the golden self-similarity
   period. A modulation cos(2π/Δ·ln(1+z)) that is invariant under golden
   rescaling (1+z) → φ·(1+z) must satisfy 2π/Δ·ln(φ) = 2πn, i.e. Δ = ln(φ)/n;
   the fundamental period is Δ0 = ln(φ). This is the standard
   log-periodic/Sornette parameterization of Fibonacci self-similarity.
3. **Secondary period anchor** Δ1 = φ = 1.6180 ("one cycle per φ e-folds"),
   expected disfavored, included to make the anchor family explicit and
   immune to post-hoc picking.

**Tracks.**

- **H59a — strict amplitude anchor.** Fix ε = ε0; fit (H0, Ωm, Δ, φ0). Is the
  master-equation amplitude visible at all in H(z)? Expectation: Δχ² ≈ 0 — a
  0.28% density modulation is far below the ±15% chronometer errors. This is
  the honest statement that the *cosmological-scale* modulation is not (yet)
  shown to equal the fundamental α/φ² amplitude.
- **H59b — golden period anchor.** Fix Δ = Δ0 = ln(φ); fit (H0, Ωm, ε, φ0).
  The data then span ln(1+zmax)/Δ0 = **2.5 cycles** (vs 0.79 cycles at the
  fitted 1.54) — the golden period is *well constrained by the same data*.
  Report whether free ε at the golden period is compatible with 0 (i.e., is a
  modulation with the golden period demanded?).
- **H59c — free-Δ scan with look-elsewhere accounting.** Scan Δ ∈ [0.3, 5.0],
  fit (H0, Ωm, ε, φ0) at each grid point, build Δχ²(Δ). Apply the Phase-54
  look-elsewhere philosophy via the frequency-band trial count
  N_ind = (1/Δmin − 1/Δmax)·ln(1+zmax), and report the *global* significance of
  the best Δ. Re-examines whether Plan 11's "0.29σ tension cut" is real or a
  chance fluctuation of the free period. The fitted 1.54 sits near 3·ln(φ) =
  1.4436 (6% off) *and* π/2 = 1.5708 (2% off) — precisely the multi-candidate
  situation look-elsewhere accounting exists for.
- **H59d — cycle coverage + detection forecast.** Quantify why Δ was
  unconstrained (partial-cycle coverage at large Δ), and how much better H(z)
  precision would be needed to reach a 3σ detection of the derived amplitude
  ε0 and of the fitted ε = 0.136. States what DESI-era data (Berti's arena)
  would have to deliver.

**Honest framing (for plan/paper).** Phase 59 is not a search for a detection;
it is the audit Plan 11 never got. If (as expected) the strict anchors give
Δχ² ≈ 0 and the free-Δ global significance is ≲2σ, the honest verdict is:
*Plan 11 remains a plausible but unverified prediction — consistent with ΛCDM
in the 60-point H(z) data after look-elsewhere accounting; its falsifiable
golden-period form (Δ = ln φ, 2.5 cycles, ε = α/φ²) is a prediction to test in
the DESI DR1/DR2 full-shape arena, not a detected signal.* The numbers decide.

**Deliverables:** `code/phase59_timecrystal_lookelsewhere.py`,
`tests/test_phase59_timecrystal_lookelsewhere.py`, outputs under
`code/outputs/phase59/`, `notes/IST_Phase_59_plan.md`.

**Phase-map sync (all three + retrospective):** README.md (highlights section
after Phase 58), `main/cross_phase_synthesis.md` (row 59),
`main/synthesis_paper.md` (§8.1ah + observable prediction #17, footer bump to
v2.8), `notes/retrospective_cross_analysis.md` (Phase 59 entry). Registry
appended (60 → 64 rows).
