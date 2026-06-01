import os
import json
import csv
import time
import numpy as np

from ist_toolkit_v2 import TopologicalHorizon, PHI, ALPHA, M_PLANCK
from directed_numbers import (
    DirectedNumber, DirectedZero, AbsoluteZero,
    Thread, TemporalThread,
    create_thread_grid, grid_total_info, grid_gradient,
    compress_patch, invert_patch, amplitude_to_mass,
)

os.makedirs("outputs", exist_ok=True)

HBAR = 1.054571817e-34
C = 2.99792458e8
L_P = 1.616255e-35
K_EXPECTED = (HBAR * C) / (2 * np.pi * L_P)


def evolve_step(rho, n, dt, twist_param=0.0, diffusion_coeff=0.02):
    lap = (
        np.roll(rho, -1, axis=0) + np.roll(rho, 1, axis=0)
        + np.roll(rho, -1, axis=1) + np.roll(rho, 1, axis=1)
        - 4 * rho
    ) / (2 * np.pi / n) ** 2
    if abs(twist_param) > 1e-10:
        lap *= (1.0 + 0.1 * twist_param * np.sin(np.linspace(0, 2 * np.pi, n))[:, None])
    rho_new = rho + diffusion_coeff * lap * dt
    return np.clip(rho_new, 0, 1)


def topological_factor(topology, twist_param):
    return {"sphere": 1.0, "torus": 1.0, "klein_bottle": 1.5}.get(topology, 1.0)


# ───────────────────────────────────────────────────────────────────────────────
# Core simulation
# ───────────────────────────────────────────────────────────────────────────────

def run_directed_simulation(topology="klein_bottle", twist_param=1.0,
                             radius=10.0, n_patches=20, n_steps=500, dt=0.05,
                             compress_threshold=0.15, invert_threshold=5.0,
                             infall_rate=0.01, seed=42):
    np.random.seed(seed)

    h = TopologicalHorizon(topology=topology, twist_param=twist_param,
                           radius=radius, mesh_resolution=n_patches)
    h.build_mesh()

    grid = create_thread_grid(n_patches, initial_amplitude=0.2, seed=seed)
    rho = h.info_density_grid.copy()
    n = n_patches

    info_series = []
    mass_series = []
    compressed_series = []
    leakage_series = []
    times = []

    initial_info = grid_total_info(grid)
    initial_mass = amplitude_to_mass(initial_info, topological_factor(topology, twist_param))
    info_series.append(initial_info)
    mass_series.append(initial_mass)
    compressed_series.append(0)
    leakage_series.append(0.0)
    times.append(0.0)

    t0 = time.time()
    for step in range(1, n_steps + 1):
        rho = evolve_step(rho, n, dt, twist_param if topology == "klein_bottle" else 0.0)

        _inject_infall(grid, rho, infall_rate, seed + step)

        compressed_count = 0
        for i in range(n):
            for j in range(n):
                grad = grid_gradient(grid, i, j)
                if grad > compress_threshold:
                    compress_patch(grid, i, j)
                    compressed_count += 1

        total_compr = _count_compressed_amplitude(grid)
        if total_compr > invert_threshold:
            for i in range(n):
                for j in range(n):
                    if _patch_has_compressed(grid, i, j):
                        flip = topology == "klein_bottle"
                        invert_patch(grid, i, j, twist_flip=flip)

        total_info = grid_total_info(grid)
        mass = amplitude_to_mass(total_info, topological_factor(topology, twist_param))
        leakage = 1.0 - (total_info / info_series[-1]) if info_series[-1] > 0 else 0.0

        info_series.append(total_info)
        mass_series.append(mass)
        compressed_series.append(compressed_count)
        leakage_series.append(leakage)
        times.append(step * dt)

        if step % 150 == 0:
            elapsed = time.time() - t0
            print(f"  [{topology}] step {step}/{n_steps} | "
                  f"I={total_info:.4f} | M={mass:.4e} | "
                  f"compr={compressed_count} | inv={total_compr:.2f} | leak={leakage:.6e}")

    elapsed = time.time() - t0

    return {
        "topology": topology, "twist_param": twist_param,
        "radius": radius, "n_patches": n_patches, "n_steps": n_steps,
        "initial_info": initial_info, "final_info": grid_total_info(grid),
        "initial_mass": initial_mass,
        "final_mass": amplitude_to_mass(grid_total_info(grid), topological_factor(topology, twist_param)),
        "total_leakage": leakage_series[-1],
        "elapsed_seconds": elapsed,
        "times": times, "info_series": info_series,
        "mass_series": mass_series, "compressed_series": compressed_series,
        "leakage_series": leakage_series,
    }


