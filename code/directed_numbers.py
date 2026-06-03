"""
IST Directed Number Algebra v0.9.0 — Plan 9 Runtime
=======================================================
Axioms 2.1–2.18: Directed numbers with parity, compression/expansion,
non-associative multiplication, thread calculus, and temporal consistency.

Enhancements from Plan 9:
  - Parity enum (UP, DOWN, ZERO, GRAV_UP, GRAV_DOWN)
  - DNumber dataclass for cleaner DirectedNumber representation
  - is_absolute_zero / is_directed_zero properties
  - Enhanced Thread with cross_multiply returning new Thread
  - TemporalThread with closed_loop_condition()
  - Omega / Omega_inv as module-level functions and methods
  - Backward-compatible with string-based parity

Reference: supplementary/directed_numbers_v0.8.1.pdf
"""

import numpy as np
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, Union, List, Tuple

# ───────────────────────────────────────────────────────────────────────────────
# Parity Enum (Plan 9)
# ───────────────────────────────────────────────────────────────────────────────

class Parity(Enum):
    UP = auto()
    DOWN = auto()
    ZERO = auto()
    GRAV_UP = auto()
    GRAV_DOWN = auto()

    def __repr__(self):
        return self.name

    def __str__(self):
        return {"UP": "up", "DOWN": "down", "ZERO": "zero",
                "GRAV_UP": "gravm_up", "GRAV_DOWN": "gravm_down"}.get(self.name, self.name)

    def flip(self):
        if self == Parity.UP:
            return Parity.DOWN
        if self == Parity.DOWN:
            return Parity.UP
        if self == Parity.GRAV_UP:
            return Parity.GRAV_DOWN
        if self == Parity.GRAV_DOWN:
            return Parity.GRAV_UP
        return self

    def is_manifest(self):
        return self in (Parity.UP, Parity.DOWN, Parity.GRAV_UP, Parity.GRAV_DOWN)

    def is_zero(self):
        return self == Parity.ZERO


# Backward-compatible: accept string or Parity enum
def _normalize_parity(p):
    if isinstance(p, Parity):
        return p
    if isinstance(p, str):
        return {"up": Parity.UP, "down": Parity.DOWN, "zero": Parity.ZERO,
                "gravm_up": Parity.GRAV_UP, "gravm_down": Parity.GRAV_DOWN}.get(p.lower(), Parity.ZERO)
    return Parity.ZERO


def _parity_to_str(p):
    """Convert Parity enum to legacy string for backward compatibility."""
    if isinstance(p, str):
        return p
    if p == Parity.UP:
        return "up"
    if p == Parity.DOWN:
        return "down"
    if p == Parity.ZERO:
        return "zero"
    if p == Parity.GRAV_UP:
        return "up"
    if p == Parity.GRAV_DOWN:
        return "down"
    return "zero"


# ───────────────────────────────────────────────────────────────────────────────
# DNumber (Plan 9 dataclass) — lightweight value type
# ───────────────────────────────────────────────────────────────────────────────

@dataclass
class DNumber:
    """Lightweight directed number value type (Plan 9)."""
    amp: float
    parity: Parity = Parity.ZERO
    memory: Optional[Tuple[float, Parity]] = None

    def info(self):
        return abs(self.amp)

    def is_absolute_zero(self):
        return self.parity == Parity.ZERO and self.memory is None and abs(self.amp) < 1e-15

    def is_directed_zero(self):
        return self.parity == Parity.ZERO and self.memory is not None

    def __repr__(self):
        p = self.parity.name
        if self.is_directed_zero():
            ma, mp = self.memory
            return f"DN({self.amp:.4f}_{p}, mem=({ma:.4f}_{mp.name}))"
        return f"DN({self.amp:.4f}_{p})"


# ───────────────────────────────────────────────────────────────────────────────
# DirectedNumber — Full class (backward-compatible with v0.8.1)
# ───────────────────────────────────────────────────────────────────────────────

