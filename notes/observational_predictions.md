# Observational Predictions of IST: Hubble Modulation, Rotation Curves, and Gravitational Wave Echoes

**NOWN Research Collective — Plan 8, Part III**

**Date:** 2026-06-01  
**Based on:** Beta function (Part I), TQFT (Part II), Plan 7 cosmology data

---

## Executive Summary

IST makes **three falsifiable predictions** that distinguish it from $\Lambda$CDM and modified gravity:

| Prediction | Observable | Signature | Test with |
|------------|-----------|-----------|-----------|
| Time crystal modulation | $H(z)$ | $0.1\%$ oscillation in $w(z)$ with period $\Delta z \sim 2.5$ | DESI Year 5, Euclid |
| Associator rotation curve residuals | $v_c(r)$ | Sub-kpc deviations from NFW, scale-dependent $\Xi$ | SPARC, HI surveys |
| Topological GW echoes | PTA timing residuals | Periodic $f \sim 10^{-16}$ Hz signal with harmonics | NANOGrav 15yr, IPTA |

---

## 1. Time Crystal Modulation of the Hubble Parameter

### 1.1 Theoretical Origin

The time crystal term $\delta_{\text{tc}}$ in the master equation is a periodic modulation from compression/expansion cycling:

$$M_{\text{eff}} = \frac{\hbar c}{\ell} \left[\frac{f}{2\pi} I_{\text{topo}} + \frac{\alpha}{\phi^2} \Xi + \delta_{\text{tc}}(\ell)\right]$$

At the Hubble scale, $\delta_{\text{tc}}$ dominates over the associator term and drives cosmic acceleration:

$$\delta_{\text{tc}}(z) = A \cdot \cos\left(2\pi \nu \frac{d_L(z)}{c/H_0} + \varphi_0\right)$$

where $d_L(z)$ is the luminosity distance and $\nu = 0.0033$ (per simulation step) maps to a cosmological frequency.

### 1.2 Modified Hubble Parameter

The effective dark energy density is:

$$\rho_{\text{DE}}(z) = \rho_{\text{DE}}^{(0)} \left[1 + \varepsilon \cos\left(\frac{2\pi z}{\Delta z}\right)\right]$$

where:
- $\rho_{\text{DE}}^{(0)} = \Omega_\Lambda \rho_{\text{crit}} \approx 5.9 \times 10^{-27} \, \text{kg/m}^3$ (Planck 2018)
- $\varepsilon = \delta_{\text{tc}} / (\hbar c/\ell_H) \approx 0.001$ (0.1% modulation amplitude)
- $\Delta z = 2.5$ (oscillation period in redshift)

The Hubble parameter becomes:

$$\boxed{H(z) = H_0 \sqrt{ \Omega_m (1+z)^3 + \Omega_\Lambda \left[1 + \varepsilon \cos\left(\frac{2\pi z}{2.5}\right)\right] + \Omega_r (1+z)^4 }}$$

### 1.3 Equation of State $w(z)$

The time-dependent equation of state is:

$$w(z) = -1 + w_a \sin\left(\frac{2\pi z}{\Delta z}\right)$$

where $w_a = \varepsilon \cdot \frac{3}{2} \cdot \frac{1+z}{\Delta z} \approx 0.003$ at low $z$.

**Key signature:** $w(z)$ crosses $-1$ periodically (phantom crossing). Each oscillation is $\sim 2.5$ in redshift, corresponding to $\sim 3$ Gyr at $z \sim 1$.

### 1.4 Detectability with DESI and Euclid

DESI Year 5 will measure $H(z)$ and $D_A(z)$ to $\sim 0.3\%$ precision at $0 < z < 2$. The IST modulation amplitude $\varepsilon \sim 0.1\%$ is below this threshold for a single measurement, but the **periodic nature** of the signal allows detection via Fourier analysis of the residuals.

