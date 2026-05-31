import os
import time
import csv
import numpy as np
import jax.numpy as jnp
from jax import jit

os.makedirs("outputs", exist_ok=True)

def jax_evolve_step(rho, twist_param, n, dt, diffusion_coeff=0.01):
    lap = (
        jnp.roll(rho, -1, axis=0) + jnp.roll(rho, 1, axis=0)
        + jnp.roll(rho, -1, axis=1) + jnp.roll(rho, 1, axis=1)
        - 4 * rho
    ) / (2 * jnp.pi / n)**2

    u_mod = jnp.linspace(0, 2 * jnp.pi, n)
    lap = lap * (1.0 + 0.1 * twist_param * jnp.sin(u_mod)[:, None])

    rho_new = rho + diffusion_coeff * lap * dt
    rho_new = jnp.clip(rho_new, 0, 1)
    return rho_new

jax_step = jit(jax_evolve_step, static_argnames=["n", "dt", "diffusion_coeff"])


def run_simulation(topology, twist_param, radius, n_steps=1000, dt=0.05):
    from ist_toolkit_v2 import TopologicalHorizon

    h = TopologicalHorizon(
        topology=topology, twist_param=twist_param,
        radius=radius, mesh_resolution=50
    )
    vertices, faces = h.build_mesh()
    initial_entropy = h.compute_entropy()

    rho_np = h.info_density_grid.copy()
    rho = jnp.array(rho_np)
    n = h.mesh_resolution

    leakages = []
    entropies = [initial_entropy]
    info_densities = [float(rho_np.mean())]
    times = [0.0]

    t0 = time.time()
    for step in range(1, n_steps + 1):
        if topology == "klein_bottle":
            rho = jax_step(rho, twist_param, n, dt)
        else:
            rho = jax_step(rho, 0.0, n, dt)

        if step % 100 == 0:
            rho_np = np.array(rho)
            mean_rho = float(rho_np.mean())
            leakage = 1.0 - (mean_rho / info_densities[-1]) if info_densities[-1] > 0 else 0.0
            leakages.append(leakage)
            info_densities.append(mean_rho)
            entropies.append(h.compute_entropy())
            times.append(step * dt)
            elapsed = time.time() - t0
            print(f"  [{topology}] step {step}/{n_steps} | rho={mean_rho:.4f} | leakage={leakage:.6e} | dt={elapsed:.1f}s")

    elapsed = time.time() - t0
    h.info_density_grid = np.array(rho)

    return {
        "topology": topology,
        "twist_param": twist_param,
        "radius": radius,
        "n_steps": n_steps,
        "final_entropy": float(h.compute_entropy()),
        "initial_entropy": float(initial_entropy),
        "entropy_ratio": float(h.compute_entropy() / initial_entropy),
        "final_info_density": float(np.array(rho).mean()),
        "total_leakage": leakages[-1] if leakages else 0.0,
        "elapsed_seconds": elapsed,
        "steps_per_second": n_steps / elapsed if elapsed > 0 else float("inf"),
        "times": times,
        "leakages": leakages,
        "info_densities": info_densities,
        "entropies": entropies,
    }


def write_csv(results, filepath="outputs/entropy_comparison.csv"):
    fieldnames = [
        "topology", "twist_param", "radius", "n_steps",
        "initial_entropy", "final_entropy", "entropy_ratio",
        "final_info_density", "total_leakage",
        "elapsed_seconds", "steps_per_second",
    ]
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            row = {k: v for k, v in r.items() if k in fieldnames}
            writer.writerow(row)
    print(f"\nSaved {filepath}")


if __name__ == "__main__":
    configs = [
        ("sphere", 0.0, 10.0),
        ("torus", 0.0, 10.0),
        ("klein_bottle", 0.5, 10.0),
        ("klein_bottle", 1.0, 10.0),
        ("klein_bottle", 2.0, 10.0),
    ]

    all_results = []
    for topo, twist, R in configs:
        print(f"\nRunning: topology={topo}, twist={twist}, radius={R}")
        result = run_simulation(topo, twist, R, n_steps=1000)
        all_results.append(result)

    write_csv(all_results)

    print("\n=== SUMMARY ===")
    for r in all_results:
        print(f"  {r['topology']:15s} twist={r['twist_param']:.1f} | "
              f"entropy={r['initial_entropy']:.2e}->{r['final_entropy']:.2e} | "
              f"leakage={r['total_leakage']:.6e} | "
              f"{r['steps_per_second']:.1f} steps/s")
