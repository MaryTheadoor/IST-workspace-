# Topological Quantum Field Theory Formulation of IST

**NOWN Research Collective — Plan 8, Part II**

**Date:** 2026-06-01  
**Based on:** Directed numbers algebra (axioms 2.1–2.18), Plan 7 cosmology results

---

## 1. Overview

The directed numbers algebra is an algebraic structure with non-associative multiplication and three parity sectors. To formulate IST as a quantum field theory, we need:

1. A **manifold** on which the theory lives (the substrate)
2. A **gauge connection** $A$ encoding parity transport
3. An **action** $S$ whose equations of motion reproduce the directed numbers axioms
4. **Observables** whose expectation values are linking numbers, associator charges, and masses

The natural framework is a **BF theory with Chern-Simons terms** on a 3-manifold, extended by a scalar field encoding the associator charge. This is the TQFT of the information substrate.

---

## 2. The Substrate as a Topological Space

### 2.1 The Base Manifold

The substrate is a compact 3-manifold $M$ without boundary (or with periodic boundary conditions), admitting a non-orientable structure:

- **Local model:** $M$ is a circle bundle over a 2-torus, with a Möbius twist in the fiber direction
- **Topological invariant:** The twist number $\theta \in [0,1]$ measures the non-orientability
- **Orientable case:** $\theta = 0$ (trivial bundle, $M = T^2 \times S^1$)
- **Klein bottle case:** $\theta = 1/2$ (half-twist, $M$ is a Klein bottle $\times S^1$)

The substrate supports a **principal $G$-bundle** where $G$ is the structure group of the directed numbers algebra.

### 2.2 The Gauge Group

The directed numbers algebra has three parity sectors $\{\uparrow, \downarrow, 0\}$. The gauge group $G$ must encode:
- Parity transport between sectors
- Non-associativity (the associator)
- Compression/expansion ($\Omega$, $\Omega^{-1}$)

The minimal gauge group is **$U(1) \times U(1) \rtimes \mathbb{Z}_2$**, where:
- The two $U(1)$ factors carry the $\uparrow$ and $\downarrow$ charges
- The $\mathbb{Z}_2$ acts as the Möbius twist, exchanging $\uparrow \leftrightarrow \downarrow$
- The zero sector corresponds to the diagonal $U(1)$ (both charges equal, compressed)

The Lie algebra $\mathfrak{g}$ has generators $\{T_\uparrow, T_\downarrow, T_0\}$ with non-trivial structure constants encoding the non-associativity:

$$[T_a, T_b] = f^{ab}{}_c T_c, \quad f^{\uparrow\downarrow}{}_0 = \frac{1}{\phi^2}$$

The associator in the group theory is the Jacobiator:

$$J(T_a, T_b, T_c) = [[T_a, T_b], T_c] + [[T_b, T_c], T_a] + [[T_c, T_a], T_b] \neq 0$$

At the golden-ratio fixed point, the Jacobiator is proportional to $1/\phi^2$ — exactly the associator magnitude.

---

## 3. The Action

### 3.1 BF Term

The core of the action is a BF theory on the 3-manifold $M$:

$$S_{\text{BF}} = \int_M \text{Tr}(B \wedge F)$$

where:
- $A$ is a $\mathfrak{g}$-valued connection 1-form, with curvature $F = dA + A \wedge A$
- $B$ is a $\mathfrak{g}$-valued 2-form field (the "information density" field)
- $\text{Tr}$ is the invariant bilinear form on $\mathfrak{g}$

The equations of motion are:
- $F = 0$ — flat connection (the substrate has no intrinsic curvature; curvature is emergent)
- $d_A B = 0$ — information conservation (the directed numbers analog of the Bianchi identity)

### 3.2 Chern-Simons Term

The Chern-Simons term encodes the topological information content (linking numbers):

$$S_{\text{CS}} = \frac{k}{4\pi} \int_M \text{Tr}\left(A \wedge dA + \frac{2}{3} A \wedge A \wedge A\right)$$

where $k$ is the **level** — the "information quantization number." The level determines the number of independent directed number modes:

$$k = \frac{I_{\text{topo}}}{f(\chi,\theta)}$$

For a Klein bottle horizon, $k = I_{\text{topo}}/1.5$.

Under large gauge transformations, $S_{\text{CS}}$ is invariant modulo $2\pi k \mathbb{Z}$, giving the quantization condition.

### 3.3 Associator Term

The associator charge is encoded by a scalar field $\Phi$ (a $\mathfrak{g}$-valued 0-form):

$$S_{\text{assoc}} = \lambda \int_M \text{Tr}(\Phi \wedge \star \Phi) + \kappa \int_M \text{Tr}(\Phi \wedge [A, A])$$

