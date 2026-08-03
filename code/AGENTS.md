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