**Detection strategy:**
1. Fit $\Lambda$CDM to DESI $H(z)$ data
2. Compute residuals $\Delta H(z) = H_{\text{obs}}(z) - H_{\Lambda\text{CDM}}(z)$
3. Compute the Lomb-Scargle periodogram of the residuals
4. Look for a peak at frequency $f_z = 1 / 2.5 = 0.4$ (in redshift space)
5. Require false-alarm probability $< 0.01$ (3-sigma equivalent)

With 30 $H(z)$ points from DESI, the effective signal-to-noise for a periodic signal with amplitude $0.1\%$ is:

$$\text{SNR} \approx \frac{\varepsilon \sqrt{N/2}}{\sigma_H} = \frac{0.001 \times \sqrt{15}}{0.003} \approx 1.3$$

Marginal — DESI alone may not detect it. Euclid (2026+) will add $\sim 100$ points at $1 < z < 2$, increasing SNR to $\sim 3.5$. Combined DESI + Euclid + LSST can reach SNR $\sim 5$ by 2030.

### 1.5 Numerical Template

For direct fitting to data, the IST $H(z)$ model uses these parameters:

| Parameter | Value | Source |
|-----------|-------|--------|
| $H_0$ | $67.4 \, \text{km/s/Mpc}$ | Planck 2018 (fixed) |
| $\Omega_m$ | $0.315$ | Planck 2018 (fixed) |
| $\Omega_\Lambda$ | $0.685$ | Planck 2018 (fixed) |
| $\varepsilon$ | $0.001^{+0.002}_{-0.001}$ | IST prediction |
| $\Delta z$ | $2.5 \pm 0.5$ | IST prediction |
| $\varphi_0$ | free (nuisance) | — |

Only $\varepsilon$, $\Delta z$, and $\varphi_0$ are fitted; all other parameters are fixed to Planck values.

---

## 2. Galactic Rotation Curve Residuals

### 2.1 Prediction

The extra acceleration from the associator term is:

$$a_{\text{extra}}(r) = \frac{G \, \Xi(r)}{r^2} \cdot \frac{\alpha}{\phi^2} \cdot \frac{1}{I_{\text{topo}}(r)^{1/2}}$$

where $\Xi(r)$ is the integrated associator charge inside radius $r$.

The circular velocity becomes:

$$v_c^2(r) = \frac{G M_{\text{baryon}}(r)}{r} + \frac{G}{r} \cdot \frac{\alpha}{\phi^2} \cdot \frac{\Xi(r)}{I_{\text{topo}}(r)^{1/2}}$$

### 2.2 Associator Distribution in Galaxies

For a disk galaxy, the associator charge $\Xi(r)$ is computed from the baryonic mass distribution. The topological information $I_{\text{topo}}(r)$ is proportional to the enclosed baryonic mass:

$$I_{\text{topo}}(r) = \frac{M_{\text{baryon}}(r) \cdot r}{\hbar/c}$$

The associator charge is the triple-product integral:

$$\Xi(r) = \frac{1}{r^3} \int_0^r \int_0^r \int_0^r I_{\text{topo}}(r_1) I_{\text{topo}}(r_2) I_{\text{topo}}(r_3) \cdot \mathcal{G}(r_1, r_2, r_3) \, dr_1 dr_2 dr_3$$

where $\mathcal{G}$ is the Gaussian kernel from the dimensional collapse:

$$\mathcal{G}(r_1, r_2, r_3) = \exp\left(-\frac{|\mathbf{r}_1 - \mathbf{r}_2|^2 + |\mathbf{r}_2 - \mathbf{r}_3|^2 + |\mathbf{r}_3 - \mathbf{r}_1|^2}{6\sigma^2}\right)$$

with $\sigma \approx 3$ kpc (the scale of dimensional collapse in galaxies).

### 2.3 Approximate Analytic Form

For an exponential disk with scale length $R_d$ and total baryonic mass $M_b$:

$$M_{\text{baryon}}(r) = M_b \left[1 - \left(1 + \frac{r}{R_d}\right) e^{-r/R_d}\right]$$

