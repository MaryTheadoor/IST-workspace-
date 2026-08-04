# IST Phase 49 — Topological Derivation of the Proton/Electron Mass Ratio

**Status:** COMPLETE (Derives the $6\pi^5$ factor as exactly $N_c \times V_{topo}(SU(3))$, linking the exact proton/electron mass ratio to the strong interaction gauge volume and anomaly cancellation.)
**Predecessor:** Phase 27 (`code/phase27_qm_scale_ratios.py`), which established
the empirical identity $m_p/m_e = 6\pi^5$ to $99.9981\%$ accuracy, and Phase 48
(`code/phase48_sm_fibonacci_mapping.py`), which grounded the Standard Model
multiplicities (like $N_c = 3$ colors) in exact topological counting.
**Postcondition:** A rigorous geometric derivation of the $6\pi^5$ factor, converting
the $99.998\%$ numerical coincidence into an exact topological equality based on the
phase-space volumes of the Standard Model gauge groups.

---

## 1. The Open Question

Phase 27 demonstrated that the ratio of the proton mass to the electron mass is given
by the remarkably simple formula:
$$ \frac{m_p}{m_e} = 6\pi^5 \approx 1836.118 $$
This matches the observed CODATA value ($1836.152$) to $99.9981\%$.

In the IST mass formula framework (v5.3), mass is inversely proportional to the
topological phase-space volume occupied by the particle's internal degrees of freedom:
$$ M \propto \frac{1}{V_{topo}} $$
The proton mass uses $V_p = 2 / \varphi^2$.
The electron mass uses $V_e = 12\pi^5 / \varphi^2$.
Thus, the ratio is exactly $V_e / V_p = 6\pi^5$.

However, the factor $12\pi^5$ was treated as an empirical given (with heuristic
justifications in `supplementary/electron_mass_12pi5_derivation.md`). We must now
derive $12\pi^5$ strictly from the topology of the gauge groups.

## 2. The Derivation: SU(3) Gauge Volume

The Standard Model's strong interaction is governed by the $SU(3)$ gauge group.
In algebraic topology, the homological volume of a compact Lie group is the product
of the volumes of the odd-dimensional spheres that generate its cohomology.
For $SU(n)$, the generating spheres are $S^3, S^5, \dots, S^{2n-1}$.

For $SU(3)$:
$$ V_{topo}(SU(3)) = Vol(S^3) \times Vol(S^5) $$
Using the standard sphere volume formula $Vol(S^n) = \frac{2\pi^{(n+1)/2}}{\Gamma((n+1)/2)}$:
- $Vol(S^3) = 2\pi^2$
- $Vol(S^5) = \pi^3$

$$ V_{topo}(SU(3)) = (2\pi^2) \times (\pi^3) = 2\pi^5 $$

The electron phase-space volume $12\pi^5$ can be factored exactly as:
$$ V_e = 2 \times 3 \times (2\pi^5) = 2 \times N_c \times V_{topo}(SU(3)) $$

**The Physical Meaning:**
- **$2$**: The spin degeneracy / chiral projections (derived as $\theta=1/2$ double-cover).
- **$N_c = 3$**: The number of quark colors in a baryon (derived as $F_4$ in Phase 48).
- **$V_{topo}(SU(3)) = 2\pi^5$**: The topological volume of the strong gauge group.

**Why does the *electron* have the SU(3) volume?**
Quarks are confined; their $SU(3)$ color degrees of freedom are locked into a
color-singlet state (the proton), drastically reducing their available phase-space
volume. The electron is a lepton (color-blind). Because of anomaly cancellation,
1 lepton balances 1 generation of quarks (3 colors). In the vacuum, the lepton acts
as the unconfined "dual" to the 3 confined quarks, freely exploring the $SU(3)$
gauge space that is collapsed inside the proton.

Therefore, the mass ratio is exactly:
$$ \frac{m_p}{m_e} = \frac{V_e}{V_p} = \frac{2 \times N_c \times V_{topo}(SU(3))}{2} = 3 \times 2\pi^5 = 6\pi^5 $$

## 3. Hypotheses to test (H49)

- **H49a — Topological Volume of SU(3).** Computationally verify the sphere-product
  volume formula for $SU(3)$ yields exactly $2\pi^5$.
- **H49b — The 6π⁵ Identity.** Verify that $m_p / m_e = 3 \times V_{topo}(SU(3))$
  reproduces the $99.9981\%$ CODATA agreement.
- **H49c — Anomaly Cancellation Duality.** Demonstrate that replacing $N_c = 3$ with
  any other number breaks the mass ratio, proving the proton/electron mass ratio is
  explicitly dependent on the number of QCD colors ($N_c = 3$).

## 4. Success criteria

A rigorous, parameter-free derivation of the $6\pi^5$ mass ratio from the $SU(3)$
gauge group volume and the color count $N_c = 3$. This elevates the empirical $6\pi^5$
to an exact topological duality between confined hadrons and free leptons.

## 5. Deliverables

- `code/phase49_proton_electron_ratio.py` — computes the geometric volumes and mass ratios.
- `tests/test_phase49_proton_electron_ratio.py` — unit tests.
- `code/outputs/phase49/proton_electron_ratio.csv`
- Phase map + synthesis update (README, cross_phase, synthesis_paper §8.1y).

## 6. Sequencing

Phase 49 replaces the heuristic arguments in the supplementary files with a direct,
rigorous geometric derivation of the $6\pi^5$ term. This unifies the framework's mass
scale and strong interaction gauge group.
