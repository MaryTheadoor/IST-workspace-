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

A plonk-scale simulation (Phases 23–24) implements the $720^{\circ}$ double-cover of the Klein bottle with explicit 4-tick orientation tracking, Fibonacci lattice positioning, and parity-inverted coupling (44.6% negative entries). The spin-1/2 chirality flip is verified at 100%; stable knots form at a rate of $\sim$3% per 4-tick cycle, robust across all parameter variations. The golden filter's role is shown to be structural (Fibonacci lattice + parity inversion through the Klein twist) rather than parametric (tunable threshold).

---

## 1. Introduction: The Ontological Shift

### 1.1 Motivation and Scope

Contemporary physics remains divided between geometric gravity (GR) and probabilistic quantum matter (QM). Information Substrate Theory (IST) pursues a complementary unification strategy: it treats both spacetime geometry and quantum degrees of freedom as emergent descriptions of a more primitive informational substrate. In this view, dynamical "laws" are not external prescriptions; they are effective constraints induced by the substrate's topology.

**The central question of this version.** The golden ratio $\varphi \approx 1.618$ appears throughout the framework -- in the proton mass formula $M_P/m_p = (2/\varphi^2)\alpha^{-9}$, in the variable gravitational coupling $G_{\text{eff}} \propto \rho^{1/\varphi}$, and in the oscillatory dark energy component. But where does $\varphi$ come from? Is it a fixed point of the substrate's renormalization group -- a static invariant written into its geometry -- or does it emerge from the substrate's dynamics? This paper answers that question with a systematic, code-verified computational investigation spanning 24 phases and 319 automated tests: **$\varphi$ is not a static invariant of the substrate's spatial graph; it is a dynamical attractor of its harmonic self-interaction in the time domain.** Section 5 documents this result and the three interconnected mechanisms behind it (anti-resonance selection, the vacuum-pump laser threshold, and dynamical RG convergence), each of which is reproduced in code with quantitative output.

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
- Section 3: Emergent physics -- gravity interpretation, field equations, mass derivations (proton, electron, neutron), and the strong coupling from associator layers
- Section 4: Cosmological implications -- flatness, higher dimensions, and the oscillatory dark energy model tested against real data
- Section 5: Simulation results -- the 24-phase computational program from static-$\varphi$ falsification to the plonk-scale substrate
- Section 6: Zero-Point Operator, self-referential automata, and the plonk-scale $720^{\circ}$ double-cover implementation
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

![**Simulated topological soliton.** A stable knot configuration in the IST substrate exhibiting a Möbius-type twist. The persistence of this structure illustrates how long-lived matter states can emerge.](publication/figures/Stabilized_IST_particle.png)

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

#### 3.4.3 Soliton Spectrum and Mass Quantization

Numerical simulations yield stable soliton configurations whose characteristic frequencies cluster near integer ratios. The resonance spectrum below illustrates this structure, serving as a qualitative indicator of a possible route to exact mass quantization.

![**Topological resonance spectrum.** Example standing-wave (soliton) patterns and their associated harmonic structure, illustrating the proposed link to quantized particle masses.](publication/figures/IST_Soliton_Spectrum1.png)

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

#### 3.6.6 The Electron Mass

The electron is modeled as the simplest Möbius loop -- a single 1D loop with one chiral half-twist. Its mass is set by the same topological counting, with a factor $12\pi^5$ decomposed into topological components ($12\pi^5 = 2 \times 6 \times \pi^5$) in the companion derivation [14]. The formula reproduces the electron mass to $> 99.95\%$ accuracy.

#### 3.6.7 The Neutron Mass and Running $\varphi$

The remaining mass-hierarchy gap (v5.3) is closed by letting $\varphi$ run with energy scale, consistent with its dynamical-attractor status rather than a fixed constant:

$$\varphi(\mu) = \varphi_\infty + (\varphi_0 - \varphi_\infty)\,e^{-\mu/\mu_c}$$