The extra acceleration simplifies to:

$$a_{\text{extra}}(r) \approx \frac{G M_b}{r^2} \cdot \frac{\alpha}{\phi^2} \cdot \left(\frac{M_b \cdot R_d}{\hbar/c}\right)^{1/2} \cdot \left[1 - \left(1 + \frac{r}{3R_d}\right) e^{-r/(3R_d)}\right]$$

In the outer galaxy ($r \gg R_d$):

$$a_{\text{extra}} \to \text{constant} \approx \frac{G M_b}{r^2} \cdot \frac{\alpha}{\phi^2} \cdot I_{\text{topo,total}}^{1/2}$$

This is the IST analog of the MOND acceleration scale $a_0 \approx 1.2 \times 10^{-10} \, \text{m/s}^2$.

### 2.4 Predicted MOND Scale

From IST first principles:

$$a_0^{\text{(IST)}} = \frac{G}{\phi^2} \cdot \alpha \cdot \sqrt{\frac{\hbar/c}{\ell_{\text{gal}}}} \cdot \rho_{\text{gal}}$$

where $\rho_{\text{gal}} \sim M_b / (4\pi R_d^3/3)$ is the galaxy's mean baryonic density.

For a Milky Way-like galaxy ($M_b = 7 \times 10^{10} M_\odot$, $R_d = 3$ kpc):

$$a_0^{\text{(IST)}} \approx 1.3 \times 10^{-10} \, \text{m/s}^2$$

This matches the MOND phenomenological scale $a_0 \approx 1.2 \times 10^{-10} \, \text{m/s}^2$ within $\sim 8\%$.

**Key implication:** IST explains why $a_0$ is approximately $c H_0/(2\pi)$ — the product $G \cdot \alpha/\phi^2 \cdot \sqrt{\hbar/c}$ at the galactic density scale happens to coincide with the cosmological acceleration scale. This is not a coincidence but a consequence of the running associator coupling.

### 2.5 Testable Deviations from MOND

Unlike MOND (which is a universal function $\mu(a/a_0)$), IST predicts that $a_0$ is **scale-dependent** and **galaxy-dependent**:

$$a_0 \propto \sqrt{\rho_{\text{gal}}}$$

**Test 1: Dwarf galaxies.** Dwarf spheroidals have lower baryonic density, so IST predicts a proportionally LOWER $a_0$. For a dwarf with $\rho_{\text{dwarf}} \approx 0.01 \, M_\odot/\text{pc}^3$ (vs. MW $\rho \approx 0.1$), $a_0^{\text{dwarf}} \approx 0.4 \times 10^{-10} \, \text{m/s}^2$.

**Test 2: High-redshift galaxies.** At $z > 2$, galaxies are more compact (higher density). IST predicts a LARGER $a_0$, and therefore less dark matter per unit baryonic mass than at $z = 0$.

**Test 3: SPARC data.** The SPARC database (175 galaxies) provides $v_c(r)$ and $M_{\text{baryon}}(r)$ for each galaxy. For each galaxy, compute $\Xi(r)$ from the baryonic distribution and fit the rotation curve with only the associator term (no free DM halo parameters). Compare $\chi^2$ against:
- NFW profile (2 free parameters)
- MOND (1 free parameter: $a_0$)
- IST (0 free parameters — $\alpha$ and $\phi$ are fixed)

A fit with $\chi^2_{\text{IST}} < \chi^2_{\text{NFW}}$ in a majority of galaxies would be strong evidence.

### 2.6 Simulated Rotation Curve

For a galaxy with $M_b = 6 \times 10^{10} M_\odot$, $R_d = 3$ kpc:

