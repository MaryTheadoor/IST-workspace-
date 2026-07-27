# Discrete Substrate: Vector Encoding, Not Raster

**Status:** Working constraint (M. Theadoor, 2026-07-27).
Affects all substrate graph constructions (Phases 1–6).

---

## 1. The constraint

At the fundamental Planck scale, the discrete units of the substrate do
**not** have a spatial shape (square, triangle, hexagon, etc.). They have:

- **a fixed minimum wavelength** of information — the plonk length `ℓ_p`
  is a spectral/bandwidth bound, not a pixel size — and
- **a vector encoding**: each unit is an oscillator whose state is
  described by the directed-numbers formalism (amplitude + parity: the
  native language of the substrate), not a spatial lattice site.

The substrate does not "tile space." It carries information with a
minimum resolution, and spatial structure (dimension, adjacency,
geometry) **emerges** from the coupling between oscillators, not from a
pre-assigned grid.

## 2. What a raster discretization gets wrong

Our current `SubstrateGraph` (Phase 1, `phase1_klein_laplacian.py`) builds
a finite 4-regular twisted torus — an `n × n` square grid with periodic +
glide-reflection boundary conditions. This is a **raster
approximation**: every vertex has the same degree, the same local
neighbourhood, and the unit cells are uniform squares.

Three artefacts follow directly from the raster assumption:

### 2.1 Rational gap structure

A regular `n × n` torus Laplacian has eigenvalues
```
λ(p, l) = 4 − 2 cos(2πp/n) − 2 cos(πl/n)
```
whose gap ratios are determined by the number-theoretic ladder `4p² + l²`.
This is a **rational orbit** on the spectral circle — the anti-thesis of
the anti-resonant (golden) structure Phase 6 proved is required for
persistence. The raster cellulation *guarantees* resonant mode-locking at
the grid scale, which is why gap ratios never converge to φ (Phase 1.2
falsification).

### 2.2 Fixed local dimension

A 4-regular graph has spectral dimension `D_eff = 2` by construction.
The block-spin RG (Phase 1.3) preserves this dimension because the
coarse-graining is itself a raster operation (`2 × 2` blocking of a
square grid). The "failure" to see `D → φ` is not a property of the
substrate — it is a property of the raster discretisation.

### 2.3 Pre-assigned adjacency

In the raster model, which vertices are coupled is decided by the grid
geometry *before* any dynamics are applied. The weave's self-interaction
(the associator, the tanh nonlinearity) then operates on a fixed wiring
diagram. But in a vector-encoding substrate, **the coupling graph itself
is a product of the associator**: two modes couple if their
information-exchange rate exceeds a threshold. Adjacency is emergent and
scale-dependent — precisely the structure Phase 6's growth model builds
(particles deposited at an apex, coupled by pairwise repulsion whose
range sets the effective dimension).

## 3. The correct encoding

### 3.1 Fundamental units as directed-number oscillators

Each primitive unit `i` carries a directed-number state
`s_i ∈ D` (amplitude + chirality + memory, the Plan 9 runtime in
`code/directed_numbers.py`). The oscillation frequency `ω_i` is set by
the internal loop topology (the number of Möbius twists), and the
information carried is
```
I_i = s_i.a_up + s_i.a_down + s_i.a_zero .
```
Spatial distance at the substrate level is a measure of information
disparity `|I_i − I_j|`, not a geometric coordinate difference.

### 3.2 Associator-generated coupling

Two oscillators `i, j` are coupled (**edge weight `J_ij > 0`**) if
there exists a third oscillator `k` such that the associator
```
|[s_i, s_j, s_k]| = |(s_i * s_j) * s_k − s_i * (s_j * s_k)|
```
is non-zero. The associator is the substrate's sole mechanism for
creating 3D volume from pairwise 2D surfaces (v5.3 §2.4). An
associator-generated coupling graph is:
- **scale-free** (heavy-tailed degree distribution): most oscillators
  have few strong couplings; a few hubs mediate information across the
  weave — exactly the structure the fractal-RG needs.
- **dynamical**: the coupling graph changes as states evolve, so the
  wiring itself flows under RG.
- **non-local**: oscillators that are "far" in the emergent spatial
  picture may be strongly associator-coupled, mimicking long-range
  connections in a fractal.

### 3.3 Minimum wavelength = Fibonacci resolution

The plonk bound `f_max = 1/(2ℓ_p)` limits how many distinct oscillator
frequencies can co-exist in a region. A bounded frequency band is an
octave of the spectral circle: exactly the setting of Phase 6. At
finite plonk resolution, the optimal anti-resonant partition of the
circle is a Fibonacci rational `F_{k−1}/F_k`, and the golden irrational
`1/φ²` is the **attractor** — approached as `ℓ_p → 0` but never exactly
reached at finite resolution.

