# Plan 11: Resolving the Hubble Tension with Time‑Crystal Dark Energy

## Objective
Use the directed numbers thread calculus (Plan 9) to derive a phenomenological model of oscillatory dark energy, then fit it to cosmological data (BAO, cosmic chronometers, Pantheon+ SNe Ia) and show that the Hubble tension can be reduced to below 2σ. This provides a testable, falsifiable prediction unique to IST.

## Background
- The Hubble tension: early‑universe measurements (Planck CMB) give \(H_0 \approx 67.4\) km/s/Mpc; late‑universe measurements (SH0ES) give \(H_0 \approx 73.0\) km/s/Mpc.
- In IST, the time‑crystal term \(\delta_{\text{tc}}\) in the unified mass formula (Plan 6) leads to a periodic modulation of the effective dark energy density.
- The modulation period is tied to the twist of the universal Klein bottle topology; its amplitude is related to the golden ratio and the associator charge \(\Xi\).
- For this plan, we first treat the modulation phenomenologically, then map the best‑fit parameters to the directed numbers runtime predictions.

## Deliverables

| File | Description |
|------|-------------|
| `code/oscillatory_dark_energy.py` | Python script implementing the oscillatory ΛCDM model and fitting to data. |
| `code/outputs/hubble_fit_plan11.png` | Plot of \(H(z)\) data with best‑fit ΛCDM and oscillatory model. |
| `code/outputs/chi2_comparison.txt` | χ² values for ΛCDM vs. oscillatory model, and reduction in Hubble tension. |
| `code/outputs/oscillation_parameters.txt` | Best‑fit parameters (\(\varepsilon\), \(z_c\) or \(\Delta\), \(\phi\)). |
| `notes/hubble_tension_resolution_IST.md` | Internal note explaining the result and its link to directed numbers / time crystal. |
| `README.md` | Update with summary of Plan 11 findings. |

## Tasks

### Task 1: Implement the Oscillatory Dark Energy Model

In `code/oscillatory_dark_energy.py`, define:

- Standard flat ΛCDM:  
  \(H(z) = H_0 \sqrt{\Omega_m (1+z)^3 + (1-\Omega_m)}\)

- Oscillatory extension (two versions, choose one for fitting):
  1. **Log‑periodic** (preferred, from scale invariance):  
     \(H(z) = H_0 \sqrt{ \Omega_m (1+z)^3 + (1-\Omega_m) \left[1 + \varepsilon \cos\left( \frac{2\pi}{\Delta} \ln(1+z) + \phi \right) \right] }\)
  2. **Simple redshift‑linear** (easier for initial fit):  
     \(H(z) = H_0 \sqrt{ \Omega_m (1+z)^3 + (1-\Omega_m) \left[1 + \varepsilon \sin\left( \frac{2\pi z}{z_c} + \phi \right) \right] }\)

- Use `scipy.optimize.curve_fit` or `emcee` to fit \(H_0\), \(\Omega_m\), and oscillation parameters (\(\varepsilon\), \(\Delta\) or \(z_c\), \(\phi\)) to the dataset.

### Task 2: Compile Observational Data

The agent should download or use local copies of:

- **Cosmic chronometers** (30+ measurements of \(H(z)\) from passively evolving galaxies, up to \(z\sim2\)).
- **BAO** (Baryon Acoustic Oscillation) measurements (e.g., from SDSS, BOSS, eBOSS, DESI early data) as \(H(z)r_s\) or isotropic BAO.
- **Pantheon+** SNe Ia (or a compressed version) – if heavy, use the binned \(H(z)\) from SNe.

For simplicity, we can start with a publicly available \(H(z)\) compilation (e.g., from the “Hubble parameter data” repository). The agent should load the data and prepare it with error bars.

### Task 3: Fit Both Models

- Fit ΛCDM (2 parameters: \(H_0\), \(\Omega_m\)) to the data.
- Fit oscillatory model (3 additional parameters: \(\varepsilon\), \(\Delta\) or \(z_c\), \(\phi\)).
- Compute χ² and AIC/BIC to assess improvement.

### Task 4: Quantify Reduction in Hubble Tension

- Compute the best‑fit \(H_0\) from the oscillatory model and compare to:
  - Planck 2018 value (\(67.4 \pm 0.5\))
  - SH0ES value (\(73.0 \pm 1.0\))
- Report the residual tension in σ.

### Task 5: Link to Directed Numbers / Time Crystal

- From the best‑fit oscillation period (\(\Delta\) or \(z_c\)), compute the corresponding frequency in the time‑crystal simulation (Plan 10). If the simulation used dimensionless steps, calibrate using the Hubble time (\(t_H \approx 13.8\) Gyr).
- Check if the best‑fit amplitude \(\varepsilon\) is consistent with the golden‑ratio scaling \(\varepsilon \sim \alpha/\phi^2 \approx 0.00285\) times the number of e‑foldings? Or a derived value from the associator. The agent should report whether the fitted \(\varepsilon\) is plausible within IST.

### Task 6: Write Internal Note and Update README

- `notes/hubble_tension_resolution_IST.md` should include:
  - Summary of the Hubble tension.
  - Description of the oscillatory model and its IST motivation.
  - Results (χ², best‑fit parameters, tension reduction).
  - Connection to directed numbers and future predictions (e.g., direction‑dependent Hubble parameter).
- Update `README.md` with a new section “Plan 11 – Resolving the Hubble Tension”.

## Execution Instructions (Agent)

1. Create branch `feature/plan11-hubble-tension`.
2. Write `code/oscillatory_dark_energy.py` using `numpy`, `scipy.optimize`, and `matplotlib`.
3. Place the observational data in `data/` (download from public sources; if not available, use mock data with realistic errors to illustrate the method).
4. Run the script and generate outputs.
5. Commit and push with message: `"feat: Plan 11 – oscillatory dark energy for Hubble tension"`.

## Dependencies
- Python 3.9+
- `numpy`, `scipy`, `matplotlib`, `emcee` (optional for MCMC)

## Expected Outcome

If the oscillatory model provides a better fit than ΛCDM (by Δχ² > 6 for 3 extra parameters), and the fitted \(H_0\) moves toward the SH0ES value while still being consistent with BAO/CMB constraints on \(\Omega_m\) and sound horizon, then this would be a noteworthy result. Even a modest improvement, when combined with the theoretical motivation from IST, could form the basis for a publication.

## Next Steps After Plan 11
- Extend to anisotropic fits (direction‑dependent modulation) using actual sky coordinates of SNe and BAO.
- Compare to the “cosmic dipole” and other large‑scale anomalies.
- Implement the full directed numbers cosmological simulation (instead of phenomenological fit).

## References
- Planck 2018 results (Astron. Astrophys. 641, A6, 2020).
- SH0ES: Riess et al. (2022, ApJ, 934, L7).
- Cosmic chronometers: Moresco et al. (2022, JCAP, 07, 019).
- IST Plan 6 (Unified mass formula), Plan 7 (Cosmological running), Plan 9 (Directed numbers runtime), Plan 10 (Time crystal simulation).