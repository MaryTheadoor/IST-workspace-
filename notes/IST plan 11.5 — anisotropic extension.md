# Plan 11.5: Anisotropic Hubble & Directed Numbers Cosmological Simulation

## Status
Extends Plan 11 after successful isotropic fit (tension reduced to 0.29σ log-periodic, 0.97σ linear).

## Plan 11 Results (Recap)

| Model | H0 [km/s/Mpc] | Tension w/ SH0ES | χ²/dof | Oscillation params |
|-------|---------------|----------------------|--------|---------------------|
| ΛCDM | 70.35 ± 0.93 | 1.94σ | 22.88/58 | — |
| Log-periodic | 71.00 ± 6.81 | **0.29σ** | 21.52/55 | ε=0.136, Δ=1.54, φ=−3.14 |
| Redshift-linear | 76.41 ± 3.37 | **0.97σ** | 19.51/55 | ε=0.242, z_c=1.41, φ=−2.92 |

**Key finding:** Oscillatory dark energy reduces the Hubble tension below 2σ, satisfying the Plan 11 objective.

---

## Phase 2A: Anisotropic Extension — Direction-Dependent Hubble Parameter

### Motivation
Plan 11 fitted an **isotropic** oscillatory model (same modulation in all sky directions). However, the IST substrate is intrinsically **anisotropic**:

1. **Klein bottle topology** breaks global isotropy — the twist axis defines a preferred direction (see `main/ist_v5_3_topology_substrate.md:280–298`).
2. The **associator field Ξ(r)** (Plan 7, `notes/IST plan 7 (topological cosmology).md:17–27`) is not uniform — it varies with the large-scale structure and the distribution of directed-number threads.
3. The **directed numbers runtime** (`code/directed_numbers.py:431–501`) encodes parity via `UP`/`DOWN` axes on the substrate. The `TemporalThread` with `twist_on_shift=True` flips parity across the Klein bottle seam, creating a **cosmic dipole** — a direction-dependent modulation of the expansion rate.
4. The time-crystal term δ_tc (Plan 7:27) couples to the associator charge Ξ. Since Ξ varies spatially, δ_tc should also vary with sky direction.

### Observable Prediction
If the Klein bottle has a preferred axis (the "twist axis"), then the Hubble parameter should show a dipolar modulation:
$$H_0(\theta) = H_0^{\text{iso}} + H_0^{\text{dip}} \cos\theta$$
where θ is the angle from the twist axis. This is analogous to the reported "cosmic dipole" in the CMB (∼0.0012 amplitude, Planck 2018) and in large-scale structure (Secrest et al. 2021, radio sources).

### IST Prediction for Dipole Amplitude
From the master equation (Plan 7:17–19):
$$M_{\text{eff}}(r) = \frac{\hbar c}{\ell(r)} \left( \frac{f}{2\pi} I_{\text{topo}}(r) + \frac{\alpha}{\phi^2} \Xi(r) + \delta_{\text{tc}}(r) \right)$$

The time-crystal term couples to the effective expansion rate:
$$H_{\text{eff}}^2 = \frac{8\pi G}{3} \rho_{\text{eff}}, \quad \rho_{\text{eff}} = \frac{M_{\text{eff}}}{V_{\text{Hubble}}}$$

For a direction-dependent associator field Ξ(θ, φ) (from the directed numbers thread grid), we predict:
$$\frac{\Delta H_0}{H_0} \sim \frac{\alpha}{\phi^2} \cdot \frac{\Xi_{\text{dipole}}}{I_{\text{topo}}} \sim \frac{\alpha}{\phi^2} \cdot \left(\frac{\text{variation in thread density}}{\text{mean thread density}}\right)$$

Using the running coupling curve from `code/cross_reference_running_coupling.py` (Ξ/I_topo^1.5 scaling across QCD → galaxy → Hubble), the expected dipole amplitude is on the order of ε_dipole ∼ 10⁻³ to 10⁻² — **within the sensitivity of current SNe Ia and BAO data**.

### Tasks

#### Task A1: Compile Sky-Coordinate Data
- Combine Pantheon+ SNe Ia (1048 SNe with sky positions) with BAO data.
- For initial test: use SNe Ia binned by sky hemisphere (North/South, East/West, or by dipole direction).
- **Reference data:** Pantheon+ sample (Scolnic et al. 2022), BAO compilations (SDSS/BOSS/eBOSS).

