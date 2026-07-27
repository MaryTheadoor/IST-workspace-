# Phase 2 Derivation: α from Hopf Fiber Geometry

**Plan:** `notes/IST_Research_Plan_Phases_1-5.md` (Phase 2)  
**Code:** `code/phase2_hopf_alpha.py`  
**Tests:** `tests/test_phase2_hopf_alpha.py`  
**Outputs:** `code/outputs/phase2/alpha_sensitivity.csv`, `alpha_sensitivity.png`

---

## 1. Physical picture

In IST each quark is modeled locally by the **Hopf fibration**

```
S^1 -> S^3 -> S^2
```

where the base `S^2` is a local patch of the 2D substrate and the fiber
`S^1` encodes spin/chirality (main paper §3.6.1). Kaluza-Klein
compactification of the fiber gives the fine-structure constant:

```
α = 4 / R_f^2     <=>     R_f = 2 / sqrt(α)
```

with `R_f` the fiber radius in Planck/plonk units.

## 2. Discrete construction

We discretize the base `S^2` as a latitude-longitude grid with a single
vertex at each pole. Over every base vertex we place a discrete circle
(`S^1`) with `p` vertices, where `p` is the **fiber period** measured in
plonk units. The total vertex count is

```
N_total = [2 + (n_lat - 2) n_lon] * p .
```

The Hopf connection is discretized from the continuum 1-form

```
A = (c/2)(1 - cos θ) dφ
```

where `c` is the Chern number (topological twist of the bundle). Moving
one step eastward at polar angle `θ` shifts the fiber index by

```
Δk = round( p * c * (1 - cos θ) / (2 n_lon) ) .
```

Meridional (latitude) edges carry **no** fiber shift because `dφ = 0` along
meridians. The construction preserves the bundle topology: the computed
Chern number equals the input `c` for any resolution.

## 3. α from the bare fiber radius

If the fiber is a regular `p`-gon of unit plonk edges, its circumference is
`p` and its radius is

```
R_f = p / (2π) .
```

The raw Kaluza-Klein prediction is therefore

```
α_raw = 4 / R_f^2 = 16 π^2 / p^2
      => α_raw^{-1} = p^2 / (16 π^2) .
```

## 4. The topological minimum and the mismatch

The plan argues that the minimum stable configuration with net chirality
has `p = 3`. Substituting:

```
R_f(p=3) = 3 / (2π) ≈ 0.4775 plonk units
α_raw(p=3) = 16 π^2 / 9 ≈ 17.55
α_raw^{-1}(p=3) ≈ 0.057 .
```

This is far from the observed

```
α^{-1} = 137.035999084 .
```

The observed fiber radius is

```
R_f(obs) = 2 / sqrt(α) ≈ 23.41 plonk units ,
```

so matching observation would require

```
p_needed = 2π R_f(obs) ≈ 147
```

or, keeping `p = 3`, a **magnification factor**

```
M = R_f(obs) / R_f(3) ≈ 49.03 .
```

## 5. The missing ingredient: fractal projection

The plan's resolution is that the fiber radius is the **effective radius
after projection through the substrate's fractal dimension** `D`. In Plan 8
and the main paper the IR fixed point is `D = φ`, and the factor
`2/φ^2` in the proton-mass formula is derived from an invariant entropy
condition at that fixed point.

Our Phase 1.3 RG calculation found `D_eff ≈ 2` for the uniform-grid
block-spin flow, not `φ`. Under that measured dimension the Hopf fiber
would not be magnified enough to reach `R_f(obs)`. The magnification
required is therefore a precise constraint on whatever fractal/nonlocal
modification of the RG is needed.

A numerological observation: the required magnification is remarkably
close to a power of the golden ratio:

```
φ^8 = 46.978...
M / φ^8 = 49.03 / 46.98 ≈ 1.044 .
```

Within ~4%, the missing projection factor is `φ^8`. Whether this is a
coincidence or a hint of an eight-step self-similar weave remains to be
derived from first principles.

## 6. Conclusion

Phase 2 confirms the topological part of the Hopf derivation:

- A discrete Hopf fibration over `S^2` with `p = 3` and Chern number
  `c = 1` is a well-defined, valid bundle.
- The Kaluza-Klein relation `α = 4 / R_f^2` follows directly from the
  fiber geometry.
- The topological minimum `p = 3` gives `α_raw ≈ 17.5`, not the observed
  `1/137`.

The absolute scale of `α` is therefore **not fixed by the local Hopf
topology alone**; it requires the still-missing projection/magnification
mechanism from the substrate's large-scale fractal structure. Phase 1.3
showed that the standard block-spin RG does not supply that mechanism;
finding one that produces a magnification of order `φ^8` is the next
open problem.
