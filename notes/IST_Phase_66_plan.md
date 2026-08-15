# IST Phase 66 Plan — Why-φ²: The Associator Amplitude from the Conjugate Root

**Origin.** The top derivation gap in the queue (status memo 2026-08-14, §2
item 1). Phase 63 resolved the c₁ normalization by setting M_assoc = φ²m_e —
but the φ² was a *motivated postulate* (analogy with the electron mass
formula's associator suppression), explicitly flagged open (H63e: "why the
loop pays exactly φ² remains an outstanding derivation"). The same gap is the
oldest open discrepancy in the repo: the Phase-5-era report
(`REPORT_PHASE5.md`) inserted associator = 1.0 by axiom and noted it differs
from the golden bound 1/φ²; every "derivation" since
(`notes/beta_function_derivation.md` §2.1, `analysis/cubic_correction_
derivation.md` §1.3) has appealed to an *assumed* fixed-point eigenvalue.
Axiom 2.14 states the proportionality; nothing has derived it.

**The candidate derivation (pre-registered).** The substrate's exact RG is
the Fibonacci substitution A→AB, B→A (Phase 58, H58b — parameter-free,
machine precision). Its substitution matrix M = [[1,1],[1,0]] has
characteristic equation λ² = λ + 1 with **two** roots:

- **φ = 1.618...** — the Perron root: the growth/inflation eigenvalue, the
  direction of expansion into time (P4; Phase 58's golden_growth_ratio).
- **ψ = −1/φ = −0.618...** — the algebraic conjugate: the **contraction**
  eigenvalue, information pushed the other way, *into* the zero point
  (compression, Axiom 2.10's Ω). Its sign is not incidental: the contraction
  direction reverses orientation — it is the seam parity flip (Phase 61's Z₂
  meridian holonomy; Phase 65's period-2 parity circle). One gate crossing
  carries the factor ψ: magnitude 1/φ, sign = parity.

The associator [x,y,z] = (x·y)·z − x·(y·z) compares two bracketings of the
same three factors. Both orderings contain the same single gate crossings, so
they agree to first order in ψ; the mismatch appears only where the two
paths' crossing histories differ — **two crossings deep**. Hence

  [x,y,z]_fixed point ∝ ψ² = (−1/φ)² = **+1/φ²** — exactly, and **parity-even**
  (the seam sign squares away), matching Phase 63's observation that the
  golden factor scales the parity-even coupling.

The inverse statement is Phase 63's: a vacuum loop pays the associator
suppression, so its effective threshold is pushed UP by φ²:
M_assoc = m_e/ψ² = φ²m_e = 1.338 MeV. The postulate becomes an output.

This also resolves the 1.0 vs 1/φ² discrepancy: the Phase-5 associator = 1.0
was the **raw, unrenormalized** gate product (inserted by axiom); 1/φ² is the
value **after RG projection** onto the fixed point — the two numbers were
never the same quantity.

**Hypotheses (pre-registered before compute):**

- **H66a — the conjugate pair.** The substitution matrix eigenvalues are
  exactly φ and ψ = −1/φ, and ψ equals the finite-resolution Fibonacci
  contraction ratio lim(−F_k/F_{k+1}) to machine precision. (Grounding;
  analytic, verified numerically.)
- **H66b — the contraction eigenvector carries the seam sign.** The ψ
  eigendirection is the orientation-reversing one: the parity-flip operator
  of Phase 61/65 conjugates the RG step (M intertwines with the Z₂ flip with
  eigenvalue −1 on the contracting axis). The minus in −1/φ IS the seam.
- **H66c — the runtime associator converges to 1/φ².** In
  `code/directed_numbers.py`, the absolute-zero gate product P(r) is a
  uniform placeholder with an explicit TODO ("replace with golden-ratio-based
  distribution"). Replace it with the distribution implied by the golden
  partition of the spectral circle (the anti-resonant Fibonacci partition of
  `notes/discrete_substrate_not_raster.md` §3.3, whose continuum attractor is
  1/φ²) and measure the associator for absolute-zero triples: the prediction
  is E|[x,y,z]| → 1/φ² in the continuum (fine-resolution) limit, vs 2/3 for
  the uniform placeholder — a clean falsifiable contrast. If the golden-gate
  distribution does NOT land on 1/φ², the analytic derivation (H66a/b)
  stands but the runtime gate axiom is what needs revision — either outcome
  closes the TODO honestly.
- **H66d — Phase 63 without the postulate.** Recompute the c₁ reading with
  the derived amplitude ψ² as INPUT: M_assoc = m_e/ψ² = φ²m_e must
  reproduce the Phase-63 band (R = 1.114, E_VR = 2.84 keV) with no
  candidate-scale selection step.
- **H66e — OQ1 first estimate.** The stacking stopping rule: if the
  stacking-triple associator at level n costs ψ²ⁿ, the level-4/level-3
  suppression ratio is 1/φ² — the first dynamical number for the
  dimensional-emergence note's OQ1.

**Honest framing.** H66a/b are exact mathematics of an already-verified RG
kernel — the phase's new content is the *identification* of ψ as the
compression eigenvalue and the second-order counting argument. H66c is the
genuinely risky runtime test: the mapping from the golden partition to P(r)
is a design choice made in the open, and a miss is informative (it localizes
the gap in Axiom 2.9, not in the RG). The phase does NOT claim to derive the
QED-strength value of c₁ — only the origin of the φ² factor in it.

**Deliverables:** `code/phase66_associator_derivation.py`,
`tests/test_phase66_associator.py`, outputs under `code/outputs/phase66/`,
this plan file; if confirmed, Axiom 2.14's status changes from axiom to
theorem-of-the-RG, and registry row 63's "why-phi^2 derivation still open"
closes.
