"""
IST Directed Number Algebra v0.8.1 — Core Implementation
=========================================================
Axioms 2.1–2.18: Directed numbers with parity, compression/expansion,
non-associative multiplication, and thread calculus.

Reference: supplementary/directed_numbers_v0.8.1.pdf
"""

import numpy as np

# ───────────────────────────────────────────────────────────────────────────────
# Directed Number Core
# ───────────────────────────────────────────────────────────────────────────────

class DirectedNumber:
    """IST directed number with amplitude, parity, and optional memory.

    Axiom 2.1: Elements are a_p where a ∈ ℝ, p ∈ {up, down, zero}.
    Axiom 2.2: 0_up / 0_down are directed zeros (memory); 0_zero is absolute zero.
    """

    def __init__(self, amplitude=0.0, parity="up", memory=None):
        self.amplitude = float(amplitude)
        self.parity = parity
        self.memory = memory

    def info(self):
        return abs(self.amplitude)

    def __repr__(self):
        p = {"up": "↑", "down": "↓", "zero": "⁰"}.get(self.parity, self.parity)
        if self.memory is not None and self.parity == "zero":
            return f"D({self.amplitude:.4f}{p}, mem=({self.memory.amplitude:.4f}{p}))"
        return f"D({self.amplitude:.4f}{p})"

    # Axiom 2.3: Same-parity addition
    # Axiom 2.4: Mixed-parity not directly defined
    def __add__(self, other):
        if isinstance(other, (int, float)):
            return DirectedNumber(self.amplitude + other, self.parity, self.memory)
        if self.parity == other.parity:
            mem = self.memory if self.parity == "zero" else None
            return DirectedNumber(self.amplitude + other.amplitude, self.parity, mem)
        raise ValueError(f"Cannot add different parities: {self.parity} + {other.parity} (Axiom 2.4)")

    # Axiom 2.5: Scalar multiplication
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return DirectedNumber(self.amplitude * other, self.parity, self.memory)
        return _multiply_directed(self, other)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return DirectedNumber(self.amplitude * other, self.parity, self.memory)
        return NotImplemented

    def __neg__(self):
        return DirectedNumber(-self.amplitude, self.parity, self.memory)

    def __sub__(self, other):
        return self + (-other)

    # Axiom 2.10: Compression operator Omega
    def Omega(self):
        if self.parity == "zero":
            return self
        return DirectedZero(memory=DirectedNumber(self.amplitude, self.parity))

    # Axiom 2.11: Expansion operator Omega^-1
    def Omega_inv(self, deterministic=False):
        if self.parity == "zero" and self.memory is not None:
            return DirectedNumber(self.memory.amplitude, self.memory.parity)
        if self.parity == "zero" and self.memory is None:
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
# Multiplication Axioms (2.6 – 2.9)
# ───────────────────────────────────────────────────────────────────────────────

def _multiply_directed(a, b):
    ap, bp = a.parity, b.parity

    if ap != "zero" and bp != "zero":
        return _multiply_manifest(a, b)

    if ap == "zero" and bp == "zero":
        return _multiply_compressed(a, b)

    # Axiom 2.7: manifest * compressed → compressed
    amp = abs(a.amplitude * b.amplitude)
    return DirectedNumber(amp, "zero")


def _multiply_manifest(a, b):
    # Axiom 2.6: Same parity → keep; opposite parity → compress
    if a.parity == b.parity:
        return DirectedNumber(a.amplitude * b.amplitude, a.parity)
    return DirectedNumber(a.amplitude * b.amplitude, "zero")


def _multiply_compressed(a, b):
    # Axiom 2.8: Product of two compressed numbers
    am, bm = a.memory, b.memory

    # Cases from table in Axiom 2.8
    if am is not None and bm is not None:
        if am.parity == "up" and bm.parity == "up":
            return DirectedNumber(1.0, "up")
        if am.parity == "down" and bm.parity == "down":
            return DirectedNumber(-1.0, "down")
        if (am.parity == "up" and bm.parity == "down") or (am.parity == "down" and bm.parity == "up"):
            return AbsoluteZero()

    # (0_p) * 0^0 → 0^0, or 0^0 * (0_p) → 0^0
    if (am is not None and bm is None) or (am is None and bm is not None):
        return AbsoluteZero()

    # Axiom 2.9: 0^0 * 0^0 → probabilistic r ∈ [-1, 1]
    r = _sample_abs_zero_product()
    return DirectedNumber(r, "zero")


def _sample_abs_zero_product():
    """Sample P(r) for absolute-zero products (Axiom 2.9).
    Start with uniform P(r) = 1/2 on [-1, 1]; refined by temporal consistency.
    """
    return (np.random.random() * 2) - 1.0


# ───────────────────────────────────────────────────────────────────────────────
# Thread Calculus (Section 3)
# ───────────────────────────────────────────────────────────────────────────────

