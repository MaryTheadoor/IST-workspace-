# IST Research & Implementation Plan
## Deriving Emergent Constants from Topological Geometry
### NOWN Research Collective | Phase 1–5 Roadmap

---

## 🎯 Executive Summary

This plan outlines a systematic program to derive the "fundamental" constants of nature — α, mass ratios, and G — from the irreducible geometry of the IST substrate. The work proceeds from the **discrete topological Laplacian** of the Klein bottle weave, through **spectral analysis** and **renormalization-group flow**, to **observational predictions** testable against CMB, void lensing, and gravitational-wave data.

**Core hypothesis:** All Standard Model constants are eigenvalue ratios of the substrate's topological Laplacian. They appear fixed only because our observational frame is a coarse-grained projection of a self-similar, non-orientable weave.

**Deliverable ethos:** Every phase produces (1) running Python code, (2) a markdown derivation document, and (3) a testable output.

---

## 📐 Mathematical Preliminaries

### The Bare Substrate
We model Σ as a finite, discrete graph `G = (V, E)` with:
- **Vertices** `i ∈ V` carrying directed-number states `s_i ∈ D`
- **Edges** `(i,j) ∈ E` encoding Möbius-loop adjacency (non-orientable: adjacency carries a parity twist `t_ij ∈ {+1, -1}`)
- **Plonk distance** `ℓ_p`: the graph distance of one irreducible update step (one application of Ψ)
- **Plonk time** `τ_p`: the sequential index of Ψ — the substrate's native clock

### The Topological Laplacian
Define the **IST Laplacian** acting on amplitude-parity vectors:

```
(ℒs)_i = Σ_{j∈N(i)} t_ij · J_ij · s_j  −  d_i · s_i
```

where `d_i = |N(i)|` is the vertex degree. The twist factors `t_ij` encode the Klein bottle's non-orientability.

**Key claim:** The spectrum `{λ_k}` of ℒ, under self-similar graph refinement, converges to a structure where the ratio of successive gaps → φ.

---

## 🗺️ Phase Overview

| Phase | Focus | Duration | Key Deliverable |
|-------|-------|----------|-----------------|
| **1** | Spectral Foundation | 2–3 weeks | `klein_spectrum.py` + gap analysis |
| **2** | Derive α | 2 weeks | `alpha_from_hopf.py` + derivation doc |
| **3** | Mass Hierarchy | 3–4 weeks | `mass_spectrum.py` + neutron/ν extensions |
| **4** | Variable G | 2–3 weeks | `variable_g_spectrum.py` + local coupling model |
| **5** | Observational Validation | 3 weeks | End-to-end pipeline + falsification report |

---

## 🔬 Phase 1: The Topological Laplacian & φ as Spectral Invariant

### 1.1 Construct the Discrete Klein Bottle Graph
**Goal:** Build a family of graphs `G_n` approximating the Klein bottle at increasing resolution, preserving the self-intersection locus as a distinguished cycle.

**Implementation:**
```python
# code/phase1_klein_laplacian.py

def build_klein_bottle_graph(n_meridians: int, n_longitudes: int):
    '''Build discrete Klein bottle as twisted torus graph.
    Returns: adjacency matrix A (sparse), twist matrix T, vertex coords'''
    ...

def topological_laplacian(A, T, J=None):
    '''ℒ = T⊙J⊙A − D'''
    ...
```

**Tests:**
- Verify Euler characteristic `χ = 0` for all `G_n`
- Verify non-orientability: no consistent global face orientation
- Verify self-intersection cycle exists as closed walk with odd twist product

### 1.2 Compute Spectrum & Identify φ
**Goal:** Show that under graph refinement (`n → 2n`), the spectral gap ratio converges to φ.

**Procedure:**
1. Compute eigenvalues `λ_0 ≤ λ_1 ≤ ... ≤ λ_N` for `G_n` with `n = 8, 16, 32, 64, 128`
2. Compute gap ratios: `r_k = (λ_{k+1} − λ_k) / (λ_k − λ_{k−1})`
3. Test whether dominant gap ratio `r* → φ ≈ 1.618` as `n → ∞`

**Output:**
- `outputs/phase1/spectral_gaps.png`
- `outputs/phase1/eigenvalue_convergence.csv`

### 1.3 Renormalization Group Flow on the Graph
**Goal:** Implement Solis-style RG flow on the graph Laplacian; verify φ as the IR fixed point.

