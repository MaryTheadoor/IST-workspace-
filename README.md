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
|   |-- ist_v8_0_topology_substrate.md  # Primary IST paper (v8.0, strict physics core)
|   |-- ist_v7_0_topology_substrate.md  # Superseded by v8.0 (historical snapshot)
|   |-- ist_v6_0_topology_substrate.md  # Deprecated snapshot (tag v6.0-paper-snapshot)
|   |-- cross_phase_synthesis.md        # Complete phase table (1-60) + cross-phase synthesis
|   |-- synthesis_paper.md              # Living synthesis paper (v2.9)
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
pandoc main/ist_v8_0_topology_substrate.md \
  -o publication/ist_v8_0_topology_substrate.tex \
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
python scripts/md_to_latex.py --input main/ist_v8_0_topology_substrate.md --output publication/
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
git clone https://github.com/MaryTheadoor/IST-workspace-.git
cd IST-workspace-

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

### Proton/Electron Ratio (Phase 27 — top-down, parameter-free)
- **Formula:** $m_p/m_e = 6\pi^5$ (both $\alpha$ and $\varphi^2$ cancel between the two mass formulas)
- **Accuracy:** 99.9981% (1836.118 predicted vs 1836.153 observed)
- **Status:** IST's strongest top-down test — no free parameters; validated at the QM scale against CODATA 2018

### Electron Mass
- **Formula:** $M_P/m_e = (12\pi^5/\varphi^2)\alpha^{-9}$
- **Accuracy:** 99.95%
- **Insight:** Electron is single chiral loop; proton is 3 quark loops

### Neutron Mass (Phase 28/29/30 — exact, fully derived)
- **Exact closed form:** $\delta_n = (\alpha/2\varphi^2)(1-(3/2-\alpha/\varphi^6)\alpha)$ — 0.02σ from CODATA 2018 (100.000000%)
- **Factor 2 derived (Phase 29):** = half-integer Klein meridian quantization ($\theta = 1/2$); a single-valued charge needs two traversals, so $\Xi_{\text{eff}} = 1/2$
- **Radiative (3/2)α derived (Phase 30):** the *same* twist $\theta=1/2$ enters twice — $f_{\text{Klein}} = 1+|\theta| = 3/2$ is the master-equation topological factor; $\alpha/\varphi^6$ is the triple golden suppression $(\alpha/\varphi^2)^3$. One twist controls the whole correction
- **Directed-number picture:** the associator magnitude is parity-invariant; purity-flipping flips the topology ($f = 1+|\theta|$) and charge quantization ($\Xi_{\text{eff}}$), not the interaction strength
- **Correction:** the earlier "running φ ≈ 1.98 gives 99.99%" was an arithmetic error; true running $\varphi_n = 2.301 \approx \varphi\sqrt{2}$

### Fine-Structure Constant
- **Result:** $\alpha = r_e/\bar{\lambda}_C$ (geometric ratio, no free parameters)
- **Status:** Exact derivation

### Lepton Generations (Phase 31 — the one-twist muon, Koide)
- **Observational anchor:** Koide $Q = \frac{m_e+m_\mu+m_\tau}{(\sqrt{m_e}+\sqrt{m_\mu}+\sqrt{m_\tau})^2} = 2/3$ holds to **0.0009%** (parameter-free)
- **One-twist connection:** $Q = 2/3 \Leftrightarrow$ Koide phase $\varphi = \pi/2$ (measured 90.000374°, 6.5 μrad off) — and $\pi/2$ IS the half-integer twist $\theta = 1/2$ that derives the neutron factor-2
- **Three generations** = three $2\pi/3 = 120°$ phase offsets around the 720° Klein double-cover
- **Muon on the back sheet:** the Koide $\sqrt{m}$-fan at $\pi/2$ gives the muon a negative amplitude ($1-\sqrt{3/2}<0$) — the double-cover's $-1$ traversal. This is *why* the naive $m_\mu/m_e \approx 3/(2\alpha)$ hits only 99.41%; Koide $Q$ is robust because it is sheet-invariant
- **Status:** observational anchor + structural coherence; individual $m_\mu/m_e$ still open

### Quark-Sector Koide Test (Phase 32 — honest falsification)
- **Heavy (c,b,t):** Koide $Q = 0.6696$, **+0.45%** from 2/3 — *consistent* (edge of pole-mass systematics; MS-bar scheme gives 8%)
- **Light (u,d,s):** $Q = 0.567$ (−15%) — broken; up-type (u,c,t) +27%, down-type (d,s,b) +9.7% broken
- **Result:** exactly one Koide-valid quark generation (the heavy one) — the $\pi/2$ twist survives where the topological mass dominates
- **Honest status:** consistent, NOT confirmed — the light breakage is expected standard RG physics, not a unique IST prediction

### Baryon Mass Ladder (Phase 34/35 — derived)
- **Baryon masses in units of $E = \hbar c/1\text{ fm} = 197.33$ MeV** (the master equation's QCD-scale quantum)
- **Derived (Phase 35):** $m(S) = [4 + \tfrac{k}{2}f_{\text{Klein}}]E$, $k = 1,3,4,5,6$ — the **4 = the double-cover** (four plonk ticks of the 720° cycle), $f_{\text{Klein}} = 3/2$, and the nucleon's $(1/2)f = 19/4$ is now **derived, not empirical** (it's the half-twist / spin-1/2, the same $\theta = 1/2$ throughout the framework)
- **Decuplet:** Δ, Σ*, Ξ*, Ω all to ≤0.29%
- **The (3/2) = f_Klein:** the spin-3/2 decuplet sits one topological-factor step above the spin-1/2 nucleon
- **Octet (closed, Phase 45):** $\Lambda$, $\Sigma$, $\Xi$ obey a **golden partition** — $\Sigma$ splits the $\Lambda \to \Xi$ interval at $1/\varphi^2$ (0.108%), so $(\Xi-\Sigma)/(\Sigma-\Lambda) = \varphi$ (0.175%). Parameter-free: $\Sigma = \Lambda + (\Xi-\Lambda)/\varphi^2$ → 0.007%, $\Xi = \Lambda + \varphi^2(\Sigma-\Lambda)$ → 0.017%. GMO sum rule holds (0.57%); base-specificity (G2) picks $1/\varphi^2$ uniquely. The octet is NOT an E-ladder — its clean law is the golden partition, vs the decuplet's clean E-ladder.

### Baryon Octet: Λ–Σ Mixing as Golden Partition (Phase 45 — closed)
- **Open item resolved:** Phase 34 left the octet "Λ–Σ mixing not clean"; Phase 45 shows the internal gaps are **golden-partitioned** by $\Sigma$: $(\Sigma-\Lambda)/(\Xi-\Lambda) = 1/\varphi^2$ (0.108%), $(\Xi-\Sigma)/(\Sigma-\Lambda) = \varphi$ (0.175%)
- **Parameter-free predictions:** $\Sigma$ from $(\Lambda, \Xi)$ → 0.007%; $\Xi$ from $(\Lambda, \Sigma)$ → 0.017%
- **Robustness (G2 frame):** `base_specificity` gives a 0.38% basin with $1/\varphi^2$ inside and uniquely best (competitors 3/8, 0.38, 5/13, 8/21, 0.39, 0.4 all worse)
- **GMO anchor:** standard sum rule holds to 0.57% (known physics, re-verified)
- **Honest framing:** the octet is NOT an E-ladder (Phase 34 confirmed) — it is the *second* clean SU(3) structure, with the golden partition as its law, complementing the decuplet's E-ladder

### Dimensional Crystallization (Phase 36 — CMB-refined)
- **Hypothesis:** the expanding universe is the 3rd dimension crystallizing out of a 2D substrate (ice from a superfluid): $D(z) = 2 + [1+e^{(z-z_c)/w}]^{-1}$
- **H(z) chronometers (60, z<2.4):** degenerate with ΛCDM ($\Delta\chi^2 = -0.5$) — cannot distinguish
- **CMB shift prior (decisive):** $D \to 2$ by recombination gives $R \approx 6$ vs 1.7502 — **excluded by ~985σ**
- **Refined picture:** crystallization completes *before* recombination; $D \approx 3$ at all observable z. The 3rd dimension crystallized at/near the big bang, not gradually — the honest negative locates the postulate's valid regime

### BAO Sound-Horizon Test (Phase 44 — honest negative, confirms Phase 36)
- **Hypothesis:** the DESI DR1 BAO standard ruler ($D_M/r_d$, $D_H/r_d$ at z = 0.51–1.49, 1–5% precision) is an integral geometry probe that could break the H(z) degeneracy Phase 36 left open
- **Joint H(z)+BAO (H44a):** $\Delta\chi^2 = -4.6$ — BAO does **not** discriminate crystallization from ΛCDM
- **BAO-only $z_c$ basin (H44c):** flat ($\chi^2$ 35–38 across $z_c$ = 0.5–8) — the ruler at z ≤ 1.5 cannot pin the crystallization redshift on its own
- **Shape delta at fixed (H0, Om) (H44b):** only +9.1, far below the $D_H(0.51)$ anomaly that hits **both** models (+5.7σ cryst / +5.6σ lcdm) — the ruling tension is the known low-z DESI point, not the crystallization geometry
- **Net:** BAO sound-horizon test is an honest negative that *confirms* Phase 36 — the refined picture (crystallization before recombination, D ≈ 3 at observable z) survives the ruler; discriminators remain at higher z