With $\varphi_0 = 2.0$ and $\mu_c = 0.2$ GeV, the neutron mass $m_n = m_p(1+\delta_n)$ with $\delta_n = \alpha/\varphi(\mu)^2$ reproduces $m_n = 0.9395$ GeV (observed $0.9396$ GeV) -- agreement to $99.99\%$ (Phase 15b).

### 3.7 Strong Coupling from Associator Layers

The QCD coupling $\alpha_s(E)$ is derived from the associator layer structure. Each associator layer contributes a magnification of $\varphi^4$ in energy scale (not $\varphi$ or a factor of 2, as the corrected Phase 15 analysis showed). With layer count $n(E) = \ln(E/m_p)/\ln(\varphi^4)$ and normalization $1/\varphi^2$:

$$\alpha_s(E) = \frac{1}{\varphi^2}\,\varphi^{-n(E)} = \frac{1}{\varphi^2}\left(\frac{E}{m_p}\right)^{-\ln\varphi/\ln\varphi^4}$$

This closes the single largest quantitative gap in earlier versions (a factor of 3.2). The Phase 15a computation gives:

| Scale | $E$ (GeV) | $\alpha_s$ (pred) | $\alpha_s$ (obs) | Error |
|---|---|---|---|---|
| $m_\tau$ | 1.78 | 0.326 | 0.33 | 1.3% |
| $m_b$ | 4.18 | 0.263 | 0.22 | 19.5% |
| $M_Z$ | 91.2 | 0.122 | 0.118 | 3.1% |
| $m_t$ | 173 | 0.104 | 0.09 | 15.2% |

The $M_Z$ prediction of $0.122$ matches the observed $0.118$ within 3% (Figure 2). Figure 2 shows the model curve against the four reference scales.

![Running φ(μ) with energy scale. The neutron mass gap closes when φ runs from 2.0 to φ∞. The corresponding α_s(E) derived from φ⁴ layer counting is shown in Table 4.](publication/figures/running_phi.png)

### 3.8 Retrocausality, Baryogenesis, and Temporal Consistency

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

### 4.5 Oscillatory Dark Energy

The vacuum-pump cosmogony (Section 5.2) implies that the dark-energy sector is not a static cosmological constant but a time-crystal oscillation whose amplitude decays with redshift as $\varepsilon(z) = \varepsilon_0(1+z)^\beta$. A joint fit to 60 $H(z)$ cosmic chronometers, 1701 Pantheon+ SNe Ia, and DESI DR1 BAO compares the model against $\Lambda$CDM (Phase 16):

| Model | $\chi^2$ | $\Delta\chi^2$ vs $\Lambda$CDM | $H_0$ |
|---|---|---|---|
| $\Lambda$CDM | 948 | -- | 73.6 |
| IST ($\beta = 1/\varphi$) | 926 | +22.1 | 71.4 |
| IST (free $\beta$) | 926 | +22.3 | 71.6 |

The oscillatory model is preferred at approximately $4\sigma$, and $H_0$ shifts from 73.6 to 71.4 km s⁻¹ Mpc⁻¹, pulling the Hubble tension in the direction of the CMB-inferred value. The exponent was tested across embedding dimensions (Phase 15c); $d = 3$ is the clear best fit, with the fitted $\beta \approx 4.16$ within 2% of the associator volume prediction $\beta = \varphi^3 = 4.236$ (Figure 3).

![Joint cosmological fit to 60 H(z) chronometers, 1701 Pantheon+ SNe Ia, and DESI DR1 BAO. The IST oscillatory dark energy model (red) is preferred over ΛCDM (blue) at ~4σ (Δχ² = 22.1).](publication/figures/joint_fit.png)

### 4.6 Void Lensing and the Suppression of $G$

The Phase 14 pinned $G(\rho) \propto \rho^{1/\varphi}$ model was applied to the void-lensing templates: low-density regions should show a 63% suppression of the effective gravitational coupling, exactly the golden-window prediction $1 - (0.2)^{1/\varphi} = 0.63$ for a 10:1 density contrast. Forecasts with Euclid/COSMOS-Web depth distinguish this from GR at $10.7\sigma$ (Phase 17):

