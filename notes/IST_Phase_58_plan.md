# IST Phase 58 Plan — The Trace-Map RG: Rescoring Phase 51's Spectral-Dimension Negative

**Origin (literature-grounded).** The user added a research-paper sweep
(`Downloads/Kimi_Agent_IST paper sourses/ist_lit/`). Among it, the quasicrystal
front returned the canonical references for the Fibonacci substrate:
**Naumis (2003, J. Phys.: Condens. Matter 15)** and **Jagannathan (2021,
Rev. Mod. Phys. 93, 045001)**. Naumis's key point: for quasiperiodic systems the
*trace map* is the natural renormalization, RG *stability* is the diagnostic
for localization, and real-space block-spin decimation is **inappropriate** for
such systems.

**Hypothesis.** Phase 51 H51c reported D_eff ≈ 2.2 (r² ≈ 0.995), *never φ*,
under **spectral (Galerkin) coarse-graining** — a block-spin-type RG. The
literature suggests this may be a *probe artifact*: the wrong RG for an
incommensurate substrate, so φ's home is missed. Phase 58 tests whether the
natural (substitution/trace-map) RG locates φ **exactly**.

**Results (confirmed):**

- **H58a — the wrong RG is non-convergent and never golden.** Block-spin
  Galerkin coarse-graining of the Fibonacci-Klein lattice gives D_eff that
  never approaches φ (min |D_eff − φ| ≈ 0.54, an order of magnitude above the
  scheme's own scatter), does not settle onto a clean fixed point (range ~0.14
  across levels), and the deepest projection degrades fit quality (r² drifts
  down). No golden fixed point.
- **H58b — the natural RG is golden-EXACT.** The substitution RG that generates
  the chain (A→AB, B→A) — the correct RG for this system — has growth
  eigenvalue F_{n+1}/F_n → **φ exactly** (parameter-free; error 9.8×10⁻⁹ at
  generation 19). Its spectral kernel is the **KKT trace map** (recurrence
  2.3×10⁻¹³, Fricke invariant conserved 4.7×10⁻¹⁰) — Phase 51 H51a's exactness
  reused.
- **H58c — the verdict.** φ is an **RG (inflation) eigenvalue** of the golden
  substitution, *not* a static spectral dimension D_eff. Phase 51's negative is
  **rescored, not overturned**: it was right that φ is not D_eff, and the
  literature now explains *why* (wrong RG). This is *consistent with* Phase
  51's own conclusion that "the golden structure lives in the Cantor gap
  hierarchy."
- **H58d — registry + consistency.** Phase-54 registry appended (56 → 60 rows).

**Honest framing (for plan/paper).** Phase 58 does **not** overturn Phase 51.
It converts a reported negative into a *mechanistically explained* one and
shows where φ *does* live in the RG structure of the substrate (the inflation
eigenvalue), with the exactness coming from a parameter-free Fibonacci identity
(F_{n+1}/F_n → φ) rather than a fit. The block-spin D_eff ≈ 2.2 result stands;
the phase's contribution is to attribute it to the probe RG.

**Deliverables:** `code/phase58_trace_map_rg.py`, `tests/test_phase58_trace_map_rg.py`,
outputs under `code/outputs/phase58/`, `notes/IST_Phase_58_plan.md`.

**Phase-map sync (all three + retrospective):** README.md (highlights section
after Phase 57), `main/cross_phase_synthesis.md` (row 58),
`main/synthesis_paper.md` (§8.1ag + observable prediction #16, footer bump to
v2.7), `notes/retrospective_cross_analysis.md` (Phase 58 entry). Registry
appended (56 → 60 rows).