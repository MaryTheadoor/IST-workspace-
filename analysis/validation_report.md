# Phase 5 Validation & Falsification Report

**Plan:** `notes/IST_Research_Plan_Phases_1-5.md` (Phase 5)
**Code:** `code/phase5_observational_tests.py`
**Tests:** `tests/test_phase5_observational.py` (27 tests)
**Outputs:** `code/outputs/phase5/` — `lensing_shear.csv`,
`cmb_antipodal_summary.csv`, `gw_modulation.csv`, `lensing_templates.png`,
`cmb_null.png`, `gw_modulation.png`, `falsification_summary.pdf`

---

## 1. Scope

Phase 5 closes the constants-from-geometry roadmap with an end-to-end
observational validation of the IST predictions that Plans 6–12 and
Phases 1–4 produced. Three test channels were built:

1. **Void lensing templates** with the Phase 4 derived `G(ρ)`.
2. **CMB antipodal (Klein parity flip) re-analysis** with rigorous
   Monte Carlo null tests.
3. **GW time-crystal modulation** searches in GWTC-3 ringdowns and the
   NANOGrav 15-yr SGWB.

All pipelines are self-contained (numpy/scipy/matplotlib). Where real
observational data products are not stored locally (Planck maps, GW
strain), the pipelines are validated on synthetic data with known ground
truth, and the detection significance of the IST signal is computed
against the actual instrument sensitivities (catalog SNRs, COSMOS-Web
depth, NANOGrav free-spectrum levels).

## 2. Void lensing (5.1)

### Setup
- Stacked top-hat void: `z_l = 0.8`, `z_s = 2.0`, `R_v = 30 Mpc`,
  `δ = −0.8` (angular radius 66.6 arcmin).
- Templates: constant G (GR), `D = 2` (Phase 1.3), `D = φ` (IST),
  `D = 1/0.600` (Phase 4 measured window).
- Noise: `n_gal = 35/arcmin²`, `σ_e = 0.30`, 100 stacked voids.

### Two mappings from G(ρ) to lensing — an open modeling question
The Phase 4 deliverable `G_eff ∝ ρ^{1/D}` does not by itself fix the
lensing observable. Two candidate mappings were implemented:

- **Model A (local Poisson):** κ sourced by the G-weighted density
  contrast `ρ̄[(1+δ)^{1+1/D} − 1]`. Voids appear **deeper** than GR
  (deviation `+16%` in shear amplitude for `D = φ`).
- **Model B (interior-G suppression, IST narrative):** the GR signal is
  scaled by `(1+δ)^{1/D}`. Voids are **suppressed** (`−63%` for `D = φ`;
  `−76%` at `δ = −0.9`, matching the README figure).

The sign of the deviation **differs between the two mappings**. Resolving
which one follows from the IST field equations (v5.3 §3.3) is now a
concrete open theoretical task, and observationally the two are trivially
separable (see below).

### Distinguishability (Δχ², 100 stacked voids)

| Comparison | Model A | Model B |
|---|---|---|
| `D = 2` vs GR | 2.3σ | **9.4σ** |
| `D = φ` vs GR | 2.7σ | **10.7σ** |
| `D = 1/0.600` vs GR | 2.6σ | **10.5σ** |
| Model A vs Model B (same D) | — | **11.7–13.4σ** |

**Verdict:** Model B (the IST suppression narrative) is decisively
distinguishable from GR at COSMOS-Web/Euclid depth; Model A is only
marginally distinguishable (~2.5σ) with 100 voids (scales as √N_voids).
The `D = φ` and Phase 4 `D = 1/0.600` templates are within 5% of each
other and effectively degenerate — the Phase 4 crossover window is
observationally indistinguishable from the golden-ratio target, which is
the best that can currently be said for the `1/φ` exponent.

## 3. CMB antipodal correlation (5.2)

### Pipeline
- `apply_klein_parity_flip(T, mirror=True)` — the orientation-reversing
  antipodal map `(θ, φ) → (π−θ, π−φ)` (exact involution on the
  cell-centered grid); plain antipodal `(θ, φ) → (π−θ, φ+π)` as control.
- Statistic `C = ⟨T·KT⟩_w / ⟨T²⟩_w` with galactic masks
  `|b| > 20°, 30°, 40°`.
- Null: 200 Gaussian ΛCDM skies per case (Planck-2018-like low-ℓ TT
  anchors, `ℓ_max = 60`, 64×128 grid).
- Injection: paired skies `(T + c·KT)/√(1+c²)` with `2c = 0.005`, so the
  recovery shift is measured without doubling the cosmic variance.

### Results

| Flip | Mask | Null mean ± σ | Recovery shift | Detection |
|---|---|---|---|---|
| Klein | \|b\|>20 | +0.038 ± 0.097 | +0.00494 | 0.051σ |
| Klein | \|b\|>30 | +0.045 ± 0.108 | +0.00493 | 0.046σ |
| Klein | \|b\|>40 | +0.052 ± 0.119 | +0.00491 | 0.041σ |
| antipodal | \|b\|>20 | +0.077 ± 0.106 | +0.00491 | 0.046σ |
| antipodal | \|b\|>30 | +0.075 ± 0.118 | +0.00490 | 0.042σ |
| antipodal | \|b\|>40 | +0.073 ± 0.130 | +0.00489 | 0.038σ |

