# Large-D Discrete Self-Similarity: IST Mapping

**Date:** 2026-06-04  
**Paper:** Ecker, Ecker & Grumiller (2026) — *Analytic discrete self-similarity in the large-D limit*

---

## Summary

Ecker et al. study spherically symmetric Einstein-massless-Klein-Gordon collapse in $D$ spacetime dimensions. Using the large-$D$ expansion, they reduce the full PDE system to a single free function of time $\beta(\tau)$, showing that critical collapse exhibits **discrete self-similarity (DSS)** with a calculable echoing period $\Delta$.

This paper connects directly to several IST concepts: the running coupling ($1/D \leftrightarrow \alpha_{\text{topo}}$), the time crystal ($\Delta \leftrightarrow \delta_{\text{tc}}$ period), and the associator as a higher-order topological correction.

---

## Key Results from Ecker et al.

1. **Reduction to free function:** In the large-$D$ limit, the Einstein-Klein-Gordon equations reduce to a single ODE governed by $\beta(\tau)$, where $\tau = -\ln(t_0 - t)$ is the logarithmic time to collapse.

2. **Echoing period:** The condition for discrete self-similarity is $\beta(\tau + \Delta) = \beta(\tau)$ with $\Delta = |\beta''|/(3|\beta'|)$ at $\beta = 0$. This selects a **unique echoing period** at next-to-leading order.

3. **Spacetime crystal:** The authors explicitly call the DSS solution a "spacetime crystal" — a self-similar repeating structure in logarithmic time.

4. **NEC lines:** The NEC (null energy condition) lines are loci where the Ricci scalar vanishes. They bend only at NNLO, suggesting the associator's influence is a higher-order effect.

---

## Mapping to IST Directed Numbers

| Large-D DSS Concept | IST Analogue |
|--------------------|--------------|
| $\beta(\tau)$ (free function of time) | Integration function determining the compression/expansion schedule in a `TemporalThread` |
| SSH function $f(x,\tau)$ | Twist factor in the Klein bottle metric |
| Echoing period $\Delta$ | Period of the time crystal $\delta_{\text{tc}}$ |
| Naked singularity | Directed zero at the centre (information compressed but not destroyed) |
| NEC lines | Contours of constant associator charge $\Xi$ |
| $1/D$ expansion parameter | Topological coupling $\alpha_{\text{topo}} \sim \Xi / I_{\text{topo}}^{3/2}$ |

---

## Key Connections

### 1. Discrete Self-Similarity and Directed Numbers

The periodicity $\beta(\tau + \Delta) = \beta(\tau)$ is a **discrete symmetry** akin to the periodic boundary conditions in our `TemporalThread`. The condition $\Delta = |\beta''|/(3|\beta'|)$ at $\beta = 0$ is a **quantization condition** — it picks out specific echoing periods. This mirrors the idea that the associator charge $\Xi$ may be quantized.

### 2. Large-D Expansion as a Running Coupling

The $1/D$ expansion is analogous to the renormalization group flow of the topological coupling $\alpha_{\text{topo}}$ in IST (Plan 7). Here, $1/D$ is the small parameter; there, it is $\alpha_{\text{topo}} \sim \Xi / I_{\text{topo}}^{3/2}$. Both control the approach to a critical solution.

### 3. Naked Singularity and Information

The naked singularity at the centre (future endpoint of the self-similar horizon) is avoided in IST by the **information density limit** — instead of a singularity, we have a maximally compressed directed zero state. However, the DSS solution's structure (centre → SSH → Cauchy horizon) could be reinterpreted in IST as a **hierarchical knot untangling process**.

### 4. NEC Lines and the Associator

The NEC lines are loci where the Ricci scalar vanishes. In IST, the Ricci scalar is related to the associator term. The fact that NEC lines bend only at NNLO suggests that the **associator's influence is a higher-order effect** in $1/D$, which corresponds to the running of $\Xi$ with scale in IST.

---

## IST Interpretation

The large-$D$ DSS solution can be mapped onto the directed numbers framework:

- The free function $\beta(\tau)$ determines the **compression/expansion schedule** — when `Omega()` and `Omega_inv()` are applied in a `TemporalThread`
- The twist factor $f(x,\tau)$ is the **Klein bottle metric** — encoding the non-orientability of the horizon
- The echoing period $\Delta$ is the **time crystal oscillation period** — matching the dominant frequency we observed in the Plan 10 simulation ($f \approx 0.00125$)
- The naked singularity is a **directed zero** — information is compressed, not destroyed
- The NEC lines are **contours of constant $\Xi$** — mapping the associator charge distribution across the collapse spacetime

### Prediction

The condition (20) from Ecker et al. that selects a unique echoing period at NLO may be the same mechanism that would **quantize the associator charge** in IST. In our PBH analysis (Plan 10 Phase A), $\Xi$ clustered around a narrow range ($\log_{10}\Xi \approx 33.8 \pm 0.25$) rather than a single integer — but this could be due to finite measurement precision. More precise PBH mass measurements could reveal quantization.

---

## References

- Ecker, Ecker & Grumiller (2026). *Analytic discrete self-similarity in the large-D limit.*
- IST Plan 7 — Topological Cosmology (Running Coupling)
- IST Plan 8 — Beta Function and TQFT
- IST Plan 10 — Time Crystal Simulation
