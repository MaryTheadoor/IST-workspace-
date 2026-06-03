# Plan 10: Computing the Associator Charge from PBH Candidates & Simulating a Time Crystal Horizon

## Objective
Use the newly implemented Directed Numbers runtime (Plan 9) to:
1. **Compute the associator charge \(\Xi\)** for the PBH candidates reported by Sugiyama et al. (2026) and Key et al. (2026a).
2. **Simulate a time crystal** on a Klein bottle horizon using `TemporalThread` with periodic boundary conditions and twisted parity.
3. **Validate** that the observed PBH mass scale \(M \sim 10^{-7} M_{\odot}\) corresponds to a quantised associator charge \(\Xi = 1\) (or small integer) when inserted into the unified mass formula.

## Deliverables

| File | Description |
|------|-------------|
| `code/associator_from_PBH.py` | Script to load PBH candidate data (mass posteriors) and compute \(\Xi\) using the unified mass formula. |
| `code/time_crystal_simulation.py` | Standalone simulation of a twisted `TemporalThread` with periodic compression/expansion; outputs oscillation plots. |
| `code/outputs/associator_histogram.png` | Histogram of inferred \(\Xi\) values for the 12 Subaru HSC candidates. |
| `code/outputs/associator_vs_mass.png` | Scatter plot of \(\Xi\) vs. PBH mass, with theoretical line \(\Xi = (\phi^2/\alpha) \cdot (M / M_{\text{fund}})\). |
| `code/outputs/time_crystal_oscillations.png` | Time series of information density on a Klein bottle patch showing persistent periodic modulation. |
| `code/outputs/time_crystal_fft.png` | Fourier power spectrum of the oscillation, peak at the predicted frequency from twist period. |
| `README.md` | Update with links to new results. |

## Task 1: Compute Associator Charge from PBH Data

### 1.1 Data Input
- Use the posterior mass distributions from Sugiyama et al. (2026) and Key et al. (2026a). For simplicity, we approximate each candidate by its median mass and \(1\sigma\) uncertainty.
- If the raw posterior samples are not available, we will use the reported \(M_{\text{PBH}}\) values from Table VII of Sugiyama et al. (2026) and the Phoebe mass \(0.032^{+0.227}_{-0.027} M_{\oplus}\) from Key et al.

### 1.2 Formula
From Plan 6 (unified mass formula) for a PBH (no baryonic component, negligible time‑crystal term):

\[
M = \frac{\hbar c}{\ell_P} \cdot \frac{\alpha}{\phi^2} \cdot \Xi
\]

where \(\ell_P = \sqrt{\hbar G/c^3}\) and \(\frac{\hbar c}{\ell_P} = M_{\text{Planck}} c^2\)? Actually \(\frac{\hbar c}{\ell_P} = M_{\text{Planck}} c^2\). But we prefer dimensionless:

\[
\frac{M}{M_{\text{Planck}}} = \frac{\alpha}{\phi^2} \cdot \Xi
\]

Thus:

\[
\Xi = \frac{\phi^2}{\alpha} \cdot \frac{M}{M_{\text{Planck}}}
\]

with \(\alpha = 1/137.036\), \(\phi = (1+\sqrt{5})/2 \approx 1.618\), \(M_{\text{Planck}} \approx 2.176 \times 10^{-8} \, \text{kg} \approx 1.097 \times 10^{-5} M_{\odot}\) (in solar masses).

### 1.3 Compute \(\Xi\) for each candidate
- Convert candidate mass to Planck units.
- Compute \(\Xi\) and its uncertainty via error propagation.
- Histogram: should peak near integer values (1, 2, …) if quantisation holds. The observed PBH mass \(10^{-7} M_{\odot}\) corresponds to \(\Xi \approx 1\) (check: \(10^{-7} / (1.1\times 10^{-5}) \approx 0.009\); times \(\phi^2/\alpha \approx 2.618 \times 137 \approx 359\) → 0.009×359 ≈ 3.2, not 1. Wait, need to re‑derive properly.)