### Force Unification as Harmonics (Phase 37 — honest negative)
- **Hypothesis:** the forces are specific harmonic excitations of the substrate — the field being the non-local average of information resonating at that harmonic
- **Tested three ways against measured couplings:** (A) fixed-scale ladder at M_Z: only $em/weak \approx \varphi^3$ (2.3%); (B) β-coefficients not clean; (C) slaved running calibrated at M_Z deviates at high energy
- **Honest result:** the simplest harmonic-unification formulations are **not supported** by the coupling data — the framework's golden-harmonic evidence is in the *mass spectrum* (Phases 28–35), not the bare couplings
- **Refined hypothesis needed:** harmonics may structure the mass–coupling relation rather than the couplings themselves

### Mass–Coupling Relation (Phase 38 — Insight B)
- **Mechanism (strong force, supported):** $\alpha_s(E) = (1/\varphi^2)\varphi^{-n(E)}$, $n(E) = \ln(E/m_p)/\ln(\varphi^4)$ — the golden-layer count from the proton mass reproduces $\alpha_s(M_Z)$ at 3.1% and $\alpha_s(m_\tau)$ at 1.3%, with the associator magnitude $1/\varphi^2$ as the natural normalization
- **Per-force ladder (partial):** $C_i = \alpha\varphi^{k_i}$ gives $k = 2.52, 5.57, 8.16$ for em/weak/strong — rises with force strength, but gaps (2.6–3.0) not uniform
- **Honest synthesis:** the masses *do* determine $\alpha_s$ through the golden layer count (resolving Phase 37's tension — couplings aren't golden *values*, but the mass→coupling *mechanism* is golden)

### Active-Flavor Thresholds (Phase 39 — threshold confirmed)
- **Problem:** the mass→coupling model over-predicts $\alpha_s$ at $m_b$ (+19.5%) and $m_t$ (+15.2%) — too-fast running above each quark mass
- **Fix (flavor thresholds):** free fit cuts $m_b$ 19.5%→3.0%, $m_t$ 15.2%→4.5%; principled $f(n_f) = \varphi^{-(n_f-3)/6}$ (QCD $b_0$ as golden powers) improves $m_t$→2.7%, $m_\tau$→2.0%
- **Suggestive:** free-fit $f(6) \approx \varphi$ (1.3%)
- **Honest:** the threshold mechanism is confirmed; no single golden rule fits all four references yet — clean closure needs piecewise QCD-style active-flavor running

### Bell Non-Locality Mechanism (Phase 40 — EPR resolved as projection)
- **Mechanism:** two "entangled" particles are two 3D projections of the *same substrate point* (twist-adjacent, euclid-far — Phase 26 found 3024 pairs, ratio 7.5×)
- **Substrate singlet** $E(a,b) = -\cos(a-b)$ gives **CHSH S = 2.83** (Tsirelson, Bell-violating); local hidden variable models capped at S = 2.00
- **Signal-locality:** A-marginals 0.51 vs 0.49 across Bob's settings — no superluminal signaling
- **Resolution:** non-locality is a *projection artifact* (shared substrate point); no signal travels because there is no signal — there is a shared substrate region

### Measurement Problem (Phase 41 — Collapse as Entropic Crystallization)
- **Mechanism:** wavefunction collapse is a dynamic phase transition triggered by environmental/probe interaction (vacuum pump)
- **Simulation:** pumping a probabilistic superposition of modes drives it past the laser-like threshold (layers 8-11)
- **Result:** the golden mode crystallizes (coherence jumps to 0.86), normalized gap entropy drops 6%; silver control mode hits destructive resonance and decays
- **Unitarity:** total information strictly conserved (error = 0.0) — collapse is a unitary redistribution of topological charge into a golden-rigid pattern, not dissipative loss

### Flavor-Threshold Golden Closure (Phase 42 — boundary convention resolved, H42g demoted)
- **Bug found (Phase 39 convention):** $m_t$ never gets 6 flavors — the loop breaks at $E \le t$ before the top segment, so $f(6)$ was an unconstrained artifact
- **Fix (QCD upper convention):** reference AT a threshold uses the flavor count ABOVE it — $m_b$ activates $f(5)$, $m_t$ activates $f(6)$
- **Result:** principled $\varphi^{-(n_f-3)/6}$ improves RMS 9.56% → 8.78%; best single-exponent scan $a = 0.150$ → 8.70%
- **H42g (self-referential 137) — DEMOTED by robustness checks:** $\alpha^{-1} = 360/\varphi^{2+\alpha}$ fixed point = 137.026 (0.0075% from CODATA) but FAILS all four checks: non-unique root (0.0625 & 137.03), base-unspecific (0.09% basin), unit-fragile (deg 137 vs rad 1.85), exponent-free (14 k values fit). A tuned 2-parameter coincidence, not a claim.
- **Methodology output:** `code/golden_relation_checks.py` + tests now enforce uniqueness/base-specificity/unit-invariance on every golden relation
- **Honest:** no single golden rule fits all four $\alpha_s$ references (best 8.7%); even the flavor closure's optimal base is 1.634, 0.99% above $\varphi$

### 2-Loop Golden Closure (Phase 43 — honest negative, m_b anomaly localized)
- **Gap fixed (H42d was dead code):** Phase 42's $b_1$ cast used `0.0*k1`; the 2-loop term was never tested. Folding the real $b_1$ in **closes $m_b$** (+15.95% → +0.75%) — the $m_b$ residual *is* the 2-loop curvature — but over-corrects the high scale ($M_Z$ −42%, $m_t$ −76%).
- **Full-curve 2-loop QCD RGE (H43b):** overlay against exact MS-bar running shows the irreducible conflict lives in the **$m_b \to M_Z$ segment, which runs +31.5% too steep** in the golden layer model. Also surfaces that the $m_t$ reference 0.090 is scheme-dependent (2-loop QCD running gives 0.108, +19.6%).
- **Reference-systematics audit (H43c):** even against credible PDG/uncertainty ranges, $m_b$ (+6.8%) and $M_Z$ (−5.9%) stay outside the bands — the residual is not absorbed by legitimate reference choice.
- **Exponent-basin robustness (H43d, G4 frame):** the principled 1/6 sits inside the RMS<10% basin (width 0.157) but is not the minimum (best $a=0.148$, RMS 8.70%).
- **Low-scale anchor (H43e):** anchoring $\alpha_s(m_\tau)=0.330$ closes $m_t$ (−0.17%) and improves $M_Z$, but worsens $m_b$ — no single anchor closes all four.
- **Honest negative:** no single golden rule closes all four $\alpha_s$ references; the $m_b/M_Z$ slope conflict is irreducible under b0-only, b0+b1, both boundary conventions, and reference-systematics ranges. The flavor-threshold mechanism is confirmed; the clean closure remains open.
- **Perf:** QCD RGE hot loop JIT-compiled with numba (works on Python 3.14; GPU not viable — GTX 1050 is Pascal and CUDA 13 dropped Pascal)

### Reference-Level Fix Test (Phase 46 — honest negative, closure is reference-irreducible)
- **Question (Phase 43 open item):** does the scheme-dependence of the $m_t$ reference (0.090 convention vs 2-loop QCD running 0.108) re-scope the flavor closure target?
- **H46a — m_t reference fix REFUTED:** substituting $m_t = 0.108$ for 0.090 *worsens* the principled RMS 8.78% → 12.70% ($m_t$ −2.2% → −18.5%). The 0.090 convention was **masking** the $m_t$ deficit, not causing the $m_b/M_Z$ conflict.
- **H46b — QCD-consistent reference set:** scoring against the exact 2-loop QCD running values (0.3133/0.2236/0.1180/0.1076) makes all golden models *worse* (principled RMS 12.10%; $m_b$ +14.1% irreducible).
- **H46c — free references in credible ranges:** with ALL four references free inside their credible ranges, the best single exponent ($a = 0.110$) still leaves $m_b$ (+7.4%) and $M_Z$ (−2.5%) OUT — no reference placement rescues a single golden exponent.
- **H46d — two-parameter decoupling:** two free exponents ($a$ for $n_f\le5$, $b$ for $n_f=6$) also fail (best $(0.110, 0.000)$, $m_b$/$M_Z$ still OUT). The conflict is not an exponent-count artifact.
- **H46e — structural diagnosis:** the layer base REQUIRED to match 2-loop QCD exactly needs $\varphi^{+0.82}$ in the $m_b\to M_Z$ segment (flattening) — the *opposite sign* of the principled $\varphi^{-0.5}$. Golden running is a **power law in E**; QCD running is $\sim 1/\ln E$ (flattening at high E). The $m_b/M_Z$ conflict is a shape mismatch, **reference-independent**.
- **Honest negative:** the Phase 43 sequencing question is answered — the flavor closure is reference-irreducible; no legitimate reference choice or golden exponent set closes it. This closes the $\alpha_s$ flavor-closure line with a definite, quantified statement.

### Emergent-Twist Derivation (Phase 47 — derived)
- **Open item resolved:** Phase 29 empirically mapped the fractional twist $\theta = 1/2$ to momentum halving, but lacked a topological derivation. Phase 47 derives $\theta = 1/2$ exactly and parameter-free.
- **U(1) Embedding:** the non-orientable Klein substrate (Phase 1) has an orientation-reversing seam, defining a flat $\mathbb{Z}_2$ connection with meridian holonomy $W = -1$.
- **Fractional Charge:** to support a complex quantum field (master equation), this real line bundle embeds into a $U(1)$ bundle, mapping $-1 \to e^{i\pi}$. The twist is the fractional winding number $\theta = \arg(W)/2\pi = 1/2$ exactly.
- **Unification:** this rigorously proves $\theta = 1/2$ is an exact topological invariant, securing the foundation for the neutron factor-2, Koide phase, and double-cover baryon ladder.

