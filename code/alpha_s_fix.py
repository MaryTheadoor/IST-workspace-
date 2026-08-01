"""
================================================================================
Fix the alpha_s gap: phi^4 layer-counting function
================================================================================
Phase 3 found alpha_s(M_Z) = 0.38 vs observed 0.118 -- off by factor 3.2.
The fix: the associator layer-counting function is NOT n(E) = log_2(E/M_Z),
but n(E) = log_{phi^4}(E/m_p) -- each associator layer spans a factor
of phi^4 ~ 6.85 in energy, corresponding to the 3D volume scaling.

Result: alpha_s(M_Z) = 0.121 (within 2.5% of 0.118).
       alpha_s(m_tau) = 0.325 (observed 0.33, within 2%).
       All 4 reference values match within 2-20%.
================================================================================
"""
import numpy as np

PHI = (1 + np.sqrt(5)) / 2
ALPHA_INV = 137.035999084

# Reference values
REF = {
    "M_Z (91.2 GeV)": (91.1876, 0.118),
    "m_tau (1.78 GeV)": (1.77686, 0.33),
    "m_b (4.18 GeV)": (4.18, 0.22),
    "m_t (173 GeV)": (173.0, 0.09),
}

M_P = 0.938272  # proton mass in GeV

# ---------- corrected model ----------
PHI4 = PHI ** 4          # phi^4 ~ 6.854
LOG_PHI4 = np.log(PHI4)  # ~ 1.925
C = 1.0 / PHI ** 2       # fixed-point normalization ~ 0.382


def n_layers(E_GeV):
    """Number of associator layers between proton scale and energy E."""
    return np.log(E_GeV / M_P) / LOG_PHI4


def alpha_s_corrected(E_GeV):
    """alpha_s(E) = C * phi^{-n(E)} with phi^4 layer spacing."""
    return C * PHI ** (-n_layers(E_GeV))


print("Scale          E(GeV)  n_layers  alpha_s(pred)  alpha_s(ref)  error%")
print("-" * 72)
for name, (E, ref) in REF.items():
    pred = alpha_s_corrected(E)
    err = 100 * abs(pred - ref) / ref
    print(f"{name:20s} {E:8.1f}  {n_layers(E):8.3f}  {pred:13.4f}  "
          f"{ref:12.4f}  {err:5.1f}%")

# neutron mass correction with running phi
phi_neutron = PHI  # at neutron scale, phi ~ fixed point (within a few %)
delta_n = (1 / ALPHA_INV) / phi_neutron ** 2
m_n = M_P * (1 + delta_n)
print(f"\nNeutron: phi ~ {phi_neutron:.3f}, delta_n = {delta_n:.6f}, "
      f"m_n = {m_n:.4f} GeV (obs 0.9396)")

# number of layers from proton to Planck scale
n_planck = n_layers(1.22e19)
print(f"Layers from proton to Planck: {n_planck:.1f} "
      f"(alpha_s at Planck ~ {alpha_s_corrected(1.22e19):.2e})")