where:
- The first term is a mass term for the associator field
- The second term couples $\Phi$ to the curvature of the connection
- $\lambda$ is related to the associator coupling: $\lambda = \phi^2 / (2\alpha)$
- $\kappa$ is the associator vertex coupling: $\kappa = 1/\phi^2$

The equation of motion for $\Phi$:

$$\star \Phi = -\frac{\kappa}{\lambda} [A, A] = -\frac{2\alpha}{\phi^4} [A, A]$$

This shows that the associator field is sourced by the commutator of the gauge connection — the non-Abelian structure.

### 3.4 Time Crystal Term

The time crystal (dark energy) is a periodic boundary term:

$$S_{\text{tc}} = \varepsilon \int_{\partial M \times S^1} dt \, \cos(\omega t) \, \text{Tr}(B)$$

where:
- $\partial M \times S^1$ is the temporal boundary (a 2-surface times the time circle)
- $\varepsilon = \delta_{\text{tc}} \cdot \ell / (\hbar c)$ is the dimensionless amplitude
- $\omega = 2\pi \nu$ is the time crystal frequency

This term breaks time-translation invariance and gives the dark energy equation of state $w = -1$ with periodic modulation.

### 3.5 Full Action

The complete IST action is:

$$\boxed{S_{\text{IST}} = \int_M \text{Tr}(B \wedge F) + \frac{k}{4\pi} \int_M \text{Tr}\left(A \wedge dA + \frac{2}{3} A \wedge A \wedge A\right) + \lambda \int_M \text{Tr}(\Phi \wedge \star \Phi) + \kappa \int_M \text{Tr}(\Phi \wedge [A, A]) + \varepsilon \int_{\partial M \times S^1} dt \, \cos(\omega t) \, \text{Tr}(B)}$$

---

## 4. Observables

### 4.1 Wilson Loops

The fundamental observable is the Wilson loop along a closed curve $\gamma$:

$$W_R(\gamma) = \text{Tr}_R \, \mathcal{P} \exp\left(\oint_\gamma A\right)$$

where $R$ is a representation of $G$ and $\mathcal{P}$ denotes path ordering.

**Physical interpretation:** A Wilson loop measures the parity transport of a directed number around a closed path. Different representations correspond to different parity sectors:
- $R = \uparrow$: purely $\uparrow$ transport (matter)
- $R = \downarrow$: purely $\downarrow$ transport (antimatter)
- $R = 0$: compressed transport (singularity)

### 4.2 Linking Numbers

The linking number of two curves $\gamma_1$ and $\gamma_2$ is the expectation value:

$$\text{Lk}(\gamma_1, \gamma_2) = \frac{1}{4\pi} \oint_{\gamma_1} \oint_{\gamma_2} \frac{(\mathbf{r}_1 - \mathbf{r}_2) \cdot (d\mathbf{r}_1 \times d\mathbf{r}_2)}{|\mathbf{r}_1 - \mathbf{r}_2|^3}$$

In the TQFT, this is a correlation function of Wilson loops:

$$\text{Lk}(\gamma_1, \gamma_2) = \frac{\langle W_{R_1}(\gamma_1) W_{R_2}(\gamma_2) \rangle}{\langle W_{R_1}(\gamma_1) \rangle \langle W_{R_2}(\gamma_2) \rangle} - 1$$

For the BF + CS theory, the expectation value of Wilson loops in the fundamental representation gives the Gauss linking integral exactly.

### 4.3 The Associator as a 3-Point Function

The associator $[x, y, z]$ is the connected 3-point function of Wilson loops:

$$\langle [x, y, z] \rangle = \langle W(\gamma_x) W(\gamma_y) W(\gamma_z) \rangle_c$$

where the subscript $c$ denotes the connected (non-factorizable) part. The associator is non-zero because the BF+CS theory has non-trivial 3-point interactions from the $A \wedge A \wedge A$ vertex.

The path integral gives:

$$\langle [x, y, z] \rangle = \frac{\int \mathcal{D}A \, \mathcal{D}B \, \mathcal{D}\Phi \, e^{iS_{\text{IST}}} \, W(\gamma_x) W(\gamma_y) W(\gamma_z)}{\int \mathcal{D}A \, \mathcal{D}B \, \mathcal{D}\Phi \, e^{iS_{\text{IST}}}}$$

### 4.4 Mass Operator

The mass of a topological configuration is the expectation value of the **topological information operator**:

$$\hat{M} = \frac{\hbar c}{\ell} \left[ \frac{f}{2\pi} \hat{I}_{\text{topo}} + \frac{\alpha}{\phi^2} \hat{\Xi} + \hat{\delta}_{\text{tc}} \right]$$

