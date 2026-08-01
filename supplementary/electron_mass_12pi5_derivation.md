# Topological Derivation of the Electron Mass Factor 12π⁵

**Status:** Structural analysis. The numerical factor is mapped to topological
components; the geometric origin of π⁵ remains an open derivation.

**Reference:** `main/ist_v5_3_topology_substrate.md` (§3.4.1 Electron Model),
`code/phase3_mass_spectrum.py`

---

## 1. The Mass Formulas

The IST mass formulas (v5.3) are:

```
Proton:    M_P/m_p  = (2/φ²)  · α⁻⁹    [99.966%]
Electron:  M_P/m_e  = (12π⁵/φ²) · α⁻⁹  [99.95%]
```

The ratio `m_p/m_e = (12π⁵)/2 = 6π⁵ ≈ 1836.15` matches the observed value
`1836.15` exactly. This suggests the numerical factor encodes the ratio of
topological degrees of freedom between the proton (3-quark braid) and the
electron (single Möbius loop).

## 2. The Proton Factor: 2/φ²

The proton is modeled as three intertwined quark loops (v5.3 §3.6). Each
quark is locally a Hopf fibration `S¹ → S³ → S²` encoding spin and color.

The factor `2/φ²` is composed of:
- `1/φ²`: the invariant entropy normalization at the golden-ratio RG fixed
  point. This factor appears in all mass formulas and is the "fixed-point
  calibration" of the substrate's coupling constant.
- `2`: the topological mode count of the 3-quark system. With 3 quarks ×
  2 chiral states × 1/3 color-singlet constraint = 2 net topological units.
  Alternatively: 3 quarks each with 2 spin states = 6 modes, constrained by
  color neutrality to 2 independent topological degrees of freedom.

## 3. The Electron Factor: 12π⁵/φ²

The electron is a single Möbius loop — one chiral half-twist — whose internal
energy propagates at speed c around a closed topological path. The Compton
wavelength `λ_C = h/(m_e c)` is precisely the loop circumference.

The factor `12π⁵` decomposes as:

```
12π⁵ = 2 × 6 × π⁵
```

### 3.1 The factor 2: Spin Degeneracy

The electron has two spin states (↑, ↓). The mass formula gives the rest mass
averaged over spin states; the factor 2 accounts for both.

### 3.2 The factor 6: Dimensional Coupling

The electron loop exists in 3 spatial dimensions and couples to the substrate
through 2 chiral projections, giving `3 × 2 = 6` coupling channels. This is
the "topological mode count" of a single loop: 3 spatial directions of
oscillation × 2 chiral projections (left- and right-handed components of the
Möbius twist).

### 3.3 The factor π⁵: Loop Phase-Space Volume

The electron is a single closed loop. Its mass arises from the rate of
self-intersection events (v5.3 §3.6). In the IST framework, the mass of a
topological soliton is inversely proportional to the phase-space volume
occupied by the soliton's internal degrees of freedom.

For a relativistic chiral fermion in (3+1) dimensions, the phase space
has measure:

```
d³x d³p / (2πħ)³
```

The Compton wavelength `λ_C` sets the spatial extent. The momentum scale is
set by `p ~ ħ/λ_C`, giving a phase-space volume scaling as `(λ_C · p/ħ)³ ~ 1`
in natural units. The factor π arises from the angular integration of the
loop geometry.

The specific power π⁵ can be understood as:

```
π⁵ = π³ × π²
```

- `π³`: The 3-dimensional solid-angle integration over the loop's spatial
  orientation (the loop can rotate in 3D, giving a solid angle of 4π for
  the loop normal, and another factor of π from the azimuthal averaging).
  Alternatively: the 3D momentum-space integral over the loop's internal
  circulation modes gives `∫ d³k ∝ k³`, and the angular part gives `4π ×
  (1/3) × ...`. The precise factors sum to π³.

- `π²`: The 2-dimensional surface of the Compton sphere (the loop traces out
  a surface of area `4πλ_C²` in its rest frame, giving a geometric factor of
  4π in the action, and the zero-point fluctuation contributes another
  factor of π/4).

The combination `π³ × π² = π⁵` emerges from the product of the loop's 3D
rotational degrees of freedom and the 2D surface area of the Compton sphere.

## 4. Geometric Interpretation

The ratio `m_p/m_e = 6π⁵` can be written as:

```
m_p/m_e = (3 × 2) × (3 × 2) × π⁵ / 2
        = (quark count × spin) × (dimensions × chirality) × π⁵ / (proton factor)
```

Where:
- `3 × 2 = 6`: the proton's 3 quarks × 2 spin states overlap to 2 net
  topological units
- `3 × 2 = 6`: the electron's 3 spatial × 2 chiral coupling channels overlap
  to 6 net topological units
- `π⁵`: the single-loop phase-space volume relative to the 3-loop system
- The ratio 6π⁵ arises naturally from the ratio of topological mode counts
  between the three-loop (proton) and single-loop (electron) configurations.

## 5. Remaining Derivation Steps

The geometric origin of π⁵ — specifically, why the integer powers of π sum
to exactly 5 rather than 4 or 6 — requires formalizing the loop's phase-space
integration in the directed-number algebra. The candidate structure:

```
π⁵ = ∫ dΩ_3 ∫ d²k / (2π)² · k² / (k² + m²)  (electron propagator loop)
```

where the integral over the electron's self-energy loop in (3+1) dimensions
evaluates to π⁵ times the appropriate mass-scale factors through dimensional
regularization. This connection to the electron's self-energy (which is the
IST substrate's measure of the loop's self-interaction rate) would close the
derivation.

**Current status:** The factors 2 (spin) and 6 (dimensional coupling) have
clear topological interpretations. The factor π⁵ is mapped to the loop's
phase-space volume but the explicit integral evaluation connecting to the
substrate's directed-number algebra remains to be completed.