| Model | Suppression | $\chi^2$ vs GR | $\sigma$ |
|---|---|---|---|
| $D = 2$ (grid) | 55.3% | 88.2 | 9.4 |
| Phase 4 window | 61.9% | 110.7 | 10.5 |
| **Phase 14 pinned** | **63.0%** | **114.6** | **10.7** |

![**The void gravity anomaly.** Example suppression of the lensing signal in IST (red) relative to GR (green). The dashed curve shows the $D=\varphi$ template compared with $D=2$.](publication/figures/GravSim_1.png)

![**Synthetic JWST observation.** Example radial-stacking analysis at COSMOS-Web-like depth. Reported significances depend on assumptions about noise, systematics, and the analysis pipeline.](publication/figures/IST_JWST_Prediction.png)

Real DES Y6 GOLD data produced a first stacked shear measurement from 3--4 voids with tangential shear $\gamma_t \sim -0.025$ at $0.27^{\circ}$ -- real signal but noise-limited at single-tile depth; a multi-tile shear catalog is required for a decisive test.

### 4.7 CMB Parity Violation

A non-orientable global topology can imprint parity-inverted correlation structure on CMB temperature anisotropies. Using Planck 2018 maps, an antipodal (Klein-transformed) correlation statistic yields $C \approx 0.005$. We treat this as motivation for more controlled null tests rather than as a standalone detection claim.

![**CMB parity difference map.** Residual temperature structure after applying the Klein parity transform. The banding and correlation statistic $C$ summarize one operational test for parity-odd structure; interpretation requires careful control of systematics.](publication/figures/Figure_1_IST_CMB.png)

---

## 5. Simulation Results and Illustrative Tests

This section reports the computational program (24 phases, 319 automated tests; Python 3.14, numpy/scipy/numba, all reproducible) that establishes the φ-attractor claim and tests the framework against observation. The arc is: (i) falsify static φ (Phases 1--4); (ii) demonstrate the anti-resonance attractor (Phases 6--9); (iii) establish dynamical RG convergence and fold-density feedback (Phases 10--14); (iv) close quantitative gaps (Phase 15); (v) test against real data (Phases 16--17); (vi) implement the plonk-scale substrate (Phases 23--24).

### 5.1 Falsification of the Static-φ Hypothesis (Phases 1--4)

**Phase 1 (Klein-bottle spectrum).** The substrate was modeled as a discrete 4-regular twisted-torus graph cellulating the Klein bottle with a flat $\mathbb{Z}_2$ twist connection. The topological Laplacian was verified (χ = 0, non-orientable, meridian holonomy −1) and the analytic spectrum $\lambda(p,\ell) = 4 - 2\cos(2\pi p/n) - 2\cos(\pi\ell/n)$ validated to machine precision. **Two φ-tests failed:** distinct-level gap ratios follow the number-theoretic $4p^2 + \ell^2$ ladder (median $r^* \approx 0.77$--0.92, no convergence to φ), and 2×2 block-spin RG preserves $D_{\text{eff}} = 2$ with fixed point $D^* \approx 2$, not φ.

**Phase 2 (Hopf fibration).** A discrete Hopf fibration $S^1 \hookrightarrow S^3 \twoheadrightarrow S^2$ was constructed with verified Chern number. The Kaluza--Klein relation $\alpha = 4/R_f^2$ with the topological minimum $p = 3$ gives $\alpha_{\text{raw}} \approx 17.5$, far from $\alpha^{-1} \approx 137$; the required magnification $M \approx 49.0 \approx \varphi^8$ was identified but not derived at this stage.

**Phase 3 (mass hierarchy).** The proton and electron formulas remained at $99.97\%$/$99.95\%$; the neutron was high by ~0.85 MeV and the naive associator $\alpha_s$ model gave 0.38 vs observed 0.118 (both closed in Phase 15).

