
# =============================================================================
# IST-NEURAL: Information Substrate Theory Applied to Neuroscience
# =============================================================================
# 
# Mapping between IST physics and neuroscience:
#   Substrate Σ      → Neural Network Topology
#   Compression Ψ    → Predictive Coding / Free Energy Principle
#   Attractor φ      → Criticality / Optimal Information Integration
#
# Key result: φ-frequency oscillators achieve maximal desynchronization
# (Pletzer et al. 2010, 2026), enabling optimal information multiplexing.
#
# Author: Dr. Mary Theadoor (NOWN Research Collective)
# =============================================================================

import numpy as np
from scipy.integrate import odeint
from scipy.signal import find_peaks

PHI = (1 + np.sqrt(5)) / 2


class NeuralThread:
    """Neural oscillation as directed number thread on substrate."""

    def __init__(self, freq, phase=0.0, chirality=1.0, coupling=0.1):
        self.freq = freq
        self.phase = phase
        self.chirality = chirality
        self.coupling = coupling

    def phase_dynamics(self, t, other_threads=None):
        dtheta = 2 * np.pi * self.freq
        if other_threads:
            for other in other_threads:
                if other is not self:
                    pd = other.phase - self.phase
                    n = int(np.round(np.log(max(self.freq, other.freq) / 
                                          min(self.freq, other.freq)) / np.log(PHI))) + 1
                    dtheta += self.coupling * (PHI ** (2*n - 1)) * np.sin(pd)
        return dtheta

    def step(self, dt, other_threads=None):
        dtheta = self.phase_dynamics(0, other_threads)
        self.phase = (self.phase + dtheta * dt) % (2 * np.pi)
        return self.phase


class PhiScaledBands:
    """EEG frequency bands from φ-scaling on neural substrate."""

    OBSERVED = {'delta': 2.0, 'theta': 6.0, 'alpha': 10.5, 'beta': 21.0, 'gamma': 60.0}
    BOUNDARIES = [0.5, 4, 8, 13, 30, 100]

    @staticmethod
    def boundary_ratio_analysis():
        """Analyze boundary ratios for φ-proximity."""
        b = PhiScaledBands.BOUNDARIES
        results = {}
        for i in range(len(b) - 1):
            r = b[i+1] / b[i]
            results[f"{b[i+1]}/{b[i]}"] = {
                'ratio': r, 
                'phi_deviation': abs(r - PHI) / PHI * 100
            }
        return results


class PletzerAnalysis:
    """Demonstrate maximal desynchronization at φ frequency ratio."""

    @staticmethod
    def coincidence_rate(r, tolerance=0.05, max_period=100):
        """Fraction of time two oscillators are in-phase (within tolerance)."""
        n_points = 100000
        t = np.linspace(0, max_period, n_points)
        phase1 = t % 1.0
        phase2 = (r * t) % 1.0
        diff = np.minimum(np.abs(phase2 - phase1), 1 - np.abs(phase2 - phase1))
        return np.mean(diff < tolerance)

    @staticmethod
    def compare_ratios():
        """Compare coincidence rates across frequency ratios."""
        test_cases = {
            '3/2 (rational)': 3/2, '5/3 (Fibonacci)': 5/3,
            '13/8 (≈φ)': 13/8, '21/13 (≈φ)': 21/13,
            '√2 (irrational)': np.sqrt(2), '√3 (irrational)': np.sqrt(3),
            'φ (golden)': PHI,
        }
        results = {}
        for name, ratio in test_cases.items():
            results[name] = PletzerAnalysis.coincidence_rate(ratio)
        return dict(sorted(results.items(), key=lambda x: x[1]))


class ISTNeuralPopulation:
    """Neural population dynamics with self-referential coupling."""

    def __init__(self, n_pops=3, alpha=0.05):
        self.n = n_pops
        self.alpha = alpha
        self.C = np.sqrt(1 + 1/PHI**4)
        self.rates = self._stable_rates()
        self.K = self._coupling_matrix()

    def _stable_rates(self):
        rates = []
        for n in range(1, self.n + 1):
            a, b, c = PHI**2, -1.0, self.alpha * (PHI ** (2*n - 1)) * self.C
            disc = b**2 - 4*a*c
            if disc >= 0:
                r = (-b - np.sqrt(disc)) / (2*a)
                rates.append(max(0.01, min(0.99, r)))
            else:
                rates.append(0.3)
        return np.array(rates)

    def _coupling_matrix(self):
        K = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    order = abs(i - j)
                    num = self.alpha * (PHI ** (2*order - 1)) * self.C
                    den = 1 + PHI**2 * abs(self.rates[i] - self.rates[j])
                    K[i, j] = num / den
        return K

    def simulate(self, T=10.0, dt=0.01):
        n_steps = int(T / dt)
        r = self.rates.copy()
        rates_t = np.zeros((n_steps, self.n))
        phi_t = np.zeros(n_steps)
        tau = 0.1

        for step in range(n_steps):
            inp = self.K @ r
            arg = np.clip(5*(inp - 0.3), -10, 10)
            act = 1 / (1 + np.exp(-arg))
            r = np.clip(r + (-r + act) * dt / tau, 0.01, 0.99)
            rates_t[step] = r
            infos = [ri * (1-ri) + 0.1 for ri in r]
            phi_t[step] = sum(infos) - sum(infos[i]*infos[j] 
                                           for i in range(self.n) for j in range(i+1, self.n))

        return np.arange(0, T, dt), rates_t, phi_t
