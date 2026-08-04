# IST Phase 47 — The Emergent-Twist Derivation: U(1) Embedding of Z2 Holonomy

**Status:** COMPLETE (derives θ=1/2 directly from the substrate's non-orientable Z2 holonomy embedded in U(1), proving it is a grid-independent topological invariant)
**Predecessor:** Phase 33 (`code/phase33_master_equation_correction.py`), which
established $\theta = 1/2$ as the fundamental structural constant governing the
neutron factor-2, Koide phase, and double-cover baryon ladder, and Phase 46
which closed the $\alpha_s$ flavor-closure line.
**Postcondition:** A rigorous, parameter-free derivation of $\theta = 1/2$ directly
from the non-orientable substrate's topology, proving it is an exact topological
invariant.

---

## 1. The Open Question

The fractional twist $\theta = 1/2$ is the most ubiquitous structural constant in
the framework, unifying:
- **Neutron anomaly (Phases 28-30):** $\Xi_{\text{eff}} = 1/2$ leading term and
  $f_{\text{Klein}} = 1 + 1/2 = 3/2$ radiative term.
- **Lepton masses (Phase 31):** The Koide phase $\pi/2$ IS the half-integer twist.
- **Baryon Decuplet (Phase 35):** The double-cover base $4 + (1/2)f_{\text{Klein}}$.

Phase 29 derived the *effect* of $\theta = 1/2$ (momentum halving due to the seam
anti-periodic boundary condition), but the *value* $1/2$ itself remained a
phenomenological mapping. We need to derive $\theta = 1/2$ strictly from the graph
topology.

## 2. The Derivation Strategy (U(1) Embedding)

1. The discrete Klein bottle graph (Phase 1) has an orientation-reversing seam.
   This defines a flat $\mathbb{Z}_2$ gauge connection with holonomy $W = -1$ around
   the meridian cycle.
2. The master equation (and quantum mechanics generally) operates on complex
   amplitudes (a $U(1)$ or $SU(2)$ bundle).
3. To support a complex quantum field, the real $\mathbb{Z}_2$ line bundle of the
   substrate must be embedded into a complex $U(1)$ line bundle.
4. The $\mathbb{Z}_2$ holonomy $-1$ embeds uniquely into $U(1)$ as the phase $e^{i\pi}$.
5. The fractional topological charge (the "twist" $\theta$) is defined as the
   $U(1)$ winding number: $\theta = \frac{\arg(W)}{2\pi}$.
6. Therefore, $\theta = \frac{\pi}{2\pi} = 1/2$ exactly.

## 3. Hypotheses to test (H47)

- **H47a — Z2 to U(1) Holonomy Embedding.** Construct the discrete $U(1)$ link
  variables on the Phase 1 Klein graph. Compute the meridian Wilson loop and
  extract the fractional twist $\theta = 1/2$.
- **H47b — Grid Independence.** Show that $\theta = 1/2$ is an exact topological
  invariant independent of the discretization size ($n_{\text{mer}}, n_{\text{lon}}$).
- **H47c — SU(2) Double-Cover Reduction.** Connect this to the Phase 25 temporal
  holonomy (where a 720° cycle gave exactly $-I$). In $U(1)$, a single 360° traversal
  gives $W = -1$, representing a half-rotation ($\theta = 1/2$).
- **H47d — The Orientable Contrast.** Show the orientable torus graph yields
  $W = +1$, giving $\theta = 0$ and $f = 1$ (recovering the proton/electron topology).

## 4. Success criteria

A robust topological derivation of $\theta = 1/2$ that requires no free parameters,
no grid-size limits, and clearly separates the orientable (proton) and non-orientable
(neutron) topologies. This removes the last "assumed" mapping in the twist framework.

## 5. Deliverables

- `code/phase47_emergent_twist.py` — implementation of the $U(1)$ embedding.
- `tests/test_phase47_emergent_twist.py` — unit tests for the derivation.
- `code/outputs/phase47/emergent_twist.csv`
- Phase map + synthesis update (README, cross_phase, synthesis_paper §8.1w).

## 6. Sequencing

Phase 47 resolves the "emergent-twist derivation" open item. The only remaining
structural open item from the retrospective is the "stable-knot $\to$ SM multiplicity
mapping".