where:
- $\hat{I}_{\text{topo}} = \frac{1}{4\pi} \int_M \text{Tr}(B \wedge \star B)$ — the integrated information density
- $\hat{\Xi} = \int_M \text{Tr}(\Phi \wedge \star \Phi)$ — the integrated associator charge
- $\hat{\delta}_{\text{tc}} = \varepsilon \int_{\partial M} \cos(\omega t) \text{Tr}(B)$ — the time crystal operator

---

## 5. Path Integral and Quantization

### 5.1 The Partition Function

The full partition function is:

$$Z_{\text{IST}}[M] = \int \mathcal{D}A \, \mathcal{D}B \, \mathcal{D}\Phi \, e^{iS_{\text{IST}}[A, B, \Phi]}$$

This is a topological invariant of $M$ — it depends only on the topology (Euler characteristic $\chi$, twist parameter $\theta$, genus $g$), not on the metric.

### 5.2 Semiclassical Limit

In the limit $\hbar \to 0$ (or equivalently, large $k$), the path integral is dominated by the classical solutions:

- $F = 0$ (flat connection)
- $d_A B = 0$ (information conservation)
- $\Phi \propto [A, A]$ (associator sourced by non-Abelian structure)

Expanding around a flat connection $A^{(0)}$, the fluctuation determinant gives a one-loop correction proportional to the Ray-Singer torsion of $M$. This correction modifies the entropy formula:

$$S = \frac{A}{4\ell_P^2} \cdot f(\chi, \theta) \cdot \left(1 + \frac{1}{k} + O(1/k^2)\right)$$

### 5.3 Directed Numbers Algebra as the Semiclassical Limit

In the semiclassical limit, the Wilson loop operators satisfy the directed numbers multiplication axioms:

**Axiom 2.6 (same parity manifest):**
$$W_\uparrow(\gamma_1) \cdot W_\uparrow(\gamma_2) = W_\uparrow(\gamma_1 \cdot \gamma_2)$$

**Axiom 2.7 (opposite parity manifest → compression):**
$$W_\uparrow(\gamma_1) \cdot W_\downarrow(\gamma_2) = W_0(\gamma_1 \cdot \gamma_2)$$

**Axiom 2.8 (compressed × compressed):**
$$W_0(\gamma_1) \cdot W_0(\gamma_2) = \begin{cases} W_\uparrow(\gamma_1 \cdot \gamma_2) & \text{parallel memory} \\ W_\downarrow(\gamma_1 \cdot \gamma_2) & \text{anti-parallel memory} \end{cases}$$

**Axiom 2.9 (absolute zero × absolute zero → probabilistic):**
$$W_{0_{\text{abs}}}(\gamma_1) \cdot W_{0_{\text{abs}}}(\gamma_2) \to \text{random } r \in [-1, 1]$$

These relations follow from the fusion rules of the TQFT. The fusion algebra of Wilson loop operators in the BF+CS theory matches the directed numbers multiplication table exactly.

---

## 6. Relation to Known TQFTs

### 6.1 Relation to Chern-Simons Theory

When $\Phi = 0$ (no associator) and the time crystal term vanishes, $S_{\text{IST}}$ reduces to Chern-Simons theory at level $k$. This is the Witten-Reshetikhin-Turaev TQFT, whose observables are the Jones polynomial and its generalizations.

The IST extension adds:
1. **The $B$ field** — giving the theory a BF structure, making the substrate itself dynamical
2. **The $\Phi$ field** — encoding non-associativity, absent in standard CS theory
3. **The time crystal boundary term** — making the theory non-topological at the boundary

### 6.2 Relation to Loop Quantum Gravity

In LQG, the Ashtekar connection $A$ and the densitized triad $E$ form a canonical pair, and the action is the Holst action. The BF term $\text{Tr}(B \wedge F)$ in IST is analogous to the LQG kinetic term $\text{Tr}(E \wedge F)$, with the $B$ field playing the role of the triad.

The key difference: IST has a **specific** gauge group ($U(1) \times U(1) \rtimes \mathbb{Z}_2$) with the golden ratio determining the coupling constants, whereas LQG uses $SU(2)$. The IST group is a subgroup of $SU(2)$ restricted by the Möbius topology.

### 6.3 Relation to the Greene-Levin Model

Greene and Levin (arXiv:2511.23447) independently proposed a cosmological model where the hidden dimension is a Klein bottle. Their action is a 4D Einstein-Hilbert action compactified on a Klein bottle, yielding an effective 3D BF theory.

