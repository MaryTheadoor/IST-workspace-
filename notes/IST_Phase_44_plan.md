# IST Phase 44 — BAO Sound-Horizon Test of Dimensional Crystallization

**Status:** COMPLETE (honest negative; BAO confirms the Phase 36 refined picture)
**Predecessor:** Phase 36 (`code/phase36_dimensional_crystallization.py`) —
H(z) chronometers cannot distinguish crystallization from LCDM (Δχ² < 1) and
the CMB shift prior excludes D→2 by recombination (985σ), forcing the refined
picture D(1090) ≈ 3.
**Open question:** the BAO standard ruler — high-precision D_M(z)/r_d and
D_H(z)/r_d at five redshifts — was never confronted with the crystallization
geometry. Does it (a) break the H(z) degeneracy, (b) independently confirm
D ≈ 3 at observable z, or (c) expose a sound-horizon tension?
**Answer:** (b) with an honest negative — BAO does NOT break the degeneracy
(Δχ² = −4.6 joint), the z_c basin is flat (χ² 35–38 across z_c = 0.5–8), and
the only strong tension is the model-independent D_H(0.51) anomaly (+5.7σ
cryst / +5.6σ lcdm). The refined picture D ≈ 3 at observable z survives the
ruler; discriminators remain at higher z.

---

## 1. The problem restated

Phase 36 established:

| probe | result |
|---|---|
| H(z) chronometers (60 pts) | Δχ²(cryst − LCDM) < 1 → degenerate |
| CMB shift R = 1.7502 ± 0.0046 | D→2 at recombination → R ~ 6 → 985σ excluded |
| Refined picture | third dimension essentially always present at observable z; z_c ≫ 1 |

But the H(z) dataset only reaches z ≈ 2.36 and its errors are ~10%. The BAO
sound-horizon ruler measures *distances* — D_M(z) (comoving, via θ_BAO = r_d/D_M)
and D_H(z) = c/H(z) (via Δz) — with 1–5% precision at z = 0.51–1.49. These are
integral geometry probes: D_M(z) = (c/H0) ∫₀ᶻ dz'/E(z') where E(z') =
√(Ωm(1+z')^D(z') + (1−Ωm)). If the crystallization geometry at observable z
deviates from LCDM, the predicted distances shift and BAO sees it.

## 2. Data

- DESI DR1 BAO (from `code/phase16_joint_fit.py`, r_d = 147.09 Mpc):
  (z, D_M/r_d, σ_DM, D_H/r_d, σ_DH, corr) at z = 0.51, 0.71, 0.93, 1.32, 1.49.
- 60 H(z) cosmic chronometers (`data/hz_cosmic_chronometers.csv`).
- Planck 2018 shift prior R = 1.7502 ± 0.0046 (for the joint constraint, from
  Phase 36).

## 3. Hypotheses to test (H44)

1. **H44a — BAO breaks the H(z) degeneracy.** Joint H(z)+BAO fit under
   crystallization vs LCDM. Report Δχ². If BAO is decisive (Δχ² ≫ 1 or z_c
   forced toward large), the standard ruler adds discriminating power Phase 36
   lacked. If Δχ² stays < 1, the degeneracy survives BAO at z ≤ 1.5.
2. **H44b — Sound-horizon consistency at the H(z)-preferred solution.** Score
   the DESI BAO points (D_M/r_d, D_H/r_d with the measured correlation
   coefficient) under Phase 36's best crystallization params
   (H0 ≈ 67, Ωm ≈ 0.34, z_c = 4, w = 1) and under best LCDM. Does the
   crystallization geometry still pass the BAO ruler?
3. **H44c — BAO-only constraint on z_c.** Fit (H0, Ωm) with z_c ∈ {1,2,3,4,8,large}
   against BAO only. Map the z_c basin. Expectation: BAO at z ≤ 1.5 is
   insensitive to z_c ≳ 4 (geometry ≈ LCDM there), but strongly rejects
   z_c ≲ 1 (D→2 inside the BAO z-range → distance shift).
4. **H44d — The sound-horizon consistency check.** Compute the predicted
   D_M(z)/r_d and D_H(z)/r_d under each model at the BAO redshifts, and report
   the worst |pred/obs − 1| and the per-point pulls. A crystallization
   geometry whose distances disagree with DESI BAO at high significance would
   be an honest falsification of the observable-z picture.

## 4. Success criteria

- **Confirmation:** BAO independently supports the refined Phase 36 picture —
  crystallization with D ≈ 3 at observable z passes all DESI BAO points within
  ~1σ, z_c ≳ 4 is BAO-allowed, and z_c ≲ 1 is BAO-excluded (complementary to
  the CMB-shift exclusion).
- **Degeneracy persists:** Δχ²(H(z)+BAO) < 1 and z_c basin includes 4 → the
  H(z) degeneracy is intrinsic to the observable-z geometry, honest negative.
- **Sound-horizon tension:** any crystallization geometry that fits H(z) fails
  DESI BAO at > 2σ (or vice versa) → report the tension and its source.

## 5. Deliverables

- `code/phase44_bao_sound_horizon.py` — crystallization geometry, BAO chi²
  (with corr), H44a–d fits, CSV + figure.
- `tests/test_phase44_bao_sound_horizon.py` — tests encoding H44a–d.
- `code/outputs/phase44/` — `bao_sound_horizon.csv`, figure.
- Phase map + synthesis update (README.md, cross_phase_synthesis.md,
  synthesis_paper.md §8.1t, retrospective_cross_analysis.md).

## 6. Conventions (reused from prior phases)

- Crystallization: H(z)² = H0² [Ωm(1+z)^D(z) + (1−Ωm)], D(z) = 2 + sigmoid((z_c − z)/w).
- BAO: D_M(z)/r_d = (c/H0)∫₀ᶻ dz'/E(z') / r_d; D_H(z)/r_d = (c/H0)/E(z) / r_d.
- Covariance: [[σ_DM², ρ σ_DM σ_DH], [ρ σ_DM σ_DH, σ_DH²]].
- r_d = 147.09 Mpc (DESI/CMB sound horizon, matches phases 16/18).

## 7. Sequencing

Phase 44 is the immediate successor to Phase 36 called out in the Phase 43
sequencing note. Standing open items after this: baryon octet Lambda-Sigma
mixing; stable-knot → SM multiplicity mapping; the m_t reference-level rescope
from Phase 43.
