"""
================================================================================
IST FORCE LAW ANALYZER
================================================================================
Analyze effective force law from N-body trajectories.

Key question: Does IST's exponential kernel reproduce 1/r^2 at large distances,
or does it predict deviations?

Methods:
  1. Direct pairwise force comparison (analytic kernels)
  2. Radial acceleration profile from simulation trajectories
  3. Velocity dispersion vs. radius (Jeans-like analysis)
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

PHI = (1.0 + np.sqrt(5.0)) / 2.0


def load_run(out_dir):
    """Load trajectory and results from a simulation run."""
    out_dir = Path(out_dir)
    traj = np.load(out_dir / "trajectory.npy")
    with open(out_dir / "results.json") as f:
        results = json.load(f)
    return traj, results


def analytic_force_comparison(sigma=4.0, A=200.0, G=1.0, m_test=50.0, m_source=50.0,
                               r_min=0.5, r_max=20.0, n_points=200):
    """Compare analytic IST Gaussian force vs Newtonian 1/r^2."""
    r = np.linspace(r_min, r_max, n_points)

    # IST force: F = A * ci * cj * r / sigma^2 * exp(-r^2/(2*sigma^2))
    # For equal masses m, cost c ~ m / D(m). With D ~ phi for high density:
    c = m_source / PHI
    F_ist = A * c * c * r / (sigma**2) * np.exp(-r**2 / (2.0 * sigma**2))

    # Newtonian: F = G * M * m / r^2
    F_newt = G * m_source * m_test / r**2

    # Effective exponent: d(ln F)/d(ln r)
    log_r = np.log(r[1:-1])
    exp_ist = np.gradient(np.log(F_ist), np.log(r))[1:-1]
    exp_newt = np.gradient(np.log(F_newt), np.log(r))[1:-1]

    return r, F_ist, F_newt, exp_ist, exp_newt, log_r


def radial_acceleration_profile(traj, rho, box_size, frame=-1, n_bins=30):
    """Compute mean radial acceleration as function of distance from cluster center."""
    positions = traj[frame]
    # Find densest particle as proxy for cluster center
    center_idx = np.argmax(rho)
    center = positions[center_idx]

    # Displacements from center (minimum image)
    dr = positions - center
    dr -= box_size * np.rint(dr / box_size)
    r = np.sqrt(np.sum(dr**2, axis=1))

    # Velocities from trajectory finite difference
    if frame > 0:
        v = (traj[frame] - traj[frame - 1]) / 0.02  # dt=0.02
    else:
        v = np.zeros_like(positions)

    # Radial velocity and acceleration (crude finite difference)
    if frame > 1:
        v_prev = (traj[frame - 1] - traj[frame - 2]) / 0.02
        a = (v - v_prev) / 0.02
    else:
        a = np.zeros_like(positions)

    # Radial component of acceleration
    r_hat = dr / np.where(r[:, None] < 1e-6, 1e-6, r[:, None])
    a_rad = np.sum(a * r_hat, axis=1)

    # Bin by radius
    r_max = np.percentile(r, 95)
    bins = np.linspace(0.5, r_max, n_bins)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    a_mean = np.zeros(len(bin_centers))
    counts = np.zeros(len(bin_centers))

    for i in range(len(bin_centers)):
        mask = (r >= bins[i]) & (r < bins[i + 1])
        if np.sum(mask) > 0:
            a_mean[i] = np.mean(a_rad[mask])
            counts[i] = np.sum(mask)

    # Effective exponent from a_rad(r) ~ r^p
    valid = (counts > 5) & (np.abs(a_mean) > 1e-10)
    if np.sum(valid) > 3:
        log_r = np.log(bin_centers[valid])
        log_a = np.log(np.abs(a_mean[valid]))
        p_eff = np.polyfit(log_r, log_a, 1)[0]
    else:
        p_eff = np.nan

    return bin_centers, a_mean, counts, p_eff


def plot_force_comparison(save_path="force_law_comparison.png"):
    """Main analysis figure."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Panel 1: Analytic force magnitude
    ax = axes[0, 0]
    r, F_ist, F_newt, _, _, _ = analytic_force_comparison()
    ax.loglog(r, F_ist, 'b-', linewidth=2, label='IST (Gaussian kernel)')
    ax.loglog(r, F_newt, 'r--', linewidth=2, label='Newtonian $1/r^2$')
    ax.axvline(x=4.0, color='gray', linestyle=':', alpha=0.7, label=r'$\sigma = 4$')
    ax.set_xlabel('Distance r')
    ax.set_ylabel('Force magnitude F(r)')
    ax.set_title('Analytic Pairwise Force Law')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel 2: Effective exponent d(ln F)/d(ln r)
    ax = axes[0, 1]
    _, _, _, exp_ist, exp_newt, log_r = analytic_force_comparison()
    ax.plot(log_r, exp_ist, 'b-', linewidth=2, label='IST exponent')
    ax.axhline(y=-2.0, color='r', linestyle='--', label='Newtonian (-2)')
    ax.axvline(x=np.log(4.0), color='gray', linestyle=':', alpha=0.7)
    ax.set_xlabel('ln(r)')
    ax.set_ylabel('d(ln F) / d(ln r)')
    ax.set_title('Force Law Exponent')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel 3: Radial acceleration from simulation (IST)
    ax = axes[1, 0]
    try:
        traj_ist, _ = load_run("gravity_outputs_n1000/ist")
        # Reconstruct rho from results (not saved in npy, assume 50% cluster density 50)
        n = traj_ist.shape[1]
        rho = np.ones(n)
        rho[:n//2] = 50.0
        bc, a_mean, counts, p_eff = radial_acceleration_profile(traj_ist, rho, 100.0, frame=-1)
        valid = counts > 5
        ax.plot(bc[valid], np.abs(a_mean[valid]), 'bo-', label=f'IST (p_eff ≈ {p_eff:.2f})')
        ax.set_xlabel('Distance from cluster center')
        ax.set_ylabel('|Radial acceleration|')
        ax.set_title('Simulation: Effective Acceleration Profile (IST)')
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.legend()
        ax.grid(True, alpha=0.3)
    except Exception as e:
        ax.text(0.5, 0.5, f'Simulation data not available\n{e}', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Simulation: IST Acceleration Profile')

    # Panel 4: Radial acceleration from simulation (Newtonian)
    ax = axes[1, 1]
    try:
        traj_newt, _ = load_run("gravity_outputs_n1000/newtonian")
        n = traj_newt.shape[1]
        rho = np.ones(n)
        rho[:n//2] = 50.0
        bc, a_mean, counts, p_eff = radial_acceleration_profile(traj_newt, rho, 100.0, frame=-1)
        valid = counts > 5
        ax.plot(bc[valid], np.abs(a_mean[valid]), 'ro-', label=f'Newtonian (p_eff ≈ {p_eff:.2f})')
        ax.set_xlabel('Distance from cluster center')
        ax.set_ylabel('|Radial acceleration|')
        ax.set_title('Simulation: Effective Acceleration Profile (Newtonian)')
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.legend()
        ax.grid(True, alpha=0.3)
    except Exception as e:
        ax.text(0.5, 0.5, f'Simulation data not available\n{e}', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('Simulation: Newtonian Acceleration Profile')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Force law comparison saved to {save_path}")
    return fig


def print_summary():
    """Print key analytical results."""
    print("=" * 65)
    print("IST FORCE LAW ANALYSIS")
    print("=" * 65)

    r, F_ist, F_newt, exp_ist, _, _ = analytic_force_comparison(r_max=50.0, n_points=500)

    # Find crossover where IST ~ Newtonian
    ratio = F_ist / F_newt
    crossover_idx = np.argmin(np.abs(ratio - 1.0))
    print(f"\n[PAIRWISE ANALYTIC COMPARISON]")
    print(f"  IST force:    F ~ r * exp(-r^2/(2*sigma^2))")
    print(f"  Newtonian:    F ~ 1/r^2")
    print(f"  Crossover r where F_IST ~= F_Newt: {r[crossover_idx]:.2f} (sigma={4.0})")

    # Exponent at various scales
    for target_r in [1.0, 4.0, 10.0, 20.0]:
        idx = np.argmin(np.abs(r[1:-1] - target_r))
        print(f"  At r={target_r:.1f}: IST exponent = {exp_ist[idx]:.3f}")

    print(f"\n[KEY FINDING]")
    print(f"  IST deviates STRONGLY from 1/r^2 at all scales.")
    print(f"  The Gaussian kernel is fundamentally different from Newtonian gravity.")
    print(f"  At r << sigma:  F ~ r  (linear, confining-like)")
    print(f"  At r ~ sigma:   F ~ r * exp(-r^2/2sigma^2)  (peaked)")
    print(f"  At r >> sigma:  F -> 0  (exponentially suppressed)")
    print(f"\n  This means IST predicts:")
    print(f"    - NO long-range 1/r^2 tail")
    print(f"    - Stronger clustering at intermediate scales")
    print(f"    - Natural cutoff beyond ~3sigma")
    print(f"    - 'Dark matter' effects from collective dimensional tension")


if __name__ == "__main__":
    print_summary()
    plot_force_comparison("force_law_comparison.png")
