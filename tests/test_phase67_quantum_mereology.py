"""Tests for Phase 67 - quantum mereology: the TPS test and K-dual scan."""

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase67_quantum_mereology import (
    construct_hamiltonian, zero_point_state, entanglement_entropy,
    tps_selection_test, photon_strand_hamiltonian, kdual_scan,
)


# ───────────────────────────────────────────────────────────────────────────────
# H67a - TPS SELECTION TEST
# ───────────────────────────────────────────────────────────────────────────────

def test_hamiltonian_is_hermitian():
    """The Hamiltonian constructed from the master equation is Hermitian."""
    H = construct_hamiltonian(n_sites=4)
    assert np.allclose(H, H.conj().T)


def test_zero_point_state_normalized():
    """The zero-point state is normalized."""
    psi = zero_point_state(n_sites=4)
    assert np.isclose(np.linalg.norm(psi), 1.0)


def test_entanglement_entropy_nonnegative():
    """Entanglement entropy is non-negative."""
    psi = zero_point_state(n_sites=4)
    S = entanglement_entropy(psi, n_sites=4, partition=[0, 1])
    assert S >= 0


def test_tps_selection_test_runs():
    """The TPS selection test runs and returns rows."""
    rows = tps_selection_test(n_sites=4)
    assert len(rows) == 11  # 1 thread/sheet + 10 random
    assert rows[0]["basis"] == "thread/sheet"


def test_tps_selection_result():
    """The TPS selection test result: the zero-point state has equal entropy
    in all bases (honest negative — the dynamics don't select the factorization
    in the pre-mereological phase)."""
    rows = tps_selection_test(n_sites=4)
    S_thread_sheet = rows[0]["entropy"]
    S_alt_mean = np.mean([r["entropy"] for r in rows[1:]])
    # the margin should be ~0 (honest negative)
    margin = (S_alt_mean - S_thread_sheet) / S_alt_mean * 100
    assert abs(margin) < 5  # within 5% (effectively zero)


# ───────────────────────────────────────────────────────────────────────────────
# H67b - K-DUAL SCAN
# ───────────────────────────────────────────────────────────────────────────────

def test_photon_strand_hamiltonian_is_hermitian():
    """The photon strand Hamiltonian is Hermitian."""
    H = photon_strand_hamiltonian()
    assert np.allclose(H, H.conj().T)


def test_kdual_scan_runs():
    """The K-dual scan runs and returns rows."""
    rows = kdual_scan(n_samples=10, tol=1e-6)
    assert len(rows) == 10
    assert "klocality_preserved" in rows[0]
    assert "factorization_changed" in rows[0]


def test_kdual_scan_result():
    """The K-dual scan result: no K-dual factorizations found (strong uniqueness
    result for the photon's dual-strand decomposition)."""
    rows = kdual_scan(n_samples=100, tol=1e-6)
    n_kdual = sum(1 for r in rows if r["klocality_preserved"] and r["factorization_changed"])
    # no K-duals found
    assert n_kdual == 0


# ───────────────────────────────────────────────────────────────────────────────
# INTEGRATION
# ───────────────────────────────────────────────────────────────────────────────

def test_h67a_h67b_combined():
    """The combined verdict: H67a fails (dynamics don't select factorization in
    pre-mereological phase), H67b passes (no K-duals). The mismatch localizes
    the gap: the thread/sheet/strand decomposition must emerge after the
    coherence threshold."""
    tps_rows = tps_selection_test(n_sites=4)
    S_thread_sheet = tps_rows[0]["entropy"]
    S_alt_mean = np.mean([r["entropy"] for r in tps_rows[1:]])
    margin = (S_alt_mean - S_thread_sheet) / S_alt_mean * 100
    h67a_pass = margin > 10

    kd_rows = kdual_scan(n_samples=100, tol=1e-6)
    n_kdual = sum(1 for r in kd_rows if r["klocality_preserved"] and r["factorization_changed"])
    h67b_pass = n_kdual == 0

    # H67a fails, H67b passes
    assert not h67a_pass
    assert h67b_pass