class DirectedNumber:
    """IST directed number with amplitude, parity, and optional memory.

    Axiom 2.1: Elements are a_p where a ∈ ℝ, p ∈ {up, down, zero}.
    Axiom 2.2: 0_up / 0_down are directed zeros (memory); 0_zero is absolute zero.

    Plan 9: Supports both string and Parity enum for parity.
    """

    def __init__(self, amplitude=0.0, parity="up", memory=None):
        self.amplitude = float(amplitude)
        self._parity_enum = _normalize_parity(parity)
        self._memory = memory

    @property
    def parity(self):
        """Legacy string parity for backward compatibility."""
        return _parity_to_str(self._parity_enum)

    @parity.setter
    def parity(self, value):
        self._parity_enum = _normalize_parity(value)

    @property
    def parity_enum(self):
        """Plan 9: Parity enum accessor."""
        return self._parity_enum

    @parity_enum.setter
    def parity_enum(self, value):
        self._parity_enum = value if isinstance(value, Parity) else _normalize_parity(value)

    @property
    def memory(self):
        """Return the memory DirectedNumber (backward-compatible)."""
        return self._memory

    @memory.setter
    def memory(self, value):
        self._memory = value

    @property
    def is_absolute_zero(self):
        return self._parity_enum == Parity.ZERO and self._memory is None and abs(self.amplitude) < 1e-15

    @property
    def is_directed_zero(self):
        return self._parity_enum == Parity.ZERO and self._memory is not None

    def info(self):
        """Axiom 2.12: Information measure I(a_p) = |a|."""
        return abs(self.amplitude)

    def to_dnumber(self):
        """Convert to lightweight DNumber (Plan 9)."""
        mem = None
        if self._memory is not None:
            mem = (self._memory.amplitude, self._memory._parity_enum)
        return DNumber(self.amplitude, self._parity_enum, mem)

    def __repr__(self):
        p = self.parity
        if self.is_directed_zero and self._memory is not None:
            mp = self._memory.parity
            return f"D({self.amplitude:.4f}_{p}, mem=({self._memory.amplitude:.4f}_{mp}))"
        return f"D({self.amplitude:.4f}_{p})"

    def __eq__(self, other):
        if not isinstance(other, DirectedNumber):
            return False
        return (abs(self.amplitude - other.amplitude) < 1e-12 and
                self.parity == other.parity)

    # ── Arithmetic ────────────────────────────────────────────────────────────

    def __add__(self, other):
        """Axiom 2.3: Same-parity addition. Axiom 2.4: Mixed-parity not defined."""
        if isinstance(other, (int, float)):
            return DirectedNumber(self.amplitude + other, self.parity, self._memory)
        if self.parity == other.parity:
            mem = self._memory if self.parity == "zero" else None
            return DirectedNumber(self.amplitude + other.amplitude, self.parity, mem)
        raise ValueError(f"Cannot add different parities: {self.parity} + {other.parity} (Axiom 2.4)")

    def __mul__(self, other):
        """Non-associative multiplication (Axioms 2.6–2.10)."""
        if isinstance(other, (int, float)):
            return DirectedNumber(self.amplitude * other, self.parity, self._memory)
        return _multiply_directed(self, other)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return DirectedNumber(self.amplitude * other, self.parity, self._memory)
        return NotImplemented

    def __neg__(self):
        return DirectedNumber(-self.amplitude, self.parity, self._memory)

    def __sub__(self, other):
        return self + (-other)

    # ── Compression / Expansion Operators ─────────────────────────────────────

    def Omega(self):
        """Axiom 2.10: Compression — manifest → directed zero with memory."""
        pe = self._parity_enum
        if pe == Parity.ZERO:
            return self
        return DirectedZero(memory=DirectedNumber(self.amplitude, self.parity))

    def Omega_inv(self, deterministic=False):
        """Axiom 2.11: Expansion — directed zero → manifest (if memory exists)."""
        pe = self._parity_enum
        if pe == Parity.ZERO and self._memory is not None:
            return DirectedNumber(self._memory.amplitude, self._memory.parity)
        if pe == Parity.ZERO and self._memory is None:
            mem_amp = abs(self.amplitude) if abs(self.amplitude) > 1e-10 else 1.0
            if deterministic:
                return DirectedNumber(mem_amp, "up")
            parity = "up" if np.random.random() < 0.5 else "down"
            return DirectedNumber(mem_amp, parity)
        return DirectedZero(memory=DirectedNumber(self.amplitude, self.parity))


class DirectedZero(DirectedNumber):
    """Directed zero with topological memory (Axiom 2.2)."""
    def __init__(self, memory=None):
        super().__init__(amplitude=0.0, parity="zero", memory=memory)


class AbsoluteZero(DirectedNumber):
    """Absolute zero — pristine zero-point gate with no history (Axiom 2.2)."""
    def __init__(self):
        super().__init__(amplitude=0.0, parity="zero", memory=None)


