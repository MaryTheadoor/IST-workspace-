"""
Unit tests for phase25_temporal_holonomy.py -- IST Phase 25
============================================================
Temporal holonomy: the Compression Operator as parallel transport along the
temporal dimension of a non-orientable 4-topology. Tests the exact SU(2)
Wilson-loop machinery, the 720-degree double-cover, the static-phi
falsification (25a), the Riccati fold flow (25b), and the rig diagnostics.

Run: cd code && python -m pytest ../tests/test_phase25_temporal_holonomy.py -v
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_klein_laplacian import PHI
from phase25_temporal_holonomy import (
    I2, SX, SZ, TemporalHolonomy, SpinorOscillator,
    fibonacci_lattice, random_lattice, rational_lattice,
    tick_unitary, cycle_product, cayley_hamilton_expm,
    phase25a_static_falsification, riccati_fold_flow,
    golden_window_gap_ratio, GAP_RATIO_TARGET,
)

N_TEST = 48


def is_su2(U):
    """True if U is a 2x2 SU(2) element to tolerance."""
    return (np.allclose(U @ U.conj().T, I2, atol=1e-12)
            and abs(np.linalg.det(U) - 1.0) < 1e-12)


# ── Exact SU(2) propagator ────────────────────────────────────────────────────

class TestTickUnitary:
    def test_flat_tick_is_su2(self):
        for crossing in (True, False):
            assert is_su2(tick_unitary(1.0, crossing))

    def test_flat_axis_is_exact(self):
        # At rho = 1 (void baseline) the crossing tick is exactly -i SX
        U = tick_unitary(1.0, crossing=True)
        assert np.allclose(U, -1j * SX, atol=1e-12)
        U = tick_unitary(1.0, crossing=False)
        assert np.allclose(U, -1j * SZ, atol=1e-12)

    def test_tilt_breaks_exact_axis(self):
        U = tick_unitary(2.0, crossing=True)      # rho > 1 tilts the axis
        assert not np.allclose(U, -1j * SX, atol=1e-6)


class TestCayleyHamilton:
    def test_expm_is_unitary(self):
        # exp(-iH) for Hermitian H is U(2): unitary with |det| = 1
        # (det = e^{-2i a} for the scalar part a I). Verified against scipy.
        rng = np.random.default_rng(3)
        import scipy.linalg as sla
        for _ in range(5):
            H = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
            H = H + H.conj().T                     # Hermitian
            U = cayley_hamilton_expm(H)
            assert np.allclose(U @ U.conj().T, I2, atol=1e-12)
            assert abs(np.linalg.det(U)) - 1.0 < 1e-12
            assert np.allclose(U, sla.expm(-1j * H), atol=1e-12)


# ── 720-degree double-cover ───────────────────────────────────────────────────

class TestDoubleCover:
    def test_flat_limit_cycle_is_minus_I(self):
        # Zero fold density (gain=0) => every crossing tick is -i SX exactly,
        # so the 4-tick holonomy is exactly -I (the fermionic sign).
        sub = TemporalHolonomy(fibonacci_lattice(N_TEST), gain=0.0, sigma=0.15)
        M = sub._forward_cycle_matrix()
        dev = np.max(np.abs(np.trace(M, axis1=1, axis2=2) + 2.0))
        assert dev < 1e-12

    def test_tick_2_flips_tick_4_restores(self):
        # One oscillator: chirality flips at the 2-tick half-cycle and is
        # restored at the 4-tick cycle (phase23a verification, 720 deg).
        osc = SpinorOscillator(0.3, 0.7, 0.5)
        sub = TemporalHolonomy([osc], gain=0.0, sigma=0.15)
        c0 = osc.chirality
        sub._plonk_tick(); sub._plonk_tick()
        assert osc.chirality == -c0               # half-cycle flip
        sub._plonk_tick(); sub._plonk_tick()
        assert osc.chirality == c0                # full-cycle restore

    def test_cycle_product_matches_frozen_propagation(self):
        # cycle_product(rho) is the ordered U_3 U_2 U_1 U_0 built from a
        # FROZEN connection snapshot. Propagating with the SAME fixed rho
        # (overriding the evolving fold density) must give the same matrix.
        sub = TemporalHolonomy(fibonacci_lattice(N_TEST), gain=0.5, sigma=0.15)
        rho = sub._fold_density()
        M_f = cycle_product(rho, orientation_start=0, reverse=False)
        M_manual = np.array([I2.copy() for _ in range(sub.N)])
        for k in range(4):
            crossing = (k + 1) % 4 in (2, 0)
            U = np.array([tick_unitary(r, crossing) for r in rho])
            M_manual = np.einsum("nij,njk->nik", U, M_manual)
        assert np.allclose(M_f, M_manual, atol=1e-12)


# ── Unitarity and time reversal ───────────────────────────────────────────────

class TestHolonomyProperties:
    def test_unitarity_to_1e_12(self):
        sub = TemporalHolonomy(fibonacci_lattice(N_TEST), gain=0.8, sigma=0.15)
        assert sub.unitarity_error() < 1e-12

    def test_time_reversal_is_inverse(self):
        sub = TemporalHolonomy(fibonacci_lattice(N_TEST), gain=0.8, sigma=0.15)
        assert sub.time_reversal_check() < 1e-12

    def test_wilson_eigenvalues_on_unit_circle(self):
        sub = TemporalHolonomy(fibonacci_lattice(N_TEST), gain=0.8, sigma=0.15)
        evals, _, _ = sub.wilson_spectrum(n_cycles=2)
        assert np.allclose(np.abs(evals), 1.0, atol=1e-12)

    def test_flat_limit_has_trivial_winding(self):
        # Gain=0 => every oscillator returns exactly -I => Im(lambda)=0.
        sub = TemporalHolonomy(fibonacci_lattice(N_TEST), gain=0.0, sigma=0.15)
        kfrac = sub.knot_fraction(n_cycles=2)
        assert kfrac == 0.0

    def test_coupled_substrate_has_nontrivial_winding(self):
        sub = TemporalHolonomy(fibonacci_lattice(N_TEST), gain=0.8, sigma=0.15)
        sub.wilson_spectrum(n_cycles=3)
        kfrac = sub.knot_fraction(n_cycles=1)
        assert 0.0 < kfrac <= 1.0


# ── Phase 25a: static-phi falsification ───────────────────────────────────────

class TestStaticFalsification:
    def test_d_eff_is_about_2_not_phi(self):
        a = phase25a_static_falsification()
        assert abs(a["d_eff_static"] - 2.0) < 0.2
        assert a["distance_from_phi"] > 0.3

    def test_gamma_min_matches_analytic_gap(self):
        a = phase25a_static_falsification()
        assert a["gamma_match"] < 1e-9


# ── Phase 25b: Riccati fold flow ─────────────────────────────────────────────

class TestRiccatiFlow:
    def test_flow_reaches_phi_fixed_point(self):
        # D_eff(f) descends through phi, so the Riccati flow must converge to
        # the fixed point f* where D_eff(f*) = phi. The exact f* depends on
        # the D_eff estimator: the spectral-dimension fit here crosses phi at
        # f ~ 2.6 (Phase 4's f ~ 4.2 came from a different log-slope D_eff).
        from phase25_temporal_holonomy import d_eff_vs_fold
        dscan = d_eff_vs_fold()
        fs, ds, steps = riccati_fold_flow(lambda f: np.interp(
            f, [x[0] for x in dscan], [x[1] for x in dscan]), f0=1.0)
        assert steps is not None
        assert abs(ds[-1] - PHI) < 1e-2
        assert 1.5 < fs[-1] < 4.0


# ── Golden filter robustness (lattice comparison) ────────────────────────────

class TestLatticeRobustness:
    def test_fibonacci_preserves_winding_better_than_rational(self):
        # The rational lattice collapses the temporal winding toward the
        # trivial fermionic -I (deviation from flat is small); the Fibonacci
        # lattice keeps the winding alive (larger deviation from flat).
        devs = {}
        for name, build in [("fibonacci", fibonacci_lattice),
                            ("rational", rational_lattice)]:
            sub = TemporalHolonomy(build(N_TEST), gain=0.8, sigma=0.15)
            sub.wilson_spectrum(n_cycles=4)
            evals, _, _ = sub.wilson_spectrum(n_cycles=1)
            tr = 2 * evals[-1].real
            devs[name] = np.mean(np.abs(tr + 2.0))
        assert devs["fibonacci"] > devs["rational"]

    def test_trace_bound_holds_for_all_lattices(self):
        for build in (fibonacci_lattice, random_lattice, rational_lattice):
            sub = TemporalHolonomy(build(N_TEST), gain=0.8, sigma=0.15)
            sub.wilson_spectrum(n_cycles=2)
            evals, _, _ = sub.wilson_spectrum(n_cycles=1)
            tr = 2 * evals[-1].real
            assert np.all(np.abs(tr) <= 2.0 + 1e-12)


# ── Rig diagnostics ───────────────────────────────────────────────────────────

class TestRigDiagnostics:
    def test_gap_ratio_runs_and_reports_deviation(self):
        rows = golden_window_gap_ratio(n_cycles=5, n=80)
        assert len(rows) == 5
        # The v6.2 target 1/phi^2 is NOT realized by the eigenphase gaps; the
        # rig instruction requires reporting the deviation, not forcing it.
        for r in rows:
            assert abs(r["dev_from_target"]) > 1e-3


class TestLattices:
    def test_lattice_sizes(self):
        assert len(fibonacci_lattice(60)) == 60
        assert len(random_lattice(60)) == 60
        assert len(rational_lattice(60)) == 60

    def test_spinors_start_in_up_state(self):
        for o in fibonacci_lattice(10):
            assert np.allclose(o.spinor, [1.0, 0.0])
            assert o.orientation == 0
            assert o.chirality == 1
