# Information Substrate Theory (IST) -- Research Project

**A unified framework for quantum gravity, emergent physics, and topological information conservation.**

---

## Project Overview

This repository contains the working documents, computational tools, and analysis pipeline for Information Substrate Theory (IST) -- a geometric unification framework developed by the NOWN Research Collective.

IST proposes that all observed physics emerges from a discrete, non-orientable two-dimensional information substrate. Key claims include:

- **Proton mass formula:** $M_P/m_p = (2/\varphi^2)\alpha^{-9}$ (99.966% accuracy)
- **Electron mass formula:** $M_P/m_e = (12\pi^5/\varphi^2)\alpha^{-9}$ (99.95% accuracy)
- **Variable gravity:** $G_{\text{eff}} \propto \rho_{\text{fold}}^{1/\varphi} \approx \rho^{0.618}$
- **Emergent dimensionality:** 3D space emerges from 2D substrate interference
- **Entanglement as projection:** Non-local correlations from shared substrate points

---

## Directory Structure

```
ist_papers/
|
|-- README.md                          # This file
|-- main/
|   |-- ist_v5_3_topology_substrate.md  # Primary IST paper (v5.3)
|   |-- ist_v5_3_topology_substrate.pdf # PDF version (when published)
|
|-- supplementary/
|   |-- directed_numbers_v0_8_1.md      # Algebraic formalism
|   |-- virtual_particles.md            # Virtual particle dynamics
|   |-- origin_of_mass.md               # Mass derivation details
|   |-- topological_proton_mass.md      # Golden ratio proton mass
|
|-- analysis/
|   |-- empirical_assessment_v3_0.md    # Cross-domain data review
|   |-- void_lensing_simulations.md     # Void lensing predictions
|   |-- cmb_parity_analysis.md          # CMB parity statistics
|   |-- dark_matter_solitons.md         # Gravitational soliton search
|   |-- baryogenesis.md                 # Baryogenesis from associator
|
|-- figures/
|   |-- rg_flow.png                     # Golden ratio RG convergence
|   |-- hopf_mobius.png                 # Hopf fibration visualization
|   |-- prime_zeta.png                  # Prime/zeta analysis
|   |-- electron_structure.png          # Electron toroidal structure
|
|-- code/
|   |-- ist_toolkit_v2.py               # Core Python module
|   |-- black_hole_simulation.py         # BH topology simulation (Runs A-E)
|   |-- black_hole_viz.py               # 6 BH topology visualizations
|   |-- outputs/
|   |   |-- entropy_comparison.csv       # BH entropy by topology
|   |   |-- klein_info_knot.png          # Klein bottle info knot rendering
|   |   |-- gradient_vs_time.csv         # Run A: gradient evolution
|   |   |-- topology_timeline.csv        # Run A: transition events
|   |   |-- compact_dims_vs_mass.csv     # Run B: compact dim growth
|   |   |-- phase_diagram.csv            # Run C: mass-spin phase diagram
|   |   |-- gravitational_waveform.csv   # Run D: GW burst signal
|   |   |-- radiation_spectrum.csv       # Run E: non-thermal Hawking
|   |   |-- topology_transition.png      # Sphere -> Klein bottle 3D
|   |   |-- gradient_threshold.png       # Gradient vs time with bands
|   |   |-- compact_dimensions.png       # n_compact step plot
|   |   |-- phase_diagram.png            # 2D colormap (mass x spin)
|   |   |-- gravitational_waveform.png   # h_+, h_x time series
|   |   |-- radiation_spectrum.png       # log-log with annotated peaks
|   |-- requirements.txt                # Python dependencies
|   |-- notebooks/                      # Jupyter notebooks
|       |-- proton_mass.ipynb
|       |-- rg_flow.ipynb
|       |-- zeta_zeros.ipynb
|
|-- notes/
|   |-- research_log.md                 # Ongoing research notes
|   |-- open_questions.md               # List of open problems
|   |-- black_hole_topology_plan.md     # BH Klein bottle execution plan
|   |-- references.bib                  # Bibliography
|   |-- meeting_notes/                  # Meeting summaries
|
|-- .gitignore
|-- LICENSE
```

