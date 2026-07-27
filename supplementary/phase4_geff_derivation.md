# Phase 4: G from the Compression Spectrum

**Plan:** `notes/IST_Research_Plan_Phases_1-5.md` (Phase 4)  
**Code:** `code/phase4_variable_g.py`  
**Tests:** `tests/test_phase4_variable_g.py` (20 tests)  
**Outputs:** `code/outputs/phase4/decay_spectrum.csv`, `geff_vs_rho.csv`,
`crossing_time.csv`, `geff_vs_rho.png`

---

## 1. Linearizing the Compression Operator (Phase 4.1)

The IST update map (v5.3 §2.3) is

```
s_i(t+1) = U_i(θ) tanh( Σ_j J_ij s_j(t) ) + ξ_i(t) .
```

We model fold density as **sequential sheet updating**: a vertex inside an
f-fold region advances by `1/f` of a full relaxation step per plonk tick,
because the f sheets stacked at that cell are updated one after another.
The explicit, noise-free map is

```
s(t+1) = s(t) + F^{-1} [ tanh(W_norm s(t)) − s(t) ] ,
```

with `W_norm = W/4` the degree-normalized signed adjacency of the Phase 1
Klein bottle graph and `F = diag(f_i)` the fold field (`f_i ≥ 1`,
`s_i ∈ ℝ`).

Linearizing at the flat equilibrium `s* = 0` (where `sech²(0) = 1`):

```
M_Ψ = I − (1/4) F^{-1} L ,
```

so the map eigenvalues are `μ_k = 1 − γ_k/4`, where `γ_k` solves the
**generalized eigenvalue problem**

```
L v = γ F v   ⇔   F^{-1/2} L F^{-1/2} w = γ w .
```

The right-hand form is symmetric positive semidefinite, so the compression
spectrum `{γ_k}` is real and nonnegative. For uniform fold `f ≡ 1` it
reduces exactly to the Phase 1 Laplacian spectrum (`γ_k = λ_k`); the tests
verify this to `1e-8`, and `γ_min` matches the analytic Klein gap
`4 sin²(π/2n)` to `1e-10`.

## 2. Slowest mode = gravitational time scale (Phase 4.2)

A mode decays as `μ_k^t`, i.e. with rate `r_k = −ln(1 − γ_k/4) ≈ γ_k/4`
per tick. The slowest mode `γ_min` sets the longest relaxation time — the
"latency of information propagation across large fold structures":

```
τ_fold = 4 / γ_min ,        G_eff ∝ τ_fold .
```

### 2.1 Non-orientability as the infrared regulator

On the torus control, the constant section gives `γ_min = 0`, so
`τ_fold = ∞`: gravitational latency diverges in the infrared. On the
Klein bottle the twist removes the zero mode (Phase 1), `γ_min > 0`, and
the latency is finite. **Within this model, non-orientability is what
keeps gravity finite-ranged in substrate time** — a structural role for
the twist complementary to its Phase 1 spectral signature.

Numerically (n = 64, flat substrate):

```
Klein: γ_min = 2.409088e-03   τ_fold = 1660.4 ticks
Torus: γ_min = 9.8e-17        τ_fold = ∞
analytic gap 4 sin²(π/2n) = 2.409088e-03  ✓
```

### 2.2 Nonlinear validation

Running the explicit nonlinear map and projecting the trajectory onto the
slowest mode gives a fitted relaxation time within **0.5%** of the linear
prediction (`τ_num = 2958` vs `τ_pred = 2974` ticks at f = 4, n = 64),
confirming that the linearized compression spectrum governs the actual
Ψ dynamics. (The raw norm ‖s(t)‖ is contaminated ~30% by the second mode
on this grid; the modal projection isolates `γ_min`.)

## 3. Sheet/void fold landscape (Phase 4.3)

Setup: a central band of rows (width 8 on a 64×64 grid) carries fold
factor f — fold density `ρ_fold = f` sheets per plonk cell — embedded in
the void background (`f = 1`). We measure three latencies as functions
of f:

