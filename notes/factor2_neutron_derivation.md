# The Factor-2 Neutron — Derivation Notes (Phase 28)

**Status:** Empirical relation, top-down validated against CODATA 2018 to
0.02σ. The factor 2 and the correction series are *consistent* with the
framework's double-cover and associator machinery but are not yet derived
from first principles.

---

## 1. The result

With `δ_n = (m_n − m_p)/m_p` (observed `0.0013784193`), the plan's literal
form `δ_n = α/φ²` overshoots by **2.02×**. The exact top-down form is

```
δ_n = (α / 2φ²) · (1 − (3/2 − α/φ⁶) α)
    = α/(2φ²) − 3α²/(4φ²) + α³/(2φ⁸) ,
```

reproducing `m_n = 0.9395654205` GeV (obs `0.9395654205`) at **0.02σ** —
100.000000% accuracy.

| Form | δ_n | m_n (GeV) | accuracy |
|---|---|---|---|
| naive α/φ² | 0.002787 | 0.940887 | 99.8593% |
| factor-2 α/(2φ²) | 0.001394 | 0.939580 | 99.9985% |
| **exact** (1−cα) | **0.0013784** | **0.9395654** | **100.000000%** |

Exact correction coefficient (from measured masses): `c = 1.4995935`.
Claimed closed form `c = 3/2 − α/φ⁶ = 1.4995933`. Agreement 1.6e-7.

## 2. Where the factor 2 could come from

Two candidate origins, both currently *hypotheses*:

**(a) The 720° double-cover.** A full cycle of the Klein bottle requires
TWO traversals of the orientation-reversing seam (Phase 23a verified
chirality flips at tick 2 and restores at tick 4 — exactly two seam
crossings per 4-tick cycle; Phase 25 verified the flat-limit holonomy is
`-I`, i.e. the fermionic sign). A neutron carrying one extra binding loop
would traverse the twist once more, contributing a factor 1/2 relative to
the single-associator naive term.

**(b) Combinatorial loop factor.** The Phase 3 supplementary already
flagged: "the coefficient of δ needs refinement — perhaps a combinatorial
factor from the number of additional loops or from isospin breaking." The
1/2 is the minimal such factor (one extra loop over the proton's three).

## 3. The (3/2)α correction

The `(3/2)α` term (with the tiny `α/φ⁶` refinement) brings the factor-2
leading term from 99.9985% to 100.000000%. Its form is QED-radiative-
corrective in character (compare the anomalous-momentum family
`1 + α/(2π)`), but no first-principles IST derivation exists yet.

## 4. Arithmetic correction to prior claims

The synthesis paper claimed running `φ ≈ 1.98` gives `m_n` at 99.99%.
This is an **arithmetic error**: `m_n = m_p(1 + α/1.98²) = 0.9400` GeV,
which is 99.95%. The true running φ that reproduces the observed excess is

```
φ_n = √(α/δ_n) = 2.3009,
```

which sits **0.55% above φ√2 ≈ 2.288** (and is NOT close to φ² = 2.618).
So the "running φ" narrative survives only if φ runs to ≈2.30 at the
neutron scale — i.e. φ√2 — not to the 1.98 the paper asserted.

## 5. Open points

1. Derive the 1/2 (double-cover vs combinatorial) from IST postulates.
2. Derive the `(3/2)α` term from the associator/directed-number machinery.
3. Decide whether `α/φ⁶` is a real term or a CODATA-precision coincidence
   (the exact c differs from `3/2` by `4.07e-4 ≈ α/φ⁶` at the 1e-7 level).
4. Extend the same method to the muon: `m_μ/m_e ≈ 3/(2α)` at 99.41% is a
   search hit, not a derivation — the factor-2 analysis may generalize.