Let’s compute carefully:

\[
M_{\text{Planck}} \approx 1.097 \times 10^{-5} M_{\odot}
\]
\[
M_{\text{PBH}} \approx 10^{-7} M_{\odot}
\]
\[
\frac{M}{M_{\text{Planck}}} \approx 10^{-7} / 1.097\times 10^{-5} \approx 0.00912
\]
\[
\frac{\phi^2}{\alpha} \approx \frac{2.618}{0.007299} \approx 358.7
\]
\[
\Xi \approx 0.00912 \times 358.7 \approx 3.27
\]

So \(\Xi\) is about 3.27, not 1. That suggests the PBH mass is not the minimum but possibly the typical scale where \(\Xi\) averages 3–4. That is fine – we will report the distribution.

The script will compute \(\Xi\) and plot.

### 1.4 Outputs
- `associator_histogram.png`
- `associator_vs_mass.png` with theoretical line \(\Xi = (\phi^2/\alpha) \cdot (M/M_{\text{Planck}})\)

## Task 2: Simulate a Time Crystal on a Klein Bottle Horizon

### 2.1 Setup
- Create a `TemporalThread` with `twisted=True` (parity flips each time step).
- Initialise the thread with a single `DirectedNumber` (amplitude 1.0, parity UP).
- Apply a periodic drive: every 2 time steps, compress (`Omega`) then expand (`Omega_inv`) but with a phase lag to create oscillation.
- Alternatively, use a simpler model: the thread is a closed loop (periodic boundary) of length \(L\). The product of all elements around the loop must satisfy the closed‑loop condition (Axiom 2.18). This forces the thread to oscillate.

### 2.2 Simulation Steps
1. Create a `TemporalThread` with length \(L = 10\) (10 time steps per loop).
2. Randomly initialise amplitudes and parities (subject to product = \(1^\uparrow\) or \((-1)^\downarrow\)).
3. Evolve the thread using `T_plus()` and `T_minus()` while applying `Omega` and `Omega_inv` at fixed intervals.
4. Record the total information `info_total()` after each step.
5. After an initial transient, check for periodic modulation.

### 2.3 Analysis
- Compute Fourier transform of the information time series.
- Peak frequency should correspond to the twist period (2 steps per full cycle if twisted).
- If oscillations persist without external driving, that is the time crystal.

### 2.4 Outputs
- `time_crystal_oscillations.png` – time series of I_total.
- `time_crystal_fft.png` – power spectrum.

## Task 3: Integration and Validation

- Ensure that the associator charge computed from PBH data matches the value of \(\Xi\) measured in the time crystal simulation for a stable knot (should be an integer or half-integer).
- Cross‑reference with the running coupling from Plan 7: \(\alpha_{\text{topo}}\) at the PBH scale should be consistent with the value derived from the associator distribution.

## Execution Instructions (Agent)

1. Create branch `feature/plan10-associator-timecrystal`.
2. Write `code/associator_from_PBH.py` – load PBH mass data (hardcoded from the papers) and compute \(\Xi\). Generate plots.
3. Write `code/time_crystal_simulation.py` – implement the twisted thread with periodic drive. Use `directed_numbers.py` from Plan 9.
4. Run both scripts and save outputs.
5. Update `README.md` with new section “Plan 10: Associator Charge from PBH Candidates and Time Crystal Simulation”.
6. Commit with message: `"feat: Plan 10 – associator from PBH data & time crystal simulation"`.

## Dependencies
- Existing `directed_numbers.py` (Plan 9)
- `numpy`, `matplotlib`
- `scipy.fft` for FFT

## Notes
- If the PBH posterior samples are not accessible, use the median values and approximate errors. The goal is a proof‑of‑concept, not a precise measurement.
- The time crystal simulation may require tuning of the drive parameters to achieve persistent oscillation. If no oscillation is found, try a longer thread length or a different drive pattern (e.g., random compressions).

## Commit Message
`"feat: Plan 10 – associator from PBH data and time crystal simulation"`