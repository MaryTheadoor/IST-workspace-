# Quantum Vacuum and Plasma Analogues in IST

**Date:** 2026-06-04  
**Context:** Mapping Zhang et al. (2025) and Timmis et al. (2026) onto the directed numbers framework

---

## Summary

Two recent experimental/theoretical papers probe nonlinear responses in extreme electromagnetic environments. Both are table-top analogues of the processes IST describes in black hole horizons and cosmological scales — the same directed numbers algebra (compression, expansion, associator, temporal twist) governs all of them.

---

## 1. Zhang et al. (2025) — Semi-Classical Quantum Vacuum in 3D

**Paper:** *Computational modelling of the semi-classical quantum vacuum in 3D*

### What They Did

Implemented a 3D numerical solver (within the OSIRIS PIC code) for the Heisenberg-Euler effective Lagrangian, enabling real-time simulation of vacuum birefringence and four-wave mixing in realistic laser pulses.

### Key Results

- Benchmarked vacuum birefringence against analytical theory — deviations ≤ 3%
- Simulated four-wave mixing with three non-coplanar Gaussian pulses:
  - The interaction region is an **ellipsoid**, not a cube (plane-wave assumption fails)
  - Astigmatism in the output beam directly tied to asymmetry of the overlap region
  - **Off-shell harmonics** appear transiently — momentum conserved but not energy
  - Output third harmonic's peak starts stationary, then moves at ≈ 0.99c

### IST Interpretation

The Heisenberg-Euler Lagrangian is an effective theory of virtual electron-positron loops. In IST, those loops are **directed zero pairs** $0_\uparrow 0_\downarrow$ that are compressed and expanded by the laser fields.

The polarization and magnetization of the vacuum become, in IST, the **net associator charge $\Xi$** induced by the external fields. The four-wave mixing output is a third-harmonic signal — in IST, this corresponds to a **triple associator** $[x, y, z]$ where three incoming directed numbers (the three laser pulses) combine to produce a new directed number (the signal).

The off-shell harmonics seen in the simulation are exactly the **non-associative intermediate products** that do not satisfy energy-momentum conservation as classical waves, but do satisfy the directed number algebra.

### Mapping

| Heisenberg-Euler Concept | IST Analogue |
|--------------------------|--------------|
| Virtual $e^+e^-$ pairs | Directed zero pairs $\langle 0_\uparrow 0_\downarrow \rangle$ |
| Polarization $P$, Magnetization $M$ | Net associator charge $\Xi$ |
| Four-wave mixing signal | Triple associator $[x, y, z]$ |
| Off-shell harmonics | Non-associative intermediate products |
| Nonlinear coupling $\xi$ | $\alpha/\phi^2$ |

---

## 2. Timmis et al. (2026) — Relativistic Plasma Harmonics

**Paper:** *Efficiency-optimized relativistic plasma harmonics for extreme fields*

### What They Did

Experimental demonstration of efficient high-order harmonic generation (up to 47th order, > 9 mJ in XUV) from a relativistic oscillating plasma surface — the "coherent harmonic focusing" (CHF) concept.

### Key Results

- Achieved the theoretically predicted slow efficiency decay $\eta_n \propto n^{-8/3}$
- Harmonic beam divergence grows rapidly with intensity
- Spectrospatial modulations appear — evidence of a curved plasma surface (dent) that can focus the harmonics
- CHF boost scales as $I_{\text{CHF}}/I \propto a_0^3$, potentially pushing multi-PW lasers into the $10^{23}$–$10^{29}$ W/cm² regime — approaching the Schwinger limit

### IST Interpretation

The coherent harmonic focusing concept is a **classical analogue of the time crystal** we simulated in Plan 10. A periodically driven plasma surface (by the laser's electric field) produces a train of attosecond pulses — that's a driven time crystal. In IST, the Klein bottle horizon with twisted $T_+$ produces an **undriven** time crystal.

The plasma density scale length control (via DPM contrast) is the experimental knob that tunes the **topological information $I_{\text{topo}}$** of the plasma surface. The efficiency roll-over regime ($I > 10^{20}$ W/cm²) corresponds to entering the **associator-dominated phase** where $\Xi$ overwhelms the classical response. The observed spectrospatial modulations are the direct signature of **non-associative mixing**.

### Mapping

| Plasma Concept | IST Analogue |
|---------------|--------------|
| Oscillating plasma surface | Driven time crystal $\delta_{\text{tc}}$ |
| Harmonic generation | Associator-mediated mixing $\Xi$ |
| Density scale length | Topological information $I_{\text{topo}}$ |
| Spectrospatial modulations | Non-associative product interference |
| CHF boost $\propto a_0^3$ | Cubic associator term $\phi^{-2} x^3$ |

---

## 3. Unified Ladder of Emergent Phenomena

The same directed numbers algebra describes every scale:

| Scale | System | Dominant IST Term | Observable |
|-------|--------|-------------------|------------|
| Quantum vacuum (Zhang) | Virtual $e^+e^-$ pairs | Directed zero pairs $\langle 0_\uparrow 0_\downarrow \rangle$ | Birefringence, four-wave mixing |
| Relativistic plasma (Timmis) | Oscillating electron surface | Time crystal $\delta_{\text{tc}}$ + associator $\Xi$ | High harmonics, CHF |
| Black hole horizon (IST Plan 10) | Klein bottle topology | $\Xi$ and $\delta_{\text{tc}}$ | Persistent oscillation, non-thermal spectrum |
| Cosmological dark energy (Plan 7) | Hubble scale | $\delta_{\text{tc}}$ running | $H(z)$ modulation |

---

## 4. Proposed Numerical Experiment

We could use the directed numbers runtime (Plan 9) to simulate the Zhang et al. four-wave mixing setup, replacing the Heisenberg-Euler polarization with our associator term:

1. Initialize three DirectedNumber threads representing the three laser pulses
2. Apply Omega compression at the overlap region
3. Expand via Omega_inv with the associator coupling $\alpha/\phi^2$
4. Measure the output third harmonic signal and compare to Zhang et al. predictions

This would test whether the associator term reproduces the observed off-shell harmonic generation without needing the full QED effective Lagrangian.

---

## References

- Zhang et al. (2025). *Computational modelling of the semi-classical quantum vacuum in 3D.*
- Timmis et al. (2026). *Efficiency-optimized relativistic plasma harmonics for extreme fields.*
- IST Plan 6 — Unified Topological Mass Formula
- IST Plan 9 — Directed Numbers Runtime
- IST Plan 10 — Time Crystal Simulation
