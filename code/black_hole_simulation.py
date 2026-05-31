import os
import time
import csv
import numpy as np
import jax.numpy as jnp
from jax import jit
from ist_toolkit_v2 import TopologicalHorizon

os.makedirs("outputs", exist_ok=True)

def jax_evolve_step(rho, twist_param, n, dt, diffusion_coeff=0.01):
    lap = (
        jnp.roll(rho, -1, axis=0) + jnp.roll(rho, 1, axis=0)
        + jnp.roll(rho, -1, axis=1) + jnp.roll(rho, 1, axis=1)
        - 4 * rho
    ) / (2 * jnp.pi / n) ** 2
    u_mod = jnp.linspace(0, 2 * jnp.pi, n)
    lap = lap * (1.0 + 0.1 * twist_param * jnp.sin(u_mod)[:, None])
    rho_new = rho + diffusion_coeff * lap * dt
    return jnp.clip(rho_new, 0, 1)

jax_step = jit(jax_evolve_step, static_argnames=["n", "dt", "diffusion_coeff"])

def jax_infall_step(rho, twist_param, n, dt, infall_rate, diffusion_coeff=0.01):
    rho_new = jax_evolve_step(rho, twist_param, n, dt, diffusion_coeff)
    u_mod = jnp.linspace(0, 2 * jnp.pi, n)
    bump = jnp.exp(-((u_mod - jnp.pi) ** 2) / (2 * (0.3 * jnp.pi) ** 2))
    infall_field = infall_rate * dt * (0.5 + 0.5 * bump[:, None])
    rho_new = rho_new + infall_field
    return jnp.clip(rho_new, 0, 1)

jax_infall = jit(jax_infall_step, static_argnames=["n", "dt", "diffusion_coeff"])

# ── Run A: Critical Gradient & One-Way Transition ──────────────────────────

