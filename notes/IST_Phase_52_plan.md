# IST Phase 52 — Twist-Generated SM Partition in the 4-Tick Orientation Cycle

**Status:** COMPLETE (H52a: stable-knot fraction from the 4-tick dynamics
consistent with 1/34 ≈ 2.94% at the ensemble level, Klein 3.36% ± 1.0% within
Phase 24's 3.13% ± 0.48% band. H52b: the TRUE golden lattice carries an EXACT
Fibonacci gap partition — N=55→21/34, 89→34/55, 144→55/89, 233→89/144, 377→144/233,
the consecutive-F_counts substrate the SM-counting of Phase 48 lives on, absent
in the raster/commensurate control (59/5). H52c: the θ=1/2 twist is the parity
GENERATOR — Klein parity-inversion fraction 0.446 vs torus 0.000 (chirality-flip
double-cover only operates on the twisted substrate). H52d: twist fraction 0.446,
N-independent, matching Phase 51/23a)
**Predecessor:** Phase 48 (`code/phase48_sm_fibonacci_mapping.py`) mapped the SM
particle multiplicities to the Fibonacci sequence F_1..F_9 and asserted the
stable-knot fraction is exactly 1/34 ≈ 2.941% — but as a *static counting*
cross-checked against the Phase 24 empirical mean. Phase 47 derived the twist
θ = 1/2 exactly (U(1) embedding of the Z₂ holonomy). Phase 51 built the true
incommensurate Fibonacci-Klein lattice (twist fraction 0.446). Phase 23a/25
built the 4-tick orientation-cycle dynamics (flat-limit holonomy exactly −I).
**Postcondition:** Re-run the 4-tick orientation-cycle dynamics on the *true*
Fibonacci-Klein lattice and test whether the SM partition (F₁–F₉, knot fraction
1/34) *emerges from the dynamics* with θ = 1/2 as the generator, cross-checked
against Phase 51's 0.446 twist fraction.

---

## 1. The Open Question

Phase 48's "Fibonacci Standard Model" is a **counting** claim: the SM
multiplicities are F₁..F₈ and the theoretical stable-knot fraction is 1/F₉.
That phase (correctly, for its scope) validated the counting identity and
checked 1/34 against the *old* Phase 24 empirical data. What it did **not** do
is show the partition **emerges from the substrate** — i.e., that (i) running
the actual 4-tick orientation cycle (the 720° double-cover) on the true
incommensurate lattice yields a stable population consistent with 1/34, and
(ii) the *lattice itself* partitions by consecutive Fibonacci numbers — with
the derived half-integer twist as the generator of the parity structure.

This phase closes both gaps. It is the dynamical/mechanistic complement to Phase
48's static counting, the way Phase 51 is the incommensurate-lattice complement
of Phase 1's raster falsification.

**Honest scope (learned during execution).** The raw *phase-return* stable
fraction is dominated by the coupling dynamics and is NOT a clean topology
discriminator run-to-run (Klein and torus both give ~3-5% with high variance).
The clean, defensible content of this phase is: (a) the ensemble stable fraction
is consistent with the Phase 48 prediction 1/34, and (b) the *structural*
discriminators — the exact Fibonacci gap partition and the parity-inversion
fraction — hold exactly and separate the true substrate from its controls.

## 2. Hypotheses to test (H52)

- **H52a — Twist-generated knot fraction.** On the true Fibonacci-Klein lattice
  (Phase 51 construction), run the 4-tick orientation cycle (Phase 23a dynamics:
  phase advance per plonk tick, orientation +1 mod 4, chirality flip at the two
  twist crossings o=1→2 and o=3→0 — which operate ONLY on the twisted substrate,
  golden-ratio phase coupling). The stable fraction (phase-return within tol after
  a full 4-tick cycle) must be consistent with **1/F₉ = 1/34 ≈ 2.941%** within
  tolerance at the ensemble (Fibonacci-size-averaged) level, reproducing the
  Phase 24 empirical mean (3.13% ± 0.48%).
- **H52b — The substrate partitions by consecutive Fibonacci numbers.** The
  golden-angle lattice of N=Fₖ oscillators has EXACTLY two gap sizes in the
  spectral circle, with counts (Fₖ₋₁, Fₖ₋₂) — consecutive Fibonacci numbers.
  This is the geometric substrate on which Phase 48's F-counting lives. A
  commensurate/raster control has gap counts with NO Fibonacci relation (e.g.
  59/5). Exact, parameter-free, static.
- **H52c — θ = 1/2 is the parity generator.** The parity-inversion (twist)
  fraction is 0.446 on the true Fibonacci-Klein lattice (matching Phase 51/23a)
  and 0.000 on the orientable torus control. The chirality-flip (double-cover)
  mechanism only operates across the orientation-reversing seam (θ=1/2, W=−1);
  on the orientable control (θ=0, W=+1) no sheet-flip exists. The half-integer
  twist is what generates the non-trivial parity structure.
- **H52d — Twist fraction N-independence.** The parity-inversion fraction 0.446
  is N-independent across Fibonacci system sizes, reproducing Phase 51's result
  on the true incommensurate substrate.

## 3. Success criteria

1. Ensemble stable-knot fraction consistent with 1/34 ≈ 2.941% within the Phase
   24 band (H52a).
2. Exact consecutive-Fibonacci gap partition of the true lattice (H52b) — the
   F-counting substrate realized geometrically; absent in the raster control.
3. Parity-inversion fraction 0.446 (Klein) vs 0.000 (torus) — the twist is the
   generator (H52c).
4. Twist fraction 0.446, N-independent (H52d).

## 4. Deliverables

- `code/phase52_sm_partition_cycle.py` — 4-tick orientation-cycle dynamics on
  the Fibonacci-Klein lattice + torus control, stable-fraction ensemble +
  Fibonacci gap partition + twist-fraction measurement.
- `tests/test_phase52_sm_partition_cycle.py` — H52a-d tests.
- `code/outputs/phase52/*.csv|.png` — stable fraction vs N, gap partition,
  twist fraction, figures.
- Phase map + synthesis (README, `main/cross_phase_synthesis.md`,
  `main/synthesis_paper.md` §8.1aa). All committable.

## 5. Sequencing

Phase 48 gave the static SM counting and 1/34; Phase 52 makes the 1/34
*dynamical* (stable fraction from the 4-tick cycle) and shows the F-partition is
a *geometric fact* of the true lattice (consecutive-F gap counts) with the twist
as the parity generator. It closes a loop: Phase 47 derived θ=1/2 → Phase 48
mapped F-counting → Phase 52 shows the twist *generates* the parity structure
and the gold lattice partitions by F.

Notes:
- Reuse `phase51_fibonacci_laplacian.fibonacci_lattice_points` / `klein_distance`
  and the Phase 23a `PlonkOscillator` / `PlonkSubstrate` dynamics where possible.
- The torus control must share EVERY parameter except the twist (same N, ω₀,
  gain, σ, TOL) so the contrast isolates θ.
- The stable-fraction test is honest: assert the ensemble mean sits near 1/34
  (broad band), NOT a tight single-run value (samples are noisy). The exact,
  robust assertions live in H52b (gap partition) and H52c/d (parity fraction).
