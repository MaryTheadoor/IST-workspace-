"""Tests for Phase 66 - why-φ²: the associator amplitude from the conjugate root.
Verifies: (H66a) the conjugate pair φ, ψ = −1/φ; (H66b) the contraction eigenvector
carries the seam sign; (H66c) the runtime associator converges to 1/φ²; (H66d) Phase 63
is reproduced without the postulate; (H66e) the OQ1 stacking ratio is 1/φ²."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_klein_laplacian import PHI
from phase66_associator_derivation import (
    PSI, PSI_SQ, conjugate_pair, seam_conjugation, golden_gate_distribution,
    associator_expectation, phase63_reproduction, oq1_stacking,
)


# ───────────────────────────────────────────────────────────────────────────────
# H66a - THE CONJUGATE PAIR
# ───────────────────────────────────────────────────────────────────────────────

def test_conjugate_pair_eigenvalues():
    """The substitution matrix eigenvalues are exactly φ and ψ = −1/φ."""
    rows, summary = conjugate_pair(n_fib=10)
    assert abs(summary["eig_phi"] - PHI) < 1e-10
    assert abs(summary["eig_psi"] - PSI) < 1e-10


def test_conjugate_pair_fibonacci_convergence():
    """The Fibonacci contraction ratio converges to ψ to machine precision."""
    rows, summary = conjugate_pair(n_fib=20)
    # at k=20, the error should be < 1e-8
    assert rows[-1]["error_vs_psi"] < 1e-8


# ───────────────────────────────────────────────────────────────────────────────
# H66b - THE CONTRACTION EIGENVECTOR CARRIES THE SEAM SIGN
# ───────────────────────────────────────────────────────────────────────────────

def test_seam_conjugation_first_component_flipped():
    """The parity-flip operator P conjugates the RG step with eigenvalue −1 on
    the contracting axis: the ψ eigenvector's first component flips sign."""
    seam = seam_conjugation()
    assert seam["first_component_flipped"]


def test_seam_conjugation_eigenvalues_preserved():
    """The conjugated matrix P·M·P⁻¹ has the same eigenvalues as M."""
    seam = seam_conjugation()
    assert seam["eigenvalues_preserved"]


# ───────────────────────────────────────────────────────────────────────────────
# H66c - THE RUNTIME ASSOCIATOR CONVERGES TO 1/φ²
# ───────────────────────────────────────────────────────────────────────────────

def test_golden_gate_distribution_symmetric():
    """The golden-gate distribution is symmetric around 0."""
    r_vals = golden_gate_distribution(10000, seed=42)
    assert abs(np.mean(r_vals)) < 0.05  # mean ≈ 0


def test_golden_gate_distribution_bounded():
    """The golden-gate distribution is bounded in [−1, 1]."""
    r_vals = golden_gate_distribution(10000, seed=42)
    assert np.all(r_vals >= -1.0) and np.all(r_vals <= 1.0)


def test_associator_expectation_converges_to_1_over_phi2():
    """The runtime associator E|[x,y,z]| converges to 1/φ² for the golden-gate
    distribution (vs 2/3 for the uniform placeholder)."""
    mean, stderr = associator_expectation(N_samples=50000, seed=42)
    # should be within 1% of 1/φ²
    assert abs(mean - PSI_SQ) < 0.01 * PSI_SQ
    # and far from the uniform placeholder 2/3
    assert abs(mean - 2/3) > 0.2


# ───────────────────────────────────────────────────────────────────────────────
# H66d - PHASE 63 WITHOUT THE POSTULATE
# ───────────────────────────────────────────────────────────────────────────────

def test_phase63_reproduction_matches():
    """Recomputing the c₁ reading with the derived amplitude ψ² reproduces the
    Phase-63 φ² m_e reading."""
    p63 = phase63_reproduction()
    assert p63["matches_phase63"]
    assert p63["in_2_4_keV_band"]


def test_phase63_reproduction_values():
    """The reproduced values match the Phase-63 outputs."""
    p63 = phase63_reproduction()
    assert abs(p63["M_assoc_MeV"] - PHI**2 * 0.51099895) < 1e-4
    assert abs(p63["R"] - 1.1142) < 0.001
    assert abs(p63["E_VR_keV"] - 2.84) < 0.01


# ───────────────────────────────────────────────────────────────────────────────
# H66e - OQ1 FIRST ESTIMATE
# ───────────────────────────────────────────────────────────────────────────────

def test_oq1_stacking_ratio():
    """The level-4/level-3 stacking suppression ratio is 1/φ²."""
    rows = oq1_stacking(n_levels=5)
    # the ratio at level 4 (index 3) should be 1/φ²
    assert abs(rows[3]["ratio_to_previous"] - PSI_SQ) < 1e-10


def test_oq1_stacking_suppression():
    """The suppression at level n is |ψ|²ⁿ."""
    rows = oq1_stacking(n_levels=5)
    for i, r in enumerate(rows):
        expected = abs(PSI) ** (2 * (i + 1))
        assert abs(r["suppression"] - expected) < 1e-10


# ───────────────────────────────────────────────────────────────────────────────
# INTEGRATION
# ───────────────────────────────────────────────────────────────────────────────

def test_psi_squared_is_1_over_phi_squared():
    """The analytic core: ψ² = (−1/φ)² = +1/φ² (parity-even)."""
    assert abs(PSI_SQ - 1.0 / PHI**2) < 1e-15


def test_psi_is_negative():
    """The contraction eigenvalue is negative (the seam sign)."""
    assert PSI < 0


def test_psi_squared_is_positive():
    """The associator amplitude is parity-even (the sign squares away)."""
    assert PSI_SQ > 0
