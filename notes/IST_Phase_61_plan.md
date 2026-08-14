# IST Phase 61 Plan — Spin-Statistics from Seam Braiding (Z₂ Exchange Holonomy)

**Origin (external gap).** Spin-statistics — why fermions exchange with phase −1
and bosons with +1, and why two identical fermions exclude each other — is an
*input* of the framework, not an output. QFT imports it as a theorem of
relativistic causality; IST should derive it from the substrate. The machinery
already exists: Phase 47 derives the meridian holonomy W = −1 (θ = 1/2) from
the Z₂→U(1) embedding; Phase 25 computes the 4-tick SU(2) holonomy, flat limit
EXACTLY −I (the "fermionic sign"); Phases 52/55/57 establish the strand
dichotomy — electron = single-strand knot (parity-inversion 0.446), photon =
dual-strand rung-bound compound (0.000). This phase closes the gap: **the
exchange (braid) phase of two identical structures is the holonomy of the
substrate's Z₂ seam connection along the exchange loop, and the strand count
determines how many times that loop threads the meridian.**

**The derivation (pre-registered).**

1. Exchanging two identical objects on a 2D substrate is a *braid*, not a
   rotation. In 2D the braid generator σ is not deformable to σ⁻¹, so in
   principle the exchange can carry any phase (anyons). IST must show why the
   phase is exactly ±1 — and it can: the seam is a **flat Z₂ connection**
   (Phase 47) with holonomy group {+1, −1}, so the phase is quantized to ±1
   before the 3D question even arises. The emergent 3D stack then forces
   σ = σ⁻¹ (unknotting room), i.e. σ² = e — the double-exchange identity —
   which the Z₂ quantization already satisfies. **Both arguments converge on
   ±1; neither is assumed.**
2. The exchange loop of a structure is one full 360° relative winding = one
   4-tick temporal cycle on the double cover (Phase 25). The exchange phase is
   the holonomy of that cycle. Measurably: the 4-tick SU(2) cycle product is
   exactly **−I** for the single-strand (spinor) excitation — the flat-limit
   fermionic sign Phase 25 already verified — and the two seam crossings per
   cycle are the two half-twists of one 360° rotation (a spinor needs 720° =
   two cycles to return, Phase 29's "2 traversals"). Extracting the U(1)
   phase: **χ(single) = −1 (fermion)**.
3. A **dual-strand** structure (photon: rung-bound, sheet-swap symmetric,
   achiral, parity-inversion 0.000) never flips — its temporal cycle has NO
   seam crossings (the compound is single-valued on the base). Its cycle
   holonomy is **+I** → **χ(dual) = +1 (boson)**.
4. On the orientable torus control there is no seam (W = +1, Phase 47 H47d):
   no crossings, cycle holonomy +I → χ = +1 for *both* strand types —
   **there are no fermions without the twist.** The two lattice-computed
   quantities that anchor χ: the meridian Wilson loop W = −1 (odd seam count;
   H61a) and the temporal cycle holonomy ±I (Phase-25 machinery on the true
   lattice; H61a). No free parameters: the strand structure (single/dual) is
   the measured Phase 55/57 dichotomy.
5. Pauli exclusion follows algebraically: two identical fermions in the same
   state must live in the antisymmetric sector (χ = −1), whose diagonal
   (double-occupancy) part vanishes: (1 + P)|i,i⟩ = 0. The forbidden
   configuration is annihilated topologically, not by decree.

**Hypotheses (pre-registered before compute):**

- **H61a — The exchange phase is the substrate holonomy.** Recompute on the
  true Fibonacci-Klein lattice: (i) the meridian Wilson loop W = −1, grid-
  independent (Phase 47 H47b re-derived on the incommensurate lattice, not the
  raster mock); (ii) the 4-tick temporal cycle holonomy (Phase-25 machinery):
  −I → phase −1 for the single-strand (seam-threading, two half-twist
  crossings per cycle), +I → phase +1 for the dual-strand (achiral, no
  crossings), +I for the torus (no seam, either strand). Exchange phase χ =
  the cycle phase: single-strand → **−1**; dual-strand → **+1**; torus →
  **+1 both**.
- **H61b — The exchange operator algebra (Pauli exclusion).** Build the
  two-particle exchange operator P|i,j⟩ = χ|j,i⟩ on the N-site lattice
  Hilbert space. Verify: P² = I (double exchange = identity, the ±1 collapse);
  fermions: (1 + P)|i,i⟩ = 0 for all i (exclusion — double occupancy
  annihilated); bosons: (1 − P)|i,i⟩ = 0 (antisymmetric double occupancy
  annihilated, symmetric survives → occupancy allowed); mixed species:
  (1 + P)|f,b⟩ ≠ 0 (no exclusion between different particles).
- **H61c — The anyon collapse is the Z₂ holonomy.** (i) The holonomy group of
  the flat seam connection is {+1, −1}: Wilson loops over a cycle basis of the
  Klein graph take only ±1. (ii) Contrast: a *continuous* U(1) holonomy
  W = e^{iθ}, θ ≠ π, gives P² = e^{2iθ} ≠ I and non-±1 eigenvalues — genuine
  anyonic double-exchange, no clean exclusion. The Z₂ is therefore load-
  bearing, not decorative. (iii) Honest guard: the exchange phase is **not**
  the random-pair geodesic twist flag (the 0.446 single-strand fraction,
  H52c) — the statistics is the *loop* holonomy W = −1, a global invariant;
  test that the naive pair-flag identification fails, and register it.
- **H61d — Consistency + registry.** Single-strand ↔ electron (parity 0.446,
  Phase 52/57) ↔ fermion (−1); dual-strand ↔ photon (0.000, Phase 55/57) ↔
  boson (+1); torus control (W = +1, Phase 47 H47d) ↔ both bosonic. The
  dimensional-emergence note's strand classifier (single-strand ⇒ seam parity)
  then **predicts the neutrino is a fermion** (single-strand) — consistent
  with observation, and the next case to classify in the runtime. Registry
  appended (69 → ~73 rows).

**Honest framing.** The one free-looking input is the strand count k — but k is
not free: it is the measured strand structure of Phases 55/57 (single-strand
electron, dual-strand photon). The exchange phase then contains no adjustable
parameters. The phase's honest scope: it derives spin-statistics *from the
already-derived Z₂ holonomy and the already-measured strand structure*; it does
not re-derive W = −1 itself (that is Phase 47) — it composes the existing
machinery into the missing statistics result. Expected outcomes range from a
clean derivation (χ(1) = −1, χ(2) = +1, P² = I, exclusion verified) to an
honest negative (if the algebra or holonomy does not cohere, the gap stays
open, now with a precise statement of why).

**Deliverables:** `code/phase61_spin_statistics.py`,
`tests/test_phase61_spin_statistics.py`, outputs under `code/outputs/phase61/`,
`notes/IST_Phase_61_plan.md` (this file).

**Phase-map sync (all three + retrospective):** README.md (highlights section
after Phase 60), `main/cross_phase_synthesis.md` (row 61),
`main/synthesis_paper.md` (§8.1aj + observable prediction #19, footer bump to
v2.10), `notes/retrospective_cross_analysis.md` (Phase 61 entry). Registry
appended (69 → ~73 rows; counts stated from the file).
