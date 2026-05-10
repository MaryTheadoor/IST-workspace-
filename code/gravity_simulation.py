"""
================================================================================
IST GRAVITY SIMULATOR - Dimensional Collapse N-Body
================================================================================
Scalable simulation of gravity as emergent dimensional collapse pressure.

Physics:
  - No 1/r^2 force programmed
  - Attraction emerges from substrate's tendency to minimize dimensionality
  - Gaussian kernel: V_ij = -A * c_i * c_j * exp(-d^2 / (2*sigma^2))
  - Cost: c_i = rho_i / D(rho_i),  D(rho) = 2 + (phi - 2)*tanh(rho/rho_0)

Implementation:
  - Cell-list spatial hashing for O(N) neighbor queries
  - Vectorized numpy force evaluation
  - Damped Euler integration
  - Parallel comparison with Newtonian gravity

Usage:
  python gravity_simulation.py --n-particles 1000 --steps 500
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import json
import time
from pathlib import Path

# ───────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ───────────────────────────────────────────────────────────────────────────────
PHI = (1.0 + np.sqrt(5.0)) / 2.0

# ───────────────────────────────────────────────────────────────────────────────
# CORE PHYSICS
# ───────────────────────────────────────────────────────────────────────────────

def effective_dimension(rho, rho_0=1.0):
    """D(rho) = 2 + (phi - 2) * tanh(rho / rho_0)"""
    return 2.0 + (PHI - 2.0) * np.tanh(rho / rho_0)


def dimensional_cost(rho, rho_0=1.0):
    """c(rho) = rho / D(rho)"""
    D = effective_dimension(rho, rho_0)
    return rho / D


def ist_force_magnitude(d2, ci, cj, A, sigma2):
    """Magnitude of IST pairwise force: F = A * ci * cj * d / sigma^2 * exp(-d^2/(2*sigma^2))"""
    # Avoid division by zero with softening
    d2 = np.where(d2 < 1e-10, 1e-10, d2)
    d = np.sqrt(d2)
    return A * ci * cj * d / sigma2 * np.exp(-d2 / (2.0 * sigma2))


def newtonian_force_magnitude(d2, mi, mj, G, epsilon2=1e-4):
    """Standard Newtonian gravity with softening."""
    d2 = np.where(d2 < epsilon2, epsilon2, d2)
    return G * mi * mj / d2


# ───────────────────────────────────────────────────────────────────────────────
# SPATIAL HASHING (CELL LIST)
# ───────────────────────────────────────────────────────────────────────────────

class CellList:
    """2D cell-list for O(N) neighbor finding with periodic boundaries."""

    def __init__(self, positions, box_size, cutoff):
        self.positions = positions
        self.box_size = box_size
        self.cutoff = cutoff
        self.n_particles = len(positions)
        self.n_cells = max(1, int(np.floor(box_size / cutoff)))
        self.cell_size = box_size / self.n_cells
        self._build()

    def _build(self):
        # Assign particles to cells
        self.cell_indices = np.floor(self.positions / self.cell_size).astype(np.int32)
        self.cell_indices = self.cell_indices % self.n_cells  # periodic wrap

        # Flatten cell coords to scalar cell id
        self.cell_ids = self.cell_indices[:, 0] * self.n_cells + self.cell_indices[:, 1]

        # Sort particles by cell id
        self.sort_order = np.argsort(self.cell_ids)
        self.sorted_ids = self.cell_ids[self.sort_order]

        # Build cell start/end arrays
        self.cell_starts = np.full(self.n_cells * self.n_cells, -1, dtype=np.int32)
        self.cell_ends = np.full(self.n_cells * self.n_cells, -1, dtype=np.int32)

        if self.n_particles > 0:
            unique_cells, start_indices = np.unique(self.sorted_ids, return_index=True)
            self.cell_starts[unique_cells] = start_indices
            end_indices = np.empty_like(start_indices)
            end_indices[:-1] = start_indices[1:]
            end_indices[-1] = self.n_particles
            self.cell_ends[unique_cells] = end_indices

        self.sorted_positions = self.positions[self.sort_order]

    def neighbor_pairs(self):
        """Yield arrays of (i, j, dx, dy, d2) for all pairs within cutoff."""
        cutoff2 = self.cutoff ** 2
        i_list, j_list, dx_list, dy_list, d2_list = [], [], [], [], []

        for px in range(self.n_cells):
            for py in range(self.n_cells):
                cell_id = px * self.n_cells + py
                start = self.cell_starts[cell_id]
                if start < 0:
                    continue
                end = self.cell_ends[cell_id]

                for dx_cell in (-1, 0, 1):
                    for dy_cell in (-1, 0, 1):
                        nx = (px + dx_cell) % self.n_cells
                        ny = (py + dy_cell) % self.n_cells
                        nbr_id = nx * self.n_cells + ny

                        # Avoid double counting
                        if nbr_id < cell_id:
                            continue

                        nbr_start = self.cell_starts[nbr_id]
                        if nbr_start < 0:
                            continue
                        nbr_end = self.cell_ends[nbr_id]

                        idx_a = self.sort_order[start:end]
                        idx_b = self.sort_order[nbr_start:nbr_end]
                        pos_a = self.positions[idx_a]
                        pos_b = self.positions[idx_b]

                        if nbr_id == cell_id:
                            # Same cell: upper triangle only
                            na = len(pos_a)
                            for ii in range(na):
                                for jj in range(ii + 1, na):
                                    dpos = pos_b[jj] - pos_a[ii]
                                    dpos -= self.box_size * np.rint(dpos / self.box_size)
                                    d2_val = float(dpos[0]**2 + dpos[1]**2)
                                    if d2_val < cutoff2:
                                        i_list.append(int(idx_a[ii]))
                                        j_list.append(int(idx_a[jj]))
                                        dx_list.append(float(dpos[0]))
                                        dy_list.append(float(dpos[1]))
                                        d2_list.append(d2_val)
                        else:
                            # Different cells: all pairs
                            na, nb = len(pos_a), len(pos_b)
                            for ii in range(na):
                                dpos = pos_b - pos_a[ii]
                                dpos -= self.box_size * np.rint(dpos / self.box_size)
                                d2 = np.sum(dpos ** 2, axis=1)
                                mask = d2 < cutoff2
                                nbrs = np.where(mask)[0]
                                for jj in nbrs:
                                    i_list.append(int(idx_a[ii]))
                                    j_list.append(int(idx_b[jj]))
                                    dx_list.append(float(dpos[jj, 0]))
                                    dy_list.append(float(dpos[jj, 1]))
                                    d2_list.append(float(d2[jj]))

        if len(i_list) == 0:
            return (np.array([], dtype=np.int32), np.array([], dtype=np.int32),
                    np.array([]), np.array([]), np.array([]))

        return (np.array(i_list, dtype=np.int32), np.array(j_list, dtype=np.int32),
                np.array(dx_list), np.array(dy_list), np.array(d2_list))


# ───────────────────────────────────────────────────────────────────────────────
# N-BODY SIMULATOR
# ───────────────────────────────────────────────────────────────────────────────

class ISTGravitySimulator:
    """Dimensional collapse N-body simulator."""

    def __init__(self, n_particles=1000, box_size=100.0, seed=42,
                 A=200.0, sigma=4.0, rho_0=1.0, dt=0.02, damping=0.90,
                 n_clusters=2, cluster_fraction=0.5, cluster_density_ratio=50.0,
                 newtonian_G=1.0, mode='ist'):
        self.n_particles = n_particles
        self.box_size = box_size
        self.A = A
        self.sigma = sigma
        self.sigma2 = sigma ** 2
        self.rho_0 = rho_0
        self.dt = dt
        self.damping = damping
        self.newtonian_G = newtonian_G
        self.mode = mode  # 'ist' or 'newtonian'
        self.rng = np.random.default_rng(seed)

        # Initialize particle densities and positions
        self._init_particles(n_clusters, cluster_fraction, cluster_density_ratio)

        # Precompute costs / masses
        if mode == 'ist':
            self.costs = dimensional_cost(self.rho, self.rho_0)
        else:
            # For Newtonian, use density as proxy mass
            self.masses = self.rho.copy()

        self.trajectory = [self.positions.copy()]
        self.velocities_history = [np.zeros_like(self.velocities)]
        self.energy_history = [self.compute_energy()]
        self.time_history = [0.0]

    def _init_particles(self, n_clusters, cluster_fraction, cluster_density_ratio):
        """Initialize positions: dense clusters + uniform background."""
        n_cluster = int(self.n_particles * cluster_fraction)
        n_bg = self.n_particles - n_cluster

        positions = []
        rho = []

        # Background: uniform random
        if n_bg > 0:
            bg_pos = self.rng.random((n_bg, 2)) * self.box_size
            positions.append(bg_pos)
            rho.append(np.ones(n_bg))

        # Clusters: Gaussian blobs
        if n_cluster > 0:
            per_cluster = n_cluster // n_clusters
            for c in range(n_clusters):
                center = self.rng.random(2) * self.box_size * 0.6 + self.box_size * 0.2
                cluster_pos = center + self.rng.normal(0, self.sigma * 0.5, (per_cluster, 2))
                cluster_pos = cluster_pos % self.box_size  # periodic wrap
                positions.append(cluster_pos)
                rho.append(np.full(per_cluster, cluster_density_ratio))

        self.positions = np.vstack(positions)
        self.rho = np.concatenate(rho)
        self.velocities = np.zeros((self.n_particles, 2))

        # Ensure arrays match expected size (trim if needed)
        if len(self.positions) > self.n_particles:
            self.positions = self.positions[:self.n_particles]
            self.rho = self.rho[:self.n_particles]

    def compute_forces(self):
        """Compute forces using cell-list spatial hashing."""
        cutoff = 3.0 * self.sigma
        cell_list = CellList(self.positions, self.box_size, cutoff)
        i, j, dx, dy, d2 = cell_list.neighbor_pairs()

        forces = np.zeros((self.n_particles, 2))

        if len(i) == 0:
            return forces

        if self.mode == 'ist':
            ci = self.costs[i]
            cj = self.costs[j]
            fmag = ist_force_magnitude(d2, ci, cj, self.A, self.sigma2)
        else:
            mi = self.masses[i]
            mj = self.masses[j]
            fmag = newtonian_force_magnitude(d2, mi, mj, self.newtonian_G)

        d = np.sqrt(d2)
        d = np.where(d < 1e-10, 1e-10, d)
        fx = fmag * dx / d
        fy = fmag * dy / d

        # Accumulate (Newton's 3rd law)
        np.add.at(forces[:, 0], i, fx)
        np.add.at(forces[:, 1], i, fy)
        np.add.at(forces[:, 0], j, -fx)
        np.add.at(forces[:, 1], j, -fy)

        return forces

    def step(self):
        """Damped Euler integration step."""
        forces = self.compute_forces()
        self.velocities += forces * self.dt
        self.velocities *= self.damping
        self.positions += self.velocities * self.dt
        self.positions = self.positions % self.box_size  # periodic boundaries

    def compute_energy(self):
        """Compute total potential + kinetic energy."""
        ke = 0.5 * np.sum(self.velocities ** 2)

        cutoff = 3.0 * self.sigma
        cell_list = CellList(self.positions, self.box_size, cutoff)
        i, j, dx, dy, d2 = cell_list.neighbor_pairs()
        pe = 0.0

        if len(i) > 0:
            d = np.sqrt(d2)
            if self.mode == 'ist':
                ci = self.costs[i]
                cj = self.costs[j]
                pe = -self.A * np.sum(ci * cj * np.exp(-d2 / (2.0 * self.sigma2)))
            else:
                mi = self.masses[i]
                mj = self.masses[j]
                pe = -self.newtonian_G * np.sum(mi * mj / d)

        return pe + ke

    def cluster_analysis(self):
        """Simple clustering metric: mean nearest-neighbor distance for top 20% densest."""
        dense_mask = self.rho >= np.percentile(self.rho, 80)
        dense_pos = self.positions[dense_mask]
        if len(dense_pos) < 2:
            return np.nan
        # Pairwise distances
        diff = dense_pos[:, np.newaxis, :] - dense_pos[np.newaxis, :, :]
        diff -= self.box_size * np.rint(diff / self.box_size)
        dists = np.sqrt(np.sum(diff ** 2, axis=2))
        dists[dists == 0] = np.inf
        nnd = np.min(dists, axis=1)
        return np.mean(nnd)

    def run(self, n_steps, save_every=10, progress_every=100):
        """Run simulation for n_steps."""
        t0 = time.time()
        for step in range(n_steps):
            self.step()
            if step % save_every == 0:
                self.trajectory.append(self.positions.copy())
                self.velocities_history.append(self.velocities.copy())
                self.energy_history.append(self.compute_energy())
                self.time_history.append((step + 1) * self.dt)
            if step % progress_every == 0 and step > 0:
                elapsed = time.time() - t0
                rate = progress_every / elapsed
                print(f"  Step {step}/{n_steps} | {rate:.1f} steps/sec | Energy: {self.energy_history[-1]:.2e}")
                t0 = time.time()
        print(f"Simulation complete. {n_steps} steps, {len(self.trajectory)} frames saved.")

    def save_results(self, out_dir):
        """Save trajectory, parameters, and metrics to disk."""
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        # Trajectory
        traj = np.array(self.trajectory)
        np.save(out_dir / "trajectory.npy", traj)

        # Velocities
        vels = np.array(self.velocities_history)
        np.save(out_dir / "velocities.npy", vels)

        # Parameters and metrics
        results = {
            "mode": self.mode,
            "n_particles": self.n_particles,
            "box_size": self.box_size,
            "A": self.A,
            "sigma": self.sigma,
            "rho_0": self.rho_0,
            "dt": self.dt,
            "damping": self.damping,
            "n_steps": len(self.trajectory) * 10,  # approximate
            "energy_history": [float(e) for e in self.energy_history],
            "time_history": [float(t) for t in self.time_history],
            "final_cluster_nnd": float(self.cluster_analysis()),
        }
        with open(out_dir / "results.json", "w") as f:
            json.dump(results, f, indent=2)

        print(f"Results saved to {out_dir}")

    def plot_final_state(self, save_path=None):
        """Scatter plot of final particle positions colored by density."""
        fig, ax = plt.subplots(figsize=(8, 8))
        scatter = ax.scatter(self.positions[:, 0], self.positions[:, 1],
                            c=self.rho, cmap='viridis', s=20, alpha=0.7)
        plt.colorbar(scatter, ax=ax, label='Density ρ')
        ax.set_xlim(0, self.box_size)
        ax.set_ylim(0, self.box_size)
        ax.set_aspect('equal')
        ax.set_title(f'{self.mode.upper()} | N={self.n_particles} | Final State')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        return fig

    def plot_energy(self, save_path=None):
        """Plot energy vs time."""
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(self.time_history, self.energy_history, linewidth=1.5)
        ax.set_xlabel('Time')
        ax.set_ylabel('Total Energy')
        ax.set_title(f'{self.mode.upper()} | Energy Evolution')
        ax.grid(True, alpha=0.3)
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        return fig


# ───────────────────────────────────────────────────────────────────────────────
# COMPARISON & BENCHMARK
# ───────────────────────────────────────────────────────────────────────────────

def run_comparison(n_particles=1000, n_steps=500, out_dir="gravity_outputs"):
    """Run IST and Newtonian simulations with identical initial conditions."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print(f"IST GRAVITY SIMULATION | N = {n_particles} | Steps = {n_steps}")
    print("=" * 65)

    # Shared random seed for identical ICs
    seed = 42
    shared_params = dict(n_particles=n_particles, box_size=100.0, seed=seed,
                         A=200.0, sigma=4.0, rho_0=1.0, dt=0.02, damping=0.90,
                         n_clusters=2, cluster_fraction=0.5, cluster_density_ratio=50.0)

    # IST run
    print("\n[1/2] Running IST dimensional collapse...")
    sim_ist = ISTGravitySimulator(mode='ist', newtonian_G=0.0, **shared_params)
    sim_ist.run(n_steps, save_every=10, progress_every=100)
    sim_ist.save_results(out_dir / "ist")
    sim_ist.plot_final_state(out_dir / "ist_final.png")
    sim_ist.plot_energy(out_dir / "ist_energy.png")
    ist_nnd = sim_ist.cluster_analysis()

    # Newtonian run
    print("\n[2/2] Running Newtonian gravity...")
    sim_newt = ISTGravitySimulator(mode='newtonian', newtonian_G=1.0, **shared_params)
    sim_newt.run(n_steps, save_every=10, progress_every=100)
    sim_newt.save_results(out_dir / "newtonian")
    sim_newt.plot_final_state(out_dir / "newtonian_final.png")
    sim_newt.plot_energy(out_dir / "newtonian_energy.png")
    newt_nnd = sim_newt.cluster_analysis()

    # Summary
    print("\n" + "=" * 65)
    print("COMPARISON SUMMARY")
    print("=" * 65)
    print(f"IST final cluster NND:       {ist_nnd:.3f}")
    print(f"Newtonian final cluster NND: {newt_nnd:.3f}")
    print(f"Clustering ratio (IST/Newt): {ist_nnd/newt_nnd:.3f}  (< 1 = more clustered)")
    print(f"Outputs: {out_dir.resolve()}")

    return sim_ist, sim_newt


