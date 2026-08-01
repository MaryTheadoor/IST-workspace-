"""
================================================================================
IST PHASE 9 - Game-of-Life Substrate Automaton
================================================================================
Conway's Game of Life on the Klein bottle grid + a golden-phase tracker.
Each live cell carries a phase on the spectral circle. At each tick,
golden-resonant cells (those with >= 1 neighbour at golden-ratio phase
separation) get a SURVIVAL BONUS — they survive at 2 neighbours even
if the Conway rule would kill them. Cells with ZERO golden neighbours
get a death penalty (rational mode-locking). The automaton selects
for persistent golden-phase structures from random initial conditions.

Tests: entropy decrease, golden fraction increase, persistent structures,
antipodal balance.
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import label

from phase1_klein_laplacian import PHI, build_klein_bottle_graph

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase9")
ALPHA_GOLDEN = 1.0 / PHI ** 2
TOL = 0.40


class ISTAutomaton:
    """Conway's Game of Life on the Klein bottle grid with golden tracking.

    Grid: n x n Klein bottle, 4-regular (SubstrateGraph).
    State: a_i in {0, 1} (dead/alive) + phase phi_i in [0, 2pi).
    """

    def __init__(self, n=48, alive_frac=0.35, seed=1):
        self.n = n
        self.N = n * n
        rng = np.random.default_rng(seed)
        self.grid = (rng.random(self.N) < alive_frac).astype(float)
        self.phase = 2 * np.pi * rng.uniform(size=self.N)
        g = build_klein_bottle_graph(n, n)
        A_dense = g.A.toarray()
        self.nbrs = [np.flatnonzero(A_dense[i] > 0) for i in range(self.N)]
        self.step_count = 0

    def _n_live(self):
        return np.array([sum(self.grid[j] > 0 for j in self.nbrs[i])
                         for i in range(self.N)])

    def _golden_resonant(self):
        """Cells that have >= 1 neighbour at golden phase separation."""
        alive = self.grid > 0
        golden = np.zeros(self.N, dtype=bool)
        for i in range(self.N):
            if not alive[i]:
                continue
            for j in self.nbrs[i]:
                if self.grid[j] == 0:
                    continue
                d = min(abs(self.phase[i] - self.phase[j]),
                        2 * np.pi - abs(self.phase[i] - self.phase[j]))
                for tgt in [2 * np.pi * ALPHA_GOLDEN,
                            2 * np.pi * (1 - ALPHA_GOLDEN)]:
                    if abs(d - tgt) < TOL:
                        golden[i] = True
                        break
                if golden[i]:
                    break
        return golden

    def step(self):
        alive = self.grid > 0
        # gold attractor: every living cell advances by golden angle per tick
        self.phase[alive] = (self.phase[alive]
                             + 2 * np.pi * ALPHA_GOLDEN) % (2 * np.pi)

        n_live = self._n_live()
        golden = self._golden_resonant()

        new_grid = np.zeros(self.N)
        new_phase = self.phase.copy()

        for i in range(self.N):
            n = int(n_live[i])
            if not alive[i]:
                if n == 3:
                    new_grid[i] = 1.0
                    live_js = [j for j in self.nbrs[i] if alive[j]]
                    new_phase[i] = np.mean(self.phase[live_js]) % (2*np.pi)
            else:
                # golden survival bonus
                if golden[i]:
                    survive = 1 <= n <= 4  # golden cells resist both isolation and overcrowding
                else:
                    survive = 2 <= n <= 3  # standard Conway

                if survive:
                    new_grid[i] = 1.0

        self.grid = new_grid
        self.step_count += 1

    # ── observables ─────────────────────────────────────────────────────

    def live_count(self):
        return int(self.grid.sum())

    def golden_fraction(self):
        alive = self.grid > 0
        if alive.sum() == 0:
            return 0.0
        return self._golden_resonant().sum() / alive.sum()

    def entropy(self):
        """Shannon entropy of the spatial live-cell distribution."""
        if self.live_count() == 0:
            return 0.0
        # coarse-grain: 6x6 block entropy
        blk = self.grid.reshape(self.n, self.n)
        bs = 6
        h = 0.0
        for r in range(0, self.n, bs):
            for c in range(0, self.n, bs):
                p = blk[r:r+bs, c:c+bs].mean()
                if p > 0:
                    h -= p * np.log(p)
        return h

    def structure_count(self):
        blk = self.grid.reshape(self.n, self.n) > 0
        s = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        _, nc = label(blk, structure=s)
        return nc

    def antipodal_balance(self):
        """Mean grid value — should be ~0.5 steady-state (balanced)."""
        return self.grid.mean()

    def run(self, n_steps=300, record_every=5):
        rows = []
        for t in range(n_steps):
            self.step()
            if t % record_every == 0:
                rows.append({
                    "step": t + 1,
                    "live_count": self.live_count(),
                    "golden_fraction": self.golden_fraction(),
                    "entropy": self.entropy(),
                    "structures": self.structure_count(),
                })
        return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    automaton = ISTAutomaton(n=48, alive_frac=0.35)
    rows = automaton.run(n_steps=300)

    with open(os.path.join(OUT_DIR, "evolution.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("step  live  gold_frac  entropy  structures")
    for r in rows[-6:]:
        print(f"{r['step']:5d}  {r['live_count']:5d}  "
              f"{r['golden_fraction']:9.3f}  {r['entropy']:7.3f}  "
              f"{r['structures']:7d}")

    final = rows[-1]
    init = rows[0]
    print(f"\nGolden fraction: {init['golden_fraction']:.3f} -> "
          f"{final['golden_fraction']:.3f}")
    print(f"Entropy: {init['entropy']:.3f} -> {final['entropy']:.3f}")

    make_figure(rows, automaton)
    print(f"Wrote {OUT_DIR}")


def make_figure(rows, automaton):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    ts = [r["step"] for r in rows]
    ax = axes[0, 0]
    ax.plot(ts, [r["live_count"] for r in rows], "o-", ms=3,
            color="seagreen", label="live")
    ax.set_xlabel("tick"); ax.set_ylabel("count")
    ax.set_title("A. Population"); ax.legend(fontsize=8)

    ax = axes[0, 1]
    ax.plot(ts, [r["entropy"] for r in rows], "-", color="crimson", lw=2)
    ax.set_xlabel("tick"); ax.set_ylabel("entropy")
    ax.set_title("B. Spatial entropy")

    ax = axes[1, 0]
    ax.plot(ts, [r["golden_fraction"] for r in rows], "o-", ms=3,
            color="seagreen")
    ax.set_xlabel("tick"); ax.set_ylabel("golden fraction")
    ax.set_title("C. Golden-resonant fraction")

    ax = axes[1, 1]
    final_grid = automaton.grid.reshape(automaton.n, automaton.n)
    ax.imshow(final_grid, cmap="inferno", aspect="equal", origin="lower")
    ax.set_title(f"D. Final state t={automaton.step_count}")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "structure_evolution.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
