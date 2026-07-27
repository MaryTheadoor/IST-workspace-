# Phase 1.1–1.2 Results: Klein Bottle Spectrum & the φ Gap-Ratio Test

**Date:** 2026-07-27
**Plan:** `notes/IST_Research_Plan_Phases_1-5.md` (Phase 1, sections 1.1–1.2)
**Code:** `code/phase1_klein_laplacian.py`, `code/phase1_spectral_analysis.py`
**Tests:** `tests/test_phase1_spectrum.py` (21 tests, all passing; full suite 99/99)
**Outputs:** `code/outputs/phase1/eigenvalue_convergence.csv`, `code/outputs/phase1/spectral_gaps.png`

---

## 1. What was built (Phase 1.1)

`SubstrateGraph`: a 4-regular cellulation of the Klein bottle as a **twisted torus graph**:

- Vertices `(i, j)`, `i ∈ Z_n` (longitude, periodic), `j ∈ Z_m` (meridian, twisted)
- All edges carry twist `t_ij = +1` except the `n` **seam edges**
  `(i, m−1) ↔ ((−i) mod n, 0)` with `t = −1`
- This is a **flat Z₂ connection**: holonomy `−1` around the meridian
  (orientation-reversing cycle), `+1` around every contractible plaquette
  and around the longitude. The seam edge set is the discrete analogue of
  the self-intersection locus required by the plan.

Topology checks (all passing):

| Check | Result |
|---|---|
| Euler characteristic χ = V − E + F | **0** for all tested grids (8×8 … 32×32) |
| Face-orientation BFS | **non-orientable** (Klein); torus control orientable |
| Meridian walk twist product | **−1** (odd) — the self-intersection cycle |
| Longitude walk twist product | +1 |
| Contractible plaquette twist product | +1 (flat) |

## 2. Analytic spectrum (derived)

Separating variables `s(i,j) = e^{iκi} e^{iθj}`, the seam imposes the
boundary condition `s(i, m) = −s(−i, 0)`, which forces `θ = πℓ/m` —
**half-spacing** in the meridian momentum. Hence:

```
λ(p, ℓ) = 4 − 2cos(2πp/n) − 2cos(πℓ/m),   p ∈ Z_n, ℓ ∈ Z_2m
```

Consequences:

- **No zero mode:** `λ_min = 4 sin²(π/2m) > 0`. The twist removes the
  constant section — a non-orientable bundle admits no globally constant
  field. (Torus control: `λ_0 = 0`, `λ_1 ≈ (2π/n)²`.)
- **Scaled ladder:** `λ·(n/π)² → {1, 4, 5, 8, 9, 13, 16, 17, 20, 25, …}`
  = distinct values of `4p² + ℓ²`. Confirmed numerically to machine
  precision (max err ~1e-15 up to n = 128).

## 3. The φ test (Phase 1.2) — result

**Claim under test:** the dominant spectral gap ratio `r*` converges to
φ ≈ 1.618 under self-similar refinement (n → 2n).

Method: distinct eigenvalue levels (exact degeneracies clustered),
gaps `g_k = λ_{k+1} − λ_k`, ratios `r_k = g_k/g_{k−1}`, statistics over the
first ~20 ratios per size, n = 8, 16, 32, 64, 128.

| n | median r* | geomean r* | P(|r − φ| < 5%) |
|---|---|---|---|
| 8 | 0.924 | 1.004 | 0.00 |
| 16 | 0.771 | 0.966 | 0.00 |
| 32 | 0.886 | 0.889 | 0.05 |
| 64 | 0.835 | 0.935 | 0.05 |
| 128 | 0.771 | 0.942 | 0.05 |

**Verdict: FALSIFIED for the bare rectangular grid.** The ratios are
number-theoretic — ratios of differences of `4p² + ℓ²`, i.e. small rational
numbers (1/3, 3/4, 1, 4/3, 3, …) — and show **no trend toward φ** under
refinement. The distribution at n = 128 is indistinguishable from the
analytic integer-ladder prediction.

## 4. Interpretation & implications for the roadmap

The bare Laplacian of a uniform rectangular Klein cellulation is too
"integrable" — its spectrum is exactly solvable and arithmetic. φ cannot
appear in it. The golden ratio must therefore enter through **additional
substrate structure**, not the bare grid:

1. **RG flow (Phase 1.3) — now the critical path.** The plan's `D_eff`
  from the spectral density under block-spin coarse-graining is the
  designed mechanism for `D* = φ`. The bare-spectrum falsification makes
  1.3 the decisive test of the φ claim.
2. **Non-uniform weave coupling `J_ij`.** The substrate is a self-similar
  *weave*, not a uniform grid. A Fibonacci/Farey-modulated `J_ij` (or
  couplings concentrated near the self-intersection locus) breaks the
  arithmetic degeneracy and could seed golden scaling. This is a cheap
  extension: `topological_laplacian(A, T, J)` already accepts `J`.
3. **Aspect-ratio / defect engineering.** Rectangular `n × φn` grids or
  defect lines along the seam change the ladder's number theory.

Note the asymmetry of the result: the *topology* machinery (1.1) works
exactly as hoped — non-orientability, holonomy, and the twisted ground
state are all correct and validated. What fails is only the strongest
reading of 1.2's spectral claim.

## 5. Reproduce

```bash
cd code
python phase1_spectral_analysis.py                       # sweep + outputs
python -m pytest ../tests/test_phase1_spectrum.py -v     # 21 tests
```
