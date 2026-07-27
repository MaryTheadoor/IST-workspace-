# Phase 1 Spectral Foundation
## Discrete Klein Bottle Graph, Topological Laplacian, and RG Flow

**Plan:** `notes/IST_Research_Plan_Phases_1-5.md` (Phase 1, sections 1.1–1.3)  
**Code:** `code/phase1_klein_laplacian.py`, `code/phase1_spectral_analysis.py`, `code/phase1_rg_flow.py`  
**Tests:** `tests/test_phase1_spectrum.py`, `tests/test_phase1_rg_flow.py` (110 tests passing)  
**Outputs:** `code/outputs/phase1/eigenvalue_convergence.csv`, `spectral_gaps.png`, `rg_trajectory.csv`, `rg_trajectory.png`

---

## 1. The bare substrate graph

We model the information substrate Σ as a finite graph `G_n` cellulating the
Klein bottle. The construction is a **twisted torus**:

- Vertices `(i, j)` with `i ∈ Z_n` (longitude, periodic) and `j ∈ Z_n`
  (meridian, twisted periodic).
- Vertex id `v = j n + i`.
- Edges:
  - longitude: `(i, j) ↔ (i+1, j)`, twist `t = +1`
  - meridian interior: `(i, j) ↔ (i, j+1)` for `j < n−1`, twist `t = +1`
  - seam: `(i, n−1) ↔ ((−i) mod n, 0)`, twist `t = −1`

The seam edges form the discrete analogue of the self-intersection locus.
All other edges are untwisted. The resulting `Z₂` connection is **flat**:
contractible plaquettes have holonomy `+1`, while a loop that circles the
meridian once crosses the seam an odd number of times and picks up `−1`.

The graph is 4-regular with `V = n²`, `E = 2n²`, `F = n²` plaquettes, so the
Euler characteristic is

```
χ = V − E + F = n² − 2n² + n² = 0
```

as required for the Klein bottle (and for the torus control).

## 2. The topological Laplacian

The plan defines the Laplacian as

```
(ℒs)_i = Σ_j t_ij J_ij s_j − d_i s_i
```

We return the conventional positive Laplacian `L = −ℒ`:

```
L = D − T ⊙ J ⊙ A
```

with `D_ii = Σ_j (J⊙A)_ij` (unsigned weighted degree). With uniform `J = 1`,
`D = 4I`. The spectrum is non-negative; gap sequences are identical under the
overall sign flip.

## 3. Analytic spectrum

Separate variables `s(i, j) = e^{iκi} e^{iθj}` with `κ = 2πp/n`. The seam
condition `s(i, n) = −s(−i, 0)` forces

```
θ = π ℓ / n,   ℓ ∈ Z_{2n}
```

i.e. the meridian momentum is **half-spaced** compared with the torus. The
eigenvalues are

```
λ(p, ℓ) = 4 − 2 cos(2πp/n) − 2 cos(πℓ/n)
```

The smallest eigenvalue is

```
λ_min = 4 sin²(π / 2n) > 0
```

**There is no zero mode:** a non-orientable flat line bundle admits no
constant section. In the continuum this is the statement that the Klein bottle
has no globally-defined orientation. The torus control retains `λ_0 = 0`.

The scaled low-energy ladder converges to the distinct values of

```
4p² + ℓ²  →  {1, 4, 5, 8, 9, 13, 16, 17, 20, 25, …}
```

## 4. Topology checks — all validated

| Property | Klein bottle | Torus control |
|---|---|---|
| Euler characteristic χ | 0 | 0 |
| Orientable | **no** | yes |
| Meridian holonomy | **−1** | +1 |
| Longitude holonomy | +1 | +1 |
| Contractible plaquette holonomy | +1 | +1 |
| λ_min | `4 sin²(π/2n)` | 0 |

Numerical spectra agree with the closed form to machine precision
(max |num − analytic| ~ 10⁻¹⁵ up to n = 128).

## 5. Phase 1.2 — Does the gap ratio converge to φ?