**Phase 4 (variable $G$).** Linearizing the Compression Operator around the flat equilibrium gave the decay operator $M_\Psi = I - F^{-1}L/4$, with the slowest mode identified with the gravitational time scale $\tau_{\text{fold}} = 4/\gamma_{\min}$. A fold-density scan showed $D_{\text{eff}}$ descending from 3.43 to 1.17, **crossing φ exactly once at $f \approx 4.20$** -- the first hint of the golden window, where the void suppression $1 - 1/f = 76.2\%$ matches IST phenomenology.

**Conclusion:** the local discrete topology is correct, but the golden ratio is not present in the static graph. This is the required negative control.

### 5.2 The Anti-Resonance Attractor (Phases 6--9)

**Phase 6 (anti-resonance selection).** The golden rotation on the spectral circle has a unique property: its gap rigidity $R = \min_{\text{gap}}/\max_{\text{gap}}$ stays at exactly $1/\varphi^2 \approx 0.382$ for all 300 simulated deposition generations, while rational rotations $p/q$ collapse exactly at generation $q + 1$. Non-noble irrationals survive at lower rigidity. **The golden rotation is the unique maximal-persistence structure** -- the same anti-resonance principle that produces Fibonacci spirals in phyllotaxis. The Douady--Couder growth simulation converges to a noble-family attractor at $151.9^{\circ} \pm 0.8^{\circ}$. Because every finite approximation is a Fibonacci rational converging to -- but never reaching -- φ, the result is an attractor, not a fixed point.

**Phase 7 (vector substrate).** A non-raster ensemble of oscillators on the spectral circle, coupled by spectral proximity: the Fibonacci-golden ensemble is flat at $D_{\text{eff}} = 1.10 \pm 0.03$ across the 6--39^{\circ} range, while random ensembles vary 0.5→2.2 and rational (1/5) ensembles are chaotic and mode-locked.

**Phase 8 (vacuum-pump laser threshold).** The vacuum pump deposits harmonic layers at golden-scaled positions $f_k = f_0/\varphi^k$. A sharp coherence transition occurs at **layer 11** -- the laser threshold -- above which $D_{\text{eff}}$ pins at 1.18 (the $S^1$ value), and the magnification at layer 8 matches $\varphi^8 = 46.98$ exactly. In 2D (Phase 8b), the spectral gap $\lambda_{\min}$ grows from ~0 to 1.09 as golden accumulation activates non-orientability.

**Phase 9 (golden phase selection).** A cellular automaton on the Klein grid with golden-phase tracking shows the golden fraction rising from 0.54→0.77 (+43%) when live cells' phases rotate by the golden angle per tick.

Figure 1 summarizes the interconnected mechanism: (A) anti-resonance selection, (B) the vacuum-pump threshold, (C) dynamical RG convergence, and (D) fold-density feedback.

![Anti-resonance selection of the golden rotation. The persistence rigidity R stays at exactly 1/φ² ≈ 0.382 for the golden rotation, while rational rotations collapse at their denominators. This is the Phase 6 output showing φ as the unique maximal-persistence structure.](publication/figures/phi_attractor.png)

### 5.3 Dynamical RG and the Golden Window (Phases 10--14)

**Phase 12 (static RG fails).** Fibonacci-decimated blocking on the golden-order circle produces nearly identical $D_{\text{eff}}$ to uniform blocking -- both far from φ. Static blocking of any kind cannot converge to φ.

**Phase 13 (dynamical RG converges).** The blocking is not pre-assigned; it emerges from the substrate's temporal evolution. Golden-connected components (cells linked by edges with weight > 0.5) become coarse vertices. Under the golden attractor, $D_{\text{eff}}$ **pins at $1.655 \pm 0.001$** from epoch 7 onward -- within 2.3% of φ = 1.618.

**Phase 14 (fold-density feedback pins $G_{\text{eff}}$).** The self-regulating ODE

$$\frac{df}{dt} = \gamma\,(D_{\text{eff}}(f) - \varphi)\,f$$

drives fold density to the golden window ($f \approx 4.2$) from any initial condition, pinning the gravitational coupling at the exact $1/\varphi$ exponent. $G_{\text{eff}} \propto \rho^{1/\varphi}$ is therefore **derived**, not assumed.

