# IST Phase 67 Plan — Quantum Mereology: The TPS Test and K-Dual Scan

**Origin.** The quantum-mereology mapping note (`notes/quantum_mereology_ist_mapping.md`,
2026-08-12) proposes two runtime tests based on Cotler et al.'s theorem (Theorem 3.9
in [C]): a Hamiltonian plus a state uniquely determine a tensor product structure (TPS),
up to global unitary — dynamics + vacuum select the correct factorization into subsystems.

**The question.** IST's runtime has an implicit ontology: threads (1D information sequences),
sheets (2D surfaces from pairwise thread interactions), and strands (helical dual-mode
structures like the photon). The question is: does the substrate's dynamics (the master
equation, Phase 33) plus its vacuum state (the zero-point, `directed_numbers.py`) select
this thread/sheet/strand factorization uniquely via K-locality? If yes, "particles are
knots" upgrades from interpretation to theorem-adjacent. If no, the mismatch localizes
exactly where the runtime's implicit ontology diverges from its dynamics.

**The two tests (pre-registered):**

- **H-QM1 (TPS selection test):** Does the master equation + zero-point state select,
  via K-locality, the runtime's thread/sheet factorization? Construct a simplified
  Hamiltonian from the master equation's associator term (Phase 33: `delta_n = (alpha/phi^2)
  Xi_eff (1 - c alpha)`), construct the zero-point state (the AbsoluteZero / DirectedZero
  with no memory), and check if the dynamics select a TPS that matches the thread/sheet
  decomposition. The test is: compute the entanglement entropy of the zero-point state
  in the thread/sheet basis vs alternative bases; if the thread/sheet basis minimizes
  the entropy (or maximizes K-locality), the dynamics select it.

- **H-QM2 (K-dual scan):** Does a K-dual factorization of the strand decomposition exist?
  Jordan-Wigner shows one Hamiltonian can admit inequivalent K-local factorizations.
  Scan for alternative factorizations of the photon's dual-strand geometry (Phase 55):
  if one exists, it predicts an alternative-but-equivalent particle description
  (registry-worthy); if none, that is itself a strong uniqueness result. The test is:
  construct the photon's strand Hilbert space (two strands E_+, E_- with rung coupling),
  search for unitary transformations that preserve K-locality but change the factorization;
  if the search finds none (within numerical tolerance), the strand decomposition is
  unique up to the substrate's symmetry orbit.

**Honest framing.** This is a structural consistency test of the runtime's implicit
ontology, not a new physical prediction. The strong form of the claim (that the thread/
sheet/strand decomposition is the unique emergent subsystem structure) remains conjectural;
the phase establishes its first checkable layer. The test is computable but non-trivial:
it requires constructing a Hamiltonian from the master equation, which is a simplification
(the full master equation is non-linear and topological). The phase tests the linearized
associator term in a finite-dimensional Hilbert space; the result is indicative, not
definitive.

**Hypotheses (pre-registered before compute):**

- **H67a (TPS selection):** The master equation's associator term, evaluated on the
  zero-point state, selects the thread/sheet factorization as the unique K-local basis
  (up to the substrate's Z₂ seam symmetry). The entanglement entropy in the thread/sheet
  basis is lower than in alternative bases by a margin > 10%.
- **H67b (K-dual scan):** No K-dual factorization of the photon's dual-strand decomposition
  exists within the substrate's symmetry orbit. The search finds no unitary transformation
  that preserves K-locality while changing the factorization (within numerical tolerance
  1e-6).
- **H67c (verdict):** If both H67a and H67b pass, the runtime's implicit ontology is
  selected by its dynamics — "particles are knots" is theorem-adjacent. If either fails,
  the mismatch localizes the gap.

**Deliverables:** `code/phase67_quantum_mereology.py`, `tests/test_phase67_quantum_mereology.py`,
outputs under `code/outputs/phase67/`, this plan file.

**References:**
- `notes/quantum_mereology_ist_mapping.md` (the proposal)
- [C] Soulas, Franzmann & Di Biagio, "On the emergence of preferred structures in
  quantum theory", hal-05406723 (Dec 2025)
- Cotler et al. (the TPS selection theorem)
- `code/phase33_master_equation_correction.py` (the master equation)
- `code/phase55_photon_compound.py` (the photon's dual-strand geometry)
- `code/directed_numbers.py` (the zero-point state)
