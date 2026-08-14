# Cautionary Note: The φ⁸ Magnification "Coincidence" Does Not Survive Scrutiny

**Status:** NEGATIVE (cautionary) — do NOT build a phase on this.
**Investigated:** Aug 2026, prompted by the external gap analysis (gap 5).
**Files consulted:** `code/phase2_hopf_alpha.py`, `code/phase8_vacuum_pump_threshold.py`,
`code/outputs/phase8/*`.

The external analysis flagged "the φ⁸ magnification coincidence" as the single
highest-leverage investigation: Phase 8 appears to produce φ⁸ = 46.98 exactly in
the vacuum-pump, and Phase 2's required magnification to reach 1/α ≈ 137 from the
topological-minimum fiber appears to be ≈ φ⁸. If the two were the same object, a
first-principles M could convert α from a fitted input into a derived output.

That claim does NOT hold. Three independent problems:

## 1. Phase 8's "φ⁸ = 46.98" is a definition, not a measurement.

The magnification in `phase8_vacuum_pump_threshold.py` is literally
`"magnification": PHI ** self.n_layers` (line 160). At 8 pumped golden layers it
equals 46.98 BY CONSTRUCTION. It is a counter column, not a measured quantity.

The actual, meaningful Phase 8 events are at OTHER layers:
- The coherence threshold fires at **layer 11** (not 8).
- D_eff pins at **1.1825**, not φ = 1.618.

So "magnification_at_n8 = 46.98, matches φ⁸" is comparing φ⁸ to itself. The two
"φ⁸ objects" are the same only in the sense that both are `PHI**8` typed in code.

## 2. Phase 2's required magnification is 4.4% off φ⁸.

Topological minimum fiber_period p = 3 → raw α⁻¹ = 0.0570. Observed α⁻¹ = 137.04.
The α⁻¹ ratio is **2404.4 = φ^16.18**, which is NOT φ⁸. The "49 ≈ φ⁸" appearance
requires TWO ad hoc moves:
- taking the square root (R_f space instead of α⁻¹ space, halving the exponent), and
- rounding log_φ(49.0) ≈ 8.09 down to 8.

## 3. The clean φ⁸ tuning point requires assuming the answer.

M = φ⁸ exactly is reached only at R_f = 0.4983, i.e. fiber period **π ≈ 3.1416** —
not 3, not an integer, not a discrete-lattice object. This is equivalent to simply
*choosing* R_f = 1/2 to force the match. That is precisely the convention-circularity
the external analysis itself warned about (its gap 4).

## Underlying logical issue

Phase 2 supplies the *form* α = 4/R_f² but R_f is a free input; the scale of α is
never derived. "The theory requires a magnification M" is backwards: M is only the
ratio of observed to assumed R_f. Until R_f (or the plonk unit) is fixed
independently, any golden coincidence found in the magnification is manufactured
by the choice of R_f.

## Conclusion

Like the H42g self-referential-137 demotion (a 0.0075% match that was killed), this
is a case where the framework should decline a seductive coincidence. There is no
computational bug, but there IS an error in the inference. Building a phase here
would manufacture numerology, not resolve it.

**No phase is planned for φ⁸.** If the absolute scale of α is ever pursued, it must
come from an independent derivation of R_f / the plonk unit, not from a fitted
magnification.

---

## Recurrence log (Aug 2026 — three independent appearances of the demoted constant)

Despite the demotion, φ⁸ = 46.979 appears in **three independent places** in the
program:

| Site | Appearance | Reading |
|---|---|---|
| Phase 2 | Required magnification M ≈ φ⁸ to reach 1/α ≈ 137 from the topological-minimum fiber p = 3 | Demoted here (§2 above): 4.4% off, R_f forced |
| Phase 8 | `"magnification": PHI ** self.n_layers` — exactly 46.98 at layer 8 | Definitional counter column, not a measurement (§1 above) |
| Phase 23c | φ⁸ used as the scale factor in the plonk→Compton bridge, plotted against the 320-tick count | Co-opted scale reference in the bridging plot (`phase23c_scale_bridging.py`) |

Disposition: three appearances of one demoted constant is either real
secondary structure or exactly what the Phase 54 trial factor predicts for a
pool of 1866 constants (a recurrence like this is well inside the look-elsewhere
budget). Registered, not revived: no new phase is planned on any of the three
appearances, and the registry rows (Phase 2 partial; φ⁸ demotion) already
cross-link this note.