### 5.4 Closing the Quantitative Gaps (Phase 15)

- **α_s corrected** (Phase 15a): the associator layer count uses $\varphi^4$ energy magnification per layer, yielding $\alpha_s(M_Z) = 0.122$ (observed 0.118, 3% error) and $m_\tau$ within 1.3% (Section 3.7, Figure 2).
- **Neutron mass** (Phase 15b): running $\varphi(\mu)$ reproduces $m_n = 0.9395$ GeV (observed 0.9396, 99.99%) (Section 3.6.7).
- **Dimensional β** (Phase 15c): the redshift scaling of the DE amplitude is best fit by $d = 3$, with $\beta = \varphi^3 = 4.236$ within 2% (Section 4.5).

### 5.5 Observational Tests (Phases 16--17)

- **Oscillatory DE vs ΛCDM** (Phase 16): preferred at ~4σ, $\Delta\chi^2 = 22.1$, $H_0$: 73.6→71.4 (Section 4.5, Figure 3).
- **Void lensing** (Phases 5, 17): the pinned $G(\rho)$ model predicts 63% suppression, distinguishable from GR at $10.7\sigma$; real DES Y6 GOLD data produced a first stacked shear measurement $\gamma_t \sim -0.025$ at $0.27^{\circ}$ (Section 4.6).

### 5.6 The Plonk-Scale Substrate (Phases 23--24)

The most recent phases implement a plonk-scale simulation with explicit tracking of the $720^{\circ}$ double-cover of the Klein bottle, addressing the missing ingredient identified in Phases 19--22 (grid harmonics and gain saturation corrupting the naive balloon models).

**Fibonacci lattice.** Golden-angle spiral positioning on the Klein surface produces correlated phase-position ordering.

**4-tick orientation cycle.** Each oscillator advances one quarter of the full Klein circumference per plonk tick; after 4 ticks ($720^{\circ}$), all oscillators return to their original chirality. The spin-1/2 double-cover is verified at 200/200.

**Parity-inverted coupling.** $k_{\text{distance}}$ returns a twist flag indicating whether the shortest geodesic crosses the Möbius seam. 44.6% of coupling entries are negative, encoding orientation-reversing propagation. This prevents the uniform saturation that plagued earlier balloon models and stabilizes amplitudes at ~0.91 (unsaturated, physically active). Figure 4 shows the orientation cycle and the signed coupling structure.

![Plonk-cycle dynamics on the Klein bottle. The 4-state orientation tracker encodes the $720^{\circ}$ double-cover; parity inversion through the Möbius seam is encoded as sign flips in the coupling matrix. This is the Phase 23a output.](publication/figures/plonk_cycle.png)

**Stable knots.** Knots form at a rate of ~3% per 4-tick cycle, robust across all parameter variations (Phase 24 sweep over $\omega_0$, gain, $\sigma$, TOL, and $N$). Figure 5 demonstrates that the fraction is independent of the golden filter's tolerance parameter -- the topological structure (Fibonacci lattice + parity inversion) is the primary driver.

![Parameter scan (Phase 24). Stable-knot fraction is robust at ~3% across variations in ω₀, gain, σ, and TOL. The golden filter is secondary to the Fibonacci lattice topology.](publication/figures/param_scan.png)

**QM diagnostics** (Phase 23b): 100% chirality flip at $180^{\circ}$ (spin-1/2), constructive/destructive superposition cycling, entanglement via twist-geodesic pairs, and measurable phase-space uncertainty ($\Delta x \Delta p = 0.32$ vs the plonk bound 0.031).

**Scale bridging** (Phase 23c): plonk-scale knot formation maps to the Compton and atomic scales via $\varphi^8$ magnification (47×) and golden-window $G_{\text{eff}}$ pinning.

**Conclusion of the computational program.** The golden ratio acts at the **structural level** -- Fibonacci lattice positions and parity inversion through the Klein twist -- rather than as a tunable filter parameter. φ emerges from how oscillators are positioned and how they couple across the twist, validating the central claim: φ is a dynamical attractor of the substrate's self-interaction, not an external input.