# ───────────────────────────────────────────────────────────────────────────────
# Module-level Omega / Omega_inv (Plan 9 convenience functions)
# ───────────────────────────────────────────────────────────────────────────────

def Omega(x: DirectedNumber) -> DirectedNumber:
    """Compression operator: manifest → directed zero."""
    return x.Omega()


def Omega_inv(x: DirectedNumber, deterministic: bool = False) -> DirectedNumber:
    """Expansion operator: directed zero → manifest."""
    return x.Omega_inv(deterministic=deterministic)


# ───────────────────────────────────────────────────────────────────────────────
# Multiplication Axioms (2.6 – 2.10)
# ───────────────────────────────────────────────────────────────────────────────

def mul(a: DirectedNumber, b: DirectedNumber) -> DirectedNumber:
    """Explicit non-associative multiplication (Plan 9)."""
    return _multiply_directed(a, b)


def associator(x: DirectedNumber, y: DirectedNumber, z: DirectedNumber) -> float:
    """Compute associator [x, y, z] = (x*y)*z - x*(y*z) (Plan 9)."""
    left = (x * y) * z
    right = x * (y * z)
    return abs(left.amplitude - right.amplitude)


def _multiply_directed(a: DirectedNumber, b: DirectedNumber) -> DirectedNumber:
    ap, bp = a._parity_enum, b._parity_enum

    if ap.is_manifest() and bp.is_manifest():
        return _multiply_manifest(a, b)

    if ap == Parity.ZERO and bp == Parity.ZERO:
        return _multiply_compressed(a, b)

    # Axiom 2.7: manifest × compressed → compressed
    amp = abs(a.amplitude * b.amplitude)
    return DirectedNumber(amp, "zero")


def _multiply_manifest(a: DirectedNumber, b: DirectedNumber) -> DirectedNumber:
    """Axiom 2.6: Same parity → keep; opposite parity → compress."""
    if a._parity_enum == b._parity_enum:
        p = "up" if a._parity_enum in (Parity.UP, Parity.GRAV_UP) else "down"
        return DirectedNumber(a.amplitude * b.amplitude, p)
    return DirectedNumber(a.amplitude * b.amplitude, "zero")


def _multiply_compressed(a: DirectedNumber, b: DirectedNumber) -> DirectedNumber:
    """Axiom 2.8–2.9: Product of two compressed numbers."""
    am, bm = a._memory, b._memory

    if am is not None and bm is not None:
        amp = am._parity_enum
        bmp = bm._parity_enum
        if amp in (Parity.UP, Parity.GRAV_UP) and bmp in (Parity.UP, Parity.GRAV_UP):
            return DirectedNumber(1.0, "up")
        if amp in (Parity.DOWN, Parity.GRAV_DOWN) and bmp in (Parity.DOWN, Parity.GRAV_DOWN):
            return DirectedNumber(-1.0, "down")
        return AbsoluteZero()

    if (am is not None and bm is None) or (am is None and bm is not None):
        return AbsoluteZero()

    # Axiom 2.9: 0^0 * 0^0 → probabilistic r ∈ [-1, 1]
    r = _sample_abs_zero_product()
    return DirectedNumber(r, "zero")


def _sample_abs_zero_product() -> float:
    """Sample P(r) for absolute-zero products (Axiom 2.9).

    Plan 9 placeholder: uniform P(r) = 1/2 on [-1, 1].
    TODO: Replace with golden-ratio-based distribution after temporal consistency.
    """
    return (np.random.random() * 2) - 1.0


# ───────────────────────────────────────────────────────────────────────────────
# Thread Calculus (Section 3) — Enhanced for Plan 9
# ───────────────────────────────────────────────────────────────────────────────

