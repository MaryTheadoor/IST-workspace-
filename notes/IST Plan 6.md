# Plan 6: Unified Topological Mass Formula – From Planck to Proton to Black Hole

## Based on Plan 5 Results
Plan 5 validated:
- The associator correction `ΔM_assoc = K₀ · (α/φ²) · Σ(associators)` closes the mass residual.
- Topological factor for a Klein bottle horizon is `f_topo = 1.5`.
- Time crystal oscillations (periodic info density) were observed – suggesting a new term in the mass equation.
- Visualisation suite successfully demonstrated the Klein bottle horizon, inversion vortex, and radiation spectrum.

## Objective
Derive and validate a **single master equation** for the mass of any composite topological object in IST, from protons to black holes.

## Master Equation (Refined)

\[
M = \frac{\hbar c}{\ell} \cdot \frac{f(\chi,\theta)}{2\pi} \cdot I_{\text{topo}} \;+\; \frac{\hbar c}{\ell} \cdot \frac{\alpha}{\phi^2} \cdot \Xi \;+\; \frac{\hbar c}{\ell} \cdot \delta_{\text{tc}}
\]

In Planck units (\(\hbar=c=1\), \(\ell_P=1\)):

\[
M = \frac{f}{2\pi} I_{\text{topo}} + \frac{\alpha}{\phi^2} \Xi + \delta_{\text{tc}}
\]

| Symbol | Meaning | Value / Range |
|--------|---------|----------------|
| \(\ell\) | Fundamental length scale | \(\ell_P\) (BH) or \(\ell_{\text{QCD}}\) (proton) |
| \(f(\chi,\theta)\) | Topological factor | 1 (sphere), 1.5 (Klein), to be computed for others |
| \(I_{\text{topo}}\) | Total topological information | Sum of linking numbers + winding numbers |
| \(\alpha\) | Fine‑structure constant | 1/137.036 |
| \(\phi\) | Golden ratio | (1+√5)/2 ≈ 1.618 |
| \(\Xi\) | Total associator charge | Sum over all triple‑compression events |
| \(\delta_{\text{tc}}\) | Time crystal contribution | Observed periodic modulation |

## Tasks for the Agent

### Phase A: Formal Derivation from Directed Numbers
- Use `supplementary/directed_numbers_v0.8.1.pdf`.
- Derive that mass = sum of `info()` of directed numbers times energy quantum.
- Derive topological factor `f` from associator integrated over horizon/volume.
- Derive associator term `Ξ` from triple products passing through zero‑point.
- Derive `δ_tc` from temporal consistency loops (Axiom 2.18).

**Output:** `notes/master_equation_derivation.md`

### Phase B: Proton Case
- Known mass: `m_p = 938.272 MeV/c²`.
- Set `ℓ = ℓ_QCD ≈ 1 fm` (confinement scale).
- Solve for `I_topo,p` assuming associator term is negligible or known from earlier proton derivation.
- Use minimal simulation: 3 directed numbers with linking numbers 1,1,1 (trefoil braid) to compute `I_topo,p`.

**Output:** `outputs/proton_topological_info.txt`

### Phase C: Black Hole Case (from Plan 5 data)
- Load `outputs/mass_scaling.csv` and `golden_ratio_fit.png` from Plan 5.
- Extract `I_topo,BH` and `Ξ_BH` for each simulated mass.
- Verify `M = (f/2π) I_topo + (α/φ²) Ξ` with `f=1.5`.
- Extract time crystal amplitude from periodic info density oscillations (Plan 5 reported dominant frequency ~0.003/step). Fit `δ_tc = A cos(2π ν t)`.

**Outputs:** 
- `outputs/bh_master_equation_fit.png`
- `outputs/bh_tc_amplitude.txt`

### Phase D: Scale Invariance Plot
- Log‑log plot of `M` (natural units) vs `I_topo` for:
  - Proton (single point)
  - Black holes (multiple masses from Plan 5)
- Overlay master equation prediction (slope 1, intercept from associator+TC).

**Output:** `outputs/scale_invariance_unified.png`

### Phase E: Write Internal Paper
- Compile derivations, data, figures into `notes/unified_mass_paper_v1.md`.
- Sections: Abstract, Introduction, Formalism, Validation (proton & BH), Time Crystal Term, Predictions, Discussion.

### Phase F: Update README and Visualisation Gallery
- Add section “Unified Mass Formula – From Quarks to Black Holes”.
- Embed scale invariance plot and link to paper.
- Add brief explanation of time crystal discovery.

## Expected Deliverables

| File | Description |
|------|-------------|
| `notes/master_equation_derivation.md` | First‑principles derivation from directed numbers |
| `outputs/proton_topological_info.txt` | Extracted `I_topo,p` from proton mass |
| `outputs/bh_master_equation_fit.png` | Verification of BH data against master equation |
| `outputs/bh_tc_amplitude.txt` | Time crystal amplitude and frequency |
| `outputs/scale_invariance_unified.png` | Log‑log plot proving scale invariance |
| `notes/unified_mass_paper_v1.md` | Complete internal paper |
| `README.md` | Updated summary and links |
| `code/unified_mass_analysis.py` | Script for all fitting and plotting |

## Execution Notes
- Use existing Plan 5 outputs where possible; do not rerun large BH simulations.
- For proton simulation: simple 3‑knot system using directed numbers. Compute `I_topo` and scale to `m_p` to infer `ℓ_QCD`.
- Time crystal term: if exact amplitude not available from saved data, use preliminary value from Plan 5 report (~0.1% of main mass) and mark as “preliminary – needs dedicated simulation”.

## Commit Message
`"feat: unified topological mass formula (Plan 6) with golden ratio closure and time crystal term"`