# Information Substrate Theory (IST): Topology as a Substrate for Emergent Physics

**Dr. Mary Theadoor**
**The Nown Research Group**
**Version 7.0 — August 2026**

## Abstract

We introduce Information Substrate Theory (IST), a unified framework in which observed physics emerges from a discrete, non-orientable two-dimensional information substrate $\Sigma$ woven from fundamental 1D Möbius loops. Gravity is interpreted as computational latency ($\tau_{\text{fold}}$); matter as stable topological solitons; the golden ratio $\varphi$ as a *dynamical attractor* of the substrate's harmonic self-interaction, not a static invariant.

The $\varphi$-emergence claim rests on a code-verified computational program (42 phases, 510 automated tests). Three interconnected mechanisms are demonstrated: (i) the vacuum-pump laser threshold, where coherent golden accumulation overtakes the noise floor at a sharp transition (Phase 8); (ii) dynamical RG convergence, where golden-connected components under temporal evolution produce $D_{\text{eff}} \to 1.655$, within 2.3% of $\varphi$ (Phase 13); and (iii) fold-density feedback, where $df/dt = \gamma(D_{\text{eff}}(f) - \varphi)f$ drives any initial condition to the golden window $f \approx 4.2$, pinning $G_{\text{eff}} \propto \rho^{1/\varphi}$ (Phase 14).

At the quantum scale the framework's strongest claims are top-down and parameter-free: $m_p/m_e = 6\pi^5$ (99.9981%, Phase 27); the neutron excess $\delta_n = \frac{\alpha}{2\varphi^2}(1 - (\frac{3}{2} - \frac{\alpha}{\varphi^6})\alpha)$ (0.02σ of CODATA, Phases 28–30); the Koide relation $Q = 2/3$ (0.0009%, Phase 31); and the baryon decuplet ladder $m(S) = [4 + \frac{k}{2}f_{\text{Klein}}]E$ (≤0.29%, Phases 34–35). Each of these derives from the single half-integer twist $\theta = 1/2$ of the Klein bottle's meridian — the 720° double-cover.

Observationally, the oscillatory dark energy model is preferred over $\Lambda$CDM at ~4σ ($\Delta\chi^2 = 22.1$ in a joint fit to 60 $H(z)$ chronometers, 1701 Pantheon+ SNe Ia, and DESI DR1 BAO); void-lensing templates predict a 63% suppression of $G$ in low-density regions, distinguishable from GR at $10.7\sigma$; and the strong coupling is reproduced at $M_Z$ (3.1%) and $m_\tau$ (1.3%) by a golden-layer mass→coupling relation, with the active-flavor threshold mechanism confirmed at best RMS 8.7% (Phases 38–42).

Honest negatives are reported alongside positives: force couplings are not golden harmonics (Phase 37); dimensional crystallization is CMB-excluded for $z_c \lesssim 1090$ (Phase 36); and the self-referential "137" fixed point fails the project's four golden-relation robustness checks (Phase 42, H42g) and is retracted as a claim.

## 1. Introduction

### 1.1 Motivation and Scope

Contemporary physics remains divided between geometric gravity (GR) and probabilistic quantum matter (QM). Information Substrate Theory (IST) pursues a complementary unification strategy: it treats both spacetime geometry and quantum degrees of freedom as emergent descriptions of a more primitive informational substrate. In this view, dynamical "laws" are not external prescriptions; they are effective constraints induced by the substrate's topology.

**The central question of this version.** The golden ratio $\varphi \approx 1.618$ appears throughout the framework — in the proton mass formula, in the variable gravitational coupling $G_{\text{eff}} \propto \rho^{1/\varphi}$, and in the oscillatory dark energy component. But where does $\varphi$ come from? Is it a fixed point of the substrate's renormalization group — a static invariant written into its geometry — or does it emerge from the substrate's dynamics? This paper answers that question with a systematic, code-verified computational investigation spanning 42 phases and 510 automated tests: **$\varphi$ is not a static invariant of the substrate's spatial graph; it is a dynamical attractor of its harmonic self-interaction in the time domain.** Section 5 documents this result and the three interconnected mechanisms behind it, each reproduced in code with quantitative output.

Because IST adopts a nonstandard starting point, the main difficulty for a new reader is not technical complexity but perspective: familiar objects (fields, particles, couplings) are treated as large-scale invariants of a discrete topological system. For clarity, we distinguish throughout between (i) postulates (assumptions about the substrate), (ii) definitions (quantities introduced within the model), (iii) derived statements (claims that follow from the postulates and definitions), and (iv) empirical signatures (observables that could support or falsify the framework).

### 1.2 Reader On-Ramp: Primitives, Definitions, and Tests

**Minimal dictionary:**

- **$\Sigma$**: Discrete non-orientable information substrate (modeled as a graph)
- **$\Psi$**: Local update map ("Compression Operator") summarizing substrate self-interaction during propagation
- **$\Omega$**: Limiting zero-point map associated with self-intersection/collapse in low fold-density regions
- **$\rho_{\text{fold}}$**: Fold-density functional measuring deviation from locally "flat" weave configurations
- **$D$**: Effective fractal dimension controlling the scaling $G(\rho_{\text{fold}}) \propto \rho_{\text{fold}}^{1/D}$
- **$\theta = 1/2$**: The half-integer twist of the Klein meridian — the single structural constant behind the neutron factor-2, the Koide phase, and the double-cover baryon ladder

**Interpretive rule.** When we use an analogy (e.g., "computational latency" or "tension in the weave"), it is intended as an intuition aid; the operational content is given by the accompanying definitions and equations.

**Evaluation standard.** We treat IST as a work in progress to be revised against observation. The framework is supported only insofar as it yields quantitative, discriminating predictions (e.g., void-lensing templates, parity correlations) that can be tested independently of interpretive language. Claims that fail the project's four golden-relation robustness checks (uniqueness of the fixed point, base-specificity, unit-invariance, parameter-freedom) are reported as negatives, not as hits.

### 1.3 The Foundational Axioms of IST

We state three working axioms that define the substrate, its evolution, and the meaning of emergence in the model.

