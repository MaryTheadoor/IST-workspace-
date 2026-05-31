# Execution Plan: Black Hole Topology (Klein Bottle & Information Knots)

## Objective
Implement and simulate black hole horizons as non‑orientable topological spaces (Klein bottle) within the IST framework, linking to subjective time and complex surface encoding.

## Tasks

### 1. Extend ist_toolkit_v2.py
- Add class `TopologicalHorizon` with attributes:
  - `topology` (choices: "sphere", "torus", "klein_bottle")
  - `twist_param` (float, for Klein bottle)
  - `info_density_grid` (2D array on mesh)
- Methods:
  - `build_mesh()` – construct a triangulated surface using `pyvista` or `trimesh`
  - `compute_entropy()` – returns corrected Bekenstein‑Hawking entropy
  - `evolve_info(dt)` – update info density using IST Hamiltonian on the non‑orientable mesh
  - `waveform_signal()` – compute ringdown Fourier modes

### 2. GPU‑Accelerated Simulation
- Use `cupy` or `jax` to evolve the info density on the mesh.
- For Klein bottle: apply periodic boundary conditions with a sign flip for the twist coordinate.
- Run for 1000 time steps, record entropy and leakage rate.

### 3. Information Knot Visualization
- Extract closed loops of high info density (threshold = mean + 2σ).
- Compute linking numbers (using `scipy.spatial` or `topetex`).
- Render 3D plot of the Klein bottle with colour‑coded information currents. Save as `outputs/klein_info_knot.png`.

### 4. Push to GitHub
- Commit new code, simulation results, and plot.
- Create a brief summary in `README.md` under a new section “Black hole topology insights”.

## Expected Output
- Updated `ist_toolkit_v2.py`
- `outputs/klein_info_knot.png`
- `outputs/entropy_comparison.csv`
- Git commit with message `"feat: Klein bottle horizon with info knots"`