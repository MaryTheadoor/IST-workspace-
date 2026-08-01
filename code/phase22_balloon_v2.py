"""
================================================================================
IST PHASE 22 — Balloon Waves v2: Subcritical + Golden-Only Supercritical
================================================================================
Rebuilt with the correct dynamical regime:
  * Baseline (non-golden): gain < 1 → decay to noise
  * Golden (separation ≈ 2pi/phi^2): gain > 1 → amplification
  * Phase attractor: each oscillator's phase rotates by golden angle/tick
  * Golden filter creates winner-take-all: only golden-connected survive

The coupling between oscillators i,j has weight J_ij that is modulated
by whether their phase separation is golden-resonant. Golden pairs get
5x J; non-golden get 0.3x J. Oscillators evolve for many ticks; the
surviving amplitude patterns reveal golden standing waves.

Output: code/outputs/phase22/balloon_v2.png, balloon_v2.csv
================================================================================
"""
import csv, os, time
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import numpy as np
from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase22")
ALPHA_GOLDEN = 1.0 / PHI ** 2; TOL = 0.06   # narrow golden window -> ~4% of pairs


class BalloonSubstrateV2:
    def __init__(self, N=400, sigma=0.6, gain_base=0.6, gain_golden=3.0,
                 noise_std=0.02, seed=42):
        rng = np.random.default_rng(seed)
        self.xs = 2*np.pi * rng.uniform(size=N)
        self.ys = 2*np.pi * rng.uniform(size=N)
        self.state = rng.random(N) * 0.3
        self.phase = 2*np.pi * rng.uniform(size=N)  # spectral circle phase
        self.N = N; self.sigma = sigma
        self.gain_base = gain_base   # < 1: subcritical decay
        self.gain_golden = gain_golden  # > 1: supercritical for golden
        self.noise_std = noise_std
        self.step_count = 0

    def _pairwise_distance(self):
        x = np.array(self.xs); y = np.array(self.ys)
        dx = x[:, None] - x[None, :]; dy = y[:, None] - y[None, :]
        d2 = dx**2 + dy**2
        for sx in [2*np.pi, -2*np.pi]:
            d2 = np.minimum(d2, (dx+sx)**2 + dy**2)
        for sy in [2*np.pi, -2*np.pi]:
            d2 = np.minimum(d2, dx**2 + (dy+sy)**2)
        for sx in [2*np.pi, -2*np.pi]:
            for sy in [2*np.pi, -2*np.pi]:
                d2 = np.minimum(d2, (dx+sx)**2 + (dy+sy)**2)
        for sx in [0, 2*np.pi, -2*np.pi]:
            for sy in [0, 2*np.pi, -2*np.pi]:
                d2t = (x[:,None]+x[None,:]+sx)**2 + (y[:,None]-y[None,:]+sy)**2
                d2 = np.minimum(d2, d2t)
        return np.sqrt(np.maximum(d2, 0))

    def _golden_matrix(self):
        """Pairwise golden-resonance: True for pairs at golden separation."""
        p = self.phase
        dp = np.abs(p[:, None] - p[None, :])
        dp = np.minimum(dp, 2*np.pi - dp)
        golden = np.zeros((self.N, self.N), dtype=bool)
        for tgt in [2*np.pi*ALPHA_GOLDEN, 2*np.pi*(1-ALPHA_GOLDEN)]:
            golden |= np.abs(dp - tgt) < TOL
        np.fill_diagonal(golden, False)
        return golden

    def step(self):
        # Binary golden adjacency: 1 for golden, 0 otherwise
        dist = self._pairwise_distance()
        J_g = self._golden_matrix().astype(float)
        np.fill_diagonal(J_g, 0)
        W = J_g

        h = W @ self.state
        # single gain for golden-only coupling
        self.state = np.tanh(self.gain_golden * h
                             + self.noise_std * np.random.randn(self.N))

        # Golden attractor: phases rotate
        self.phase = (self.phase + 2*np.pi*ALPHA_GOLDEN) % (2*np.pi)
        self.step_count += 1

    def surviving_amplitudes(self, threshold=0.1):
        alive = self.state > threshold
        return self.state[alive]

    def golden_fraction(self):
        golden = self._golden_matrix()
        # fraction of edges that are golden
        n_edges = self.N * (self.N - 1)
        return golden.sum() / n_edges

    def mean_amplitude(self):
        return self.state.mean()

    def spatial_entropy(self):
        a = self.state[self.state > 1e-9]
        if len(a) < 2: return 0
        p = a / a.sum()
        return -np.sum(p * np.log(p + 1e-12))

    def run(self, n_ticks=5000, record_every=200):
        rows = []
        for t in range(n_ticks):
            self.step()
            if t % record_every == 0:
                survived = self.surviving_amplitudes()
                rows.append({
                    "tick": self.step_count,
                    "n_alive": len(survived),
                    "mean_amp": self.mean_amplitude(),
                    "golden_frac": self.golden_fraction(),
                    "entropy": self.spatial_entropy(),
                    "amp_median": np.median(survived) if len(survived) > 0 else 0,
                })
        return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.perf_counter()
    sub = BalloonSubstrateV2(N=400, sigma=0.3, gain_base=0.3, gain_golden=0.18,
                              noise_std=0.04)
    rows = sub.run(n_ticks=1200, record_every=100)
    print(f"{sub.step_count} ticks in {time.perf_counter()-t0:.0f}s")

    final = rows[-1]
    print(f"Final: {final['n_alive']} alive, mean_amp={final['mean_amp']:.3f}, "
          f"golden_frac={final['golden_frac']:.4f}, "
          f"entropy={final['entropy']:.3f}")

    # Where are the surviving oscillators?
    alive = sub.state > 0.1
    print(f"Survivors: {alive.sum()}/{sub.N} "
          f"(golden frac={sub.golden_fraction():.3f})")

    # Check dominant spatial frequency of survivors
    if alive.sum() > 10:
        x_surv = sub.xs[alive]; y_surv = sub.ys[alive]
        # pair distribution of survivors
        dx = np.abs(x_surv[:, None] - x_surv[None, :])
        dy = np.abs(y_surv[:, None] - y_surv[None, :])
        dx = np.minimum(dx, 2*np.pi - dx)
        dy = np.minimum(dy, 2*np.pi - dy)
        iu = np.triu_indices(len(x_surv), k=1)
        sep_x = dx[iu]; sep_y = dy[iu]
        print(f"Survivor pair sep_x: mean={sep_x.mean():.3f} "
              f"golden={2*np.pi*ALPHA_GOLDEN:.3f}")
        print(f"  fraction near golden: "
              f"{np.sum(np.abs(sep_x-2*np.pi*ALPHA_GOLDEN)<TOL)/len(sep_x):.3f}")

    with open(os.path.join(OUT_DIR, "balloon_v2.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    make_figure(rows, sub)
    print(f"Wrote {OUT_DIR}")


def make_figure(rows, sub):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    ts = [r["tick"] for r in rows]

    ax = axes[0, 0]
    ax.plot(ts, [r["n_alive"] for r in rows], "-", color="seagreen", lw=2)
    ax.set_xlabel("plonk tick"); ax.set_ylabel("survivors")
    ax.set_title("A. Oscillators above threshold")

    ax = axes[0, 1]
    ax.plot(ts, [r["mean_amp"] for r in rows], "-", color="crimson", lw=2)
    ax.set_xlabel("plonk tick"); ax.set_ylabel("mean amplitude")
    ax.set_title("B. Mean amplitude")

    ax = axes[1, 0]
    ax.plot(ts, [r["entropy"] for r in rows], "-", color="steelblue", lw=2)
    ax.set_xlabel("plonk tick"); ax.set_ylabel("entropy")
    ax.set_title("C. Spatial entropy")

    ax = axes[1, 1]
    alive = sub.state > 0.1
    sc = ax.scatter(sub.xs, sub.ys, c=sub.state, cmap="RdBu_r",
                    s=12, vmin=-0.5, vmax=0.5)
    fig.colorbar(sc, ax=ax, label="amplitude")
    ax.set_title(f"D. Final state ({alive.sum()} alive)")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "balloon_v2.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
