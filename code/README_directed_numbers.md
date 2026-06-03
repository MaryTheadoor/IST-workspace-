# Directed Numbers Runtime — Plan 9

**Executable thread calculus for IST manifold dynamics**

---

## Overview

This module implements the Directed Numbers algebra (v0.9.0) as a native Python runtime library. It provides the core building blocks for simulating non-associative information flow on black hole horizons, cosmic manifolds, and any topological substrate.

### Key Features

- **Directed numbers** with parity (UP, DOWN, ZERO, GRAV_UP, GRAV_DOWN)
- **Non-associative multiplication** per Axioms 2.6–2.10
- **Compression/expansion operators** (Omega / Omega_inv) with memory
- **Thread calculus** — push/pop, fork/join, cross-multiplication
- **Temporal threads** — time-indexed with parity flip across twists
- **Closed loop consistency** — verifies Axiom 2.18 constraints
- **Thread grid utilities** — for horizon patch simulations
- **Mass formula** — converts topological information to physical mass

---

## Installation

```bash
pip install numpy
```

Requires Python 3.9+. NumPy is optional but recommended for vectorized operations.

---

## Quick Start

```python
from directed_numbers import *

# Create directed numbers
x = DirectedNumber(2.0, "up")     # manifest up
y = DirectedNumber(3.0, "down")   # manifest down

# Multiplication (non-associative)
z = x * y                          # opposite parity -> compressed zero
print(z.parity)                    # "zero"

# Compression and expansion
compressed = Omega(x)              # D(0.0000_zero, mem=(2.0000_up))
restored = Omega_inv(compressed)   # D(2.0000_up)

# Associator: measures non-associativity
dz = DirectedZero(memory=DirectedNumber(0.0, "up"))
dn = DirectedNumber(1.0, "down")
a = associator(dz, dz, dn)        # ~1.0 (Axiom 2.14)
```

### Thread Calculus

```python
# Create a thread
t = Thread()
t.push(DirectedNumber(1.0, "up"))
t.push(DirectedNumber(2.0, "down"))

# Fork a parallel thread
child = t.fork()
child.push(DirectedNumber(3.0, "up"))

# Cross-multiply two threads
t2 = Thread([DirectedNumber(1.0, "up")])
result = t.cross_multiply(t2)      # returns new Thread

# Join a child back
t.join(child)

# Total information
print(t.info_total())              # includes children
```

### Temporal Threads

```python
# Create temporal thread with twist
tt = TemporalThread(
    [DirectedNumber(1.0, "up")],
    twist_on_shift=True
)

tt.T_plus()                        # time +1, parity flips up->down
tt.T_plus()                        # time +2, parity flips down->up

# Check closed loop consistency (Axiom 2.18)
valid, msg = tt.closed_loop_condition()
```

### Horizon Simulation

```python
# Create a patch grid for black hole simulation
grid = create_thread_grid(20, initial_amplitude=0.3, seed=42)

# Compress patches under gradient
for i, j in high_gradient_patches:
    compress_patch(grid, i, j)

# Expand with parity flip (Klein bottle twist)
for i, j in compressed_patches:
    invert_patch(grid, i, j, twist_flip=True)

# Compute mass
mass = amplitude_to_mass(grid_total_info(grid), topological_factor=1.5)
```

---

## API Reference

### Core Types

| Class | Description |
|-------|-------------|
| `DirectedNumber(amplitude, parity, memory=None)` | Main directed number. Parity: string (`"up"`, `"down"`, `"zero"`) or `Parity` enum |
| `DirectedZero(memory=None)` | Directed zero — compressed number with memory |
| `AbsoluteZero()` | Absolute zero — pristine zero-point gate, no history |
| `DNumber(amp, parity, memory)` | Lightweight dataclass value type |
| `Parity` | Enum: `UP`, `DOWN`, `ZERO`, `GRAV_UP`, `GRAV_DOWN` |

### DirectedNumber Properties