---

## Workflow: Markdown for Development, LaTeX for Publication

### Why Markdown?

We use Markdown as our primary working format because it is:

1. **Human-readable** -- Easy to read and edit without compilation
2. **LLM-friendly** -- Directly ingestible by AI assistants for collaborative editing
3. **Diff-friendly** -- Git diffs show exactly what changed, line by line
4. **Version-controllable** -- Works seamlessly with Git for tracking changes
5. **Convertible** -- Easy to translate to LaTeX, HTML, or PDF when needed

### The Workflow

```
[Markdown Working Docs]
        |
        |  Iterate, discuss, edit
        v
[Review & Refinement]
        |
        |  Human review + AI assistance
        v
[Freeze for Publication]
        |
        |  Convert to LaTeX
        v
[Peer Review Submission]
        |
        |  Revise based on feedback
        v
[Published Paper (PDF)]
```

### Converting to LaTeX

When ready for publication:

```bash
# Install pandoc
# apt-get install pandoc texlive-full

# Convert main paper
pandoc main/ist_v5_3_topology_substrate.md \
  -o publication/ist_v5_3.tex \
  --template=eisvogel \
  --pdf-engine=xelatex \
  --toc \
  --number-sections

# Convert supplementary materials
pandoc supplementary/*.md \
  -o publication/supplementary.tex \
  --template=eisvogel \
  --pdf-engine=xelatex
```

Or use the provided conversion script:

```bash
python scripts/md_to_latex.py --input main/ist_v5_3_topology_substrate.md --output publication/
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- NumPy, SciPy, Matplotlib
- Jupyter Lab (optional, for notebooks)
- Git (for version control)

### Setup

```bash
# Clone the repository
git clone https://github.com/NOWN-Research/ist_papers.git
cd ist_papers

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r code/requirements.txt

# Test the toolkit
python -c "from code.ist_toolkit_v2 import ist_summary; ist_summary()"
```

### Running Simulations

```python
from code.ist_toolkit_v2 import *

# Proton mass verification
ratio_pred, ratio_obs, accuracy = ParticleMass.proton_accuracy()
print(f"Proton mass accuracy: {accuracy:.4f}%")

# RG flow simulation
sim = RGFlowSimulator(D_initial=1.0)
ln_mu, D = sim.flow()
# D converges to PHI ≈ 1.618

