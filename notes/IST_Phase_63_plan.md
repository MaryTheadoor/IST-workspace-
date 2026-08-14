# IST Phase 63 Plan — The c₁ Normalization Resolution (the IXPE Gate's Required Derivation)

**Origin.** Phase 62's gate verdict produced a required derivation: the
physical normalization of the golden parity-even coupling c₁ = α/φ² (Phase 56).
The observed 2–4 keV vacuum-resonance dip in 1E 1547.0−5408 pins the physical
vacuum-polarization coefficient to near-QED strength, while Phase 56's
"52.3× QED" reading (the same dimensionless slot as QED's α²) is excluded.
The template is the Phase 49 result (this session's memo): **physical
normalizations in the framework are fixed by the phase space that is actually
paid, and the data select the counting** — Vol_topo(SU(3)) = 2π⁵ (6π⁵ matches
at 10⁻⁵) over Vol_Haar = √3π⁵ (13.4% off).

**The physics.** QED's one-loop coefficient is c₁_QED = α²/(90 m_e⁴) — a
phase-space statement (the electron loop's proper-time integral, with the
same 1/90 kinematic structure verified in Phase 62 H62a). The framework's
claim c₁ = α/φ² is a dimensionless golden coupling that must acquire its
physical 1/M⁴ scale from the loop mass the substrate actually pays:

c₁_IST,phys = (α/φ²)/(90 M_assoc⁴)  ⟹  R ≡ c₁_IST/c₁_QED = 52.33·(m_e/M_assoc)⁴

The IXPE VR-dip anchor (E_VR = 3 keV midpoint, observed band 2–4 keV;
E_VR ∝ 1/√c₁) implies R ∈ [(3/4)², (3/2)²] = [0.5625, 2.25], i.e.
M_assoc/m_e ∈ [2.19, 3.11] ⟺ M_assoc ∈ [1.12, 1.59] MeV.

**Pre-registered candidate reading (before compute).** The framework's
electron mass formula pays the associator suppression φ²: M_P/m_e =
(12π⁵/φ²)α⁻⁹ — the same golden factor that scales the parity-even coupling.
The natural reading: **the vacuum-polarization loop pays the same associator
suppression, so M_assoc = φ²m_e = 1.338 MeV.** Predicted consequences:
R = 52.33/φ⁸ = **1.114** (c₁ = 1.114×QED), E_VR = 3/√1.114 = **2.84 keV**
(inside the observed band), |Δn| = (4/3)×1.114 = **1.485×QED**, decoupling
radius ≈ **147 R\***. The nearest independent physical anchor: the
neutron–proton mass difference m_n − m_p = 1.293 MeV, inside the implied band.

**Hypotheses (pre-registered before compute):**

- **H63a — the normalization map.** R(M) = 52.33·(m_e/M)⁴ from
  c₁ = α/φ² (Phase 56) and c₁_QED = α²/90m_e⁴ (Phase 62-verified). The
  52.3× reading (M = m_e) is the excluded branch (i) of the gate.
- **H63b — the IXPE-implied band.** E_VR = 3 keV/√R with the observed
  2–4 keV band implies R ∈ [0.5625, 2.25] and M_assoc ∈ [1.12, 1.59] MeV.
  Report the band and the inversion.
- **H63c — the candidate-scale table.** m_e (R = 52.3, E_VR = 0.41 keV —
  excluded); 2m_e (R = 3.27, 1.66 keV — borderline/out); **φ²m_e (R = 1.114,
  2.84 keV — in band)**; m_n−m_p = 1.293 MeV (R = 1.09, 2.87 keV — in band);
  √(m_e m_μ) = 7.35 MeV (R = 1.1×10⁻³, ~90 keV — out); m_π (out).
- **H63d — the framework rationale and the resulting prediction.** The
  associator suppression φ² that the electron mass formula pays (M_P/m_e =
  (12π⁵/φ²)α⁻⁹) is the same golden factor the vacuum loop pays, giving
  M_assoc = φ²m_e. The phase's deliverable prediction: **c₁_IST = 1.114×QED,
  E_VR = 2.84 keV for the magnetar dip, |Δn| = 1.485×QED (sign-flipped),
  decoupling ≈ 147 R\*** — all inside the IXPE anchors, and falsifiable the
  moment |Δn| is extracted or the dip centroid is measured.
- **H63e — the honest status.** The normalization is *empirically anchored*
  (the IXPE band + the φ² rationale), not yet first-principles: why the loop
  pays exactly φ² remains an open derivation (the associator-amplitude item
  already in the registry). The phase records: the 52.3× 4WM enhancement
  (Phase 56 H56b) stays gated; the surviving 4WM magnitude claim becomes
  1.114×QED in the parity-even channel; c₂/c₁ = 0 registration proceeds in
  the structural form. Registry 77 → ~81 rows.

**Honest framing.** This is the "adapt the model to the evidence" step: the
IXPE data do not merely constrain — they select a normalization, and the
selected one (φ²m_e) is exactly the golden factor the framework already pays
elsewhere. The phase states both the success (a new falsifiable number) and
the gap (the why-φ² derivation remains open).

**Deliverables:** `code/phase63_c1_normalization.py`,
`tests/test_phase63_c1_normalization.py`, outputs under `code/outputs/phase63/`,
`notes/IST_Phase_63_plan.md` (this file), `notes/phase49_internal_memo.md`
(companion, written this session).

**Phase-map sync (all three + retrospective):** README.md, row 63 in
`main/cross_phase_synthesis.md`, §8.1al + prediction #21 + footer v2.12 in
`main/synthesis_paper.md`, `notes/retrospective_cross_analysis.md`, registry
append.
