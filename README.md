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
|   |-- black_hole_simulation.py         # GPU-accelerated BH topology simulation
|   |-- black_hole_viz.py               # Klein bottle information knot visualization
|   |-- outputs/
|   |   |-- entropy_comparison.csv       # BH entropy by topology
|   |   |-- klein_info_knot.png          # Klein bottle info knot rendering
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

### Black Hole Topology (Klein Bottle Horizon)
- **Model:** Black hole horizons as non-orientable topological spaces
- **Class:** `TopologicalHorizon` in `ist_toolkit_v2.py`
- **Entropy:** Topology-corrected Bekenstein-Hawking $S = A/(4\ell_P^2) \times f(T)$, where $f(\text{Klein}) = 1 + |\text{twist}|$
- **Simulation:** JAX-accelerated 1000-step info-density evolution across sphere, torus, and Klein bottle
- **Ringdown:** Topology-dependent quasinormal mode frequencies
- **Viz:** 3D Klein bottle with extracted information knots and linking numbers
- **Status:** Proof-of-concept; see `notes/black_hole_topology_plan.md`

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
