# IST Phase 45 — Baryon Octet: Λ–Σ Mixing as the Golden Partition

**Status:** COMPLETE — the golden partition CLOSES the octet (Σ predicted to
0.007%, both splits < 0.2%, base-specificity 0.38% basin selects 1/φ²,
GMO 0.57%)
**Predecessor:** Phase 34 (`code/phase34_baryon_ladder.py`) — decuplet is the
clean SU(3) equal-spacing E-ladder; the octet was left OPEN ("internal Λ–Σ
mixing not captured by the simple E-ladder"). Phase 35 derived the decuplet
from the double-cover + f_Klein; the octet remained unresolved.
**Open question resolved:** is there a principled, parameter-free structure
for the baryon octet's internal mass gaps, or is the Λ–Σ mixing genuinely
irreducible? (Answer: the Λ→Ξ mass interval is GOLDEN-PARTITIONED by Σ.)

---

## 1. The octet residual, restated

PDG 2022 octet masses (MeV):

    N = 938.92   (nucleon, isospin average)
    Λ = 1115.68  (I=0 singlet)
    Σ = 1193.15  (I=1 triplet average)
    Ξ = 1318.28  (isospin average)

Phase 34's honest negatives:

    Λ − N = 176.76 MeV  ~ (9/10) E   (0.47%)
    Ξ − N = 379.37 MeV  ~ 2 E        (3.9%, not clean)
    Σ − Λ = 77.47,  Ξ − Σ = 125.13   (internal, "not clean")

The Gell-Mann–Okubo sum rule (m_N + m_Ξ)/2 = (3m_Λ + m_Σ)/4 holds to 0.57%
— the standard octet relation. But the octet does NOT sit on the E-ladder
(decuplet coefficients 4+(2S+1)/2·f are 5.65, 6.05, 6.68 vs the octet's
5.65, 6.05, 6.68 — no clean ladder match).

## 2. The discovery: Σ golden-partitions the Λ→Ξ interval

    (Σ − Λ) / (Ξ − Λ) = 0.38238   vs   1/φ² = 0.381966   →  0.108% off
    (Ξ − Σ) / (Σ − Λ) = 1.61521   vs   φ     = 1.618034   →  0.175% off

Equivalently the two internal gaps — the Λ–Σ hyperfine splitting (ud pair
spin-flip, I=0↔I=1) and the Ξ−Σ strangeness step (S=−1→−2) — stand in the
golden ratio to each other. This is a single, parameter-free constraint.

Prediction power (2 anchors → 1 predicted mass):

    Σ = Λ + (Ξ − Λ)/φ²      → 1193.070 MeV  vs obs 1193.154  (0.0070%)
    Ξ = Λ + φ²(Σ − Λ)       → 1318.504 MeV  vs obs 1318.285  (0.0166%)

## 3. Hypotheses to test (H45)

1. **H45a — the golden split.** Verify (Σ−Λ)/(Ξ−Λ) = 1/φ² and
   (Ξ−Σ)/(Σ−Λ) = φ to < 0.2%. This is the octet's structural law.
2. **H45b — parameter-free prediction.** From (Λ, Ξ) predict Σ; from
   (Λ, Σ) predict Ξ. Both must land < 0.05%.
3. **H45c — GMO as consistency anchor.** The octet obeys the standard
   Gell-Mann–Okubo sum rule to < 1% (known physics; re-verified here).
4. **H45d — robustness (G2 frame).** Apply `base_specificity` from
   `golden_relation_checks.py` to the split fraction 1/φ²: narrow basin,
   φ uniquely selected vs competitors (3/8, 0.38, 0.39, 0.4, ...).
5. **H45e — contrast with the decuplet.** The octet is NOT an E-ladder
   (confirm Phase 34); its clean content is the golden partition, while the
   decuplet is the clean E-ladder. Two different SU(3) structures, two
   different quantization laws.

## 4. Success criteria

- **Closure:** the golden partition passes — split fraction within 0.2% of
  1/φ², both predictions < 0.05%, base-specificity basin narrow with 1/φ²
  inside and uniquely best, GMO < 1%. This CLOSES the Phase 34 octet open
  item with a parameter-free structure.
- **Honest negative:** if the split fraction deviates > 0.2% or the basin is
  not φ-selective, report the octet as genuinely irreducible (Phase 34
  stands) and quantify the residual.

## 5. Deliverables

- `code/phase45_baryon_octet.py` — octet masses, golden split, predictions,
  GMO, base-specificity, CSV + figure.
- `tests/test_phase45_baryon_octet.py` — tests encoding H45a–e.
- `code/outputs/phase45/` — `baryon_octet.csv`, figure.
- Phase map + synthesis update (README.md, cross_phase_synthesis.md,
  synthesis_paper.md §8.1u, retrospective_cross_analysis.md).

## 6. Conventions (reused from prior phases)

- Octet masses = PDG 2022 (same as Phase 34/35).
- E = hbar c / 1 fm = 197.327 MeV (master-equation quantum).
- Robustness: `golden_relation_checks.base_specificity` (Phase 42 frame).

## 7. Sequencing

Phase 45 is the immediate successor to Phase 44 called out in the Phase 43/44
sequencing notes (baryon octet Λ–Σ mixing). Standing open items after this:
stable-knot → SM multiplicity mapping; the Phase 43 m_t reference-rescope.
