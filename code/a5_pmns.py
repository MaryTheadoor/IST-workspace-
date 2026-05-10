"""
A5-PMNS Module: Icosahedral Symmetry and Neutrino Mixing

Derives the PMNS mixing matrix and neutrino mass scaling from A5 symmetry.

Key formulas:
  q = cos(72° · φ⁻³) = 0.9563  (neutrino mass scaling exponent)
  θ₁₂ = arcsin(√(1/(2φ))) = 33.77°  (solar mixing angle)
  θ₂₃ = 45°  (atmospheric, maximal at A5 level)
  θ₁₃ = arcsin(√(1/(2φ⁵)))  (reactor angle)
  δ = 2π/φ  (CP-violating phase)

Author: NOWN Research Collective
"""

import numpy as np

PHI = (1 + np.sqrt(5)) / 2  # Golden ratio

def q_factor():
    """
    Neutrino mass scaling exponent from A5 associator.

    q = cos(72° · φ⁻³) = cos(2π/5 · φ⁻³)

    Physical origin: The A5 associator has a geometric series expansion:
    [x,y,z] = Σ φ⁻ⁿ · e^(i·n·72°)
    The n=3 term's phase projection gives the q correction.
    """
    return np.cos(2 * np.pi / 5 * PHI**(-3))

def pmns_angles():
    """
    PMNS mixing angles from A5 icosahedral symmetry.

    Returns:
    --------
    dict with angles in degrees and radians
    """
    theta_12 = np.arcsin(np.sqrt(1 / (2 * PHI)))
    theta_23 = np.arcsin(np.sqrt(1 / 2))
    theta_13 = np.arcsin(np.sqrt(1 / (2 * PHI**5)))
    delta = 2 * np.pi / PHI

    return {
        'theta_12_deg': theta_12 * 180 / np.pi,
        'theta_23_deg': theta_23 * 180 / np.pi,
        'theta_13_deg': theta_13 * 180 / np.pi,
        'delta_deg': delta * 180 / np.pi,
        'theta_12_rad': theta_12,
        'theta_23_rad': theta_23,
        'theta_13_rad': theta_13,
        'delta_rad': delta,
    }

def pmns_matrix():
    """
    Construct the PMNS matrix from A5-derived angles.

    U = R₂₃(θ₂₃) · R₁₃(θ₁₃, δ) · R₁₂(θ₁₂)
    """
    angles = pmns_angles()

    t12, t23, t13 = angles['theta_12_rad'], angles['theta_23_rad'], angles['theta_13_rad']
    d = angles['delta_rad']

    s12, c12 = np.sin(t12), np.cos(t12)
    s23, c23 = np.sin(t23), np.cos(t23)
    s13, c13 = np.sin(t13), np.cos(t13)

    cd = np.cos(d)
    sd = np.sin(d)

    U = np.array([
        [c12*c13,             s12*c13,             s13*np.exp(-1j*d)],
        [-s12*c23-c12*s23*s13*np.exp(1j*d), c12*c23-s12*s23*s13*np.exp(1j*d), s23*c13],
        [s12*s23-c12*c23*s13*np.exp(1j*d), -c12*s23-s12*c23*s13*np.exp(1j*d), c23*c13]
    ])

    return U

def neutrino_mass_with_q(m_lepton_mev, generation, k=22):
    """
    Neutrino mass with A5-derived q correction.

    m_νn = m_ℓn^q · φ^(-2(n+k)) · C
    where q = cos(72° · φ⁻³) ≈ 0.956
    """
    from ist_neutrino import neutrino_mass
    q = q_factor()
    return neutrino_mass(m_lepton_mev, generation, k=k, q=q)


def a5_invariants():
    """
    Key A5 group invariants involving φ.

    Returns:
    --------
    dict with group-theoretic quantities
    """
    return {
        'order': 60,
        'num_classes': 5,
        'irreps': [1, 3, 3, 4, 5],
        'cos_72': np.cos(2*np.pi/5),  # 1/(2φ)
        'cos_36': np.cos(np.pi/5),     # φ/2
        'vertex_coords': [
            (0, 1, PHI),
            (0, 1, -PHI),
            (0, -1, PHI),
            (0, -1, -PHI),
            (1, PHI, 0),
            (1, -PHI, 0),
            (-1, PHI, 0),
            (-1, -PHI, 0),
            (PHI, 0, 1),
            (PHI, 0, -1),
            (-PHI, 0, 1),
            (-PHI, 0, -1),
        ],
        'edge_length_ratio': 2 / np.sqrt(PHI + 2),
        'golden_triangles': True,  # Icosahedron faces are golden triangles
    }


if __name__ == '__main__':
    print("A5-PMNS Module")
    print("=" * 50)

    print(f"
q factor: {q_factor():.6f}")

    print(f"
PMNS angles:")
    angles = pmns_angles()
    for k, v in angles.items():
        if 'deg' in k:
            print(f"  {k} = {v:.2f}°")

    print(f"
PMNS matrix:")
    U = pmns_matrix()
    print(np.round(U, 4))
