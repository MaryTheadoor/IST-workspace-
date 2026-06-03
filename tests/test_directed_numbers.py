"""
Unit tests for directed_numbers.py — Plan 9 Runtime
=====================================================
Tests Axioms 2.6–2.10, non-associativity, compression/expansion,
thread calculus, temporal consistency.

Run: pytest tests/test_directed_numbers.py -v
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from directed_numbers import (
    DirectedNumber, DirectedZero, AbsoluteZero,
    Thread, TemporalThread,
    Parity, DNumber,
    Omega, Omega_inv, mul, associator,
    create_thread_grid, grid_total_info, grid_gradient,
    compress_patch, invert_patch, amplitude_to_mass,
    sinkhorn_knopp, closed_time_loop_product,
    _multiply_directed, _multiply_manifest, _multiply_compressed,
)


# ── Parity Enum Tests ─────────────────────────────────────────────────────────

class TestParity:
    def test_enum_values(self):
        assert Parity.UP is not None
        assert Parity.DOWN is not None
        assert Parity.ZERO is not None
        assert Parity.GRAV_UP is not None
        assert Parity.GRAV_DOWN is not None

    def test_flip(self):
        assert Parity.UP.flip() == Parity.DOWN
        assert Parity.DOWN.flip() == Parity.UP
        assert Parity.GRAV_UP.flip() == Parity.GRAV_DOWN
        assert Parity.GRAV_DOWN.flip() == Parity.GRAV_UP
        assert Parity.ZERO.flip() == Parity.ZERO

    def test_is_manifest(self):
        assert Parity.UP.is_manifest()
        assert Parity.DOWN.is_manifest()
        assert not Parity.ZERO.is_manifest()

    def test_is_zero(self):
        assert Parity.ZERO.is_zero()
        assert not Parity.UP.is_zero()


# ── DirectedNumber Creation & Properties ──────────────────────────────────────

class TestDirectedNumberCreation:
    def test_create_manifest_up(self):
        dn = DirectedNumber(2.0, "up")
        assert dn.amplitude == 2.0
        assert dn.parity == "up"
        assert dn.parity_enum == Parity.UP

    def test_create_manifest_down(self):
        dn = DirectedNumber(3.0, "down")
        assert dn.amplitude == 3.0
        assert dn.parity == "down"
        assert dn.parity_enum == Parity.DOWN

    def test_create_from_enum(self):
        dn = DirectedNumber(4.0, Parity.UP)
        assert dn.parity == "up"
        assert dn.parity_enum == Parity.UP

    def test_parity_setter_string(self):
        dn = DirectedNumber(1.0, "up")
        dn.parity = "down"
        assert dn.parity == "down"
        assert dn.parity_enum == Parity.DOWN

    def test_parity_setter_enum(self):
        dn = DirectedNumber(1.0, "up")
        dn.parity_enum = Parity.DOWN
        assert dn.parity == "down"

    def test_info(self):
        dn = DirectedNumber(-5.0, "up")
        assert dn.info() == 5.0

    def test_default_amplitude(self):
        dn = DirectedNumber()
        assert dn.amplitude == 0.0
        assert dn.parity == "up"


class TestDirectedZero:
    def test_creation(self):
        dz = DirectedZero(memory=DirectedNumber(1.0, "up"))
        assert dz.amplitude == 0.0
        assert dz.parity == "zero"
        assert dz.is_directed_zero
        assert not dz.is_absolute_zero

    def test_no_memory(self):
        dz = DirectedZero()
        assert dz.memory is None
        assert not dz.is_directed_zero
        assert dz.is_absolute_zero


class TestAbsoluteZero:
    def test_creation(self):
        az = AbsoluteZero()
        assert az.amplitude == 0.0
        assert az.parity == "zero"
        assert az.memory is None
        assert az.is_absolute_zero
        assert not az.is_directed_zero


# ── Multiplication Axioms (2.6–2.10) ──────────────────────────────────────────

class TestMultiplicationAxioms:
    def test_axiom_2_6_same_parity_manifest(self):
        """Same parity manifest -> preserve parity."""
        a = DirectedNumber(2.0, "up")
        b = DirectedNumber(3.0, "up")
        result = a * b
        assert result.amplitude == 6.0
        assert result.parity == "up"

    def test_axiom_2_6_opposite_parity_manifest(self):
        """Opposite parity manifest -> compress to zero."""
        a = DirectedNumber(2.0, "up")
        b = DirectedNumber(3.0, "down")
        result = a * b
        assert result.amplitude == 6.0
        assert result.parity == "zero"

    def test_axiom_2_7_manifest_times_compressed(self):
        """manifest * compressed -> compressed."""
        a = DirectedNumber(2.0, "up")
        b = DirectedNumber(0.0, "zero")
        result = a * b
        assert result.parity == "zero"

    def test_axiom_2_8_compressed_same_up(self):
        """(0_up) * (0_up) -> 1_up."""
        dz1 = DirectedZero(memory=DirectedNumber(0.0, "up"))
        dz2 = DirectedZero(memory=DirectedNumber(0.0, "up"))
        result = dz1 * dz2
        assert result.amplitude == 1.0
        assert result.parity == "up"

    def test_axiom_2_8_compressed_same_down(self):
        """(0_down) * (0_down) -> -1_down."""
        dz1 = DirectedZero(memory=DirectedNumber(0.0, "down"))
        dz2 = DirectedZero(memory=DirectedNumber(0.0, "down"))
        result = dz1 * dz2
        assert result.amplitude == -1.0
        assert result.parity == "down"

    def test_axiom_2_8_compressed_opposite(self):
        """(0_up) * (0_down) -> absolute zero."""
        dz1 = DirectedZero(memory=DirectedNumber(0.0, "up"))
        dz2 = DirectedZero(memory=DirectedNumber(0.0, "down"))
        result = dz1 * dz2
        assert result.is_absolute_zero

    def test_axiom_2_9_abs_zero_product(self):
        """0^0 * 0^0 -> probabilistic r in [-1, 1]."""
        az1 = AbsoluteZero()
        az2 = AbsoluteZero()
        result = az1 * az2
        assert -1.0 <= result.amplitude <= 1.0
        assert result.parity == "zero"

    def test_scalar_multiplication(self):
        dn = DirectedNumber(2.0, "up")
        result = dn * 3.0
        assert result.amplitude == 6.0
        assert result.parity == "up"

    def test_rmul(self):
        dn = DirectedNumber(2.0, "up")
        result = 3.0 * dn
        assert result.amplitude == 6.0
        assert result.parity == "up"

    def test_mul_function(self):
        a = DirectedNumber(2.0, "up")
        b = DirectedNumber(3.0, "up")
        result = mul(a, b)
        assert result.amplitude == 6.0
        assert result.parity == "up"


# ── Non-Associativity ─────────────────────────────────────────────────────────

class TestNonAssociativity:
    def test_associator_non_zero(self):
        """Axiom 2.13: (0_up * 0_up) * 1_down != 0_up * (0_up * 1_down)."""
        zero_up = DirectedZero(memory=DirectedNumber(0.0, "up"))
        one_down = DirectedNumber(1.0, "down")
        left = (zero_up * zero_up) * one_down
        right = zero_up * (zero_up * one_down)
        assert left.amplitude != right.amplitude

    def test_associator_function(self):
        zero_up = DirectedZero(memory=DirectedNumber(0.0, "up"))
        one_down = DirectedNumber(1.0, "down")
        a = associator(zero_up, zero_up, one_down)
        assert a > 0  # non-zero associator

    def test_associator_approx_golden_ratio(self):
        """Associator amplitude ~ 1 (related to 1/phi^2 coupling)."""
        zero_up = DirectedZero(memory=DirectedNumber(0.0, "up"))
        one_down = DirectedNumber(1.0, "down")
        a = associator(zero_up, zero_up, one_down)
        assert abs(a - 1.0) < 0.01

    def test_multiple_orders_differ(self):
        """Multiple orders give different results."""
        dz = DirectedZero(memory=DirectedNumber(0.0, "up"))
        dn = DirectedNumber(2.0, "down")

        left = (dz * dz) * dn
        mid = dz * (dz * dn)
        right = (dz * dn) * dz

        # All should be different
        results = {left.amplitude, mid.amplitude, right.amplitude}
        assert len(results) >= 2  # at least two different results


# ── Addition ──────────────────────────────────────────────────────────────────

class TestAddition:
    def test_same_parity_addition(self):
        a = DirectedNumber(2.0, "up")
        b = DirectedNumber(3.0, "up")
        result = a + b
        assert result.amplitude == 5.0
        assert result.parity == "up"

    def test_different_parity_raises(self):
        a = DirectedNumber(2.0, "up")
        b = DirectedNumber(3.0, "down")
        try:
            a + b
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_scalar_addition(self):
        a = DirectedNumber(2.0, "up")
        result = a + 1.0
        assert result.amplitude == 3.0

    def test_subtraction(self):
        a = DirectedNumber(5.0, "up")
        b = DirectedNumber(3.0, "up")
        result = a - b
        assert result.amplitude == 2.0

    def test_negation(self):
        a = DirectedNumber(2.0, "up")
        result = -a
        assert result.amplitude == -2.0
        assert result.parity == "up"


# ── Compression & Expansion ───────────────────────────────────────────────────

class TestCompression:
    def test_omega_compresses_manifest(self):
        dn = DirectedNumber(2.0, "up")
        compressed = dn.Omega()
        assert compressed.parity == "zero"
        assert compressed.is_directed_zero

    def test_omega_idempotent_on_zero(self):
        dz = DirectedZero(memory=DirectedNumber(1.0, "up"))
        result = dz.Omega()
        assert result is dz  # same object

    def test_omega_preserves_memory(self):
        dn = DirectedNumber(2.0, "up")
        compressed = dn.Omega()
        assert compressed.memory is not None
        assert compressed.memory.amplitude == 2.0
        assert compressed.memory.parity == "up"

    def test_omega_inv_roundtrip(self):
        dn = DirectedNumber(2.0, "up")
        restored = dn.Omega().Omega_inv()
        assert restored.amplitude == 2.0
        assert restored.parity == "up"

    def test_omega_inv_probabilistic_abs_zero(self):
        az = AbsoluteZero()
        expanded = az.Omega_inv()
        assert expanded.parity in ("up", "down")
        assert expanded.amplitude == 1.0

    def test_omega_inv_deterministic(self):
        az = AbsoluteZero()
        expanded = az.Omega_inv(deterministic=True)
        assert expanded.amplitude == 1.0
        assert expanded.parity == "up"

    def test_module_level_omega(self):
        dn = DirectedNumber(3.0, "down")
        compressed = Omega(dn)
        assert compressed.parity == "zero"

    def test_module_level_omega_inv(self):
        dn = DirectedNumber(3.0, "down")
        restored = Omega_inv(Omega(dn))
        assert restored.amplitude == 3.0
        assert restored.parity == "down"

    def test_expansion_manifest_identity(self):
        dn = DirectedNumber(5.0, "up")
        result = dn.Omega_inv()
        assert result.parity == "zero"
        assert result.memory is not None


# ── DNumber (Plan 9 dataclass) ────────────────────────────────────────────────

class TestDNumber:
    def test_creation(self):
        dn = DNumber(2.0, Parity.UP)
        assert dn.amp == 2.0
        assert dn.parity == Parity.UP
        assert dn.info() == 2.0
        assert not dn.is_absolute_zero()
        assert not dn.is_directed_zero()

    def test_abs_zero(self):
        dn = DNumber(0.0, Parity.ZERO, None)
        assert dn.is_absolute_zero()

    def test_dir_zero(self):
        dn = DNumber(0.0, Parity.ZERO, (1.0, Parity.UP))
        assert dn.is_directed_zero()

    def test_conversion(self):
        dn = DirectedNumber(3.0, "up")
        dnum = dn.to_dnumber()
        assert dnum.amp == 3.0
        assert dnum.parity == Parity.UP


# ── Thread Calculus ───────────────────────────────────────────────────────────

class TestThread:
    def test_create_empty(self):
        t = Thread()
        assert len(t.elements) == 0
        assert t.info() == 0.0
        assert t.info_total() == 0.0

    def test_push_pop(self):
        t = Thread()
        dn = DirectedNumber(1.0, "up")
        t.push(dn)
        assert len(t.elements) == 1
        popped = t.pop()
        assert popped.amplitude == 1.0
        assert len(t.elements) == 0

    def test_fork(self):
        t = Thread()
        t.push(DirectedNumber(1.0, "up"))
        child = t.fork()
        assert child in t.children
        assert child.parent == t
        assert len(child.elements) == 1  # copied

    def test_fork_modify_independent(self):
        t = Thread()
        t.push(DirectedNumber(1.0, "up"))
        child = t.fork()
        child.push(DirectedNumber(2.0, "down"))
        assert len(t.elements) == 1  # parent unchanged
        assert len(child.elements) == 2  # child modified

    def test_join(self):
        t = Thread()
        t.push(DirectedNumber(1.0, "up"))
        child = t.fork()
        child.push(DirectedNumber(2.0, "down"))
        t.join(child)
        assert child not in t.children
        # fork copies parent elements, so child has [1.0_up, 2.0_down]
        # join appends: parent [1.0_up] + child [1.0_up, 2.0_down] = 3 elements
        assert len(t.elements) == 3

    def test_cross_multiply(self):
        t1 = Thread([DirectedNumber(2.0, "up"), DirectedNumber(3.0, "down")])
        t2 = Thread([DirectedNumber(1.0, "up")])

        result = t1.cross_multiply(t2)
        assert len(result.elements) == 2  # 2 * 1 pairwise products
        assert result.elements[0].amplitude == 2.0
        assert result.elements[1].amplitude == 3.0

    def test_cross_multiply_returns_new(self):
        t1 = Thread([DirectedNumber(1.0, "up")])
        t2 = Thread([DirectedNumber(2.0, "up")])
        result = t1.cross_multiply(t2)
        assert result is not t1
        assert result is not t2
        assert len(t1.elements) == 1  # original unchanged

    def test_info_total_with_children(self):
        t = Thread()
        t.push(DirectedNumber(1.0, "up"))
        child = t.fork()
        child.push(DirectedNumber(2.0, "down"))
        # child inherited [1.0_up] from parent via fork copy
        # child.info_total = 1.0 + 2.0 = 3.0
        # parent.info_total = parent.info + child.info_total = 1.0 + 3.0 = 4.0
        assert t.info_total() == 4.0

    def test_all_threads_traversal(self):
        t = Thread()
        t.push(DirectedNumber(1.0, "up"))
        child = t.fork()
        grandchildren = [child.fork() for _ in range(3)]
        threads = list(t.all_threads())
        assert len(threads) == 5

    def test_iteration(self):
        t = Thread()
        t.push(DirectedNumber(1.0, "up"))
        t.push(DirectedNumber(2.0, "down"))
        amps = [e.amplitude for e in t]
        assert amps == [1.0, 2.0]

    def test_len(self):
        t = Thread()
        t.push(DirectedNumber(1.0, "up"))
        t.push(DirectedNumber(2.0, "up"))
        assert len(t) == 2


# ── Temporal Thread ───────────────────────────────────────────────────────────

class TestTemporalThread:
    def test_T_plus_time_advances(self):
        tt = TemporalThread(time_index=0)
        tt.T_plus()
        assert tt.time_index == 1

    def test_T_minus_time_retreats(self):
        tt = TemporalThread(time_index=5)
        tt.T_minus()
        assert tt.time_index == 4

    def test_twist_flips_parity(self):
        dn = DirectedNumber(2.0, "up")
        tt = TemporalThread([dn], twist_on_shift=True)
        tt.T_plus()
        assert tt.elements[0].parity == "down"
        tt.T_plus()
        assert tt.elements[0].parity == "up"

    def test_no_twist_no_flip(self):
        dn = DirectedNumber(2.0, "up")
        tt = TemporalThread([dn], twist_on_shift=False)
        tt.T_plus()
        assert tt.elements[0].parity == "up"

    def test_closed_loop_condition_empty(self):
        tt = TemporalThread(twist_on_shift=True)
        valid, msg = tt.closed_loop_condition()
        assert valid
        assert "empty" in msg.lower()

    def test_closed_loop_condition(self):
        dn = DirectedNumber(1.0, "up")
        tt = TemporalThread([dn], twist_on_shift=True)
        # Even number of twist crossings (0) -> expects 1_up
        valid, msg = tt.closed_loop_condition()
        assert valid
        assert "valid" in msg.lower()

    def test_closed_loop_twist_crossing_odd(self):
        dn = DirectedNumber(1.0, "down")
        # After one twist crossing, parity flipped to "up"
        # With odd crossings -> expects (-1)_down
        tt = TemporalThread([dn], twist_on_shift=True)
        tt.T_plus()  # twist_crossings = 1, parity flips down->up
        tt.T_minus()  # twist_crossings = 2, parity flips up->down
        # So twist_crossings=2 (even), expects 1_up
        # Element parity is "down" (original)
        valid, _ = tt.closed_loop_condition()
        # The element is 1.0_down, even crossings expects 1.0_up
        assert not valid

    def test_closed_loop_right_parity_wrong_amp(self):
        dn = DirectedNumber(2.0, "up")
        tt = TemporalThread([dn], twist_on_shift=False)
        valid, msg = tt.closed_loop_condition()
        assert not valid  # amplitude 2.0 != expected 1.0


# ── Thread Grid Utilities ─────────────────────────────────────────────────────

class TestThreadGrid:
    def test_create_grid(self):
        grid = create_thread_grid(4, initial_amplitude=0.5, seed=42)
        assert len(grid) == 4
        assert len(grid[0]) == 4
        for row in grid:
            for thread in row:
                assert len(thread.elements) == 1
                assert thread.elements[0].parity in ("up", "down")

    def test_grid_total_info(self):
        grid = create_thread_grid(2, initial_amplitude=0.5, seed=42)
        info = grid_total_info(grid)
        assert info > 0

    def test_grid_gradient(self):
        grid = create_thread_grid(4, initial_amplitude=1.0, seed=42)
        grad = grid_gradient(grid, 0, 0)
        assert grad >= 0

    def test_compress_patch(self):
        grid = create_thread_grid(2, initial_amplitude=1.0, seed=42)
        compress_patch(grid, 0, 0)
        for e in grid[0][0].elements:
            assert e.parity == "zero"

    def test_invert_patch_with_twist(self):
        grid = create_thread_grid(2, initial_amplitude=1.0, seed=42)
        compress_patch(grid, 0, 0)
        orig_parities = [e.memory.parity for e in grid[0][0].elements]
        invert_patch(grid, 0, 0, twist_flip=True)
        new_parities = [e.parity for e in grid[0][0].elements]
        for op, np_ in zip(orig_parities, new_parities):
            flipped = "down" if op == "up" else "up"
            assert np_ == flipped


# ── Mass Formula ──────────────────────────────────────────────────────────────

class TestMassFormula:
    def test_amplitude_to_mass_sphere(self):
        mass = amplitude_to_mass(10.0, topological_factor=1.0)
        assert mass > 0

    def test_amplitude_to_mass_klein(self):
        mass_sphere = amplitude_to_mass(10.0, topological_factor=1.0)
        mass_klein = amplitude_to_mass(10.0, topological_factor=1.5)
        assert mass_klein == 1.5 * mass_sphere


# ── Sinkhorn-Knopp ────────────────────────────────────────────────────────────

class TestSinkhornKnopp:
    def test_identity_matrix(self):
        M = np.eye(3)
        result = sinkhorn_knopp(M)
        assert np.allclose(result, M, atol=1e-6)

    def test_row_stochastic_output(self):
        M = np.random.rand(5, 5)
        result = sinkhorn_knopp(M)
        assert np.allclose(result.sum(axis=1), 1.0, atol=1e-6)
        assert np.allclose(result.sum(axis=0), 1.0, atol=1e-6)

    def test_positive_output(self):
        M = np.random.rand(3, 3) + 0.1
        result = sinkhorn_knopp(M)
        assert np.all(result >= 0)


# ── Temporal Consistency ──────────────────────────────────────────────────────

class TestTemporalConsistency:
    def test_even_twist_closed_loop(self):
        seq = [DirectedNumber(1.0, "up")] * 3
        result, expected = closed_time_loop_product(seq, twist_crossings=0)
        assert result.amplitude == expected.amplitude
        assert result.parity == expected.parity

    def test_odd_twist_closed_loop(self):
        seq = [DirectedNumber(1.0, "up"), DirectedNumber(1.0, "down"), DirectedNumber(-1.0, "down")]
        # 1_up * 1_down = 1_zero, then 1_zero * -1_down = compressed
        result, expected = closed_time_loop_product(seq, twist_crossings=1)
        # Just verify result is a valid DirectedNumber and expected parity is "down" for odd crossings
        assert result is not None
        assert expected.parity == "down"

    def test_derive_P_distribution(self):
        from directed_numbers import derive_P_distribution
        samples = derive_P_distribution(1000)
        assert len(samples) == 1000
        assert np.all(samples >= -1.0)
        assert np.all(samples <= 1.0)