#### Task A2: Implement Anisotropic Fit
In `code/anisotropic_hubble.py`:
```python
def hz_osc_anisotropic(z, ra, dec, H0, Om_m, eps, Delta, phi, H_dip, ra_axis, dec_axis):
    # Compute angle θ between SN direction and dipole axis
    cos_theta = sky_angle(ra, dec, ra_axis, dec_axis)
    H0_eff = H0 * (1 + H_dip * cos_theta)
    # Same log-periodic form but with direction-dependent H0
    return hz_osc_log(z, H0_eff, Om_m, eps, Delta, phi)
```

#### Task A3: Fit and Compare
- Fit isotropic vs anisotropic oscillatory model.
- Compute significance of dipole term (Δχ², p-value).
- Compare fitted dipole direction to known anomalies (CMB dipole, radio dipole, quasar dipole).

#### Task A4: Link to Directed Numbers
- Map the fitted dipole direction (ra_axis, dec_axis) to the substrate's twist axis.
- Compare fitted dipole amplitude (H_dip) to the associator charge variation predicted by the directed numbers thread grid.

### Expected Deliverables
| File | Description |
|------|-------------|
| `code/anisotropic_hubble.py` | Anisotropic H(z) fitting script |
| `code/outputs/anisotropic_fit.png` | Sky map of best-fit H0 variation |
| `code/outputs/anisotropic_params.txt` | Dipole direction, amplitude, significance |
| `data/sne_sky_coords.csv` | SNe Ia positions + distance moduli (if data available) |

---

## Phase 2B: Directed Numbers Cosmological Simulation

### Motivation
Plan 11 used a **phenomenological** oscillatory model. The next step is to **simulate** the full cosmology from the directed numbers substrate, bottom-up:

1. Build a 3D grid of **TemporalThread** objects (from `code/directed_numbers.py:431–501`).
2. Each grid cell represents a Hubble-scale patch with local associator charge Ξ(x) and time-crystal amplitude δ_tc(x).
3. Evolve the grid forward in time using Omega/Omega_inv compression-expansion cycles (`code/directed_numbers.py:267–274`).
4. The time-crystal oscillation naturally emerges from the TemporalThread closed-loop condition (Axiom 2.18, `supplementary/directed_numbers_zero_point_operators_v0_8_1.md:167–173`).
5. The anisotropic dipole emerges from the spatial variation of the associator field across the thread grid.

### Mapping from Plan 11 Parameters to Directed Numbers

| Plan 11 Parameter | Directed Numbers Counterpart | Reference |
|-------------------|------------------------------|-----------|
| ε (oscillation amplitude) | Associator charge density ∮_thread [x,y,z] | `directed_numbers.py:286–290` |
| Δ (log-period) | Twist period of TemporalThread | `directed_numbers.py:442,469` |
| φ (phase at z=0) | Boundary condition at t=0 slice | `directed_numbers.py:469–501` |
| H0 (Hubble constant) | Mean expansion rate = n_cycles / t_Hubble | time_crystal_simulation.py:42–132 |
| Dipole direction | Klein bottle twist axis | `main/ist_v5_3...md:280–298` |
| Ωm (matter density) | Thread density × (f/2π) I_topo / total | `topological_cosmology.py:107–122` |

### Simulation Architecture

```
┌─────────────────────────────────────────────────────┐
│            Thread Grid (N × N × N)                  │
│  Each cell = TemporalThread with local:             │
│    - thread_density(x)  →  ρ_m(x)                   │
│    - associator_charge(x) → Ξ(x) → DM enhancement   │
│    - time_crystal_phase(x) → δ_tc(x) → DE modulation│
│    - twist_direction(x) → preferred axis             │
├─────────────────────────────────────────────────────┤
│  Evolution (each time step = one T_plus operation): │
│    1. Infall: inject perturbation at random sites    │
│    2. Compress: Omega() on cells above threshold     │
│    3. Expand: Omega_inv() when compressed > limit    │
│    4. Twist: parity flip on Klein bottle seam        │
│    5. Measure: log H_eff(x), Ξ(x), δ_tc(x)         │
├─────────────────────────────────────────────────────┤
│  Output: time series of                              │
│    - Global H(z) (compare to Plan 11 fit)            │
│    - Sky H0 map (compare to anisotropic fit)         │
│    - Power spectrum of expansion fluctuations        │
└─────────────────────────────────────────────────────┘
```

### Calibration to Physical Units

From `code/topological_cosmology.py:102–122`:
- Hubble scale: L_H = c / H0 ≈ 4.28 Gpc
- Critical density: ρ_crit = 3H0^2 / (8πG)
- One simulation time step ↔ physical time dt = t_Hubble / n_steps
- Grid spacing ↔ physical distance dx = L_H / n_grid