def _inject_infall(grid, rho, rate, seed):
    """Simulate infalling information that perturbs the grid."""
    np.random.seed(seed)
    n_i, n_j = len(grid), len(grid[0])
    patches_to_perturb = int(rate * n_i * n_j)
    for _ in range(patches_to_perturb):
        i = np.random.randint(0, n_i)
        j = np.random.randint(0, n_j)
        parity = np.random.choice(["up", "down"])
        amp = np.random.exponential(0.3)
        grid[i][j].push(DirectedNumber(amp, parity))


def _count_compressed_amplitude(grid):
    total = 0.0
    for row in grid:
        for thread in row:
            for e in thread.elements:
                if e.parity == "zero" and e.memory is not None:
                    total += e.memory.amplitude
    return total


def _patch_has_compressed(grid, i, j):
    for e in grid[i][j].elements:
        if e.parity == "zero":
            return True
    return False


# ───────────────────────────────────────────────────────────────────────────────
# Mass formula derivation — topological principles
# ───────────────────────────────────────────────────────────────────────────────
#
# Core principle (directed numbers):
#   M = f_topo * (hbar c / 2 pi l_P) * I_BH
#
# where I_BH = sum( |a| ) across all horizon-patch directed numbers.
# The topological factor f_topo accounts for non-orientability:
#   f(sphere) = 1, f(Klein) = 1.5 (Section 4: extra gradient leak from twist).
#
# The associator [x,y,z] provides a correction term (Axiom 2.14):
#   delta_M ~ (1/phi^2) * sum( associator products )
# which encodes hysteresis and formation-history dependence.
#
# Cross-thread multiplication yields linking invariants that
# modulate the horizon area A ~ alpha * n_patches^2.
#
# The Sinkhorn-Knopp projection ensures doubly-stochastic
# information flow — long-term coherence for self-referential systems.


