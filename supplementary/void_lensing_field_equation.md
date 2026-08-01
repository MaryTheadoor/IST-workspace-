# Field Equation for Void Lensing: Model A vs Model B

**Status:** Working derivation. Resolves the sign ambiguity in the Phase 5/17
void lensing predictions.

**Reference:** `code/phase5_observational_tests.py` (Phase 5 void templates),
`code/phase17_des_voids.py` (DES void-shear stacking)

---

## 1. The IST Field Equations

The IST-modified Einstein equations (v5.3 §3.3) are:

```
R_μν − (1/2)R g_μν + Λ(ρ_fold) g_μν = 8π G(ρ_fold) T^(knot)_μν
```

where `G(ρ_fold) ∝ ρ_fold^(1/D)` and D = φ at the golden window (Phase 14). Both
G and Λ are functionals of the local fold density, not constants. This
environment-dependence produces the void lensing anomaly.

## 2. The Lensing Observable

For a thin lens, the convergence κ is the surface mass density weighted by the
lensing kernel:

```
κ(θ) = Σ(θ) / Σ_crit
```

where `Σ(θ) = ∫ ρ(r) dz` is the projected (surface) density along the line of
sight, and `Σ_crit = c²/(4πG_N) D_s/(D_l D_ls)` is the critical surface
density (conventionally defined with the Newtonian G_N).

The question: when G depends on position, does the convergence formula change?

## 3. Model A: Local Poisson (G-weighted density contrast)

In the Newtonian limit of the IST equations, the gravitational potential
satisfies the generalized Poisson equation:

```
∇²Φ(x) = 4π G(ρ(x)) ρ(x)
```

The lensing deflection is determined by the gradient of Φ integrated along the
line of sight. The convergence is:

```
κ_A(θ) = [∫ G(ρ(r)) ρ(r) dz] / [G_N Σ_crit]
        = [G_N Σ_crit]⁻¹ ∫ G(ρ(r)) ρ(r) dz
```

For a top-hat void with δ = −0.8 and D = φ at the golden window:

```
Inside void:  ρ = 0.2 ρ̄,  G(ρ) = G_N (0.2)^(1/φ) = 0.370 G_N
              G(ρ)·ρ = 0.370 G_N · 0.2 ρ̄ = 0.0738 G_N ρ̄
Background:   ρ = ρ̄,      G(ρ̄) = G_N
              G(ρ̄)·ρ̄ = G_N ρ̄
```

The **contrast** (void − background contribution to convergence):

```
Δκ_A ∝ (0.0738 − 1) = −0.926  (vs GR: −0.800)
```

**Model A prediction:** Voids appear 15.8% DEEPER than in GR. The shear signal
is ENHANCED, not suppressed. (Phase 5: Model A gives 2.3−2.7σ vs GR at 100
voids — marginally distinguishable.)

## 4. Model B: Interior-G Suppression (IST narrative)

The alternative model treats G as a spatially constant factor over the void
region, scaling the entire convergence profile:

```
κ_B(θ) = (G_void / G_N) · κ_GR(θ)
       = (1+δ)^(1/D) · κ_GR(θ)
```

For δ = −0.8 and D = φ:

```
κ_B = (0.2)^(1/φ) · κ_GR = 0.370 κ_GR
```

**Model B prediction:** Voids have 63.0% SUPPRESSED shear. This is the 10.7σ
signal at 100 stacked voids.

## 5. Which Model Follows from the Field Equations?

Model A is the direct weak-field limit of generalizing the Einstein source
term: `8π G(ρ) T` → in the Newtonian limit the Poisson source is G(ρ)·ρ.
This is the minimal coupling prescription for the IST modification.

Model B requires an additional assumption: that the deflection angle
experiences a spatially-averaged G factor rather than the local G at each
mass element. This could arise if:

1. **The photon's path averages G along the line of sight.** For a photon
   passing through a void-dominated line of sight, the effective G is the
   path-length-weighted average, which is lower than G_N due to the void
   interior. This is an integral effect of Model A computed along the actual
   photon geodesic — it would produce a suppression intermediate between
   A and B.

2. **The deflection is set by the boundary geometry.** The void shear peaks
   at the void radius (Phase 17 DES measurement: γ_t peaks at ~0.27° for
   R_v=30 Mpc at z=0.8). At the void boundary, the density transitions from
   0.2ρ̄ to ρ̄wall, and G transitions from 0.37G_N to something closer to
   G_N (the wall has moderate density enhancement). The lensing signal at the
   peak radius is dominated by the wall region, where G ≈ G_N. The suppression
   has to be computed from the full density-G profile, not from the void
   interior alone.

3. **The photon geodesic equation in the IST metric** may involve the
   connection coefficients that depend on gradients of G(ρ), not just G(ρ)
   itself. The Weyl tensor may couple to ∂_μ G, producing additional
   deflection terms that partially cancel the G-weighted source.

## 6. Resolution Path

The resolution requires explicit computation of the photon geodesic equation
in the weak-field IST metric:

```
ds² = −(1 + 2Φ) dt² + (1 − 2Ψ) δ_ij dx^i dx^j
```

with `∇²Φ = 4π G(ρ) ρ` and the lensing potential `(Φ+Ψ)/2` governing the
convergence. The slip between Φ and Ψ (absent in GR, potentially non-zero in
IST due to the G(ρ) gradient) determines whether the convergence is
G-weighted (Model A) or scalar-averaged (Model B).

**Current status:** Model B is the IST phenomenological narrative (63%
suppression). Model A is the standard modified-gravity weak-field limit.
The Phase 5 distinguishability at 100 voids: Model A vs B at >11σ — Euclid/
COSMOS-Web data will decide empirically regardless of the theoretical
resolution. The field-equation derivation is in progress.
