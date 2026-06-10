# Plan 12: Testing the Time‑Crystal Origin of the Hubble Tension – Golden Ratio, Inflationary Amplification, and 3D Simulations

## Objective
- Test the hypothesis that the observed dark energy oscillation amplitude ε is **ε = (α/φ²) × N_inflation**, where N_inflation ≈ 50–60 e‑folds.
- Determine whether the log‑periodic period Δ is equal to the golden ratio φ ≈ 1.618.
- Perform a joint fit of the oscillatory dark energy model to **Planck CMB data + BAO + cosmic chronometers** to constrain Ω_m and the sound horizon consistently.
- Run a **3D directed numbers time‑crystal simulation** to see if the amplitude amplification factor emerges naturally from the dimensionality of the substrate.

## Background
Plan 11 showed:
- A log‑periodic oscillatory dark energy model reduces the Hubble tension to <0.3σ.
- The best‑fit amplitude ε ≈ 0.136 is ≈49 times larger than the bare IST coupling α/φ² ≈ 0.00279.
- 49 is within the typical range of inflationary e‑folds (50–60), suggesting ε = (α/φ²) × N_inflation.
- The best‑fit period Δ ≈ 1.54 is close to the golden ratio φ = 1.618.

These coincidences demand rigorous testing.

## Deliverables

| File | Description |
|------|-------------|
| `code/plan12_fixed_parameters.py` | Fit log‑periodic model with Δ = φ, and with ε = α/φ² or ε free. |
| `code/plan12_joint_cmb_fit.py` | Joint MCMC fit of log‑periodic model to Planck 2018 CMB likelihood + BAO + H(z). |
| `code/plan12_3d_time_crystal.py` | 3D extension of the directed numbers time‑crystal simulation (Plan 10). |
| `code/outputs/plan12_fixed_delta_fit.png` | H(z) fit with Δ = φ. |
| `code/outputs/plan12_cmb_constraints.png` | Constraints on (Ω_m, H₀, ε, Δ) from joint fit. |
| `code/outputs/plan12_3d_tc_oscillations.png` | Information density oscillations from a 3D twisted temporal thread. |
| `notes/inflationary_amplification_hypothesis.md` | Internal note explaining ε = (α/φ²) × N_inflation. |
| `README.md` | Update with Plan 12 summary. |

## Detailed Tasks

### Task 1: Refit with Fixed Golden Ratio Period
- Modify the log‑periodic model to set Δ = φ = (1+√5)/2 ≈ 1.618.
- Fit to the same 60 H(z) data points (or extended compilation) with free parameters: H₀, Ω_m, ε, φ (but φ fixed, only Δ fixed).
- Compute χ² and tension with SH0ES.
- If χ² does not degrade significantly (Δχ² < 2), the golden ratio period is supported.

### Task 2: Test ε = (α/φ²) × N_inflation
- Define N_inflation as a free parameter with prior [40, 80].
- Set ε = (α/φ²) × N_inflation.
- Fit the model (free H₀, Ω_m, N_inflation, Δ, φ) to the H(z) data.
- Report best‑fit N_inflation and its uncertainty.
- Check whether N_inflation is consistent with independent bounds (e.g., from B‑modes, r < 0.036 ⇒ N > 50).
- This provides a direct, cross‑checkable prediction.

### Task 3: Joint Fit with Planck CMB Data
- Use publicly available Planck 2018 CMB likelihood (high‑ℓ TT, TE, EE + low‑ℓ) via `camb` and `cosmosis` or `cobaya`.
- Extend the log‑periodic model to include the CMB temperature and polarisation power spectra.
- Sample parameters: {H₀, Ω_b h², Ω_c h², τ_reio, A_s, n_s, ε, Δ, φ}. (Fix φ to 1.618 or free).
- Compare Bayesian evidence (logZ) to ΛCDM.
- Output constraints on Ω_m and the sound horizon. If Ω_m moves closer to Planck’s value (~0.31), the model is viable.

### Task 4: 3D Directed Numbers Time‑Crystal Simulation
- Extend the `TemporalThread` class to operate on a 3D cubic lattice (each cell has a thread).
- Apply twisted boundary conditions in one direction (e.g., x‑axis, with parity flip when crossing the boundary).
- Drive the system with a periodic compression/expansion cycle (as in Plan 10) but now in 3D.
- Measure the amplitude ε_3D of the resulting information density oscillation.
- Compare ε_3D to the 2D simulation result and to the fitted ε.
- Hypothesis: ε scales with the number of spatial dimensions? Or with the number of compactified dimensions? 2D gave ε ~ 0.136? Actually Plan 10 gave oscillation amplitude ~0.1 of total information. But we need to calibrate.

**Simpler approach:** In the 3D simulation, compute the power spectrum of the total information density. The amplitude at the fundamental frequency divided by the mean information density gives a dimensionless ε_sim. Compare to ε_fitted.

### Task 5: Write Internal Note and Update README
- `notes/inflationary_amplification_hypothesis.md` – explain the relation ε = (α/φ²) × N_inflation, its motivation from the directed numbers thread calculus (integration of associator over e‑folds), and how to test it.
- `README.md` – add new section “Plan 12 – Testing the Time‑Crystal Origin”.

## Execution Instructions (Agent)

1. Create branch `feature/plan12-hubble-tension-adv`.
2. Set up environment with `cobaya` or `cosmoMC` (for Planck likelihood) – if too heavy, use distance priors instead (e.g., Planck 2018 R, l_a, ω_b).
3. Implement Task 1 and Task 2 using `scipy.optimize` and `emcee`.
4. For Task 3, use compressed CMB distance priors (Ω_m, H₀, sound horizon) to avoid heavy likelihood. If possible, run a full MCMC with `cobaya`.
5. For Task 4, extend `directed_numbers.py` with a 3D lattice of `TemporalThread`s. Run for at least 10,000 steps to extract stable oscillation amplitude.
6. Generate all outputs and commit.

## Dependencies
- Existing `directed_numbers.py`, `numpy`, `scipy`, `matplotlib`
- For CMB: `camb`, `cobaya` (optional) or just use Planck distance prior data from `data/cmb_distance_priors.txt`
- For 3D simulation: `numba` (optional) for speed.

## Expected Timeline
- Tasks 1‑2: 1‑2 hours
- Task 3 (compressed priors): 1 hour; full MCMC: several hours
- Task 4 (3D simulation): 1‑2 hours (depending on grid size)

## Commit Message
`"feat: Plan 12 – golden ratio period, inflationary amplification, joint CMB fit, and 3D time crystal"`