class Thread:
    """Sequence of directed numbers forming an information thread.

    Plan 9 enhancements:
      - cross_multiply returns a new Thread (non-mutating)
      - info_total() sums over all threads (tree traversal)
      - push/pop stack semantics with index checking
      - __len__, __getitem__, __iter__ for iteration

    Section 3.4: fork/join balance ensures no dangling references.
    """

    def __init__(self, elements=None, parent=None, time_index=0):
        self.elements = list(elements) if elements else []
        self.parent = parent
        self.children = []
        self.time_index = time_index

    def info(self):
        """Sum of info() over direct elements only (backward-compatible)."""
        return sum(e.info() for e in self.elements)

    def info_total(self):
        """Plan 9: Sum of info() over all elements including children (tree traversal)."""
        return sum(e.info() for e in self.elements) + sum(c.info_total() for c in self.children)

    def total_info(self):
        """Backward-compatible alias for info_total."""
        return self.info_total()

    def push(self, element: DirectedNumber):
        """Push a directed number onto the thread stack."""
        self.elements.append(element)

    def pop(self) -> Optional[DirectedNumber]:
        """Pop a directed number from the thread stack."""
        return self.elements.pop() if self.elements else None

    def fork(self):
        """Create a new child thread with a copy of current elements."""
        child = Thread(elements=list(self.elements), parent=self, time_index=self.time_index)
        self.children.append(child)
        return child

    def join(self, child: 'Thread'):
        """Merge a child thread back: absorb its elements and children."""
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            self.elements.extend(child.elements)
            self.children.extend(child.children)
            for gc in child.children:
                gc.parent = self

    def cross_multiply(self, other: 'Thread') -> 'Thread':
        """Plan 9: Pairwise cross-multiplication — returns a NEW Thread."""
        result = Thread()
        for a in self.elements:
            for b in other.elements:
                result.push(a * b)
        return result

    def all_threads(self):
        """Generator yielding self and all descendant threads."""
        yield self
        for c in self.children:
            yield from c.all_threads()

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, idx):
        return self.elements[idx]

    def __iter__(self):
        return iter(self.elements)

    def __repr__(self):
        return (f"Thread(t={self.time_index}, n={len(self.elements)}, "
                f"children={len(self.children)}, I={self.info():.2f})")


class TemporalThread(Thread):
    """Thread with time-indexed directed numbers and temporal shift operators.

    Axiom 2.15–2.18: Temporal directed numbers carry time coordinate.
    T_plus / T_minus shift time with optional parity flip across twists.

    Plan 9 enhancements:
      - closed_loop_condition() — checks Axiom 2.18
      - twist counter for parity tracking
    """

    def __init__(self, elements=None, parent=None, time_index=0, twist_on_shift=False):
        super().__init__(elements, parent, time_index)
        self.twist_on_shift = twist_on_shift
        self.twist_crossings = 0

    def T_plus(self):
        """Forward temporal shift (Axiom 2.16). Flips parity if twisted."""
        self.time_index += 1
        if self.twist_on_shift:
            self.twist_crossings += 1
            for e in self.elements:
                if e.parity == "up":
                    e._parity_enum = Parity.DOWN
                elif e.parity == "down":
                    e._parity_enum = Parity.UP

    def T_minus(self):
        """Backward temporal shift (Axiom 2.16). Flips parity if twisted."""
        self.time_index -= 1
        if self.twist_on_shift:
            self.twist_crossings += 1
            for e in self.elements:
                if e.parity == "up":
                    e._parity_enum = Parity.DOWN
                elif e.parity == "down":
                    e._parity_enum = Parity.UP

    def closed_loop_condition(self) -> Tuple[bool, str]:
        """Plan 9: Check Axiom 2.18 — closed time loop constraint.

        After a complete cycle (returning to original time), the product
        of all elements must equal 1_up (even twist crossings) or (-1)_down
        (odd twist crossings).

        Returns:
            (is_valid: bool, message: str)
        """
        if len(self.elements) == 0:
            return True, "empty thread"

        result = self.elements[0]
        for x in self.elements[1:]:
            result = result * x

        expected_parity = "down" if self.twist_crossings % 2 != 0 else "up"
        expected_amp = -1.0 if self.twist_crossings % 2 != 0 else 1.0

        parity_ok = result.parity == expected_parity
        amp_ok = abs(result.amplitude - expected_amp) < 1e-10

        if parity_ok and amp_ok:
            return True, f"closed loop valid: result={result} matches expected parity={expected_parity}"
        return False, (f"closed loop violation: result={result}, "
                       f"expected parity={expected_parity}, "
                       f"twist_crossings={self.twist_crossings}")

    def __repr__(self):
        return (f"TemporalThread(t={self.time_index}, n={len(self.elements)}, "
                f"children={len(self.children)}, twisted={self.twist_on_shift}, "
                f"twist_crossings={self.twist_crossings}, I={self.info():.2f})")


# ───────────────────────────────────────────────────────────────────────────────
# Sinkhorn-Knopp Projection (Section 4)
# ───────────────────────────────────────────────────────────────────────────────

