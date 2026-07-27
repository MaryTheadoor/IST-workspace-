# Phase 3 Mass Hierarchy: Neutron, Strong Coupling, and Neutrino Tunneling

**Plan:** `notes/IST_Research_Plan_Phases_1-5.md` (Phase 3)  
**Code:** `code/phase3_mass_spectrum.py`  
**Tests:** `tests/test_phase3_mass_spectrum.py`  
**Outputs:** `code/outputs/phase3/mass_predictions.csv`, `mass_hierarchy.png`

---

## 1. Mass formulas tested

The IST mass ratios from the main paper are:

```
M_P / m_p = (2/φ²) α^{-9}          (proton)
M_P / m_e = (12π⁵/φ²) α^{-9}       (electron)
```

Phase 3 asks us to extend this to the neutron and to the strong coupling
and neutrino sectors.

## 2. Neutron mass

### 2.1 Two ways to write the neutron correction

The plan proposes

```
M_P / m_n = (2/φ²) α^{-9} (1 + δ_n),    δ_n ~ α/φ² .
```

With δ_n = α/φ² this predicts `m_n ≈ 0.9352 GeV`, which is **lighter**
than the predicted proton (`m_p ≈ 0.9378 GeV`). Observationally the
neutron is heavier, so the literal ratio form has the **wrong sign**.

A physically clearer ansatz is

```
m_n = m_p (1 + δ_n),
```

i.e. the neutron is the proton plus an extra associator-mediated binding
loop. With δ_n = α/φ²:

```
m_n(pred) = 0.9404 GeV
m_n(obs)  = 0.9396 GeV
accuracy  = 99.91%
```

The prediction is high by ~0.85 MeV. A best fit gives

```
δ_n(best) = 0.001884 ≈ 0.676 * (α/φ²).
```

So the neutron mass splitting is correctly **ordered** by the
associator-scale correction, but its coefficient is somewhat smaller than
the plan's first guess.

### 2.2 Implication

The proton/electron formulas are high-precision empirical relations. The
neutron extension works at the ~0.1% level if written as `m_n = m_p(1+δ)`,
but the coefficient of δ needs refinement — perhaps a combinatorial
factor from the number of additional loops or from isospin breaking.

## 3. Strong coupling α_s from the associator

### 3.1 Model

The plan hypothesizes

```
α_s(E) ~ |[q1, q2, q3]| φ^{-n(E)}
```

with associator magnitude `|[q1,q2,q3]| = 1/φ²` at the fixed point, and
`n(E)` the number of fractal layers probed at energy `E`. We implement

```
α_s(E) = C φ^{-n(E)},    n(E) = log(E/E_ref) / log(2) .
```

`C` is either fixed to `1/φ²` (topological prediction) or fitted to
`α_s(M_Z) = 0.118`.

### 3.2 Results

| Scale | Ref α_s | Fitted model | Fixed-point model |
|---|---|---|---|
| M_Z (91.2 GeV) | 0.118 | 0.118 | 0.382 |
| m_τ (1.78 GeV) | 0.330 | 1.816 | 5.880 |
| m_b (4.18 GeV) | 0.220 | 1.003 | 3.247 |
| m_t (173 GeV) | 0.090 | 0.076 | 0.245 |

The model is **qualitatively** asymptotically free (decreases with
energy above M_Z), but **quantitatively** it fails at scales below M_Z.
The fixed-point normalization is about 3× too large at M_Z.

### 3.3 Implication

The associator gives a plausible *form* for the running — a power law
modulated by φ — but the layer-counting function `n(E)` is not fixed by
local topology. The discrepancy is another instance of the same pattern
seen in Phases 1–2: φ-scaling is present in the framework's
phenomenology but not yet derivable from the bare discrete substrate.

## 4. Neutrino mass as topological tunneling

### 4.1 Model

Neutrinos are hypothesized to be "chiral ghosts" that do not form closed
loops but instead tunnel through the zero-point each plonk tick. The
effective mass is

```
m_ν = M_Planck * P_tunnel       (M_Planck in eV)
```

where `P_tunnel` is the per-tick tunneling probability.

### 4.2 Results

For an observed neutrino mass scale `m_ν ~ 0.05 eV`:

```
P_tunnel(required) = 0.05 eV / M_Planck
                   ≈ 4.1 × 10^{-30} .
```

A naive topological estimate would be

```
P_tunnel(naive) ~ α/φ² ≈ 2.8 × 10^{-3} .
```

The required tunneling probability is smaller by a factor of

```
P_req / P_naive ≈ 1.5 × 10^{-27} .
```

### 4.3 Implication

The tunneling picture is conceptually attractive — the non-orientable
twist provides a natural channel for chiral leakage — but the local
coupling `α/φ²` is far too large to explain the observed neutrino mass.
An enormous suppression is needed. Possibilities include:

- The tunneling event is suppressed by many powers of `α` (higher-order
  electroweak loops).
- The effective number of tunneling modes is tiny because the neutrino
  couples only to a high-dimensional, rarely-occupied subset of the
  substrate (the "bulk depth" `k = 22` discussed in Plan 8).
- The per-tick probability is diluted over many substrate layers, giving
  a factor like `(α/φ²)^N` with `N ~ 8–10`.

## 5. Cross-phase summary

| Quantity | Local topology result | Missing ingredient |
|---|---|---|
| Proton/electron mass | 99.95% accurate | absolute scale from α, already known |
| Neutron mass | 99.91% with `m_n = m_p(1+α/φ²)` | precise coefficient of δ_n |
| α_s running | qualitatively asymptotically free | layer-counting function `n(E)` |
| Neutrino mass | tunneling channel exists | suppression mechanism (~10^{-27}) |
| φ gap ratio (Phase 1) | not in bare grid | fractal RG |
| α scale (Phase 2) | not from local Hopf | magnification ~φ⁸ |

The pattern across Phases 1–3 is consistent: **local topology is
correct, global/fractal scaling is missing.**
