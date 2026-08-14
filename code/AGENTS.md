# code/ AGENTS.md

Non-obvious quirks in specific phase modules.

## phase25_temporal_holonomy.py

- `tick_unitary(rho, crossing)` returns `-i·axis` — an exact SU(2) element
  (unitary, det=+1). It does NOT multiply by a phase; the fold density enters
  only through the axis tilt `phi = beta*(rho - 1)`. Do not "fix" it to add
  `exp(-i*omega)` — that breaks the flat-limit `-I` verification.
- **`cycle_product(rho, ...)` uses a FROZEN rho snapshot**, while
  `propagate_holonomy()` recomputes rho each tick. They are NOT equivalent:
  a test that asserts `cycle_product(...) == propagate_holonomy()` fails.
  To compare, rebuild the product manually from the frozen rho.
- `cayley_hamilton_expm` implements `exp(-iH)` for Hermitian H — the result is
  U(2) (det = e^{-2ia}), not SU(2). Test for unitarity + |det|=1, not det=1.

## phase35_doublecover_baryons.py

- **`ladder_table()` returns TUPLES `(name, S, coeff, pred, obs)`, not dicts.**
  Index with `r[2]`, `r[3]`, `r[4]` — not `r["coeff"]` (TypeError).
- The ladder index `k` differs from strangeness `S`: `k = [1,3,4,5,6]`
  (N=1, Delta=3, Sig*=4, Xi*=5, Omega=6). `m(S)/E = 4 + (k/2)(3/2)`.

## phase40_bell_nonlocality.py

- CHSH maximal-violation settings are `(a,a',b,b') = (0, π/2, π/4, 3π/4)`
  giving |S| = 2√2. The intuitive `(0, π/4, π/8, 3π/8)` gives only 2.39.
- Signal-locality check must measure the A-outcome MARGINAL (the +1 fraction),
  not the A×B product, or it spuriously shows non-locality.

## phase41_measurement_collapse.py

- `gap_entropy_norm` divides by ln(N) so it's size-independent. A pure golden
  orbit at Fibonacci N has entropy ~0.99 (near max), NOT low — the collapse
  signal is the DROP from the noise baseline, not the absolute value.
- Control must be a non-noble irrational (√2−1), NOT a rational like 1/3:
  low-denominator rationals grid-lock on the spectral circle and show
  artificially low entropy.

## phase42_flavor_closure.py / phase43_flavor_closure_2loop.py

- **The 2-loop RGE rate must use B0/B1 as-is** (they already contain 1/π and
  1/π²): `da/dlnE = -2·B0[nf]·a² - 2·B1[nf]·a³`. Do NOT add extra π factors.
- **The QCD RGE integrator must anchor α_s(M_Z)=0.118 at the M_Z grid point
  and integrate both directions** (down to 0.9, up to 300). Starting the
  integration at the bottom of the grid silently corrupts every target
  (m_tau 0.106 vs 0.313).
- **`n_f_active(E, upper=True)` at thresholds**: the numba-JIT inline flavor
  count must exactly match it (`6 if e>=173 else (5 if e>=4.18 else (4 if
  e>=1.27 else 3))`). A wrong inline ternary silently breaks all QCD targets
  (e.g. m_tau 0.382 vs 0.313) while M_Z stays correct — the anchor masks it.
- **`f_b1(nf)` in phase42 is DEAD CODE** (`PHI**(-(k0 + 0.0*k1))`): the "b1
  golden cast" CSV row is bit-identical to "exact b0". Phase 43 implements the
  real b1 cast (`f_b1_cast`). Do not trust the phase42 "b1" row.
- **`errors()` returns PERCENT values (8.78 means 8.78%) but
  `golden_relation_checks.base_specificity()` expects FRACTIONS (0.0878).**
  Pass `rms(...)/100.0` or the basin comes out empty/NaN.

## golden_relation_checks.py

- `base_specificity(error_fn, ...)` takes error_fn returning a FRACTION
  (0.001 = 0.1%), not percent. `fixed_point_roots(g, lo, hi)` uses sign changes
  of `x - g(x)`; equal roots require `diffs[i] == 0.0` exact, so pass a
  function evaluated on a fine grid.
- `unit_robustness` takes `scale` as a 2-tuple (deg, rad); the fixed-point
  function passed must accept the circle measure as its only argument.

## phase51_fibonacci_laplacian.py

- **All `spla.eigsh` calls must pass a deterministic `v0`** (a normalized
  `np.ones(N)` vector). ARPACK's default random start makes `rg_flow_2d` /
  `block_spin_drift` drift run-to-run (observed: min |D_eff − φ| flapping
  0.55 ↔ 0.34), which flakes `test_phase58_trace_map_rg` intermittently.
  The deterministic value is min |D_eff − φ| = 0.5462 — if a future edit
  removes `v0` and the Phase-58 test fails only sometimes, this is why.

## phase46_reference_rescope.py

- **The flavor-closure modules form a one-way import chain:**
  `phase42_flavor_closure` → `phase43_flavor_closure_2loop` →
  `phase46_reference_rescope`. phase46 reuses BOTH `alpha_s_piecewise`
  (phase42) and `alpha_s_qcd_2loop`/`qcd_layer_count` (phase43). Do NOT
  change `alpha_s_piecewise`'s signature/`upper` default — it would silently
  break all three modules' reference scoring.
- **`range_residual_free(pred)` returns a FRACTION-of-relevant-bound residual**
  (0.0 inside the range, else distance-to-near-boundary over that boundary),
  whereas phase43's `range_residual` returns PERCENT of the nominal reference.
  They have different units — don't treat them as interchangeable when
  comparing H43c and H46c numbers.
- **The closing-negative is the shape/λ-power-law mismatch**, not a reference
  artifact: matching 2-loop QCD needs a layer base that FLATTENS above m_b
  (required `phi^+0.82` in the m_b→M_Z segment) — the OPPOSITE sign of the
  principled `phi^-(nf-3)/6`. Do not re-open the α_s golden-closure line with a
  new reference choice; Phase 46 H46a-e already refuted free-refs, QCD-consistent
  refs, and two free exponents.