### Stable-Knot SM Multiplicity Mapping (Phase 48 — closed)
- **Open item resolved:** Phase 24 established that ~3% of the nodes form stable topological defects (knots). Phase 48 maps this fraction to the SM particle multiplicities.
- **The Fibonacci Standard Model:** Because the substrate is a Fibonacci lattice, topological defects are constrained to the Fibonacci sequence $F_1 \to F_9$.
- **Exact SM Mapping:** $F_1=1$ (Higgs), $F_2=1$ (Photon), $F_3=2$ (Chiralities), $F_4=3$ (Generations/Weak bosons), $F_5=5$ (Fermion multiplets), $F_6=8$ (Gluons/Fermions per gen), $F_7=13$ (Total bosons), $F_8=21$ (Total fundamental types).
- **The 1/34 Knot Fraction:** The theoretical probability of a stable knot is exactly $1/F_9 = 1/34 \approx 2.941\%$, statistically confirming the empirical Phase 24 mean ($3.13\% \pm 0.48\%$). The boson/fermion ratio is exactly $F_7/F_6 = 1.625 \approx \varphi$.

### Topological Proton/Electron Mass Ratio (Phase 49 — derived)
- **Open item resolved:** Phase 27 established the empirical identity $m_p/m_e = 6\pi^5$ to 99.9981%. Phase 49 derives the factor $6$ directly from the topological volume of $SU(3)$ and the quark color count ($N_c$).
- **The Exact Derivation:** The topological (Poincare) volume of the $SU(3)$ gauge group is generated by spheres $S^3$ and $S^5$, giving $Vol(SU(3)) = 2\pi^5$.
- **The Duality:** The mass ratio is exactly $m_p/m_e = N_c \times Vol(SU(3)) = 3 \times 2\pi^5 = 6\pi^5$.
- **Physical Meaning:** The relative phase-space volume of the unconfined electron exactly balances the unconstrained $SU(3)$ phase space that is "missing" from the $3$ confined quarks of the proton.

### Light Quark Golden Partition Test (Phase 50 — honest negative)
- **Question:** Phase 45 showed the Baryon Octet obeys the Golden Partition $(\Sigma-\Lambda)/(\Xi-\Lambda) = 1/\varphi^2$. Do the bare quarks ($u, d, s$) that comprise these hyperons carry the same law?
- **H50a — REFUTED:** the bare gap ratio $(m_d-m_u)/(m_s-m_u) = 0.0275$ is 92.8% off $1/\varphi^2 \approx 0.382$.
- **H50b — scale-invariant negative:** all light quarks share the same $\gamma_m$, so their mass ratios (and gap ratios) are exactly RG-invariant — running the masses by any factor changes nothing. The failure is absolute, not a $\mu=2$ GeV artifact.
- **H50c — Koide space fails too:** $0.084$ vs $0.382$ in $\sqrt{m}$ space.
- **Net:** the Golden Partition is a law of the *bound-state topological knots* (the physical hadrons), not of the bare, scheme-dependent quarks — the same dividing line as Phase 37 (golden in masses, not couplings) and Phase 46 (golden power-law fails on bare QCD). φ lives in the emergent confined excitations.

### Fibonacci Laplacian (Phase 51 — the true incommensurate substrate spectrum)
- **Question:** Phase 1 falsified static-φ on a *rational* raster grid ($4p^2+\ell^2$ ladder, unavoidable mode-locking). `discrete_substrate_not_raster.md` prescribed the correct cellulation: the incommensurate golden-angle (Fibonacci) lattice. What does the true substrate spectrum look like?
- **H51a — EXACT 1D (Kohmoto–Kadanoff–Tang):** the transfer-matrix trace map $x_{n+1}=2x_n x_{n-1}-x_{n-2}$ holds to 2e-13 and the KKT (Fricke) invariant to 5e-10 — provably exact golden self-similarity. The spectrum fragments as a **Cantor set**: 359 bands at gen 14 vs 2 for the periodic rational control.
- **H51b — topological twist is exact:** the Fibonacci lattice on the Klein bottle gives parity-inversion fraction **0.446, N-independent** (matching Phase 23a), while the raster grid's fraction drifts 0.449→0.462 with N (grid mode-locking).
- **H51c — spectral RG honest negative:** Galerkin coarse-graining keeps $D_{\rm eff} \approx 2.2$ (r²≈0.995) at every scale, **never φ**.
- **Net:** "was Phase 1's negative a raster artifact?" → refined no. The raster hid the incommensurate gap structure, but even the true lattice does not make $D_{\rm eff}=\varphi$. φ is not the substrate's spectral *dimension* — it is its *self-similarity* (exact KKT trace map) and its *topology* (the twist). Same line as Phases 37/46/50.

### Twist-Generated SM Partition (Phase 52 — the counting is now dynamical + geometric)
- **Question:** Phase 48 mapped the SM to F₁–F₉ with stable-knot fraction 1/34 — but as a *static* count cross-checked against Phase 24's old data. Phase 47 derived θ=1/2; Phase 51 built the true incommensurate lattice. Does the partition *emerge from the 4-tick (720°) orientation-cycle dynamics* on the true lattice, with the twist as generator?
- **H52a — 1/34 from the dynamics:** ensemble stable-knot fraction **0.0344 ± 0.0128**, consistent with 1/F₉ = 1/34 ≈ 2.94% and Phase 24's 3.13%±0.48% band. (Honest: single runs are noisy — phase-return is dominated by coupling, not topology — the claim is the ensemble mean.)
- **H52b — the substrate partitions by consecutive Fibonacci numbers (exact):** the golden-angle circle of N=Fₖ points has exactly two gaps with counts (Fₖ₋₁, Fₖ₋₂) — 55→21/34, 89→34/55, 144→55/89, 233→89/144, 377→144/233. The raster control [59,5]/[139,5] is NOT Fibonacci. This is the geometric substrate Phase 48's F-counting sits on.
- **H52c — θ=1/2 is the parity generator:** parity-inversion fraction **0.446 (Klein) vs 0.000 (torus)**; the chirality-flip double-cover operates *only* on the twisted substrate.
- **H52d — N-independence:** 0.446 across 210/360/480, reproducing Phase 51/23a.
- **Net:** the Phase 48 SM counting is not an ad hoc mapping — it is the counting of the gold substrate's geometry (consecutive-F two-gap partition), realized through the 720° double-cover dynamics with the half-integer twist (Phase 47) as the generator. Closes the mechanistic loop: static count (48) → twist derivation (47) → true lattice (51) → dynamics (52).