**Axiom 1: Substrate axiom (topology and discreteness).** The primitive description is a finite, discrete, two-dimensional substrate $\Sigma$ with non-orientable global topology. The Klein bottle ($K_2$) provides a minimal working model; the axiom also admits more general non-orientable quotients.

**Axiom 2: Dynamical axiom (local update).** The substrate evolves via a local, unitary update map $\Psi$ (the Compression Operator). $\Psi$ is not treated as an externally applied command; it summarizes how non-orientable geometry can induce self-interaction during propagation within the model.

**Axiom 3: Emergence axiom (effective physics).** Observed physics -- spatial geometry, time, effective couplings, matter degrees of freedom -- corresponds to stable, coarse-grained patterns in $\Sigma$.

### 1.4 The Epistemological Status of the Substrate

A crucial clarification: the 2D non-orientable information lattice $\Sigma$ is a **mathematical model, not a literal substance**. It is a conceptual embedding used to represent the propagation and interaction of physical degrees of freedom, much as Hilbert space in quantum mechanics is a mathematical arena in which wavefunctions are defined. The substrate is a **map of the territory**. The territory itself is inferred only through the empirical patterns it produces. We treat IST as a work in progress whose claims are intended to be evaluated and revised against observation.

### 1.5 Organization of the Paper

- Section 2: Mathematical structure of the substrate and operator formalism
- Section 3: Emergent physics -- gravity, field equations, mass derivations, and the strong coupling
- Section 4: Cosmological implications -- flatness and the oscillatory dark energy model tested against real data
- Section 5: Simulation results -- the 42-phase computational program from static-$\varphi$ falsification to the plonk-scale substrate
- Section 6: Quantum-scale derivations -- the half-integer twist and the particle spectrum
- Section 7: The zero-point operator and the $720^{\circ}$ double-cover
- Section 8: Critical analysis and discussion
- Appendices: Phase map, simulation protocols

## 2. Mathematical Foundations

### 2.1 Overview and Notation

We model the substrate as a discrete dynamical system with local update rules constrained by global non-orientability. Throughout, we represent $\Sigma$ as a graph $G = (V, E)$. Vertex indices are denoted by $i, j \in V$, time by $t \in \mathbb{N}$, and the neighborhood of vertex $i$ by $N(i)$.

### 2.2 The Primitive Lattice as a Weave of 1D Möbius Loops

The 2D lattice $\Sigma$ is not a primitive continuum; it is **woven from fundamental 1D Möbius loops**. Each loop has intrinsic chirality, encoded in the directed number formalism [3] as clockwise ($\circlearrowright$) and counterclockwise ($\circlearrowleft$) states.

The weave creates the 2D surface through **nested recurrent interactions**. Pairwise interactions of loops create 2D surfaces; triple interactions (measured by the associator $[x, y, z]$) create 3D volume; higher-order interactions create 4D spacetime. This yields a recursive, self-similar hierarchy with scale-dependent effective descriptions.

### 2.3 The Compression Operator ($\Psi$)

The local update map is generated by the **Compression Operator** $\Psi$, whose action on a neighborhood is governed by the fold density $\rho_{\text{fold}}$ of the local weave:

$$\Psi[\rho](v) = \sum_{u \in N(v)} w_{uv}(\rho)\, \rho(u),$$

where the weights $w_{uv}$ encode both the lattice adjacency and the non-orientable twist (a sign flip when the geodesic crosses the Möbius seam). In the flat limit the operator linearizes to $M_\Psi = I - F^{-1}L/4$, whose slowest mode sets the gravitational time scale $\tau_{\text{fold}} = 4/\gamma_{\min}$ (Section 3.2).

### 2.4 The Weave as Information Substrate

Because $\Sigma$ is non-orientable, "left" and "right" are not globally well-defined: a loop transported around the Klein circumference returns with flipped chirality. This single property -- the meridian holonomy $-1$ -- is the geometric root of the framework's distinctive results (Section 6). We emphasize that this is a *property of the mathematical model*, not an assertion about a literal substance.

## 3. Emergent Physics

### 3.1 Overview

The substrate generates effective physics through coarse-grained invariants: gravity as the latency of propagation through the weave; matter as stable solitonic knots; couplings as the running between mass harmonics (Section 5.5). The strong coupling is the cleanest example: it is *derived* from the mass spectrum via a golden layer count, not assumed.

### 3.2 Gravity as Computational Latency

Linearizing $\Psi$ around the flat equilibrium gives the decay operator $M_\Psi = I - F^{-1}L/4$. The slowest mode of this operator decays on the time scale $\tau_{\text{fold}} = 4/\gamma_{\min}$, which we identify with the gravitational interaction time. Under the fractal-projection argument of Section 3.5, the effective coupling scales as

$$G_{\text{eff}}(x) \propto \rho_{\text{fold}}(x)^{1/D}.$$

The exponent $1/D$ measures how the 2D substrate folds to yield an effective 3D volume; $D = \varphi$ gives $G_{\text{eff}} \propto \rho_{\text{fold}}^{0.618}$.

### 3.3 Topological Field Equations

The field content is not introduced as a gauge bundle over spacetime; it is derived from the substrate's topology. U(1), SU(2), and SU(3) structures correspond to distinct features of the non-orientable weave (Section 4.3 sketches the higher-dimensional generalization). The operational content is the mass→coupling relation of Section 5.5, which is tested directly against measured $\alpha_s$.

### 3.4 Matter as Topological Solitons

Matter corresponds to stable knots in the weave -- localized solitonic configurations that survive the substrate's unitary evolution. The plonk-scale simulation (Section 5.6) produces stable knots at a rate of ~3% per 4-tick cycle, robust across all parameter variations (Phase 24), and the parameter sweep establishes that knot formation is driven by the substrate's *topology* (Fibonacci lattice positioning + parity inversion through the twist), not by a tunable threshold parameter.

![**Simulated topological soliton.** A stable knot configuration in the IST substrate exhibiting a Möbius-type twist; the persistence of the structure illustrates how long-lived matter states can emerge.](publication/figures/Stabilized_IST_particle.png)

![**Topological resonance spectrum.** Example standing-wave (soliton) patterns and their associated harmonic structure, illustrating the proposed route to quantized particle masses.](publication/figures/IST_Soliton_Spectrum1.png)