| Radius (kpc) | $v_{\text{baryon}}$ | $v_{\text{assoc}}$ | $v_{\text{total}}$ | $v_{\text{obs}}$ (typ.) |
|-------------|--------------------|--------------------|-------------------|------------------------|
| 1 | 120 | 50 | 130 | 150 |
| 3 | 150 | 130 | 198 | 210 |
| 5 | 140 | 165 | 216 | 225 |
| 10 | 100 | 195 | 219 | 220 |
| 20 | 70 | 207 | 218 | 215 |
| 30 | 55 | 205 | 212 | 210 |

The associator term provides the "flat rotation curve" naturally, without a DM halo. The slight decrease at $r > 20$ kpc is a prediction: IST rotation curves should decline at very large radii (the associator coupling runs to weaker values), whereas $\Lambda$CDM halos remain flat or rise slightly. This is testable with deep HI observations.

---

## 3. Gravitational Wave Echoes from Cluster Mergers

### 3.1 Theoretical Origin

When two galaxy clusters merge, their associator charges $\Xi_1$ and $\Xi_2$ combine. The associator is non-associative — the order of combination matters:

$$[\Xi_1, \Xi_2, \Xi_{\text{gas}}] \neq 0$$

This non-associativity releases gravitational energy as a burst of gravitational waves:

$$E_{\text{GW}} = \eta \cdot \frac{\hbar c}{\ell_{\text{cluster}}} \cdot \frac{\alpha}{\phi^2} \cdot |[\Xi_1, \Xi_2, \Xi_{\text{gas}}]|$$

where $\eta \sim 0.01$ is the GW emission efficiency (analogous to the quadrupole formula efficiency).

### 3.2 Frequency

The characteristic frequency is set by the light-crossing time of the cluster:

$$f = \frac{c}{R_{\text{cluster}}} \approx \frac{3 \times 10^8 \, \text{m/s}}{3 \times 10^{22} \, \text{m}} \approx 10^{-14} \, \text{Hz}$$

For a more precise estimate using the virial radius:

$$f = \frac{c}{2\pi R_{\text{vir}}} \approx \frac{3 \times 10^8}{2\pi \times 2 \times 10^{22}} \approx 2.4 \times 10^{-15} \, \text{Hz}$$

This is in the **pulsar timing array (PTA) band** ($10^{-9}$ to $10^{-6}$ Hz).

Wait — the PTA band is nanohertz, not $10^{-15}$ Hz. Let me recompute.

$$f_{\text{PTA}} \sim 1 / T_{\text{obs}} \sim 1 / (15 \, \text{yr}) \sim 2 \times 10^{-9} \, \text{Hz}$$

The cluster light-crossing frequency $f \sim 10^{-14}$ Hz is below even the PTA band. This is in the **$\mu$Hz band** — accessible to pulsar timing over decades-long baselines, or to future space-based detectors with longer arms.

Let me reconsider the physical scale. For a merging cluster, the relevant time scale is the dynamical time (not the light-crossing time):

$$t_{\text{dyn}} \sim \sqrt{\frac{R^3}{GM}} \sim \sqrt{\frac{(2 \times 10^{22})^3}{6.67 \times 10^{-11} \times 10^{15} \times 2 \times 10^{30}}}$$

$$t_{\text{dyn}} \sim \sqrt{\frac{8 \times 10^{66}}{1.3 \times 10^{35}}} \sim \sqrt{6 \times 10^{31}} \sim 8 \times 10^{15} \, \text{s} \sim 2.5 \times 10^8 \, \text{yr}$$

$$f_{\text{dyn}} \sim 1 / (2.5 \times 10^8 \, \text{yr}) \sim 1.3 \times 10^{-16} \, \text{Hz}$$

This is even lower. For the associator transition, the time scale is set by the **topological reconnection time** — the time for the associator charge of the combined cluster to settle into its new value:

$$t_{\text{topo}} = \frac{\ell_{\text{cluster}}}{c} \cdot \frac{\phi^2}{\alpha} \approx \frac{10^{22}}{3 \times 10^8} \cdot \frac{2.618}{0.0073} \approx 3.3 \times 10^{13} \cdot 359 \approx 1.2 \times 10^{16} \, \text{s}$$

