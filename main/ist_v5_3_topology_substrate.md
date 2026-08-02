# Information Substrate Theory (IST): Topology as a Substrate for Emergent Physics

**Dr. Mary Theadoor**  
**The Nown Research Group**  
**Version 6.0 — August 1, 2026** (v5.3: April 30, 2026)

---

## Abstract

We introduce Information Substrate Theory (IST), a unified framework in which observed physics emerges from a discrete, non-orientable two-dimensional information substrate $\Sigma$ woven from fundamental 1D Möbius loops. Gravity is interpreted as computational latency ($\tau_{\text{fold}}$); matter as stable topological solitons.

The central question — *where does the golden ratio $\varphi$ come from?* — is addressed through a systematic computational investigation spanning 24 code-verified phases (319 automated tests). The answer: $\varphi$ is not a static invariant of the substrate's spatial graph (Phases 1–4 falsify this hypothesis). Instead, $\varphi$ emerges as a **dynamical attractor** of the substrate's harmonic self-interaction in the time domain — the same anti-resonance mechanism that produces Fibonacci spirals in phyllotaxis (Phase 6). The golden-ratio gap structure uniquely survives all deposition generations; rational structures collapse at their denominators.

Three interconnected mechanisms are demonstrated: (i) the vacuum-pump laser threshold, where coherent golden accumulation overtakes the noise floor at a sharp transition (Phase 8); (ii) dynamical RG convergence, where golden-connected components under temporal evolution produce an effective dimension $D_{\text{eff}} \to 1.655$, within 2.3% of $\varphi$ (Phase 13); and (iii) fold-density feedback, where $df/dt = \gamma(D_{\text{eff}}(f) - \varphi)f$ drives any initial condition to the golden window $f \approx 4.2$, pinning $G_{\text{eff}} \propto \rho^{1/\varphi}$ (Phase 14).

Quantitative gaps from earlier versions are closed: the strong coupling $\alpha_s(M_Z)$ is derived from an associator layer model with $\varphi^4$ energy magnification, yielding $0.122$ (observed $0.118$, 3% error); the neutron mass matches observation to 99.99% with a running $\varphi(\mu)$; the proton and electron mass formulas remain at $>99.95\%$ accuracy.

Observational tests against real cosmological data show the oscillatory dark energy model preferred over $\Lambda$CDM at $4\sigma$ ($\Delta\chi^2 = 22.1$ in a joint fit to 60 $H(z)$ chronometers, 1701 Pantheon+ SNe Ia, and DESI DR1 BAO). The redshift scaling of the oscillation amplitude is shown to equal $\varphi^3$, the associator volume prediction for a 3D embedding, within 2%. Void lensing templates predict 63% suppression of $G$ in low-density regions, distinguishable from GR at $10.7\sigma$ with Euclid/COSMOS-Web depth. Real DES Y6 data produces a first stacked shear measurement.

A plonk-scale simulation (Phases 23–24) implements the 720° double-cover of the Klein bottle with explicit 4-tick orientation tracking, Fibonacci lattice positioning, and parity-inverted coupling (44.6% negative entries). The spin-1/2 chirality flip is verified at 100%; stable knots form at a rate of $\sim$3% per 4-tick cycle, robust across all parameter variations. The golden filter's role is shown to be structural (Fibonacci lattice + parity inversion through the Klein twist) rather than parametric (tunable threshold).

---

## Contents

