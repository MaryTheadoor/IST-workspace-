# Plan 10: Web Data Acquisition and Pipeline Integration

## Objective
Develop a systematic workflow to search for, retrieve, and integrate publicly available astronomical datasets into the IST computational framework. The goal is to validate and refine the unified mass formula (Plan 6), the running coupling (Plan 7), and the directed numbers runtime (Plan 9) using real observational data.

## Scope
- Identify relevant datasets (microlensing, large‑scale structure, gravitational waves).
- Implement scripts to download and preprocess data.
- Convert raw observations into the directed numbers thread representation.
- Use the runtime to compute associator charges \(\Xi\) and information content \(I_{\text{topo}}\).
- Compare IST predictions with data (e.g., PBH mass functions, rotation curves, Hubble expansion).

## Phase 1: Data Source Identification

### 1.1 Primary Targets

| Dataset | Description | Relevance to IST |
|---------|-------------|------------------|
| **OGLE** (Optical Gravitational Lensing Experiment) | Microlensing light curves toward Galactic bulge and Magellanic Clouds | PBH mass function, timescale distributions |
| **Subaru HSC M31** (Sugiyama et al. 2026) | 12 PBH candidates with posterior samples | Direct input for \(M_{\text{PBH}} \propto \alpha/\phi^2 \cdot \Xi\) |
| **DECam AMPM** (Key et al. 2026a) | “Phoebe” light curve | Sub‑lunar PBH mass validation |
| **COSMOS‑Web** (Hatamnia et al. 2026) | Density maps, galaxy properties (stellar mass, SFR) up to \(z \sim 7\) | Environmental quenching → associator charge maps |
| **Gaia DR3** | Parallaxes, proper motions, photometry | Source star distances, lens proper motions |
| **LIGO/Virgo/KAGRA** (GWTC‑3, O4) | Gravitational wave events | Waveform echoes from topological transitions (time crystal signature) |
| **NANOGrav / IPTA** | Pulsar timing arrays (nHz GW background) | Cluster merger echoes predicted by \(\delta_{\text{tc}}\) |
| **Planck / DESI / Euclid** | CMB, BAO, weak lensing | Dark energy equation of state, comparison with \(\delta_{\text{tc}}\) modulation |

### 1.2 Secondary Targets
- SMASH DR2 (LMC stellar catalog) – for source star characterization.
- TESS / Kepler flare catalogs – to rule out false positives (already used in Key et al.).
- SDSS DR16 / DES DR2 – additional LSS data for redshift shells.

## Phase 2: Data Retrieval Methods

### 2.1 Automated Download Scripts
Implement Python modules in `code/data_fetch/`:

- `fetch_ogle.py` – use OGLE public archive (rsync or HTTP) to download light curves for long‑duration events.
- `fetch_hsc_m31.py` – download posterior samples from Sugiyama et al. (2026) supplementary material (Zenodo/arXiv).
- `fetch_decam.py` – access NOIRLab Astro Data Archive (via `astroquery` or direct API) for AMPM raw images or processed light curves.
- `fetch_cosmos_web.py` – retrieve density maps and galaxy catalogs from COSMOS‑Web public release (MAST).
- `fetch_ligo.py` – use `gwpy` or `ligo.skymap` to query GWTC‑3 event data.

### 2.2 Data Formats
Standardise all data into:
- **Light curves**: CSV with columns `time (MJD)`, `flux`, `flux_err`, `bandpass`.
- **Density maps**: FITS or HDF5 with 2D arrays per redshift slice.
- **Posterior samples**: HDF5 or text files with parameter chains.

## Phase 3: Preprocessing and Conversion to IST Representation