def run_a():
    print("=== Run A: Critical Gradient & One-Way Transition ===")
    h = TopologicalHorizon(topology="sphere", radius=10.0, mesh_resolution=40, mass_solar=10.0)
    h.build_mesh()
    rho = jnp.array(h.info_density_grid)
    n = h.mesh_resolution

    times, gradients, topologies, masses, rho_means = [], [], [], [], []
    t = 0.0; dt = 0.05
    mass = 10.0

    for step in range(8000):
        infall = 0.1 if mass < 30.0 else -0.05
        rho_np = np.array(rho)
        h.info_density_grid = rho_np
        grad = float(h.compute_gradient())
        h.info_density_grid = jnp.array(rho_np)

        was_sphere = h.topology == "sphere"
        if was_sphere:
            flipped = h.transition_if_needed()
            if flipped:
                print(f"  Transition at t={t:.1f}s, mass={mass:.1f} M_sun")
                rho = jnp.array(h.info_density_grid)
        else:
            if infall < 0 and grad < h.gradient_hold:
                reverted = h.hysteresis_test(grad)

        rho = jax_infall(rho, h.twist_param, n, dt, infall)
        mass += infall * dt
        t += dt

        if step % 200 == 0:
            rho_mean = float(np.array(rho).mean())
            times.append(t); gradients.append(grad)
            topologies.append(h.topology)
            masses.append(mass); rho_means.append(rho_mean)
            print(f"  t={t:.0f}s mass={mass:.1f} M_sun grad={grad:.2e} topo={h.topology}")

    h.info_density_grid = np.array(rho)

    with open("outputs/gradient_vs_time.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["time", "gradient", "topology", "mass", "rho_mean"])
        for i in range(len(times)):
            w.writerow([times[i], gradients[i], topologies[i], masses[i], rho_means[i]])
    print("Saved outputs/gradient_vs_time.csv")

    with open("outputs/topology_timeline.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["time", "from_topo", "to_topo", "gradient"])
        for idx, entry in enumerate(h._transition_history):
            t_entry = times[min(idx, len(times) - 1)]
            w.writerow([t_entry, entry[0], entry[1], entry[2]])
    print(f"Saved outputs/topology_timeline.csv ({len(h._transition_history)} transitions)")

    return h, times, gradients, topologies, masses

# ── Run B: Compact Dimension Growth ────────────────────────────────────────

def run_b():
    print("\n=== Run B: Compact Dimension Growth ===")
    h = TopologicalHorizon(topology="sphere", radius=10.0, mesh_resolution=40, mass_solar=10.0)
    h.build_mesh()
    rho = jnp.array(h.info_density_grid)
    n = h.mesh_resolution

    masses, n_compacts, rho_means = [], [], []
    mass = 10.0; t = 0.0; dt = 0.05

    for step in range(8000):
        infall = 0.1 if mass < 40.0 else 0.0
        rho_np = np.array(rho)
        h.info_density_grid = rho_np
        _ = h.compute_gradient()
        h.transition_if_needed()
        delta_n = h.update_compact_dimensions()
        rho = jax_infall(rho, h.twist_param, n, dt, infall)
        mass += infall * dt; t += dt

        if step % 200 == 0:
            n_compacts.append(h.compact_dimensions)
            masses.append(mass)
            rho_means.append(float(np.array(rho).mean()))

    with open("outputs/compact_dims_vs_mass.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["mass", "compact_dimensions", "rho_mean"])
        for i in range(len(masses)):
            w.writerow([masses[i], n_compacts[i], rho_means[i]])
    print("Saved outputs/compact_dims_vs_mass.csv")

    return masses, n_compacts

# ── Run C: Formation Phase Diagram ─────────────────────────────────────────

def run_c():
    print("\n=== Run C: Formation Phase Diagram ===")
    results = []

    for mass_init in [5.0, 10.0, 20.0]:
        for spin in [0.0, 0.5, 0.9]:
            h = TopologicalHorizon(topology="sphere", radius=mass_init / 2.0,
                                    mesh_resolution=30, mass_solar=mass_init, spin=spin)
            h.build_mesh()
            rho = jnp.array(h.info_density_grid)
            n = h.mesh_resolution
            transition_time = None
            t = 0.0; dt = 0.05; mass = mass_init

            for step in range(4000):
                infall = 0.1
                rho_np = np.array(rho)
                h.info_density_grid = rho_np
                if h.topology == "sphere":
                    if h.transition_if_needed():
                        transition_time = t
                rho = jax_infall(rho, h.twist_param, n, dt, infall)
                mass += infall * dt; t += dt
                if transition_time is not None and step > 100:
                    break

            results.append({
                "mass_init": mass_init, "spin": spin,
                "transition_time": transition_time if transition_time is not None else -1.0,
                "topology_after": h.topology
            })
            tt_str = f"{transition_time:.0f}" if transition_time is not None else "None"
            print(f"  M={mass_init} a*={spin} -> transition={tt_str}s topo={h.topology}")

    with open("outputs/phase_diagram.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["mass_init", "spin", "transition_time", "topology_after"])
        w.writeheader(); w.writerows(results)
    print("Saved outputs/phase_diagram.csv")
    return results

# ── Run D: Gravitational Wave Burst ────────────────────────────────────────

def run_d():
    print("\n=== Run D: Gravitational Wave Burst ===")
    h = TopologicalHorizon(topology="sphere", radius=10.0, mesh_resolution=40, mass_solar=10.0)
    h.build_mesh()
    rho = jnp.array(h.info_density_grid)
    n = h.mesh_resolution
    t = 0.0; dt = 0.05; mass = 10.0

    for step in range(1000):
        infall = 0.1 if t < 50 else 0.5
        rho_np = np.array(rho)
        h.info_density_grid = rho_np
        h.transition_if_needed()

        if t < 50:
            h.compact_dimensions = 2
            delta_n_prev = 0
        elif abs(t - 50) < dt:
            h.compact_dimensions = 2
            delta_n_prev = h.update_compact_dimensions()

        rho = jax_infall(rho, h.twist_param, n, dt, infall)
        mass += infall * dt; t += dt

        if abs(t - 50) < 0.1:
            print(f"  Jump at t=50s: infall 0.1->0.5 M_sun/s")

    h.update_compact_dimensions()
    delta_n = 1
    t_gw, h_plus, h_cross = h.emit_gravitational_wave(delta_n=delta_n, duration=2.0, dt=1e-3)

    with open("outputs/gravitational_waveform.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["time", "h_plus", "h_cross"])
        for i in range(len(t_gw)):
            w.writerow([t_gw[i], h_plus[i], h_cross[i]])
    print("Saved outputs/gravitational_waveform.csv")

    return t_gw, h_plus, h_cross

# ── Run E: Non-Thermal Hawking Spectrum ────────────────────────────────────

def run_e():
    print("\n=== Run E: Non-Thermal Hawking Spectrum ===")
    h = TopologicalHorizon(topology="klein_bottle", twist_param=1.5, radius=10.0,
                            mesh_resolution=40, mass_solar=10.0)
    h.build_mesh()
    rho = h.info_density_grid.copy()

    np.random.seed(7)
    for _ in range(5):
        cx = np.random.randint(0, 40)
        cy = np.random.randint(0, 40)
        i_arr, j_arr = np.meshgrid(np.arange(40), np.arange(40), indexing="ij")
        d = np.sqrt((i_arr - cx) ** 2 + (j_arr - cy) ** 2)
        rho += 0.3 * np.exp(-(d ** 2) / (2 * (4) ** 2))
    h.info_density_grid = np.clip(rho, 0, 1)

    h.winding_numbers = [2, 3, 5]
    freqs = np.logspace(10, 25, 2000)
    spectrum = h.hawking_spectrum(freqs)

    with open("outputs/radiation_spectrum.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["frequency", "power"])
        for i in range(len(freqs)):
            w.writerow([freqs[i], spectrum[i]])
    print("Saved outputs/radiation_spectrum.csv")

    return freqs, spectrum

# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    t0_all = time.time()

    h_a, times_a, grads_a, topos_a, masses_a = run_a()
    masses_b, n_comp_b = run_b()
    phase_c = run_c()
    t_gw, hp, hc = run_d()
    freqs_e, spec_e = run_e()

    elapsed = time.time() - t0_all
    print(f"\nAll runs completed in {elapsed:.1f}s")
    print(f"  Run A: {len(times_a)} samples, transition: {len(h_a._transition_history)} events")
    print(f"  Run B: compact dims tracked to n={max(n_comp_b)}")
    trans_count = sum(1 for r in phase_c if r["transition_time"] > 0)
    print(f"  Run C: {trans_count}/{len(phase_c)} configurations transitioned")
    print(f"  Run D: GW waveform generated ({len(t_gw)} samples)")
    print(f"  Run E: radiation spectrum ({len(freqs_e)} bins)")
