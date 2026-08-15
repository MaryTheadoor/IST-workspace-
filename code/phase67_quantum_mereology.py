"""
================================================================================
IST PHASE 67 - Quantum Mereology: The TPS Test and K-Dual Scan
================================================================================
Purpose:
    Tests the quantum-mereology mapping (notes/quantum_mereology_ist_mapping.md):
    does the substrate's dynamics (master equation + zero-point state) select
    the thread/sheet/strand factorization uniquely via K-locality? If yes,
    "particles are knots" upgrades from interpretation to theorem-adjacent
    (Cotler et al. Theorem 3.9: Hamiltonian + state uniquely determine a tensor
    product structure, up to global unitary).

    The runtime has an implicit ontology: threads (1D information sequences),
    sheets (2D surfaces from pairwise thread interactions), strands (helical
    dual-mode structures like the photon). This phase tests whether the
    substrate's dynamics select this factorization.

    Tracks:
      H67a - TPS selection test: construct a Hamiltonian from the master
             equation's associator term (Phase 33), construct the zero-point
             state (AbsoluteZero), and check if the dynamics select the
             thread/sheet factorization as the unique K-local basis. Compute
             the entanglement entropy in the thread/sheet basis vs alternative
             bases; if the thread/sheet basis minimizes the entropy, the
             dynamics select it.
      H67b - K-dual scan: does a K-dual factorization of the photon's dual-
             strand decomposition exist? Jordan-Wigner shows one Hamiltonian
             can admit inequivalent K-local factorizations. Scan for alternative
             factorizations of the photon's strand geometry (Phase 55): if one
             exists, it predicts an alternative-but-equivalent particle
             description; if none, that is a strong uniqueness result.
      H67c - Verdict: if both H67a and H67b pass, the runtime's implicit
             ontology is selected by its dynamics. If either fails, the
             mismatch localizes the gap.

Inputs:   none
Outputs:  code/outputs/phase67/tps_selection.csv
          code/outputs/phase67/kdual_scan.csv
          code/outputs/phase67/quantum_mereology.png

References:
    notes/IST_Phase_67_plan.md
    notes/quantum_mereology_ist_mapping.md
    code/phase33_master_equation_correction.py
    code/phase55_photon_compound.py
    code/directed_numbers.py
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import expm, logm

from phase1_klein_laplacian import PHI
from phase33_master_equation_correction import associator_term

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase67")

ALPHA = 7.2973525693e-3


# ───────────────────────────────────────────────────────────────────────────────
# H67a - TPS SELECTION TEST
# ───────────────────────────────────────────────────────────────────────────────

def construct_hamiltonian(n_sites=4):
    """Construct a Hamiltonian from the master equation's associator term.
    The associator [x,y,z] = (x*y)*z - x*(y*z) measures the failure of
    associativity. In a finite-dimensional Hilbert space, model this as a
    3-body interaction: H_assoc = sum_{i,j,k} J_{ijk} |i><j| x |k><k|,
    where J_{ijk} is the associator coupling. For the thread/sheet
    factorization, the coupling is local (K-local): only adjacent sites
    interact. Returns the Hamiltonian matrix."""
    dim = 2 ** n_sites
    H = np.zeros((dim, dim), dtype=complex)
    # associator coupling from Phase 33
    J = associator_term(ALPHA / PHI ** 2, theta=0.5)
    # 3-body interaction: sigma_z on site i, sigma_x on site j, sigma_z on site k
    # for adjacent triples (i, i+1, i+2)
    for i in range(n_sites - 2):
        # construct the 3-body term
        op = np.eye(1, dtype=complex)
        for site in range(n_sites):
            if site == i or site == i + 2:
                op = np.kron(op, np.array([[1, 0], [0, -1]]))  # sigma_z
            elif site == i + 1:
                op = np.kron(op, np.array([[0, 1], [1, 0]]))  # sigma_x
            else:
                op = np.kron(op, np.eye(2))
        H += J * op
    return H


def zero_point_state(n_sites=4):
    """Construct the zero-point state: the AbsoluteZero with no memory.
    In the directed-numbers runtime, this is the state with amplitude 0,
    parity 'zero', memory None. Model it as the maximally mixed state
    (equal superposition of all basis states) — the pre-mereological phase
    where parts are potential, not actual."""
    dim = 2 ** n_sites
    psi = np.ones(dim, dtype=complex) / np.sqrt(dim)
    return psi


def entanglement_entropy(psi, n_sites, partition):
    """Compute the entanglement entropy of state psi across a bipartition.
    partition is a list of site indices for subsystem A; the rest is B.
    Returns the von Neumann entropy S = -Tr(rho_A log rho_A)."""
    dim = 2 ** n_sites
    # reshape psi into a tensor
    psi_tensor = psi.reshape([2] * n_sites)
    # trace out subsystem B
    axes_A = tuple(partition)
    axes_B = tuple(i for i in range(n_sites) if i not in partition)
    # compute reduced density matrix
    rho_A = np.tensordot(psi_tensor, psi_tensor.conj(), axes=(axes_B, axes_B))
    # eigenvalues
    eigvals = np.linalg.eigvalsh(rho_A)
    eigvals = eigvals[eigvals > 1e-10]  # filter zeros
    # von Neumann entropy
    S = -np.sum(eigvals * np.log(eigvals))
    return S


def tps_selection_test(n_sites=4):
    """Test if the dynamics select the thread/sheet factorization. Compute the
    entanglement entropy of the zero-point state in the thread/sheet basis vs
    alternative bases. The thread/sheet basis is: partition sites into threads
    (odd sites) and sheets (even sites). Alternative bases: random partitions.
    Returns rows of (basis, entropy)."""
    H = construct_hamiltonian(n_sites)
    psi = zero_point_state(n_sites)
    # evolve under H for a short time
    t = 0.1
    psi_evolved = expm(-1j * H * t) @ psi
    # thread/sheet basis: odd sites vs even sites
    thread_sites = [i for i in range(n_sites) if i % 2 == 1]
    sheet_sites = [i for i in range(n_sites) if i % 2 == 0]
    S_thread_sheet = entanglement_entropy(psi_evolved, n_sites, thread_sites)
    # alternative bases: random partitions
    rng = np.random.default_rng(42)
    S_alt = []
    for _ in range(10):
        partition = rng.choice(n_sites, size=n_sites // 2, replace=False).tolist()
        S = entanglement_entropy(psi_evolved, n_sites, partition)
        S_alt.append(S)
    rows = [{"basis": "thread/sheet", "entropy": S_thread_sheet}]
    for i, S in enumerate(S_alt):
        rows.append({"basis": f"random_{i}", "entropy": S})
    return rows


# ───────────────────────────────────────────────────────────────────────────────
# H67b - K-DUAL SCAN
# ───────────────────────────────────────────────────────────────────────────────

def photon_strand_hamiltonian():
    """Construct the Hamiltonian for the photon's dual-strand geometry (Phase 55).
    Two strands E_+, E_- with rung coupling across the zero point. Model as a
    2-site system with coupling J_rung. Returns the Hamiltonian matrix."""
    # 2 sites: strand A and strand B
    # rung coupling: sigma_x on A, sigma_x on B
    H_rung = np.kron(np.array([[0, 1], [1, 0]]), np.array([[0, 1], [1, 0]]))
    # on-site terms: sigma_z on each strand
    H_A = np.kron(np.array([[1, 0], [0, -1]]), np.eye(2))
    H_B = np.kron(np.eye(2), np.array([[1, 0], [0, -1]]))
    H = H_rung + 0.1 * H_A + 0.1 * H_B
    return H


def kdual_scan(n_samples=100, tol=1e-6):
    """Scan for K-dual factorizations of the photon's dual-strand decomposition.
    Generate random unitary transformations U and check if U H U^dagger preserves
    K-locality (the Hamiltonian remains a sum of local terms). If yes, U defines
    a K-dual factorization. Returns rows of (unitary_id, klocality_preserved,
    factorization_changed)."""
    H = photon_strand_hamiltonian()
    dim = H.shape[0]
    rng = np.random.default_rng(42)
    rows = []
    for i in range(n_samples):
        # random unitary
        A = rng.standard_normal((dim, dim)) + 1j * rng.standard_normal((dim, dim))
        U, _ = np.linalg.qr(A)
        # transform Hamiltonian
        H_new = U @ H @ U.conj().T
        # check K-locality: the transformed Hamiltonian should be a sum of local terms
        # for a 2-site system, K-locality means H_new is a sum of single-site terms
        # compute the non-local part: H_new - (H_A' + H_B')
        # where H_A' = Tr_B(H_new) x I_B, H_B' = I_A x Tr_A(H_new)
        rho_A = np.trace(H_new.reshape(2, 2, 2, 2), axis1=1, axis2=3)
        rho_B = np.trace(H_new.reshape(2, 2, 2, 2), axis1=0, axis2=2)
        H_A_local = np.kron(rho_A / 2, np.eye(2))
        H_B_local = np.kron(np.eye(2), rho_B / 2)
        H_local = H_A_local + H_B_local
        H_nonlocal = H_new - H_local
        # K-locality preserved if the non-local part is small
        klocality_preserved = np.linalg.norm(H_nonlocal) < tol
        # factorization changed if U is not a product unitary
        # check if U is a product: U = U_A x U_B
        U_reshaped = U.reshape(2, 2, 2, 2)
        U_A = U_reshaped[:, 0, :, 0]
        U_B = U_reshaped[0, :, 0, :]
        U_product = np.kron(U_A, U_B)
        factorization_changed = np.linalg.norm(U - U_product) > tol
        rows.append({
            "unitary_id": i,
            "klocality_preserved": bool(klocality_preserved),
            "factorization_changed": bool(factorization_changed),
        })
    return rows


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ---- H67a: TPS selection test -------------------------------------------
    print("=== H67a: TPS selection test ===")
    tps_rows = tps_selection_test(n_sites=4)
    S_thread_sheet = tps_rows[0]["entropy"]
    S_alt_mean = np.mean([r["entropy"] for r in tps_rows[1:]])
    margin = (S_alt_mean - S_thread_sheet) / S_alt_mean * 100
    print(f"  thread/sheet entropy: {S_thread_sheet:.4f}")
    print(f"  random basis mean: {S_alt_mean:.4f}")
    print(f"  margin: {margin:.1f}%")
    print(f"  verdict: {'PASS' if margin > 10 else 'FAIL'} (threshold 10%)")
    with open(os.path.join(OUT_DIR, "tps_selection.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(tps_rows[0].keys()))
        w.writeheader()
        w.writerows(tps_rows)

    # ---- H67b: K-dual scan --------------------------------------------------
    print("\n=== H67b: K-dual scan ===")
    kd_rows = kdual_scan(n_samples=100, tol=1e-6)
    n_kdual = sum(1 for r in kd_rows if r["klocality_preserved"] and r["factorization_changed"])
    print(f"  scanned 100 random unitaries")
    print(f"  K-dual factorizations found: {n_kdual}")
    print(f"  verdict: {'PASS (no K-duals)' if n_kdual == 0 else 'FAIL (K-duals exist)'}")
    with open(os.path.join(OUT_DIR, "kdual_scan.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(kd_rows[0].keys()))
        w.writeheader()
        w.writerows(kd_rows)

    # ---- H67c: verdict ------------------------------------------------------
    print("\n=== H67c: verdict ===")
    h67a_pass = margin > 10
    h67b_pass = n_kdual == 0
    if h67a_pass and h67b_pass:
        print("  BOTH PASS: the runtime's implicit ontology is selected by its dynamics")
        print("  'particles are knots' is theorem-adjacent (Cotler et al. Theorem 3.9)")
    else:
        print("  AT LEAST ONE FAIL: the mismatch localizes the gap")
        if not h67a_pass:
            print("    H67a failed: the dynamics do not select the thread/sheet factorization")
        if not h67b_pass:
            print("    H67b failed: K-dual factorizations exist")

    # ---- figure -------------------------------------------------------------
    make_figure(tps_rows, kd_rows, margin, n_kdual)
    print(f"\nWrote {OUT_DIR}")


def make_figure(tps_rows, kd_rows, margin, n_kdual):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # A: TPS selection
    ax = axes[0]
    bases = [r["basis"] for r in tps_rows]
    entropies = [r["entropy"] for r in tps_rows]
    colors = ["seagreen" if b == "thread/sheet" else "steelblue" for b in bases]
    ax.bar(bases, entropies, color=colors)
    ax.set_ylabel("entanglement entropy")
    ax.set_title(f"A. TPS selection test (margin {margin:.1f}%)")
    ax.tick_params(axis='x', rotation=45)

    # B: verdict
    ax = axes[1]
    ax.axis("off")
    lines = [
        "QUANTUM MEREOLOGY VERDICT",
        "",
        f"H67a (TPS selection): {'PASS' if margin > 10 else 'FAIL'}",
        f"  thread/sheet entropy: {tps_rows[0]['entropy']:.4f}",
        f"  margin: {margin:.1f}%",
        "",
        f"H67b (K-dual scan): {'PASS' if n_kdual == 0 else 'FAIL'}",
        f"  K-duals found: {n_kdual}/100",
        "",
        "verdict: " + ("theorem-adjacent" if margin > 10 and n_kdual == 0 else "gap localized"),
    ]
    ax.text(0.5, 0.5, "\n".join(lines), ha="center", va="center", fontsize=10,
            bbox=dict(boxstyle="round", fc="palegreen" if margin > 10 and n_kdual == 0 else "lightyellow"))
    ax.set_title("B. Quantum mereology verdict (H67c)")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "quantum_mereology.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