| Property | Description |
|----------|-------------|
| `amplitude` | Float amplitude |
| `parity` | String parity (backward-compatible) |
| `parity_enum` | `Parity` enum |
| `memory` | Original `DirectedNumber` before compression |
| `is_absolute_zero` | True if absolute zero |
| `is_directed_zero` | True if directed zero (has memory) |
| `info()` | Absolute amplitude (information measure) |
| `to_dnumber()` | Convert to lightweight `DNumber` |

### DirectedNumber Methods

| Method | Description |
|--------|-------------|
| `Omega()` | Compress to directed zero (Axiom 2.10) |
| `Omega_inv(deterministic=False)` | Expand from zero (Axiom 2.11) |

### Thread & TemporalThread

| Method | Description |
|--------|-------------|
| `push(dn)` | Push directed number onto thread |
| `pop()` | Pop directed number from thread |
| `fork()` | Create child thread with copy of elements |
| `join(child)` | Merge child thread back |
| `cross_multiply(other)` | Return NEW thread with pairwise products |
| `info()` | Sum of info over direct elements |
| `info_total()` / `total_info()` | Sum of info over all elements + children |
| `all_threads()` | Generator: self + all descendants |
| `T_plus()` | Time +1, parity flip if twisted |
| `T_minus()` | Time -1, parity flip if twisted |
| `closed_loop_condition()` | Check Axiom 2.18 (returns `(bool, str)`) |

### Module Functions

| Function | Description |
|----------|-------------|
| `mul(a, b)` | Explicit non-associative multiplication |
| `associator(x, y, z)` | Compute `|(x*y)*z - x*(y*z)|` |
| `Omega(x)` | Module-level compression |
| `Omega_inv(x, deterministic)` | Module-level expansion |
| `sinkhorn_knopp(M, iters, tol)` | Doubly-stochastic projection |
| `closed_time_loop_product(seq, twists)` | Return `(result, expected)` |
| `create_thread_grid(n, amp, seed)` | Create n×n thread grid |
| `grid_total_info(grid)` | Sum info over grid |
| `grid_gradient(grid, i, j)` | Local info gradient |
| `compress_patch(grid, i, j)` | Omega all elements in patch |
| `invert_patch(grid, i, j, twist_flip)` | Omega_inv all zeros in patch |
| `amplitude_to_mass(amp, f)` | Convert to physical mass (kg) |

---

## Axioms Tested

All 78 unit tests pass, covering:

- **Axiom 2.3–2.4** — Same-parity addition, mixed-parity error
- **Axiom 2.6** — Manifest × manifest (same/opposite parity)
- **Axiom 2.7** — Manifest × compressed → compressed
- **Axiom 2.8** — Compressed × compressed (memory-dependent products)
- **Axiom 2.9** — Absolute zero × absolute zero → probabilistic
- **Axiom 2.10** — Omega compression
- **Axiom 2.11** — Omega_inv expansion
- **Axiom 2.12** — Information conservation
- **Axiom 2.13** — Non-associativity
- **Axiom 2.14** — Associator magnitude
- **Axiom 2.15–2.18** — Temporal shifts and closed loop consistency

---

## Running Tests

```bash
python -m pytest tests/test_directed_numbers.py -v
```

---

## Integration with Black Hole Simulation

The `black_hole_simulation.py` module imports the directed numbers runtime for:

- Horizon patch grids as `Thread` objects
- Information density via `grid_total_info()`
- Compression/inversion via `compress_patch()` / `invert_patch()`
- Associator charge via `compute_associator_charge()`
- Mass computation via `amplitude_to_mass()`

Run the validation simulation:

```bash
cd code
python -c "from black_hole_simulation import run_validation_simulation; run_validation_simulation()"
```

---

## Related Documents

- `supplementary/directed_numbers_v0.8.1.pdf` — Full axiomatic development
- `notes/IST Plan 8.md` — Plan 8 theoretical foundations
- `notes/beta_function_derivation.md` — Beta function from directed numbers
- `notes/tqft_action.md` — TQFT formulation

---

*"The directed numbers runtime is the executable form of the substrate algebra. Every compression records memory. Every expansion restores history. Every twist flips parity."*