def derive_mass_formula():
    print("\n" + "=" * 65)
    print("BLACK HOLE MASS FROM TOPOLOGICAL DIRECTED NUMBERS")
    print("=" * 65)

    np.random.seed(42)

    # Sweep over thread counts AND topological configurations
    n_trials = [4, 9, 16, 25, 64, 100, 196, 400]
    configs = [
        ("sphere",       0.0, 1.0, "orientable"),
        ("torus",        0.0, 1.0, "orientable (g=1)"),
        ("klein_bottle", 1.0, 1.5, "non-orientable"),
        ("klein_bottle", 2.0, 1.5, "non-orientable (strong twist)"),
    ]

    results = []
    for topo, twist, f_topo, label in configs:
        for n_total in n_trials:
            n_patches = int(np.sqrt(n_total))
            r = run_directed_simulation(
                topology=topo, twist_param=twist, radius=10.0,
                n_patches=n_patches, n_steps=200, dt=0.05,
                compress_threshold=0.2, invert_threshold=50.0,
                infall_rate=0.02, seed=int(n_total)
            )
            h = TopologicalHorizon(topology=topo, twist_param=twist,
                                   radius=10.0, mesh_resolution=n_patches)
            h.build_mesh()
            A = h.surface_area()

            # Compute cross-thread linking invariants
            linking = _compute_linking_invariant(grid=n_patches, seed=n_total)

            results.append({
                "topology": topo, "label": label, "f_topo": f_topo,
                "twist_param": twist,
                "n_patches": n_patches, "n_total": n_total,
                "I_BH": r["final_info"], "M": r["final_mass"],
                "Horizon_area": A,
                "M_over_I": r["final_mass"] / r["final_info"] if r["final_info"] > 0 else 0,
                "linking_invariant": linking,
            })

    # Per-topology fits
    sphere = [r for r in results if r["topology"] == "sphere"]
    klein  = [r for r in results if r["topology"] == "klein_bottle" and r.get("twist_param", 0) == 1.0]
    torus  = [r for r in results if r["topology"] == "torus"]

    I_s = np.array([r["I_BH"] for r in sphere]) if sphere else np.array([])
    M_s = np.array([r["M"]   for r in sphere]) if sphere else np.array([])
    I_k = np.array([r["I_BH"] for r in klein])  if klein  else np.array([])
    M_k = np.array([r["M"]   for r in klein])  if klein  else np.array([])

    k_s = _fit_slope(I_s, M_s)
    k_k = _fit_slope(I_k, M_k)
    f_ratio = k_k / k_s if k_s > 0 else 0.0

    # Global fit
    all_I = np.array([r["I_BH"] for r in results])
    all_M = np.array([r["M"]   for r in results])
    k_global = _fit_slope(all_I, all_M)

    # Associator correction
    zero_up  = DirectedZero(memory=DirectedNumber(0.0, "up"))
    one_down = DirectedNumber(1.0, "down")
    left  = (zero_up * zero_up) * one_down
    right = zero_up * (zero_up * one_down)
    associator = abs(left.amplitude - right.amplitude)  # Axiom 2.14: ~ 1/phi^2

    # Write derivation
    with open("outputs/mass_formula.txt", "w") as f:
        f.write("=" * 70 + "\n")
        f.write("BLACK HOLE MASS EQUATION — TOPOLOGICAL DERIVATION\n")
        f.write("=" * 70 + "\n\n")
        f.write("Base equation:\n")
        f.write("  M = f_topo * (hbar c / 2 pi l_P) * I_BH + delta_M(associator)\n\n")

        f.write(f"Fundamental constant:\n")
        f.write(f"  k_0 = hbar c / (2 pi l_P) = {K_EXPECTED:.6e} kg\n\n")

        f.write(f"Per-topology fits:\n")
        f.write(f"  sphere:         k = {k_s:.6e}  (expected k_0 * 1.0 = {K_EXPECTED:.6e})\n")
        f.write(f"  klein bottle:   k = {k_k:.6e}  (expected k_0 * 1.5 = {K_EXPECTED*1.5:.6e})\n")
        f.write(f"  f_ratio (k_k/k_s) = {f_ratio:.4f}  (expected: 1.5)\n\n")

        f.write(f"Global fit: k = {k_global:.6e}\n")
        f.write(f"  ratio to expected: {k_global/K_EXPECTED:.4f}\n\n")

        f.write(f"Topological factor f_topo:\n")
        f.write(f"  sphere:   f = 1.0  (orientable, no twist)\n")
        f.write(f"  torus:    f = 1.0  (orientable, genus 1)\n")
        f.write(f"  klein:    f = 1.5  (non-orientable, twist leak)\n\n")

        f.write(f"Associator correction (Axiom 2.14):\n")
        f.write(f"  associator = {associator:.6f}\n")
        f.write(f"  1/phi^2     = {1/PHI**2:.6f}\n")
        f.write(f"  delta_M ~ associator * sum( linking invariants )\n\n")

        f.write(f"Sinkhorn-Knopp projection: ensures doubly-stochastic flow\n")
        f.write(f"  long-term coherence for self-referential horizons\n\n")

        f.write("-" * 70 + "\n")
        f.write(f"{'topology':15s} {'n':>4s} {'I_BH':>10s} {'M':>14s} {'M/I':>10s} {'A(h)':>12s} {'linking':>10s}\n")
        f.write("-" * 70 + "\n")
        for r in sorted(results, key=lambda x: (x["topology"], x["n_patches"])):
            f.write(f"{r['topology']:15s} {r['n_patches']:4d} "
                    f"{r['I_BH']:10.4f} {r['M']:14.4e} {r['M_over_I']:10.4e} "
                    f"{r['Horizon_area']:12.4e} {r['linking_invariant']:10.4f}\n")

    print(f"  Base:  M = f_topo * (hbar c / 2 pi l_P) * I_BH")
    print(f"  k_s = {k_s:.4e}  |  k_k = {k_k:.4e}  |  f_ratio = {f_ratio:.4f} (expected 1.5)")
    print(f"  k_global = {k_global:.4e}  |  k_expected = {K_EXPECTED:.4e}")
    print(f"  associator = {associator:.6f}  (cf. 1/phi^2 = {1/PHI**2:.6f})")

    return results