The solitons are the substrate-level counterpart of the electron-as-confined-field proposals of van der Mark & 't Hooft [4] and Williamson & van der Mark [5], cited as suggestive analogues, not as direct evidence.

### 3.5 Fractal Dimension and the Scaling of Gravity

In a self-similar hierarchy generated by $\Psi$, fold density scales as $\rho_{\text{fold}} \propto N^D$, where $N$ is the recursion depth and $D$ the effective fractal dimension. Since $\tau_{\text{fold}} \propto N$ and $G \propto \tau_{\text{fold}}$, we obtain $G_{\text{eff}} \propto \rho_{\text{fold}}^{1/D}$ (Section 3.2). The value $D = \varphi$ is the dynamical RG fixed point of Section 5.3, and the exponent $0.618$ yields the testable void-lensing prediction of Section 4.6.

### 3.6 Topological Derivation of the Proton Mass

A critical test of any fundamental theory is its ability to predict particle masses from first principles. In IST, fermions are modeled as stable topological solitons whose effective mass is associated with the rate of self-intersection events per unit time.

**Local geometry (Hopf fibration).** Each quark is modeled locally by the Hopf fibration $S^1 \hookrightarrow S^3 \twoheadrightarrow S^2$; Kaluza–Klein compactification of the fiber gives $\alpha = 4/R_f^2$, so $R_f = 2/\sqrt{\alpha}$. With 18 phase-space dimensions (3 quarks × 6 degrees of freedom), the addressable-state count scales as $\alpha^{-9}$, identified with $M_P/m_p$. Fractal projection with normalization $2/\varphi^2$ gives

$$\frac{M_P}{m_p} = \frac{2}{\varphi^2}\,\alpha^{-9},$$

reproducing $m_p$ at 99.97% (CODATA 2022). The remaining residual is consistent with the leading QED correction $2\pi\alpha^2$ at the ~1% level.

**Scale caveat.** This bottom-up form inherits the uncertainty in $M_P$. The framework's strongest mass claim is the *ratio* $m_p/m_e = 6\pi^5$ (Section 6.3), which cancels both $\alpha$ and $M_P$ entirely and is parameter-free.

### 3.7 Strong Coupling from Associator Layers

The QCD coupling is derived from the associator layer structure. Each associator layer contributes an energy magnification of $\varphi^4$; with layer count $n(E) = \ln(E/m_p)/\ln(\varphi^4)$ and normalization $1/\varphi^2$,

$$\alpha_s(E) = \frac{1}{\varphi^2}\,\varphi^{-n(E)} = \frac{1}{\varphi^2}\left(\frac{E}{m_p}\right)^{-\ln\varphi/\ln\varphi^4}.$$

| Scale | $E$ (GeV) | $\alpha_s$ (pred) | $\alpha_s$ (obs) | Error |
|---|---|---|---|---|
| $m_\tau$ | 1.78 | 0.326 | 0.33 | 1.3% |
| $m_b$ | 4.18 | 0.263 | 0.22 | 19.5% |
| $M_Z$ | 91.2 | 0.122 | 0.118 | 3.1% |
| $m_t$ | 173 | 0.104 | 0.09 | 15.2% |

![**Running coupling.** The model curve from golden-layer counting against the four reference scales ($m_\tau$, $m_b$, $M_Z$, $m_t$).](publication/figures/running_phi.png)

The $M_Z$ and $m_\tau$ values agree to 3.1% and 1.3%. The $m_b$/$m_t$ residuals are the active-flavor threshold issue addressed in Section 5.5.

## 4. Cosmological Implications

### 4.1 Overview

This section sketches testable cosmological consequences of a non-orientable information substrate. The two quantitative claims -- oscillatory dark energy and void-lensing suppression -- are tested against real data; the flatness and CMB-parity points are stated as structural consequences with appropriate caveats.

### 4.2 The Flatness Problem

The intrinsic geometry of a Klein bottle ($K_2$) is flat, so Klein-bottle-based models provide a setting in which $\Omega_K \approx 0$ can arise without fine-tuning at the level of the assumed topology.

### 4.3 Generalization to Higher Dimensions

The framework is compatible with richer topologies, including non-orientable quotients of Calabi–Yau manifolds. In such settings, gauge symmetries may be associated with nontrivial features of moduli space. This is a structural compatibility, not a tested prediction.

### 4.4 Oscillatory Dark Energy

The vacuum-pump cosmogony implies that the dark-energy sector is not a static cosmological constant but a time-crystal oscillation whose amplitude decays with redshift as $\varepsilon(z) = \varepsilon_0(1+z)^\beta$. A joint fit to 60 $H(z)$ cosmic chronometers, 1701 Pantheon+ SNe Ia, and DESI DR1 BAO compares the model against $\Lambda$CDM (Phase 16):

| Model | $\chi^2$ | $\Delta\chi^2$ vs $\Lambda$CDM | $H_0$ |
|---|---|---|---|
| $\Lambda$CDM | 948 | -- | 73.6 |
| IST ($\beta = 1/\varphi$) | 926 | +22.1 | 71.4 |
| IST (free $\beta$) | 926 | +22.3 | 71.6 |

![**Joint cosmological fit.** 60 $H(z)$ chronometers, 1701 Pantheon+ SNe Ia, and DESI DR1 BAO. The IST oscillatory dark energy model is preferred over $\Lambda$CDM at ~4$\sigma$ ($\Delta\chi^2 = 22.1$).](publication/figures/joint_fit.png)

The oscillatory model is preferred at approximately $4\sigma$, and $H_0$ shifts from 73.6 to 71.4 km s⁻¹ Mpc⁻¹, toward the CMB-inferred value. The exponent was tested across embedding dimensions (Phase 15c): $d = 3$ is the clear best fit, with the fitted $\beta \approx 4.16$ within 2% of the associator volume prediction $\beta = \varphi^3 = 4.236$.

### 4.5 Void Lensing and the Suppression of $G$

The Phase 14 pinned $G(\rho) \propto \rho^{1/\varphi}$ model was applied to the void-lensing templates: low-density regions should show a 63% suppression of the effective gravitational coupling, exactly the golden-window prediction $1 - (0.2)^{1/\varphi} = 0.63$ for a 10:1 density contrast:

