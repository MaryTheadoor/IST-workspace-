"""
Plan 11.5 — Phase 2B: Directed Numbers Cosmological Simulation
===============================================================
Bridges the Plan 9 directed numbers runtime to cosmological observables.

Builds a 3D grid of TemporalThread objects, evolves them through
compression-expansion cycles (Omega/Omega_inv), and extracts:
  - Global H(z): mean expansion rate vs redshift
  - Sky H0 map: per-cell expansion rate projected onto celestial sphere
  - Oscillation power spectrum: FFT of expansion fluctuations
  - Dipole amplitude: spherical harmonic l=1 component

Calibrated to physical units via:
  - Hubble time t_H = 13.8 Gyr
  - Hubble length L_H = c/H0
  - Associator charge Xi couplings from Plan 7 (topological_cosmology.py)
  - Time crystal frequency from Plan 10 (time_crystal_simulation.py)

References:
  - code/directed_numbers.py (Plan 9): TemporalThread, Omega, Omega_inv, associator
  - code/topological_cosmology.py (Plan 7): Xi & delta_tc computation
  - code/time_crystal_simulation.py (Plan 10): simulation calibration
  - notes/IST plan 11.5 — anisotropic extension.md: full methodology
  - supplementary/directed_numbers_zero_point_operators_v0_8_1.md: axioms
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from directed_numbers import (
    DirectedNumber, DirectedZero, AbsoluteZero,
    Thread, TemporalThread, Omega, Omega_inv, associator, Parity,
)

os.makedirs("code/outputs", exist_ok=True)

# ── Constants ─────────────────────────────────────────────────────────────────

PHI = (1 + np.sqrt(5)) / 2
ALPHA = 1 / 137.035999084
HBAR = 1.054571817e-34
C = 2.99792458e8
G = 6.67430e-11
L_P = 1.616255e-35
M_P_KG = 2.176434e-8

COUPLING = ALPHA / PHI**2
T_HUBBLE_GYR = 13.8
T_HUBBLE_S = T_HUBBLE_GYR * 1e9 * 365.25 * 24 * 3600
H0_NOMINAL = 73.0
H0_SI = H0_NOMINAL * 1000 / (3.0857e22)
L_H = C / H0_SI

PLANCK_H0 = 67.4
SHOES_H0 = 73.0


# ── Grid Construction ─────────────────────────────────────────────────────────

def build_cosmological_grid(n_grid=12, seed=42):
    """Build 3D grid of TemporalThread objects representing Hubble-scale patches.

    Each cell has:
      - thread_density (amplitude) → proxies for matter density ρ_m
      - associator_charge (from thread cross-multiplications) → Ξ(x)
      - twist_on_shift (True near Klein bottle seam) → time crystal activation
      - parity (UP/DOWN) → substrate chirality
    """
    rng = np.random.default_rng(seed)
    grid = np.empty((n_grid, n_grid, n_grid), dtype=object)

    center = n_grid / 2
    for i in range(n_grid):
        for j in range(n_grid):
            for k in range(n_grid):
                dist_from_seam = abs(i - center) / center

                n_elements = max(2, int(5 + rng.poisson(3)))
                elements = []
                for _ in range(n_elements):
                    amp = rng.uniform(0.5, 2.0) * (1 + 0.3 * (1 - dist_from_seam))
                    parity = Parity.UP if rng.random() > 0.5 else Parity.DOWN
                    elements.append(DirectedNumber(amplitude=amp, parity=parity))

                twist = dist_from_seam < 0.25
                grid[i, j, k] = TemporalThread(
                    elements=elements,
                    time_index=0,
                    twist_on_shift=twist
                )

    return grid


# ── Grid Observables ──────────────────────────────────────────────────────────

def compute_grid_H0(grid, H0_base=73.0):
    """Compute effective H0 per cell from thread density.

    H_eff^2 = 8πG/3 * ρ_eff where ρ_eff ∝ total_info / cell_volume.

    Following Plan 7 master equation (topological_cosmology.py:17-19):
    Each cell's effective mass ∝ I_topo + COUPLING*Xi + delta_tc.
    """
    n = grid.shape[0]
    H0_map = np.zeros((n, n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                thread = grid[i, j, k]
                I_topo = thread.info_total()
                Xi_cell = _compute_cell_associator(thread)
                delta_tc = 0.01 * I_topo if thread.twist_on_shift else 0.0

                M_eff = (HBAR * C / L_H) * (I_topo + COUPLING * Xi_cell + delta_tc)
                rho_eff = M_eff / (L_H / n)**3
                H_eff = np.sqrt(8 * np.pi * G * rho_eff / 3) * (3.0857e22 / 1000)
                H0_map[i, j, k] = H_eff
    return H0_map


def _compute_cell_associator(thread, max_triplets=20):
    """Estimate associator charge Xi per cell from thread cross-multiplications.

    Xi ~ mean(|[x,y,z]|) across triplets of elements in the thread.
    From code/directed_numbers.py:286-290.
    """
    elements = thread.elements
    if len(elements) < 3:
        return 0.0
    n_triplets = min(max_triplets, len(elements) - 2)
    xi_sum = 0.0
    rng = np.random.default_rng(42)
    for _ in range(n_triplets):
        x, y, z = rng.choice(elements, 3, replace=False)
        xi_sum += associator(x, y, z)
    return xi_sum / n_triplets


def compute_sky_H0_map(grid, H0_map):
    """Project the 3D H0 map onto a celestial sphere (Mollweide-like projection)."""
    n = grid.shape[0]
    n_sky = 72
    ra_bins = np.linspace(0, 360, n_sky)
    dec_bins = np.linspace(-90, 90, n_sky // 2)

    center = n / 2
    sky_map = np.zeros((n_sky // 2, n_sky))

    for i in range(n):
        for j in range(n):
            for k in range(n):
                dx = i - center
                dy = j - center
                dz = k - center
                r = np.sqrt(dx**2 + dy**2 + dz**2)
                if r < 1e-6:
                    continue
                dec = np.degrees(np.arcsin(dz / r))
                ra = np.degrees(np.arctan2(dy, dx)) % 360
                ra_idx = int(np.interp(ra, [0, 360], [0, n_sky - 1]))
                dec_idx = int(np.interp(dec, [-90, 90], [0, n_sky // 2 - 1]))
                ra_idx = np.clip(ra_idx, 0, n_sky - 1)
                dec_idx = np.clip(dec_idx, 0, n_sky // 2 - 1)
                sky_map[dec_idx, ra_idx] += H0_map[i, j, k]

    sky_map /= (n**3 / (n_sky * n_sky // 2))
    return sky_map, ra_bins, dec_bins


def compute_dipole_amplitude(sky_map):
    """Compute spherical harmonic l=1 (dipole) amplitude from sky map."""
    mean_H0 = np.mean(sky_map)
    n_sky, m_sky = sky_map.shape
    dipole = 0.0
    for i in range(n_sky):
        dec = np.radians(-90 + 180 * (i + 0.5) / n_sky)
        for j in range(m_sky):
            dipole += (sky_map[i, j] - mean_H0) * np.sin(dec + np.pi / 2)
    dipole /= (n_sky * m_sky * mean_H0)
    return dipole


# ── Evolution Engine ──────────────────────────────────────────────────────────

def evolve_cosmological_grid(grid, n_steps=500, injection_rate=0.05,
                              compress_threshold_factor=0.20,
                              expand_threshold_factor=1.5, seed=42):
    """Evolve the thread grid forward in time using directed numbers operations.

    Each step:
      1. Injection: add infalling perturbation elements to random cells
      2. Compression: Omega() cells with gradient above threshold
      3. Expansion: Omega_inv() when total compressed amplitude > limit (Klein twist)
      4. Measurement: record H_eff and Xi field
    """
    n = grid.shape[0]
    rng = np.random.default_rng(seed)
    H_history = []
    Xi_history = []
    compressed_history = []
    twist_history = []

    for step in range(n_steps):
        # 1. Injection
        n_inject = int(injection_rate * n**3)
        for _ in range(n_inject):
            i = rng.integers(0, n)
            j = rng.integers(0, n)
            k = rng.integers(0, n)
            amp = rng.uniform(0.1, 0.5)
            parity = Parity.UP if rng.random() > 0.5 else Parity.DOWN
            grid[i, j, k].push(DirectedNumber(amplitude=amp, parity=parity))

        # 2. Compression: compress cells with high local gradient
        compressed_mask = np.zeros((n, n, n), dtype=bool)
        total_compressed = 0.0
        mean_info = np.mean([grid[i, j, k].info_total() for i in range(n) for j in range(n) for k in range(n)])
        threshold = compress_threshold_factor * mean_info

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    info = grid[i, j, k].info_total()
                    if info > threshold:
                        for el in grid[i, j, k].elements:
                            if el._parity_enum.is_manifest():
                                total_compressed += el.amplitude
                                Omega(el)
                        compressed_mask[i, j, k] = True

        compressed_history.append(total_compressed)

        # 3. Expansion + twist
        n_twisted = 0
        if total_compressed > expand_threshold_factor * mean_info:
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        thread = grid[i, j, k]
                        if compressed_mask[i, j, k]:
                            for el in thread.elements:
                                if el._parity_enum.is_zero() and not isinstance(el, AbsoluteZero):
                                    Omega_inv(el, deterministic=False)
                            if thread.twist_on_shift:
                                thread.T_plus()
                                n_twisted += 1
                        else:
                            thread.T_plus()
            twist_history.append(n_twisted)
        else:
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        grid[i, j, k].T_plus()
            twist_history.append(0)

        # 4. Measurement
        H0_map = compute_grid_H0(grid)
        H_mean = np.mean(H0_map)
        Xi_mean = np.mean([_compute_cell_associator(grid[i, j, k]) for i in range(n) for j in range(n) for k in range(n)])

        H_history.append(H_mean)
        Xi_history.append(Xi_mean)

        if step % 100 == 0:
            print(f"  Step {step:4d}/{n_steps}: H0={H_mean:.2f}, Xi={Xi_mean:.4f}, "
                  f"compressed={total_compressed:.2f}, twists={twist_history[-1]}")

    return np.array(H_history), np.array(Xi_history), np.array(compressed_history), twist_history


# ── Analysis ──────────────────────────────────────────────────────────────────

def analyze_oscillation(H_history, n_steps):
    """FFT analysis of H(t) time series — extract time crystal frequency."""
    H_detrend = H_history - np.mean(H_history)
    fft = np.abs(np.fft.rfft(H_detrend))
    freqs = np.fft.rfftfreq(n_steps)
    dominant_idx = np.argmax(fft[1:]) + 1
    dominant_freq = freqs[dominant_idx]
    dominant_power = fft[dominant_idx]

    t_Hubble = T_HUBBLE_GYR / (n_steps / len(H_history))
    freq_physical = dominant_freq / t_Hubble

    return {
        "dominant_freq_sim": dominant_freq,
        "dominant_freq_Gyr": freq_physical,
        "dominant_power": dominant_power,
        "freqs": freqs,
        "fft": fft,
        "t_per_step_Gyr": T_HUBBLE_GYR / n_steps,
    }


def calibrate_to_plan11(H_history, analysis):
    """Compare simulation oscillation parameters to Plan 11 best-fit values.

    Plan 11 log-periodic fit: Delta = 1.54 (log-period)
    Time crystal simulation (Plan 10): f_sim = 0.00125
    """
    print()
    print("=" * 65)
    print("  CALIBRATION TO PLAN 11 RESULTS")
    print("=" * 65)

    Delta_fitted = 1.54
    eps_fitted = 0.136

    f_sim = analysis["dominant_freq_sim"]
    f_phy = analysis["dominant_freq_Gyr"]

    Delta_sim = 1.0 / f_sim if f_sim > 0 else np.inf

    print(f"  Plan 11 log-periodic fit: Delta = {Delta_fitted:.2f}, eps = {eps_fitted:.4f}")
    print(f"  Simulation dominant frequency: f_sim = {f_sim:.6f} (sim units)")
    print(f"  Simulation period: Delta_sim = 1/f_sim = {Delta_sim:.2f}")
    print(f"  Physical frequency: {f_phy:.6f} Gyr^-1")
    print(f"  Period in Gyr: {1/f_phy:.2f}" if f_phy > 0 else "  (undefined)")
    print()

    H_std = np.std(H_history)
    H_mean = np.mean(H_history)
    eps_sim = H_std / H_mean

    print(f"  Plan 11 amplitude: eps = {eps_fitted:.4f}")
    print(f"  Simulation std(H)/mean(H): eps_sim = {eps_sim:.6f}")
    print(f"  IST predicted eps = alpha/phi^2 = {COUPLING:.6f}")
    print()

    return {
        "Delta_fitted": Delta_fitted,
        "Delta_sim": Delta_sim,
        "eps_fitted": eps_fitted,
        "eps_sim": eps_sim,
    }


# ── Plotting ──────────────────────────────────────────────────────────────────

def plot_results(grid, H_history, Xi_history, compressed_history, twist_history,
                 analysis, calib, n_grid, n_steps):
    """Generate diagnostic plots."""

    # 1. H(z) evolution
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    t = np.arange(n_steps) * (T_HUBBLE_GYR / n_steps)
    z_equiv = T_HUBBLE_GYR / np.clip(t[1:], 1e-6, None) - 1

    ax1 = axes[0, 0]
    ax1.plot(t, H_history, "b-", lw=1)
    ax1.axhline(y=SHOES_H0, color="orange", ls=":", lw=1, label=f"SH0ES H0={SHOES_H0}")
    ax1.axhline(y=PLANCK_H0, color="green", ls=":", lw=1, label=f"Planck H0={PLANCK_H0}")
    ax1.set_xlabel("Cosmic time [Gyr]")
    ax1.set_ylabel("H(t) [km/s/Mpc]")
    ax1.set_title("Simulated Hubble Parameter vs Time")
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)

    # 2. FFT power spectrum
    ax2 = axes[0, 1]
    freqs = analysis["freqs"]
    fft = analysis["fft"]
    ax2.semilogy(freqs[1:len(fft)], fft[1:len(fft)], "r-", lw=1)
    ax2.axvline(x=analysis["dominant_freq_sim"], color="b", ls="--",
                label=f"Dominant f={analysis['dominant_freq_sim']:.4f}")
    ax2.set_xlabel("Frequency [1/sim-step]")
    ax2.set_ylabel("Power")
    ax2.set_title("FFT of H(t) — Time Crystal Oscillation")
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    # 3. Sky H0 map
    ax3 = axes[1, 0]
    H0_map = compute_grid_H0(grid)
    sky_map, ra_bins, dec_bins = compute_sky_H0_map(grid, H0_map)
    ext = [0, 360, -90, 90]
    im3 = ax3.imshow(sky_map, extent=ext, aspect="auto", origin="lower",
                      cmap="RdBu_r", interpolation="bilinear")
    ax3.set_xlabel("RA [deg]")
    ax3.set_ylabel("Dec [deg]")
    ax3.set_title("Simulated Sky H0 Map (Mollweide-equiv)")
    plt.colorbar(im3, ax=ax3, label="H0 [km/s/Mpc]")

    # 4. Compressed + twist history
    ax4 = axes[1, 1]
    ax4.plot(range(n_steps), compressed_history, "b-", lw=0.7, alpha=0.7, label="Compressed amplitude")
    ax4_twin = ax4.twinx()
    ax4_twin.plot(range(n_steps), twist_history, "r-", lw=0.7, alpha=0.7, label="N twists/step")
    ax4.set_xlabel("Simulation step")
    ax4.set_ylabel("Total compressed amplitude", color="b")
    ax4_twin.set_ylabel("Twists per step", color="r")
    ax4.set_title("Compression-Expansion Cycles (Omega/Omega_inv)")
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("code/outputs/cosmo_grid_diagnostics.png", dpi=150)
    plt.close(fig)

    # 5. Comparison to Plan 11 fit
    fig2, ax = plt.subplots(figsize=(8, 5))

    z_fine = np.linspace(0.01, 2.5, 100)
    H_lcdm = 70.35 * np.sqrt(0.2547 * (1 + z_fine)**3 + (1 - 0.2547))
    H_log = hz_osc_log_fn(z_fine, 71.00, 0.2470, 0.136, 1.54, -3.1416)

    t_steps = np.arange(len(H_history))
    t_cosmic = t_steps * (T_HUBBLE_GYR / n_steps)
    z_sim = T_HUBBLE_GYR / np.clip(t_cosmic, 1e-6, None) - 1
    z_sim = np.clip(z_sim, 0, 2.5)

    ax.axhline(y=SHOES_H0, color="orange", ls=":", lw=1, label=f"SH0ES H0={SHOES_H0}")
    ax.axhline(y=PLANCK_H0, color="green", ls=":", lw=1, label=f"Planck H0={PLANCK_H0}")
    ax.plot(z_fine, H_lcdm, "b-", lw=1.5, label="Plan 11 LCDM (H0=70.35)")
    ax.plot(z_fine, H_log, "r--", lw=1.5, label="Plan 11 Log-periodic (H0=71.00)")

    sort_sim = np.argsort(z_sim)
    ax.plot(z_sim[sort_sim], H_history[sort_sim], "k-", lw=1, alpha=0.7,
            label=f"Simulation (mean H0={np.mean(H_history):.1f})")

    ax.set_xlabel("Redshift z")
    ax.set_ylabel("H(z) [km/s/Mpc]")
    ax.set_title("Directed Numbers Cosmology vs Plan 11 Fits")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 2.5)

    plt.tight_layout()
    plt.savefig("code/outputs/cosmo_grid_hz.png", dpi=150)
    plt.close(fig2)

    print("  Plots saved:")
    print("    - code/outputs/cosmo_grid_diagnostics.png")
    print("    - code/outputs/cosmo_grid_hz.png")


def hz_osc_log_fn(z, H0, Om_m, eps, Delta, phi):
    """Convenience function matching Plan 11 log-periodic model."""
    cos_arg = (2 * np.pi / Delta) * np.log(1 + z) + phi
    return H0 * np.sqrt(Om_m * (1 + z)**3 + (1 - Om_m) * (1 + eps * np.cos(cos_arg)))


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 65)
    print("Plan 11.5 — Phase 2B: Direct Numbers Cosmological Simulation")
    print("=" * 65)
    print(f"  Grid: {n_grid}x{n_grid}x{n_grid} Hubble-scale patches")
    print(f"  Time steps: {n_steps} (~{T_HUBBLE_GYR/n_steps:.1f} Gyr/step)")
    print(f"  Hubble time: {T_HUBBLE_GYR} Gyr")
    print(f"  Coupling: alpha/phi^2 = {COUPLING:.6f}")
    print(f"  Target: reproduce Plan 11 Delta=1.54, eps=0.136 oscillation")
    print()

    n_grid = 6
    n_steps = 100

    print("Building cosmological thread grid...")
    grid = build_cosmological_grid(n_grid=n_grid)

    def grid_total_info_3d(g):
        n = g.shape[0]
        total = 0.0
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    total += g[i, j, k].info_total()
        return total

    initial_info = grid_total_info_3d(grid)
    print(f"  Initial total info: {initial_info:.2f}")

    print("Evolving grid (compression-expansion cycles)...")
    H_history, Xi_history, compressed_history, twist_history = evolve_cosmological_grid(
        grid, n_steps=n_steps,
        injection_rate=0.05,
        compress_threshold_factor=0.20,
        expand_threshold_factor=1.5,
    )

    final_info = grid_total_info_3d(grid)
    print(f"  Final total info: {final_info:.2f} (conservation delta = {final_info - initial_info:.4f})")
    print()

    analysis = analyze_oscillation(H_history, n_steps)
    calib = calibrate_to_plan11(H_history, analysis)

    dipole = compute_dipole_amplitude(compute_sky_H0_map(grid, compute_grid_H0(grid))[0])

    print("Plotting results...")
    plot_results(grid, H_history, Xi_history, compressed_history, twist_history,
                 analysis, calib, n_grid, n_steps)

    with open("code/outputs/cosmo_grid_params.txt", "w", encoding="utf-8") as f:
        f.write("=" * 65 + "\n")
        f.write("DIRECTED NUMBERS COSMOLOGICAL SIMULATION PARAMETERS\n")
        f.write("=" * 65 + "\n\n")
        f.write(f"Grid size: {n_grid}^3 = {n_grid**3} patches\n")
        f.write(f"Time steps: {n_steps}\n")
        f.write(f"Physical time per step: {T_HUBBLE_GYR/n_steps:.3f} Gyr\n")
        f.write(f"Initial total information: {initial_info:.2f}\n")
        f.write(f"Final total information: {final_info:.2f}\n\n")
        f.write(f"Simulation oscillation frequency: {analysis['dominant_freq_sim']:.6f} (sim units)\n")
        f.write(f"Physical oscillation frequency: {analysis['dominant_freq_Gyr']:.6f} Gyr^-1\n")
        f.write(f"Simulation period (1/f): {calib['Delta_sim']:.2f}\n")
        f.write(f"Plan 11 fitted period (Delta): {calib['Delta_fitted']:.2f}\n\n")
        f.write(f"Simulation eps (std/mean): {calib['eps_sim']:.6f}\n")
        f.write(f"Plan 11 fitted eps: {calib['eps_fitted']:.4f}\n")
        f.write(f"IST predicted eps (alpha/phi^2): {COUPLING:.6f}\n\n")
        f.write(f"Sky dipole amplitude (l=1): {dipole:.6f}\n")
        f.write(f"Mean simulated H0: {np.mean(H_history):.2f} km/s/Mpc\n")

    print()
    print("=" * 65)
    print("  SUMMARY")
    print("=" * 65)
    print(f"  Mean H0: {np.mean(H_history):.1f} km/s/Mpc (SH0ES={SHOES_H0}, Planck={PLANCK_H0})")
    print(f"  Oscillation: f_sim={analysis['dominant_freq_sim']:.4f}, period={calib['Delta_sim']:.2f}")
    print(f"  Plan 11 Delta: {calib['Delta_fitted']:.2f}")
    print(f"  Simulation eps: {calib['eps_sim']:.4f} vs fitted {calib['eps_fitted']:.4f}")
    print(f"  Dipole amplitude: {dipole:.6f}")
    print(f"  Info conservation: {final_info - initial_info:.6f} (~0 expected)")
    print()
    print("  Output files:")
    print("    - code/outputs/cosmo_grid_diagnostics.png")
    print("    - code/outputs/cosmo_grid_hz.png")
    print("    - code/outputs/cosmo_grid_params.txt")