def benchmark_scaling(particle_counts=(100, 500, 1000, 2000, 5000), steps=100):
    """Measure steps/sec vs N to verify O(N) scaling."""
    print("\n" + "=" * 65)
    print("SCALING BENCHMARK")
    print("=" * 65)
    results = []
    for N in particle_counts:
        sim = ISTGravitySimulator(n_particles=N, box_size=100.0, seed=42,
                                   A=200.0, sigma=4.0, mode='ist')
        t0 = time.time()
        for _ in range(steps):
            sim.step()
        elapsed = time.time() - t0
        rate = steps / elapsed
        results.append((N, elapsed, rate))
        print(f"  N = {N:5d} | {steps} steps in {elapsed:.3f}s | {rate:.1f} steps/sec")
    return results


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IST Gravity N-Body Simulator")
    parser.add_argument("--n-particles", type=int, default=1000, help="Number of particles")
    parser.add_argument("--steps", type=int, default=500, help="Integration steps")
    parser.add_argument("--out-dir", type=str, default="gravity_outputs", help="Output directory")
    parser.add_argument("--benchmark", action="store_true", help="Run scaling benchmark")
    args = parser.parse_args()

    if args.benchmark:
        benchmark_scaling()
    else:
        run_comparison(n_particles=args.n_particles, n_steps=args.steps, out_dir=args.out_dir)
