# IST Phase 55 — The Photon as a Dual-Mode Wave Function (DNA Double Helix
# Across Both Sides of the Manifold)

**Status:** COMPLETE. First phase to model photon DYNAMICS (registry gap: zero
photon-propagation entries before this). Supersedes the repo's scattered
photon defaults ("no knot → v=c, m=0" in `ist_toolkit_v2.py`; "information knot
with I_topo=1, no rest mass" in `emc2_in_IST.md`) with an explicit,
numerically-tested propagating model: the photon is a dual-mode wave function
ψ = (E₊, E₋) whose two strands cross the zero point like a DNA double helix.
**Predecessor:** `code/phase52_sm_partition_cycle.py` (4-tick orientation cycle,
electron knot, twist fraction 0.446); `code/phase51_fibonacci_laplacian.py`
(Fibonacci-Klein lattice). **Postcondition:** the photon's achirality, massless
E=hν, universal speed, and single-species status are each measured on the
framework's own substrate.

---

## 1. The Open Question

The repo had NO model of photon propagation: `ist_toolkit_v2.py` simply says
"photon: no knot → v=c, m=0"; `emc2_in_IST.md` calls the photon an
"information knot with I_topo=1, no rest mass"; Phase 48 assigns F₂=1. The
external gap analysis noted the photon is the framework's least-justified
particle. Phase 55 supplies the missing dynamics and, in doing so, sharpens the
gap-7 (4WM experiment) discriminator: a photon whose self-interaction is
structured (dual-mode) rather than point-like has a testable internal
structure.

## 2. The Physics Idea

The user's mental picture, adopted as the model's geometry: **a DNA double
helix**. Two strands — the two circular-polarization (helicity) modes E₊ and E₋
— each carry the peak of the amplitude propagation. The connecting **rungs go
across the zero point**: the transverse coupling ties E₊ to E₋ through the
manifold seam. Because the rungs cross symmetrically, parity (E₊ ↔ E₋) leaves
the helix invariant → the photon is achiral (spin-1), in sharp contrast to the
electron knot, which as a SINGLE strand must traverse the seam and flip
chirality (0.446, Phase 52).

This gives the substrate-native reason for the four photon facts:

- **Universal c** — both strands share one group velocity v_g = dω/dk,
  independent of the carrier (energy) frequency ω₀.
- **Achiral spin-1** — rungs cross the zero point symmetrically →
  parity-inversion EXACTLY 0.000.
- **Massless, E=hν** — energy linear in ω₀ while v_g stays constant.
- **Single species F₂=1** — two strands, one gapless branch, one U(1) mode.

## 3. Tracks and Results

| track | claim | measurement | verdict |
|---|---|---|---|
| H55a | dispersion-free translation | v_g = 1.00000 for ω₀ ∈ {0,…,1.2}; rung-lock 0.0000 (helix never unbinds); packet non-dispersing | PASS |
| H55b | achirality (spin-1) | photon parity-inversion **0.000** vs electron knot **0.446** (N = 210/360/480) | PASS |
| H55c | massless, E = h·ν | E = ω₀ **exactly** (linear, slope 1.0); v_g constant as energy added | PASS |
| H55d | single species F₂=1 | one gapless branch, two helicity modes on it | PASS |

## 4. Success criteria / verdict

- [x] H55a — group velocity constant across ω₀; dual helix translates rigidly (rung-lock 0.0000).
- [x] H55b — photon achirality 0.000 measured on the true Fibonacci-Klein lattice; electron 0.446 contrast.
- [x] H55c — E = h·ν exact linear; v_g independent of carried energy (m = 0).
- [x] H55d — single U(1) species: one gapless branch, two shared helicity modes.
- [x] First photon-DYNAMICS phase; registry note added (no more "photon = no knot" default).

## 5. Relation to gap analysis

Gap 7 (4WM tabletop experiment) now has a sharper target: the dual-mode photon's
structured self-interaction (rung coupling across the zero point) is the
non-QED feature a four-wave-mixing probe could discriminate. Gap 2 (log β)
remains a candidate follow-up; gap 4 (convention-circularity) untouched here.

## 6. Deliverables

- `code/phase55_photon_compound.py` (+ `code/outputs/phase55/{dispersion,achirality,energy,twist_fraction}.csv`, `photon_dual_mode.png`)
- `tests/test_phase55_photon_compound.py` (8 tests)
- Phase map + synthesis update (README, cross_phase, synthesis_paper, retrospective).