| Model | Suppression | $\chi^2$ vs GR | $\sigma$ |
|---|---|---|---|
| $D = 2$ (grid) | 55.3% | 88.2 | 9.4 |
| Phase 4 window | 61.9% | 110.7 | 10.5 |
| **Phase 14 pinned** | **63.0%** | **114.6** | **10.7** |

![**The void gravity anomaly.** Example suppression of the lensing signal in IST relative to GR; the dashed curve shows the $D = \varphi$ template compared with $D = 2$.](publication/figures/GravSim_1.png)

![**Synthetic JWST observation.** Example radial-stacking analysis at COSMOS-Web-like depth [2]. Reported significances depend on assumptions about noise, systematics, and the analysis pipeline.](publication/figures/IST_JWST_Prediction.png)

Real DES Y6 GOLD data produced a first stacked shear measurement from 3--4 voids with tangential shear $\gamma_t \sim -0.025$ at $0.27^{\circ}$ -- a real signal, noise-limited at single-tile depth. A multi-tile shear catalog is required for a decisive test.

![**DES stacked shear.** First real void-lensing shear measurement from DES Y6 GOLD, noise-limited at single-tile depth.](publication/figures/void_shear_des.png)

### 4.6 CMB Parity Violation

A non-orientable global topology can imprint parity-inverted correlation structure on CMB temperature anisotropies. Using Planck 2018 maps, an antipodal (Klein-transformed) correlation statistic yields $C \approx 0.005$. We treat this as motivation for more controlled null tests rather than as a standalone detection claim.

![**CMB parity difference map.** Residual temperature structure after applying the Klein parity transform; interpretation requires careful control of systematics.](publication/figures/Figure_1_IST_CMB.png)

## 5. Simulation Results and Illustrative Tests

### 5.1 The Computational Program

The $\varphi$-emergence claim rests on a code-verified computational program (42 phases, 510 automated tests; Python 3.14, numpy/scipy/numba, all reproducible). The arc is: (i) falsify static $\varphi$ (Phases 1--4); (ii) demonstrate the anti-resonance attractor (Phases 6--9); (iii) establish dynamical RG convergence and fold-density feedback (Phases 10--14); (iv) close quantitative gaps (Phase 15); (v) test against real data (Phases 16--17); (vi) implement the plonk-scale substrate (Phases 23--24); (vii) validate at the quantum scale top-down (Phases 27--35); (viii) test and honestly bound the strong-coupling and QM claims (Phases 36--42).

### 5.2 Falsification of the Static-$\varphi$ Hypothesis (Phases 1--4)

**Phase 1 (Klein-bottle spectrum).** The substrate was modeled as a discrete 4-regular twisted-torus graph cellulating the Klein bottle with a flat $\mathbb{Z}_2$ twist connection. The topological Laplacian was verified (χ = 0, non-orientable, meridian holonomy −1) and the analytic spectrum $\lambda(p,\ell) = 4 - 2\cos(2\pi p/n) - 2\cos(\pi\ell/n)$ validated to machine precision. **Two $\varphi$-tests failed:** distinct-level gap ratios follow the number-theoretic $4p^2 + \ell^2$ ladder (median $r^* \approx 0.77$--0.92, no convergence to $\varphi$), and 2×2 block-spin RG preserves $D_{\text{eff}} = 2$ with fixed point $D^* \approx 2$, not $\varphi$.

**Phase 2 (Hopf fibration).** A discrete Hopf fibration $S^1 \hookrightarrow S^3 \twoheadrightarrow S^2$ was constructed with verified Chern number. The Kaluza–Klein relation $\alpha = 4/R_f^2$ with the topological minimum $p = 3$ gives $\alpha_{\text{raw}} \approx 17.5$, far from $\alpha^{-1} \approx 137$; the required magnification $M \approx 49.0 \approx \varphi^8$ was identified but not derived at this stage.

**Phase 3 (mass hierarchy).** The proton and electron formulas held at 99.97%/99.95%; the neutron was high by ~0.85 MeV and the naive associator $\alpha_s$ model gave 0.38 vs observed 0.118 (both closed in Phase 15 and refined in Phases 27--30).

**Phase 4 (variable $G$).** Linearizing the Compression Operator around the flat equilibrium gave the decay operator $M_\Psi = I - F^{-1}L/4$, with the slowest mode identified with the gravitational time scale $\tau_{\text{fold}} = 4/\gamma_{\min}$. A fold-density scan showed $D_{\text{eff}}$ descending from 3.43 to 1.17, **crossing $\varphi$ exactly once at $f \approx 4.20$** -- the first hint of the golden window.

**Conclusion:** the local discrete topology is correct, but the golden ratio is not present in the static graph. This is the required negative control.

### 5.3 The Anti-Resonance Attractor (Phases 6--9)

**Phase 6 (anti-resonance selection).** The golden rotation on the spectral circle has a unique property: its gap rigidity $R = \min_{\text{gap}}/\max_{\text{gap}}$ stays at exactly $1/\varphi^2 \approx 0.382$ for all 300 simulated deposition generations, while rational rotations $p/q$ collapse exactly at generation $q + 1$. **The golden rotation is the unique maximal-persistence structure.** The Douady–Couder growth simulation converges to a noble-family attractor at $151.9^{\circ} \pm 0.8^{\circ}$ -- the continued-fraction structure of the golden ratio [6] realizes the KAM-type stability of the most-irrational rotation [7]. Because every finite approximation is a Fibonacci rational converging to -- but never reaching -- $\varphi$, the result is an attractor, not a fixed point.

![**Anti-resonance selection of the golden rotation.** The persistence rigidity $R$ stays at exactly $1/\varphi^2 \approx 0.382$ for the golden rotation while rational rotations collapse at their denominators (Phase 6 output).](publication/figures/phi_attractor.png)

**Phase 7 (vector substrate).** A non-raster ensemble of oscillators on the spectral circle, coupled by spectral proximity: the Fibonacci-golden ensemble is flat at $D_{\text{eff}} = 1.10 \pm 0.03$ across the 6--39° range, while random ensembles vary 0.5→2.2 and rational (1/5) ensembles are chaotic and mode-locked.