For distinct eigenvalue levels `d_0 < d_1 < …` (exact degeneracies clustered),
define gaps `g_k = d_{k+1} − d_k` and ratios `r_k = g_k / g_{k−1}`.

### Result

| n | median r* | geomean r* | P(|r − φ| < 5%) |
|---|---|---|---|
| 8 | 0.924 | 1.004 | 0.00 |
| 16 | 0.771 | 0.966 | 0.00 |
| 32 | 0.886 | 0.889 | 0.05 |
| 64 | 0.835 | 0.935 | 0.05 |
| 128 | 0.771 | 0.942 | 0.05 |

**Verdict: FALSIFIED for the bare uniform grid.** The ratios are the small
rational numbers of the `4p² + ℓ²` ladder (`1/3`, `3/4`, `1`, `4/3`, `3`,
…). They show no refinement trend toward φ ≈ 1.618.

## 6. Phase 1.3 — RG flow on the graph Laplacian

### Method

We perform **2×2 block-spin (Galerkin) coarse-graining**:

```
L_{ℓ+1} = P^T L_ℓ P
```

where `P` maps each 2×2 block of fine vertices to one coarse vertex. Starting
from `n = 128` we iterate down to `n = 8`. The effective spectral dimension
at each level is extracted from the low-energy Weyl law

```
N(λ) ~ C λ^{D_eff/2}
```

via a linear fit of `log N` vs `log λ` over the first 5–50% of positive
eigenvalues. RG time is `t = ℓ ln 2`.

### Result

| level | n | N | t | D_eff (Klein) | D_eff (torus) |
|---|---|---|---|---|---|
| 0 | 128 | 16384 | 0.000 | 1.978 | 2.031 |
| 1 | 64 | 4096 | 0.693 | 1.992 | 2.043 |
| 2 | 32 | 1024 | 1.386 | 2.045 | 2.093 |
| 3 | 16 | 256 | 2.079 | 2.409 | 2.431 |
| 4 | 8 | 64 | 2.773 | 2.303 | 2.266 |

At the finest scale both topologies give `D_eff ≈ 2`, as expected for a 2D
manifold. Under coarse-graining the dimension stays near 2 and only deviates
upward at very small graph size (finite-size effects). The observed beta
function is `β(D) ≈ 0` near `D = 2` with a fixed point at `D* ≈ 2`, **not**
at `D* = φ`.

The Solis phenomenological beta function used elsewhere in the toolkit,

```
β(D) = −(1/φ²)(D − φ)
```

is overlaid for comparison. The graph-coarsening flow does **not** realize it.

## 7. Conclusion and next steps

Phase 1.1 succeeds: the discrete Klein bottle substrate graph is correctly
constructed, its topology is validated, and its Laplacian spectrum is derived
and confirmed numerically.

Phase 1.2 and 1.3 show that **φ does not emerge from the bare uniform-grid
Laplacian**. Both the raw gap ratios and the block-spin RG spectral dimension
are controlled by ordinary 2D geometry (the `4p² + ℓ²` integer ladder and the
Weyl law with D = 2).

Therefore the golden-ratio fixed point must come from **additional substrate
structure** not yet included:

1. **Fractal / self-similar coarse-graining.** A non-uniform block-spin rule
   (e.g. Fibonacci-decimated blocking, or couplings that scale by φ at each
   RG step) could produce a spectral dimension `D_eff → φ`.
2. **Non-uniform weave coupling `J_ij`.** The Laplacian already accepts an
   arbitrary positive weight matrix `J`. A self-similar `J` breaks the
   arithmetic degeneracy of the bare grid and may seed golden scaling.
3. **Nonlocal or long-range interactions.** The Solis reference invoked in
   the main paper is a *nonlocal* field-theory model; local graph
   coarse-graining may need to be replaced by a nonlocal RG kernel.

Phase 2 (deriving α from Hopf fiber geometry) can proceed independently,
since the α formula is a *local* geometric statement and does not depend on
the RG fixed point.
