# IST Phase 57 Plan — The Single- vs Dual-Strand Discriminator

**Question:** Phase 55 built the photon as a dual-mode (DNA double-helix) wave
function. But the repo's OLD photon default — `"no knot -> v=c, m=0"`
(`ist_toolkit_v2.py`) — was a single structureless strand and was never tested.
Could a single bare strand also be a photon?

**Why this matters:** if a single strand can serve as the photon, the dual-mode
helix is not forced and the achiral premise of Phases 55/56 (parity-inversion
0.000, the parity-odd 4WM channel = 0) is a free choice, not a requirement. If
the dual-mode geometry IS forced, then the achirality (and the Phase 56 vacuum
selection rule) is a consequence of the substrate, which is what Phases 55–56
claim. This phase is the highest-information test of that core assumption.

**The two halves of the answer (the crucial asymmetry):**

1. **Speed does NOT discriminate.** A single translating strand also moves at
   v_g = 1.00000 (shared linear dispersion). The old default passed every
   speed/massless test — which is exactly why it was never caught. Speed alone
   cannot tell a photon from a fermion.
2. **Parity DOES discriminate.** A single strand threading the non-orientable
   Klein seam must flip chirality at 2 ticks: its parity-inversion is the
   COMPUTED lattice twist fraction **0.446** (numerically identical to the
   electron knot, Phase 52 H52c). Only the rung-bound dual mode, whose
   symmetric rung-crossing makes sheet-swap a symmetry, gives **0.000**.
   A single-strand "photon" is chirally indistinguishable from a fermion — it
   cannot be the parity-conserving photon.

**Tracks:**

- **H57a — The parity discriminator (core).** Single strand: parity-inversion
  0.446, computed on the true Fibonacci-Klein lattice (N = 210/360/480), vs
  dual-mode 0.000 — both at the shared v_g = 1.00000. Speed is degenerate;
  parity is the separator.
- **H57b — Two polarizations need two strands.** Helicity-mode count: single
  strand = 1, dual mode = 2 (E₊, E₋). The physical photon has two transverse
  polarizations; a single strand cannot supply the doublet.
- **H57c — The bare "no knot" default disperses.** A localized single-strand
  excitation evolved on the Klein proximity graph (free Schrödinger walk, no
  rung binding) spreads: amplitude concentration collapses (1.0 → ~0.03), while
  the rung-bound dual-mode compound stays at 1.0 (rigid translation, Phase 55
  rung-lock 0.0000). Without the rungs there is nothing holding the photon
  together.
- **H57d — Registry + consistency.** Append Phase-57 rows to the Phase-54
  registry (relation_registry.csv, 53 → 56 relations); DEMOTE the old
  `"no knot -> v=c"` default to "speed-only, insufficient"; confirm consistency
  with Phases 55 (dual-mode achirality) and 52 (electron = single-strand knot,
  0.446).

**Deliverables:** `code/phase57_singlestrand_discriminator.py`,
`tests/test_phase57_singlestrand_discriminator.py`, outputs under
`code/outputs/phase57/`, `notes/IST_Phase_57_plan.md`.

**Phase-map sync (all three + retrospective):** README.md (new highlights
section after Phase 56), `main/cross_phase_synthesis.md` (row 57),
`main/synthesis_paper.md` (§8.1af + observable prediction #15, footer bump to
v2.6), `notes/retrospective_cross_analysis.md` (Phase 57 entry). Registry
appended.

**Honest framing (for the plan and paper):** the phase's value is a
discriminator, not a numeric fit — 0.446/0.000 and 1/2 are structural counts
and a computed lattice fraction. It does not add a free parameter; it closes the
last loophole in the photon model by excluding the untested single-strand
default. The surviving falsifiable core remains Phase 55's 0.000 achirality (a
measured 0.446-like photon twist would contradict the double-helix geometry).