**Phase 8 (vacuum-pump laser threshold).** The vacuum pump deposits harmonic layers at golden-scaled positions $f_k = f_0/\varphi^k$. A sharp coherence transition occurs at **layer 11** -- the laser threshold -- above which $D_{\text{eff}}$ pins at 1.18, and the magnification at layer 8 matches $\varphi^8 = 46.98$ exactly.

![**Vacuum-pump threshold.** $D_{\text{eff}}$ versus pump strength: coherence jumps at layer 11 and pins at 1.18 (Phase 8 output).](publication/figures/d_eff_vs_pump.png)

**Phase 9 (golden phase selection).** A cellular automaton on the Klein grid with golden-phase tracking shows the golden fraction rising from 0.54→0.77 (+43%) when live cells' phases rotate by the golden angle per tick.

### 5.4 Dynamical RG and the Golden Window (Phases 10--14)

**Phase 12 (static RG fails).** Fibonacci-decimated blocking on the golden-order circle produces nearly identical $D_{\text{eff}}$ to uniform blocking -- both far from $\varphi$. Static blocking of any kind cannot converge to $\varphi$.

**Phase 13 (dynamical RG converges).** The blocking is not pre-assigned; it emerges from the substrate's temporal evolution. Golden-connected components (cells linked by edges with weight > 0.5) become coarse vertices. Under the golden attractor, $D_{\text{eff}}$ **pins at $1.655 \pm 0.001$** from epoch 7 onward -- within 2.3% of $\varphi = 1.618$.

![**Dynamical RG convergence.** Golden-connected components become coarse vertices; $D_{\text{eff}}$ pins at $1.655 \pm 0.001$ from epoch 7 (Phase 13 output).](publication/figures/dynamical_rg.png)

**Phase 14 (fold-density feedback pins $G_{\text{eff}}$).** The self-regulating ODE $df/dt = \gamma\,(D_{\text{eff}}(f) - \varphi)\,f$ drives fold density to the golden window ($f \approx 4.2$) from any initial condition, pinning the gravitational coupling at the exact $1/\varphi$ exponent. $G_{\text{eff}} \propto \rho^{1/\varphi}$ is therefore **derived**, not assumed.

![**Fold-density feedback.** Trajectories from diverse initial fold densities all converge to the golden window $f \approx 4.2$ (Phase 14 output).](publication/figures/feedback_trajectory.png)

### 5.5 Observational Tests and the Strong-Coupling Closure (Phases 15--17, 38--42)

**Oscillatory DE vs $\Lambda$CDM** (Phase 16): preferred at ~4σ, $\Delta\chi^2 = 22.1$, $H_0$: 73.6→71.4 (Section 4.4).

**Void lensing** (Phases 5, 17): the pinned $G(\rho)$ model predicts 63% suppression, distinguishable from GR at $10.7\sigma$; real DES Y6 GOLD data produced a first stacked shear measurement $\gamma_t \sim -0.025$ at $0.27^{\circ}$ (Section 4.5).

**The mass→coupling relation** (Phase 38): the golden-layer count from $m_p$ reproduces $\alpha_s(M_Z)$ at 3.1% and $\alpha_s(m_\tau)$ at 1.3%, with the associator magnitude $1/\varphi^2$ as the natural normalization -- the *mechanism* from masses to couplings is golden, even though the couplings themselves are not golden values (Phase 37, §8.2).

**Active-flavor thresholds** (Phases 39, 42): the $m_b$/+19.5% and $m_t$/+15.2% residuals trace to the golden-layer base being held constant while QCD's running slows as flavors activate. A boundary-convention fix (reference AT a threshold uses the flavor count ABOVE it) improves the principled form $\varphi^{-(n_f-3)/6}$ from RMS 9.56% to 8.78%; the best single-exponent scan reaches 8.70%. **No single golden rule fits all four references below ~8.7%** -- the threshold mechanism is confirmed, the clean closure remains open.

### 5.6 The Plonk-Scale Substrate (Phases 23--24)

The plonk-scale simulation implements the $720^{\circ}$ double-cover of the Klein bottle explicitly, addressing the missing ingredient identified in Phases 19--22 (grid harmonics and gain saturation corrupting the naive balloon models).

**Fibonacci lattice.** Golden-angle spiral positioning on the Klein surface produces correlated phase-position ordering.

**4-tick orientation cycle.** Each oscillator advances one quarter of the full Klein circumference per plonk tick; after 4 ticks ($720^{\circ}$), all oscillators return to their original chirality. The spin-1/2 double-cover is verified at 200/200.

![**Plonk-cycle dynamics on the Klein bottle.** The 4-state orientation tracker encodes the $720^{\circ}$ double-cover; parity inversion through the Möbius seam is encoded as sign flips in the coupling matrix (Phase 23a output).](publication/figures/plonk_cycle.png)

**Parity-inverted coupling.** The shortest geodesic either stays on the same sheet or crosses the Möbius seam, encoded as a sign flip (44.6% of coupling entries negative). This prevents the uniform saturation that plagued earlier balloon models and stabilizes amplitudes at ~0.91.

**Stable knots.** Knots form at ~3% per 4-tick cycle, robust across all parameter variations (Phase 24 sweep over $\omega_0$, gain, $\sigma$, TOL, $N$), independent of the golden filter's tolerance parameter -- the topological structure is the primary driver.

![**Parameter scan.** Stable-knot fraction is robust at ~3% across variations in $\omega_0$, gain, $\sigma$, and TOL; the golden filter is secondary to the Fibonacci lattice topology (Phase 24 output).](publication/figures/param_scan.png)

**QM diagnostics** (Phase 23b): 100% chirality flip at $180^{\circ}$ (spin-1/2), constructive/destructive superposition cycling, entanglement via twist-geodesic pairs, and phase-space uncertainty $\Delta x \Delta p = 0.32$ vs the plonk bound 0.031.

**Conclusion of the computational program.** The golden ratio acts at the **structural level** -- Fibonacci lattice positions and parity inversion through the Klein twist -- rather than as a tunable filter parameter.

