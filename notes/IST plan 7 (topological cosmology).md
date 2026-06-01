# Plan 7: Topological Cosmology – From Primordial Remnants to Galaxies to Dark Energy

## Based on Plan 5 & 6 Results
- Unified master equation validated for proton and black hole scales.
- Associator term `(α/φ²) Ξ` provides extra binding (dark matter effect).
- Time crystal term `δ_tc` provides periodic modulation (potential dark energy).
- Directed numbers algebra and compression/expansion operators are the foundation.

## Objective
Apply the unified topological mass formula to cosmology:
1. Simulate primordial black hole evaporation → stable remnants as dark matter.
2. Model galactic rotation curves using topological binding (associator term).
3. Derive cosmic expansion from the time‑crystal term at Hubble scale.

## Master Equation (Cosmological Form)

\[
M_{\text{eff}}(r) = \frac{\hbar c}{\ell(r)} \cdot \left( \frac{f}{2\pi} I_{\text{topo}}(r) + \frac{\alpha}{\phi^2} \Xi(r) + \delta_{\text{tc}}(r) \right)
\]

Where `r` is the scale (from sub‑Planckian to Hubble). Each term has a specific role:

| Term | Role at small scale (BH) | Role at galactic scale | Role at cosmological scale |
|:---|:---|:---|:---|
| `(f/2π) I_topo` | Main black hole mass | Stellar + gas mass | Baryonic matter |
| `(α/φ²) Ξ` | Associator correction (0.1% level) | **Dark matter binding** | Large‑scale structure |
| `δ_tc` | Time crystal (periodic modulation) | Negligible? | **Dark energy** (Hubble expansion) |

## Phases

### Phase A: Primordial Black Hole Remnants (Dark Matter)

#### A.1 Setup
- Simulate early universe density fluctuations (power spectrum from Planck).
- Form primordial black holes (PBHs) in mass range `10¹² – 10¹⁵ g` (asteroid‑mass).
- Use the directed numbers evaporation model (Ω/Ω⁻¹) from Plan 5.

#### A.2 Evaporation & Remnants
- Each PBH evaporates, but directed zeros (information knots) remain as stable remnants.
- Remnant mass = `(α/φ²) Ξ` times fundamental quantum (∼10⁻⁸ kg). This is the dark matter particle mass.
- Compute remnant abundance: number density = initial PBH number density × (1 – fraction fully evaporated).

#### A.3 Outputs
- `outputs/pbh_remnant_abundance.csv` – mass spectrum and number density.
- `outputs/dark_matter_mass.txt` – predicted DM particle mass (should be ∼10⁻⁸ kg).
- `outputs/dm_abundance_vs_redshift.png` – evolution.

### Phase B: Galactic Rotation from Topological Binding

#### B.1 Model a Spiral Galaxy
- Represent galaxy as a 2D disk (spiral arms as twist lines) with a central bulge.
- Embed in a non‑orientable substrate (Klein bottle topology for the halo).
- The effective gravitational potential includes the associator term `(α/φ²) Ξ` integrated over the galactic information content.

#### B.2 Compute Rotation Curve
- Use the master equation at galactic scale: `ℓ_gal = 1 kpc` (scale length).
- `I_topo_gal` = sum of baryonic mass (stars, gas) in topological information units.
- `Ξ_gal` = total associator charge from dark matter remnants (from Phase A) plus contribution from disk structure.
- `δ_tc` set to zero at galactic scale (negligible).
- Solve for circular velocity: `v_c(r) = sqrt( G M_eff(r) / r )`.

#### B.3 Compare to Observed Galaxies
- Fit to rotation curves of M33, Milky Way, NGC 3198 (classic examples).
- Use no free parameters: `α = 1/137.036`, `φ = 1.618`, `Ξ_gal` computed from remnant distribution.
- Evaluate goodness of fit (χ²) against NFW profile.

