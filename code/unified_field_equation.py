# =============================================================================
# IST Unified Field Equation Module
# =============================================================================
# 
# All Standard Model forces emerge from the self-referential polynomial:
#
#   P_n(x) = c_n·x^n + φ²·x² - x + α·φ^(2n-1) = 0
#
#   n=1 (EM):     c_1 = 0      →  x = α
#   n=2 (Weak):   c_2 = 0      →  φ²x² - x + α·φ³ = 0
#   n=3 (Strong): c_3 = φ⁻²    →  φ⁻²x³ + φ²x² - x + α·φ⁵ = 0
#
# Author: Dr. Mary Theadoor (NOWN Research Collective)
# =============================================================================

import numpy as np

PHI = (1 + np.sqrt(5)) / 2
ALPHA = 1 / 137.035999084


def unified_force(n, alpha=ALPHA, phi=PHI):
    """
    Solve the IST Unified Field Equation for force of topological order n.
    """
    if n == 1:
        return alpha, "x = α", [alpha], [1.0, -alpha]

    elif n == 2:
        a, b, c = phi**2, -1.0, alpha * (phi**3)
        disc = b**2 - 4*a*c
        x1 = (-b + np.sqrt(disc)) / (2*a)
        x2 = (-b - np.sqrt(disc)) / (2*a)
        x_phys = min(x1, x2)
        coeffs = [c, b, a]
        return x_phys, "φ²x² - x + α·φ³ = 0", [x1, x2], coeffs

    elif n == 3:
        a3 = phi**(-2)
        a2 = phi**2
        a1 = -1.0
        a0 = alpha * (phi**5)
        all_roots = np.roots([a3, a2, a1, a0])
        real_pos = [r.real for r in all_roots if abs(r.imag) < 1e-8 and r.real > 0]
        x_phys = min(real_pos) if real_pos else None
        coeffs = [a0, a1, a2, a3]
        return x_phys, "φ⁻²x³ + φ²x² - x + α·φ⁵ = 0", all_roots, coeffs

    else:
        raise ValueError(f"n={n} not supported. Use n=1,2,3.")


def gravity_ist(G_newton=6.67430e-11, phi=PHI):
    """G_IST = φ² · G"""
    return phi**2 * G_newton


def planck_mass_ist(phi=PHI):
    """M_P^IST = M_P^std / φ"""
    hbar = 1.054571817e-34
    c = 2.99792458e8
    G = gravity_ist(phi=phi)
    M_P = np.sqrt(hbar * c / G)
    return M_P * c**2 / 1.602e-10


def all_forces(alpha=ALPHA, phi=PHI):
    """Compute all three force couplings."""
    empirical = {
        1: ('EM', alpha, 'Exact'),
        2: ('Weak', 1/29.53, '~1/29.53'),
        3: ('Strong', 0.118, '~0.118'),
    }
    results = {}
    for n in [1, 2, 3]:
        name, emp, label = empirical[n]
        pred, eq, roots, coeffs = unified_force(n, alpha, phi)
        err = abs(pred - emp) / emp * 100 if emp > 0 else 0
        results[name] = {
            'predicted': pred, 'empirical': emp,
            'error_%': err, 'equation': eq,
        }
    return results


if __name__ == '__main__':
    print("IST UNIFIED FIELD EQUATION")
    print("=" * 60)

    forces = all_forces()
    print(f"{'Force':<10} {'Predicted':<14} {'Empirical':<14} {'Error':<10}")
    print("-" * 50)
    for name, data in forces.items():
        print(f"{name:<10} {data['predicted']:<14.8f} {data['empirical']:<14.8f} "
              f"{data['error_%']:<10.4f}%")

    print(f"Gravity: G_IST = φ²·G = {gravity_ist():.6e} m³/kg/s²")
    print(f"Planck mass: M_P^IST = {planck_mass_ist()/1e18:.3f} × 10¹⁸ GeV")