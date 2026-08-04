# IST Phase 56 — The 4-Wave-Mixing Discriminator: Dual-Mode Photon Vacuum vs QED

**Status:** COMPLETE (gap 7 of the external analysis: a table-top falsifiability
target). The dual-mode photon of Phase 55 predicts a quantitative 4WM signature
that separates it from the QED Heisenberg-Euler vacuum.
**Predecessor:** `code/phase55_photon_compound.py` (dual-mode photon, achirality
0.000, v_g = 1.0); `code/associator_from_PBH.py` (golden charge scale
φ²/α ≈ 358.8); `notes/quantum_vacuum_and_plasma_analogues_in_IST.md` (Zhang et
al. 2025 pending experiment). **Postcondition:** IST now makes a specific,
discriminating, lab-testable prediction about photon self-interaction — closing
the framework's least-contact observation channel.

---

## 1. The Open Question (gap 7)

The external analysis promoted the 4WM experiment: *"Zhang et al. is the one
place IST could make contact with a laboratory system rather than astrophysical
data with large systematics. If IST predicts a specific signature in 4WM that
standard QED vacuum physics doesn't, that's tabletop falsifiability."* The
condition is "a specific signature QED doesn't have" — Phase 55 supplies it, in
the vacuum's parity structure.

## 2. The Physics

QED's vacuum is described by the Heisenberg–Euler effective Lagrangian, whose
quartic part is **two** invariants,
L_quartic = c₁(F²)² + c₂(F·F̃)², with the canonical one-loop ratio
**c₂/c₁ = 7/4**. The second term, (F·F̃)² = (E·B)², is a **pseudo-scalar**:
it is nonzero only in a vacuum not invariant under parity (its coefficient
drives vacuum birefringence and polarization rotation in 4WM).

Phase 55's photon is a dual-mode wave function whose two helicity strands cross
the zero point (seam) symmetrically, giving **parity-inversion EXACTLY 0.000**
(H55b) — i.e. the IST vacuum IS parity-invariant. A parity-invariant vacuum
cannot source the parity-odd (F·F̃)² invariant at leading order:
**c₂_IST = 0**.

## 3. Tracks and Results

| track | claim | measurement | verdict |
|---|---|---|---|
| H56a | achiral selection rule | QED c₂/c₁ = **1.7500** (parity-odd OPEN); IST c₂/c₁ = **0.0000** (parity-odd FORBIDDEN) | PASS — the table-top discriminator |
| H56b | golden-weighted parity-even magnitude | IST/QED coupling = **(α/φ²)/(α²) = 1/(αφ²) ≈ 52.3**; 4WM signal ≈ **(52.3)² ≈ 2.7×10³**; charge scale φ²/α ≈ 358.8 | PASS |
| H56c | output peak at universal c | v_g = **1.000000** for ω₀ ∈ {0.1…0.8}; Zhang et al. observe ~0.99c | PASS (consistent) |
| H56d | consistency | predictions agree with Phase 55 achirality (0.000) and massless-E=hν; added to Phase-54 registry | PASS |

## 4. Success criteria / verdict

- [x] H56a — the parity-odd 4WM channel is FORBIDDEN for the achiral dual-mode photon (0.000) but OPEN for QED (7/4): a single polarization-rotation / ellipticity measurement separates the models.
- [x] H56b — the surviving parity-even IST coupling is golden-weighted, α/φ² (charge scale φ²/α ≈ 358.8), giving a ~52× coupling / ~2.7×10³ signal enhancement vs QED in the allowed channel.
- [x] H56c — the 4WM output peak propagates at universal c (1.000000), consistent with Zhang et al.'s ~0.99c observation.
- [x] H56d — Phase-56 relations added to the Phase-54 living registry.

## 5. Relation to the framework and gap list

- Gap 7 now has a concrete, quantitative prediction: the dual-mode vacuum's
  parity-odd 4WM channel is exactly zero (vs QED's 7/4). This is the sharpest
  possible falsification/corroboration contact IST has with a table-top system.
- Consistency: H56a mirrors Phase 55 H55b (photon achirality 0.000 vs electron
  0.446); H56c mirrors H55a (universal c). The 4WM predictions are not new free
  numbers — they are the Phase-55 dual-mode geometry pushed into the vacuum.
- Registry (Phase 54): appended the Phase-56 4WM relations.

## 6. Deliverables

- `code/phase56_four_wave_mixing.py` (+ `code/outputs/phase56/{parity_odd_ratio,golden_magnitude,group_velocity,heisenberg_euler_invariants}.csv`, `photon_4wm_discriminator.png`)
- `tests/test_phase56_four_wave_mixing.py` (7 tests)
- Phase map + synthesis update (README, cross_phase, synthesis_paper, retrospective); Phase-54 registry appended.