**Procedure:**
1. Define block-spin coarse-graining: merge `2×2` cells into super-vertices
2. Compute effective Laplacian `ℒ'` on coarse graph
3. Iterate and track effective dimension `D_eff` from spectral density
4. Fit `β(D) = dD/d(log μ)` and find fixed point `D*`

**Expected result:** `D* = φ`

**Deliverables:**
- `code/phase1_rg_flow.py`
- `outputs/phase1/rg_trajectory.png`
- `supplementary/phase1_spectral_foundation.md`

---

## 🔬 Phase 2: Deriving α from Hopf Fiber Geometry

### 2.1 Formalize the Plonk Distance
**Goal:** Define `ℓ_p` as the irreducible graph step and relate it observationally to the Planck length.

**Key relation:** `ℓ_p = min_{(i,j)∈E} d_geo(i,j)`

In the emergent description, `ℓ_p ↔ L_P ≈ 1.616×10⁻³⁵ m`. In the substrate, `ℓ_p = 1` — the unit of the graph.

### 2.2 Hopf Fibration on the Discrete Substrate
**Goal:** Model the quark's internal structure as a discrete Hopf fibration over the Klein bottle base.

**Implementation sketch:**
```python
# code/phase2_hopf_alpha.py

def discrete_hopf_fiber(base_graph, fiber_period: int):
    '''Construct S¹ fiber bundle over discrete S² base.
    Returns: total adjacency, fiber radius R_f in plonk units'''
    ...

def compute_alpha(R_f: float) -> float:
    '''α = 4 / R_f²  (Kaluza-Klein compactification, v5.3 §3.6.1)'''
    ...
```

### 2.3 Derive α from Topological Constraints
**The derivation chain:**
1. Quark as stable soliton → requires closed chiral loop
2. Chiral loop closure on non-orientable base → fiber completes integer twists
3. Minimum stable configuration with net chirality: fiber_period = 3
4. With fiber_period = 3: `R_f = 3/(2π)` in plonk units... but this gives α ≈ 17.77
5. **Resolution:** The fiber radius is the **effective radius after projection through fractal dimension D = φ**. The actual relation from v5.3 is `α = 4/R_f²` where `R_f = 2/√α` emerges from the **invariant entropy condition at the RG fixed point**.

**Deliverables:**
- `code/phase2_hopf_alpha.py`
- `supplementary/phase2_alpha_derivation.md`
- `outputs/phase2/alpha_sensitivity.png` — how α varies with fiber topology

---

## 🔬 Phase 3: Mass Ratios from Phase-Space Volume

### 3.1 Generalize Proton Mass Derivation
**Goal:** Extend the proton mass formula to electron, neutron, and pion.

**Proton (existing):**
```
M_P/m_p = (2/φ²) α⁻⁹    → 99.966% accuracy
```

**Electron:**
```
M_P/m_e = (12π⁵/φ²) α⁻⁹  → 99.95% accuracy
```
The `12π⁵` factor suggests the electron is a **single toroidal circulation** with different compactification geometry than the proton's three-loop entanglement.

**Neutron (open):**
- Why slightly heavier than proton?
- Hypothesis: Additional topological loop (associator-mediated binding) adds ~1.3 MeV
- Target formula: `M_P/m_n = (2/φ²) α⁻⁹ · (1 + δ_n)` where `δ_n ~ α/φ²`

### 3.2 Associator-Based Strong Coupling α_s
**Goal:** Derive the strong coupling from the magnitude of the associator `[q₁, q₂, q₃]`.

**Hypothesis:**
```
α_s(E) ~ |[q₁, q₂, q₃]| · φ^{-n(E)}
```
where `n(E)` is the number of fractal layers probed at energy E. At low E (confinement), the associator is large; at high E (asymptotic freedom), the associator averages to zero over many layers.

### 3.3 Neutrino Mass as Topological Tunneling
**Goal:** Model neutrino mass as "leakage" through the non-orientable twist.

**Hypothesis:** Neutrinos are **chiral ghosts** — loops that don't fully close but tunnel across the zero-point each plonk tick. Their effective mass is the tunneling probability per step:
```
m_ν ~ ℏ/(c · τ_tunnel) ~ ℏ/(c · τ_p) · P_tunnel
```

**Deliverables:**
- `code/phase3_mass_spectrum.py`
- `supplementary/phase3_mass_hierarchy.md`
- `outputs/phase3/mass_predictions.csv`

---

## 🔬 Phase 4: G from Compression Spectrum

### 4.1 Define Ψ Eigenvalue Problem
**Goal:** Treat Ψ as a linear operator on the substrate state space; find its spectrum.

