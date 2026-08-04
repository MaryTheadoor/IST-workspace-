# IST Phase 53 — Heavy-Flavor Octet: Does the Golden Partition Extend?

**Status:** COMPLETE (honest negative: the Phase 45 golden partition is LIGHT-OCTET
SPECIFIC — the charmed and bottom SU(3) analog triplets fail by 139% and 190%
respectively, and the bottom hierarchy inverts, so the partition is a law of the
emergent light near-degenerate octet, not of the general (Lambda, Sigma, Xi) triplet)
**Predecessor:** Phase 45 (`code/phase45_baryon_octet.py`) discovered the light octet's
golden partition; Phase 50 (`code/phase50_light_quark_partition.py`) showed the bare
quarks do NOT carry it (RG-invariant negative). Phase 53 tests the sibling domain: the
heavy-flavor analog baryons.
**Postcondition:** A definitive answer to whether the golden partition generalizes to
the charmed/bottom analogs of (Lambda, Sigma, Xi), closing gap 6 of the external
analysis.

---

## 1. The Open Question

The external gap analysis (`C:\Users\AmosA\Desktop\IST analysis.txt`, gap 6) flagged a
genuine untested predictive domain: the golden partition

    (Sigma - Lambda) / (Xi - Lambda) = 1/phi^2      (Phase 45, 0.108% off)

has only been tested on the LIGHT octet. PDG gives precise masses for the heavy-flavor
analog triplets {Lambda_Q, Sigma_Q, Xi_Q} (Q = c, b), so the law can be pre-registered
as a prediction:

    IF the partition is a universal SU(3)-flavor law of (Lambda, Sigma, Xi) triplets,
    THEN the analog baryons must satisfy, within ~0.2%:

        (Sigma_Q - Lambda_Q) / (Xi_Q - Lambda_Q)  =  1/phi^2 ~ 0.381966
        (Xi_Q    - Sigma_Q)  / (Sigma_Q - Lambda_Q) =  phi     ~ 1.618034

## 2. Masses used (PDG 2024, J^P = 1/2^+ ground states)

| flavor | Lambda (MeV) | Sigma (MeV) | Xi (MeV) |
|--------|--------------|-------------|----------|
| light  | 1115.683     | 1193.15     | 1318.28  |
| charm  | 2286.46      | 2453.54 (Σ_c 2455 isospin avg) | 2469.08 (Ξ_c 2470 avg) |
| bottom | 5619.60      | 5813.10 (Σ_b ±) | 5794.45 (Ξ_b 0/−) |

Uncertainties: charm ±(0.14–0.4), bottom ±(0.17–0.6) MeV.

## 3. Hypotheses tested (H53)

- **H53a — Charm.** (Σ_c−Λ_c)/(Ξ_c−Λ_c) = 0.9149 vs 1/φ² (139.5% off, 205σ);
  (Ξ_c−Σ_c)/(Σ_c−Λ_c) = 0.0930 vs φ (94.3% off, 491σ). FAILS.
- **H53b — Bottom.** (Σ_b−Λ_b)/(Ξ_b−Λ_b) = 1.1067 vs 1/φ² (189.7% off, 177σ);
  (Ξ_b−Σ_b)/(Σ_b−Λ_b) = −0.0964 vs φ (106.0% off, 512σ). FAILS, and the
  SU(3) hierarchy INVERTS: Λ_b (5619.6) < Ξ_b (5794.4) < Σ_b (5813.1).
- **H53c — Ordering check.** The charm failure is not an ordering artifact
  (Λ_c < Σ_c < Ξ_c still holds); the bottom inversion is structural (HQET:
  the Σ_b−Λ_b hyperfine splitting ~193 MeV now exceeds the Ξ_b−Λ_b step
  ~175 MeV, so Σ sits above Ξ).

## 4. Success criteria / verdict

- [x] Quantified honest negative on both flavors, with error propagation
      (failures are 177–512σ — not uncertainty artifacts).
- [x] Light-octet anchor still obeys inside the same module (0.11% off).
- [x] Interpretation: the golden partition is a law of the EMERGENT, NEAR-DEGENERATE
      light octet (diquark hyperfine vs strangeness step balanced at 1/φ). A hard
      heavy-quark mass (c/b — set at the Higgs/Yukawa scale, NOT emergent) injects
      an off-scale splitting that erases the balance — the same dividing line
      Phase 50's RG-invariance argument predicted for any non-light sector.

## 5. Deliverables

- `code/phase53_heavy_flavor_octet.py`
- `tests/test_phase53_heavy_flavor_octet.py` (10 tests)
- `code/outputs/phase53/heavy_flavor_octet.csv` (+ .png)
- Phase map + synthesis update (README, cross_phase, synthesis_paper, retrospective).

## 6. Sequencing

Phase 53 closes gap 6 of the external analysis and NARROWS where φ lives: the golden
partition is specific to the light near-degenerate emergent octet — neither the bare
quarks (Phase 50) nor the heavy-flavor baryons (Phase 53) carry it. Remaining
candidate next step: gap 1 (statistical look-elsewhere registry).