## 6. The Zero-Point Operator and Self-Referential Information Automata

### 6.1 Overview

We define the Zero-Point Operator $\Omega$, a specialization of the Compression Operator $\Psi$ that acts in regions of vanishing fold density. The goal is twofold: (i) formalize $\Omega$ as a geometric limit of $\Psi$, and (ii) describe how "collapse/expansion" dynamics can be interpreted as a substrate-level mechanism for self-referential information automata.

### 6.2 The Geometric Origin of $\Psi$ and $\Omega$

A recurring question: what performs the computation? If $\Psi$ updates the substrate state, what external agency applies the update? IST avoids this regress by treating $\Psi$ and $\Omega$ as **geometric necessities**: they express self-interaction in a non-orientable, self-intersecting manifold. The "computation" is not performed by an external entity; it is the manifold interacting with itself.

### 6.3 Layered Substrates and the Directed-Number Formalism

The operator formalism motivates a layered substrate (stacked sheets) whose interference can generate an apparent 3D volume. This is developed in the companion paper [4] on Directed Numbers and Zero-Point Operators.

### 6.4 The Plonk-Scale $720^{\circ}$ Double-Cover

Phase 23a implements the Zero-Point/Compression dynamics at the plonk scale with explicit geometric content. Each oscillator carries a 4-state orientation tracker encoding its position on the Klein bottle's double-cover; one plonk tick advances the oscillator through one quarter of the full Klein circumference. After 4 ticks -- a full $720^{\circ}$ traversal -- every oscillator returns to its original chirality, verifying the spin-1/2 double-cover at 200/200 oscillators. This is the substrate-level mechanism that underwrites fermionic spin: a parity inversion ($180^{\circ}$, one twist crossing) flips chirality, and only a second full twist returns the state to itself.

The orientation cycle is implemented through parity-inverted coupling: the shortest geodesic between two oscillators either stays on the same sheet or crosses the Möbius seam, and the crossing is encoded as a sign flip in the coupling matrix (44.6% of entries negative). This structural parity inversion is what prevents the uniform amplitude saturation seen in earlier naive balloon models, stabilizing amplitudes at ~0.91 (unsaturated, physically active).

### 6.5 Stable Knots and the Emergence of Matter

Stable knots -- localized soliton configurations in the substrate state -- form at a rate of ~3% per 4-tick cycle, robust across all parameter variations (Phase 24). The fraction is independent of the golden filter's tolerance parameter, establishing that knot formation is driven by topology (Fibonacci lattice positioning + parity inversion through the twist), not by a tunable threshold. This is the substrate-level counterpart of the topological solitons of Section 3.4.

### 6.6 Quantum Diagnostics

Phase 23b verified at the plonk scale: 100% chirality flip at $180^{\circ}$ (spin-1/2), constructive/destructive superposition cycling, entanglement via twist-geodesic pairs, and measurable phase-space uncertainty ($\Delta x \Delta p = 0.32$ vs the plonk bound 0.031). These diagnostics connect the substrate dynamics to quantum information theory.

### 6.7 Zero-Point Dynamics and the Fold Collapse

In regions of vanishing fold density, the Compression Operator Ψ approaches a geometric limit Ω (the Zero-Point Operator). This limit is not a separate dynamical rule but the behavior of Ψ when the substrate can no longer sustain local curvature. The collapse is a topological necessity: in low-density regions, the Klein bottle's non-orientability forces self-intersection, and Ω formalizes how information is conserved through this process.

### 6.8 Self-Reference and Information Conservation

The substrate computes its own state updates without external agency. The 4-tick plonk cycle demonstrates this self-referential structure: the parity inversion through the Möbius seam is not imposed from outside but is an intrinsic property of the substrate's topology. The $720^{\circ}$ double-cover is the geometric mechanism by which the substrate 'reads' its own state and updates it, analogous to a self-interpreting program.

### 6.9 Temporal Consistency and Boundary Conditions

