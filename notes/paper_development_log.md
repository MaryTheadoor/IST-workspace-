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
- Phase 45 (baryon octet, Λ–Σ golden partition): `notes/IST_Phase_45_plan.md`,
  `code/phase45_baryon_octet.py`. Resolves the Phase 34 open octet: Σ golden-partitions
  the Λ→Ξ interval — (Σ−Λ)/(Ξ−Λ) = 1/φ² (0.108%), parameter-free Σ prediction 0.007%,
  Ξ from (Λ,Σ) 0.017%, GMO anchor 0.57%, base-specificity 0.38% basin. Two clean SU(3)
  laws (decuplet E-ladder + octet golden partition). A v8.0 paper update should fold
  this into the Phase 34/35 (§8.1j-k) discussion as the octet closure.
- Phase 46 (reference-level fix, honest negative): `notes/IST_Phase_46_plan.md`,
  `code/phase46_reference_rescope.py`. Answers the Phase 43 sequencing question:
  the m_t 0.090/0.108 scheme-dependence does NOT re-scope the alpha_s flavor
  closure. REFUTED on all fronts (H46a-e): m_t=0.108 worsens RMS 8.78→12.70%;
  QCD-consistent refs score worse (12.10%); free refs in credible ranges still
  leave m_b +7.4%/M_Z −2.5% OUT; two free exponents fail; the required layer base
  flips sign above m_b (phi^+0.82 vs principled phi^-0.5) — golden power-law
  running cannot match QCD's ~1/ln E curvature at ANY reference choice. Closes the
  alpha_s closure line as reference-irreducible. A v8.0 paper update should fold
  this into the Phase 39/§8.4(flavor) discussion as the definitive closure negative.
- Phase 47 (emergent-twist derivation, closed): `notes/IST_Phase_47_plan.md`,
  `code/phase47_emergent_twist.py`. Derives the framework's ubiquitous $\theta=1/2$
  fractional twist directly from the non-orientable substrate topology. The Klein
  seam has a flat Z2 holonomy of -1; to support a complex quantum field, this embeds
  into a U(1) bundle as the phase $e^{i\pi}$. The twist is the fractional winding
  number $\arg(-1)/2\pi = 1/2$. Parameter-free, exact, and grid-independent. Unifies
  neutron, Koide, and baryon decuplet under a derived topological invariant. A v8.0
  paper update should add this as §8.1w.
- Phase 48 (stable-knot SM multiplicity mapping, closed): `notes/IST_Phase_48_plan.md`,
  `code/phase48_sm_fibonacci_mapping.py`. Resolves the final structural open item.
  Maps the Phase 24 empirical ~3% stable-knot fraction to the Standard Model particle
  multiplicities. Because the substrate is a Fibonacci lattice, topological defects
  follow the Fibonacci sequence F_1 through F_9 exactly: 1 (Higgs), 1 (Photon),
  2 (Chiralities), 3 (Generations/Weak bosons), 5 (Fermion multiplets), 8 (Gluons/Fermions
  per gen), 13 (Total bosons), 21 (Total fundamental types). The theoretical knot
  fraction is exactly 1/F_9 = 1/34 ≈ 2.941%, consistent with the Phase 24 data. The
  boson/fermion ratio is F_7/F_6 = 1.625 ≈ φ. A v8.0 paper update should add this as §8.1x.
- Phase 49 (topological proton/electron mass ratio, closed): `notes/IST_Phase_49_plan.md`,
  `code/phase49_proton_electron_ratio.py`. Re-evaluates the Phase 27 finding that
  m_p/m_e = 6pi^5. Derives this factor exactly from the topological (Poincare) volume
  of the SU(3) gauge group, Vol(SU(3)) = 2pi^5. Shows that the mass ratio is exactly
  N_c * Vol(SU(3)) = 3 * 2pi^5 = 6pi^5. A v8.0 paper update should add this as §8.1y.
- Phase 50 (light quark golden partition test, honest negative): `notes/IST_Phase_50_plan.md`,
  `code/phase50_light_quark_partition.py`. Tests whether the bare (u,d,s) quarks obey the
  Baryon Octet's Golden Partition. REFUTED: (m_d-m_u)/(m_s-m_u)=0.0275 vs 1/φ²=0.382 (92.8%
  off). Proves the ratio is RG-invariant (all light quarks share γ_m), so the negative is
  scale-independent, and fails in Koide sqrt-space too. Conclusion: the Golden Partition is
  an emergent property of hadronic bound-state knots, not bare quarks — refining where φ
  lives (with Phase 37 and Phase 46). A v8.0 paper update should add this as §8.1z.
