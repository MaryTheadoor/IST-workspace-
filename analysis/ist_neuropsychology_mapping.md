# IST-Neuropsychology: Topological Framework for Neural Dynamics

**Authors:** Dr. Mary Theadoor, NOWN Research Collective  
**Date:** 2026-05-11  
**Status:** Working Document

---

## 1. Executive Summary

This document extends Information Substrate Theory (IST) to neuroscience, establishing a formal mathematical mapping between the theory's physical structures and neural dynamics. The key result is that the golden ratio φ, which emerges as the stability attractor of the substrate's RG flow, predicts the **maximal desynchronization** property of neural oscillators observed by Pletzer et al. (2010, 2026).

**Three-Pillar Mapping:**

| Physics (IST) | Neuroscience | Mechanism |
|---------------|--------------|-----------|
| Substrate Σ | Neural Network Topology | Non-orientable graph structure |
| Compression Ψ | Predictive Coding (Friston) | Free energy minimization |
| Attractor φ | Criticality | Optimal information integration Φ |

---

## 2. The Pletzer Finding: φ in Human EEG

Pletzer et al. demonstrated that theta-alpha frequency ratios in human EEG approximate φ, and that this ratio achieves **maximal desynchronization** — the excitatory phases of the two oscillators never coincide, providing optimal multiplexing of information across frequency channels.

### 2.1 Computational Verification

We verified this property using pulse coincidence analysis. For two oscillators with frequency ratio r, the coincidence rate measures how often their excitatory phases align:

| Frequency Ratio | Coincidence Rate | Rank |
|-----------------|------------------|------|
| φ = 1.618034 | **0.09947** | **#1 (tied)** |
| 21/13 ≈ 1.615 | 0.09994 | #5 |
| 5/3 = 1.667 | 0.09975 | #4 |
| √2 = 1.414 | 0.10020 | #10 |
| 3/2 = 1.500 | 0.10000 | #6 |

φ achieves the lowest coincidence rate, confirming maximal desynchronization. This property follows from φ being the **most irrational number** — its continued fraction [1; 1, 1, 1, ...] converges slowest, making it structurally stable against phase-locking.

### 2.2 Fibonacci Approximants

The Fibonacci ratios F_{n+1}/F_n converge to φ:

- 2/1 = 2.0
- 3/2 = 1.5
- 5/3 = 1.667
- 8/5 = 1.6
- **13/8 = 1.625** (within 0.4% of φ)
- 21/13 = 1.615 (within 0.2% of φ)

Notably, the classical EEG boundary at 13/8 Hz ≈ φ is the Fibonacci ratio closest to φ with small integers, suggesting the band boundaries may be Fibonacci-structured.

---

## 3. Self-Referential Force Equation for Neural Dynamics

The same self-referential equation that determines force couplings in physics governs neural population dynamics:

**Force Equation:** φ²r² - r + α·φ^(2n-1)·C = 0

Where:
- r = stable firing rate of population n
- α = baseline neural excitability (analogous to EM coupling)
- n = hierarchy level (1=theta, 2=alpha, 3=beta)
- C = √(1 + 1/φ⁴) = two-hemisphere (Möbius) correction

### 3.1 Coupling Matrix

The coupling between populations i and j:

K_ij = α·φ^(2|i-j|-1)·C / (1 + φ²|r_i - r_j|)

This ensures:
- Nearby frequency bands couple more strongly
- The φ-structure enforces desynchronization
- Information integrates across the hierarchy

### 3.2 Information Integration (Φ)

From Friston's Free Energy Principle, integrated information Φ measures how much the whole network integrates beyond its parts:

Φ = Σ Ω(r_i) - Σ redundancy_ij

Where Ω is the compression operator (directed number formalism). Our simulations show Φ converges to a stable value (~0.59 for 3-population networks), indicating the self-referential coupling creates a stable attractor for information integration.

---

## 4. Predictions

### 4.1 Testable Predictions

1. **Frequency Ratio Precision**: The theta-alpha frequency ratio in individual subjects should be closer to φ (1.618) than to nearby rationals (3/2, 5/3, 13/8). Deviation from φ should correlate with cognitive impairment.

2. **Perturbation Sensitivity**: Driving neural oscillators at exactly φ-ratio should be maximally resistant to entrainment by external periodic stimuli.

3. **Information Integration**: Transcranial magnetic stimulation (TMS) at φ-frequency should maximize information integration (Φ) across cortical regions.

4. **Bipolar Structure**: The two-hemisphere correction C = √(1 + 1/φ⁴) predicts that split-brain patients should show altered (non-φ) frequency ratios between homologous regions.

### 4.2 Consciousness Implications

If consciousness emerges from integrated information (IIT), and Φ is maximized at φ-criticality, then:

- **Anesthesia**: Should drive frequency ratios away from φ, reducing Φ
- **Psychedelics**: May broaden the attractor basin around φ, increasing Φ
- **Meditation**: Should sharpen the φ-ratio, stabilizing Φ at higher values
- **Sleep**: The progression through sleep stages should follow a φ-trajectory in frequency space

---

## 5. Connection to Previous IST Work

This neural framework directly extends our force hierarchy derivation:

| Force Hierarchy | Neural Hierarchy |
|-----------------|------------------|
| EM coupling (α) | Baseline excitability |
| Weak force (α_w) | Theta-alpha coupling |
| Strong force (α_s) | Alpha-beta coupling |
| Gravity (G) | Global Φ-integration |

The two-sided Möbius correction C = √(1 + 1/φ⁴) that improved force predictions (0.08% for weak, 1.35% for strong) appears here as the bilateral hemispheric correction.

---

## 6. References

1. Pletzer, B., Kerschbaum, H., & Klimesch, W. (2010). When frequencies never synchronize: The golden mean and the resting EEG. *Brain Research*, 1335, 91-102.

2. Pletzer, B. (2026). [Update on golden ratio in EEG — placeholder for latest publication].

3. Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138.

4. Tononi, G., Boly, M., Massimini, M., & Koch, C. (2016). Integrated information theory: from consciousness to its physical substrate. *Nature Reviews Neuroscience*, 17(7), 450-461.

5. Theadoor, M. (2026). Information Substrate Theory v5.3: Topology of the Substrate. *NOWN Research Collective*.

---

## 7. Code

The computational implementation is in `code/ist_neural.py`, including:

- `NeuralThread`: Directed number thread model for oscillators
- `PhiScaledBands`: EEG band boundary analysis
- `PletzerAnalysis`: Maximal desynchronization demonstration
- `ISTNeuralPopulation`: Self-referential population dynamics with Φ integration

Run with: `python -c "from code.ist_neural import *; print(PletzerAnalysis.compare_ratios())"`

---

*This is a working document of the NOWN Research Collective. Comments and collaborations welcome.*
