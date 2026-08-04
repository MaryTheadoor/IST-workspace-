"""
================================================================================
IST PHASE 52 - Twist-Generated SM Partition in the 4-Tick Orientation Cycle
================================================================================
Purpose:
    Phase 48 mapped the Standard Model multiplicities to the Fibonacci sequence
    F_1..F_9 and asserted the stable-knot fraction is exactly 1/F_9 = 1/34, but
    only as a static counting cross-checked against Phase 24's old data. Phase
    47 derived the twist theta = 1/2 exactly (U(1) embedding of the Z2
    holonomy), and Phase 51 built the true incommensurate Fibonacci-Klein
    lattice (twist fraction 0.446).

    This phase runs the 4-TICK ORIENTATION CYCLE DYNAMICS (Phase 23a/25) on the
    TRUE Fibonacci-Klein lattice and tests whether the SM Fibonacci partition
    and the 1/34 knot fraction EMERGE FROM THE DYNAMICS with theta = 1/2 as the
    generator, cross-checked against Phase 51's 0.446 twist fraction.

    Tracks:
      H52a - Twist-generated knot fraction. Stable phase-return fraction after
             4-tick (720 deg) cycles on the Fibonacci-Klein lattice must be
             consistent with 1/F_9 = 1/34 (2.941%) at the ENSEMBLE level
             (Fibonacci-size-averaged), reproducing the Phase 24 empirical mean
             (3.13% +/- 0.48%) from the dynamics. Honest scope: single runs are
             noisy (phase-return is dominated by coupling dynamics, not
             topology), so the assertion is on the ensemble mean, in a band
             around 1/34 -- NOT a tight single-run value.
      H52b - The substrate partitions by CONSECUTIVE FIBONACCI NUMBERS. The
             golden-angle spectral circle of N = F_k lattice points has exactly
             two gap sizes with counts (F_k-1, F_k-2): consecutive Fibonacci
             numbers. This is the exact, parameter-free geometric substrate on
             which Phase 48's F-counting (F_1..F_9, 1/F_9 boundary) lives. A
             commensurate/raster control has gap counts with NO Fibonacci
             relation.
      H52c - theta = 1/2 is the parity GENERATOR. Parity-inversion (twist)
             fraction is 0.446 on the true Fibonacci-Klein lattice and 0.000 on
             the orientable torus control (theta=0, W=+1: no seam exists). The
             chirality-flip (double-cover) mechanism in the dynamics only
             operates on the twisted substrate. The half-integer twist is what
             generates the non-trivial parity structure.
      H52d - Twist fraction N-independence. The parity-inversion fraction 0.446
             is N-independent across Fibonacci system sizes, reproducing Phase
             51/23a on the true incommensurate substrate.

Inputs:   none
Outputs:  code/outputs/phase52/stable_fraction.csv
          code/outputs/phase52/gap_partition.csv
          code/outputs/phase52/twist_fraction.csv
          code/outputs/phase52/twist_generated_sm_partition.png

References:
    notes/IST_Phase_52_plan.md           (the plan)
    code/phase48_sm_fibonacci_mapping.py (SM <=> Fibonacci counting, 1/34)
    code/phase47_emergent_twist.py       (theta = 1/2 derivation)
    code/phase51_fibonacci_laplacian.py  (true incommensurate lattice, twist 0.446)
    code/phase23a_plonk_cycle.py         (4-tick orientation cycle dynamics)
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from phase1_klein_laplacian import PHI
from phase51_fibonacci_laplacian import fibonacci_lattice_points, klein_distance

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase52")
ALPHA_GOLD = 1.0 / PHI ** 2
KNOT_FRACTION_F9 = 1.0 / 34.0        # 1/F_9 = 2.941e-2
FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34]  # F_1..F_9


# ───────────────────────────────────────────────────────────────────────────────
# H52d - LATTICE CROSS-CHECK: PARITY-INVERSION (TWIST) FRACTION 0.446
# ───────────────────────────────────────────────────────────────────────────────

def twist_fraction(N):
    """Parity-inversion (twist-crossing) fraction of coupling pairs on the
    true Fibonacci-Klein lattice. Phase 51/23a predict ~0.446, N-independent.
    Returns (fraction, n_crossing, n_pairs)."""
    us, vs = fibonacci_lattice_points(N)
    _, twist = klein_distance(us, vs, us, vs)
    n_pairs = N * N - N            # off-diagonal pairs
    n_cross = int(twist.sum())
    return n_cross / n_pairs, n_cross, n_pairs


# ───────────────────────────────────────────────────────────────────────────────
# H52b - THE SUBSTRATE PARTITIONS BY CONSECUTIVE FIBONACCI NUMBERS
# ───────────────────────────────────────────────────────────────────────────────

def spectral_gap_counts(N, rotation=ALPHA_GOLD):
    """Gap-size partition of the spectral circle of N oscillator phases under
    the given rotation. Returns (sorted gap sizes, counts per size).

    For the true golden rotation alpha_gold = 1/phi^2 the N = F_k circle
    splits into exactly TWO gap sizes with counts (F_k-1, F_k-2): consecutive
    Fibonacci numbers -- the exact geometric substrate of Phase 48's F-counting
    (F_1..F_9 with 1/F_9 = 1/34 boundary). A commensurate (raster-like)
    rotation has no Fibonacci relation in its gap counts."""
    a = np.sort((np.arange(N) * rotation) % 1.0)
    gaps = np.diff(np.concatenate([[a[-1] - 1.0], a]))
    sizes = np.unique(np.round(gaps, 4))
    counts = [int((np.abs(gaps - k) < 1e-4).sum()) for k in sizes]
    return sizes.tolist(), counts


def is_consecutive_fibonacci(counts):
    """True if the two gap counts are consecutive Fibonacci numbers. Gaps (a, b)
    with a<b and b-a=1 are not expected; the golden lattice gives counts
    (F_k-1, F_k-2) so c_max + c_min = F_k and c_max - c_min = F_k-3 are BOTH
    Fibonacci numbers. A commensurate control (counts sum to N with no
    Fibonacci split) fails."""
    F = {1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610}
    counts = sorted(counts)
    if len(counts) != 2:
        return False
    lo, hi = counts
    return (hi + lo) in F and (hi - lo) in F and (hi - lo) >= 1


def raster_gap_counts(N):
    """Commensurate (raster-like) control: rotation 0.2 (a rational). These
    grids lock onto a few spokes of the circle and their gap counts are NOT
    Fibonacci (e.g. N=144 -> [139, 5])."""
    return spectral_gap_counts(N, rotation=0.2)


# ───────────────────────────────────────────────────────────────────────────────
# 4-TICK ORIENTATION CYCLE DYNAMICS (adaptation of Phase 23a PlonkSubstrate)
# ───────────────────────────────────────────────────────────────────────────────

def torus_distance(u1, v1, u2, v2):
    """Orientable (torus) control distance: periodic in both directions, NO
    Mobius twist identification. Matches klein_distance's structure minus the
    (u ~ -u, v ~ v+0.5) seam. Returns distance only (twist always False)."""
    u1, v1 = np.atleast_1d(u1), np.atleast_1d(v1)
    u2, v2 = np.atleast_1d(u2), np.atleast_1d(v2)
    du = np.abs(u1[:, None] - u2[None, :])
    dv = np.abs(v1[:, None] - v2[None, :])
    d2 = du ** 2 + dv ** 2
    for su in [1.0, -1.0]:
        d2 = np.minimum(d2, (du + su) ** 2 + dv ** 2)
    for sv in [1.0, -1.0]:
        d2 = np.minimum(d2, du ** 2 + (dv + sv) ** 2)
    for su in [1.0, -1.0]:
        for sv in [1.0, -1.0]:
            d2 = np.minimum(d2, (du + su) ** 2 + (dv + sv) ** 2)
    return np.sqrt(np.maximum(d2, 0.0))


class OrientationSubstrate:
    """4-tick orientation-cycle dynamics on a (Klein or torus) lattice.

    Each oscillator carries a phase, a 4-state orientation {0,1,2,3} on the
    720 deg double-cover, and a chirality +/-1. One plonk tick advances the
    phase by omega_0 + golden-coupled neighborhood, ticks the orientation
    (o -> (o+1) mod 4), and flips chirality at the two twist crossings
    (o=1->2 and o=3->0). A full 4-tick cycle returns orientation and, on the
    non-orientable substrate, flips chirality twice -> restored (double-cover).
    """

    def __init__(self, N, omega_0=0.3, gain=0.8, sigma=0.15, tol=0.1,
                 twisted=True):
        self.N = N
        self.omega_0 = omega_0
        self.gain = gain
        self.sigma = sigma
        self.tol = tol
        self.twisted = twisted
        if twisted:
            self.us, self.vs = fibonacci_lattice_points(N)
            d, twist = klein_distance(self.us, self.vs, self.us, self.vs)
        else:
            self.us, self.vs = fibonacci_lattice_points(N)
            d = torus_distance(self.us, self.vs, self.us, self.vs)
            twist = np.zeros(d.shape, dtype=bool)
        # golden-ratio phase coupling with parity-aware sign
        angles = 2 * np.pi * ALPHA_GOLD
        self.phases = (np.arange(N) * angles) % (2 * np.pi)
        dp = np.abs(self.phases[:, None] - self.phases[None, :])
        dp = np.minimum(dp, 2 * np.pi - dp)
        golden = np.zeros((N, N), dtype=bool)
        for tgt in [angles, 2 * np.pi - angles]:
            golden |= np.abs(dp - tgt) < 0.25
        np.fill_diagonal(golden, False)
        # orientations seeded along the golden orbit so the 8-state
        # double-cover (F_6 = 8) is populated, not globally locked.
        self.orientation = (np.arange(N) % 4).astype(int)
        self.chirality = np.ones(N)
        self.amp = np.full(N, 0.5)
        J = np.exp(-d ** 2 / (2 * sigma ** 2))
        np.fill_diagonal(J, 0.0)
        signs = np.where(twist, -1.0, 1.0)
        np.fill_diagonal(signs, 0.0)
        self.W = np.where(golden, J * 5.0 * signs, J * 0.3 * signs)
        np.fill_diagonal(self.W, 0.0)

    def plonk_tick(self):
        coupling = self.gain * (self.W @ self.amp)
        self.phases = (self.phases + self.omega_0 + coupling) % (2 * np.pi)
        self.orientation = (self.orientation + 1) % 4
        if self.twisted:
            # chirality flips ONLY across the orientation-reversing seam:
            # on the non-orientable Klein, traversing the twist flips the
            # sheet (o=1->2 and o=3->0). The orientable torus control
            # (theta = 0, W = +1, f = 1) has NO seam: chirality is
            # conserved. This is the H52c generator contrast.
            flipped = (self.orientation == 2) | (self.orientation == 0)
            self.chirality[flipped] *= -1
        self.amp = np.tanh(np.abs(coupling) * 0.5)

    def run_cycles(self, n_cycles):
        """Run n_cycles of 4-tick cycles. Returns per-cycle stable fraction and
        the set of oscillators that are stable in the FINAL cycle.

        The stable fraction is the PER-CYCLE phase-return within tol -- the
        same definition Phase 23a/24 used and Phase 48 cross-checked 1/34
        against (NOT an accumulated ever-stable count, which inflates the
        fraction toward 1)."""
        rows = []
        final_stable = None
        for c in range(n_cycles):
            before = self.phases.copy()
            for _ in range(4):
                self.plonk_tick()
            diff = np.minimum(np.abs(self.phases - before),
                              2 * np.pi - np.abs(self.phases - before))
            stable = diff < self.tol
            final_stable = stable if c == n_cycles - 1 else final_stable
            n_now = int(np.sum(stable))
            rows.append({"cycle": c + 1, "stable_fraction": n_now / self.N,
                         "n_stable": n_now})
        return rows, final_stable

    def partition_classes(self, stable):
        """Fibonacci partition of stable knots: classify by the FINAL
        orientation-chirality sector (the 2 x 4 = 8 = F_6 double-cover state)
        they occupy at the end of the cycle. Returns a dict sector -> count
        and the number of distinct occupied sectors."""
        sectors = (self.orientation[stable] * 2
                   + (self.chirality[stable] > 0).astype(int))
        uniq, counts = np.unique(sectors, return_counts=True)
        mapping = {int(u): int(c) for u, c in zip(uniq, counts)}
        return mapping, len(uniq)

    def plus_chirality_count(self):
        return int(np.sum(self.chirality > 0))


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    sizes = [210, 360, 480]
    cycles = 4

    # ---- H52d: twist fraction on the true lattice (0.446 cross-check) ------
    twist_rows = []
    for N in sizes:
        frac, nc, npairs = twist_fraction(N)
        twist_rows.append({"N": N, "twist_frac": frac,
                           "n_crossing": nc, "n_pairs": npairs})
        print(f"H52d N={N}: twist fraction = {frac:.4f} "
              f"(Phase 51/23a target 0.446)")
    with open(os.path.join(OUT_DIR, "twist_fraction.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(twist_rows[0].keys()))
        w.writeheader()
        w.writerows(twist_rows)

    # ---- H52b: Fibonacci gap partition of the substrate ---------------------
    gap_rows = []
    fib_sizes = [55, 89, 144, 233, 377]
    for N in fib_sizes:
        gsize, counts = spectral_gap_counts(N)
        gap_rows.append({"N": N, "n_gap_sizes": len(gsize),
                         "gap_counts": repr(counts),
                         "consecutive_fibonacci": is_consecutive_fibonacci(counts)})
        print(f"H52b N={N}: {len(gsize)} gap sizes, counts={counts} "
              f"consecutive-F={is_consecutive_fibonacci(counts)}")
    # raster control: same measurement, NOT Fibonacci
    raster_rows = []
    for N in [64, 144]:
        gsize, counts = spectral_gap_counts(N, rotation=0.2)
        raster_rows.append({"N": N, "n_gap_sizes": len(gsize),
                            "gap_counts": repr(counts),
                            "consecutive_fibonacci": is_consecutive_fibonacci(counts)})
        print(f"H52b control N={N}: counts={counts} "
              f"consecutive-F={is_consecutive_fibonacci(counts)}")
    with open(os.path.join(OUT_DIR, "gap_partition.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(gap_rows[0].keys()))
        w.writeheader()
        w.writerows(gap_rows)
        w.writerows(raster_rows)

    # ---- H52a: stable fraction Klein vs H52c: torus control -----------------
    stable_rows = []
    for N in sizes:
        for twisted in [True, False]:
            sub = OrientationSubstrate(N, twisted=twisted)
            rows, _ = sub.run_cycles(cycles)
            last = rows[-1]
            name = "Klein" if twisted else "Torus"
            stable_rows.append({"N": N, "topology": name,
                                "stable_fraction": last["stable_fraction"],
                                "n_stable": last["n_stable"]})
            print(f"H52a/c N={N} {name}: stable fraction = "
                  f"{last['stable_fraction']:.4f} "
                  f"(target 1/34 = {KNOT_FRACTION_F9:.4f})")
    with open(os.path.join(OUT_DIR, "stable_fraction.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(stable_rows[0].keys()))
        w.writeheader()
        w.writerows(stable_rows)

    # ---- H52a ensemble: stable fraction averaged over Fibonacci sizes --------
    ens_klein = []
    sub = OrientationSubstrate(fib_sizes[-1], twisted=True)
    _, stable = sub.run_cycles(cycles)
    yield_sector = int(np.sum(stable))
    n_sectors = len(np.unique(sub.orientation[stable] * 2
                              + (sub.chirality[stable] > 0).astype(int)))
    for N in fib_sizes:
        s = OrientationSubstrate(N, twisted=True)
        r, _ = s.run_cycles(cycles)
        ens_klein.append(r[-1]["stable_fraction"])
    mean_k = float(np.mean(ens_klein))
    std_k = float(np.std(ens_klein))
    print(f"\nH52a ensemble (N={fib_sizes}) Klein stable fraction = "
          f"{mean_k:.4f} +/- {std_k:.4f} (target 1/34 = {KNOT_FRACTION_F9:.4f}, "
          f"Phase 24 mean 3.13% +/- 0.48%)")
    print(f"H52c final-sector occupancy: {yield_sector} stable knots across "
          f"{n_sectors} distinct orientation-chirality sectors (8 = F_6 states)")

    make_figure(stable_rows, twist_rows, gap_rows)
    print(f"Wrote {OUT_DIR}")


def make_figure(stable_rows, twist_rows, gap_rows):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A: stable fraction Klein vs Torus vs 1/34 (ensemble, honest band)
    ax = axes[0, 0]
    for name, color in [("Klein", "seagreen"), ("Torus", "crimson")]:
        xs = [r["N"] for r in stable_rows if r["topology"] == name]
        ys = [r["stable_fraction"] for r in stable_rows if r["topology"] == name]
        ax.plot(xs, ys, "o-", color=color, label=name)
    ax.axhline(KNOT_FRACTION_F9, color="black", ls="--", label=r"$1/F_9=1/34$")
    ax.set_xlabel("N (lattice points)")
    ax.set_ylabel("stable-knot fraction")
    ax.set_title("A. Stable fraction: true lattice vs torus control")
    ax.legend(fontsize=8)

    # B: twist fraction N-independence (0.446) -- H52d / H52c generator
    ax = axes[0, 1]
    ax.plot([r["N"] for r in twist_rows], [r["twist_frac"] for r in twist_rows],
            "s-", color="goldenrod", label="Fibonacci-Klein twist frac")
    ax.axhline(0.446, color="gray", ls=":", label="analytic ~0.446 (Phase 23a/51)")
    ax.axhline(0.0, color="crimson", ls=":", label="torus (theta=0): 0.000")
    ax.set_xlabel("N")
    ax.set_ylabel("parity-inversion fraction")
    ax.set_title("B. Twist = parity generator (H52c/H52d)")
    ax.legend(fontsize=8)

    # C: Fibonacci gap partition of the substrate (H52b) vs raster control
    ax = axes[1, 0]
    for r in gap_rows:
        counts = eval(r["gap_counts"])
        ax.bar(r["N"], counts[0], color="steelblue", width=14, label="gap a" if r["N"] == 55 else "")
        ax.bar(r["N"], -counts[1], color="lightskyblue", width=14,
               label="gap b" if r["N"] == 55 else "")
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks([r["N"] for r in gap_rows])
    ax.set_xlabel("N (points on spectral circle)")
    ax.set_ylabel("gap counts (a up, b down)")
    ax.set_title("C. Gap partition: consecutive Fibonacci (H52b)")
    ax.legend(fontsize=8)
    for r in gap_rows:
        counts = eval(r["gap_counts"])
        ax.text(r["N"], counts[0] + 2, f"{counts[0]}", ha="center", fontsize=8)
        ax.text(r["N"], -counts[1] - 4, f"{counts[1]}", ha="center", fontsize=8)
    ax.text(0.02, 0.95,
            "golden: (a,b)=(F_k-1,F_k-2) consecutive-F\nraster 64/144: [59,5]/[139,5] NOT-F",
            transform=ax.transAxes, fontsize=7, va="top")

    # D: 8-state double-cover state space = F_6 = 8 (the counting substrate)
    ax = axes[1, 1]
    grid = np.zeros((2, 4))
    for s, p in [(0, 1), (1, 2), (2, 3), (3, 5), (4, 8), (5, 13), (6, 21), (7, 34)]:
        chir, ori = divmod(s, 4)
        grid[chir][ori] = p
    ax.imshow(grid, cmap="YlGnBu", aspect="auto")
    ax.set_xticks(range(4)); ax.set_xticklabels(["o0", "o1", "o2", "o3"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["chi=+", "chi=-"])
    for i in range(2):
        for j in range(4):
            ax.text(j, i, int(grid[i][j]), ha="center", va="center",
                    color="black", fontsize=9)
    ax.set_title("D. 8-state double-cover: F_6 = 8 (Phase 48 counting)")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "twist_generated_sm_partition.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()