#### B.4 Outputs
- `outputs/galaxy_rotation_fit.png` – observed vs predicted rotation curves.
- `outputs/galaxy_best_fit_params.txt` – inferred `Ξ_gal` for each galaxy.
- `outputs/topological_binding_profile.png` – extra acceleration as function of radius.

### Phase C: Cosmic Expansion (Dark Energy)

#### C.1 Cosmological Scale Master Equation
- Treat universe as a 4D Klein bottle (or higher‑genus) with Hubble length `ℓ_H = c/H_0`.
- Total mass–energy of universe: `M_univ = (3c^2)/(8πG) H_0^{-2}` (critical density).
- Write the master equation for the whole universe:
  \[
  M_{\text{univ}} = \frac{\hbar c}{\ell_H} \left( \frac{f_{\text{univ}}}{2\pi} I_{\text{topo,univ}} + \frac{\alpha}{\phi^2} \Xi_{\text{univ}} + \delta_{\text{tc,univ}} \right)
  \]
- Identify `δ_tc,univ` as the **dark energy** term. It is constant (time crystal period >> Hubble time) or slowly varying.

#### C.2 Derive Hubble Expansion
- From the master equation, the effective energy density `ρ_eff = M_eff / (volume)`.
- The time‑crystal term contributes a constant `ρ_Λ` that drives acceleration.
- Predict equation of state `w = p/ρ` from time‑crystal dynamics (should be close to -1 but with small oscillations).

#### C.3 Compare to Observational Data
- Use Planck CMB + BAO + SNe Ia data to constrain `δ_tc` amplitude and frequency.
- Compute predicted `H(z)` and compare to observed Hubble diagram.

#### C.4 Outputs
- `outputs/cosmological_fit.png` – H(z) vs redshift with best‑fit δ_tc.
- `outputs/dark_energy_eos.txt` – w(z) prediction.
- `outputs/universe_topology_inferred.txt` – inferred f_univ and I_topo,univ.

## Integration & Synthesis

### Phase D: Unified Cosmological Simulation (Optional)
- Run a large‑scale simulation (box size ~1 Gpc) with directed numbers as the underlying substrate.
- Initial conditions: Gaussian fluctuations → structure formation → remnants act as dark matter → time‑crystal term drives expansion.
- Output final matter power spectrum and compare to observational data (SDSS, DESI).

### Phase E: Write Internal Paper
- Title: "Topological Cosmology: Dark Matter as Directed‑Number Remnants, Dark Energy as Time‑Crystal Term"
- Sections: Introduction, Formalism, Phase A (PBH remnants), Phase B (galactic rotation), Phase C (cosmic expansion), Synthesis, Predictions.

## Deliverables Summary

| File | Description |
|:---|:---|
| `outputs/pbh_remnant_abundance.csv` | Remnant mass spectrum |
| `outputs/dark_matter_mass.txt` | Predicted DM particle mass |
| `outputs/galaxy_rotation_fit.png` | Rotation curves with topological binding |
| `outputs/galaxy_best_fit_params.txt` | Ξ_gal for each galaxy |
| `outputs/cosmological_fit.png` | H(z) fit with dark energy term |
| `outputs/dark_energy_eos.txt` | Equation of state prediction |
| `notes/topological_cosmology_paper_v1.md` | Internal paper |
| `README.md` | Update with new cosmological section |
| `code/topological_cosmology.py` | Unified simulation script (optional) |

## Execution Notes
- Use existing `directed_numbers.py` and `black_hole_simulation.py` as base.
- For Phase A, start with simple PBH evaporation (already in Plan 5) and count remnants.
- For Phase B, use rotation curve data from references (e.g., Sofue 2016). Fit with `scipy.optimize.curve_fit`.
- For Phase C, use publicly available Hubble data (e.g., from Pantheon+). Compute χ².
- All constants: `α = 1/137.036`, `φ = (1+sqrt(5))/2`, `ħc = 197.327 MeV·fm`, `G`, `H0 = 67.4 km/s/Mpc`.

## Commit Message
`"feat: Topological Cosmology (Plan 7) – dark matter from PBH remnants, galactic binding, dark energy from time crystal"`