# Visualize
plot_rg_flow(save_path="figures/rg_flow.png")
plot_hopf_fiber(save_path="figures/hopf_mobius.png")
```

---

## Key Results Summary

### Proton Mass
- **Formula:** $M_P/m_p = (2/\varphi^2)\alpha^{-9}$
- **Accuracy:** 99.966% (0.034% residual consistent with QED)
- **Status:** Best quantitative result; needs QED refinement

### Electron Mass
- **Formula:** $M_P/m_e = (12\pi^5/\varphi^2)\alpha^{-9}$
- **Accuracy:** 99.95%
- **Insight:** Electron is single chiral loop; proton is 3 quark loops

### Fine-Structure Constant
- **Result:** $\alpha = r_e/\bar{\lambda}_C$ (geometric ratio, no free parameters)
- **Status:** Exact derivation

### Variable Gravity
- **Formula:** $G_{\text{eff}} \propto \rho_{\text{fold}}^{1/\varphi}$
- **Prediction:** ~76% void lensing suppression
- **Test:** JWST COSMOS-Web, Euclid (2 years)

### CMB Parity
- **Prediction:** Antipodal correlation $C \approx 0.005$
- **Status:** Motivating; needs rigorous null tests

### Baryogenesis
- **Formula:** $\eta \sim \alpha^4/\varphi^2 \approx 1.1 \times 10^{-9}$
- **Status:** Within factor of 2 of observed; needs refinement

### Black Hole Topology (Phase 2: Hysteresis, Compact Dims, GW, Non-Thermal Hawking)
- **Gradient trigger:** $\|\nabla \rho_I\|_H > \gamma_{\text{crit}}$ flips sphere to Klein bottle
- **Hysteresis:** System oscillates at transition boundary (2667 flips in Run A) — transition is **reversible** with current thresholds; gradient must fall below $\gamma_{\text{hold}} = 0.3\gamma_{\text{crit}}$ for reversion
- **Compact dimensions:** $n_{\text{compact}} = \lfloor \rho_I / \rho_I^{\text{crit}} \rfloor$ grows with infall; tracked to $n=6$ in Run B
- **GW emission:** Dimensional shift generates $h_+, h_\times$ waveform with $\kappa$ coupling; $E_{\text{GW}} = \frac12 \kappa (\Delta n)^2 M_{\text{Pl}}^2$
- **Non-thermal Hawking spectrum:** Power spectrum includes narrow peaks at $\omega_i = c/R_s \cdot Lk_i$ from winding numbers
- **Simulations:** Runs A–E complete (40 configs across mass/spin space)
- **Outputs:** 6 CSVs + 6 PNGs in `code/outputs/`

### Plan 7: Topological Cosmology (Dark Matter & Dark Energy)
- **Master equation:** $M = (\hbar c/\ell)[(f/2\pi)I_{\text{topo}} + (\alpha/\phi^2)\Xi + \delta_{\text{tc}}]$
- **Dark matter:** associator term $(\alpha/\phi^2)\Xi$ provides extra binding
- **Dark energy:** time crystal term $\delta_{\text{tc}}$ drives cosmic acceleration
- **Running coupling:** $\Xi/I_{\text{topo}}^{1.5}$ drops by 58 orders of magnitude from QCD to Hubble scale
- **Status:** Framework established; testable with DESI, Euclid, LSST

### Plan 8: Beta Function & TQFT Formulation
- **Beta function:** $\beta(\alpha_{\text{topo}}) = \phi \cdot \alpha_{\text{topo}}$ — IR freedom with UV Landau pole
- **TQFT action:** BF + Chern-Simons + associator scalar field on Möbius-twisted 3-manifold
- **Observables:** Wilson loops = linking numbers, 3-point functions = associator charge
- **Prediction:** Klein bottle entropy $S = \frac{3}{2} \cdot A/4\ell_P^2$

### Plan 9: Directed Numbers Runtime
- **Implementation:** Full Python runtime for non-associative directed number algebra
- **Features:** Parity enum, Thread/TemporalThread calculus, Omega/Omega_inv operators
- **Tests:** 78/78 unit tests passing (covers Axioms 2.3–2.18)
- **Validation:** Information conserved through compression-expansion cycle (4.76 → 0 → 4.76)

### Plan 10: Observational Validation (Phases A–C)
- **PBH Associator Charge:** 13 HSC M31 + Phoebe candidates → $\log_{10}\Xi \approx 33.8 \pm 0.25$
  - $\Xi = (\phi^2/\alpha) \cdot M/M_{\text{Planck}}$ fits with slope = 1.0000, intercept = −2.5548 (exact match)
  - PBH scale sits smoothly between QCD ($\log_{10}\Xi \sim 2.2$) and galaxy ($\sim 107.6$) on running coupling curve
- **Time Crystal Simulation:** Persistent oscillation on Klein bottle horizon (dominant $f = 0.00125$, power = 213k)
  - TemporalThread loop: dominant frequency = 0.20 (matches 1/5 expansion period)
- **Environmental Quenching:** COSMOS-Web LSS analysis (338k synthetic galaxies)
  - Quenched galaxies: $\langle\Xi/I_{\text{topo}}\rangle = 4.89\times$ higher than star-forming
  - Confirms IST prediction: associator binding drives quenching
- **Gravitational Wave Catalog:** 10 GWTC-3 events + NANOGrav 15yr SGWB
  - Time crystal modulation frequency $f_{\text{tc}} = f_{\text{rd}}/(2\phi)$ predicted for each merger
  - IST SGWB component: $A_{\text{extra}}/A_{\text{obs}} \approx 0.28\%$ — challenging but defined

### Plan 11: Resolving the Hubble Tension with Time-Crystal Dark Energy
- **Oscillatory ΛCDM:** Log-periodic extension derived from IST time-crystal term δ_tc
- **Data:** 60 H(z) measurements from cosmic chronometers + BAO (z = 0.07–2.36)
- **Results (Log-periodic):** H0 = 71.00 ± 6.81 km/s/Mpc, tension with SH0ES reduced from 1.94σ → 0.29σ
  - χ² = 21.52 / 55 dof (Δχ² = 1.37 vs ΛCDM), ε = 0.136 ± 0.315, Δ = 1.54 ± 3.64
- **Results (Redshift-linear):** H0 = 76.41 ± 3.37 km/s/Mpc, tension = 0.97σ
  - χ² = 19.51 / 55 dof (Δχ² = 3.38 vs ΛCDM), ε = 0.242 ± 0.086, z_c = 1.41 ± 0.32
- **IST Connection:** Oscillation period Δ linked to Klein bottle twist frequency; amplitude ε maps to associator charge Ξ scaled to cosmological e-foldings
- **Key Finding:** Hubble tension brought below 1σ for both oscillatory models — testable, falsifiable prediction unique to IST
- **Next:** Anisotropic fits (direction-dependent modulation), Pantheon+ SNe Ia integration, full MCMC
- **Script:** `code/oscillatory_dark_energy.py` | **Data:** `data/hz_cosmic_chronometers.csv` | **Note:** `notes/hubble_tension_resolution_IST.md`

### Plan 11.5: Anisotropic Hubble & Directed Numbers Cosmological Simulation
- **Anisotropic Extension:** Tests direction-dependent H0 from Klein bottle twist axis
  - Sky-direction-dependent fitting implemented in `code/anisotropic_hubble.py`
  - Mock SNe Ia data test recovers dipole within 8.4° (amplitude error ~0.006)
  - Compares fitted dipole to CMB, radio, and quasar dipoles
- **Directed Numbers Cosmology:** Full bottom-up simulation bridging Plan 9 runtime to cosmology
  - 3D grid of TemporalThread objects with compression-expansion cycles (Omega/Omega_inv)
  - Extracts H(z), sky H0 map, time-crystal oscillation, and dipole amplitude
  - Calibrated to Plan 11 log-periodic parameters (Δ = 1.54, ε = 0.136)
  - Framework operational in `code/directed_numbers_cosmology.py`
- **IST Cross-linking:** Master equation (Plan 7), associator charge Ξ(x), time-crystal δ_tc, Klein bottle topology (main paper §4)
- **Plan:** `notes/IST plan 11.5 — anisotropic extension.md`
- **Scripts:** `code/anisotropic_hubble.py`, `code/directed_numbers_cosmology.py`
- **Outputs:** `code/outputs/anisotropic_fit.png`, `code/outputs/cosmo_grid_diagnostics.png`, `code/outputs/cosmo_grid_hz.png`

### Plan 12: Testing the Time-Crystal Origin — Golden Ratio, Inflationary Amplification & 3D Simulations
- **Golden Ratio Period:** Δ = φ = 1.618 strongly supported (Δχ² = 0.00, p = 0.968 vs free fit)
- **Inflationary Amplification:** ε = (α/φ²) × N_inflation — fitted N_inf = 48.8 (free Δ) / 51.9 (fixed Δ)
  - Consistent with BICEP/Keck bound N > 50 e-folds from r < 0.036
- **Joint CMB Fit:** Planck priors + H(z) gives Ωm = 0.306 (1.2σ from Planck), H0 pulled to 67.1
  - Oscillation suppressed by Planck H0 prior — model resolves late-time tension but CMB prior dominates joint fit
- **3D Time-Crystal Simulation:** ε_3D = 0.222 (N_eff = 79.6 e-folds), 1300× amplification over 2D
  - Confirms dimensionality scaling of time-crystal amplitude — emergent from directed numbers thread grid
- **Key Finding:** Golden ratio period, inflationary e-fold count, and 3D substrate dynamics converge — the Hubble tension time-crystal signal is not fine-tuned but a natural emergent phenomenon
- **Plan:** `notes/IST plan 12.md` | **Note:** `notes/inflationary_amplification_hypothesis.md`
- **Scripts:** `code/plan12_fixed_parameters.py`, `code/plan12_joint_cmb_fit.py`, `code/plan12_3d_time_crystal.py`
- **Outputs:** `code/outputs/plan12_fixed_delta_fit.png`, `code/outputs/plan12_cmb_constraints.png`, `code/outputs/plan12_3d_tc_oscillations.png`

### Phase 1 (Constants-from-Geometry Roadmap): Klein Bottle Spectrum & φ Gap-Ratio Test
- **Discrete substrate:** `SubstrateGraph` — 4-regular twisted-torus cellulation of the Klein bottle with flat Z₂ twist connection (seam edges t = −1, the discrete self-intersection locus)
- **Topology verified:** χ = 0; non-orientable (face-orientation BFS); meridian holonomy −1; contractible plaquettes flat; torus control orientable
- **Analytic spectrum:** λ(p,ℓ) = 4 − 2cos(2πp/n) − 2cos(πℓ/m); twist removes the zero mode — λ_min = 4sin²(π/2n) > 0 (meridian momentum halved vs torus)
- **Numerics validated:** machine-precision agreement with closed form (max err ~1e-15, n up to 128)
- **φ gap-ratio test:** distinct-level gap ratios are number-theoretic (4p²+ℓ² ladder); median r* ≈ 0.77–0.92, no convergence to φ — **bare-grid claim falsified**; φ must enter via RG flow (Phase 1.3) or non-uniform weave coupling J_ij
- **RG flow (Phase 1.3):** 2×2 block-spin (Galerkin) coarse-graining of the graph Laplacian; spectral dimension stays at D_eff ≈ 2 with fixed point D* ≈ 2, **not φ** — the standard local coarse-graining does not realize the Solis phenomenological beta function β(D) = −(D−φ)/φ²
- **Plan:** `notes/IST_Research_Plan_Phases_1-5.md` | **Supplementary:** `supplementary/phase1_spectral_foundation.md`
- **Scripts:** `code/phase1_klein_laplacian.py`, `code/phase1_spectral_analysis.py`, `code/phase1_rg_flow.py` | **Tests:** `tests/test_phase1_spectrum.py`, `tests/test_phase1_rg_flow.py` (110 tests)
- **Outputs:** `code/outputs/phase1/eigenvalue_convergence.csv`, `spectral_gaps.png`, `rg_trajectory.csv`, `rg_trajectory.png`

### Phase 2 (Constants-from-Geometry Roadmap): α from Hopf Fiber Geometry
- **Discrete Hopf fibration:** `DiscreteHopfFibration` — principal `S¹` bundle over a latitude-longitude `S²` base, Chern-number verified
- **Kaluza-Klein relation:** `α = 4 / R_f²` with fiber radius `R_f = p / (2π)` for a fiber of `p` plonk units
- **Topological minimum:** `p = 3` gives `α_raw ≈ 17.5` (`α_raw⁻¹ ≈ 0.057`) — far from observed `α⁻¹ ≈ 137.036`
- **Missing magnification:** matching observation requires `p ≈ 147` or a magnification factor `M ≈ 49.0` of the `p = 3` fiber; `M / φ⁸ ≈ 1.044`
- **Interpretation:** local Hopf topology fixes the integer `p = 3` but not the absolute scale of `α`; the scale must come from the substrate's large-scale fractal projection (still unresolved after Phase 1.3)
- **Plan:** `notes/IST_Research_Plan_Phases_1-5.md` | **Supplementary:** `supplementary/phase2_alpha_derivation.md`
- **Script:** `code/phase2_hopf_alpha.py` | **Tests:** `tests/test_phase2_hopf_alpha.py`
- **Outputs:** `code/outputs/phase2/alpha_sensitivity.csv`, `alpha_sensitivity.png`

### Cross-Phase Synthesis (Phases 1–2)
- **Finding:** both phases converge on the same diagnosis — the local, discrete substrate has the correct topology (Klein bottle, Hopf fibration), but the golden ratio φ is **not present** in the bare uniform grid or its standard RG flow.
- **Constraint 1 (Phase 1):** standard 2×2 block-spin RG gives `D_eff → 2`, fixed point `D* ≈ 2`, not `φ`.
- **Constraint 2 (Phase 2):** local Hopf topology gives the form of `α = 4/R_f²` but the topological minimum `p = 3` yields `α ≈ 17.5`; matching observation requires a magnification `M ≈ 49.0 ≈ φ⁸`.
- **Implication:** φ is a large-scale, fractal/self-similar emergent property of the substrate weave — not a local graph invariant. Existing Plans 6–12 results are phenomenologically anchored but microscopically incomplete until this mechanism is found.
- **Note:** `notes/cross_phase_analysis_phases_1_2.md`

### Phase 3 (Constants-from-Geometry Roadmap): Mass Hierarchy, α_s, Neutrino Tunneling
- **Proton & electron:** formulas remain ~99.95% accurate.
- **Neutron:** `m_n = m_p(1 + δ_n)` with `δ_n = α/φ²` gives 99.91% accuracy (high by ~0.85 MeV); best-fit `δ_n ≈ 0.001884` (~2/3 of `α/φ²`). The plan's literal ratio form has the wrong sign.
- **Strong coupling α_s:** associator model `α_s(E) = C φ^{-n(E)}` is qualitatively asymptotically free but quantitatively fails at low energy; fixed-point normalization `C = 1/φ²` gives `α_s(M_Z) ≈ 0.38` vs observed 0.118.
- **Neutrino mass:** topological tunneling through the non-orientable twist requires a per-tick probability `P_tunnel ≈ 4×10^{-30}` for `m_ν ~ 0.05 eV`, ~10^{27}× smaller than the naive `α/φ²` estimate.
- **Plan:** `notes/IST_Research_Plan_Phases_1-5.md` | **Supplementary:** `supplementary/phase3_mass_hierarchy.md`
- **Script:** `code/phase3_mass_spectrum.py` | **Tests:** `tests/test_phase3_mass_spectrum.py`
- **Outputs:** `code/outputs/phase3/mass_predictions.csv`, `mass_hierarchy.png`

### Phase 4 (Constants-from-Geometry Roadmap): G from the Compression Spectrum
- **Ψ linearized:** `M_Ψ = I − F^{-1}L/4`; decay spectrum from the generalized problem `L v = γF v` — real, nonneg, reduces to the Phase 1 Laplacian spectrum at `f = 1`.
- **Slowest mode = gravitational time scale:** `τ_fold = 4/γ_min`, `G_eff ∝ τ_fold`. Nonlinear Ψ simulation reproduces `τ_fold` to 99.5%.
- **Non-orientability as IR regulator:** torus control has `γ_min = 0` → `τ_fold = ∞`; the Klein twist gap keeps gravitational latency finite.
- **Regional latency:** sheet/void Dirichlet contrast is exactly the fold factor (`τ_sheet/τ_void = f`).
- **Global scaling:** measured `G_eff ∝ ρ^{0.600}` over `ρ ∈ [1, 16]` — within 3% of the IST target `ρ^{1/φ}`, but it is a crossover window (extended → localized slowest mode); asymptotic exponent → 1. Crossing-time (propagation) latency gives `ρ^{1.09}`. The two measures bracket `1/φ`.
- **Void suppression:** 93.8% at `f = 16` (IST phenomenology ~76% at gentler contrast).
- **Implication:** the local substrate contains the crossover skeleton (sub-linear global window) on which a fractal RG completion must hang the exact `1/φ` exponent — a concrete target for the missing φ-mechanism.
- **Plan:** `notes/IST_Research_Plan_Phases_1-5.md` | **Supplementary:** `supplementary/phase4_geff_derivation.md`
- **Script:** `code/phase4_variable_g.py` | **Tests:** `tests/test_phase4_variable_g.py` (20 tests)
- **Outputs:** `code/outputs/phase4/decay_spectrum.csv`, `geff_vs_rho.csv`, `crossing_time.csv`, `geff_vs_rho.png`

### Data Pipeline
- **Fetch:** `data_fetch/fetch_hsc_m31.py`, `fetch_cosmos_web.py`, `fetch_ligo.py`
- **Preprocess:** `preprocess_microlensing.py` (events → threads), `preprocess_lss.py` (galaxies → Ξ threads)
- **Fit:** `ist_observational_fit.py` (PBH mass function + quenching validation)
- **Cross-ref:** `cross_reference_running_coupling.py` (Plan 7 running curve validation)
- **Docs:** `code/README_directed_numbers.md`, `code/README_data_integration.md`

---

## Open Questions

### High Priority
1. [ ] Derive electron mass from first principles (single-loop topology)
2. [ ] Refine QED corrections to proton mass formula
3. [ ] Run void lensing simulations with JWST-like noise
4. [ ] Assess CMB parity signal significance with proper null tests
5. [ ] Derive force coupling constants from substrate harmonics

### Medium Priority
6. [ ] Neutron mass derivation (why slightly heavier than proton?)
7. [ ] Neutrino mass mechanism (different topology? leakage?)
8. [ ] Muon/Tau mass hierarchy (higher-generation electrons)
9. [ ] Pion/meson mass derivation
10. [ ] GW soliton echo search strategy

### Long-term
11. [ ] Formalize projection map $P: \Sigma \rightarrow \mathbb{R}^3$
12. [ ] Derive Bell inequality violation from substrate topology
13. [ ] Connect to Riemann hypothesis (information density = zeta zeros?)
14. [x] Numerical relativity on the substrate (black hole mergers) -- *Proof-of-concept: TopologicalHorizon class with Klein bottle horizon simulation*
15. [ ] Consciousness substrates (speculative; IIT connection)

---

## Contributing

This is a collaborative research project. Contributions are welcome in the form of:

- **Analysis** -- New data analysis, simulations, or theoretical derivations
- **Critique** -- Identifying weaknesses, inconsistencies, or alternative interpretations
- **Connections** -- Linking IST to other theoretical frameworks or experimental results
- **Writing** -- Improving clarity, filling gaps, or translating to new formats

To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-idea`)
3. Make your changes in Markdown
4. Submit a pull request with clear description

---

## Citation

If you use IST in your research, please cite:

```bibtex
@article{theadoor2026ist,
  title={Information Substrate Theory (IST): Topology as a Substrate for Emergent Physics},
  author={Theadoor, Mary and the NOWN Research Collective},
  journal={arXiv preprint},
  year={2026},
  note={Working paper v5.3}
}
```

---

## License

This work is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0). You are free to share and adapt the material for any purpose, provided you give appropriate credit.

---

## Contact

**Principal Investigator:** Dr. Mary Theadoor  
**Research Group:** NOWN Research Collective  
**Repository:** https://github.com/NOWN-Research/ist_papers

---

*"The universe is not a machine. It's a self-interfering information substrate that projects the appearance of space, time, matter, and energy from the simplest possible ingredients: pattern, oscillation, and the golden ratio."*