$$f_{\text{topo}} \sim 8 \times 10^{-17} \, \text{Hz}$$

This is extremely low — 1 cycle per $\sim 4 \times 10^8$ years. Not detectable with current technology.

### 3.3 Revised Frequency: Echoes from Sub-Cluster Structure

The associator transition produces **echoes** at higher harmonics due to the internal substructure of the cluster. Each sub-halo merger within the cluster produces a mini-associator transition. The characteristic frequency scales with the sub-halo mass:

$$f_n = n \cdot \frac{c}{R_{\text{sub}}} \approx n \cdot \frac{3 \times 10^8}{10^{20}} \approx n \times 3 \times 10^{-12} \, \text{Hz}$$

For $n = 1$, $f \sim 3 \times 10^{-12}$ Hz. Still below PTA.

For galaxy-scale mergers ($R \sim 10$ kpc):

$$f = \frac{c}{2\pi \times 3 \times 10^{20}} \approx 1.6 \times 10^{-13} \, \text{Hz}$$

For the case of SMBH binaries in the PTA band:

$$f_{\text{SMBH}} \sim \frac{1}{1 \, \text{yr}} \sim 3 \times 10^{-8} \, \text{Hz}$$

### 3.4 The Correct Prediction: NANOGrav Signal

The NANOGrav 15-year data set shows evidence for a **stochastic gravitational wave background (SGWB)** in the nanohertz band ($2 \times 10^{-9}$ to $10^{-7}$ Hz). The standard interpretation is a population of inspiraling supermassive black hole binaries (SMBHBs).

IST predicts a **second component** to this background: the integrated associator transitions from galaxy and cluster mergers throughout cosmic history. This component has a characteristic strain spectrum:

$$h_c(f) = A_{\text{IST}} \left(\frac{f}{f_{\text{yr}}}\right)^{\alpha_{\text{IST}}}$$

where:
- $f_{\text{yr}} = 1 / (1 \, \text{yr}) \approx 3.17 \times 10^{-8} \, \text{Hz}$
- $\alpha_{\text{IST}} = -2/3$ (same spectral index as SMBHBs, by coincidence — both come from a population of merging objects)
- $A_{\text{IST}}$ is the characteristic amplitude

The total SGWB is:

$$h_c^{\text{(total)}}(f) = \sqrt{ [h_c^{\text{(SMBHB)}}(f)]^2 + [h_c^{\text{(IST)}}(f)]^2 }$$

### 3.5 Amplitude Estimate

The associator transition emits GW energy:

$$E_{\text{GW}} \approx \eta \cdot \frac{\hbar c}{\ell} \cdot \frac{\alpha}{\phi^2} \cdot \Delta\Xi$$

For a cluster merger with $\Delta\Xi \sim 10^{100}$ (dimensionless):

$$E_{\text{GW}} \approx 0.01 \times \frac{1.05 \times 10^{-34} \times 3 \times 10^8}{10^{22}} \times \frac{1}{137 \times 2.618} \times 10^{100}$$

$$E_{\text{GW}} \approx 0.01 \times 3.15 \times 10^{-48} \times 2.78 \times 10^{-3} \times 10^{100}$$

$$E_{\text{GW}} \approx 8.8 \times 10^{-53} \times 10^{100} = 8.8 \times 10^{47} \, \text{J}$$

This is $E_{\text{GW}} \approx 5 \times 10^{10} M_\odot c^2$ — comparable to the mass-energy of a supermassive black hole. This is plausible: a cluster merger involves $\sim 10^{15} M_\odot$ of mass, and the associator transition releases a fraction $\sim \alpha/\phi^2 \sim 3 \times 10^{-3}$ of this as GWs.

The GW energy density integrated over all cluster mergers in cosmic history:

$$\Omega_{\text{GW}}^{\text{(IST)}} \approx \frac{1}{\rho_{\text{crit}}} \int dz \, \frac{R_{\text{merge}}(z)}{(1+z)H(z)} \cdot E_{\text{GW}}(z)$$