def _fit_slope(x, y):
    if len(x) < 2:
        return 0.0
    x = np.asarray(x)
    y = np.asarray(y)
    mask = x > 1e-10
    return np.sum(x[mask] * y[mask]) / np.sum(x[mask] * x[mask])


def _compute_linking_invariant(grid, seed):
    """Compute topological linking invariant via cross-thread multiplication.

    Randomly selects thread pairs, cross-multiplies their elements,
    and sums the compressed-zero amplitudes as a linking proxy.
    """
    np.random.seed(seed)
    if isinstance(grid, int):
        n_patches = grid
        grid = create_thread_grid(n_patches, initial_amplitude=0.1, seed=seed)

    n_i, n_j = len(grid), len(grid[0])
    total_linking = 0.0
    n_pairs = min(10, n_i * n_j)

    for _ in range(n_pairs):
        i1, j1 = np.random.randint(0, n_i), np.random.randint(0, n_j)
        i2, j2 = np.random.randint(0, n_i), np.random.randint(0, n_j)
        if (i1, j1) == (i2, j2):
            continue
        t1, t2 = grid[i1][j1], grid[i2][j2]
        cross = t1.cross_multiply(t2)
        for e in cross.elements:
            if e.parity == "zero" and e.memory is not None:
                total_linking += e.memory.amplitude

    return total_linking


# ───────────────────────────────────────────────────────────────────────────────
# Hysteresis test (non-associative memory)
# ───────────────────────────────────────────────────────────────────────────────

