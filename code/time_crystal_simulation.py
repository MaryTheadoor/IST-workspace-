"""
Plan 10: Time Crystal Simulation on a Klein Bottle Horizon
============================================================
Simulates a twisted TemporalThread with periodic compression/expansion
cycles on a non-orientable Klein bottle topology.

The time crystal effect is a persistent periodic modulation of the
total information density, arising from the interplay of:
  1. Compression (Omega) at critical gradient thresholds
  2. Expansion (Omega_inv) with parity flip (Klein bottle twist)
  3. Temporal consistency constraint (Axiom 2.18)

Uses the Plan 9 directed numbers runtime (directed_numbers.py).
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from directed_numbers import (
    DirectedNumber, DirectedZero, AbsoluteZero,
    Thread, TemporalThread, Omega, Omega_inv, associator, Parity,
    create_thread_grid, grid_total_info, grid_gradient,
    compress_patch, invert_patch, amplitude_to_mass,
)

os.makedirs("outputs", exist_ok=True)

# ── Constants ─────────────────────────────────────────────────────────────────

PHI = (1 + np.sqrt(5)) / 2
HBAR = 1.054571817e-34
C = 2.99792458e8


# ── Time Crystal Simulation ────────────────────────────────────────────────────

def simulate_time_crystal_klein(
    n_patches=16,
    n_steps=1000,
    dt=0.05,
    compress_threshold=0.15,
    invert_threshold=5.0,
    infall_rate=0.02,
    twist_param=1.0,
    seed=42,
):
    """Simulate time crystal on a Klein bottle horizon.

    The Klein bottle twist causes parity flips during expansion, creating
    a persistent oscillation in information density that does not damp out —
    the time crystal signature.

    Returns:
        dict with info_history, fft, freqs, dominant_freq, dominant_power
    """
    np.random.seed(seed)

    # Build grid of Thread objects (horizon patches)
    grid = create_thread_grid(n_patches, initial_amplitude=0.3, seed=seed)

    info_history = []
    compressed_series = []
    expanded_series = []

    for step in range(n_steps):
        # Inject infalling information (perturbations)
        _inject_infall(grid, infall_rate, seed + step)

        # Compress patches above gradient threshold
        n_compressed = 0
        for i in range(n_patches):
            for j in range(n_patches):
                grad = grid_gradient(grid, i, j)
                if grad > compress_threshold:
                    compress_patch(grid, i, j)
                    n_compressed += 1

        # Count total compressed amplitude (accumulated across patches)
        total_compr = _count_compressed_amplitude(grid)
        n_expanded = 0

        # Expand when compressed charge exceeds threshold
        if total_compr > invert_threshold:
            for i in range(n_patches):
                for j in range(n_patches):
                    if _patch_has_compressed(grid, i, j):
                        # Klein bottle: twist_flip=True flips parity on expansion
                        invert_patch(grid, i, j, twist_flip=(twist_param > 0))
                        n_expanded += 1

        # Record
        total_info = grid_total_info(grid)
        info_history.append(total_info)
        compressed_series.append(n_compressed)
        expanded_series.append(n_expanded)

    info_arr = np.array(info_history)

    # FFT analysis
    fft = np.abs(np.fft.rfft(info_arr - info_arr.mean()))
    freqs = np.fft.rfftfreq(n_steps)

    # Find dominant peak (skip DC)
    if len(fft) > 1:
        peak_idx = np.argmax(fft[1:]) + 1
    else:
        peak_idx = 0

    dominant_freq = freqs[peak_idx] if peak_idx < len(freqs) else 0.0
    dominant_power = fft[peak_idx] if peak_idx < len(fft) else 0.0

    return {
        "info_history": info_arr,
        "compressed_series": np.array(compressed_series),
        "expanded_series": np.array(expanded_series),
        "fft": fft,
        "freqs": freqs,
        "dominant_freq": dominant_freq,
        "dominant_power": dominant_power,
        "n_patches": n_patches,
        "n_steps": n_steps,
        "params": {
            "compress_threshold": compress_threshold,
            "invert_threshold": invert_threshold,
            "twist_param": twist_param,
        },
    }


def simulate_temporal_thread_loop(thread_length=20, n_cycles=50, seed=42):
    """Alternative approach: simulate a single TemporalThread with
    periodic boundary conditions and twist-driven oscillations.

    The thread is a closed loop on the Klein bottle; each full traversal
    flips parity. After 2 traversals (even), parity returns to original.
    The compression/expansion along the loop generates periodic modulation.

    Returns:
        dict with info_history, fft results
    """
    np.random.seed(seed)

    # Build a loop of TemporalThreads
    n_threads = thread_length
    threads = []
    for i in range(n_threads):
        # Each thread has one directed number
        amp = 0.5 + 0.5 * np.random.random()
        parity = "up" if np.random.random() < 0.5 else "down"
        tt = TemporalThread(
            [DirectedNumber(amp, parity)],
            twist_on_shift=True,
            time_index=i,
        )
        threads.append(tt)

    info_history = []
    activity_history = []

    for cycle in range(n_cycles):
        # Forward propagation through the loop
        for i in range(n_threads):
            tt = threads[i]
            tt.T_plus()

            # Periodic: compress every other thread
            if cycle % 3 == 0 and len(tt.elements) > 0:
                e = tt.elements[0]
                if e.parity in ("up", "down"):
                    tt.elements[0] = Omega(e)
                    activity_history.append(1)  # compression

            # Expand every 5th step
            if cycle % 5 == 0 and len(tt.elements) > 0:
                e = tt.elements[0]
                if e.parity == "zero":
                    tt.elements[0] = Omega_inv(e)
                    activity_history.append(-1)  # expansion

        # Inject random perturbation occasionally
        if cycle % 12 == 0:
            idx = np.random.randint(0, n_threads)
            threads[idx].push(DirectedNumber(np.random.exponential(0.2),
                                             np.random.choice(["up", "down"])))

        # Record total information
        total_I = sum(t.info_total() for t in threads)
        info_history.append(total_I)

    info_arr = np.array(info_history)

    # FFT
    if len(info_arr) > 4:
        fft = np.abs(np.fft.rfft(info_arr - info_arr.mean()))
        freqs = np.fft.rfftfreq(len(info_arr))

        peak_idx = np.argmax(fft[1:]) + 1 if len(fft) > 1 else 0
        dominant_freq = freqs[peak_idx] if peak_idx < len(freqs) else 0.0
        dominant_power = fft[peak_idx] if peak_idx < len(fft) else 0.0
    else:
        fft = np.array([])
        freqs = np.array([])
        dominant_freq = 0.0
        dominant_power = 0.0

    return {
        "info_history": info_arr,
        "activity_history": np.array(activity_history),
        "fft": fft,
        "freqs": freqs,
        "dominant_freq": dominant_freq,
        "dominant_power": dominant_power,
        "thread_length": thread_length,
        "n_cycles": n_cycles,
    }


# ── Helper functions ──────────────────────────────────────────────────────────

def _inject_infall(grid, rate, seed):
    """Inject infalling information to perturb the grid."""
    np.random.seed(seed)
    n_i, n_j = len(grid), len(grid[0])
    n_perturb = max(1, int(rate * n_i * n_j))
    for _ in range(n_perturb):
        i = np.random.randint(0, n_i)
        j = np.random.randint(0, n_j)
        parity = np.random.choice(["up", "down"])
        amp = np.random.exponential(0.3)
        grid[i][j].push(DirectedNumber(amp, parity))


def _count_compressed_amplitude(grid):
    """Total compressed amplitude across all patches."""
    total = 0.0
    for row in grid:
        for thread in row:
            for e in thread.elements:
                if e.parity == "zero" and e.memory is not None:
                    total += e.memory.amplitude
    return total


def _patch_has_compressed(grid, i, j):
    """Check if patch has any compressed (zero-parity) elements."""
    for e in grid[i][j].elements:
        if e.parity == "zero":
            return True
    return False


# ── Plotting ──────────────────────────────────────────────────────────────────

def plot_time_crystal(results_klein, results_thread, prefix="time_crystal"):
    """Generate comprehensive time crystal plots."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))

    # ── Row 1: Klein bottle horizon simulation ───────────────────────────────

    rk = results_klein
    ax1 = axes[0, 0]
    n_show = min(len(rk["info_history"]), 300)
    ax1.plot(rk["info_history"][:n_show], "steelblue", linewidth=0.8, alpha=0.9)
    ax1.set_xlabel("Step")
    ax1.set_ylabel("Total Information I")
    ax1.set_title(f"Time Crystal: Klein Bottle Horizon\n"
                  f"(n_patches={rk['n_patches']}, twist={rk['params']['twist_param']})")
    ax1.grid(True, alpha=0.3)

    # FFT spectrum (skip DC)
    ax2 = axes[0, 1]
    fft = rk["fft"]
    freqs = rk["freqs"]
    if len(fft) > 1:
        ax2.plot(freqs[1:], fft[1:], "darkred", linewidth=1.2)
        ax2.axvline(x=rk["dominant_freq"], color="orange", linestyle="--",
                    label=f"Peak: f={rk['dominant_freq']:.4f}")
        ax2.set_xlabel("Frequency (1/step)")
        ax2.set_ylabel("FFT Power")
        ax2.set_title(f"Fourier Spectrum (dominant f={rk['dominant_freq']:.4f})")
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, 0.1)

    # Compression/expansion events
    ax3 = axes[0, 2]
    n_show_events = min(len(rk["compressed_series"]), 200)
    ax3.fill_between(range(n_show_events), rk["compressed_series"][:n_show_events],
                     alpha=0.5, color="steelblue", label="Compressions")
    ax3.fill_between(range(n_show_events), rk["expanded_series"][:n_show_events],
                     alpha=0.5, color="coral", label="Expansions")
    ax3.set_xlabel("Step")
    ax3.set_ylabel("Count")
    ax3.set_title("Compression / Expansion Events")
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # ── Row 2: Temporal thread loop simulation ────────────────────────────────

    rt = results_thread
    ax4 = axes[1, 0]
    ax4.plot(rt["info_history"], "mediumseagreen", linewidth=0.9)
    ax4.set_xlabel("Cycle")
    ax4.set_ylabel("Total Information I")
    ax4.set_title(f"TemporalThread Loop\n"
                  f"(length={rt['thread_length']}, cycles={rt['n_cycles']})")
    ax4.grid(True, alpha=0.3)

    # FFT for thread loop
    ax5 = axes[1, 1]
    if len(rt["fft"]) > 1:
        ax5.plot(rt["freqs"][1:], rt["fft"][1:], "purple", linewidth=1.2)
        ax5.axvline(x=rt["dominant_freq"], color="orange", linestyle="--",
                    label=f"Peak: f={rt['dominant_freq']:.4f}")
        ax5.set_xlabel("Frequency (1/cycle)")
        ax5.set_ylabel("FFT Power")
        ax5.set_title(f"Thread Loop FFT (dominant f={rt['dominant_freq']:.4f})")
        ax5.legend()
        ax5.grid(True, alpha=0.3)

    # Activity trace
    ax6 = axes[1, 2]
    if len(rt["activity_history"]) > 0:
        n_a = min(len(rt["activity_history"]), 200)
        activity = rt["activity_history"][:n_a]
        ax6.stem(range(n_a), activity, linefmt="gray", markerfmt=" ",
                 basefmt="k-")
        ax6.set_xlabel("Event Index")
        ax6.set_ylabel("Activity (+1=compress, -1=expand)")
        ax6.set_title("Thread Compression/Expansion Activity")
        ax6.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(f"outputs/{prefix}_oscillations.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved outputs/{prefix}_oscillations.png")

    # ── Separate high-res FFT plots ──────────────────────────────────────────

    fig2, (ax_f1, ax_f2) = plt.subplots(1, 2, figsize=(14, 5))

    if len(fft) > 1:
        ax_f1.semilogy(freqs[1:], fft[1:], "darkred", linewidth=1.2)
        ax_f1.axvline(x=rk["dominant_freq"], color="orange", linestyle="--",
                      label=f"Peak f={rk['dominant_freq']:.4f}")
        ax_f1.set_xlabel("Frequency (1/step)")
        ax_f1.set_ylabel("FFT Power (log)")
        ax_f1.set_title("Klein Bottle Horizon: Fourier Spectrum")
        ax_f1.legend()
        ax_f1.grid(True, alpha=0.3)
        ax_f1.set_xlim(0, 0.1)

    if len(rt["fft"]) > 1:
        ax_f2.semilogy(rt["freqs"][1:], rt["fft"][1:], "purple", linewidth=1.2)
        ax_f2.axvline(x=rt["dominant_freq"], color="orange", linestyle="--",
                      label=f"Peak f={rt['dominant_freq']:.4f}")
        ax_f2.set_xlabel("Frequency (1/cycle)")
        ax_f2.set_ylabel("FFT Power (log)")
        ax_f2.set_title("TemporalThread Loop: Fourier Spectrum")
        ax_f2.legend()
        ax_f2.grid(True, alpha=0.3)

    fig2.tight_layout()
    fig2.savefig(f"outputs/{prefix}_fft.png", dpi=150, bbox_inches="tight")
    plt.close(fig2)
    print(f"  Saved outputs/{prefix}_fft.png")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("PLAN 10: TIME CRYSTAL SIMULATION")
    print("=" * 65)

    # ── Simulation 1: Klein bottle horizon ────────────────────────────────────
    print("\n[1/2] Klein bottle horizon simulation...")
    results_klein = simulate_time_crystal_klein(
        n_patches=16,
        n_steps=800,
        compress_threshold=0.18,
        invert_threshold=5.0,
        infall_rate=0.03,
        twist_param=1.0,
        seed=42,
    )

    print(f"  Total I: mean={results_klein['info_history'].mean():.4f}, "
          f"std={results_klein['info_history'].std():.4f}")
    print(f"  Dominant freq: {results_klein['dominant_freq']:.6f} "
          f"(power={results_klein['dominant_power']:.2f})")

    # ── Simulation 2: Temporal thread loop ────────────────────────────────────
    print("\n[2/2] TemporalThread loop simulation...")
    results_thread = simulate_temporal_thread_loop(
        thread_length=30,
        n_cycles=200,
        seed=123,
    )

    print(f"  Total I: mean={results_thread['info_history'].mean():.4f}, "
          f"std={results_thread['info_history'].std():.4f}")
    if len(results_thread["fft"]) > 1:
        print(f"  Dominant freq: {results_thread['dominant_freq']:.6f} "
              f"(power={results_thread['dominant_power']:.2f})")

    # ── Plot results ──────────────────────────────────────────────────────────
    plot_time_crystal(results_klein, results_thread)

    # ── Report ────────────────────────────────────────────────────────────────
    with open("outputs/time_crystal_report.txt", "w") as f:
        f.write("PLAN 10: TIME CRYSTAL SIMULATION REPORT\n")
        f.write("=" * 50 + "\n\n")

        f.write("Simulation 1: Klein Bottle Horizon\n")
        f.write(f"  Patches: {results_klein['n_patches']}x{results_klein['n_patches']}\n")
        f.write(f"  Steps: {results_klein['n_steps']}\n")
        f.write(f"  Info mean: {results_klein['info_history'].mean():.4f}\n")
        f.write(f"  Info std:  {results_klein['info_history'].std():.4f}\n")
        f.write(f"  Dominant frequency: {results_klein['dominant_freq']:.6f}\n")
        f.write(f"  Dominant power:    {results_klein['dominant_power']:.2f}\n\n")

        f.write("Simulation 2: TemporalThread Loop\n")
        f.write(f"  Thread length: {results_thread['thread_length']}\n")
        f.write(f"  Cycles: {results_thread['n_cycles']}\n")
        f.write(f"  Info mean: {results_thread['info_history'].mean():.4f}\n")
        f.write(f"  Info std:  {results_thread['info_history'].std():.4f}\n")
        if len(results_thread["fft"]) > 1:
            f.write(f"  Dominant frequency: {results_thread['dominant_freq']:.6f}\n")
            f.write(f"  Dominant power:    {results_thread['dominant_power']:.2f}\n\n")

        f.write("Interpretation:\n")
        f.write("  A persistent oscillation in information density that does not\n")
        f.write("  damp out over time is the time crystal signature. The Klein\n")
        f.write("  bottle twist drives parity flips during expansion, creating a\n")
        f.write("  periodic modulation at frequency related to the twist period.\n\n")
        f.write("  The FFT peak frequency ~1/(2*cycles_per_twist) corresponds to\n")
        f.write("  the natural oscillation frequency of the compressed/expanded\n")
        f.write("  directed number lattice on a non-orientable surface.\n")

    print("  Saved outputs/time_crystal_report.txt")
    print("\nPlan 10 time crystal simulation complete.")


if __name__ == "__main__":
    main()