- **global modal latency** `τ_fold(f) = 4/γ_min` (whole substrate);
- **regional Dirichlet latencies** of equal-size sheet and void windows;
- **band crossing time** from the explicit nonlinear map (a ring
  perturbation below the band detected above it; longitudinal translation
  symmetry reduces this to meridian diffusion).

### 3.1 Regional contrast is exactly linear

The regional sheet/void latency ratio equals the fold factor **exactly**
at every scanned point (f = 1.5, 2, 3, …, 16 all reproduce the ratio to
machine precision): the Dirichlet ground eigenvalue of the sheet window
scales as `λ_patch/f`. Locally, latency is proportional to fold density —
the v5.3 §3.2 identification `G_eff ∝ τ_fold ∝ ρ_fold` is exact for
regional Dirichlet spectra.

### 3.2 Global modal scaling: a ρ^{1/φ} window inside a ρ^1 asymptotics

The global slowest mode is a crossover object. For small f it is the
extended Klein ground mode, weakly weighted by the band; for large f it
localizes into the band, where `γ_min ~ λ_band/f` and hence `τ ~ f`.

Over the scan window f ∈ [1, 16] the log-log fit gives

```
d log G_eff / d log ρ_fold = 0.600        (IST target: 1/φ = 0.618)
asymptotic local slope (f = 12 → 16) = 0.859 → 1
```

So the measured global exponent **passes within 3% of the IST target
`1/φ`** over the phenomenologically relevant fold range — but this is a
finite-size crossover window, not an asymptotic power law. The asymptotic
exponent is 1 (the D = 1 of sequential updating), not `1/φ`, and the
window value itself depends on band geometry.

### 3.3 Crossing-time scaling is super-linear

The propagation-latency measure gives a *steeper* slope:

```
t_cross ∝ ρ^{1.094}
```

consistent with diffusion across the band (`t ~ w²/D_eff` with
`D_eff ∝ 1/f`, plus broadening corrections). The two latency measures
bracket the IST target: modal decay gives 0.60–1.0, propagation gives
~1.1.

### 3.4 Void suppression

At f = 16 the sheet/void coupling contrast implies a void lensing
suppression of **93.8%**, to be compared with the ~76% figure in the IST
phenomenology (which corresponds to a gentler fold contrast ~4–5×). The
model reproduces the *sign and order* of the effect; the exact percentage
is fold-contrast dependent.

## 4. Cross-phase summary

| Quantity | Local topology result | Missing ingredient |
|---|---|---|
| Compression spectrum | real, nonneg, reduces to Phase 1 spectrum | — |
| IR behaviour | Klein gap regulates τ (torus diverges) | — |
| Regional latency | exactly ∝ ρ_fold | — |
| Global G_eff exponent | 0.600 window ≈ 1/φ; → 1 asymptotic | fractal RG for a true ρ^{1/φ} power law |
| Propagation latency | ρ^{1.09} | — |
| Void suppression | 93.8% at f = 16 | fold-contrast calibration |
| φ gap ratio (Phase 1) | not in bare grid | fractal RG |
| α scale (Phase 2) | not from local Hopf | magnification ~φ⁸ |

Phase 4 sharpens the cross-phase picture in one important way: it
**localizes where the IST exponent can appear**. The regional Dirichlet
latency is rigidly linear, but the *global* slowest mode — the mode that
couples the sheet to the whole substrate — produces a sub-linear window
numerically close to `1/φ`. The crossover mechanism (extended mode →
localized mode) is exactly the kind of structure through which a fractal
RG completion could stabilize the exponent at `1/φ` instead of letting it
run to 1. That is a concrete, testable target for the missing
φ-mechanism: it must pin the global slowest mode at the crossover point.

The pattern across Phases 1–4 remains consistent: **local topology is
correct, global/fractal scaling is missing** — but Phase 4 shows the
local model already contains the crossover skeleton on which the missing
scaling must hang.