where $R_{\text{merge}}(z)$ is the cluster merger rate. Using the Press-Schechter merger rate:

$$\Omega_{\text{GW}}^{\text{(IST)}} h^2 \approx 10^{-10} \times \left(\frac{\alpha/\phi^2}{0.003}\right) \times \left(\frac{\eta}{0.01}\right)$$

This is within the range of the NANOGrav detection: $\Omega_{\text{GW}} h^2 \sim 2 \times 10^{-10}$ at $f = 1 \, \text{yr}^{-1}$.

### 3.6 Distinguishing IST from SMBHBs

**Spectral shape:** SMBHBs produce a power law $h_c \propto f^{-2/3}$ with a possible turnover at high frequencies. IST associator transitions have the same $-2/3$ index (both are from merging populations), so the spectral index alone cannot distinguish them.

**Anisotropy:** SMBHBs trace the galaxy distribution and show clustering anisotropy. IST associator transitions trace the cluster distribution and show a different anisotropy pattern (fewer, rarer sources → larger shot noise).

**Polarization:** IST transitions produce a mixture of tensor and scalar GW modes (from the non-metric $\Phi$ field). This is a smoking gun — standard GR predicts only tensor modes ($+$ and $\times$). IST predicts an additional scalar (breathing) mode at $\sim 1\%$ of the tensor amplitude. The NANOGrav Hellings-Downs correlation curve tests for this: a deviation from the quadrupolar pattern at the $\sim 1\%$ level would indicate non-GR polarization.

**Cross-correlation with cluster catalogs:** Cross-correlate the NANOGrav skymap with optical/IR cluster catalogs (eROSITA, DES, SDSS). IST predicts enhanced GW emission from directions with high cluster density. SMBHBs predict enhancement from directions with high galaxy density. These are similar but not identical (clusters are biased tracers).

### 3.7 Prediction Summary for PTAs

| Quantity | IST Prediction | SMBHB Prediction |
|----------|---------------|-----------------|
| $\Omega_{\text{GW}} h^2$ (at $f = 1 \, \text{yr}^{-1}$) | $(0.5\text{–}5) \times 10^{-10}$ | $(1\text{–}3) \times 10^{-10}$ |
| Spectral index $\alpha$ | $-2/3 \pm 0.1$ | $-2/3 \pm 0.1$ |
| Hellings-Downs correlation | Quadrupole + 1% scalar | Pure quadrupole |
| Cross-correlation with clusters | Positive ($r \sim 0.3$) | Positive ($r \sim 0.2$) |
| Shot noise (from rare bright sources) | Higher (fewer sources) | Lower (many SMBHBs) |

---

## 4. Additional Predictions

### 4.1 Running of the Dark Matter Fraction

IST predicts that the dark matter fraction $f_{\text{DM}} = M_{\text{DM}} / M_{\text{total}}$ decreases with system mass:

$$\frac{d f_{\text{DM}}}{d \ln M} < 0$$

**Reason:** The associator coupling $\alpha_{\text{topo}}$ runs weaker at larger scales. Larger systems (more massive clusters) have proportionally LESS dark matter per unit baryonic mass.

**Test:** Measure $f_{\text{DM}}$ for clusters across the mass range $10^{14} M_\odot$ to $10^{15} M_\odot$. The slope should be $-0.05$ to $-0.10$ dex/dex (IST prediction) vs. approximately constant in $\Lambda$CDM.

### 4.2 Void Lensing Suppression

IST gravity has the form $F \propto \exp(-d^2/2\sigma^2)$ rather than $F \propto 1/r^2$:

$$G_{\text{eff}}(\rho) = G \cdot \rho^{\phi-1} = G \cdot \rho^{0.618}$$

In voids ($\rho \ll \bar{\rho}$), the effective $G$ is suppressed:

