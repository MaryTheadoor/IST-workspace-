# IST Phase 50 — The Light Quark Golden Partition Test

**Status:** COMPLETE (honest negative: the bare light quarks do NOT carry the Golden
Partition; the ratio is RG-invariant and definitively fails in both linear and Koide
space — the partition is an emergent property of the bound-state topological knots,
not the perturbative quarks)
**Predecessor:** Phase 45 (`code/phase45_baryon_octet.py`), which discovered the Baryon
Octet obeys the Golden Partition ($1/\varphi^2$), and Phase 32 (`code/phase32_quark_koide.py`),
which found the light quarks break the Koide relation.
**Postcondition:** A definitive test of whether the bare light quark masses ($u, d, s$)
are structured by the same Golden Partition as the hyperons they comprise, or whether
the partition is an emergent property of the bound state alone.

---

## 1. The Open Question

In Phase 32, we found that the heavy quarks ($c, b, t$) conform to the $\pi/2$ Koide
phase, but the light quarks ($u, d, s$) break it completely. We accepted this as an
"honest negative" due to the topological mass vs RG running distinction.

In Phase 45, we discovered the true law of the Baryon Octet: the hyperons do not
sit on the decuplet's E-ladder. Instead, they follow the **Golden Partition**:
$$ \frac{\Sigma - \Lambda}{\Xi - \Lambda} = \frac{1}{\varphi^2} $$
The $\Sigma$ hyperon splits the $\Lambda \to \Xi$ mass interval exactly at the
$1/\varphi^2$ ratio.

Because these hyperons are bound states of the light quarks ($\Lambda=uds$, $\Sigma=uus/uds/dds$,
$\Xi=uss/dss$), it raises a critical hypothesis: **do the light quark masses break the
Koide relation because they actually follow the Golden Partition themselves?**
Are the bare masses $m_u, m_d, m_s$ golden-partitioned exactly like the baryons they
comprise?

## 2. Hypotheses to test (H50)

- **H50a — The Bare Quark Golden Partition.** Verify whether the bare mass gap ratio
  $(m_d - m_u) / (m_s - m_u)$ matches the target $1/\varphi^2 \approx 0.382$.
- **H50b — RG-Invariance of the Negative.** Because bare quark masses run with the
  renormalization scale $\mu$, a naive test might fail due to the scale choice (e.g.,
  $\mu=2$ GeV). We will prove that because all light quarks run multiplicatively by the
  *same* 1-loop factor ($\gamma_m$), their mass ratios — and thus their gap ratios — are
  strictly RG-invariant. The result is scale-independent.
- **H50c — The Koide-Space Partition.** Test if the partition holds in the
  square-root mass space used by the Koide formula: $(\sqrt{m_d} - \sqrt{m_u}) / (\sqrt{m_s} - \sqrt{m_u})$.

## 3. Success criteria

A clear, quantified answer to whether the bare light quarks carry the Golden Partition.
If it fails (as preliminary math suggests), it stands as a rigorous **honest negative**:
the Golden Partition is a structural law of the hadronic BOUND STATES (topological knots),
not the bare perturbative degrees of freedom. This perfectly mirrors Phase 37, which
found that golden harmonics live in the masses, not the bare couplings.

## 4. Deliverables

- `code/phase50_light_quark_partition.py` — implementation of the scale-invariant test.
- `tests/test_phase50_light_quark_partition.py` — unit tests.
- `code/outputs/phase50/light_quark_partition.csv`
- Phase map + synthesis update (README, cross_phase, synthesis_paper §8.1z).

## 5. Sequencing

Phase 50 re-examines the broken light-quark Koide result through the new lens of the
Octet Golden Partition. It establishes the final dividing line between emergent
topological properties (hadrons) and perturbative quantities (bare quarks).