The minimum wavelength therefore **directly selects which Fibonacci
rational is observed**: the finer the plonk resolution, the further
along the Fibonacci sequence the best-approximant advances. This is
"the golden ratio varies with scale" — a concrete, quantitative
version of the Phase 6 hypothesis.

## 4. Consequences for the existing simulation framework

| File | Raster assumption | Correction |
|---|---|---|
| `phase1_klein_laplacian.py` | `SubstrateGraph` is a fixed 4-regular `n × n` grid | Replace with associator-generated coupling from a population of `N` directed-number oscillators; keep the Klein twist as a global parity constraint (the non-orientability survives because it is a topological condition on the information flow, not on the grid) |
| `phase1_rg_flow.py` | `block_prolongation` on `2 × 2` grid cells | Replace with spectral coarse-graining on the associator-generated graph (no geometric blocking; Laplacian-based Galerkin projection onto the low-energy eigenspace) |
| `phase4_variable_g.py` | Fold field parameterised as a band of rows on the grid; `FoldedSubstrate` inherits grid | Replace with fold density as a local oscillator-density field on the associator graph; sequential updating with vertex-dependent gain |
| `phase6_phi_attractor.py` | Independent of raster substrate (works on the spectral circle); no correction needed | — (this module already models the correct structure) |

**What does NOT change:**
- The Klein bottle **topology** (non-orientability, `χ = 0`, twist holonomy) survives because it is a global constraint on parity parity, not on spatial geometry.
- The Hopf fibration (Phase 2) and mass formulas (Phase 3) depend on **topological loop counts** — invariant under the encoding change.
- The φ-attractor dynamics (Phase 6) are proven on the circle and do not depend on the raster substrate at all.
- The observational predictions (Phase 5) are *less* affected because the golden window in the Phase 4 data (`D_eff` crossing `φ` at `f ≈ 4.2`) is already measured and does not require re-derivation — it is an emergent property of the fold-density parametrisation, which can be re-expressed in vector-encoding language once the associator-generated graph is built.

## 5. Testable prediction of the correct encoding

If the raster grid is replaced by an associator-generated coupling graph,
the effective spectral dimension should **flow naturally toward
golden-ratio values** under RG, without the Solis β-function being
imposed by hand:

```
network D_eff  →  φ    (conjecture, from maximum anti-resonance)
grid D_eff     →  2    (raster artefact, confirmed Phase 1.3)
```

This is a sharp, falsifiable prediction — and the Phase 6 persistence
mechanism (only golden-ratio gap structures survive all deposition
generations) provides the theoretical basis for why associator-generated
coupling, which is inherently dynamical and history-dependent, should
realise it.

## 6. Angular propagation freedom and the raster mode-locking

A distinct but compounding raster artefact is the **restricted propagation
directions** of the grid. The 4-regular (cardinal-only) and 8-regular
(graphs with diagonals) force wave functions to propagate along a
fixed set of lattice vectors:

| Graph | Propagation directions | Intersection angles |
|---|---|---|
| 4-regular (Phase 1) | 4 cardinal | multiples of 90 deg only |
| 8-regular (R=1) | 4 cardinal + 4 diagonal | multiples of 45 deg |
| R=2 Chebyshev | 24 neighbours | 12 unique angles |
| Continuous 2D manifold | all angles [0, 2pi) | any relative angle |

On a continuous 2D substrate, two wave functions can propagate at any
angle and intersect at any relative angle. The grid constrains this to a
discrete set, producing the 4p^2 + l^2 number-theoretic ladder in the
Laplacian spectrum (Phase 1.2).

A high-connectivity substrate graph with Chebyshev neighbourhood radius R
on the twisted torus has degree (2R+1)^2 - 1 and restores angular freedom
as R grows: code/angular_connectivity_substrate.py implements this.

| R | Avg degree | Median r* (n=32) | D_eff |
|---|---|---|---|
| 1 | 8 | 0.90 | 1.90 |
| 2 | 24 | 1.09 | 1.97 |
| 3 | 48 | 0.96 | 2.09 |
| 4 | 80 | 0.94 | 2.27 |
| phi target | -- | 1.618 | 1.618 |

**Finding.** The gap-ratio distribution does **not** converge toward phi
as R increases. Median r* fluctuates (0.90-1.09 across R) but stays well
below phi. High connectivity dilutes the discrete 4p^2 + l^2 ladder into a
more continuous mode distribution, but the anti-resonant golden structure
does not appear in the static Laplacian -- it requires the dynamical
deposition and persistence mechanism (Phase 6).

Removing the angular raster constraint fixes the rational mode-locking
but is not sufficient. Phi emerges from the self-interaction history, not
from the static spectrum of any graph, regardless of connectivity.