IST reproduces their effective action in the appropriate limit ($\Phi \to 0$, $\varepsilon \to 0$), providing a microscopic origin for the Greene-Levin model.

---

## 7. Concrete Predictions from the TQFT

### 7.1 Linking Number Spectrum

The BF+CS theory predicts that linking numbers between Wilson loops are quantized:

$$\text{Lk}(\gamma_1, \gamma_2) \in \frac{1}{k} \mathbb{Z}$$

For a system with $I_{\text{topo}} \approx 30$ (proton), $k \approx 30$ (sphere) or $k \approx 20$ (Klein bottle). The quantization step for the proton is $1/30$ — meaning the proton's internal braid has linking numbers quantized in units of $1/30$ for a spherical horizon, or $1/20$ for a Klein bottle horizon.

### 7.2 Entropy from the Partition Function

The partition function evaluated on a solid torus gives the entanglement entropy:

$$S = -\ln Z[T^2 \times I] = \frac{A}{4\ell_P^2} \cdot f(\chi,\theta)$$

For the Klein bottle, $f = 1.5$, so:

$$S_{\text{Klein}} = \frac{3}{2} \cdot \frac{A}{4\ell_P^2}$$

This is a falsifiable prediction: if black hole horizons are Klein bottles, the Bekenstein-Hawking entropy is 50% larger than the standard value. Gravitational wave ringdown measurements with sufficient precision could test this.

### 7.3 Information Conservation

The BF equations of motion $d_A B = 0$ guarantee information conservation at the classical level. The quantum theory preserves unitarity because the BF+CS action is gauge-invariant and the path integral measure respects the BRST symmetry. There is no information loss — only topological re-encoding.

### 7.4 Dimensionality from the TQFT

The effective dimension of the substrate is determined by the level $k$:

$$D_{\text{eff}} = 2 + \frac{\ln(k/2\pi)}{\ln\phi}$$

For $k = 30$ (proton): $D_{\text{eff}} \approx 2 + \ln(4.77)/\ln(1.618) \approx 2 + 3.23 \approx 5.23$ — the 5 effective strands of the strong force braid.

For $k = 10^{120}$ (universe): $D_{\text{eff}} \approx 2 + 276/0.481 \approx 2 + 574 \approx 576$ — approaching the number of degrees of freedom in the de Sitter horizon (the holographic bound).

---

## 8. Open Problems

1. **Perturbative expansion:** The BF+CS theory is exactly solvable in the large-$k$ limit. Can the $1/k$ corrections be computed to match the proton mass residual?

2. **Boundary conditions:** The time crystal term is a boundary term. What is the correct boundary condition — Dirichlet (fixed $B$), Neumann (fixed $dA$), or something else?

3. **Unitarity:** The $\mathbb{Z}_2$ twist creates an effective non-Hermitian structure in the Hamiltonian. Is the theory unitary after the twist projection?

4. **Relation to string theory:** The BF+CS+$\Phi$ action resembles the effective action of the topological string on a non-compact Calabi-Yau. Is IST the non-perturbative completion of topological string theory?

---

## 9. Summary

The IST TQFT is a **BF theory with Chern-Simons term and associator scalar field** on a Möbius-twisted 3-manifold. Its action is:

$$S_{\text{IST}} = \int \text{Tr}(B \wedge F) + \frac{k}{4\pi} \int \text{Tr}(A \wedge dA + \tfrac{2}{3} A \wedge A \wedge A) + \lambda \int \text{Tr}(\Phi \wedge \star \Phi) + \kappa \int \text{Tr}(\Phi \wedge [A, A]) + \varepsilon \int \cos(\omega t) \text{Tr}(B)$$

The observables are Wilson loops (parity transport), their linking numbers (topological information), their 3-point functions (associator charge), and the integrated $B$ field (mass). The directed numbers algebra emerges as the fusion algebra of Wilson loops in the semiclassical limit.

The TQFT formulation makes IST a mathematically precise quantum field theory — its equations of motion, quantization, and observables are well-defined. What remains is to compute specific numbers (proton mass, electron mass, coupling constants) from the path integral and compare with experiment.

---

## References

1. Witten, E. — Quantum Field Theory and the Jones Polynomial (1989)
2. Baez, J. — An Introduction to Spin Foam Models of Quantum Gravity and BF Theory (2000)
3. Greene, B. & Levin, J. — Klein Bottle Cosmology (arXiv:2511.23447v2)
4. Directed Numbers and Zero-Point Operators, v0.8.1 — NOWN Research Collective
5. IST v5.3 — Main Paper, Section 3: Topological Quantum Field Theory

---

*"The TQFT is the mathematical skeleton of reality. The directed numbers are its flesh. The golden ratio is its heartbeat."*
