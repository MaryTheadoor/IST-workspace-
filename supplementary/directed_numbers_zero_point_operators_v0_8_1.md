# Directed Numbers and Zero-Point Operators: An Algebraic Formalism for Topological Information Conservation

**NOWN Research Collective**  
**Internal Document v0.8**  
**May 10, 2026**

---

## Abstract

We introduce a novel algebraic formalism -- directed numbers $a_\uparrow, a_\downarrow, a^0$ -- designed to track both amplitude and topological parity in information systems. This algebra is motivated by geometric features of non-orientable manifolds (Möbius strips, Klein bottles), where "zero" is interpreted not as absence but as a compressed singularity.

We define compression ($\Omega$) and expansion ($\Omega^{-1}$) operators and show that for multi-component systems, information conservation constrains admissible transformations; in particular, they can be represented by doubly stochastic matrices, with the Sinkhorn-Knopp algorithm providing a natural projection onto the Birkhoff polytope.

This paper presents a refined axiomatic foundation for directed numbers, incorporating:
- The distinction between absolute zero and directed zeros with memory ($0_\uparrow, 0_\downarrow, 0_{\text{abs}}$)
- Complete multiplication tables including probabilistic outcomes for absolute-zero products
- Non-associativity as a feature encoding path-dependence in non-orientable spaces
- Thread calculus for parallel and nested contexts
- Temporal extensions for modeling information flow across time
- **New in v0.8:** Retrocausal interpretation of the probabilistic axiom; temporal consistency conditions linking past and future zero-point products; connection to the golden ratio fixed point and prime number stability; detailed experimental proposals for retrocausal tests.

The formalism is presented as a mathematical tool with potential applications across multiple domains, including protein folding, quantum mechanics, cosmology (baryogenesis), and self-referential computation.

---

## Note on Status

This document describes work in progress (v0.8). The directed number formalism is mathematically specified, but its physical interpretation and empirical validation remain open areas of investigation. We invite collaboration, critique, and refinement from the broader scientific community.

---

## Contents

