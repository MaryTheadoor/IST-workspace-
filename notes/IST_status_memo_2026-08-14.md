# IST Status Memo — Session Close 2026-08-14 (Resume Document)

**Repo head:** `ffc02e7` (Phases 64–65 docs sync) · **Tests:** 737 passing ·
**Working tree:** clean, up to date with `origin/main` (GitHub = backup, kept
in tight sync — the protocol in `AGENTS.md`).

---

## 1. Theory center of gravity (as of Phase 65)

| Pillar | State | Where |
|---|---|---|
| θ = ½ twist | Derived (Phase 47); now also the **spin-statistics generator** (Phase 61: exchange phase = Z₂ meridian holonomy; fermions −1, bosons +1; Pauli exclusion = the exchange algebra; anyon collapse IS the Z₂) | Phases 47, 61 |
| Mass tower | 6π⁵ = N_c·Vol_topo(SU(3)) (99.9981%; the **topological** volume, data-selected over the Haar √3π⁵ — `notes/phase49_internal_memo.md`); neutron 0.02σ; Koide 0.0009%; octet partition | Phases 27–49 |
| **Flagship 4WM** | **GATED but surviving**: c₂/c₁ = 0 structurally (n(E∥B) ≡ 1 exactly — the E∥B mode is non-refractive at all angles); the 52.3× magnitude reading gated off; **c₁_IST = 1.114×QED with M_assoc = φ²m_e** (Phase 63); registration proceeds in the structural form only | Phases 55–57, 62–63 |
| Fermion taxonomy | **Complete**: electron = closed single-strand knot (massive), neutrino = open single-strand (light), photon = dual-strand (boson) — parity from strand count, mass from closure (Phase 64) | Phases 52–64 |
| φ dividing line | φ lives in emergent bound states, NOT bare couplings/quarks/spectral dimension; φ = RG/inflation eigenvalue (err 9.8e-9) | Phases 37–58 |
| Dimensional emergence | **Upgraded this session**: P3′ locus/QRF (the zero point is a locus, stacking is observer-relative — isotropy selects the locus reading); P4 (universe expands into time); P4′ (entanglement shares the zero point, not space — Phase 26/40 unification); spin = rotation around the locus (§5); OQ7 signature duality (elliptic zero vs hyperbolic time — **runtime-confirmed at the first layer**, Phase 65) | `notes/IST_dimensional_emergence.md` |
| Cosmology | "4σ" retracted (Phase 60); golden-period form (Δ = ln φ, ε = α/φ²) is the pre-registered DESI DR2 target; **×38 amplitude gap** remains the honest open problem | Phases 59–60 |

## 2. Open items — prioritized queue (for the next session)

**Derivations**
1. **Why-φ² (associator amplitude)** — the top derivation gap: why the vacuum
   loop pays exactly φ² (Phase 63's outstanding item; ties to the oldest open
   discrepancy, Phase 5 §7.3: associator 1.0 vs 1/φ²). Likely drags OQ1 (the
   stacking stopping rule) with it.
2. **Photon template → Lorentz structure** (OQ5): does the dual-mode geometry
   fix the sheet's local frame so the Lorentz structure follows?
3. **Gravity from thread-counting**: derive 1/r² from counting stretched
   lattice threads (`notes/gravity_from_dimensional_collapse.md`).

**Runtime phases**
4. **H-QM1/H-QM2 (TPS test + K-dual scan)** — `notes/quantum_mereology_ist_mapping.md`;
   the master equation + zero-point state should select the thread/sheet
   factorization via K-locality; either outcome publishable.
5. **Phase 6x sheet-stacking automaton** — D_eff crossing 3 with the golden
   window; calibrated on Phases 13/14; now to be built with the P3′ locus
   reading in mind (no naive global stacking axis).
6. **Twist baryogenesis** — Z₂ seam bias + primordial knot-tying; commits to
   absolute proton stability.

**Publishing / observational**
7. **4WM public registration** — structural form (n(E∥B) ≡ 1, mode-resolved)
   with the Phase 62/63 constraint table attached.
8. **DESI DR2 full-shape arena** — the golden-period dark-energy target
   (Berti "Stratoverso"); the ×38 gap's next data.
9. **BH surface-knot sector** — the Kamada refinement's consequence for the
   Hawking knot-census spectrum (dimensional-emergence note §7.2).

## 3. Non-obvious traps (in addition to `AGENTS.md`)

- **Phase-58 flake is FIXED**: `phase51_fibonacci_laplacian.py`'s eigsh calls
  need the deterministic `v0` — the trap is documented in `code/AGENTS.md`.
- **Pytest must run from `code/`**; full suite ≈ 4 min (numba cold cache).
- **Phase-map sync** on new phases: README (theme cluster after the newest),
  `main/cross_phase_synthesis.md` (row), `main/synthesis_paper.md` (§8.1x +
  prediction #N + footer bump), `notes/retrospective_cross_analysis.md`,
  registry CSV (now 89 relations) — then regenerate
  `publication/synthesis_paper.tex/.html` (pandoc portable at
  `C:\Users\AmosA\pandoc\pandoc-3.6.4\pandoc.exe`).
- **Commit protocol**: feat → push, docs → push, per phase; never end a
  session with unpushed commits.

## 4. The user's conceptual contributions this session (all landed)

- Spin as rotation around the zero point (dimensional note §5)
- P3′: the zero point is a **locus, not an axis**; stacking is observer-relative
  (QRF); isotropy selects the locus reading
- P4: the universe expands **into time**; the flow of time is that expansion
- P4′: entanglement propagates through the zero point (no space to traverse) —
  unified with Phase 26/40
- OQ7: hyperbolic time vs elliptic zero — now a runtime-confirmed first layer
  (Phase 65)
- The strand-rule intuition → Phase 64's complete fermion taxonomy

*The next session can pick up anywhere in §2; the top recommendation is
item 1 (why-φ²) or item 4 (TPS test).*