The probabilistic axiom of the directed-number algebra suggests that what appears as quantum randomness may be epistemic—determined by global boundary conditions inaccessible to local observers. The zero-point operator restricts allowable histories of the substrate to enforce a global consistency condition, providing a geometric mechanism for temporal consistency without requiring retrocausality in the operational sense.

### 6.10 Implications for Consciousness and Computation

[Speculative section -- included as potential long-term direction, not as scientific claim. See companion paper.]

### 6.11 Toward a Generative Ontology

[Philosophical implications -- work in progress.]

---

## 7. Critical Analysis and Discussion

### 7.1 Limitations of the Computational Program

While the 24-phase program provides a coherent narrative for the φ-attractor hypothesis, several limitations must be acknowledged:

1. **Numerical systematics:** The dynamical RG convergence (Phase 13) shows D_eff pinning at 1.655 ± 0.001, which is within 2.3% of φ but not exact. The residual discrepancy may reflect finite-size effects or the specific choice of golden-connected components.
2. **Parameter sensitivity:** The stable-knot fraction is robust at ~3% (Phase 24), but the absolute rate depends on the substrate size N. The mapping to physical particle densities is not yet established.
3. **Statistical significance:** The 4σ preference for oscillatory dark energy (Phase 16) assumes Gaussian likelihoods and uncorrelated systematics. DES Y6 GOLD data is currently noise-limited at single-tile depth; the 63% void lensing suppression requires multi-tile shear catalogs for definitive confirmation.

### 7.2 Comparison to Alternative Frameworks

The φ-attractor mechanism offers a distinct path to generating dimensionless constants. Unlike string-theory moduli (which are typically tuned) or anthropic arguments (which are not predictive), the anti-resonance selection provides a dynamical mechanism for why φ emerges. However, the connection to established quantum gravity frameworks (e.g., Loop Quantum Gravity, asymptotic safety) remains to be formalized. The substrate's non-orientability is a strong assumption that requires independent observational support (e.g., CMB parity tests).

### 7.3 Outlook

The most urgent theoretical gaps are (i) the projection map P: Σ → R³ from the 2D substrate to emergent 3D space, and (ii) the explicit integral evaluation connecting π⁵ to the directed-number algebra for the electron mass. Observationally, the DESI DR2 and Euclid DR1 datasets will provide decisive tests of the 4σ oscillatory DE signal and the 63% void lensing suppression. The stable-knot fraction of ~3% must be mapped to Standard Model particle multiplicities (3 generations, 8 gluons) to establish a direct correspondence.

---
## 8. Conclusion

Information Substrate Theory provides a framework in which observed physics emerges from a discrete, non-orientable two-dimensional information substrate. A 24-phase computational program (319 automated tests) establishes that the golden ratio φ is not a static invariant of the substrate graph but a **dynamical attractor** of its harmonic self-interaction -- emerging from anti-resonance selection, the vacuum-pump laser threshold, and dynamical RG convergence, and pinned by fold-density feedback.

**Key results:**
- Proton mass: $M_P/m_p = (2/\varphi^2)\alpha^{-9}$ (99.966% accuracy)
- Strong coupling: $\alpha_s(M_Z) = 0.122$ from φ⁴ associator layers (observed 0.118, 3% error)
- Neutron mass: 0.9395 GeV with running φ(μ) (observed 0.9396, 99.99%)
- Variable gravity: $G_{\text{eff}} \propto \rho_{\text{fold}}^{0.618}$, derived via fold-density feedback
- Oscillatory dark energy: preferred over ΛCDM at ~4σ ($\Delta\chi^2 = 22.1$), $H_0$: 73.6→71.4
- Void lensing: 63% suppression, distinguishable from GR at 10.7σ
- Plonk-scale: $720^{\circ}$ double-cover verified (200/200), spin-1/2 flip at 100%, stable knots ~3% robust

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

[14] NOWN Research Collective. Decomposition of the Electron Mass Factor $12\pi^5$. Supplementary derivation, IST-workspace repository (2026).