class Thread:
    """Sequence of directed numbers forming an information thread.

    Threads may be linear, nested, or parallel. Fork/join balance ensures
    no dangling references (Section 3.4).
    """

    def __init__(self, elements=None, parent=None, time_index=0):
        self.elements = list(elements) if elements else []
        self.parent = parent
        self.children = []
        self.time_index = time_index

    def info(self):
        return sum(e.info() for e in self.elements) + sum(c.info() for c in self.children)

    def push(self, element):
        self.elements.append(element)

    def pop(self):
        return self.elements.pop() if self.elements else None

    def fork(self):
        child = Thread(parent=self, time_index=self.time_index)
        self.children.append(child)
        return child

    def join(self, child):
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            self.elements.extend(child.elements)
            self.children.extend(child.children)

    def cross_multiply(self, other):
        result = Thread()
        for a in self.elements:
            for b in other.elements:
                result.push(a * b)
        return result

    def all_threads(self):
        yield self
        for c in self.children:
            yield from c.all_threads()

    def total_info(self):
        return sum(t.info() for t in self.all_threads())

    def __repr__(self):
        return f"Thread(t={self.time_index}, n={len(self.elements)}, children={len(self.children)}, I={self.info():.2f})"


class TemporalThread(Thread):
    """Thread with time-indexed directed numbers and temporal shift operators.

    Axiom 2.15–2.18: Temporal directed numbers carry time coordinate.
    T_plus / T_minus shift time with optional parity flip across twists.
    """

    def __init__(self, elements=None, parent=None, time_index=0, twist_on_shift=False):
        super().__init__(elements, parent, time_index)
        self.twist_on_shift = twist_on_shift

    def T_plus(self):
        """Forward temporal shift (Axiom 2.16)."""
        self.time_index += 1
        if self.twist_on_shift:
            for e in self.elements:
                if e.parity == "up":
                    e.parity = "down"
                elif e.parity == "down":
                    e.parity = "up"

    def T_minus(self):
        """Backward temporal shift (Axiom 2.16)."""
        self.time_index -= 1
        if self.twist_on_shift:
            for e in self.elements:
                if e.parity == "up":
                    e.parity = "down"
                elif e.parity == "down":
                    e.parity = "up"


# ───────────────────────────────────────────────────────────────────────────────
# Sinkhorn-Knopp Projection (Section 4)
# ───────────────────────────────────────────────────────────────────────────────

def sinkhorn_knopp(matrix, iterations=100, tol=1e-9):
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

def closed_time_loop_product(sequence, twist_crossings=0):
    """Compute product of directed numbers along a closed time loop.

    Axiom 2.17: Π must equal 1_up (even parity) or (-1)_down (odd parity).
    """
    result = sequence[0]
    for x in sequence[1:]:
        result = result * x
    expected = DirectedNumber(1.0, "down") if twist_crossings % 2 != 0 else DirectedNumber(1.0, "up")
    return result, expected


def derive_P_distribution(num_samples=100000):
    """Derive P(r) distribution from temporal consistency requirements.

    Samples absolute-zero products and measures the empirical distribution
    of outcomes for 0^0 * 0^0.
    """
    samples = np.array([(AbsoluteZero() * AbsoluteZero()).amplitude for _ in range(num_samples)])
    return samples


# ───────────────────────────────────────────────────────────────────────────────
# Utility: Thread Grid for Horizon Patches
# ───────────────────────────────────────────────────────────────────────────────

def create_thread_grid(n_patches, initial_amplitude=0.5, seed=None):
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


def grid_total_info(grid):
    return sum(grid[i][j].info() for i in range(len(grid)) for j in range(len(grid[0])))


def grid_gradient(grid, i, j):
    """Compute local information gradient at patch (i, j)."""
    n_i, n_j = len(grid), len(grid[0])
    info_ij = grid[i][j].info()
    neighbors = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = (i + di) % n_i, (j + dj) % n_j
        neighbors.append(grid[ni][nj].info())
    return (sum((info_ij - n) ** 2 for n in neighbors) / len(neighbors)) ** 0.5


def compress_patch(grid, i, j):
    """Apply Omega() to all directed numbers in a patch (frozen knot formation)."""
    thread = grid[i][j]
    thread.elements = [e.Omega() for e in thread.elements]


def invert_patch(grid, i, j, twist_flip=True):
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

def amplitude_to_mass(total_amplitude, topological_factor=1.0):
    """Convert total directed number amplitude to physical mass.

    M = (hbar * c / (2 * pi * l_P)) * f * sum(amplitudes)
    where f = topological factor (1.5 for Klein, 1.0 for sphere).
    """
    HBAR = 1.054571817e-34
    C = 2.99792458e8
    L_P = 1.616255e-35
    k = (HBAR * C) / (2 * np.pi * L_P)
    return k * topological_factor * total_amplitude