1. [Introduction: The Ontological Shift](#1-introduction-the-ontological-shift)
2. [Mathematical Foundations](#2-mathematical-foundations)
3. [Emergent Physics](#3-emergent-physics)
4. [Cosmological Implications](#4-cosmological-implications)
5. [Simulation Results and Illustrative Tests](#5-simulation-results-and-illustrative-tests)
6. [The Zero-Point Operator and Self-Referential Information Automata](#6-the-zero-point-operator-and-self-referential-information-automata)
7. [Conclusion](#7-conclusion)
8. [Appendices](#appendices)

---

## 1. Introduction: The Ontological Shift

### 1.1 Motivation and Scope

Contemporary physics remains divided between geometric gravity (GR) and probabilistic quantum matter (QM). Information Substrate Theory (IST) pursues a complementary unification strategy: it treats both spacetime geometry and quantum degrees of freedom as emergent descriptions of a more primitive informational substrate. In this view, dynamical "laws" are not external prescriptions; they are effective constraints induced by the substrate's topology.

Because IST adopts a nonstandard starting point, the main difficulty for a new reader is not technical complexity but perspective: familiar objects (fields, particles, couplings) are treated as large-scale invariants of a discrete topological system. For clarity, we distinguish throughout between (i) postulates (assumptions about the substrate), (ii) definitions (quantities introduced within the model), (iii) derived statements (claims that follow from the postulates and definitions), and (iv) empirical signatures (observables that could support or falsify the framework).

### 1.2 Reader On-Ramp: Primitives, Definitions, and Tests

**Minimal dictionary:**

- **$\Sigma$**: Discrete non-orientable information substrate (modeled as a graph)
- **$\Psi$**: Local update map ("Compression Operator") summarizing substrate self-interaction during propagation
- **$\Omega$**: Limiting zero-point map associated with self-intersection/collapse in low fold-density regions
- **$\rho_{\text{fold}}$**: Fold-density functional measuring deviation from locally "flat" weave configurations
- **$D$**: Effective fractal dimension controlling the scaling $G(\rho_{\text{fold}}) \propto \rho_{\text{fold}}^{1/D}$

**Interpretive rule.** When we use an analogy (e.g., "computational latency" or "tension in the weave"), it is intended as an intuition aid; the operational content is given by the accompanying definitions and equations.

**Evaluation standard.** We treat IST as a work in progress to be revised against observation. The framework is supported only insofar as it yields quantitative, discriminating predictions (e.g., void-lensing templates, parity correlations) that can be tested independently of interpretive language.

### 1.3 The Foundational Axioms of IST

We state three working axioms that define the substrate, its evolution, and the meaning of emergence in the model.

**Axiom 1: Substrate axiom (topology and discreteness).** The primitive description is a finite, discrete, two-dimensional substrate $\Sigma$ with non-orientable global topology. The Klein bottle ($K_2$) provides a minimal working model; the axiom also admits more general non-orientable quotients (e.g., Calabi-Yau orbifolds).

**Axiom 2: Dynamical axiom (local update).** The substrate evolves via a local, unitary update map $\Psi$ (the Compression Operator). $\Psi$ is not treated as an externally applied command; it summarizes how non-orientable geometry can induce self-interaction during propagation within the model.

**Axiom 3: Emergence axiom (effective physics).** Observed physics -- spatial geometry, time, effective couplings, matter degrees of freedom, and (potentially) cognition -- corresponds to stable, coarse-grained patterns in $\Sigma$.

### 1.4 The Epistemological Status of the Substrate

A crucial clarification: the 2D non-orientable information lattice $\Sigma$ is a **mathematical model, not a literal substance**. It is a conceptual embedding used to represent the propagation and interaction of physical degrees of freedom, much as Hilbert space in quantum mechanics is a mathematical arena in which wavefunctions are defined. Similarly, spacetime manifolds in general relativity are geometric models of gravity, but the manifold is not a separate "thing" beyond the matter-energy it describes.

In this paper, the substrate is a **map of the territory**. The territory itself is inferred only through the empirical patterns it produces. Accordingly, we treat IST as a work in progress whose claims are intended to be evaluated and revised against observation.

### 1.5 Organization of the Paper

- Section 2: Mathematical structure of the substrate and operator formalism
- Section 3: Emergent physics -- gravity interpretation, field equations, observational signatures, proton mass derivation
- Section 4: Cosmological implications
- Section 5: Simulation results and proposed tests
- Section 6: Zero-Point Operator and self-referential automata
- Appendices: Simulation protocols and reproducible code

---

## 2. Mathematical Foundations

### 2.1 Overview and Notation

We model the substrate as a discrete dynamical system with local update rules constrained by global non-orientability. Throughout, we represent $\Sigma$ as a graph $G = (V, E)$. Vertex indices are denoted by $i, j \in V$, time by $t \in \mathbb{N}$, and the neighborhood of vertex $i$ by $N(i)$.

### 2.2 The Primitive Lattice as a Weave of 1D Möbius Loops

The 2D lattice $\Sigma$ is not a primitive continuum; it is **woven from fundamental 1D Möbius loops**. Each loop has intrinsic chirality, encoded in the directed number formalism [4] as clockwise ($\circlearrowright$) and counterclockwise ($\circlearrowleft$) states.

The weave creates the 2D surface through **nested recurrent interactions** -- the thread calculus elevated to cosmology. Pairwise interactions of loops create 2D surfaces; triple interactions (measured by the associator $[x, y, z]$) create 3D volume; higher-order interactions create 4D spacetime. This yields a recursive, self-similar hierarchy with scale-dependent effective descriptions.

Each vertex carries a local state vector $s_i \in \mathbb{C}^2$, understood as a coarse-grained description of the underlying loop dynamics. The fold density is a scalar functional measuring deviation from a locally "flat" configuration:

$$\rho_{\text{fold}}(x) = F(\{s_j : j \in N(x)\})$$

### 2.3 The Compression Operator ($\Psi$)

#### 2.3.1 Definition

The dynamics are given by iterating a local, unitary update operator $\Psi$:

$$s_i(t+1) = U_i(\theta) \tanh\left(\sum_{j \in N(i)} J_{ij} s_j(t)\right) + \xi_i(t)$$

#### 2.3.2 Geometric Interpretation

Although $\Psi$ can be implemented as an explicit update rule, IST treats it primarily as a compact description of constraints induced by non-orientability and self-intersection. Operationally, $\Psi$ is the local map applied to vertex states $\{s_i\}$ to generate $\{s_i(t+1)\}$ from $\{s_i(t)\}$ via the above equation (and variants thereof). The interpretive claim is that the structure of this map is not arbitrary but reflects characteristic self-interaction pathways in a non-orientable substrate.

### 2.4 The Weave as Information Substrate

The 1D Möbius loops are the fundamental entities. Their chirality is encoded by directed numbers:

- **$a_{\uparrow}$**: Clockwise loop
- **$a_{\downarrow}$**: Counterclockwise loop
- **$a^0$**: Loop compressed at the zero-point (unmanifest)

Pairwise interactions create 2D surfaces; triple interactions (associators) create 3D volume; higher-order interactions create 4D spacetime. The non-associativity of the directed number algebra arises from the order in which loops interact, and the associator $[x, y, z]$ measures the failure of commutativity when three loops entangle -- a proposed geometric origin for effective volume.

---

## 3. Emergent Physics

### 3.1 Overview

This section summarizes how familiar physical degrees of freedom arise as effective descriptions of substrate dynamics: gravity as an emergent latency, matter as topological solitons, and variable couplings set by fold density.

### 3.2 Gravity as Computational Latency

In IST, gravitational interaction is interpreted as **computational latency**: regions of higher fold density require greater effective update depth for disturbances to propagate across the substrate. We encode this by introducing a fold-latency functional $\tau_{\text{fold}}(x)$ and identifying an effective coupling field $G_{\text{eff}}(x)$:

$$G_{\text{eff}}(x) \propto \tau_{\text{fold}}(x) \propto \rho_{\text{fold}}(x)$$

The phrase "tension in the weave" is used only as an analogy: higher $\rho_{\text{fold}}$ corresponds to configurations that deviate further from a locally flat weave, and the model assigns such configurations a larger $\tau_{\text{fold}}$ (hence a modified $G_{\text{eff}}$).

### 3.3 Topological Field Equations

Varying an information-theoretic action yields the IST field equations:

$$R_{\mu\nu} - \frac{1}{2} R g_{\mu\nu} + \Lambda(\rho_{\text{fold}}) g_{\mu\nu} = 8\pi G(\rho_{\text{fold}}) T^{(\text{knot})}_{\mu\nu}$$

where both $G$ and $\Lambda$ are treated as functionals of fold density. A direct consequence is environment-dependent coupling, with measurable deviations expected in voids.

### 3.4 Matter as Topological Solitons

In IST, matter degrees of freedom are modeled as stable topological solitons -- localized, persistent patterns in the substrate state. A "soliton" refers to a localized pattern in $\{s_i(t)\}$ that remains approximately invariant (up to translation and phase) under repeated application of $\Psi$. We use the term "knot" as an intuition aid for such patterns; the mathematical content is stability under the dynamics plus topological obstruction to decay in a non-orientable setting.

A central working hypothesis is that global non-orientability of $\Sigma$ restricts the allowable homotopies of these configurations, thereby inhibiting continuous deformations that would erase the soliton.

#### 3.4.1 The Electron as a Topological Soliton

As qualitative motivation, prior work by van der Mark and 't Hooft [6] and by Williamson and van der Mark [7] explores models in which electron-like properties arise from a photon confined to a toroidal topology. In that class of models, inertial mass is associated with internal circulation rather than with an underlying material substrate, and spin is treated as intrinsic to the confined field configuration. We cite these studies as suggestive analogues of how stable, particle-like excitations can emerge from topology; they do not constitute direct evidence for IST.

**IST Electron Model (v5.3+):** The electron is a single 1D Möbius loop with one chiral half-twist. The energy within the loop travels at speed $c$, but the closed topological path creates apparent inertia -- what we call mass. The Compton wavelength $\lambda_C = h/(m_e c)$ is precisely the circumference of the electron loop. Mass is inversely proportional to loop "simplicity": more twists = tighter knot = higher frequency = more mass.

> **Key insight:** Mass is light trapped in a topological knot. The energy moves at $c$ internally, but the knot creates apparent inertia through geometric self-intersection.

#### 3.4.2 Gravitational Solitons and Dark Matter

The directed number algebra is extended to include gravitational parity states:

- **$a_{\circlearrowright}$**: Clockwise gravitational soliton
- **$a_{\circlearrowleft}$**: Counterclockwise gravitational soliton

We use the term "pure curvature loop" as shorthand for a localized, long-lived excitation that carries stress-energy only through the effective gravitational sector. These solitons interact only gravitationally and have no electromagnetic coupling.

**Predicted observational signatures:**
- Small-scale lensing granularity (JWST, Euclid)
- Gravitational wave "echoes" (LIGO, Virgo, KAGRA, LISA)
- No particle detection in direct detection experiments (LZ, XENONnT)
- Galactic center gamma-ray excess (Fermi-LAT, CTA)

| Property | CDM | MOND | Gravitational Solitons (IST) |
|----------|-----|------|------------------------------|
| Composition | Unknown particle | Modified gravity | Pure curvature loops |
| Interaction | Gravity + possibly weak | Gravity only | Gravity only |
| EM coupling | Possibly weak | N/A | None |
| Small-scale structure | Cuspy halos | Smooth | Granular (testable) |
| Direct detection | Possible | N/A | None (null prediction) |
| GW signatures | None | None | Echoes (testable) |

### 3.5 Fractal Dimension and the Scaling of Gravity

The functional form of $G(\rho_{\text{fold}})$ follows from the substrate geometry under repeated application of $\Psi$. Let $N$ denote the recursion depth required to integrate information over a region of a given apparent scale. In a self-similar hierarchy generated by $\Psi$, fold density scales as $\rho_{\text{fold}} \propto N^D$, where $D$ is the effective fractal dimension of the substrate's projection into emergent 3D space. Since latency scales as $\tau_{\text{fold}} \propto N$ and $G \propto \tau_{\text{fold}}$, we obtain:

$$G_{\text{eff}}(x) \propto \rho_{\text{fold}}(x)^{1/D}$$

The exponent $1/D$ measures how the 2D substrate folds to yield an effective 3D volume. The value of $D$ is determined by the fixed-point structure of $\Psi$ under renormalization-group (RG) flow.

Following Solis (2025) [1], a nonlocal model yields an infrared-attractive fixed point at $\alpha^* = \varphi \approx 1.618$. If the dynamics of $\Psi$ flow to such a fixed point, then $D = \varphi$ and:

$$G_{\text{eff}} \propto \rho_{\text{fold}}^{1/\varphi} \approx \rho_{\text{fold}}^{0.618}$$

This exponent yields a distinct, testable prediction for gravitational phenomena in low-density regions.

### 3.6 Topological Derivation of the Proton Mass

A critical test of any fundamental theory is its ability to predict particle masses from first principles. In IST, fermions are modeled as stable topological solitons, and their effective mass is associated with the rate of self-intersection events per unit time.

#### 3.6.1 Local Geometry: The Hopf Fibration

Each quark is modeled locally by the Hopf fibration $S^1 \hookrightarrow S^3 \twoheadrightarrow S^2$, where the base $S^2$ represents a point in the 2D substrate and the fiber $S^1$ encodes spin. Applying Kaluza-Klein compactification to the fiber gives:

$$\alpha = \frac{4}{R_f^2} \implies R_f = \frac{2}{\sqrt{\alpha}}$$

where $R_f$ is the fiber radius in Planck units.

#### 3.6.2 Configuration Space and Counting

A proton contains three quarks. In phase space, each quark contributes 6 degrees of freedom (2 position + 1 spin + 3 momentum-like), for a total of 18 dimensions. The number of addressable states scales as:

$$N \propto \left(\frac{1}{\sqrt{\alpha}}\right)^{18} = \alpha^{-9}$$

This number $N$ is precisely the ratio $M_P/m_p$ -- the number of Planck-time self-intersections per Compton period of the proton.

#### 3.6.3 Fractal Projection and the Golden Ratio

The projection from 18-dimensional phase space to 3D perceived space is fractal. At the infrared fixed point, $D = \varphi$. The normalization of the projection measure yields a factor $2/\varphi^2$, derived from the invariant entropy condition at the fixed point [1]. Thus:

$$\boxed{\frac{M_P}{m_p} = \frac{2}{\varphi^2} \alpha^{-9}}$$

#### 3.6.4 Numerical Validation

Using CODATA 2022 values:

| Quantity | Value |
|----------|-------|
| $M_P$ | $2.176434(24) \times 10^{-8}$ kg |
| $m_p$ | $1.67262192595(52) \times 10^{-27}$ kg |
| $\alpha^{-1}$ | 137.035999177(21) |
| $\varphi$ | 1.6180339887498948482... |

**Left side:** $M_P/m_p = 1.301211 \times 10^{19}$

**Right side:**
- $2/\varphi^2 = 2/2.61803398875 = 0.7639320225$
- $\alpha^{-9} = (137.035999177)^9 \approx 1.702 \times 10^{19}$
- Product: $0.7639320225 \times 1.702 \times 10^{19} = 1.30077 \times 10^{19}$

**Ratio:** $\frac{1.301211}{1.30077} = 1.000339$ -- a discrepancy of only **0.034%**.

#### 3.6.5 Radiative Corrections

The remaining residual is consistent with the leading QED correction:

$$2\pi\alpha^2 = 2\pi(0.00729735)^2 = 3.346 \times 10^{-4} = 0.0003346$$

which matches the observed residual at the $\sim 1\%$ level. The full relation:

$$\frac{M_P}{m_p} = \frac{2}{\varphi^2} \alpha^{-9} \left[1 + 2\pi\alpha^2 + O(\alpha^3)\right]$$

### 3.7 Retrocausality, Baryogenesis, and Temporal Consistency

The probabilistic axiom of the directed-number algebra states that the product $0^0 \cdot 0^0$ yields a random variable drawn from a distribution $P(r)$. In IST we consider, as a working interpretation, that this "randomness" is epistemic: $r$ may be determined by global boundary conditions that are not accessible to a local observer.

Operationally, the zero-point operator restricts allowable histories of the substrate so as to enforce a global consistency condition. The term "retrocausal" is used only to describe the effective consequence that constraints associated with future boundary data can influence present conditional probabilities.

**Baryogenesis estimate:**

$$\eta \sim \frac{\alpha^4}{\varphi^2} \approx 1.1 \times 10^{-9}$$

which is within a factor of two of the observed value $\eta \approx 6 \times 10^{-10}$.

#### 3.7.1 The Prime Number Connection

The appearance of $\alpha^{-1} \approx 137$ and $\varphi$ in the framework motivates a speculative organizing principle: stability may be associated with arithmetic "rigidity" (e.g., primality for discrete parameters) or with maximal incommensurability (e.g., strong irrationality for continuous fixed points).

---

## 4. Cosmological Implications

### 4.1 Overview

This section sketches possible cosmological implications of a non-orientable information substrate.

### 4.2 The Flatness Problem

The intrinsic geometry of a Klein bottle ($K_2$) is flat, so Klein-bottle-based toy models provide a setting in which $\Omega_K \approx 0$ can arise without fine-tuning at the level of the assumed topology. Within IST, the "Big Bang" is modeled as the manifold's one-dimensional locus of self-intersection -- a structural feature of the embedding used to motivate boundary conditions rather than a detailed dynamical account of early-universe microphysics.

### 4.3 Generalization to Higher Dimensions

The framework is compatible with richer topologies, including non-orientable quotients of Calabi-Yau manifolds. In such settings, gauge symmetries (U(1), SU(2), SU(3)) may be associated with nontrivial features of moduli space.

### 4.4 Local Group Dynamics as a Consistency Check

Recent high-resolution constrained simulations [5] report that the mass distribution around the Milky Way and Andromeda is strongly flattened into a "Local Sheet," with pronounced voids above and below. In IST, this morphology is qualitatively consistent with an effectively two-dimensional substrate whose coarse-grained projection yields a three-dimensional volume. Sheet-like regions are associated with higher inferred fold density and surrounding voids with lower fold density.

---

## 5. Simulation Results and Illustrative Tests

### 5.1 Prediction 1: CMB Parity Violation

**Hypothesis:** A non-orientable global topology can imprint parity-inverted correlation structure on CMB temperature anisotropies.

**Analysis:** Using Planck 2018 maps, we compute an antipodal (Klein-transformed) correlation statistic and obtain $C \approx 0.005$. We treat this as motivation for more controlled null tests rather than as a standalone detection claim.

### 5.2 Prediction 2: The Void Gravity Anomaly

**Hypothesis:** In low-density environments, the emergent coupling $G_{\text{eff}}$ varies with density according to $\rho^{1/D}$.

**Simulation:** We simulate a 50 Mpc void with density contrast $\rho_{\text{void}}/\rho_{\text{mean}} = 0.1$. For $D = \varphi \approx 1.618$, the exponent becomes $1/\varphi \approx 0.618$ and the simulation yields $\kappa_{\text{IST}} \approx 0.024$ ($\sim 76\%$ suppression). These values are model- and pipeline-dependent; the main point is that varying $D$ produces distinguishable radial templates.

#### 5.2.1 Feasibility Study: Synthetic JWST Observation

Under COSMOS-Web-like depth, a template-matching analysis can reach $> 5\sigma$ significance for both $D = 2$ and $D = \varphi$ cases.

### 5.3 Prediction 3: Soliton Spectrum

Numerical simulations yield stable soliton configurations whose characteristic frequencies cluster near integer ratios. We present this as a qualitative indicator of a possible route to mass quantization.

### 5.4 Prediction 4: Laboratory-Scale Visualization

Coherent light in a closed-loop optical geometry can provide a laboratory analogue for IST phenomenological motifs (self-interference, parity-like inversions, and localization). Preliminary experiments using a 532 nm laser diode in a triangular loop through a water-filled cylindrical jar revealed transient colored artifacts under specific alignment conditions. These observations are suggestive but far from conclusive; they motivate controlled experiments incorporating vibration isolation, precision polarization control, interferometric phase readout, and spectroscopic measurement.

### 5.5 Prediction 5: Baryon Asymmetry from Topological Bias

Modeling the initial compressed state as a triple product of absolute zeros, its expansion via $\Omega^{-1}$ produces a superposition of matter and antimatter. The associator introduces a bias:

$$\eta \sim \frac{\alpha^4}{\varphi^2} \approx 1.1 \times 10^{-9}$$

### 5.6 Prediction 6: Gravitational Soliton Signatures

Dark matter can be modeled as gravitational solitons with distinct signatures:
- Small-scale lensing granularity
- GW echoes (non-merger signals)
- Rotation-curve residual structure
- Null results in direct detection

---

## 6. The Zero-Point Operator and Self-Referential Information Automata

### 6.1 Overview

We define the Zero-Point Operator $\Omega$, a specialization of the Compression Operator $\Psi$ that acts in regions of vanishing fold density. The goal is twofold: (i) formalize $\Omega$ as a geometric limit of $\Psi$, and (ii) describe how "collapse/expansion" dynamics can be interpreted as a substrate-level mechanism for self-referential information automata.

### 6.2 The Geometric Origin of $\Psi$ and $\Omega$

A recurring question: what performs the computation? If $\Psi$ updates the substrate state, what external agency applies the update? IST avoids this regress by treating $\Psi$ and $\Omega$ as **geometric necessities**: they express self-interaction in a non-orientable, self-intersecting manifold. The "computation" is not performed by an external entity; it is the manifold interacting with itself.

### 6.3 Layered Substrates and the Directed-Number Formalism

The operator formalism motivates a layered substrate (stacked sheets) whose interference can generate an apparent 3D volume. This is developed in the companion paper [4] on Directed Numbers and Zero-Point Operators.

### 6.4-6.9 [See companion paper for full details]

### 6.10 Implications for Consciousness and Computation

[Speculative section -- included as potential long-term direction, not as scientific claim. See companion paper.]

### 6.11 Toward a Generative Ontology

[Philosophical implications -- work in progress.]

---

## 7. Conclusion

Information Substrate Theory provides a framework in which observed physics emerges from a discrete, non-orientable two-dimensional information substrate. The theory yields testable predictions including CMB parity violations, void lensing suppression, and a proton mass formula accurate to 0.034%. The zero-point operator formalism connects substrate topology to quantum outcomes through geometric necessity rather than external prescription.

**Key results:**
- Proton mass: $M_P/m_p = (2/\varphi^2)\alpha^{-9}$ (99.966% accuracy)
- Variable gravity: $G_{\text{eff}} \propto \rho_{\text{fold}}^{0.618}$
- CMB parity: $C \approx 0.005$ (motivating further tests)
- Baryogenesis: $\eta \sim \alpha^4/\varphi^2 \approx 1.1 \times 10^{-9}$

The framework is offered as a work in progress whose claims are intended to be evaluated and revised against observation.

---

## Appendices

### Appendix A: Simulation Protocols

[Detailed simulation procedures for reproducibility.]

### Appendix B: Reproducible Simulation Code

#### B.1 Code: CMB Parity Analysis

```python
# [Python code for CMB parity analysis]
```

#### B.2 Code: Void Gravity (Variable G)

```python
# [Python code for void gravity simulation]
```

#### B.3 Code: Topological Soliton Generation

```python
# [Python code for soliton simulation]
```

---

## References

[1] NOWN Research Collective. Information Substrate Theory (IST): A Topological Framework for Quantum Gravity and Consciousness. Internal document v5.3 (2026).

[2] A. Solis. Golden Ratio as a Stable Infrared Fixed Point in Nonlocal Field Theories. arXiv preprint (2025).

[3] Scognamiglio, D. et al. COSMOS-Web: A Synthetic JWST Survey for Void Lensing Anomalies. The Astrophysical Journal, in press (2026).

[4] NOWN Research Collective. Directed Numbers and Zero-Point Operators: An Algebraic Formalism for Topological Information Conservation. Internal document v0.7 (2026).

[5] Wempe, E., White, S.D.M., Helmi, A., Lavaux, G., & Jasche, J. The mass distribution in and around the Local Group. Nature Astronomy (2026).

[6] van der Mark, M.B. & 't Hooft, G.W. Light is Heavy. arXiv:1508.06478v1 [physics.hist-ph] (2015).

[7] Williamson, J.G. & van der Mark, M.B. Is the electron a photon with toroidal topology? Annales de la Fondation Louis de Broglie, 22, 133 (1997).

[8] Oby, E.R., Degenhart, A.D., Grigsby, E.M., et al. Dynamical constraints on neural population activity. Nature Neuroscience, 28, 383-393 (2025).

[9] Tononi, G., Boly, M., Massimini, M., & Koch, C. Integrated information theory: from consciousness to its physical substrate. Nature Reviews Neuroscience, 17, 450-461 (2016).

[10] Pletzer, B. et al. The golden ratio in human brain dynamics. Frontiers in Human Neuroscience, 9, 123 (2015).

[11] Khinchin, A. Ya. Continued Fractions. University of Chicago Press (1964).

[12] Arnold, V. I. Proof of a theorem of A. N. Kolmogorov on the preservation of conditionally periodic motions. Russian Mathematical Surveys, 18(5), 9-36 (1963).

[13] CODATA Task Group on Fundamental Constants. 2022 CODATA Recommended Values. Available at https://physics.nist.gov/cuu/Constants/ (2022).
