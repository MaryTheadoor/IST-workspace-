"""
IST Plan 5 — Visualisation Suite
=================================
Phase 2: Comprehensive visualisations for communicating IST black hole
topology. Uses pyvista, plotly, matplotlib, imageio.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

os.makedirs("outputs/visualisations", exist_ok=True)


# ───────────────────────────────────────────────────────────────────────────────
# Constants
# ───────────────────────────────────────────────────────────────────────────────

PHI = (1 + np.sqrt(5)) / 2
ALPHA = 1 / 137.035999084
C = 2.99792458e8
G = 6.67430e-11
HBAR = 1.054571817e-34
KB = 1.380649e-23
L_P = 1.616255e-35

M_SOLAR = 1.989e30
R_S = 2 * G * M_SOLAR / C**2  # Schwarzschild radius for 1 solar mass


# ───────────────────────────────────────────────────────────────────────────────
# 1. Klein Bottle Horizon — 3D mesh with information density colormap
# ───────────────────────────────────────────────────────────────────────────────

def klein_bottle_mesh(n=80, radius=10.0, twist=1.0):
    u = np.linspace(0, 2 * np.pi, n)
    v = np.linspace(0, 2 * np.pi, n)
    u, v = np.meshgrid(u, v)

    x = (radius + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)) * np.cos(u)
    y = (radius + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)) * np.sin(u)
    z = np.sin(u / 2) * np.sin(v) + np.cos(u / 2) * np.sin(2 * v)
    x *= twist

    return x, y, z


def klein_info_density(x, y, z):
    """Simulated information density pattern on the Klein bottle."""
    r = np.sqrt(x**2 + y**2 + z**2)
    r_norm = r / r.max()
    density = 0.5 + 0.3 * np.sin(x * 0.5) * np.cos(y * 0.5) * np.sin(z * 0.3)
    density += 0.15 * np.sin(r_norm * 4 * np.pi)
    density = np.clip(density, 0.05, 1.0)
    return density


def plot_klein_horizon():
    print("  [1/6] Klein bottle horizon...")
    x, y, z = klein_bottle_mesh(n=60)
    density = klein_info_density(x, y, z)

    # --- HTML (plotly, interactive) ---
    try:
        import plotly.graph_objects as go
        fig = go.Figure(data=[go.Surface(
            x=x, y=y, z=z, surfacecolor=density,
            colorscale="plasma", cmin=0, cmax=1,
            colorbar=dict(title="Info Density"),
        )])
        fig.update_layout(
            title="Klein Bottle Black Hole Horizon — Information Density",
            scene=dict(
                xaxis_title="X", yaxis_title="Y", zaxis_title="Z",
                aspectmode="data",
            ),
            width=900, height=700,
        )
        fig.write_html("outputs/visualisations/klein_horizon_density.html")
        print("    -> klein_horizon_density.html")
    except ImportError:
        print("    (plotly not available, skipping HTML)")

    # --- PNG (matplotlib) ---
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(x, y, z, facecolors=plt.cm.plasma(density / density.max()),
                           rstride=1, cstride=1, alpha=0.9, antialiased=True)
    ax.set_title("Klein Bottle Horizon — Information Density")
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    m = plt.cm.ScalarMappable(cmap="plasma")
    m.set_array(density)
    plt.colorbar(m, ax=ax, shrink=0.5, label="Info Density")
    fig.savefig("outputs/visualisations/klein_horizon_density.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("    -> klein_horizon_density.png")


# ───────────────────────────────────────────────────────────────────────────────
# 2. Axis of Knots — high-density nodes along central axis
# ───────────────────────────────────────────────────────────────────────────────

def plot_axis_knots():
    print("  [2/6] Axis of knots...")
    x, y, z = klein_bottle_mesh(n=50, radius=8.0)
    density = klein_info_density(x, y, z)

    threshold = np.percentile(density, 90)
    mask = density > threshold
    kx, ky, kz = x[mask], y[mask], z[mask]
    kd = density[mask]

    center_x = kx.mean()
    center_y = ky.mean()
    center_z = kz.mean()

    axis_t = np.linspace(-1, 1, len(kx))
    proj_x = center_x + axis_t * (kx.std() * 3)
    proj_y = center_y + axis_t * (ky.std() * 3)
    proj_z = center_z + axis_t * (kz.std() * 3)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    scatter = ax.scatter(proj_x, proj_y, proj_z, c=kd, cmap="hot",
                         s=kd * 80, alpha=0.7, edgecolors="white", linewidth=0.3)
    ax.plot([center_x - 3, center_x + 3],
            [center_y, center_y], [center_z, center_z],
            "gray", linewidth=1, alpha=0.3, linestyle="--", label="central axis")

    plt.colorbar(scatter, ax=ax, shrink=0.5, label="Knot Density")
    ax.set_title(f"Axis of High-Density Information Knots\n({len(kx)} nodes > 90th percentile)")
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    ax.legend()
    fig.savefig("outputs/visualisations/axis_knots.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("    -> axis_knots.png")


# ───────────────────────────────────────────────────────────────────────────────
# 3. Inversion Vortex Animation — compression/expansion GIF
# ───────────────────────────────────────────────────────────────────────────────

def plot_inversion_animation():
    print("  [3/6] Inversion vortex animation...")
    n_frames = 60
    frames = []

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="3d")

    for i in range(n_frames):
        ax.clear()

        if i < 15:
            # Pre-compression: blue sphere (up), amplitude 1.0
            amp = 1.0
            color = "blue"
            label = "manifest (up)"
        elif i < 18:
            # Omega(): collapsing to directed zero
            amp = 1.0 * (1 - (i - 15) / 3.0)
            color = "purple"
            label = "Omega() compressing"
        elif i < 25:
            # Compressed state (directed zero)
            amp = 0.15
            color = "black"
            label = "directed zero"
            for _ in range(3):
                jitter = np.random.randn(3) * 0.15
                ax.scatter(*jitter, c="gray", s=20, alpha=0.5)
        elif i < 28:
            # Omega_inv(): expanding with parity flip
            amp = 0.15 + 0.85 * ((i - 25) / 3.0)
            color = "red"
            label = "Omega_inv() expanding (down)"
        elif i < 40:
            # Post-expansion: red sphere (down), amplitude 1.0
            amp = 1.0
            color = "red"
            label = "manifest (down)"
        else:
            # Compressed again for cycle
            amp = 1.0 * (1 - (i - 40) / 15.0)
            amp = max(0.15, amp)
            color = "purple"
            label = "re-compression"

        u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 20), np.linspace(0, np.pi, 20))
        xs = amp * np.sin(v) * np.cos(u)
        ys = amp * np.sin(v) * np.sin(u)
        zs = amp * np.cos(v)
        ax.plot_surface(xs, ys, zs, color=color, alpha=0.8)

        ax.set_xlim([-1.3, 1.3]); ax.set_ylim([-1.3, 1.3]); ax.set_zlim([-1.3, 1.3])
        ax.set_title(f"Information Knot Inversion\n{label}")
        ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")

        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))
        frames.append(image[:, :, :3])

    plt.close(fig)

    # Save as GIF
    try:
        import imageio
        imageio.mimsave("outputs/visualisations/inversion_vortex.gif", frames, fps=8, loop=0)
        print("    -> inversion_vortex.gif")
    except ImportError:
        print("    (imageio not available, skipping GIF)")

    # Save as MP4 if ffmpeg available
    try:
        import imageio
        imageio.mimsave("outputs/visualisations/inversion_vortex.mp4", frames, fps=10, codec="libx264")
        print("    -> inversion_vortex.mp4")
    except Exception:
        print("    (MP4 write failed — ffmpeg may not be installed)")


# ───────────────────────────────────────────────────────────────────────────────
# 4. Non-Thermal Radiation Spectrum
# ───────────────────────────────────────────────────────────────────────────────

def plot_radiation_spectrum(M_solar=30.0):
    print("  [4/6] Radiation spectrum...")
    M = M_solar * M_SOLAR
    R_s = 2 * G * M / C**2
    T_H = HBAR * C**3 / (8 * np.pi * G * M * KB)

    # Thermal background (Planck)
    nu = np.logspace(8, 22, 500)
    x = HBAR * 2 * np.pi * nu / (KB * T_H)
    # Clip x to avoid overflow in exp
    x = np.clip(x, -500, 500)
    planck = (2 * HBAR * nu**3 / C**2) / (np.exp(x) - 1 + 1e-300)
    planck = planck / (planck.max() + 1e-300)
    planck += 0.001 * (np.random.random(len(nu)) - 0.5)

    # Lorentzian peaks at linking frequencies
    nu_peaks = []
    peak_heights = []
    for Lk in range(1, 11):
        omega_k = (C / R_s) * Lk
        nu_k = omega_k / (2 * np.pi)
        if nu[0] < nu_k < nu[-1]:
            nu_peaks.append(nu_k)
            peak_heights.append(0.3 / Lk)

    signal = planck.copy()
    for nu_p, h in zip(nu_peaks, peak_heights):
        gamma = 0.05 * nu_p
        lorentz = h * gamma**2 / ((nu - nu_p)**2 + gamma**2)
        signal += lorentz

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.loglog(nu, planck, "k-", linewidth=1.5, alpha=0.7, label="thermal (Planck)")
    if nu_peaks:
        ax.loglog(nu_peaks, [signal[np.argmin(np.abs(nu - np_))] for np_ in nu_peaks],
                  "ro", markersize=6, label="linking peaks (Lk=1..10)")
        for nu_p, Lk in zip(nu_peaks, range(1, 11)):
            ax.axvline(x=nu_p, color="red", alpha=0.2, linewidth=0.5, linestyle="--")

    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Spectral Power (normalised)")
    ax.set_title(f"Non-Thermal Black Hole Radiation Spectrum\n"
                 f"M = {M_solar} M_solar, T_H = {T_H:.2e} K, R_s = {R_s:.2e} m")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.savefig("outputs/visualisations/radiation_spectrum_peaks.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("    -> radiation_spectrum_peaks.png")


# ───────────────────────────────────────────────────────────────────────────────
# 5. Hysteresis Path Dependence
# ───────────────────────────────────────────────────────────────────────────────

def plot_hysteresis_path():
    print("  [5/6] Hysteresis path dependence...")

    # Data from the associator test — different pairing orders yield different results
    from directed_numbers import DirectedNumber, DirectedZero, AbsoluteZero, Thread

    orders = ["same-order", "reversed", "shuffled"]
    order_idx = [0, 1, 2]
    final_I = []
    delta_I = []

    zero_up  = DirectedZero(memory=DirectedNumber(0.0, "up"))
    one_down = DirectedNumber(1.0, "down")

    # Test 1: (0_up * 0_up) * 1_down  = order 0
    left = (zero_up * zero_up) * one_down
    final_I.append(left.info())
    delta_I.append(left.amplitude - 0)

    # Test 2: 0_up * (0_up * 1_down)  = order 1
    right = zero_up * (zero_up * one_down)
    final_I.append(right.info())
    delta_I.append(right.amplitude - 0)

    # Test 3: (0_up * 1_down) * 0_up  = order 2
    alt = (zero_up * one_down) * zero_up
    final_I.append(alt.info())
    delta_I.append(alt.amplitude - 0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    colors = ["blue", "red", "green"]
    ax1.bar(order_idx, final_I, color=colors, alpha=0.7, edgecolor="black")
    ax1.set_xticks(order_idx)
    ax1.set_xticklabels(orders, rotation=15)
    ax1.set_ylabel("Final Mass |I|")
    ax1.set_title("Hysteresis: Mass Depends on Pairing Order")
    ax1.grid(True, alpha=0.3, axis="y")

    ax2.scatter(order_idx, delta_I, c=colors, s=150, zorder=5, edgecolors="black")
    for i, (oi, d) in enumerate(zip(order_idx, delta_I)):
        ax2.annotate(f"{d:.3f}", (oi, d), textcoords="offset points",
                     xytext=(0, 12), ha="center", fontsize=11)
    ax2.axhline(y=0, color="gray", linewidth=1)
    ax2.set_xticks(order_idx)
    ax2.set_xticklabels(orders, rotation=15)
    ax2.set_ylabel("ΔI (associator)")
    ax2.set_title(f"Non-Associativity: ΔI ≠ 0\n(1/φ² = {1/PHI**2:.4f} reference)")
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig("outputs/visualisations/hysteresis_path_dependence.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("    -> hysteresis_path_dependence.png")


# ───────────────────────────────────────────────────────────────────────────────
# 6. Summary Figure — all key IST scales
# ───────────────────────────────────────────────────────────────────────────────

def plot_summary_figure():
    print("  [6/6] Summary figure...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    (ax1, ax2), (ax3, ax4) = axes

    # Top-left: topological factor comparison
    topologies = ["sphere\nf=1.0", "torus\nf=1.0", "Klein\nf=1.5"]
    factors = [1.0, 1.0, 1.5]
    ax1.bar(topologies, factors, color=["blue", "green", "red"], alpha=0.7, edgecolor="black")
    ax1.set_ylabel("Topological Factor f")
    ax1.set_title("Topological Factor by Horizon Type")
    ax1.grid(True, alpha=0.3, axis="y")

    # Top-right: alpha/phi^2 contribution
    contrib = ALPHA / PHI**2
    ax2.barh(["α/φ²"], [contrib], color="gold", edgecolor="black")
    ax2.axvline(x=contrib, color="red", linewidth=2, linestyle="--")
    ax2.text(contrib * 1.1, 0, f"{contrib:.6f}", va="center", fontsize=12)
    ax2.set_xlabel("Value")
    ax2.set_title("Golden Ratio Coupling α/φ²")
    ax2.grid(True, alpha=0.3, axis="x")

    # Bottom-left: Mass scaling
    n_vals = np.array([7, 10, 16, 22, 34, 64])
    M_vals = 1.5 * 3.113e8 * (n_vals**2 * 0.3)
    ax3.loglog(n_vals, M_vals, "bo-", linewidth=2, markersize=8)
    ax3.set_xlabel("n_patches")
    ax3.set_ylabel("M (kg)")
    ax3.set_title("Mass Scales as n_patches²")
    ax3.grid(True, alpha=0.3)

    # Bottom-right: philosophical topology
    text = (
        "IST Black Hole Topology\n"
        "=======================\n"
        f"Mass: M = f·(ħc/2πℓ_P)·I_BH + δM_assoc\n"
        f"Coupling: α/φ² = {contrib:.6f}\n"
        f"Associator: ~ 1/φ² = {1/PHI**2:.4f}\n"
        f"Klein factor: f = 1.5\n\n"
        "\"Information is never destroyed — \n"
        "only compressed, flipped, and released.\""
    )
    ax4.text(0.1, 0.5, text, transform=ax4.transAxes, fontsize=12,
             verticalalignment="center", fontfamily="monospace")
    ax4.set_xticks([]); ax4.set_yticks([])
    ax4.set_title("Summary")

    fig.tight_layout()
    fig.savefig("outputs/visualisations/ist_summary.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("    -> ist_summary.png")


# ───────────────────────────────────────────────────────────────────────────────
# Main
# ───────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("IST Plan 5 — Visualisation Suite")
    print("=" * 40)

    plot_klein_horizon()
    plot_axis_knots()
    plot_inversion_animation()
    plot_radiation_spectrum(M_solar=30.0)
    plot_hysteresis_path()
    plot_summary_figure()

    print("\nDone. All files saved in outputs/visualisations/")