## 6. Quantum-Scale Derivations: The Half-Integer Twist and the Particle Spectrum

The framework's most secure quantitative claims are top-down ratio tests at the quantum scale (Phases 27--35), all traced to the single half-integer twist $\theta = 1/2$.

### 6.1 The Half-Integer Twist (Phases 25, 29)

Phase 25 implements the Compression Operator as the **temporal holonomy** of an SU(2)-like connection over the closed $720^{\circ}$ cycle. In the flat limit the 4-tick Wilson product is *exactly* $-I$ to machine precision -- the fermionic sign of the spin-1/2 double-cover. The parity gauge flips chirality at tick 2 and restores it at tick 4.

Phase 29 derives the factor-2 from this structure. The orientation-reversing seam imposes the meridian boundary condition $\theta = \pi\ell/n_{\text{mer}}$ with $\ell$ **odd**, halving the momentum relative to the torus (verified: momentum ratio exactly 0.5; the Klein gap $4\sin^2(\pi/2n)$ matches the odd-$\ell$ analytic value to 1e-6). A charge living on the Klein meridian is anti-periodic: its single-valued unit is half the orientable unit, so $\Xi_{\text{eff}} = 1/2$.

### 6.2 The Neutron Factor-2 (Phases 28--30)

The plan's literal $\delta_n = \alpha/\varphi^2$ overshoots the neutron excess by 2.02×. The half-integer twist gives the leading factor $1/2$, and the same $\theta = 1/2$ enters the radiative sector as $f_{\text{Klein}} = 1 + |\theta| = 3/2$; the triple-golden suppression $1/\varphi^6$ completes the correction:

$$\delta_n = \frac{\alpha}{2\varphi^2}\left(1 - \left(\tfrac{3}{2} - \tfrac{\alpha}{\varphi^6}\right)\alpha\right),$$

reproducing $m_n$ to **0.02σ of CODATA 2018** [8]. The exact coefficient $c = 1.4995935$ agrees with $3/2 - \alpha/\varphi^6 = 1.4995933$ to 1.6e-7. The leading $1/2$ is derived (Phase 29); the $3/2$ and $\alpha/\varphi^6$ terms are radiative corrections consistent with the associator algebra, not yet independently derived.

### 6.3 The Parameter-Free Mass Ratio (Phase 27)

Dividing the proton and electron mass formulas cancels *both* $\alpha$ and $\varphi^2$, giving the exact prediction

$$\frac{m_p}{m_e} = 6\pi^5 = 1836.118 \quad\text{vs}\quad 1836.153 \text{ observed}\quad (99.9981\%).$$

This is IST's strongest top-down test: no free parameters at all. The electron mass factor $12\pi^5 = 2 \times 6 \times \pi^5$ decomposes into the double-cover (Section 6.4), the three lepton generations, and the topological harmonic factor, per the companion derivation [9]; the ratio $6\pi^5$ survives the division by the proton's spin factor.

### 6.4 The Koide Relation and the Muon (Phase 31)

The Koide relation $Q = \frac{m_e + m_\mu + m_\tau}{(\sqrt{m_e} + \sqrt{m_\mu} + \sqrt{m_\tau})^2} = 2/3$ holds to **0.0009%** with CODATA 2018 masses [8]. $Q = 2/3$ is equivalent to a Koide phase $\pi/2$ (measured 90.000374°, 6.5 μrad from $\pi/2$) -- the same $\theta = 1/2$ that derives the neutron factor-2. The three lepton generations are a three-fold phase fan at three $2\pi/3 = 120^{\circ}$ offsets wrapping the $720^{\circ}$ double-cover.

**Honest scope.** The muon sits on the double-cover's back sheet (negative Koide amplitude), which is why the naive $m_\mu/m_e \approx 3/(2\alpha)$ reaches only 99.41%. $Q$ is invariant to the sheet choice and is the robust observable; the individual ratio is not yet derived.

### 6.5 The Quark Sector (Phase 32)

The one-twist Koide test on quarks gives an honest falsification map: the heavy generation (c,b,t) is consistent with $Q = 2/3$ at 0.45% (edge of pole-mass systematics; the MS-bar scheme gives 8%); every triplet involving the light quarks is broken. The $\pi/2$ twist survives where the topological mass dominates -- the heavy generation -- and is washed out where light-quark masses are RG/scheme-dominated. This is a *falsification map*, not a confirmation.

### 6.6 The Baryon Decuplet (Phases 34--35)

The baryon spectrum maps onto the energy quantum $E = \hbar c/1\text{ fm} = 197.33$ MeV. Phase 35 derives the nucleon coefficient:

$$m(S) = \left[4 + \tfrac{k}{2}f_{\text{Klein}}\right]E, \qquad f_{\text{Klein}} = \tfrac{3}{2}, \qquad k = 1, 3, 4, 5, 6,$$

where the base 4 is the double-cover (four plonk ticks of the $720^{\circ}$ cycle) and each strangeness step adds half $f_{\text{Klein}}$:

| Baryon | k | m/E | predicted (MeV) | observed (MeV) | |
|---|---|---|---|---|---|
| N | 1 | 19/4 | 937.30 | 938.92 | −0.17% |
| Δ | 3 | 25/4 | 1233.29 | 1232.00 | +0.11% |
| Σ* | 4 | 7 | 1381.29 | 1383.70 | −0.17% |
| Ξ* | 5 | 31/4 | 1529.28 | 1531.80 | −0.16% |
| Ω | 6 | 17/2 | 1677.28 | 1672.45 | +0.29% |

**Honest scope.** The decuplet is the clean object (≤0.29%); the octet does NOT fit a single ladder ($\Lambda$–$\Sigma$ mixing not captured). The $\Delta$ anchor and the 1-fm scale retain a combined ~1% ambiguity.

### 6.7 The Master-Equation Correction (Phase 33)

The original master equation wrote the associator term as $(\alpha/\varphi^2)\Xi$; the neutron derivation requires the associator term to carry the twist. The corrected form

$$M = \frac{f}{2\pi}I_{\text{topo}} + \frac{\alpha}{\varphi^2}\,\Xi_{\text{eff}}\,(1 - c\alpha) + \delta_{\text{tc}},$$