**Verdict:** the pipeline recovers an injected `C = 0.005` signal
*exactly* (shift/0.005 = 0.99), so the statistic is sound — but the
ΛCDM null has `σ_C ≈ 0.10–0.13`, roughly **25× the claimed signal**. A
`C ≈ 0.005` antipodal correlation is **not recoverable in a single CMB
sky** with this statistic. The motivating measurement reported in v5.3
(`C ≈ 0.005`) is consistent with ΛCDM noise and cannot be cited as
evidence either for or against IST; the non-zero null means (mask-induced
bias, +0.04 to +0.08) further show that un-masking-corrected single-map
values of that size are expected. The pipeline is ready to be pointed at
Planck 2018 maps; the prediction must be reformulated at larger amplitude
or with a variance-reducing statistic (e.g. a matched low-ℓ template)
to become testable.

## 4. GW time-crystal modulation (5.3)

### Setup
- Per GWTC-3 event: ringdown `h(t) = A e^{−t/τ} sin(2π f_rd t)` with
  `τ = Q/(π f_rd)`, `Q = 10`; IST modulation at `f_tc = f_rd/(2φ)` with
  amplitude `ε = α/φ² ≈ 2.79×10⁻³`.
- Estimator: exact 2×2 matched filter on `{h, g}` with
  `g = ∂h/∂ε|₀`, white noise normalized to the catalog SNR. (A naive
  inner-product estimator is biased when `f_tc` overlaps the ringdown
  envelope; the 2×2 fit is exact — verified by injection/recovery:
  injected 0.2 → recovered 0.191 ± 0.046, analytic σ 0.049.)

### Results

| Event | f_rd (Hz) | f_tc (Hz) | SNR | Detection | SNR needed (3σ) |
|---|---|---|---|---|---|
| GW150914 | 251 | 77.6 | 24.0 | 0.042σ | ~1710 |
| GW170817 | 2000 | 618.0 | 32.4 | 0.057σ | ~1710 |
| GW190814 | 370 | 114.4 | 24.7 | 0.045σ | ~1660 |
| … (all 10 in `gw_modulation.csv`) | | | 11–32 | 0.02–0.06σ | ~1.7×10³ |

- **NANOGrav:** `A_extra/A_obs = α/φ² = 0.28%`; cross-power ratio
  `(α/φ²)² ≈ 7.8×10⁻⁶` — below current PTA sensitivity by ~5 orders of
  magnitude.

**Verdict:** the `ε = α/φ²` ringdown modulation is **not detectable**
with GWTC-3 SNRs (best: 0.057σ on GW170817); detection requires SNR
~1.7×10³, i.e. third-generation detectors (ET/CE) *and* a favorable
event, or a stacking analysis across the full catalog with careful
non-stationarity control. The NANOGrav extra component is likewise below
sensitivity. These are currently **null-consistent** predictions: IST is
not excluded, but the channel provides no confirming evidence yet. The
modulation amplitude `ε` is the parameter to watch — any future revision
upward of `ε` by ≥ 30× would bring the entire catalog into range.

## 5. Falsification summary

| # | Prediction | Target | Result | Verdict |
|---|---|---|---|---|
| 5.1 | Void lensing suppression | `γ_t` templates, 100 voids | Model B: 9.4–10.7σ from GR; Model A: 2.3–2.7σ; A vs B: >11σ | **Testable now** (Euclid/COSMOS-Web); mapping A vs B is the open theory item |
| 5.2 | CMB antipodal `C ≈ 0.005` | Planck-like skies | Null σ ≈ 0.12 ≈ 25× signal | **Not testable** as formulated; claim consistent with noise |
| 5.3a | Ringdown `f_tc = f_rd/2φ`, `ε = α/φ²` | GWTC-3 | 0.02–0.06σ per event | **Not detectable** (needs SNR ~1.7×10³) |
| 5.3b | SGWB extra component | NANOGrav 15yr | power ratio 7.8×10⁻⁶ | **Below sensitivity** (~10⁵× needed) |

### What Phase 5 establishes
1. The **void-lensing channel is the only currently decisive test** of
   the IST variable-gravity sector, and it decisively discriminates the
   two candidate mappings (A vs B) — Euclid/COSMOS-Web void stacks can
   either kill Model B or exclude GR at >10σ under the stated survey
   assumptions.
2. The CMB antipodal claim must be **reformulated** (larger amplitude or
   variance-reduced statistic) before it can testify either way.
3. The GW/PTA channels are **sensitivity-limited**, not
   theory-limited: their null outcome is predicted by IST itself
   (`ε = α/φ²` is small), so non-detection is consistent and carries no
   evidence either direction.

Cross-phase consistency note: the Phase 4 window slope (0.600) and the
IST target `1/φ` (0.618) produce observationally degenerate lensing
templates — so a Model-B detection would not by itself discriminate the
microscopic (Phase 4 crossover) from the macroscopic (`D = φ`) origin of
the exponent. That discrimination requires the missing fractal-RG
mechanism identified in Phases 1–4, not more lensing data.