### 3.1 Microlensing Data
For each event:
1. Fit the finite‑source point‑lens (FS‑PL) model using the directed numbers runtime (replace standard magnification with `DNumber` multiplication? Actually, magnification is classical; we need to map event parameters to lens mass and distance.
2. Convert the best‑fit mass \(M\) into an associator charge: \(\Xi = M \cdot \frac{2\pi \ell_P}{\hbar c} \cdot \frac{\phi^2}{\alpha} \cdot \frac{1}{f_{\text{topo}}}\) (derived from the master equation).
3. Store as a `Thread` with a single `DirectedNumber` having amplitude \(\Xi\) and parity according to the lens’s motion direction (UP for outgoing, DOWN for infalling).

### 3.2 Large‑Scale Structure Data
1. For each galaxy in COSMOS‑Web, compute local overdensity \(\log(1+\delta)\).
2. Use the known stellar mass to estimate \(I_{\text{topo}}\) (baryonic information).
3. Solve the master equation for \(\Xi\): \(\Xi = \frac{\phi^2}{\alpha} \left( M - \frac{f}{2\pi} I_{\text{topo}} \right)\) (neglecting \(\delta_{\text{tc}}\) at galaxy scales).
4. Assign \(\Xi\) to a `Thread` representing that galaxy’s environmental influence.

### 3.3 Gravitational Wave Data
For candidate merger events:
1. Extract ringdown frequencies and any reported echo delays.
2. Use the time crystal term \(\delta_{\text{tc}}\) to predict the expected echo period \(\tau_{\text{echo}} = 2\pi R_s / c\) (for black holes) or the cluster‑scale period for PTA.
3. Compare with data; if an event shows unexplained periodic structure, fit to the IST modulation formula.

## Phase 4: Integration into Existing Pipeline

### 4.1 New Modules
- `code/data_pipeline.py` – orchestrates fetch → preprocess → store → analyse.
- `code/ist_observational_fit.py` – uses directed numbers runtime to compute \(\Xi\) and \(I_{\text{topo}}\) from data, then compares to master equation.

### 4.2 Validation Workflows

| Test | Data | IST Prediction | Metric |
|------|------|----------------|--------|
| PBH mass function | HSC M31 candidates | \(M_{\text{PBH}} \approx \frac{\alpha}{\phi^2} \Xi\) with \(\Xi\) quantised | Posterior overlap |
| Rotation curve | COSMOS‑Web galaxies | \(v_c(r) \propto \sqrt{G (M_{\text{bar}} + (\alpha/\phi^2)\Xi(r)) / r}\) | \(\chi^2\) fit |
| Hubble expansion | Pantheon+ SNe Ia | \(H(z)\) with \(\delta_{\text{tc}}\) modulation | Bayesian evidence |

### 4.3 Outputs
- `outputs/data/` – downloaded raw data (gitignored).
- `outputs/ist_fits/` – best‑fit \(\Xi\) maps, light curve residuals, etc.
- `figures/` – comparison plots (e.g., observed PBH mass distribution vs. IST quantised spectrum).

## Phase 5: Agent Execution Plan

### Task 1: Set up data fetching infrastructure
- Create `code/data_fetch/` directory.
- Write `fetch_hsc_m31.py` to download the Sugiyama et al. posterior samples (available at DOI or arXiv source files).
- Write `fetch_cosmos_web.py` to download the density maps (public via STScI MAST).

### Task 2: Preprocessing scripts
- `preprocess_microlensing.py` – converts light curves to directed number threads.
- `preprocess_lss.py` – maps galaxy overdensities to \(\Xi\) threads.

### Task 3: Integration and fitting
- Extend `black_hole_simulation.py` to read external event parameters and compute \(\Xi\).
- Implement `compute_xi_from_mass()` using the master equation.
- Run fits on the HSC M31 candidate list and produce a table of inferred \(\Xi\) values.

### Task 4: Validation and visualisation
- Plot the PBH candidate mass distribution alongside the predicted quantised \(\Xi\) spectrum (with \(\alpha/\phi^2\) spacing).
- Overlay COSMOS‑Web quenching efficiencies versus \(\Xi\) maps.
- Save figures to `outputs/figures/`.

### Task 5: Documentation
- Write `code/README_data_integration.md` explaining how to reproduce the data acquisition and fitting.
- Update `README.md` with a new section “Observational constraints on IST”.

## Expected Deliverables

| File | Description |
|------|-------------|
| `code/data_fetch/fetch_hsc_m31.py` | Downloads PBH posterior samples |
| `code/data_fetch/fetch_cosmos_web.py` | Downloads LSS density maps |
| `code/preprocess_microlensing.py` | Converts events to directed number threads |
| `code/preprocess_lss.py` | Converts galaxy catalogs to \(\Xi\) threads |
| `code/ist_observational_fit.py` | Main fitting routine |
| `outputs/figures/pbh_mass_histogram.png` | Observed vs IST‑predicted mass distribution |
| `outputs/figures/quenching_vs_xi.png` | Environmental quenching efficiency vs \(\Xi\) |
| `outputs/data/hsc_pbh_posteriors.h5` | Local cache of posterior samples |
| `code/README_data_integration.md` | Reproducibility guide |

## Dependencies
- `astroquery` (for MAST, NOIRLab archives)
- `gwpy` (for LIGO data)
- `h5py` (for HDF5)
- `requests` / `wget` (for generic downloads)
- `numpy`, `scipy`, `matplotlib`

## Notes for the Agent
- Many datasets are large (GB scale). Use streaming downloads and chunked processing.
- Respect data usage policies (cite original papers when publishing results).
- The HSC M31 posterior samples are likely available as supplementary material to Sugiyama et al. (2026). If not directly accessible, use the summary statistics from their Table VII as a starting point.
- For COSMOS‑Web, the density maps are available as FITS images in the public release (MAST). The agent can use `astropy.io.fits` to read them.

## Commit Message
`"feat: Plan 10 – data integration pipeline for observational validation"`