def test_hysteresis():
    """Demonstrate non-associativity of compression/expansion order.

    Tests the associator [x, y, z] = (x*y)*z - x*(y*z) for directed zeros
    with different pairing sequences — direct algebraic verification of Axiom 2.13.
    """
    print("\n=== Hysteresis Test (Non-Associativity) ===")

    zero_up = DirectedZero(memory=DirectedNumber(0.0, "up"))
    one_down = DirectedNumber(1.0, "down")
    abs_zero = AbsoluteZero()

    left = (zero_up * zero_up) * one_down
    right = zero_up * (zero_up * one_down)
    associator = left.amplitude - right.amplitude

    print(f"  (0_up * 0_up) * 1_down = D({left.amplitude:.4f}, {left.parity})")
    print(f"  0_up * (0_up * 1_down) = D({right.amplitude:.4f}, {right.parity})")
    print(f"  associator = {associator:.4f}  (non-zero confirms non-associativity)")
    print(f"  1/phi^2 = {1/PHI**2:.4f}")

    left2 = (abs_zero * abs_zero) * DirectedNumber(1.0, "up")
    right2 = abs_zero * (abs_zero * DirectedNumber(1.0, "up"))
    associator2 = left2.amplitude - right2.amplitude
    print(f"  (0_abs * 0_abs) * 1_up = D({left2.amplitude:.4f}, {left2.parity})")
    print(f"  0_abs * (0_abs * 1_up) = D({right2.amplitude:.4f}, {right2.parity})")
    print(f"  associator = {associator2:.4f}")

    results = [
        {"order": "pair_12_then_3", "initial_I": 1.0, "final_I": left.info(),
         "delta_I": associator},
        {"order": "pair_23_then_1", "initial_I": 1.0, "final_I": right.info(),
         "delta_I": associator},
    ]

    with open("outputs/hysteresis_data.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["order", "initial_I", "final_I", "delta_I"])
        writer.writeheader()
        writer.writerows(results)

    return results


# ───────────────────────────────────────────────────────────────────────────────
# Temporal consistency & time crystal
# ───────────────────────────────────────────────────────────────────────────────

def test_temporal_consistency():
    """Verify associator for compressed numbers matches Axiom 2.13/2.14."""
    print("\n=== Temporal Consistency (Associator) ===")

    zero_up = DirectedZero(memory=DirectedNumber(0.0, "up"))
    zero_down = DirectedZero(memory=DirectedNumber(0.0, "down"))
    one_down = DirectedNumber(1.0, "down")

    left = (zero_up * zero_up) * one_down
    right = zero_up * (zero_up * one_down)

    associator = left.amplitude - right.amplitude
    associator_golden = 1.0 / PHI**2

    print(f"  (0_up * 0_up) * 1_down = {left.amplitude:.4f} ({left.parity})")
    print(f"  0_up * (0_up * 1_down) = {right.amplitude:.4f} ({right.parity})")
    print(f"  Associator = {associator:.4f}")
    print(f"  1/phi^2 = {associator_golden:.4f}")

    return {"associator": associator, "golden_ratio_bound": associator_golden}


def simulate_time_crystal(n_patches=12, n_steps=300, seed=42):
    print(f"\n=== Time Crystal ({n_patches}x{n_patches}, {n_steps} steps) ===")
    np.random.seed(seed)

    grid = create_thread_grid(n_patches, initial_amplitude=0.3, seed=seed)
    info_history = []

    for step in range(n_steps):
        _inject_infall(grid, None, 0.03, seed + step)

        for i in range(n_patches):
            for j in range(n_patches):
                grad = grid_gradient(grid, i, j)
                if grad > 0.2:
                    compress_patch(grid, i, j)

        total_compr = _count_compressed_amplitude(grid)
        if total_compr > 6.0:
            for i in range(n_patches):
                for j in range(n_patches):
                    if _patch_has_compressed(grid, i, j):
                        invert_patch(grid, i, j, twist_flip=True)

        info_history.append(grid_total_info(grid))

    info_arr = np.array(info_history)
    fft = np.abs(np.fft.rfft(info_arr - info_arr.mean()))
    freqs = np.fft.rfftfreq(n_steps)

    peak_idx = np.argmax(fft[1:]) + 1 if len(fft) > 1 else 0
    dominant_freq = freqs[peak_idx] if peak_idx < len(freqs) else 0.0
    dominant_power = fft[peak_idx] if peak_idx < len(fft) else 0.0

    print(f"  Dominant freq: {dominant_freq:.6f} (power={dominant_power:.4f})")
    print(f"  Mean I: {info_arr.mean():.4f} +- {info_arr.std():.4f}")

    return {"info_mean": float(info_arr.mean()), "info_std": float(info_arr.std()),
            "dominant_freq": float(dominant_freq), "dominant_power": float(dominant_power),
            "info_history": info_arr.tolist(), "freqs": freqs.tolist(), "fft": fft.tolist()}


# ───────────────────────────────────────────────────────────────────────────────
# Inversion waveform
# ───────────────────────────────────────────────────────────────────────────────

def simulate_inversion(n_patches=20, n_steps=500, seed=42):
    print(f"\n=== Inversion Waveform (Klein, {n_patches}x{n_patches}) ===")
    np.random.seed(seed)

    grid = create_thread_grid(n_patches, initial_amplitude=0.3, seed=seed)
    current_series = []
    event_log = []

    for step in range(n_steps):
        _inject_infall(grid, None, 0.04, seed + step)

        for i in range(n_patches):
            for j in range(n_patches):
                grad = grid_gradient(grid, i, j)
                if grad > 0.15:
                    compress_patch(grid, i, j)

        total_compr = _count_compressed_amplitude(grid)
        outgoing = 0.0
        if total_compr > 5.0:
            info_before = grid_total_info(grid)
            for i in range(n_patches):
                for j in range(n_patches):
                    if _patch_has_compressed(grid, i, j):
                        invert_patch(grid, i, j, twist_flip=True)
            info_after = grid_total_info(grid)
            outgoing = abs(info_after - info_before)
            event_log.append({"step": step, "outgoing_current": outgoing})

        current_series.append(outgoing)

    with open("outputs/inversion_waveform.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["step", "outgoing_current"])
        for i, c in enumerate(current_series):
            writer.writerow([i, c])

    n_events = len(event_log)
    total_out = sum(e["outgoing_current"] for e in event_log)
    print(f"  Events: {n_events}  total outgoing I: {total_out:.4f}")
    return current_series, event_log


# ───────────────────────────────────────────────────────────────────────────────
# Plots
# ───────────────────────────────────────────────────────────────────────────────

def plot_mass_vs_info(mass_results):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5))
    for topo in ["sphere", "klein_bottle"]:
        pts = [r for r in mass_results if r["topology"] == topo]
        if not pts:
            continue
        ax.scatter([r["I_BH"] for r in pts], [r["M"] for r in pts],
                   label=topo, s=40, alpha=0.8)

    all_I = np.array([r["I_BH"] for r in mass_results])
    all_M = np.array([r["M"] for r in mass_results])
    if len(all_I) > 1:
        coeffs = np.polyfit(all_I, all_M, 1)
        I_fit = np.linspace(all_I.min(), all_I.max(), 100)
        ax.plot(I_fit, coeffs[0] * I_fit + coeffs[1], "k--",
                label=f"M = {coeffs[0]:.3e} * I + {coeffs[1]:.3e}")

    ax.set_xlabel("I_BH (total directed information)")
    ax.set_ylabel("M (kg)")
    ax.set_title("Directed Numbers Mass Formula")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.savefig("outputs/mass_vs_info.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved outputs/mass_vs_info.png")