with $\Xi_{\text{eff}} = 1 - \theta$, $c = 2\theta(f - \alpha/\varphi^6)$, $f = 1 + |\theta|$, reduces *exactly* to the original at $\theta = 0$ (proton/electron unchanged at 99.95%) and fixes the neutron at 0.02σ for $\theta = 1/2$. This is a framework correction, not a new free parameter.

## 7. The Zero-Point Operator and the $720^{\circ}$ Double-Cover

### 7.1 Overview

We define the Zero-Point Operator $\Omega$, a specialization of the Compression Operator $\Psi$ that acts in regions of vanishing fold density. The goal is twofold: (i) formalize $\Omega$ as a geometric limit of $\Psi$, and (ii) describe how "collapse/expansion" dynamics can be interpreted as a substrate-level mechanism for self-referential information automata. In the flat limit the double-cover holonomy is exactly $-I$ (Section 6.1), and a parity inversion flips chirality at one twist crossing, restoring it only after a full $720^{\circ}$ traversal.

### 7.2 The Zero-Point Limit

In regions of vanishing fold density, $\Psi$ approaches $\Omega$, the behavior of the operator when the substrate can no longer sustain local curvature. The collapse is a topological necessity: in low-density regions, non-orientability forces self-intersection, and $\Omega$ formalizes how information is conserved through this process. The substrate computes its own state updates without external agency -- the 4-tick plonk cycle demonstrates this self-referential structure.

### 7.3 Temporal Consistency and Boundary Conditions

The probabilistic axiom of the directed-number algebra suggests that what appears as quantum randomness may be epistemic, determined by global boundary conditions inaccessible to local observers. The zero-point operator restricts allowable histories to enforce a global consistency condition. We emphasize that "retrocausal" is used only operationally: constraints from future boundary data can influence present conditional probabilities, without a superluminal mechanism. This is a working interpretation, not a derived claim.

## 8. Critical Analysis and Discussion

### 8.1 The Mechanism

The arc across 42 phases converges on a single picture: $\varphi$ is not written into the substrate's spatial structure. It emerges from the temporal dynamics of harmonic self-interaction through three interconnected mechanisms -- anti-resonance selection, the vacuum-pump laser threshold, and dynamical RG convergence -- with fold-density feedback closing the loop so that $G_{\text{eff}}$ converges to $\rho^{1/\varphi}$ from any initial condition.

### 8.2 Honest Negatives

- **Force couplings are not golden harmonics (Phase 37).** At the fixed scale, only $em/weak \approx \varphi^3$ (2.3%); $weak/strong$ and $em/strong$ are ~19–22% off. The simplest harmonic-unification formulations are **not supported**. The golden-harmonic evidence lives in the *mass spectrum*, and the couplings are the slaved running between the mass harmonics (Phase 38, Section 5.5).
- **Dimensional crystallization is CMB-excluded at recombination (Phase 36).** A $D \to 2$ early universe gives a shift parameter $R \approx 6$ vs observed 1.7502 — excluded by ~985σ. Crystallization must complete before recombination; $D \approx 3$ at all observable $z$. The 60 $H(z)$ chronometers cannot distinguish the transition from $\Lambda$CDM.
- **The self-referential "137" fixed point is retracted (Phase 42, H42g).** The relation $\alpha^{-1} = 360/\varphi^{2+\alpha}$ has a fixed point at 137.026 (0.0075% off CODATA), but it fails the project's four golden-relation robustness checks: the equation is non-unique (a second spurious root at 0.0625), base-unspecific (a 0.09% band of bases fits equally well), unit-fragile (degrees → 137, radians → 1.85), and exponent-free (14 exponents in [1.5, 2.5] reach the same precision). Reported as a cautionary example of over-fitting, not as a claim.

### 8.3 Comparison to Alternative Frameworks

The $\varphi$-attractor mechanism offers a distinct path to generating dimensionless constants. Unlike string-theory moduli (typically tuned) or anthropic arguments (not predictive), anti-resonance selection provides a dynamical mechanism for why $\varphi$ emerges. Independent proposals for the golden ratio as a stable IR fixed point in nonlocal field theories [1] are complementary to this mechanism. The connection to established quantum gravity frameworks (e.g., Loop Quantum Gravity, asymptotic safety) remains to be formalized.

### 8.4 Outlook

The stable-knot fraction of ~3% must be mapped to Standard Model particle multiplicities; the clean golden closure of the $\alpha_s$ flavor running (best 8.7%) remains open; and the octet's $\Lambda$–$\Sigma$ mixing is uncaptured by the E-ladder.

## 9. Conclusion

Information Substrate Theory provides a framework in which observed physics emerges from a discrete, non-orientable two-dimensional information substrate. A 42-phase computational program (510 automated tests) establishes that the golden ratio $\varphi$ is not a static invariant of the substrate graph but a **dynamical attractor** of its harmonic self-interaction.

**Key results:**
- Parameter-free $m_p/m_e = 6\pi^5$ (99.9981%); neutron excess at 0.02σ of CODATA; Koide $Q = 2/3$ (0.0009%); baryon decuplet ladder ≤0.29% — all traced to the half-integer twist $\theta = 1/2$ (the $720^{\circ}$ double-cover)
- Strong coupling via mass→coupling relation: $M_Z$ 3.1%, $m_\tau$ 1.3%; active-flavor threshold mechanism confirmed (best RMS 8.7%, clean closure open)
- Oscillatory dark energy preferred over $\Lambda$CDM at ~4σ; void-lensing suppression 63% distinguishable at $10.7\sigma$; first stacked DES Y6 shear signal
- Honest negatives reported: force couplings not golden harmonics; crystallization CMB-excluded at recombination; the "137" fixed point retracted by robustness checks

The framework is offered as a work in progress whose claims are intended to be evaluated and revised against observation.

## Appendices

### Appendix A: Phase Map

