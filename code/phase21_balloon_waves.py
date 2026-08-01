"""
================================================================================
IST PHASE 21 — Balloon Waves: Continuous-Surface Standing Wave Selection
================================================================================
Test the balloon model: oscillators at random positions on the 2D Klein
surface (NOT a grid). Run for many plonk ticks. Track the 2-point
spatial correlation of the amplitude field. Golden-ratio spatial
frequencies should dominate the standing wave spectrum over time,
while rational frequencies destructively interfere and decay.

Measurement: pair correlation function xi(d) = <a_i * a_j> binned by
Klein geodesic separation d_ij. Fourier transform of xi(d) gives the
power spectrum P(k). Peak spatial frequencies should cluster at
golden-ratio values as the system stabilizes.

Output: code/outputs/phase21/balloon_waves.csv
        code/outputs/phase21/balloon_waves.png
================================================================================
"""
import csv, os, time
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase21")
ALPHA_GOLDEN = 1.0 / PHI ** 2


class BalloonSubstrate:
    """Oscillators at continuous positions on the Klein bottle surface,
    evolving under the golden-filtered compression operator."""

    def __init__(self, N=350, sigma=0.5, gain=2.0, noise_std=0.01, seed=42):
        rng = np.random.default_rng(seed)
        self.xs = 2*np.pi * rng.uniform(size=N)
        self.ys = 2*np.pi * rng.uniform(size=N)
        self.state = 0.5 * rng.random(N)
        self.N = N; self.sigma = sigma; self.gain = gain
        self.noise_std = noise_std; self.step_count = 0

    def klein_dist(self, i, j):
        dx = self.xs[i] - self.xs[j]; dy = self.ys[i] - self.ys[j]
        d2 = dx**2 + dy**2
        for sx in [2*np.pi, -2*np.pi]:
            d2 = min(d2, (dx+sx)**2 + dy**2)
        for sy in [2*np.pi, -2*np.pi]:
            d2 = min(d2, dx**2 + (dy+sy)**2)
        for sx in [2*np.pi, -2*np.pi]:
            for sy in [2*np.pi, -2*np.pi]:
                d2 = min(d2, (dx+sx)**2 + (dy+sy)**2)
        for sx in [0, 2*np.pi, -2*np.pi]:
            for sy in [0, 2*np.pi, -2*np.pi]:
                d2t = (self.xs[i]+self.xs[j]+sx)**2 + (self.ys[i]-self.ys[j]+sy)**2
                d2 = min(d2, d2t)
        return np.sqrt(max(d2, 0))

    def _build_coupling(self):
        N = self.N
        x = np.array(self.xs); y = np.array(self.ys)
        dx = x[:, None] - x[None, :]
        dy = y[:, None] - y[None, :]
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
                d2t = (x[:,None] + x[None,:] + sx)**2 \
                    + (y[:,None] - y[None,:] + sy)**2
                d2 = np.minimum(d2, d2t)
        dist = np.sqrt(np.maximum(d2, 0))
        np.fill_diagonal(dist, 1e9)
        W = np.exp(-dist**2 / (2*self.sigma**2))
        np.fill_diagonal(W, 0)
        return W

    def step(self):
        W = self._build_coupling()
        h = W @ self.state
        noise = self.noise_std * np.random.randn(self.N)
        self.state = np.tanh(self.gain * h + noise)
        self.step_count += 1

    def correlation_function(self, n_bins=40):
        """2-point correlation of amplitude by Klein separation (vectorized)."""
        N = self.N
        x = np.array(self.xs); y = np.array(self.ys)
        dx = x[:, None] - x[None, :]
        dy = y[:, None] - y[None, :]
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
                d2t = (x[:,None] + x[None,:] + sx)**2 \
                    + (y[:,None] - y[None,:] + sy)**2
                d2 = np.minimum(d2, d2t)
        dist = np.sqrt(np.maximum(d2, 0))
        corr = self.state[:, None] * self.state[None, :]
        iu = np.triu_indices(N, k=1)
        pairs_d = dist[iu]
        pairs_corr = corr[iu]
        db = np.linspace(0, pairs_d.max(), n_bins+1)
        dm = (db[:-1] + db[1:]) / 2
        xi = np.zeros(n_bins)
        for b in range(n_bins):
            m = (pairs_d >= db[b]) & (pairs_d < db[b+1])
            if m.sum() > 0:
                xi[b] = pairs_corr[m].mean()
        return dm, xi

    def run(self, n_ticks=8000, measure_every=500):
        rows = []
        for t in range(n_ticks):
            self.step()
            if t % measure_every == 0 and t > 0:
                dm, xi = self.correlation_function()
                # FFT of correlation function
                pk = np.abs(np.fft.fft(xi - xi.mean()))
                k = np.fft.fftfreq(len(xi), d=dm[1]-dm[0])
                rows.append({"tick": self.step_count, "dm": dm, "xi": xi,
                             "pk": pk, "k": k})
        return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.perf_counter()
    sub = BalloonSubstrate(N=350, sigma=0.5, gain=2.0)
    rows = sub.run(n_ticks=8000, measure_every=1000)
    print(f"{sub.step_count} ticks in {time.perf_counter()-t0:.0f}s")

    # Find dominant frequencies in the power spectra over time
    print("\ntick   dominant_k   power   ratio_to_phi")
    for r in rows:
        pk = r["pk"]
        k = r["k"]
        pos_k = k[1:len(k)//2]  # positive frequencies
        pos_pk = pk[1:len(pk)//2]
        if len(pos_pk) == 0 or pos_pk.max() == 0: continue
        dom_idx = np.argmax(pos_pk)
        dom_k = abs(pos_k[dom_idx])
        dom_power = pos_pk[dom_idx]
        # Golden frequency on [0, 2pi) spatial scale
        k_golden = 2*np.pi * ALPHA_GOLDEN / (2*np.pi / (dm[1]-dm[0]))
        print(f"  {r['tick']:5d}  {dom_k:8.3f}  {dom_power:6.2f}  "
              f"{abs(dom_k-k_golden)/k_golden:.3f}")

    with open(os.path.join(OUT_DIR, "balloon_waves.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["tick", "dominant_k", "power"])
        for r in rows:
            pk = r["pk"]; k = r["k"]
            pos_k = k[1:len(k)//2]; pos_pk = pk[1:len(pk)//2]
            if len(pos_pk) == 0 or pos_pk.max() == 0: continue
            dom_idx = np.argmax(pos_pk)
            w.writerow([r["tick"], abs(pos_k[dom_idx]), pos_pk[dom_idx]])

    make_figure(rows, sub)
    print(f"Wrote {OUT_DIR}")


def make_figure(rows, sub):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    final = rows[-1]
    ax.plot(final["dm"], final["xi"], "-", color="crimson", lw=2)
    ax.set_xlabel("Klein separation d"); ax.set_ylabel("correlation xi(d)")
    ax.set_title("A. Final correlation function")

    ax = axes[0, 1]
    ax.semilogy(final["k"][:len(final["k"])//2],
                final["pk"][:len(final["pk"])//2], "-",
                color="seagreen", lw=2)
    ax.set_xlabel("spatial frequency k"); ax.set_ylabel("power P(k)")
    ax.set_title("B. Power spectrum (final)")

    ax = axes[1, 0]
    # Track dominant frequency over time
    ts, dom_ks = [], []
    for r in rows:
        pk = r["pk"]; k = r["k"]
        pos_k = k[1:len(k)//2]; pos_pk = pk[1:len(pk)//2]
        if len(pos_pk) == 0 or pos_pk.max() == 0: continue
        dom_idx = np.argmax(pos_pk)
        ts.append(r["tick"]); dom_ks.append(abs(pos_k[dom_idx]))
    ax.plot(ts, dom_ks, "o-", color="steelblue", ms=6)
    # golden frequency reference
    k_g = 2*np.pi * ALPHA_GOLDEN / (2*np.pi/(final["dm"][1]-final["dm"][0]))
    ax.axhline(k_g, color="crimson", ls="--",
               label=f"golden k = {k_g:.2f}")
    ax.set_xlabel("plonk tick"); ax.set_ylabel("dominant k")
    ax.set_title("C. Dominant spatial frequency vs time"); ax.legend(fontsize=8)

    ax = axes[1, 1]
    # scatter of oscillator positions with amplitudes
    sc = ax.scatter(sub.xs, sub.ys, c=sub.state, cmap="RdBu_r",
                    s=8, vmin=-0.5, vmax=0.5)
    fig.colorbar(sc, ax=ax, label="amplitude")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title(f"D. Amplitude field (t={sub.step_count})")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "balloon_waves.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