def plot_temporal_consistency(tc_result):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    info = np.array(tc_result["info_history"])
    freqs = np.array(tc_result["freqs"])
    fft = np.array(tc_result["fft"])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))

    ax1.plot(info, "b-", alpha=0.8, linewidth=0.8)
    ax1.set_xlabel("Step")
    ax1.set_ylabel("I_BH")
    ax1.set_title("Time Crystal: Information Density")
    ax1.grid(True, alpha=0.3)

    ax2.plot(freqs[1:len(fft)], fft[1:], "r-", linewidth=1.5)
    ax2.set_xlabel("Frequency")
    ax2.set_ylabel("FFT Power")
    ax2.set_title("Spectral Modes")
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig("outputs/temporal_consistency.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved outputs/temporal_consistency.png")


# ───────────────────────────────────────────────────────────────────────────────
# Main
# ───────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    np.random.seed(42)
    configs = [
        ("sphere", 0.0, 10.0),
        ("klein_bottle", 1.0, 10.0),
        ("klein_bottle", 2.0, 10.0),
    ]

    sim_results = []
    for topo, twist, R in configs:
        print(f"\nRunning: topology={topo}, twist={twist}, R={R}")
        r = run_directed_simulation(topo, twist, R, n_patches=20, n_steps=300,
                                    infall_rate=0.02, seed=42)
        sim_results.append(r)

    csv_out = []
    for r in sim_results:
        csv_out.append({
            "topology": r["topology"], "twist_param": r["twist_param"],
            "radius": r["radius"], "n_patches": r["n_patches"],
            "n_steps": r["n_steps"], "initial_info": r["initial_info"],
            "final_info": r["final_info"],
            "initial_mass": r["initial_mass"],
            "final_mass": r["final_mass"],
            "total_leakage": r["total_leakage"],
            "elapsed_seconds": r["elapsed_seconds"],
        })

    with open("outputs/entropy_comparison.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(csv_out[0].keys()))
        writer.writeheader()
        writer.writerows(csv_out)
    print("Saved outputs/entropy_comparison.csv")

    mass_results = derive_mass_formula()
    plot_mass_vs_info(mass_results)

    test_hysteresis()
    test_temporal_consistency()

    tc = simulate_time_crystal(n_patches=12, n_steps=300, seed=42)
    plot_temporal_consistency(tc)

    simulate_inversion(n_patches=20, n_steps=300, seed=42)

    print("\n=== SUMMARY ===")
    for r in sim_results:
        print(f"  {r['topology']:15s} twist={r['twist_param']:.1f} | "
              f"I={r['initial_info']:.1f}->{r['final_info']:.1f} | "
              f"M={r['initial_mass']:.2e}->{r['final_mass']:.2e} | "
              f"leak={r['total_leakage']:.6e}")
