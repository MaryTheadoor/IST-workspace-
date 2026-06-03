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
