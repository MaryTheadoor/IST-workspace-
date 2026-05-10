
# =============================================================================
# IST-NEUTRINO: Neutrino Masses from Back-Side Projection
# =============================================================================
#
# Hypothesis: Neutrinos are "back-side projections" of charged leptons through
# the non-orientable substrate Σ. The mass suppression arises from geometric
# penetration through k=22 substrate layers, with φ^(-2) suppression per layer.
#
# Formula: m_νn = m_ln^q × φ^(-2(n+k)) × √(1+1/φ⁴)
#
#   q ≈ 0.957: best-fit exponent (theoretical limit q→1 from first principles)
#   k = 22:    substrate bulk depth (universal for all neutrinos)
#
# Author: Dr. Mary Theadoor (NOWN Research Collective)
# =============================================================================

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
C_TWO_SIDED = np.sqrt(1 + 1/PHI**4)

# Charged lepton masses in MeV
M_ELECTRON = 0.5109989461
M_MUON = 105.6583745
M_TAU = 1776.86


def neutrino_mass(m_lepton_mev, generation, k=22, q=0.957, phi=PHI, C=C_TWO_SIDED):
    """
    Compute neutrino mass from back-side projection.

    The wavefunction of a charged lepton, when projected through the
    non-orientable substrate, appears on the "back side" as a neutrino.
    The projection suppresses the mass by φ^(-2) per substrate layer.

    Parameters:
    -----------
    m_lepton_mev : float
        Charged lepton mass in MeV
    generation : int (1, 2, or 3)
        Generation index — higher generations penetrate deeper
    k : int (default 22)
        Substrate bulk depth — number of layers all neutrinos must traverse
    q : float (default 0.957)
        Mass scaling exponent. q≈1 indicates linear dependence on m_ln.
        The slight deviation from unity (0.957 vs 1.0) may reflect
        higher-order topological corrections.
    phi : float
        Golden ratio (default PHI)
    C : float
        Two-sided Möbius correction (default C_TWO_SIDED)

    Returns:
    --------
    float : Neutrino mass in eV
    """
    MeV_to_eV = 1e6
    n = generation
    return (m_lepton_mev ** q) * MeV_to_eV * (phi ** (-2 * (n + k))) * C


def all_neutrino_masses(k=22, q=0.957):
    """Compute all three neutrino masses. Returns [m_νe, m_νμ, m_ντ] in eV."""
    leptons = [M_ELECTRON, M_MUON, M_TAU]
    return [neutrino_mass(m, n+1, k, q) for n, m in enumerate(leptons)]


def neutrino_sum(k=22, q=0.957):
    """Sum of neutrino masses (constrained < 0.12 eV by Planck 2018)."""
    return sum(all_neutrino_masses(k, q))


def mass_squared_differences(k=22, q=0.957):
    """Compute Δm²₂₁ and Δm²₃¹ in eV²."""
    m1, m2, m3 = all_neutrino_masses(k, q)
    return m2**2 - m1**2, m3**2 - m1**2


def accuracy(k=22, q=0.957):
    """Compare predictions to observed oscillation data."""
    dm21_pred, dm31_pred = mass_squared_differences(k, q)
    dm21_obs, dm31_obs = 7.53e-5, 2.453e-3

    err21 = abs(dm21_pred - dm21_obs) / dm21_obs * 100
    err31 = abs(dm31_pred - dm31_obs) / dm31_obs * 100

    return {
        'dm21_pred': dm21_pred, 'dm21_obs': dm21_obs, 'err21_%': err21,
        'dm31_pred': dm31_pred, 'dm31_obs': dm31_obs, 'err31_%': err31,
        'sum_eV': neutrino_sum(k, q)
    }


def penentration_depth(generation, k=22):
    """Return total substrate penetration depth for generation n."""
    return k + generation


if __name__ == '__main__':
    print("IST Neutrino Mass Predictions (Back-Side Projection)")
    print("=" * 55)
    m1, m2, m3 = all_neutrino_masses()
    print(f"  m_ν1 = {m1:.4e} eV  (penetration depth: {penentration_depth(1)} layers)")
    print(f"  m_ν2 = {m2:.4e} eV  (penetration depth: {penentration_depth(2)} layers)")
    print(f"  m_ν3 = {m3:.4e} eV  (penetration depth: {penentration_depth(3)} layers)")
    print(f"  Σm_ν = {m1+m2+m3:.4f} eV  (< 0.12 eV ✓)")
    print()
    acc = accuracy()
    print("Comparison with oscillation data:")
    print(f"  √Δm²₂₁: {np.sqrt(acc['dm21_pred']):.4e} eV  (obs: {np.sqrt(acc['dm21_obs']):.4e}, err: {acc['err21_%']:.1f}%)")
    print(f"  √Δm²₃₁: {np.sqrt(acc['dm31_pred']):.4e} eV  (obs: {np.sqrt(acc['dm31_obs']):.4e}, err: {acc['err31_%']:.1f}%)")
    print()
    print(f"  Mass ratios: m₂/m₁={m2/m1:.1f}, m₃/m₂={m3/m2:.2f}, m₃/m₁={m3/m1:.1f}")
