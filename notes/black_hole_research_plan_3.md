# Research Plan 3: Beyond the Horizon — Topological Signatures & Observables

## Objective
Bridge from simulation to observation: compute testable signatures of IST black hole topology (Klein bottle horizon, compact dimension dynamics, topological flickering) and design observational strategies for LIGO, LISA, Event Horizon Telescope, and future gamma-ray observatories.

---

## Theme A: Gravitational Wave Signatures of Topological Flickering

### A.1 Stochastic GW Background from Flickering Horizons
- Compute the power spectral density of the flickering regime (Run A: 2667 transitions over ~170s).
- Use the transition timeseries to generate a synthetic stochastic GW background.
- Compare to LIGO O5 sensitivity curve. Predict minimum detectable distance.

### A.2 GW Echoes from Topological Phase Transitions
- When the horizon flips sphere→Klein bottle, the ringdown waveform changes (different QNM frequencies).
- Simulate a "double ringdown": initial QNM from perturbation, then a second burst when topology flips.
- Search for echo-like features in the ringdown that cannot be explained by standard GR echoes.

### A.3 Burst Waveform Catalog from Dimensional Shifts
- Run Monte Carlo over Δn = 1, 2, 3 with varying κ.
- Generate waveform template bank for matched-filter searches.
- Estimate detection horizon for LIGO A+ and LISA.

---

## Theme B: Electromagnetic Counterparts

### B.1 Non-Thermal Hawking Spectrum Predictions
- For stellar-mass BHs (1–100 M_sun), compute the full non-thermal spectrum.
- Identify the strongest spectral lines from winding numbers Lk = 1, 2, 3, 5.
- Predict line-to-continuum ratio for primordial black hole searches (Fermi, AMEGO, e-ASTROGAM).

### B.2 Jet Launching from Compact Dimension Asymmetry
- If n_compact grows asymmetrically (different winding numbers on different axis hemispheres), the metric develops a preferred axis.
- This could naturally launch relativistic jets along the axis of maximal compact dimension gradient.
- Model: jet power ∝ |∇n_compact| × ρ_I^2.
- Compare to Blandford-Znajek: does IST predict a different jet efficiency for the same BH spin?

### B.3 Shadow Morphology at EHT Resolution
- Klein bottle horizons have a different null geodesic structure than Schwarzschild/Kerr.
- Ray-trace photons through the Klein bottle metric (approximate as Kerr + topological correction).
- Predict EHT-observable deviations: shadow size, asymmetry, photon ring substructure.
- Focus on M87* and Sgr A*.

---

## Theme C: Formal Theory Development

### C.1 Derivation of γ_crit from First Principles
- γ_crit is currently an empirical threshold. Can it be derived from IST axioms?
- Hypothesis: γ_crit = (φ / α) × (M_Pl / ℓ_P) in natural units.
- Test against simulation: does this match the observed threshold behavior?

### C.2 Coupling Between Compact Dimensions
- Currently n_compact dimensions are independent. In a more complete theory, winding numbers w_i interact.
- Propose a Hamiltonian term: H_int = Σ_{i<j} g_ij · w_i · w_j · cos(θ_i - θ_j).
- Simulate coupled winding dynamics: do they synchronize or chaotically decorrelate?

### C.3 Information Leakage & the Black Hole Information Paradox
- In IST, information is stored in the topology (winding numbers), not destroyed.
- As the BH evaporates, winding numbers unwind, releasing information in spectral lines.
- Compute the information capacity of the winding number space: I_max = Σ_i log₂(2|w_i|).
- Does this satisfy the Page curve? Simulate information entanglement entropy over evaporation.

### C.4 Connection to Subjective Time (from IST v5.3)
- The plan mentions "subjective time and complex surface encoding."
- Develop the mapping between horizon winding numbers and the complex phase of the wavefunction.
- Hypothesis: the Klein bottle's non-orientability enables a natural arrow of time (one-way information flow).

---

## Theme D: Computational Infrastructure

### D.1 Parallelized Monte Carlo Pipeline
- Extend simulation to sweep over 100+ BH parameters (mass, spin, infall rate, initial topology).
- Store results in SQLite database for post-hoc analysis.
- Implement in JAX with vmap for automatic batching over parameter space.

### D.2 Interactive 3D Visualization
- Build a web-based (Three.js or pyvista) interactive viewer for the Klein bottle horizon.
- Allow rotation, zoom, density slice, and real-time evolution of info density.
- Export frames for video: "topology_flickering.mp4".

### D.3 Validation Suite
- Unit tests for gradient computation (analytic gradient on sphere should be zero for uniform density).
- Integration tests: transition does not occur below γ_crit, does occur above.
- Regression tests: same random seed produces identical results.

---

## Expected Outputs

| Item | Description |
|------|-------------|
| `analysis/gw_flickering_psd.md` | Stochastic background power spectrum |
| `analysis/double_ringdown.md` | Echo waveform from topology flip |
| `analysis/non_thermal_hawking.md` | Line spectrum predictions |
| `analysis/eht_shadow.md` | Klein bottle shadow morphology |
| `analysis/information_paradox.md` | Page curve from winding numbers |
| `code/bh_parameter_sweep.py` | Parallelized MC pipeline |
| `figures/` | All publication-quality figures |

## Timeline
- **Theme A** (GW signatures): 2–3 sessions
- **Theme B** (EM counterparts): 2–3 sessions
- **Theme C** (Formal theory): 3–4 sessions
- **Theme D** (Infrastructure): ongoing
