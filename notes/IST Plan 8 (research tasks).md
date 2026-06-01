# Plan 8: Theoretical Foundations – Beta Function, TQFT, and Predictions

## Objective
Derive the renormalization group flow of the topological coupling, formalize the underlying TQFT, and produce testable observational signatures.

## Part I – Beta Function from Directed Numbers

### 1.1 Define the running coupling
\[
\alpha_{\text{topo}}(\mu) = \frac{\alpha}{\phi^2} \cdot \frac{\Xi(\mu)}{I_{\text{topo}}(\mu)^{3/2}}
\]
where \( \mu = \ell_P / \ell \) is the energy scale.

### 1.2 Empirical flow (from Plan 7)
- At proton scale (\( \ell \approx 1\,\text{fm} \)): \( \log_{10} \alpha_{\text{topo}} \approx 2.23 - 1.5 \times 0.63 = 2.23 - 0.945 = 1.285 \)
- At Hubble scale (\( \ell = c/H_0 \)): \( \log_{10} \alpha_{\text{topo}} \approx 123.54 - 1.5 \times 120.25 = 123.54 - 180.375 = -56.835 \)

So \( \alpha_{\text{topo}} \) runs from ~\(10^{1.3}\) down to ~\(10^{-57}\) – a decrease of 58 orders.

### 1.3 Proposed beta function
\[
\beta(\alpha_{\text{topo}}) = \frac{d\alpha_{\text{topo}}}{d\ln\mu} = -b_0 \alpha_{\text{topo}}^2 - b_1 \alpha_{\text{topo}}^3 + \dots
\]
where \( b_0 > 0 \) gives asymptotic freedom at high energy (large μ). Use the directed numbers associator to compute \( b_0 \).

**Task:** Derive \( b_0 \) from the associator’s scaling dimension.

## Part II – Topological Quantum Field Theory Formulation

### 2.1 Action
Propose a BF‑type action with a Chern‑Simons term:
\[
S = \int \text{Tr}(B \wedge F) + \frac{k}{4\pi} \int \text{Tr}(A \wedge dA + \frac{2}{3} A \wedge A \wedge A) + \lambda \int \text{Tr}(\Phi \wedge \Phi)
\]
where \( \Phi \) is a scalar field encoding the associator charge.

### 2.2 Observables
- Wilson loops: \( W_R(\gamma) = \text{Tr}_R \mathcal{P} e^{\oint_\gamma A} \).
- Linking numbers as correlation functions of Wilson loops.
- The associator \( [x,y,z] \) is a three‑point function of vertex operators.

**Task:** Write the path integral, show that the directed numbers algebra emerges in the semiclassical limit.

## Part III – Observational Predictions

### 3.1 Hubble parameter modulation (dark energy)
From time‑crystal term \( \delta_{\text{tc}} \):
\[
H(z) = H_0 \sqrt{ \Omega_m (1+z)^3 + \Omega_\Lambda \left(1 + \varepsilon \cos\left(\frac{\omega z}{H_0}\right)\right) }
\]
with \( \varepsilon \sim 0.1\% \) and \( \omega \sim H_0 \times (\text{small integer}) \). Fit to Pantheon+ data.

### 3.2 Galactic rotation curve residuals
The extra acceleration from the associator:
\[
a_{\text{extra}}(r) = \frac{G \Xi(r)}{r^2} \cdot \frac{\alpha}{\phi^2} \cdot \frac{1}{I_{\text{topo}}(r)^{1/2}}
\]
where \( \Xi(r) \) is the integrated associator charge inside radius \( r \). This gives a modified rotation curve that can be tested against SPARC data.

### 3.3 Gravitational wave echoes from topological transitions
When a galaxy cluster merges, the change in \( \Xi \) emits a burst of gravitational waves at frequency \( f \sim c / R_{\text{cluster}} \approx 10^{-16} \, \text{Hz} \) – in the PTA band (NANOGrav). Look for periodic signatures.

**Task:** Compute the waveform and match to existing PTA candidates.

## Deliverables (Theoretical – no code execution needed in this plan)
- `notes/beta_function_derivation.md`
- `notes/tqft_action.md`
- `notes/observational_predictions.md`
- `plans/plan_8_beta_function_tqft.md` (this outline, expanded)

## Execution
This plan is theoretical; it does not require simulation. The agent can produce the markdown documents with full equations and explanatory text.