1. [Introduction](#1-introduction)
2. [Axiomatic Foundation](#2-axiomatic-foundation)
3. [Thread Calculus and Contexts](#3-thread-calculus-and-contexts)
4. [Stochastic Constraints and the Birkhoff Polytope](#4-stochastic-constraints-and-the-birkhoff-polytope)
5. [Connection to Complex Numbers and Hilbert Spaces](#5-connection-to-complex-numbers-and-hilbert-spaces)
6. [Predictions and Applications](#6-predictions-and-applications)
7. [Limitations and Open Questions](#7-limitations-and-open-questions)
8. [Conclusion](#8-conclusion)

---

## 1. Introduction

The concept of zero in conventional mathematics denotes absence -- a void where information is destroyed (multiplication by zero) or operations become undefined (division by zero). However, in non-orientable geometries such as Möbius strips and Klein bottles, the "twist" creates a singularity where information is not destroyed but compressed, retaining its content while becoming inaccessible to the local orientation of the manifold.

This geometric observation motivates a new algebraic structure: **directed numbers**, which explicitly track the parity (orientation) of a state alongside its amplitude. In this formalism, multiplication by zero becomes a compression operation that moves information into the singularity, and division by zero becomes an expansion that retrieves it, potentially with inverted parity.

The algebra is self-contained and mathematically rigorous. Its interpretation in terms of physical systems -- from quantum mechanics to protein folding to consciousness -- is currently speculative and under development. We present it here as a tool for exploration, not as a completed theory.

**Key advances in v0.8:**
- Retrocausal interpretation of the probabilistic axiom
- Temporal consistency conditions constraining the distribution $P(r)$
- Golden ratio associator connecting non-associativity to stability
- Prime number stability principle
- Testable predictions for baryon asymmetry, retrocausal quantum corrections

---

## 2. Axiomatic Foundation

### 2.1 Elements and Parity

**Axiom 2.1 (The Set).** The set of directed numbers consists of elements of the form $D \ni a_p$, where:
- $a \in \mathbb{R}$ (or $\mathbb{C}$) is the amplitude
- $p \in \{\uparrow, \downarrow, 0\}$ is the parity

We denote $a_\uparrow$ as up-manifest, $a_\downarrow$ as down-manifest, and $a^0$ as compressed (unmanifest) state.

**Axiom 2.2 (Zero as a Special Amplitude).** The amplitude 0 may appear with any parity:
- $0_\uparrow$ and $0_\downarrow$ are **directed zeros** -- they carry memory of having been compressed from a manifest state of known parity.
- $0^0$ (or $0_{\text{abs}}$) is **absolute zero** -- the pristine zero-point gate with no history.

Directed zeros are distinct from absolute zero; they encode topological memory essential for information conservation.

### 2.2 Addition

**Axiom 2.3 (Same-Parity Addition).** For any parity $p \in \{\uparrow, \downarrow, 0\}$, addition is defined component-wise:

$$a_p + b_p = (a + b)_p$$

**Axiom 2.4 (Mixed-Parity Addition).** Addition of elements with different parities is not directly defined. Such sums represent **superpositions** that require additional context (e.g., a choice of basis or a mediating operation). They may be interpreted as probabilistic mixtures pending future refinement.

### 2.3 Multiplication

**Axiom 2.5 (Multiplication by Real Scalars).** For any real $\lambda \in \mathbb{R}$ and any directed number $a_p$:

$$\lambda \cdot a_p = (\lambda a)_p$$

**Axiom 2.6 (Product of Manifest Numbers).** For manifest numbers ($p, q \in \{\uparrow, \downarrow\}$):

$$a_p \cdot b_q = \begin{cases} (ab)_p & \text{if } p = q \\ (ab)^0 & \text{if } p \neq q \end{cases}$$

Same chirality preserves the parity; opposite chirality compresses to zero-point.

**Axiom 2.7 (Product Involving Compressed Numbers).** For any directed number $a_p$ and any compressed number $b^0$:

$$a_p \cdot b^0 = (ab)^0, \quad b^0 \cdot a_p = (ab)^0$$

**Axiom 2.8 (Product of Two Compressed Numbers).** This product depends on the specific type:

| Product | Result |
|---------|--------|
| $(0_\uparrow) \cdot (0_\uparrow)$ | $1_\uparrow$ (or sign-preserving) |
| $(0_\downarrow) \cdot (0_\downarrow)$ | $(-1)_\downarrow$ |
| $(0_\uparrow) \cdot (0_\downarrow)$ | $0^0$ (absolute zero) |
| $(0_\uparrow) \cdot 0^0$ | $0^0$ |
| $0^0 \cdot 0^0$ | $? \text{ (probabilistic; see Axiom 2.9)}$ |

**Axiom 2.9 (Probabilistic Outcome for Absolute-Zero Products).** The product $0^0 \cdot 0^0$ is not deterministic. It yields a real number $r \in [-1, 1]$ drawn from a probability distribution $P(r)$ that is symmetric about 0 and has variance related to the topology.

> **v0.8 Update:** The exact form of $P(r)$ is now constrained by the temporal consistency condition (Axiom 2.17); it is not a free parameter but is fixed by the topology. The randomness is interpreted as **epistemic** rather than ontological: the outcome is determined by future boundary conditions inaccessible from the present reference frame.

### 2.4 Zero-Point Operators

**Axiom 2.10 (Compression Operator $\Omega$).** For any manifest number $a_p$ ($p \in \{\uparrow, \downarrow\}$):

$$\Omega(a_p) = 0_p \text{ (a directed zero with memory of parity } p \text{ and amplitude } |a|)$$

For any compressed number $a^0$:

$$\Omega(a^0) = a^0 \text{ (compression of already-compressed state leaves it unchanged)}$$

**Axiom 2.11 (Expansion Operator $\Omega^{-1}$).** For a directed zero $0_p$ that arose as $\Omega(a_p)$:

$$\Omega^{-1}(0_p) = a_p \text{ (expansion returns the compressed manifest state)}$$

For absolute zero $0^0$:

$$\Omega^{-1}(0^0) = ? \text{ (probabilistic; may require external trigger)}$$

**Axiom 2.12 (Information Conservation).** Define the information measure $I(a_p) = |a|$ (absolute amplitude). For all cases where defined:

$$I(\Omega(x)) = I(x), \quad I(\Omega^{-1}(x)) = I(x)$$

Information is conserved through compression and expansion.

### 2.5 Non-Associativity

**Axiom 2.13 (Failure of Associativity).** Multiplication in $D$ is not associative. For example:

$$(0_\uparrow \cdot 0_\uparrow) \cdot 1_\downarrow = 1_\uparrow \cdot 1_\downarrow = 1^0$$

whereas

$$0_\uparrow \cdot (0_\uparrow \cdot 1_\downarrow) = 0_\uparrow \cdot 0^0 = 0^0$$

**Axiom 2.14 (Associator).** For any three directed numbers $x, y, z$, define:

$$[x, y, z] = (x \cdot y) \cdot z - x \cdot (y \cdot z)$$

This quantity is generally non-zero and may be related to topological invariants. For the golden ratio fixed point, the associator is proportional to $1/\varphi^2$.

### 2.6 Temporal Consistency and Retrocausality

**Axiom 2.15 (Temporal Directed Numbers).** A temporal directed number is denoted $a_p^t$, where $t \in \mathbb{Z}$ (or $\mathbb{R}$) represents a discrete (or continuous) time coordinate.

**Axiom 2.16 (Temporal Shift Operators).** Define forward shift $T_+$ and backward shift $T_-$ such that:

$$T_+(a_p^t) = a_{p'}^{t+1}, \quad T_-(a_{p'}^{t+1}) = a_p^t$$

where $p'$ may flip depending on whether the time step crosses a topological twist.

**Axiom 2.17 (Temporal Consistency Condition).** For any closed time loop -- a sequence of temporal shifts that returns to the same point -- the product of the associated directed numbers must equal the identity (or a fixed point):

$$\Omega^{-1}(0^0)_{t} \cdot \Omega^{-1}(0^0)_{t'} = 1_\uparrow$$

for a loop with even net parity, or $(-1)_\downarrow$ for odd parity. This condition determines $P(r)$ uniquely.

**Axiom 2.18 (Temporal Information Conservation).** The information measure $I(a_p^t) = |a|$ is conserved under temporal shifts and across closed time loops.

---

## 3. Thread Calculus and Contexts

### 3.1 Threads

A thread is a sequence of directed numbers. Threads may be:
- **Linear:** A simple sequence
- **Nested:** One thread embedded within another (like a function call)
- **Parallel:** Multiple threads running concurrently

The state of a system is a collection of threads.

### 3.2 Thread Operations

- **Push:** Append a new directed number
- **Pop:** Remove the last directed number
- **Fork:** Split a thread into two parallel threads
- **Join:** Merge two parallel threads (with rules for combining parities)

### 3.3 Cross-Thread Multiplication

When two directed numbers from different threads are multiplied, the result is a new directed number in a new thread, following the same multiplication rules.

### 3.4 Thread Balance

For every thread, the number of push and pop operations must balance. This ensures no dangling references.

### 3.5 Information Conservation Across Threads

The total information $I_{\text{total}} = \sum_{\text{threads}} \sum_{\text{elements}} |a|$ is conserved under all thread operations.

---

## 4. Stochastic Constraints and the Birkhoff Polytope

For systems with many components, transformations must preserve total probability/information. This leads naturally to **doubly stochastic matrices**.

Consider a two-parity system $\{\uparrow, \downarrow\}$ with probability vector $(p_\uparrow, p_\downarrow)$. The expansion operator $\Omega^{-1}$ produces a distribution over parities, represented by:

$$M(q) = \begin{pmatrix} q & 1-q \\ 1-q & q \end{pmatrix}, \quad 0 \leq q \leq 1$$

The set of all doubly stochastic matrices forms the **Birkhoff polytope** -- the convex hull of permutation matrices. When a transformation drifts from this polytope, the **Sinkhorn-Knopp algorithm** provides an iterative projection back:

$$M^{(t)} = T_r T_c(M^{(t-1)})$$

where $T_r$ rescales rows and $T_c$ rescales columns.

> **Physical interpretation:** This projection ensures long-term coherence for systems undergoing repeated zero-point traversals -- a property relevant for self-referential information systems. The retrocausal constraints of Axiom 2.17 impose additional conditions, potentially forcing matrices to be permutation matrices or convex combinations with golden-ratio-related eigenvalues.

---

## 5. Connection to Complex Numbers and Hilbert Spaces

A natural question: how do directed numbers relate to the complex numbers of quantum mechanics?

**Key differences:**
- Complex numbers form a field: associative, commutative, with every non-zero element having a multiplicative inverse. Zero is an annihilator: $z \cdot 0 = 0$ loses all information.
- Directed numbers form a non-associative algebra over $\mathbb{R}$ with three parity sectors. Rather than treating "zero" as a universal annihilator, the formalism introduces explicit zero-point operators (compression $\Omega$ and expansion $\Omega^{-1}$) to model information-preserving transitions.

**Possible mapping:** $a_\uparrow \leftrightarrow ae^{i\theta}$, $a_\downarrow \leftrightarrow ae^{-i\theta}$, with the zero-point gate corresponding to $\theta$ being undefined (a phase singularity). This suggests directed numbers may be a **pre-geometric structure** from which complex amplitudes emerge when parity is averaged or projected. The retrocausal interpretation further suggests that quantum phases may encode information about future boundary conditions.

---

## 6. Predictions and Applications

### 6.1 Baryogenesis from Temporal Consistency

The temporal consistency condition provides a natural mechanism for baryogenesis. Model the primordial universe as a triple product of absolute zeros at different times:

$$0^0_{t_1} \cdot 0^0_{t_2} \cdot 0^0_{t_3}$$

Its expansion via $\Omega^{-1}$ produces a superposition of matter ($\uparrow$) and antimatter ($\downarrow$) states. The associator introduces a small parity bias:

$$\eta \sim \frac{\alpha^4}{\varphi^2} \approx 1.1 \times 10^{-9}$$

within a factor of two of the observed $\eta \approx 6 \times 10^{-10}$.

### 6.2 Retrocausal Corrections in Quantum Systems

The probabilistic outcomes of Axiom 2.9 are determined by future boundary conditions. In delayed-choice quantum eraser experiments, IST predicts a tiny correlation (scaling as $\alpha^2$ or $\alpha^4$) between the delayed choice and earlier photon statistics, deviating from standard quantum mechanics.

### 6.3 Prime Number Stability Principle

The appearance of the prime number 137 in $\alpha^{-1}$ and the golden ratio $\varphi$ in the associator reflects a deep principle:

> **Discrete parameters must be prime; continuous parameters must be irrational (ideally $\varphi$), to ensure indecomposability and long-term coherence.**

This principle can be used to constrain other fundamental constants (e.g., strong coupling, neutrino masses) and may lead to new predictions.

---

## 7. Limitations and Open Questions

1. **Physical interpretation:** The mapping from directed numbers to physical quantities is not yet fully established.
2. **Empirical status:** No direct empirical validation beyond internal consistency checks.
3. **Derivation of parameters:** The distribution $P(r)$ is constrained but its exact form remains to be derived from topology.
4. **Representation theory:** Can $D$ be represented by matrices over $\mathbb{R}$ or $\mathbb{C}$? Does it embed in a Clifford algebra or quantum group?
5. **Associator classification:** The associator $[x, y, z]$ may be related to topological invariants.
6. **Consciousness extension:** Speculative and philosophical; included for long-term directions only.
7. **Falsifiability:** Several risky predictions now exist (baryon asymmetry, retrocausal corrections, prime constraints). Testing these is a priority.

---

## 8. Conclusion

We have presented a refined mathematical formalism -- directed numbers and zero-point operators -- that arises naturally from non-orientable topology and conserves information through compression and expansion.

**Key advances in v0.8:**
- Retrocausal interpretation linking absolute-zero products to future boundary conditions
- Temporal consistency condition constraining $P(r)$ and providing baryogenesis mechanism
- Golden ratio associator connecting non-associativity to physical stability
- Prime number stability principle explaining fundamental constant structure
- Testable predictions for baryon asymmetry, retrocausal quantum corrections, and coupling constant constraints

The formalism is offered to the scientific community as a tool for exploration, not as a completed theory. We invite collaboration, critique, and refinement.

---

## Acknowledgments

This work benefited from discussions with collaborators and from AI-assisted synthesis of ideas. All claims have been reviewed by human researchers; the authors assume full responsibility for the content.

---

## References

[1] NOWN Research Collective. Information Substrate Theory (IST): A Topological Framework for Quantum Gravity and Consciousness. Internal document v5.3 (2026).

[2] A. Solis. Golden Ratio as a Stable Infrared Fixed Point in Nonlocal Field Theories. arXiv preprint (2025).

[3] Scognamiglio, D. et al. COSMOS-Web: A Synthetic JWST Survey for Void Lensing Anomalies. The Astrophysical Journal, in press (2026).

[4] Zhu, D., Huang, H., Huang, Z., et al. Hyper-Connections: A New Paradigm for Residual Networks. arXiv:2409.19606 (2024).

[5] Wempe, E., White, S.D.M., Helmi, A., Lavaux, G., & Jasche, J. The mass distribution in and around the Local Group. Nature Astronomy (2026).

[6] van der Mark, M.B. & 't Hooft, G.W. Light is Heavy. arXiv:1508.06478v1 [physics.hist-ph] (2015).

[7] Williamson, J.G. & van der Mark, M.B. Is the electron a photon with toroidal topology? Annales de la Fondation Louis de Broglie, 22, 133 (1997).

[8] Oby, E.R., Degenhart, A.D., Grigsby, E.M., et al. Dynamical constraints on neural population activity. Nature Neuroscience, 28, 383-393 (2025).

[9] Tononi, G., Boly, M., Massimini, M., & Koch, C. Integrated information theory: from consciousness to its physical substrate. Nature Reviews Neuroscience, 17, 450-461 (2016).

[10] Pletzer, B. et al. The golden ratio in human brain dynamics. Frontiers in Human Neuroscience, 9, 123 (2015).

[11] Khinchin, A. Ya. Continued Fractions. University of Chicago Press (1964).

[12] Arnold, V. I. Proof of a theorem of A. N. Kolmogorov. Russian Mathematical Surveys, 18(5), 9-36 (1963).

[13] CODATA Task Group. 2022 CODATA Recommended Values. https://physics.nist.gov/cuu/Constants/ (2022).