def sinkhorn_knopp(matrix, iterations: int = 100, tol: float = 1e-9) -> np.ndarray:
    """Project onto doubly-stochastic matrices (Birkhoff polytope).

    Ensures information conservation for multi-component transformations.
    """
    M = np.array(matrix, dtype=float)
    M = np.maximum(M, 1e-120)
    for _ in range(iterations):
        row_sums = M.sum(axis=1, keepdims=True)
        M = M / row_sums
        col_sums = M.sum(axis=0, keepdims=True)
        M = M / col_sums
        err = np.max(np.abs(row_sums - 1.0)) + np.max(np.abs(col_sums - 1.0))
        if err < tol:
            break
    return M


# ───────────────────────────────────────────────────────────────────────────────
# Temporal Consistency (Axiom 2.17-2.18)
# ───────────────────────────────────────────────────────────────────────────────

def closed_time_loop_product(sequence: List[DirectedNumber], twist_crossings: int = 0):
    """Compute product of directed numbers along a closed time loop.

    Axiom 2.17: Product must equal 1_up (even parity) or (-1)_down (odd parity).
    """
    result = sequence[0]
    for x in sequence[1:]:
        result = result * x
    expected = DirectedNumber(1.0, "down") if twist_crossings % 2 != 0 else DirectedNumber(1.0, "up")
    return result, expected


def derive_P_distribution(num_samples: int = 100000) -> np.ndarray:
    """Derive P(r) distribution from temporal consistency requirements.

    Samples absolute-zero products and measures the empirical distribution
    of outcomes for 0^0 * 0^0.
    """
    samples = np.array([(AbsoluteZero() * AbsoluteZero()).amplitude for _ in range(num_samples)])
    return samples


# ───────────────────────────────────────────────────────────────────────────────
# Utility: Thread Grid for Horizon Patches (backward-compatible)
# ───────────────────────────────────────────────────────────────────────────────

def create_thread_grid(n_patches: int, initial_amplitude: float = 0.5,
                       seed: Optional[int] = None) -> List[List[Thread]]:
    """Create an n×n grid of Thread objects for horizon patches."""
    if seed is not None:
        np.random.seed(seed)
    grid = []
    for i in range(n_patches):
        row = []
        for j in range(n_patches):
            thread = Thread()
            parity = np.random.choice(["up", "down"])
            amp = abs(np.random.normal(initial_amplitude, 0.1 * initial_amplitude))
            thread.push(DirectedNumber(amp, parity))
            row.append(thread)
        grid.append(row)
    return grid


def grid_total_info(grid: List[List[Thread]]) -> float:
    """Sum total info over all grid patches."""
    return sum(grid[i][j].info() for i in range(len(grid)) for j in range(len(grid[0])))


def grid_gradient(grid: List[List[Thread]], i: int, j: int) -> float:
    """Compute local information gradient at patch (i, j)."""
    n_i, n_j = len(grid), len(grid[0])
    info_ij = grid[i][j].info()
    neighbors = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = (i + di) % n_i, (j + dj) % n_j
        neighbors.append(grid[ni][nj].info())
    return (sum((info_ij - n) ** 2 for n in neighbors) / len(neighbors)) ** 0.5


def compress_patch(grid: List[List[Thread]], i: int, j: int):
    """Apply Omega() to all directed numbers in a patch (frozen knot formation)."""
    thread = grid[i][j]
    thread.elements = [e.Omega() for e in thread.elements]


def invert_patch(grid: List[List[Thread]], i: int, j: int, twist_flip: bool = True):
    """Apply Omega_inv() to all directed zeros in a patch (inversion)."""
    thread = grid[i][j]
    new_elements = []
    for e in thread.elements:
        if e.parity == "zero":
            expanded = e.Omega_inv()
            if twist_flip:
                expanded.parity = "down" if expanded.parity == "up" else "up"
            new_elements.append(expanded)
        else:
            new_elements.append(e)
    thread.elements = new_elements


# ───────────────────────────────────────────────────────────────────────────────
# Mass Formula (from amplitudes to physical mass)
# ───────────────────────────────────────────────────────────────────────────────

def amplitude_to_mass(total_amplitude: float, topological_factor: float = 1.0) -> float:
    """Convert total directed number amplitude to physical mass.

    M = (hbar * c / (2 * pi * l_P)) * f * sum(amplitudes)
    where f = topological factor (1.5 for Klein, 1.0 for sphere).
    """
    HBAR = 1.054571817e-34
    C = 2.99792458e8
    L_P = 1.616255e-35
    k = (HBAR * C) / (2 * np.pi * L_P)
    return k * topological_factor * total_amplitude
