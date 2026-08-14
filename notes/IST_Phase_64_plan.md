# IST Phase 64 Plan — Neutrino Classification: the Strand Rule's Next Test

**Origin.** Phase 61's strand rule (single-strand ⇒ seam parity ⇒ fermion;
dual-strand ⇒ achiral ⇒ boson) flagged the neutrino as the next case to
classify; the dimensional-emergence note's §5 records it as the outstanding
test. Observationally the neutrino IS a fermion — so the framework REQUIRES it
to be single-strand. The framework's existing neutrino content: Phase 3's
tunneling hypothesis (m_ν = M_P·P_tunnel, requiring P_tunnel ≈ 4×10⁻³⁰ — a
10²⁷× gap below the naive α/φ² estimate) and Phase 44's near-misses.

**The classification (pre-registered).** The neutrino is a *single open
strand* — a seam-tunneling excitation that never closes into a knot (unlike
the electron, a closed single-strand knot). Same parity, different topology:
the electron's mass is knot tension; the neutrino's near-masslessness is the
open strand's failure to knot. This distinguishes fermions by closure, not by
strand count — both single-strand, both parity 0.446, one knotted, one not.

**Hypotheses (pre-registered before compute):**

- **H64a — the parity test (classification core).** On the true
  Fibonacci-Klein lattice, a single open strand threading the seam has
  parity-inversion **0.446** (the electron value, Phase 52/57) — the
  fermionic signature. A dual-strand (bosonic) reading would give 0.000.
  The runtime confirms the neutrino's required classification: **single-strand
  ⇒ fermion**, consistent with observation; the dual-strand alternative is
  excluded by the same discriminator that forced the photon geometry.
- **H64b — the closure test (why the neutrino is light).** The electron is a
  *closed* single-strand knot (stable fraction ≈ 1/34, Phases 24/52); the
  neutrino is an *open* strand — the stable-knot criterion applied to the
  open strand gives ≈ 0 (it never phase-returns; it tunnels). The
  electron-vs-neutrino mass hierarchy is therefore knot closure, a
  topological distinction within the same parity class — a falsifiable
  mechanism: no open-strand excitation may be massive without closure.
- **H64c — the tunneling quantity (honest re-anchor).** Recompute the
  substrate's seam-crossing probability for an open strand (the twist
  fraction 0.446 per encounter) and restate Phase 3's gap precisely: the
  tunneling-probability-to-mass mapping (m_ν = M_P·P_tunnel) still requires
  P_tunnel ≈ 4×10⁻³⁰, which the naive per-encounter crossing probability
  does NOT supply — the gap is re-anchored, not closed. The classification
  result (H64a/b) does not depend on closing it.
- **H64d — registry + consistency.** Electron (closed single-strand knot,
  0.446, stable) ↔ fermion; neutrino (open single-strand, 0.446, tunneling) ↔
  fermion; photon (dual-strand, 0.000) ↔ boson. Registry appended (81 → ~85).

**Honest framing.** The phase classifies, and separates what the runtime
confirms (parity = fermion; closure = lightness) from what remains open (the
10²⁷ tunneling-probability gap of Phase 3). If the open-strand parity came
out ≠ 0.446 the strand rule would fail — that is the pre-registered
falsification.

**Deliverables:** `code/phase64_neutrino_classification.py`,
`tests/test_phase64_neutrino_classification.py`, outputs under
`code/outputs/phase64/`, this plan file.
