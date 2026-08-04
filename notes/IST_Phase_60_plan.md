# IST Phase 60 Plan — Auditing the "4σ" Oscillatory-DE Headline + the Amplitude Bridge

**Origin.** Phase 59 audited the *log-periodic* time-crystal form of the
oscillatory dark energy (H(z)-only) and found the free-period claim collapses
(global p = 0.62) while the pre-registered golden period Δ = ln φ survives as a
well-constrained hint (Δχ² = +2.20, ε ≈ 0.106, 2.5 cycles). But the paper's
headline observable claim is **different and larger**: "oscillatory DE preferred
over ΛCDM at ~4σ (Δχ² = 22.1) in a joint fit to 60 H(z) chronometers, 1701
Pantheon+ SNe Ia, and DESI DR1 BAO", with an **amplitude-decaying** form
ε(z) = ε0·(1+z)^β and "fitted β ≈ 4.16 within 2% of β = φ³ = 4.236"
(`main/ist_v8_0_topology_substrate.md` §4.4, Table). That claim has never been
audited the way Phase 59 audited the H(z)-only claim.

**The claim is already internally inconsistent at the source.** (1) The v8
table lists *both* "IST (β = 1/φ)" and "IST (free β)" with *identical* χ² = 926 —
suspicious. (2) The prose says "fitted β ≈ 4.16 ≈ φ³", but the code that backs
it (`code/phase16_joint_fit.py`) uses **β = 1/φ** as the fixed case and its
"dimensional test" fixes β = φ^d (d = 1..4) rather than fitting β freely. (3)
ε0 is never stated as a derived value in the table (the code's
`EPS_PRED = α/φ²` is used in a *different*, never-tabulated "fixed_eps" case).
(4) The modulation's frequency/phase is under-specified in prose (the code uses
cos(2π·ln(1+z)/Δ) with Δ free).

**Phase 60 — the audit + the bridge (both tracks, as chosen):**

**Track A — the 4σ audit (reproducible, pre-registered, look-elsewhere-accounted).**

- **H60a — reproduce the joint fit.** Joint ΛCDM vs the free oscillatory model
  (fit H0, Ωm, ε0, Δ, β) over 60 H(z) + 1701 Pantheon+ + DESI DR1 BAO. Report
  the *actual* Δχ², H0, and best (ε0, Δ, β) and compare against the v8 claim
  (Δχ² = 22.1, H0 73.6→71.4, β ≈ 4.16). This closes a reproducibility gap:
  the claim exists only as prose + a slow, partially-redundant Phase-16 script.
- **H60b — the pre-registered strict fit.** Fix ALL oscillation parameters at
  derived values — (ε0, Δ, β) = (α/φ², ln φ, φ³) — and fit only (H0, Ωm).
  Also the v8-consistent variant (α/φ², ln φ, 1/φ). Does the *derived*
  prediction beat ΛCDM on the full data, or is the 4σ an artifact of free
  (large) ε0?
- **H60c — look-elsewhere accounting.** The free fit searches Δ over the
  log-redshift window and β over a range. Apply the Phase-59 frequency-band
  trial count for Δ (N_ind = (1/Δmin−1/Δmax)·ln(1+zmax) ≈ 4) to the Δ-profile
  maximum and report the *global* significance of the headline Δχ². Verdict:
  does the "4σ" survive accounting? (Nominal 4σ over 1701 SNe is statistically
  plausible, but a searched period + exponent inflates it — the numbers decide.)

**Track B — the amplitude bridge (why ε ≈ 0.1, not α/φ²).**

- **H60d — the (1+z)^β law as the e-fold amplification.** Phase 59's golden
  period fit wants ε ≈ 0.106; the master equation gives ε0 = α/φ² = 0.002787
  (~37× gap). Test whether ε_eff(z) = ε0·(1+z)^β with the *derived* β = φ³
  (and the code's β = 1/φ) bridges the gap at the characteristic redshifts of
  each dataset (H(z) at z̄ ≈ 1, Pantheon+ at z̄ ≈ 0.2): ε_eff vs the fitted ε0
  from H60a and vs Phase 59's ε ≈ 0.106. If the φ³ law lands within the fitted
  band, the amplification is *derived*; if it does not, the gap is admitted as
  open (the old note's "e-fold running" hand-wave is either quantified or
  rejected).

**Honest framing (for plan/paper).** This is the paper's most prominent
observational claim being put through the same discipline Phase 59 applied to
its smaller cousin: reproducible code, pre-registered anchors, look-elsewhere
accounting. Expected spectrum of outcomes: (a) the joint Δχ² ~ 22 reproduces
but its global significance is reduced (searched Δ/β) and the strict derived
model (H60b) is near-invisible — the "4σ" becomes "a fitted-parameter
preference, not a derived prediction"; (b) the H60d bridge quantifies (or fails
to quantify) ε ≈ 0.1 from α/φ². The numbers decide; the phase is the audit.

**Deliverables:** `code/phase60_oscillatory_de_audit.py`,
`tests/test_phase60_oscillatory_de_audit.py`, outputs under
`code/outputs/phase60/`, `notes/IST_Phase_60_plan.md`.

**Phase-map sync (all three + retrospective):** README.md (highlights section
after Phase 59), `main/cross_phase_synthesis.md` (row 60),
`main/synthesis_paper.md` (§8.1ai + observable prediction #18, footer bump to
v2.9), `notes/retrospective_cross_analysis.md` (Phase 60 entry). Registry
appended (65 → 69 rows). Note the historical registry count drift (footers
claimed 60 at Phase 58; file then held 61; now 65) — this phase states counts
from the file.
