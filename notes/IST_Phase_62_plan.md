# IST Phase 62 Plan — The IXPE Vacuum-Birefringence Gate (Stewart et al. 2026)

**Origin (memo item 9, urgent).** Stewart et al. 2026 (arXiv 2509.19446, Nature;
IXPE+NICER+Parkes, magnetar 1E 1547.0−5408, B ≈ 2.2×10¹⁴ G ≈ 5 B_cr) report the
strongest evidence yet for QED vacuum birefringence (VB): phase-averaged PD
65±8% at 2 keV (peaking 82±15%), a PD depression across 2–4 keV attributed to
mode conversion at the QED vacuum resonance (VR), RVM-consistent PA swings, and
radiative-transfer fits where VB-on crushes VB-off (Q/I χ²/dof 19.0/4 vs
106.8/4). The absolute Δn is **not** extracted as a clean number (the authors
say so: model-dependent, single source). This is the flagship prediction's
first empirical neighbor: vacuum birefringence and four-wave mixing are the
**same two Heisenberg–Euler coefficients** c₁, c₂ of
L_quartic = c₁(F²)² + c₂(F·F̃)², and Phase 56 predicts c₂/c₁ = 0 (QED: 7/4).

**The physics (verified against the canonical literature).** In a pure magnetic
background the two photon eigenmodes decouple cleanly by invariant:

n(E∥B) − 1 = 16·c₂·B²·sin²θ_B ;  n(E⊥B) − 1 = 16·c₁·B²·sin²θ_B

QED: c₁ = α²/90m⁴, c₂ = (7/4)c₁ → (14/45) and (8/45)(α²/m⁴)B²sin²θ — the
canonical numbers, ratio 7/4 = c₂/c₁. **Consequence: c₂ = 0 does NOT kill VB —
it makes the E∥B mode non-refractive (index exactly 1) while the E⊥B mode
keeps the c₁ shift.** Δn = n_∥ − n_⊥: QED = 12c₁B²sin²θ; IST = −16c₁B²sin²θ
(sign-flipped, magnitude 4/3× at equal c₁). The mode roles: at perpendicular
incidence E∥B is the O-mode (the surface-dominant mode in the magnetar), E⊥B
the X-mode. **The code's eigenvector check is authoritative on mode assignment.**

**The two-branch normalization question.** Phase 56 claims c₁_IST = α/φ² with
"IST/QED coupling ≈ 52.3 = 1/(αφ²)" — but that ratio sits in a dimensionless
slot against QED's c₁ = α², while the *physical* c₁ carries the 1/(90m⁴)
kinematic structure. The physical reading of α/φ² is underived. Two branches:
**(i)** c₁_IST = 52.3·c₁_QED physically → Δn_IST ≈ 70×Δn_QED, sign-flipped;
**(ii)** c₁_IST ≈ c₁_QED (only c₂ = 0) → Δn_IST = (4/3)Δn_QED, sign-flipped.

**Hypotheses (pre-registered before compute):**

- **H62a — the mode algebra (verification).** Derive the two-mode index shifts
  from L(c₁, c₂) by explicit Lorentz-tensor expansion of the quadratic
  probe terms, diagonalize the transverse photon self-energy, and verify:
  (i) the eigenmodes are E∥B and E⊥B with shifts ∝ c₂ and ∝ c₁ respectively
  (decoupling exact at all θ); (ii) QED (c₂ = 7/4 c₁) reproduces the canonical
  (14/45, 8/45)(α²/m⁴)B²sin²θ; (iii) c₂ = 0 ⟹ n(E∥B) = 1 exactly.
- **H62b — the magnetar observable.** For 1E 1547.0−5408 parameters
  (B_surf ≈ 2.2×10¹⁴ G, B/B_cr ≈ 5, R* = 12 km, E = 2–4 keV, dipole field):
  (i) the accumulated VB phase along the radial path and the mode-decoupling
  radius (where the phase drops to ~1) — QED must land in the paper's stated
  30–300 R* range (a validation of the whole chain); (ii) the vacuum-resonance
  (VR) energy, E_VR ∝ 1/√(vacuum coefficient) (Lai–Ho scaling), anchored at
  the observed 2–4 keV dip; (iii) both for QED and for IST branches (i) and
  (ii). **Pre-registered expectations:** branch (ii) — decoupling radius ≈
  4/3^(1/5)×QED ≈ 167 R* (indistinguishable), VR unchanged → CONSISTENT;
  branch (i) — VR moves to ~0.3–0.6 keV (√52.3× down) and the dip the paper
  sees at 2–4 keV would be unexplained → TENSION; additionally, c₂ = 0 removes
  the E∥B mode's vacuum resonance entirely (its index is exactly 1 — no
  plasma-vacuum crossing for that mode).
- **H62c — the structural discriminator survives.** The c₂ = 0 prediction is
  normalization-independent: n(E∥B) ≡ 1 at all angles, no E∥B-mode vacuum
  resonance, no E∥B-mode locking — a sharp, mode-resolved falsifiable signature
  that no current dataset tests. The paper's own caveat (magnitude not
  extracted; single source) means c₂ = 0 is **not falsified** by this paper.
- **H62d — the registration gate.** Verdict per branch, with the repo's honest
  discipline: (1) c₂/c₁ = 0 can be publicly registered in the structural
  (mode-resolved) form; (2) the 52.3× 4WM enhancement claim (Phase 56 H56b) is
  **gated off** pending a physical c₁ normalization derivation, because the
  IXPE 2–4 keV dip location constrains c₁ to near-QED strength (within an O(1)
  factor); (3) the registry records the constraint, the branch table, and the
  derivation gap — same discipline as the 4σ-DE retraction. Expected outcome
  spectrum includes the honest negative: if the data's dip location and the
  standard VR scaling rule out even branch (ii)'s 4/3 magnitude (they will not
  at current sensitivity, but the phase states the condition), c₂ = 0 would
  acquire its first quantitative tension.

**Honest framing.** This is the flagship prediction put through the same
discipline as the cosmology audits: reproducible code, pre-registered
expectations, the paper's own caveats stated, and the empirical neighbor
treated as a live constraint. The phase adapts the model to the evidence:
where the α/φ² magnitude fails (branch i), the failure localizes exactly the
derivation that must be supplied — the physical c₁ normalization — and the
structural c₂ = 0 core stands on its own.

**Deliverables:** `code/phase62_ixpe_vb_gate.py`,
`tests/test_phase62_ixpe_vb_gate.py`, outputs under `code/outputs/phase62/`,
`notes/IST_Phase_62_plan.md` (this file). Registry appended (73 → ~77 rows).

**Phase-map sync (all three + retrospective):** README.md (highlights after
Phase 61), `main/cross_phase_synthesis.md` (row 62),
`main/synthesis_paper.md` (§8.1ak + observable prediction #20, footer v2.11),
`notes/retrospective_cross_analysis.md` (Phase 62 entry).