From `code/time_crystal_simulation.py:42–132`:
- Dominant frequency from FFT of the time-crystal simulation: f_sim = 0.00125 (simulation units)
- In physical units: f_phys = f_sim / dt (Hz)
- Hubble-time calibration: t_Hubble = 13.8 Gyr → f_phys ≈ f_sim × (n_steps / t_Hubble)

### Tasks

#### Task B1: Build Thread Grid
```python
def build_cosmological_grid(n_grid=16, n_steps=2000, H0_seed=73.0):
    grid = np.empty((n_grid, n_grid, n_grid), dtype=object)
    for ijk in ...
        grid[ijk] = TemporalThread(
            elements=[DirectedNumber(amplitude=..., parity=...)],
            twist_on_shift=(ijk near Klein bottle seam)
        )
    return grid
```

#### Task B2: Evolution Engine
```python
def evolve_grid(grid, n_steps, compress_threshold, expand_threshold):
    H_history = []
    Xi_history = []
    for step in range(n_steps):
        inject_perturbations(grid)
        compressed = compress_above_threshold(grid, compress_threshold)
        if total_compressed > expand_threshold:
            grid = expand_and_twist(grid)
        H_eff = measure_effective_expansion(grid)
        Xi_mean = measure_associator_field(grid)
        H_history.append(H_eff)
        Xi_history.append(Xi_mean)
    return H_history, Xi_history
```

#### Task B3: Extract Cosmological Observables
- Global H(z): mean expansion rate vs time → convert to H(z) curve
- Sky H0 map: per-cell expansion rate projected onto celestial sphere
- Oscillation power spectrum: FFT of H(t) → compare to Plan 11 log-periodic fit
- Dipole significance: spherical harmonic ℓ=1 component of sky H0 map

### Expected Deliverables
| File | Description |
|------|-------------|
| `code/directed_numbers_cosmology.py` | Full thread grid cosmological simulation |
| `code/outputs/cosmo_grid_hz.png` | Simulated H(z) vs ΛCDM and oscillatory fits |
| `code/outputs/cosmo_grid_skymap.png` | Simulated sky H0 map (Mollweide or orthographic) |
| `code/outputs/cosmo_grid_power.png` | Power spectrum of expansion fluctuations |
| `code/outputs/cosmo_grid_params.txt` | Calibrated simulation parameters |

---

## Cross-References to IST Core Documentation

| Concept | Document | Lines |
|---------|----------|-------|
| Master equation (cosmological form) | `notes/IST plan 7 (topological cosmology).md` | 17–27 |
| Xi & delta_tc computation | `code/topological_cosmology.py` | 102–122 |
| Associator [x,y,z] definition | `code/directed_numbers.py` | 286–290 |
| TemporalThread with twist | `code/directed_numbers.py` | 431–501 |
| Compression-expansion cycle | `supplementary/directed_numbers_zero_point_operators_v0_8_1.md` | 119–139 |
| Temporal consistency condition | `supplementary/directed_numbers_zero_point_operators_v0_8_1.md` | 167–173 |
| Time crystal simulation (Plan 10) | `code/time_crystal_simulation.py` | 42–132 |
| Klein bottle topology in cosmology | `main/ist_v5_3_topology_substrate.md` | 280–298 |
| Golden ratio scaling ε ∼ α/φ² | `code/topological_cosmology.py` | 40 (COUPLING) |
| Running coupling curve (Ξ vs I_topo) | `code/cross_reference_running_coupling.py` | — |
| Variabile gravity G_eff ∝ ρ_fold^(1/φ) | `main/ist_v5_3_topology_substrate.md` | 197–203 |

---

## Execution Instructions

1. Create branch `feature/plan11.5-anisotropic-cosmology`.
2. Write `code/anisotropic_hubble.py` (Phase 2A).
3. Write `code/directed_numbers_cosmology.py` (Phase 2B).
4. Run both scripts, verify outputs.
5. Update `README.md` with Plan 11.5 section.
6. Commit with message: `"feat: Plan 11.5 – anisotropic Hubble fitting + directed numbers cosmological simulation"`.

## Dependencies
- All Plan 11 dependencies (numpy, scipy, matplotlib)
- `code/directed_numbers.py` (Plan 9 runtime)
- `code/time_crystal_simulation.py` (Plan 10, for calibration reference)
- `code/topological_cosmology.py` (Plan 7, for master equation constants)
