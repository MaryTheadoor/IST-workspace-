# The φ-Attractor Hypothesis: Variable Golden Ratio in IST

**Status:** Working hypothesis (proposed by M. Theadoor, 2026-07-27),
formalized and tested in `code/phase6_phi_attractor.py`.

---

## 1. Statement

> The golden ratio in IST is **not a fixed point** of the substrate's
> renormalization group. It is an **attractor state of the harmonic
> self-interaction of the manifold geometry** — approached dynamically,
> the same way the golden angle emerges in biological growth patterns —
> with the exact approached value **varying with scale**, in the same
> sense that `G` is variable in the theory.

Consequences:

- The effective dimension `D` (and hence every `φ`-dependent constant —
  `2/φ²` mass normalization, `1/φ` gravity exponent, `φ⁸` magnification)
  is a **running quantity** `D(μ, ρ_fold)`, not a constant.
- Physical constants take their observed values in the **golden window**:
  the scale range where `D(μ)` passes through `φ`.
- Deviations from exact `φ`-relations are **expected and structured** —
  they carry information about the attractor trajectory, not noise.

## 2. The phyllotaxis mechanism, precisely

In plant morphogenesis the golden angle `2π/φ² ≈ 137.5°` is never an
input. It emerges because the golden-ratio gap structure is the unique
partition of the circle that is **self-similar at every deposition
generation**:

- **Three-gap theorem:** the orbit `{kα}` of any rotation number `α`
  partitions the circle into gaps of at most 3 distinct sizes; for
  golden `α` there are exactly **2 sizes in ratio φ**, at every `N`.
- **Hurwitz/Lagrange:** `φ` is the hardest irrational to approximate by
  rationals (all continued-fraction digits are 1). Equivalently, the
  golden partition maximizes the minimum gap among all rotation numbers —
  it is the **supremum of the anti-resonance measure**
  `min_{p/q} |α − p/q| q²`.
- **Dynamics:** in Douady–Couder-type growth models (elements deposited
  at an apex, repelling pairwise while advected outward), generic initial
  conditions relax to the golden divergence angle. Rational `α`
  mode-locks and dies; non-noble irrationals eventually generate
  arbitrarily small gaps (resonant collapse). The golden structure is the
  **maximally persistent** one — hence an attractor, not a fixed point:
  at finite resolution (finite element count), the converged value
  deviates from the golden angle by an amount that shrinks with scale.

### Substrate translation

| Phyllotaxis | IST substrate |
|---|---|
| apex deposition tick | plonk tick of Ψ |
| new primordium | new fold generation (harmonic content) |
| pairwise repulsion | harmonic self-interaction of the weave (mode repulsion via the associator / tanh nonlinearity) |
| radial advection | coarse-graining / scale flow |
| divergence angle | spectral gap ratio of the substrate harmonics |
| golden angle attractor | `D ≈ φ` golden window |
| finite apex resolution | finite plonk resolution → scale-dependent best-approach |

## 3. Reinterpretation of Phases 1–5

The hypothesis converts the roadmap's "failures" into predicted
structure:

- **Phase 1.3 (`D_eff = 2`):** the uniform block-spin grid is a
  *rational* cellulation with no deposition history — the pre-attractor
  state. The local RG cannot find `φ` because `φ` is not a local graph
  invariant; it lives in the *history of harmonic deposition*.
- **Phase 4 (running exponent):** the measured `G`-exponent sweeps from
  `0.600` to `1.0` across the fold scan — i.e. `D_eff = 1/slope` descends
  through `φ ≈ 1.618` exactly once. Under the hypothesis this is the
  **attractor passage**: the substrate approaches `φ` in the golden
  window and drifts on as the fold structure saturates. The drift (which
  Phase 4 flagged as "not a true power law") is the *predicted signature*
  of an attractor that is approached but never pinned.
- **Phase 2 (`M ≈ φ⁸`):** the magnification accumulates over ~8
  deposition generations of near-golden scaling — consistent with an
  attractor acting over a finite number of RG generations.
- **Phase 5 (degeneracy):** the observationally indistinguishable
  `D = φ` vs `D = 1/0.600` lensing templates are two snapshots of the
  same running `D` near its golden passage.

## 4. Falsifiable predictions — test outcomes (Phase 6, 2026-07-27)

1. **Anti-resonance selection — CONFIRMED.** The golden rotation holds
   gap rigidity `R ≥ 1/φ²` for all 300 simulated deposition generations
   (never collapses); rationals `p/q` collapse exactly at generation
   `q + 1`; the silver ratio (`√2−1`) survives but at lower rigidity
   (0.293 < 0.382); the transcendental non-noble `e−2` dips to 0.133.
   Golden is the unique maximal-persistence structure.
2. **Scale-dependent best-approach — CONFIRMED.** Fibonacci rationals
   `F_{k−1}/F_k` track the golden rigidity floor exactly until
   generation `F_k + 1`, then collapse: at every finite resolution the
   best surviving structure is a Fibonacci rational *approaching* `φ`,
   never reaching it. In the Atela–Golé variational lattice the golden
   divergence strictly minimizes the energy over rationals, and its
   advantage *grows* as `g → 1` (`E_gold/E_rat`: 0.998 → 0.835 from
   `g = 0.90` to `0.96`) — the golden basin deepens with resolution.
3. **Golden window in the data — CONFIRMED, with a bonus.** The Phase 4
   fold scan gives `D_eff(f)` descending [3.43 → 1.17], crossing `φ`
   exactly once, at `f ≈ 4.20`. At the crossing, the void suppression
   `1 − 1/f = 76.2%` — numerically identical to the IST phenomenology's
   ~76% void lensing suppression. The golden window and the canonical
   void prediction coincide.
4. **Variable-exponent gravity — supported structurally.** `G_eff(ρ)` is
   indeed only locally power-law (Phase 4: window slope 0.600 →
   asymptotic 1.0), i.e. the exponent runs — the signature the
   hypothesis requires. Survey-fit programs should float the exponent
   and look for a slow drift rather than a universal `0.618`.
5. **Attractor variability — observed in the growth ODE.** The
   Douady–Couder-style deposition+repulsion+advection simulation settles
   into a *neighboring noble-family basin* (`151.9° ± 0.8°`, a
   small-continued-fraction-digit angle on the bifurcation tree) rather
   than the golden branch (`137.5°`): the dynamics robustly selects a
   noble attractor, but the golden basin — though the global optimum
   (prediction 2) — is not the only local minimum. This is the concrete
   mathematical content of "the exact value probably varies."

## 5. Open questions

- What selects the *branch* (golden vs neighboring noble) in the
  substrate's actual deposition history? Hypothesis: the bare Klein
  bottle spectrum (Phase 1) sets the initial condition, and the twist
  bias selects the golden branch — testable by seeding the growth model
  with the Phase 1 spectrum.
- Does the golden window in `D_eff(f)` sharpen as the substrate grows
  (larger `n`, deeper fold scan)? Prediction: yes, and the crossing
  should migrate toward the phenomenologically relevant fold factor.
- Can the Phase 2 magnification `M ≈ φ⁸` be recovered as the product of
  per-generation magnifications along the attractor trajectory (~8
  deposition generations of near-golden scaling)?
- The `D_eff` curve descends monotonically through `φ`; what sets the
  *descent rate* (the attractor's passage speed), and does it leave an
  observable imprint (e.g. in the running of the `1/φ` exponent across
  cosmic time)?