| # | Name | Key Finding |
|---|---|---|
| 1 | Klein spectrum | Gap ratios falsify bare-grid $\varphi$ |
| 2 | Hopf $\alpha$ | Form correct, scale needs $\varphi^8$ |
| 3 | Mass hierarchy | p/e at 99.9%+, $\alpha_s = 0.38$ (gap, closed Ph 15) |
| 4 | Variable G | $D_{\text{eff}}$ crosses $\varphi$ at $f \approx 4.2$ |
| 5 | Observable validation | Void lensing 10.7σ forecast |
| 6 | $\varphi$-attractor | Golden = maximal anti-resonance |
| 7 | Vector substrate | $D_{\text{eff}} \approx 1.10$, self-similar, not grid-D=2 |
| 8 | Vacuum pump | Laser threshold at layer 11 |
| 9 | GoL automaton | Golden fraction 0.54→0.77 |
| 10–11 | Klein vector field / golden-filtered substrate | Twist correlation emerges; edge-level golden weights |
| 12 | Fibonacci RG | Static blocking fails |
| 13 | Dynamical RG | $D_{\text{eff}}$ pins at 1.655 (2.3% of $\varphi$) |
| 14 | Fold feedback | $G$ exponent → $1/\varphi$ from any initial $f$ |
| 15 | Running $\varphi$ | $\alpha_s$ fixed (3%), neutron exact, $\beta = \varphi^3$ |
| 16 | Joint fit | Oscillatory DE at 4σ over $\Lambda$CDM |
| 17 | DES void lensing | Real shear stacking (3 voids, ~0.025) |
| 19–22 | Unified sim / balloon models | Grid harmonics + gain saturation → corrected in 23–24 |
| 23 | Plonk-scale | Fibonacci lattice + 4-state tracker + 720° verified (200/200) |
| 24 | Parameter scan | Stable fraction ~3% robust; topology primary |
| 25 | Temporal holonomy | $\Psi$ = Wilson loop of SU(2) connection; flat limit EXACTLY $-I$; static-$\varphi$ falsification reproduced |
| 27 | QM-scale ratio validation | Parameter-free $m_p/m_e = 6\pi^5$ (99.9981%); factor-2 neutron found |
| 28 | Factor-2 neutron | $\delta_n = (\alpha/2\varphi^2)(1-(\tfrac{3}{2}-\alpha/\varphi^6)\alpha)$ at 0.02σ |
| 29 | Factor-2 derivation | The 2 = half-integer Klein meridian quantization (odd-$\ell$); the 720° double-cover |
| 30 | Radiative (3/2)α derived | $f_{\text{Klein}} = 1 + |\theta| = 3/2$; full $\delta_n$ at 0.02σ |
| 31 | One-twist muon (Koide) | $Q = 2/3$ to 0.0009%; phase at 6.5 μrad from $\pi/2$; muon on back sheet |
| 32 | Quark-sector Koide test | Heavy (c,b,t) consistent (+0.45%); light broken — a falsification map |
| 33 | Master-equation correction | Twist-dependent associator; reduces to original at $\theta = 0$ |
| 34 | Baryon mass ladder | Decuplet ≤0.27%; octet honest (mixing open) |
| 35 | Double-cover baryon derivation | $m(S) = [4 + (k/2)f_{\text{Klein}}]E$; 19/4 derived; decuplet ≤0.29% |
| 36 | Dimensional crystallization | $D \to 2$ early universe CMB-excluded (~985σ); crystallization precedes recombination |
| 37 | Force harmonics test | Couplings NOT golden harmonics — evidence is in the mass spectrum |
| 38 | Mass-coupling relation | $\alpha_s(E) = (1/\varphi^2)\varphi^{-n(E)}$: M_Z 3.1%, $m_\tau$ 1.3% |
| 39 | Active-flavor thresholds | Mechanism confirmed; free fit cuts $m_b$ 19.5%→3.0% |
| 40 | Bell non-locality | Substrate singlet → CHSH 2.83; non-locality is a projection artifact |
| 41 | Measurement problem | Collapse as entropic crystallization; strict unitarity |
| 42 | Flavor closure + 137 test | Boundary convention resolved (RMS 8.78%); "137" fixed point RETRACTED (fails robustness checks) |

### Appendix B: Code and Data Availability

All code, tests, and outputs at: `https://github.com/MaryTheadoor/IST-workspace-`

- 42 phases, 510 automated tests (pytest)
- Plonk-scale substrate: 4-state orientation tracker, parity-inverted coupling, Fibonacci lattice
- QM diagnostic suite: spin, superposition, entanglement, uncertainty
- Golden-relation robustness checks (`golden_relation_checks.py`): uniqueness, base-specificity, unit-invariance, parameter-freedom
- Real data: DES Y6 GOLD (`Y6_GOLD_2_2-0-0000.parquet`, 3.5 GB), Pantheon+ SNe Ia (1701 events), DESI DR1 BAO (5 redshift bins), H(z) cosmic chronometers (60 points)
- Figures and CSVs in `code/outputs/phase*/`
- Derivation documents in `supplementary/phase*/`

## References

[1] A. Solis. Golden Ratio as a Stable Infrared Fixed Point in Nonlocal Field Theories. arXiv preprint (2025).

[2] Scognamiglio, D. et al. COSMOS-Web: A Synthetic JWST Survey for Void Lensing Anomalies. The Astrophysical Journal, in press (2026).

[3] NOWN Research Collective. Directed Numbers and Zero-Point Operators: An Algebraic Formalism for Topological Information Conservation. Internal document v0.7 (2026).

[4] van der Mark, M.B. & 't Hooft, G.W. Light is Heavy. arXiv:1508.06478v1 [physics.hist-ph] (2015).

[5] Williamson, J.G. & van der Mark, M.B. Is the electron a photon with toroidal topology? Annales de la Fondation Louis de Broglie, 22, 133 (1997).

[6] Khinchin, A. Ya. Continued Fractions. University of Chicago Press (1964).

[7] Arnold, V. I. Proof of a theorem of A. N. Kolmogorov on the preservation of conditionally periodic motions. Russian Mathematical Surveys, 18(5), 9-36 (1963).

[8] CODATA Task Group on Fundamental Constants. 2022 CODATA Recommended Values. Available at https://physics.nist.gov/cuu/Constants/ (2022).

[9] NOWN Research Collective. Decomposition of the Electron Mass Factor $12\pi^5$. Supplementary derivation, IST-workspace repository (2026).
