# IST Phase 70 Plan — H-GRAV2: The Attraction Sign from Linking-Mode Tension

**Origin.** The gravity-as-latency-gradient note (`notes/IST_gravity_as_latency_gradient.md`,
§4) flags the honest obstacle to the knot-widening picture: in 2+1-D, conical
defects do NOT attract — pure geometry (widening alone) gives curvature but
not necessarily *pull*. The model's candidate answer is the **linking modes**:
forces between defects in a medium are carried by the medium's restoring modes,
and the sign depends on the tension in the shared configuration. The burden is
precise:

> Derive that the shared harmonic modes between two knots are under tension,
> and that letting the knots approach lowers the total mode energy.

That is a statement about the substrate Hamiltonian (the master equation,
Phase 33), not about geometry. This phase supplies it. H-GRAV1 (the 1/r²
skeleton) is already satisfied by Phase 69; H-GRAV2 is the sign — the thing
that turns "consistent with GR" into "predicts gravity."

**The mechanism.** The substrate Hamiltonian (master equation, Phase 33) has
the coupling term `(α/φ²)·Ξ_eff`. A knot is a defect: it sources a local
excess of transverse strand length (the "widening"). Two knots interact
because their excesses couple through the medium's restoring (linking) modes.
The interaction energy between two defects at separation d is, to leading
order, the product of their source strengths times the medium's Green's
function: `E_int(d) = −(α/φ²)·Ξ_eff·c₁·c₂·G(d)`, where `G(d)` is the lattice
Green's function (in 3D emergent space, `G ~ 1/d`). The derivative `dE/dd`
sign gives attraction or repulsion — this is the test.

**Hypotheses (pre-registered before compute):**

- **H70a — the interaction energy is a Green's-function product.** The total
  substrate energy shift from two knot-sources at separation d factors as
  `E_int(d) = −κ·c₁·c₂·G(d)`, with `κ = (α/φ²)·Ξ_eff` the master-equation
  coupling and `G(d)` the lattice Green's function. Verified numerically by
  computing the ground-state energy of the coupled Hamiltonian for a range of d
  and fitting against `G(d)`.
- **H70b — attraction (dE/dd < 0).** The interaction energy DECREASES as the
  two knots approach, over a physical range of d: `dE/dd < 0`. This is the
  attraction sign. On the emergent 3D lattice `G(d) ~ 1/d`, so `E_int ~ −1/d`
  and `dE/dd = +1/d²·κ·c₁c₂ > 0`... **wait — sign care.** The convention that
  makes the force `F = −dE/dd` attractive (toward smaller d) requires `E_int` to
  be a *negative* energy that grows more negative as d shrinks, i.e. `dE/dd > 0`
  for `E_int < 0`. The test states this cleanly: `E_int(d) < 0` (bound) and
  `dE/dd > 0` (becomes more negative as d decreases) ⇒ potential-well
  attraction, with `F = −dE/dd < 0` pointing toward the other knot.
- **H70c — the sign comes from the tension, not the geometry.** The attraction
  is carried by the `(α/φ²)·Ξ_eff` coupling tension (the master-equation
  associator term), NOT by the widening geometry alone. Control: a *pure
  geometry* term (no coupling tension) gives `dE/dd = 0` (no attraction,
  matching the 2+1-D no-attraction theorem) — the honest negative that
  isolates the mechanism.
- **H70d — the profile is 1/r².** The force `F = −dE/dd` falls as `1/d²` on the
  emergent 3D lattice (`G ~ 1/d`), consistent with the Phase 69 skeleton across
  the whole family. On a 2D lattice `G ~ ln(1/d)` and the force is `~1/d` (not
  inverse-square) — the D = 3 requirement re-asserted, cross-validating Phase 68
  and Phase 69.
- **H70e — the verdict.** Attraction is DERIVED from the master-equation
  linking-mode tension, not assumed; the 2+1-D no-attraction warning is
  respected (H70c control shows pure geometry doesn't attract); the sign and
  the 1/r² profile are consistent. Registry +H-GRAV2; the knot-widening ansatz
  survives its hardest obstacle.

**Honest framing.** This is the first phase that must get a SIGN right, and the
note (correctly) warns the 2+1-D theorem is the canonical way the picture dies.
H70c is the deliberate control: if pure-geometry also attracts, the mechanism
is mis-identified. H70a's factorization is a leading-order (linear-response)
model — higher-order terms are not tested, so a failure there does not kill the
ansatz, only the linear-response reading. The computation uses the
master-equation Hamiltonian on a discrete lattice, not continuum GR; it is a
*derivation of attraction in the IST substrate*, not a full metric (which is
H-GRAV3's mandate).

**Deliverables:** `code/phase70_grav_attraction_sign.py`,
`tests/test_phase70_grav_attraction_sign.py`, outputs under
`code/outputs/phase70/`, this plan file.

**References:**
- `notes/IST_gravity_as_latency_gradient.md` §4–§5 (the obstacle, H-GRAV2)
- `code/phase33_master_equation_correction.py` (the Hamiltonian coupling)
- `code/phase69_gravity_thread_count.py` (the 1/r² skeleton, D=3 shell)
- `code/phase68_sheet_stacking.py` (D_eff = 3)
- `code/phase1_klein_laplacian.py` (the lattice / Green's function)
