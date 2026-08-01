"""
================================================================================
IST PHASE 20 — Klein Standing Waves: Temporal Amplitude Selection
================================================================================
Test Mary's insight: ripples on the 2D Klein surface propagate in a
closed loop (inside -> outside -> inside via the twist). Coherent
waves (golden-ratio frequencies) survive the full cycle; incoherent
waves destructively interfere and decay to noise.

The simulation: Phase 10/11 vector substrate on the Klein grid running
for many plonk ticks. Measure the 2D Fourier power spectrum of the
amplitude field. The dominant frequency ratios among surviving modes
should cluster around phi and the golden family.

Output: code/outputs/phase20/standing_waves.png
        code/outputs/phase20/fourier_modes.csv
================================================================================
"""
import csv, os, time
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase20")


class KleinStandingWaves:
    """2D vector substrate on Klein bottle, tracked over long timescales
    to measure standing wave patterns and Fourier mode selection."""

    def __init__(self, n=96, gain=1.3, noise_std=0.015, seed=42):
        self.n = n; self.N = n * n
        self.gain = gain; self.noise_std = noise_std
        rng = np.random.default_rng(seed)
        self.state = rng.random((n, n, 3)) * 0.5
        self.step_count = 0

    def step(self):
        s = self.state; n = self.n
        up, dn, zr = s[:,:,0], s[:,:,1], s[:,:,2]

        def neigh(x):
            hx = np.zeros_like(x)
            hx += np.roll(x, -1, axis=1) + np.roll(x, 1, axis=1)
            hx[:-1] += x[1:]; hx[1:] += x[:-1]
            hx[-1] += -x[0, ::-1]; hx[0] += -x[-1, ::-1]
            return hx

        g = self.gain / 4.0; cr = 0.25
        h_up = neigh(up) + cr * neigh(-dn)
        h_dn = neigh(dn) + cr * neigh(-up)
        h_zr = neigh(zr) + cr * neigh(up * dn)

        ns = self.noise_std * np.random.randn(n, n, 3)
        self.state[:,:,0] = np.tanh(g * h_up + ns[:,:,0])
        self.state[:,:,1] = np.tanh(g * h_dn + ns[:,:,1])
        self.state[:,:,2] = np.tanh(g * h_zr + ns[:,:,2])
        self.step_count += 1

    def fourier_power(self):
        """2D FFT power spectrum of the amplitude field. Returns radial
        average P(k) where k is the spatial frequency magnitude."""
        amp = np.sqrt(np.sum(self.state**2, axis=-1))
        ft = np.abs(np.fft.fftshift(np.fft.fft2(amp)))
        n = self.n
        ky, kx = np.mgrid[-n//2:n//2, -n//2:n//2]
        k = np.sqrt(kx**2 + ky**2).astype(int)
        k_max = n // 2
        pk = np.zeros(k_max)
        for ki in range(1, k_max):
            pk[ki] = ft[k == ki].mean()
        return pk

    def peak_ratios(self, pk, n_peaks=8):
        """Find the top n_peaks in the power spectrum and compute
        frequency ratios between consecutive peaks."""
        from scipy.signal import find_peaks
        peaks, props = find_peaks(pk, height=pk.max()*0.05, distance=2)
        if len(peaks) < 2:
            return np.array([]), np.array([])
        order = np.argsort(-pk[peaks])[:n_peaks]
        top_peaks = peaks[order]
        top_peaks = np.sort(top_peaks)
        ratios = top_peaks[1:] / top_peaks[:-1]
        return top_peaks, ratios

    def run_and_measure(self, n_ticks=5000, measure_every=200):
        records = []
        for t in range(n_ticks):
            self.step()
            if t % measure_every == 0 and t > 0:
                pk = self.fourier_power()
                peaks, ratios = self.peak_ratios(pk)
                records.append({
                    "tick": self.step_count,
                    "n_peaks": len(peaks),
                    "peak_ratios": ratios,
                    "peak_positions": peaks,
                    "mean_ratio": ratios.mean() if len(ratios) > 0 else np.nan,
                })
        return records


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("Running Klein standing wave simulation (5000 ticks)...")
    t0 = time.perf_counter()
    sub = KleinStandingWaves(n=96, gain=1.4, noise_std=0.012)
    records = sub.run_and_measure(n_ticks=5000)

    print(f"  {sub.step_count} ticks in {time.perf_counter()-t0:.0f}s")

    # Collect all peak ratios from late-time records
    late = [r for r in records if r["tick"] > sub.step_count * 0.5]
    all_ratios = np.concatenate([r["peak_ratios"] for r in late
                                  if len(r["peak_ratios"]) > 0])

    # Final power spectrum
    pk_final = sub.fourier_power()
    peaks_final, ratios_final = sub.peak_ratios(pk_final)

    print(f"\nFinal Fourier modes: n_peaks={len(peaks_final)}")
    print(f"Peak positions (k): {peaks_final}")
    print(f"Peak ratios: {[round(r,3) for r in ratios_final]}")
    print(f"Golden ratio phi: {PHI:.3f}")
    if len(all_ratios) > 0:
        print(f"All late-time ratios: mean={all_ratios.mean():.3f} "
              f"std={all_ratios.std():.3f}")
        closeness = sorted(all_ratios, key=lambda r: abs(r-PHI))[:3]
        print(f"Closest ratios to phi: {[round(r,3) for r in closeness]}")

    with open(os.path.join(OUT_DIR, "fourier_modes.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["tick", "n_peaks", "peak_positions", "peak_ratios",
                     "mean_ratio"])
        for r in records:
            w.writerow([r["tick"], r["n_peaks"],
                       ",".join(map(str, r["peak_positions"])),
                       ",".join(f"{x:.3f}" for x in r["peak_ratios"]),
                       r["mean_ratio"]])

    make_figure(records, pk_final, peaks_final, ratios_final, all_ratios)
    print(f"Wrote {OUT_DIR}")


def make_figure(records, pk, peaks, ratios, all_ratios):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    ks = np.arange(len(pk))
    ax.semilogy(ks[1:], pk[1:], "-", color="crimson", lw=2)
    ax.plot(peaks, pk[peaks], "o", color="seagreen", ms=8,
            label=f"{len(peaks)} peaks")
    ax.set_xlabel("spatial frequency k"); ax.set_ylabel("power P(k)")
    ax.set_title("A. Final Fourier power spectrum"); ax.legend(fontsize=8)

    ax = axes[0, 1]
    ts = [r["tick"] for r in records]
    ns = [r["n_peaks"] for r in records]
    ax.plot(ts, ns, "o-", color="steelblue", ms=4)
    ax.set_xlabel("plonk tick"); ax.set_ylabel("n peaks")
    ax.set_title("B. Mode count vs time")

    ax = axes[1, 0]
    if len(all_ratios) > 0:
        ax.hist(all_ratios, bins=25, color="seagreen", alpha=0.7,
                label=f"all ratios (n={len(all_ratios)})")
        ax.axvline(PHI, color="crimson", ls="--", lw=2,
                   label=f"phi = {PHI:.3f}")
        ax.axvline(1/PHI, color="gray", ls=":", label=f"1/phi = {1/PHI:.3f}")
        ax.axvline(PHI**2, color="steelblue", ls=":", label=f"phi^2 = {PHI**2:.1f}")
    ax.set_xlabel("frequency ratio"); ax.set_ylabel("count")
    ax.set_title("C. Peak frequency ratios (late-time)"); ax.legend(fontsize=7)

    ax = axes[1, 1]
    means = [r["mean_ratio"] for r in records if not np.isnan(r["mean_ratio"])]
    if means:
        t_means = [r["tick"] for r in records if not np.isnan(r["mean_ratio"])]
        ax.plot(t_means, means, "o-", color="crimson", ms=4)
        ax.axhline(PHI, color="gray", ls="--", label=f"phi")
    ax.set_xlabel("plonk tick"); ax.set_ylabel("mean peak ratio")
    ax.set_title("D. Mean ratio vs time"); ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "standing_waves.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