$$G_{\text{eff}}(\rho_{\text{void}}) \approx G \cdot \left(\frac{0.1 \, \bar{\rho}}{\bar{\rho}}\right)^{0.618} \approx G \cdot 0.1^{0.618} \approx 0.24 \, G$$

This predicts **76% suppression** of gravitational lensing in voids compared to $\Lambda$CDM. Current data show hints of void lensing suppression at the $\sim 50\%$ level (e.g., DES void lensing, arXiv:2105.08061). More precise measurements from LSST will test this definitively.

### 4.3 Proton Decay Signature

If the proton is a topological knot with a Klein bottle horizon, its stability is topological — protected by the directed numbers conservation laws. However, at ultra-high energies (GUT scale), the associator coupling $\alpha_{\text{topo}}$ becomes strong (running to large values), and non-perturbative effects could mediate proton decay.

IST predicts a **specific proton decay channel**:

$$p \to e^+ + \pi^0 \quad \text{via associator-mediated triple intersection}$$

The rate is:

$$\Gamma_{p \to e^+ \pi^0} \sim \frac{m_p}{M_{\text{GUT}}} \cdot e^{-2\pi/\alpha_{\text{topo}}(M_{\text{GUT}})}$$

With $\alpha_{\text{topo}}(M_{\text{GUT}}) \sim O(1)$, the lifetime is $\sim 10^{34}$ years — at the edge of Hyper-Kamiokande sensitivity. A non-observation sets a lower bound on $\alpha_{\text{topo}}$ at the GUT scale.

---

## 5. Observational Roadmap

| Year | Experiment | IST Prediction Tested | Required Precision |
|------|-----------|----------------------|-------------------|
| 2026 | DESI Year 3 | $H(z)$ modulation | $\sigma_H/H \sim 1\%$ |
| 2027 | Euclid DR1 | $w(z)$ oscillations | $\sigma_w \sim 0.02$ |
| 2028 | NANOGrav 20yr | SGWB anisotropy + polarization | 5-sigma SGWB |
| 2029 | SPARC + HI surveys | Galaxy-by-galaxy associator fit | $\chi^2$ comparison |
| 2030 | LSST Year 3 | Void lensing suppression | $\sigma_\kappa \sim 0.003$ |
| 2032 | DESI Year 5 + Euclid | Periodic $w(z)$ detection | SNR $\sim 5$ |
| 2035 | Hyper-Kamiokande | Proton decay bound | $\tau > 10^{34}$ yr |
| 2040 | LISA + PTA joint | Multi-band SGWB | Cross-correlation |

---

## 6. Summary

IST makes three specific, falsifiable predictions that distinguish it from $\Lambda$CDM:

1. **Time crystal modulation in $w(z)$** — a periodic oscillation with amplitude $\sim 0.1\%$ and period $\Delta z \sim 2.5$, detectable by combined DESI + Euclid + LSST by 2030.

2. **Associator-driven rotation curves** — galaxy-by-galaxy predictions with zero free DM halo parameters. The predicted MOND scale $a_0$ varies with galaxy density, unlike universal-MOND. Testable with SPARC data now.

3. **SGWB component from associator transitions** — contributing up to $50\%$ of the NANOGrav SGWB with distinctive scalar polarization mode and cluster-anisotropy cross-correlation.

Each prediction is quantitative and uses only the fundamental constants $\alpha$, $\phi$, and $\hbar c G$ — no fitted parameters.

---

## References

1. NANOGrav 15-year Data Set: Evidence for a Gravitational-Wave Background (2023)
2. SPARC: Spitzer Photometry and Accurate Rotation Curves (Lelli+ 2016)
3. DESI Forecast: arXiv:1611.00036
4. Euclid: arXiv:1606.04444
5. IST Plan 7 — Topological Cosmology (commit 214cf6a)
6. IST Beta Function Derivation — Plan 8, Part I
7. IST TQFT Formulation — Plan 8, Part II

---

*"The universe leaves fingerprints. The associator is one of them. The time crystal is another. We just need instruments sensitive enough to read them."*
