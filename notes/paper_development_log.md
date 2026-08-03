# IST Paper Development Log

## v7.0 — Strict Physics Core (August 2026)

### Decision

Approved reframe of the paper: **new clean document** with a **strict physics core**. The
previous v6.0 build (`main/ist_v6_0_topology_substrate.md`) was a Phase 1-24 snapshot with
stale counts and placeholder appendices. v7.0 (`main/ist_v7_0_topology_substrate.md`) covers
the full 42-phase arc (510 tests), the half-integer twist $\theta = 1/2$, and the honest
negatives (Phases 36, 37, 42-H42g).

The following material was deliberately cut from v7.0 and is preserved here so the story is
not lost.

### Cut: consciousness/neuroscience material

v7.0 is scoped to physics. The consciousness / neuroscience line (IIT, Tononi, golden-ratio
brain dynamics) is excluded from the paper body.

- **Tononi IIT reference** — `Integrated information theory: from consciousness to its
  physical substrate` (Nature Reviews Neuroscience, 17, 450-461, 2016). Was cited in v6.0
  reference list; removed from v7.0 as an orphaned, out-of-scope citation.
- **Oby et al. neural population activity** — `Dynamical constraints on neural population
  activity` (Nature Neuroscience, 28, 383-393, 2025). v6.0 reference; out of scope.
- **Pletzer golden-ratio brain** — `The golden ratio in human brain dynamics` (Frontiers in
  Human Neuroscience, 9, 123, 2015). v6.0 reference; out of scope.
- v6.0 Section 6.10 "Implications for Consciousness and Computation" and Section 6.11
  "Toward a Generative Ontology" were already stubs (`[Speculative section...]`) and are
  intentionally absent from v7.0. Any future companion paper on this line can start from
  those stubs.

### Cut: Greene-Levin convergence narrative

The "window is NOW / three independent convergences" narrative around Greene-Levin-Kabat-
Porrati *Klein Bottle Cosmology* (arXiv:2511.23447v2) is excluded from the paper body to keep
the physics core strict. It is fully preserved in:

- `analysis/greene_levin_klein_bottle_cosmology.md` — the complete technical comparison
  (CP violation by boundary conditions vs. IST chiral preference; condensate neutrino mass
  vs. generation-dependent mass; DM mass scales).
- `PUBLISHING.md` — the convergence framing, urgency argument, and outreach plan.

### Cut: superseded v6.0 text

- v6.0 abstract/sections carried the stale "24 phases, 319 tests" counts; v7.0 reports
  42 phases / 510 tests.
- v6.0 Appendix A (Simulation Protocols) and Appendix B (Reproducible Simulation Code) were
  placeholders (`[Python code for ...]`); v7.0 replaces them with a real phase map
  (Appendix A) and code/data availability (Appendix B).
- v6.0 Section 3.8 (Retrocausality, Baryogenesis) and Section 4.4 (Local Group dynamics as
  a consistency check) were condensed out; v7.0 keeps only the operational "boundary
  conditions" note (Section 7.3). The Local Group analysis itself lives in
  `analysis/` (Wempe et al. citation removed from the reference list accordingly).

The complete v6.0 markdown, its generated `.tex`, `synthesis_paper.md`, and `PUBLISHING.md`
are preserved verbatim under git tag **`v6.0-paper-snapshot`**.

### Reference bookkeeping (v7.0)

- Removed: Tononi (consciousness), Wempe Local Group (section cut).
- Kept but renumbered: Khinchin (continued fractions), Arnold (KAM), CODATA 2022, NOWN
  electron-mass decomposition. These are now cited explicitly in the body (Sections 5.2,
  5.3, 6.2, 6.3, 6.4, 8.3).

### Related records

- The H42g "137" retraction is documented in `notes/IST_golden_angle_137.md` (Section 5:
  cross-analysis downgrade) and referenced in v7.0 Section 8.2.
- Full Phase 42 detail: `notes/IST_Phase_42_plan.md`, `code/phase42_flavor_closure.py`,
  `code/golden_relation_checks.py`.
- Phase 43 (2-loop golden closure, honest negative): `notes/IST_Phase_43_plan.md`,
  `code/phase43_flavor_closure_2loop.py`. Localizes the flavor-closure residual to the
  m_b→M_Z running slope (+31.5% too steep); confirms the m_t = 0.090 reference is
  scheme-dependent (2-loop QCD running gives 0.108). A v8.0 paper update should fold
  this into the Outlook / Open Questions section.
- Phase 44 (BAO sound-horizon test, honest negative): `notes/IST_Phase_44_plan.md`,
  `code/phase44_bao_sound_horizon.py`. Confronts the Phase 36 crystallization geometry
  with the DESI DR1 BAO ruler (D_M/r_d, D_H/r_d at z 0.51–1.49): joint Δχ² = −4.6,
  flat z_c basin (χ² 35–38), shape delta +9.1 vs the model-independent D_H(0.51)
  anomaly (+5.7σ/+5.6σ). Confirms D ≈ 3 at observable z; discriminators remain at
  higher z. A v8.0 paper update should note this in the Phase 36/§8.1l discussion.