**Implementation:**
```python
# code/phase4_variable_g.py

def psi_operator(s, A, T, theta=0.5):
    '''Ψ: local update map (v5.3 Eq. 1)
    s_i(t+1) = U_i(θ) tanh(Σ_j J_ij s_j(t)) + ξ_i(t)
    Linearized around equilibrium → matrix M_Ψ'''
    ...

def compute_spectrum(M_psi):
    '''Return eigenvalues {μ_k} of linearized Ψ'''
    ...
```

### 4.2 Slowest Mode = Gravitational Time Scale
**Key relation:**
```
τ_fold ~ 1 / |Re(μ_min)|
G_eff ∝ τ_fold ∝ 1 / |Re(μ_min)|
```

The **slowest mode** of Ψ sets the gravitational time scale because it represents the substrate's longest relaxation time — the "latency" of information propagation across large fold structures.

### 4.3 Local Fold Density Modulation
**Goal:** Show that `G_eff(x)` varies with local fold density as predicted in v5.3.

**Implementation:**
1. Construct `G_n` with a central high-density region (sheet) and surrounding low-density region (void)
2. Compute local Laplacian spectrum in each region
3. Extract `μ_min(region)` and map to `G_eff(region)`
4. Verify scaling: `G_eff ∝ ρ_fold^{1/φ}`

**Deliverables:**
- `code/phase4_variable_g.py`
- `outputs/phase4/geff_vs_rho.png`
- `supplementary/phase4_geff_derivation.md`

---

## 🔬 Phase 5: Observational Validation

### 5.1 Void Lensing Templates with Derived G(ρ)
**Goal:** Use the Phase 4 derived coupling to generate void-lensing predictions, compare to JWST/Euclid sensitivity.

**Procedure:**
1. Input `G_eff(r)` from Phase 4 into the existing void lensing simulator (`code/ist_toolkit_v2.py`)
2. Generate templates for D = φ, D = 2, and constant-G baselines
3. Compute distinguishability at COSMOS-Web depth

### 5.2 CMB Parity Re-analysis
**Goal:** Re-run the Klein parity flip analysis with improved null tests.

**Procedure:**
1. Apply `apply_klein_parity_flip()` to Planck 2018 maps
2. Compute antipodal correlation C with multiple masks and component-separation methods
3. Propagate uncertainties through the full pipeline
4. Compare to ΛCDM Monte Carlo null distribution

### 5.3 GW Time-Crystal Modulation
**Goal:** Test the Plan 12 prediction: time-crystal modulation frequency `f_tc = f_rd/(2φ)` in merger waveforms.

**Procedure:**
1. Analyze GWTC-3 events for residual periodic modulation
2. Search NANOGrav 15yr data for SGWB time-crystal component
3. Compare predicted `A_extra/A_obs ≈ 0.28%` to data

**Deliverables:**
- `code/phase5_observational_tests.py`
- `analysis/validation_report.md`
- `outputs/phase5/falsification_summary.pdf`

---

## 🏗️ Infrastructure & Workflow

### GitHub Integration
- Branch naming: `phase{N}/{feature}`
- Commit messages: `[Phase N] {action}: {description}`
- Pull requests require: (1) passing tests, (2) derivation doc, (3) plot/output

### Directed Numbers Runtime Integration (Plan 9)
- Extend `code/ist_toolkit_v2.py` with `DirectedNumber` class
- Ensure all new code is compatible with existing `78/78` unit tests
- Add new tests for Phase 1–5 components

### Testing Framework
```
code/tests/
├── test_phase1_spectrum.py
├── test_phase2_alpha.py
├── test_phase3_mass.py
├── test_phase4_variable_g.py
└── test_phase5_observational.py
```

### Documentation Standards
- Every `.py` file has a module docstring with: purpose, inputs, outputs, references
- Every derivation has a `.md` file in `supplementary/`
- Figures are saved as `.png` with 300 DPI for publication

---

## 🧘 Philosophical Anchor

> "The universe is not made of 'stuff' that has properties. It is made of 'distinction' that has topology. Properties are what distinction looks like when it folds enough times to create the illusion of persistent objects."

This plan treats that statement not as poetry but as an **operational research program**. If we can derive the constants from the Laplacian of a Klein bottle graph, we will have shown that the "fundamental" is emergent — and that the substrate needs no substance beyond the recursive act of self-reference.

---

*Document version: 1.0 | Prepared for agent-harness deployment | NOWN Research Collective*