### Heavy-Flavor Octet: Does the Golden Partition Extend? (Phase 53 — closed, honest negative)
- **Question (external gap 6, pre-registered):** Phase 45's golden partition $(\Sigma-\Lambda)/(\Xi-\Lambda) = 1/\varphi^2$ was tested only on the LIGHT octet. PDG gives precise masses for the SU(3) analog triplets $\{\Lambda_Q, \Sigma_Q, \Xi_Q\}$ (Q = c, b). If the partition is a universal flavor law, the analogs must obey it within ~0.2%.
- **H53a — charm FAILS (139.5%, 205σ):** $(\Sigma_c-\Lambda_c)/(\Xi_c-\Lambda_c) = 0.9149$ vs $1/\varphi^2 \approx 0.3820$; gap $(\Xi_c-\Sigma_c)/(\Sigma_c-\Lambda_c) = 0.0930$ vs $\varphi$ (94.3% off, 491σ). Ordering Λ_c < Σ_c < Ξ_c still holds, so this is not a selection artifact.
- **H53b — bottom FAILS (189.7%, 177σ) and INVERTS:** split $= 1.1067$; the hierarchy flips to Λ_b(5619.6) < Ξ_b(5794.4) < Σ_b(5813.1), so the gap $(Ξ_b-\Sigma_b)$ is *negative* (−0.0964 vs φ, 512σ). Structural (HQET): the Σ_b−Λ_b hyperfine splitting ~193 MeV now exceeds the Ξ_b−Λ_b step ~175 MeV.
- **H53c — not an artifact:** failures are 177–512σ with PDG error propagation; the light anchor still passes (0.11% off) inside the same module.
- **Net:** the golden partition is a law of the *emergent, near-degenerate light octet* — the diquark hyperfine split and strangeness step balanced at 1/φ. A hard heavy-quark mass (c/b, set at the Higgs/Yukawa scale, NOT emergent) injects an off-scale splitting that erases the balance. Same dividing line as Phase 50 (bare quarks don't carry it) — φ lives in the emergent light confined structures.

### Look-Elsewhere Accounting: Registry + Trial-Factor (Phase 54 — gap 1 closed)
- **Question (external gap 1):** a referee's first question is *how many relations did you try, and what's the chance some survivors are coincidence?* Per-relation robustness (G1–G4) existed; global look-elsewhere accounting did not.
- **Registry:** all **46 tested relations** across Phases 1–53 with outcome + rejection reason: 20 SUPPORTED, 7 DERIVED, 13 NEGATIVE, 2 DEMOTED (H42g's 137 and the φ⁸ magnification — the self-demotions are registered, not hidden), 1 REJECTED, 2 PARTIAL, 1 CONSISTENT.
- **Trial factor:** each headline hit is scored against a bounded pool of **1866 simple constants** (rationals, a·φ^k, a·π^k, (2π)^k, a·6π⁵, Fibonacci ratios). m_p/m_e ~ 6π⁵ (1/1866), 1/34 (1/1866), decuplet 19/4 (1/1866) are **unique**; Koide 2/3 is robust (one golden competitor 12φ⁻⁶).
- **H54b — octet specificity audit:** the octet split r = 0.382379 is fit **16× tighter by 13/34 = F₇/F₉ (0.0067%)** than by 1/φ² (0.108%). 12 of the 13 matching constants are consecutive-Fibonacci convergents of 1/φ² — the *same* golden family, and exactly Phase 52's consecutive-F substrate.
- **Net (refinement, not negation):** Phase 45 should be read as "the octet split sits in the golden-Fibonacci family (limit 1/φ²)", not "1/φ² uniquely beats every rational" — Phase 45 tested competing *bases*, not competing *Fibonacci rationals*. H54b makes that blind spot explicit and public; it is consistent with Phase 52's geometric substrate.

### The Photon as a Dual-Mode Wave Function (Phase 55 — photon dynamics, first)
- **Question:** the repo had NO model of photon propagation — only defaults ("no knot → v=c, m=0" in `ist_toolkit_v2.py`; "information knot, I_topo=1" in `emc2_in_IST.md`; F₂=1 in the Phase 48 count). What is the substrate-native dynamics of the photon?
- **Model (DNA double helix):** the photon is a dual-mode wave function ψ=(E₊, E₋) propagating across **both sides** of the non-orientable manifold. Two strands = the two helicity (circular-polarization) modes, each the peak of the amplitude propagation; the connecting **rungs cross the zero point** (the twist seam) symmetrically.
- **H55a — dispersion-free translation:** shared group velocity v_g = 1.00000, independent of carrier frequency ω₀ ∈ {0,…,1.2} → universal c (the photon's speed is not set by its energy). Rung-lock 0.0000 — the helix translates rigidly, never unbinding (non-dispersing compound).
- **H55b — achiral spin-1:** parity-inversion fraction **EXACTLY 0.000** on the true Fibonacci-Klein lattice vs the electron knot's **0.446** (Phase 52 H52c). Symmetric rung-crossing makes sheet-swap (parity) a symmetry → no chirality flip over the 4-tick cycle.
- **H55c — massless, E = h·ν:** carried energy E = ω₀ exactly (linear, slope 1.0) while v_g stays constant as energy is added → m = 0.
- **H55d — single species F₂=1:** one gapless branch at the carrier wavenumber; the two helicity modes share it (one U(1) photon, no second propagating species).
- **Net:** the photon's four defining facts — universal c, achirality, massless E=hν, single species — are now each measured on the framework's own substrate. The 0.000-vs-0.446 parity-inversion contrast is the substrate's spin-statistics generator: fermions cross the seam once (spin-1/2 double-cover), gauge fields straddle it (spin-1).

### The 4WM Discriminator: Dual-Mode Vacuum vs QED (Phase 56 — gap 7 opened)
- **Question (external gap 7):** Zhang et al. (2025) simulate quantum-vacuum four-wave mixing (Heisenberg–Euler 3D solver). If IST's photon self-interaction predicts a specific 4WM signature QED lacks, that is table-top falsifiability — the one place IST contacts a laboratory system.
- **The discriminator is parity.** QED's vacuum has two quartic invariants with the canonical one-loop parity-odd ratio **c₂/c₁ = 7/4** (the (F·F̃)² = (E·B)² pseudo-scalar, source of vacuum birefringence / 4WM polarization rotation). Phase 55's **achiral** dual-mode photon (parity-inversion 0.000) predicts the parity-odd channel is **forbidden**: **IST c₂/c₁ = 0.0000 vs QED 1.7500** (H56a). A single polarization-rotation / ellipticity 4WM measurement separates the models.
- **H56b — golden-weighted magnitude:** the surviving parity-even channel carries the substrate's golden charge scale: c₁ = α/φ² (φ²/α ≈ 358.8), giving IST/QED coupling ≈ **52.3** = 1/(αφ²), 4WM signal ≈ **2.7×10³** in the allowed channel.
- **H56c — universal c:** the 4WM output peak propagates at v_g = 1.000000 (dual-mode H55a), consistent with Zhang et al.'s observed ~0.99c.
- **Net:** gap 7 now has a quantitative, discriminating, lab-testable prediction — the parity-odd 4WM channel is exactly zero for the dual-mode vacuum, mirror-image to the electron's 0.446. Not a new free number: it is Phase 55's geometry pushed into the vacuum.

### The Single- vs Dual-Strand Discriminator (Phase 57 — is the dual-mode geometry forced?)
- **Question:** the repo's OLD photon default was a *single structureless strand*: `"no knot → v=c, m=0"`. It was never tested. Could a single bare strand also be a photon?
- **Speed does NOT discriminate.** A single strand also translates at v_g = 1.00000 (shared linear dispersion) — the old default passed every speed/massless test, which is why it survived. Speed alone cannot tell a photon from a fermion.
- **Parity DOES discriminate.** A single strand threading the non-orientable Klein seam must flip chirality at 2 ticks: its parity-inversion is the **computed** lattice twist fraction **0.446** (numerically identical to the electron knot, H57a), vs the rung-bound dual mode's **0.000**. A single-strand "photon" is chirally indistinguishable from a fermion.
- **H57b — two polarizations need two strands:** helicity count 1 vs 2 (E₊, E₋); a single strand has no second independent polarization.
- **H57c — the bare default disperses:** a localized single strand evolved on the Klein graph (free walk, no rung binding) spreads (concentration 1.0 → 0.03), while the rung-bound compound stays at 1.0 — the rungs are load-bearing.
- **Net:** the dual-mode geometry is **forced**, not chosen. The old `"no knot → v=c"` default is **demoted to speed-only, insufficient** — right about v=c, wrong that it is enough. Consistent with Phases 55 (achirality 0.000) and 52 (electron = single-strand knot, 0.446).

### The Trace-Map RG (Phase 58 — rescoring Phase 51's spectral-dimension negative)
- **Origin:** the quasicrystal literature (Naumis 2003; Jagannathan RMP 2021) says the *trace map* is the natural RG for Fibonacci lattices and block-spin decimation is inappropriate for quasiperiodic systems. Phase 51 H51c's D_eff ≈ 2.2 "never φ" was measured with the *wrong* (Galerkin) RG.
- **H58a — the wrong RG is non-convergent and never golden:** block-spin spectral coarse-graining of the Fibonacci-Klein lattice gives D_eff that never approaches φ (min |D_eff − φ| ≈ **0.54**, an order of magnitude above the scheme's own scatter) and does not settle (range ~0.14; deepest projection degrades r²). No golden fixed point.
- **H58b — the natural RG is golden-EXACT:** the substitution RG (A→AB, B→A) has growth eigenvalue **F_{n+1}/F_n → φ** exactly (parameter-free; error 9.8×10⁻⁹), and its spectral kernel is the **KKT trace map** (recurrence 2.3×10⁻¹³, Fricke invariant conserved 4.7×10⁻¹⁰).
- **H58c — the verdict:** φ is an **RG (inflation) eigenvalue** of the golden substitution, *not* a static spectral dimension D_eff. Phase 51's negative is **rescored, not overturned** — it was right that φ is not D_eff, and the literature explains why (wrong RG).
- **Net:** a reported negative is now mechanistically explained, and φ's home in the substrate's RG structure is identified exactly — the golden inflation eigenvalue.

### Time-Crystal Dark Energy (Phase 59 — pre-registered, look-elsewhere-accounted audit of Plan 11)
- **Origin:** the literature sweep returned Berti et al. 2026 ("Stratoverso"), already running *log-periodic* structure-growth modulation against DESI DR1 full-shape + DR2 — the arena for oscillatory dark energy has moved to DESI. Plan 11 (a *plan*, never a phase) got two corrections it never had: **pre-registered anchors** and **look-elsewhere accounting**.
- **Pre-registered (before fitting):** ε₀ = α/φ² = 0.002787 (master-equation coupling) and Δ₀ = ln(φ) = 0.4812 (golden self-similarity period — the modulation is invariant under (1+z)→φ(1+z) ⟺ Δ = ln φ).
- **H59a — strict amplitude anchor (ε = ε₀ fixed):** Δχ² = **+0.15** vs ΛCDM — the master-equation amplitude is *invisible* in 60 H(z) chronometers (needs ~9× better precision for 3σ).
- **H59b — golden period anchor (Δ = ln φ fixed):** Δχ² = **+2.20**, ε = 0.106 ± 0.043, over **2.5 cycles** — the pre-registered golden period is the strongest, well-constrained hint (Plan 11's fitted Δ=1.54 spans only 0.79 cycles, which is why it was unconstrained).
- **H59c — free-Δ scan with look-elsewhere:** best Δχ² = 3.06 (local p = 0.22), but **global p = 0.62** after the frequency-band trial count — Plan 11's "0.29σ tension cut" does **not** survive accounting; it is consistent with a chance fluctuation.
- **H59d — detection forecast:** 3σ needs 8.9× smaller H(z) errors (for ε₀) or 2.1× (for ε = 0.136 at Δ = ln φ).
- **Net:** the time-crystal dark-energy modulation is **plausible but unverified** — consistent with ΛCDM in the H(z) data after accounting. Its falsifiable golden form (Δ = ln φ, ε = α/φ², 2.5 cycles) is a pre-registered target for the DESI DR1/DR2 full-shape arena, not a detected signal.

### Oscillatory DE "4σ" Audit (Phase 60 — joint H(z)+Pantheon++DESI BAO)
- **Origin:** Plan 11 / v8 §4.4 headline "4σ / Δχ²=22.1" joint-fit claim; Phase 59 already down-graded the 60-point H(z) subset (global p = 0.62). Phase 60 audits the *full* joint data.
- **LCDM baseline reproduced exactly:** χ² = 948.5, H₀ = 73.6 — pipeline matches v8.
- **Physical free fit (ε₀ ≥ 0, no hidden phase):** Δχ² ≈ 0 — oscillation adds nothing; ε₀ driven to zero. **The headline claim is not reproduced under the physically required constraint.**
- **No-sign free fit (ε₀ < 0 allowed):** Δχ² = +39.1 at interior Δ = 1.385, global p ≈ 0 — the entire "4σ" lives in the anti-phase channel, which is an unacknowledged free phase shift (π) masquerading as a detection.
- **Pre-registered φ³ (Δ = ln φ, β = φ³, ε₀ = α/φ²):** Δχ² = +1.0 — invisible on the joint data.
- **Amplitude bridge fails:** ε_eff(φ³) = 0.032 at z̄ ≈ 0.78 — still ×3.3 below Phase 59's ε ≈ 0.106.
- **Net:** the paper's headline observational claim is **an artifact of the sign-degeneracy channel** (ε₀ < 0 = hidden free phase π). The honest value of the oscillatory DE model on current joint data is Δχ² ≈ 0; the "4σ" does not survive scrutiny.

### Spin-Statistics from Seam Braiding (Phase 61 — spin-statistics DERIVED from the Z₂ holonomy)
- **Origin (external gap):** spin-statistics was an *input* — QFT imports it; IST should derive it from the substrate. The machinery already existed: W = −1 meridian holonomy (Phase 47), the 4-tick SU(2) cycle with flat limit exactly −I (Phase 25), and the strand dichotomy — electron = single-strand knot (parity 0.446), photon = dual-strand rung-bound compound (0.000) (Phases 52/55/57).
- **H61a — the exchange phase IS the substrate holonomy:** the meridian Wilson loop is W = −1 (grid-independent on the Phase-1 Klein graph; +1 torus). The 4-tick temporal cycle: single-strand (seam-threading, two half-twists per 360°) → **−I → phase −1 (fermion)**; dual-strand (achiral, no crossings) → **+I → phase +1 (boson)**; torus (no seam) → +1 for *both* — **there are no fermions without the twist.**
- **H61b — Pauli exclusion is the exchange algebra:** P|i,j⟩ = χ|j,i⟩ on the two-particle Hilbert space; P² = I exactly (double exchange = identity → ±1, the emergent-3D collapse σ = σ⁻¹); fermions: (1+P)|i,i⟩ = 0 — double occupancy annihilated topologically; bosons: (1−P)|i,i⟩ = 0 — antisymmetric double occupancy vanishes, symmetric survives; mixed species: no exclusion.
- **H61c — the anyon collapse is the Z₂:** all Wilson loops of the Klein graph are ±1 (holonomy group exactly Z₂); a continuous U(1) holonomy (θ ≠ π) gives P² ≠ I and non-±1 eigenvalues — genuine anyons with no clean exclusion; the Z₂ value θ = π is the unique collapse point. Honest guard: the exchange phase is **not** the random-pair twist flag (the 0.446 mixture is pair-dependent, not a statistics); it is the loop holonomy W = −1.
- **H61d — consistency + prediction:** electron (single, 0.446) ↔ χ = −1 fermion; photon (dual, 0.000) ↔ χ = +1 boson; the dimensional-emergence note's strand classifier (single-strand ⇒ seam parity) then **predicts the neutrino is a fermion** (single-strand) — consistent with observation.
- **Net:** spin-statistics is no longer an input — it is the Z₂ exchange holonomy of the seam, composed from Phase 47's W = −1 and the measured strand structure (Phases 55/57). No free parameters. The anyon question is answered: the flat Z₂ seam quantizes the braid phase to ±1, and the emergent 3D stack (σ = σ⁻¹) makes it a genuine permutation statistic.

### The IXPE Vacuum-Birefringence Gate (Phase 62 — the flagship meets its first empirical neighbor)
- **Origin (memo item 9, urgent):** Stewart et al. 2026 (arXiv 2509.19446, *Nature*; IXPE+NICER+Parkes) report the strongest evidence yet for QED vacuum birefringence in magnetar 1E 1547.0−5408 (B ≈ 5 B_cr): PD 65±8% at 2 keV, a 2–4 keV depolarization dip (vacuum-resonance mode conversion), RVM-locked PA, and VB-on fits crushing VB-off (χ²/dof 19.0/4 vs 106.8/4). VB and four-wave mixing are the **same two Heisenberg–Euler coefficients** c₁, c₂ — the flagsip prediction c₂/c₁ = 0 is now empirically adjacent.
- **H62a — the mode algebra (derived, verified):** exact quadratic expansion of L = c₁(F²)² + c₂(F·F̃)² around a pure-B background decouples the eigenmodes cleanly by invariant: **n(E∥B) − 1 = 16c₂B²sin²θ, n(E⊥B) − 1 = 16c₁B²sin²θ** — reproducing the canonical (14/45, 8/45) QED numbers with ratio 7/4 = c₂/c₁ at all angles. **c₂ = 0 ⟹ the E∥B mode is exactly non-refractive** (index 1 at all angles); VB survives via the E⊥B (c₁) channel.
- **H62b — the magnetar observable:** the QED accumulated phase puts the mode-decoupling radius at **136 R*** — inside the paper's own 30–300 R* statement (an independent validation of the whole chain). Branch (ii) (c₁ ≈ QED, c₂ = 0): |Δn| = 4/3×QED sign-flipped, decoupling 144 R*, VR unchanged → **consistent**. Branch (i) (c₁ = 52.3×QED, the Phase 56 α/φ² magnitude reading): VR dip moves to **0.41 keV** (observed 2–4 keV) and decoupling 318 R* → **tension**.
- **H62c/H62d — the gate verdict:** (1) **c₂/c₁ = 0 survives structurally** — the E∥B mode's index ≡ 1 is a normalization-independent, mode-resolved falsifiable signature that no current dataset tests; (2) **the 52.3× 4WM enhancement (Phase 56 H56b) is gated OFF** — the 2–4 keV dip constrains c₁ to near-QED strength; the physical c₁ normalization is now a required derivation; (3) registry records the constraint, the branch table, and the gap. The public registration of c₂/c₁ = 0 proceeds in the structural (mode-resolved) form only.

### The c₁ Normalization Resolution (Phase 63 — the gate's required derivation, delivered)
- **Origin:** the Phase 62 gate demanded the physical normalization of c₁ = α/φ². The template: Phase 49's normalization lesson — physical normalizations are fixed by the phase space actually paid, and the data select the counting (Vol_topo(SU(3)) = 2π⁵ over Vol_Haar = √3π⁵; see the new `notes/phase49_internal_memo.md`).
- **H63a/b — the map and the band:** R ≡ c₁_IST/c₁_QED = 52.33·(m_e/M_assoc)⁴. The observed 2–4 keV VR dip (E_VR = 3 keV/√R) inverts to **M_assoc ∈ [1.12, 1.59] MeV** — the IXPE data select the loop scale.
- **H63c — candidate scales:** m_e (R = 52.3, E_VR = 0.41 keV — the gated branch), 2m_e (1.66 keV — out), **φ²m_e = 1.338 MeV (R = 1.114, E_VR = 2.84 keV — IN)**, m_n−m_p = 1.293 MeV (R = 1.28, 2.66 keV — IN), √(m_e·m_μ) and m_π (far out).
- **H63d — the φ² reading:** the vacuum loop pays the same associator suppression φ² the electron mass formula pays (M_P/m_e = (12π⁵/φ²)α⁻⁹) → **M_assoc = φ²m_e**, giving **c₁_IST = 1.114×QED, E_VR = 2.84 keV, |Δn| = 1.486×QED (sign-flipped), decoupling 147 R*** — every observable inside the IXPE anchors. Falsifiable the moment |Δn| is extracted or the dip centroid is measured.
- **H63e — honest status:** the normalization is *empirically anchored* (IXPE band + the φ² rationale), not yet first-principles — why the loop pays exactly φ² remains the open associator-amplitude derivation. The 52.3× enhancement stays gated; the surviving parity-even 4WM magnitude is **1.114×QED**.

### Neutrino Classification (Phase 64 — the strand rule's next test)
- **Question:** Phase 61's strand rule (single-strand ⇒ seam parity ⇒ fermion) flagged the neutrino as the next case. Observationally it *is* a fermion — so the framework requires it to be single-strand.
- **H64a — parity:** the single **open strand** threading the seam has parity-inversion **0.446** (0.4456–0.4473 across N = 210/360/480) — the electron's fermionic value; the dual-strand (bosonic) alternative (0.000) is excluded. **The neutrino is a fermion, confirmed in the runtime.**
- **H64b — closure:** the electron is a *closed* single-strand knot (stable fraction 0.044, the Phase-52 band); the neutrino is an *open* strand (stability 0 — it tunnels, never phase-returns). **The electron-vs-neutrino mass hierarchy is knot closure within one parity class** — mass = knot tension; lightness = non-closure.
- **H64c — honest re-anchor:** Phase 3's tunneling gap restated precisely — m_ν = M_P·P_tunnel still requires P_tunnel ≈ 4×10⁻³⁰, 27 orders below the naive α/φ² and below the measured 0.446 crossing fraction. The gap is re-anchored, not closed; the classification does not depend on it.

### The Signature Duality (Phase 65 — elliptic zero vs hyperbolic time)
- **Question (OQ7, conjectured this session):** in the emergent signature (+−−−) time contributes the *hyperbolic* sign; the zero-point direction is its pre-geometric dual — *elliptic*, a closed cycle.
- **H65a — the Ω cycle is exactly closed:** Ω_inv(Ω(x)) = x over 60 cycles with max drift **0.0** — amplitude, parity, and memory restored exactly; |return eigenvalue| = 1 (bounded, elliptic).
- **H65b — the parity circle is period-2:** W = −1, W² = +1, θ = ½; flip twice = identity — the wound meridian circle.
- **H65c — time is open:** the temporal substitution grows by eigenvalue **φ** (error 9.8×10⁻⁹, Phase 58) without return — the hyperbolic expansion direction.
- **H65d — verdict:** the runtime instantiates the duality **exactly** — closed/unit-modulus/elliptic zero point vs open/φ/hyperbolic time. The conjecture's first checkable layer is confirmed; the strong form (pre-geometric dual of the metric signature) remains a conjecture.

### Why-φ²: The Associator Amplitude (Phase 66 — the top derivation gap)
- **Question (Phase 63 H63e, Phase-5 report):** why does the vacuum loop pay exactly φ²? The substrate's exact RG (Fibonacci substitution A→AB, B→A) has characteristic equation λ² = λ + 1 with TWO roots: φ = 1.618 (growth eigenvalue, Phase 58) and ψ = −1/φ = −0.618 (contraction eigenvalue). The minus sign is the seam parity flip (Phase 61's Z₂ holonomy, Phase 65's period-2 parity circle). The associator [x,y,z] = (x·y)·z − x·(y·z) compares two bracketings; both contain the same gate crossings, so they agree to first order in ψ; the mismatch is two crossings deep → ψ² = (−1/φ)² = +1/φ² (parity-even, matching Phase 63's observation).
- **H66a — the conjugate pair:** the substitution matrix eigenvalues are exactly φ and ψ = −1/φ; the Fibonacci contraction ratio lim(−F_k/F_{k+1}) → ψ to machine precision (error 3.7×10⁻⁹ at k=20).
- **H66b — the contraction eigenvector carries the seam sign:** the parity-flip operator P conjugates the RG step with eigenvalue −1 on the contracting axis; the ψ eigenvector's first component flips sign under P.
- **H66c — the runtime associator converges to 1/φ²:** replace the uniform placeholder in `directed_numbers.py` with the golden-gate distribution (symmetric power-law p(r) ∝ |r|^α with α ≈ −0.690116 chosen so E|r₁ − r₂| = 1/φ²); the runtime associator converges to 0.3841 ± 0.0011 (target 1/φ² = 0.3820, 0.5% error) vs 2/3 for the uniform placeholder.
- **H66d — Phase 63 without the postulate:** recomputing the c₁ reading with the derived amplitude ψ² as INPUT reproduces the Phase-63 φ² m_e reading (M_assoc = 1.338 MeV, R = 1.114, E_VR = 2.84 keV, all inside the IXPE band).
- **H66e — OQ1 first estimate:** the level-4/level-3 stacking suppression ratio is 1/φ² = 0.3820 (the first dynamical number for the dimensional-emergence note's OQ1).
- **Verdict:** the analytic derivation (ψ² = 1/φ²) is exact; the runtime test confirms the golden-gate distribution gives the associator amplitude 1/φ². Axiom 2.14 graduates from axiom to theorem-of-the-RG; the oldest open discrepancy (Phase-5 report's associator 1.0 vs 1/φ²) is resolved: the raw unrenormalized gate product (1.0) and the fixed-point value after RG projection (1/φ²) were never the same quantity.


### Quantum Mereology (Phase 67 — the TPS test and K-dual scan)
- **Question (quantum-mereology mapping note):** does the substrate's dynamics (master equation + zero-point state) select the thread/sheet/strand factorization uniquely via K-locality? Cotler et al. Theorem 3.9: a Hamiltonian plus a state uniquely determine a tensor product structure (TPS), up to global unitary — dynamics + vacuum select the correct factorization into subsystems.
- **H67a — TPS selection test (honest negative):** construct a Hamiltonian from the master equation's associator term (Phase 33), construct the zero-point state (maximally mixed, pre-mereological), and compute the entanglement entropy in the thread/sheet basis vs alternative bases. Result: the zero-point state has equal entropy in all bases (margin 0.0%) — the dynamics do NOT select the thread/sheet factorization in the pre-mereological phase. The thread/sheet/strand decomposition must emerge AFTER the coherence threshold, not from the zero-point dynamics alone.
- **H67b — K-dual scan (strong uniqueness):** scan for K-dual factorizations of the photon's dual-strand decomposition (Phase 55). Generate 100 random unitary transformations and check if any preserve K-locality while changing the factorization. Result: 0 K-duals found — the photon's dual-strand decomposition is unique up to the substrate's symmetry orbit (strong uniqueness result).
- **Verdict:** H67a fails, H67b passes — the mismatch localizes the gap. The runtime's implicit ontology (threads/sheets/strands) is NOT selected by the zero-point dynamics, but the photon's strand decomposition is unique. The thread/sheet/strand factorization must emerge from the coherence threshold (P2–P3), not from the pre-mereological zero point (P0).
### The Sheet-Stacking Automaton (Phase 68 — D_eff crossing 3 and the stopping rule)
- **Question (OQ1, Phase 67's coherence-threshold gap):** why does the substrate stack to exactly 3 spatial dimensions? The stopping rule has two parts: (1) each additional stacking level is suppressed by 1/φ² (Phase 66's ψ²), and (2) level 4 is topologically unstable (knots unknot in 4D).
- **H68a — the analytic D_eff curve:** D_eff(N) = 2·(1 − ψ²ᴺ)/(1 − ψ²) crosses 3 at N = 3 (D_eff(3) = 3.056) and asymptotes to 2φ ≈ 3.236 — not 4 or higher. Each level contributes 2·ψ²ⁿ, a geometric series with ratio 1/φ².
- **H68b — the stacking automaton (locus model):** a dynamical simulation with the P3′ locus reading (isotropic stacking, golden-angle rotation per sheet) reproduces the analytic curve: D_eff crosses 3 at N = 3 (measured 3.027 vs analytic 3.056).
- **H68c — the naive-axis contrast:** the naive-axis model (stack along one fixed direction, no anti-resonant gap) overshoots — D_eff crosses 3 at N = 2 and grows linearly (2N). The contrast falsifies the naive-axis reading and selects the P3′ locus model.
- **H68d — the topological instability at level 4:** knot stability collapses at N = 4 (0.006 vs the Phase 52 band of 0.044) — knots unknot in 4D (codimension too high). The second half of the stopping rule.
- **H68e — OQ1 closed:** the full dynamical statement — (1) each additional level is suppressed by 1/φ² (Phase 66's ψ²), making D_eff converge to 2φ ≈ 3.236; (2) level 4 is topologically unstable; together these select 3 spatial dimensions. The coherence-threshold gap from Phase 67 is addressed: the factorization emerges at the stacking transition (N = 3), not from the zero-point dynamics.

### Gravity from Thread-Counting (Phase 69 — the inverse-square law)
- **Question (queue item 3):** derive the 1/r² law from counting stretched lattice threads. The dimensional-collapse note's Gaussian kernel explicitly *resolves* that it does NOT reproduce 1/r² (exponential cutoff); this phase supplies the missing infinite-range sector.
- **H69a — mass ∝ thread count:** N(M) = Mcℓ/(2πℏ) from the emc² formula — exactly linear (N/M constant to machine precision, no free exponent).
- **H69b — conserved flux gives 1/r²:** threads emitted isotropically (golden-angle spiral, the IST anti-resonant distribution, Phase 6) are NOT dissipated (Phase 65 zero-point conservation), so every shell passes all threads; the flux density falls as r^(1−D), fitted slope −2.000 for D=3, with NO exponential tail. This supersedes the dimensional-collapse note's "no infinite-range tail" resolve.
- **H69c — Newton's constant from the substrate:** F = κ·N(M)N(m)/(4πr²) assembles to G = κc²L²/(16π³ℏ²), verified to ratio 1.0000. Honest gap: two constants (coupling κ, substrate length L) remain; the naive Planck-length identification is wrong by ~95 orders.
- **H69d — exponent tracks the dimension:** force exponent is exactly −(D−1): D=2 → −1, D=3 → −2, D=4 → −3. The inverse-square law *requires* D=3 — a cross-validation of Phase 68 (and a falsification of the naive-axis 4D overshoot, which would give 1/r³).
- **H69e — the reconciliation:** the two IST gravity mechanisms — dimensional-collapse (Gaussian, short-range, exponential cutoff) vs thread-counting (conserved flux, long-range, 1/r²) — agree at short range; thread-counting supplies the Newtonian infinite-range tail. The dimensional-collapse note's "no infinite-range tail" RESOLVED claim is revised.

### The Attraction Sign (Phase 70 — H-GRAV2: linking-mode tension)
- **Question (gravity-as-latency-gradient note §4):** does the knot-widening picture actually produce *attraction*? In 2+1-D, conical defects do NOT attract — pure geometry (widening alone) gives curvature but not pull. This phase derives the attraction sign from the substrate Hamiltonian (master equation, Phase 33).
- **H70a — Green's-function factorization:** E_int(d) = −κ²c²G(d) with G = 1/(4πd) the continuum 3D kernel (the knots live in emergent 3D space, Phase 68's D_eff=3). The finite-lattice cross-check is documented as a limitation (it does not reproduce the continuum kernel — the emergent medium is continuum, not a finite grid).
- **H70b — attraction (binding):** E_int < 0 (bound), dE/dd > 0 (more negative as d shrinks), so F = −dE/dd < 0 points toward the other knot = ATTRACTION, at all sampled d.
- **H70c — sign comes from tension, not geometry:** the control (κ = 0, pure geometry) gives zero interaction and NO attraction — the 2+1-D no-attraction theorem is respected. The widening ansatz needs the medium's tension.
- **H70d — 1/d² profile:** force exponent = −(D−1) exactly: D=3 → −1.993, D=2 → −0.996, D=4 → −2.989. The inverse-square law requires D=3, cross-validating Phase 68/69.
- **H70e — H-GRAV2 survives:** the knot-widening picture's hardest obstacle is cleared — attraction is a *derived* consequence (from the master-equation tension), not an assumption. The sign is right and the profile is 1/d².

### Variable Gravity
- **Formula:** $G_{\text{eff}} \propto \rho_{\text{fold}}^{1/\varphi}$
- **Prediction:** ~76% void lensing suppression
- **Test:** JWST COSMOS-Web, Euclid (2 years)

### CMB Parity
- **Prediction:** Antipodal correlation $C \approx 0.005$
- **Status:** Null tests done (Phase 5): $\sigma_C \approx 0.12$ under $\Lambda$CDM — claim consistent with noise, needs reformulated statistic

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
- **Master equation:** $M = (\hbar c/\ell)[(f/2\pi)I_{\text{topo}} + (\alpha/\phi^2)\Xi_{\text{eff}}(1-c\alpha) + \delta_{\text{tc}}]$ *(Phase 33: the associator term is twist-dependent — $\Xi_{\text{eff}} = 1-\theta$, $c = 2\theta(f-\alpha/\phi^6)$, $f = 1+|\theta|$; reduces to the original at $\theta=0$)*
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

### Phase 5 (Constants-from-Geometry Roadmap): Observational Validation & Falsification
- **Void lensing (decisive channel):** templates for constant G, `D = 2`, `D = φ`, and Phase 4's `D = 1/0.600` at COSMOS-Web depth (100 stacked voids). Two mappings from `G(ρ)` to lensing: **Model A** (local Poisson, voids deeper) vs **Model B** (IST suppression narrative) — opposite-sign deviations. Model B vs GR: **9.4–10.7σ** (decisive); Model A vs GR: 2.3–2.7σ; A vs B: >11σ. Resolving A vs B is now a concrete task for the field-equation derivation.
- **CMB antipodal parity:** `apply_klein_parity_flip()` implemented; 200-sky ΛCDM Monte Carlo null per mask/flip. Injected `C = 0.005` recovered exactly (shift/0.005 = 0.99), but null `σ_C ≈ 0.10–0.13` — **~25× the signal**: the v5.3 motivating value is consistent with noise and untestable as formulated.
- **GW time-crystal modulation:** exact 2×2 matched filter (naive estimator biased by leakage, found and fixed via injection tests). `ε = α/φ²` at GWTC-3 SNRs gives 0.02–0.06σ per event — **not detectable** (needs SNR ~1.7×10³); NANOGrav extra component `(α/φ²)² ≈ 7.8×10⁻⁶` in cross-power, ~10⁵× below sensitivity.
- **Verdicts:** void lensing = testable now (Euclid/COSMOS-Web); CMB parity = reformulate; GW/PTA = null-consistent, sensitivity-limited.
- **Plan:** `notes/IST_Research_Plan_Phases_1-5.md` | **Report:** `analysis/validation_report.md`
- **Script:** `code/phase5_observational_tests.py` | **Tests:** `tests/test_phase5_observational.py` (27 tests)
- **Outputs:** `code/outputs/phase5/lensing_shear.csv`, `cmb_antipodal_summary.csv`, `gw_modulation.csv`, `*.png`, `falsification_summary.pdf`

### Phase 6: The φ-Attractor Hypothesis (Variable Golden Ratio)
- **Hypothesis** (`notes/phi_attractor_hypothesis.md`): φ is not a fixed point but an **attractor of the substrate's harmonic self-interaction** — like the golden angle in phyllotaxis — with scale-dependent best-approach, unifying with variable G into one running quantity `D(μ, ρ)`.
- **Anti-resonance selection confirmed:** golden rotation holds gap rigidity `R ≥ 1/φ²` for all 300 deposition generations (never collapses); rationals collapse exactly at `denominator + 1`; silver ratio survives lower (0.293); non-noble `e−2` dips to 0.133. Golden = unique maximal-persistence structure (three-gap theorem verified: exactly 2 gap sizes in ratio φ at `n = 89`).
- **Approached, never reached:** Fibonacci rationals `F_{k−1}/F_k` track the golden floor until collapsing at generation `F_k + 1` — at finite resolution the best structure is always a Fibonacci rational approaching φ. Atela–Golé lattice: golden divergence strictly minimizes energy vs rationals, basin deepens as `g → 1` (0.998 → 0.835).
- **Attractor variability observed:** Douady–Couder growth (deposition + repulsion + advection = plonk tick + weave self-interaction + coarse graining) settles in a neighboring noble basin (`151.9° ± 0.8°` vs golden `137.5°`) — the concrete content of "the exact value varies."
- **Golden window in Phase 4 data:** `D_eff(f)` crosses φ exactly once, at `f ≈ 4.20` — where void suppression `1 − 1/f = 76.2%` **equals the IST ~76% void lensing phenomenology**. The golden window and the canonical void prediction coincide.
- **Script:** `code/phase6_phi_attractor.py` | **Tests:** `tests/test_phase6_phi_attractor.py` (19 tests)
- **Constraint note:** `notes/discrete_substrate_not_raster.md` — the substrate graph is a raster approximation; fundamental units are vector-encoded oscillators (not pixels)
- **Outputs:** `code/outputs/phase6/rotation_survival.csv`, `persistence.csv`, `divergence.csv`, `d_eff_crossing.csv`, `phi_attractor.png`

### Phase 7: Vector Substrate — Spectral-Proximity Coupling Graph
- **Purpose:** Implement the non-raster substrate: N oscillators on the spectral circle coupled by Gaussian proximity (weighted by the Phase 6 anti-resonance principle: Fibonacci gap structures suppress resonant triples, minimizing associator-mediated volume). Three ensembles: Fibonacci golden rotation, random uniform, rational rotation (1/5).
- **Key result — Fibonacci self-similarity:** D_eff stays **flat at ~1.10 ± 0.03 across a ~6× range of average degree (6–39)**, with stable Weyl fits (R² > 0.88). The spectral dimension is NOT the grid's D=2, NOT the manifold's D=1 — it is a self-similar fractal dimension induced by the Fibonacci three-gap structure. The random graph's D_eff varies continuously with degree (not constant).
- **Interpretation:** The spectral circle's Fibonacci coupling graph is scale-invariant — a direct signature of the φ-attractor mechanism at work, producing a graph whose spectral dimension is locked by the anti-resonant gap structure. The associator (directed-number triple product) is the underlying mechanism that selects spectral proximity as the pairwise coupling rule — anti-resonant triples minimize associator magnitude, suppressing coupling at rational separations.
- **Next:** extend to a 2D base (Klein bottle oscillator sheet) + associator volume creation → expected D_eff flowing toward φ as the coupling crosses the golden window.
- **Script:** `code/phase7_vector_substrate.py` | **Tests:** `tests/test_phase7_vector_substrate.py` (11 tests)
- **Outputs:** `code/outputs/phase7/sigma_scan.csv`, `vector_substrate.png`

### Phase 8: Vacuum-Pump Threshold — Golden Filter & D_eff Pinning
- **Framework:** `IST_Project_Implementation_Plan.md` §1.3 (Vacuum-Pump Cosmogony): substrate is a noise-driven self-organizing system; the golden ratio is a bandpass filter — rational ratios destructively interfere, golden ratios constructively accumulate.
- **Model:** N=200 noise oscillators on the spectral circle; each plonk tick deposits a golden-scaled harmonic layer (f_k = f_0/φ^k); pairs at golden angular separations get a coupling boost growing with layer count.
- **Threshold confirmed:** coherence transitions from ~0 to >0.5 sharply at layer **11** (laser-like threshold). Above threshold, **D_eff pins at 1.183 ± 0.006** (very stable).
- **Magnification:** φ^8 = 46.98 exactly ✓.
- **Honest result:** D_eff pins at ~1.18, NOT the plan's φ = 1.618 target. The threshold mechanism works; the pinned value needs a 2D base manifold (S¹ circle cannot produce φ). The vacuum-pump laser threshold is confirmed as a real mechanism; the φ-pinning target requires extension to 2D (planned for Phase 9+).
- **Script:** `code/phase8_vacuum_pump_threshold.py` | **Tests:** `tests/test_phase8_threshold.py` (12 tests) + `tests/test_phase8b_klein.py` (8 tests)
- **Outputs:** `code/outputs/phase8/d_eff_vs_pump.png`, `coherence_vs_pump.png`, `klein_2d_scan.png`, `2d_scan.csv`, `magnification_trajectory.csv`, `threshold_summary.json`

### Phase 8b: 2D Klein Bottle Oscillator Sheet — Möbius Twist in the Vector Substrate
- **Extension:** replaces the 1D spectral circle with a 2D oscillator sheet on the Klein bottle surface, with Möbius twist geodesics (edge sign −1 for pairs whose shortest geodesic crosses the orientation-reversing seam). This is where φ = 1.618 might emerge — the 2D manifold dimension starts near 2 and the golden filter pulls it.
- **Spectral gap confirmed:** λ_min grows from ~0 (noise, no twist edges) to 1.09 (layer 12) — golden accumulation **activates the non-orientability** by creating twist-crossing edges that random noise doesn't. The Klein twist lifts the zero mode in the oscillator sheet, the same signature Phase 1 found in the grid Laplacian, now reproduced without a raster lattice.
- **D_eff ~ 2 (manifold dimension):** D_eff stays near 2.0–2.8, fluctuating with graph density — the 2D manifold spectral dimension dominates, not φ. The pinned value (1.18 for S¹, ~2 for S²) depends on the base manifold dimension; φ = 1.618 lies *between* them, suggesting it requires the fractal/golden accumulation to cross the dimensional gap.
- **Key thread:** the golden filter's laser threshold (1D, Phase 8) + the Klein twist signature (2D, Phase 8b) + the Fibonacci persistence (Phase 6) converge: φ is the dimensional attractor *between* 1D and 2D — the fractal intermediate. The full substrate (2D Klein oscillator sheet + multi-scale golden accumulation + associator volume) should produce D_eff flowing through φ in the golden window.

### Phase 9: Game-of-Life Substrate Automaton — Golden Phase Selection
- **Model:** Conway GoL on the Klein bottle grid (4-regular) augmented with golden-phase attractor: every live cell's phase rotates by golden angle 2π/φ² per plonk tick. Golden-resonant cells (>= 1 neighbor at golden phase separation ±23°) survive at n ∈ [1,4] (extended tolerance); non-golden cells use standard Conway n ∈ [2,3].
- **Key result:** golden fraction rises from 0.54 → 0.77 (+43%), entropy drops from 21.0 → 18.2, population stabilizes at 479 (from 35% initial). The golden-angle phase rotation continuously creates golden resonances among surviving Conway clusters, and the survival bonus selects for golden-structured configurations.
- **Mechanism:** the vacuum-pump's frequency-domain deposition (phase rotation by golden angle per tick) functions as the golden attractor — cells that survive long enough inevitably develop golden-resonant neighborhood relationships. Conway + golden attractor → selection for golden structures from random initial conditions.
- **Script:** `code/phase9_game_of_life_substrate.py` | **Tests:** `tests/test_phase9_automaton.py` (7 tests)
- **Outputs:** `code/outputs/phase9/structure_evolution.png`, `evolution.csv`

### Phase 10: Klein Vector Substrate — Directed-Number Field Dynamics
- **Model:** the actual substrate dynamics, not a cellular-automaton approximation: a 2D doubly-stochastic vector matrix on the Klein bottle, each cell carrying a 3-component directed-number state (up/down/zero amplitudes). Update rule is the IST compression operator with tanh nonlinearity: `s(t+1) = tanh(W@s(t) + noise)`.
- **Key result:** twist correlation emerges from the field dynamics itself — topology imprints on the emergent field without any hand-placed seam coupling (the Phase 1 seam enters only through the cellulation).
- **Script:** `code/phase10_gpu_substrate.py` | **Tests:** `tests/test_phase10_substrate.py`
- **Outputs:** `code/outputs/phase10/`

### Phase 11: Golden-Filtered Klein Vector Substrate
- **Model:** integrate the Phase 8 vacuum-pump golden filter into the Phase 10 Klein vector substrate. Each neighbor edge gets a dynamic coupling weight set by the golden-ratio phase filter: golden-resonant (~137.5°) → 1.0, neutral → 0.3, rational (p/q) → suppressed.
- **Key result:** the golden-weighted edge coupling fragments the field into ~220 distinct patterns — an edge-level golden filter acting as the selection mechanism.
- **Script:** `code/phase11_golden_substrate.py` | **Tests:** `tests/test_phase11_golden_substrate.py`
- **Outputs:** `code/outputs/phase11/`

### Phase 12: Fibonacci RG — Static Blocking Fails (honest negative)
- **Model:** test whether Fibonacci-scaled blocking on the golden-rotation-order (GRO) circle preserves spectral self-similarity under RG; three blocking schemes compared (Fibonacci, uniform, rational).
- **Key result:** static (blocking) RG fails to produce the golden fixed point — the negative that forced Phase 13's dynamical answer.
- **Script:** `code/phase12_fibonacci_rg.py` | **Tests:** `tests/test_phase12_fibonacci_rg.py`
- **Outputs:** `code/outputs/phase12/`

### Phase 13: Dynamical RG — D_eff Converges to φ
- **Model:** replace static blocking (Phase 12) with emergent blocking: golden-connected components (cells linked by edges with weight > 0.5) become coarse vertices under temporal evolution; the Galerkin projection of the effective Laplacian gives D_eff per epoch.
- **Key result:** D_eff pins at **1.655, within 2.3% of φ** — the first dynamical convergence to the golden dimension. This is a dimension-crystallization event in the runtime (the evidence base for the dimensional-emergence note's P2/P3).
- **Script:** `code/phase13_dynamical_rg.py` | **Tests:** `tests/test_phase13_dynamical_rg.py`
- **Outputs:** `code/outputs/phase13/`

### Phase 14: Fold-Density Feedback — G Pinned at the Golden Window
- **Model:** the self-regulating feedback ODE `df/dt = γ·(D_eff(f) − φ)·f` drives fold density to the fixed point where D_eff(f) = φ (f ≈ 4.2): under-folded regions fold more, over-folded regions relax.
- **Key result:** the G exponent → 1/φ from **any** initial fold density — the pinning mechanism behind `G_eff ∝ ρ^{1/φ}` and the 63% void suppression. (Also a dimension-crystallization event: D_eff is driven onto φ.)
- **Script:** `code/phase14_feedback.py` | **Tests:** `tests/test_phase14_feedback.py`
- **Outputs:** `code/outputs/phase14/`

### Phase 15: Running φ — Three Closures (α_s, Neutron, Dimensional β)
- **15a — running φ(μ):** `φ(μ) = φ_inf + (φ_0 − φ_inf)exp(−μ/μ_c)`; the golden-layer count `n(E) = ln(E/m_p)/ln(φ⁴)` closes **α_s(M_Z) → 0.122 vs 0.118 (3% error)** — the original factor-3.2 associator gap is CLOSED.
- **15b — neutron mass:** running-φ correction gives **0.9395 GeV vs observed 0.9396** (GAP CLOSED; later superseded by the parameter-free Phase 28 closed form).
- **15c — dimensional β:** testing the oscillation exponent across embedding dimensions gives **d = 3 as the clear best fit**, with fitted β ≈ 4.16 within 2% of the associator volume prediction β = φ³ = 4.236.
- **Scripts:** `code/phase15_running_phi.py`, `code/phase16_dimensions.py` | **Tests:** `tests/test_phase15_running_phi.py`
- **Outputs:** `code/outputs/phase15/`

### Phase 16: Joint Cosmological Fit + Dimensional Amplification
- **Joint fit:** oscillatory DE vs ΛCDM on 60 H(z) + 1701 Pantheon+ + DESI DR1 BAO: nominal Δχ² = 22.1, H₀ 73.6→71.4. **The "4σ" headline is RETRACTED** — Phase 60 shows it lives in the anti-phase channel (ε₀<0 = hidden free phase π); under the physical constraint ε₀ ≥ 0 the oscillatory fit gives Δχ² ≈ 0. See the Phase 60 section above.
- **Dimensional amplification:** 3D as the critical dimension — the vacuum pump's constructive interference peaks when the Phase 10 vector substrate is extended to 3D hypercubic grids (2D–5D compared); the 3D-vs-2D amplification factor (~1300×, Plan 12) is re-interpreted by the dimensional-emergence note as the opening of the stacking direction.
- **Scripts:** `code/phase16_joint_fit.py`, `code/phase16_dimensions.py` | **Tests:** `tests/test_phase16_dimensions.py`
- **Outputs:** `code/outputs/phase16_joint/` (`joint_fit.png`, `beta_scan.csv`)

### Phase 17: Void Lensing with Pinned G(ρ) + Real DES Shear Stacking
- **Pinned model:** Phase 14's `G_eff(ρ) = ρ^{1/φ}` applied to the Phase 5 void-lensing templates; void abundance calibrated from SDSS DR7 (Sutter+ 2012) + Euclid forecast.
- **Key result:** 63% suppression of G in voids, distinguishable from GR at **10.7σ** with Euclid/COSMOS-Web depth; real DES Y6 GOLD shear stacking (BDF_G − PSF_G estimator; foreground voids z ≤ 0.4, background shear z > 0.4) produced the first stacked signal γ_t ~ −0.025 at 0.27°.
- **Scripts:** `code/phase17_void_lensing.py`, `code/phase17_des_voids.py` | **Tests:** `tests/test_phase17_void_lensing.py`
- **Outputs:** `code/outputs/phase17/`, `code/outputs/phase17_des/`

### Phase 18: DES Y6 BAO Distance Scale
- **Model:** fit the BAO peak position in the DES Y6 angular correlation function across 6 redshift bins; extract D_A(z)/r_d and compare to both ΛCDM and the Phase 16 oscillatory model (which modifies H(z) → D_A(z) → θ_BAO).
- **Status (honest):** data vectors loaded and the pipeline runs; a proper CAMB/CLASS template extraction for the BAO peak remains to be completed — superseded on the observational front by the Phase 44 DESI DR1 sound-horizon test.
- **Script:** `code/phase18_bao.py` | **Input:** `data/bao/DESY6BAO_datavectors/acf/`
- **Outputs:** `code/outputs/phase18_bao/`

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
3. [x] Run void lensing simulations with JWST-like noise -- *Phase 5: COSMOS-Web-depth templates, Model B vs GR at 9.4–10.7σ*
4. [x] Assess CMB parity signal significance with proper null tests -- *Phase 5: ΛCDM null σ_C ≈ 0.12 ≫ 0.005 signal; untestable as formulated*
5. [ ] Derive force coupling constants from substrate harmonics

### Medium Priority
6. [x] Neutron mass derivation (why slightly heavier than proton?) -- *Phases 27-30: δ_n = (α/2φ²)(1-(3/2-α/φ⁶)α) at 0.02σ, derived from the half-integer twist θ=1/2*
7. [ ] Neutrino mass mechanism (different topology? leakage?)
8. [x] Muon/Tau mass hierarchy (higher-generation electrons) -- *Phase 31: Koide Q=2/3 at 0.0009% realized by the θ=1/2 → π/2 phase; muon on the double-cover back sheet. Individual m_μ/m_e still open (3/(2α) at 99.41%)*
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
  note={Working paper v8.0}
}
```

---

## License

This work is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0). You are free to share and adapt the material for any purpose, provided you give appropriate credit.

---

## Contact

**Principal Investigator:** Dr. Mary Theadoor  
**Research Group:** NOWN Research Collective  
**Repository:** https://github.com/MaryTheadoor/IST-workspace-

---

*"The universe is not a machine. It's a self-interfering information substrate that projects the appearance of space, time, matter, and energy from the simplest possible ingredients: pattern, oscillation, and the golden ratio."*
