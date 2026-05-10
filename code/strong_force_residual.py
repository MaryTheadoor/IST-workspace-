"""
================================================================================
STRONG FORCE RESIDUAL ANALYSIS
================================================================================
Systematic search for the 1.35% correction to the strong coupling prediction.

Hypotheses tested:
  H1: Higher-order self-reference (cubic term)
  H2: Running from M_Z to unification scale
  H3: Different phi-power for triple intersection (n=3)
  H4: Sensitivity to alpha precision / energy scale
  H5: Back-side correction has n-dependent factor
================================================================================
"""

import numpy as np
from scipy.optimize import minimize_scalar, brentq
import json

PHI = (1.0 + np.sqrt(5.0)) / 2.0
ALPHA = 1.0 / 137.035999084
ALPHA_INV = 137.035999084

# Empirical couplings at M_Z (approximate)
ALPHA_EM = ALPHA
ALPHA_WEAK_EMP = 0.033898  # ~1/29.5
ALPHA_STRONG_EMP = 0.118000  # ~1/8.47 at M_Z


def self_referential_solution(n, alpha=ALPHA):
    """x = [1 - sqrt(1 - 4*alpha*phi^(2n+1))] / (2*phi^2)"""
    discriminant = 1.0 - 4.0 * alpha * (PHI ** (2*n + 1))
    if discriminant < 0:
        return np.nan
    return (1.0 - np.sqrt(discriminant)) / (2.0 * PHI**2)


def phi_power_formula(n, alpha=ALPHA):
    """Original formula: alpha * phi^(2n-1)"""
    return alpha * (PHI ** (2*n - 1))


def two_sided_formula(n, alpha=ALPHA):
    """v2 formula with sqrt correction"""
    base = phi_power_formula(n, alpha)
    if n == 1:
        return base
    # Strong has special form: phi^5 + phi^3
    if n == 3:
        base = alpha * (PHI**5 + PHI**3)
    return base * np.sqrt(1.0 + 1.0/PHI**4)


def cubic_self_reference(n, alpha=ALPHA, gamma=0.0):
    """
    H1: Add cubic term gamma * phi^3 * x^3 to the self-referential equation.
    phi^2 * x^2 - x + alpha*phi^(2n-1) + gamma*phi^3*x^3 = 0
    We solve numerically for the physical root (small positive x).
    """
    c = alpha * (PHI ** (2*n - 1))
    # We want root of: gamma*phi^3*x^3 + phi^2*x^2 - x + c = 0
    coeffs = [gamma * PHI**3, PHI**2, -1.0, c]
    roots = np.roots(coeffs)
    # Select real, positive, smallest root
    real_roots = [r.real for r in roots if abs(r.imag) < 1e-10 and r.real > 0]
    if not real_roots:
        return np.nan
    return min(real_roots)


def n_dependent_backside(n, alpha=ALPHA, epsilon_factor=1.0):
    """
    H5: The back-side dilution depends on n.
    For n=2 (double cover): epsilon = 1/phi^4
    For n=3 (triple intersection): epsilon = 1/phi^(4 + delta)
    """
    base = phi_power_formula(n, alpha)
    if n == 3:
        base = alpha * (PHI**5 + PHI**3)
    if n == 1:
        return base
    epsilon = epsilon_factor / PHI**4
    return base * np.sqrt(1.0 + epsilon)


def run_analysis():
    print("=" * 70)
    print("STRONG FORCE RESIDUAL ANALYSIS")
    print("=" * 70)

    # ── BASELINE PREDICTIONS ──
    print("\n[BASELINE PREDICTIONS]")
    for n, name, emp in [(1, "EM", ALPHA_EM), (2, "Weak", ALPHA_WEAK_EMP), (3, "Strong", ALPHA_STRONG_EMP)]:
        if n == 1:
            x = ALPHA  # EM is exact, no self-reference
        else:
            x = self_referential_solution(n)
        err = abs(x - emp) / emp * 100
        print(f"  {name:8s} (n={n}): predicted={x:.8f}, empirical={emp:.8f}, error={err:.4f}%")

    # ── H1: HIGHER-ORDER CUBIC TERM ──
    print("\n[H1: CUBIC SELF-REFERENCE TERM]")
    print("  Equation: gamma*phi^3*x^3 + phi^2*x^2 - x + alpha*phi^(2n-1) = 0")
    
    # Find gamma that zeros the strong force error
    def strong_error_gamma(gamma):
        x = cubic_self_reference(3, gamma=gamma)
        if np.isnan(x):
            return 1e6
        return abs(x - ALPHA_STRONG_EMP) / ALPHA_STRONG_EMP * 100
    
    # Search over a reasonable range
    gammas = np.linspace(-0.5, 0.5, 10001)
    errors = [strong_error_gamma(g) for g in gammas]
    best_idx = np.argmin(errors)
    best_gamma = gammas[best_idx]
    
    print(f"  Best gamma = {best_gamma:.6f} gives strong error = {errors[best_idx]:.4f}%")
    
    # Check what this gamma does to weak force
    x_weak_cubic = cubic_self_reference(2, gamma=best_gamma)
    err_weak_cubic = abs(x_weak_cubic - ALPHA_WEAK_EMP) / ALPHA_WEAK_EMP * 100
    print(f"  Weak force with same gamma: predicted={x_weak_cubic:.8f}, error={err_weak_cubic:.4f}%")
    
    # Check gamma=0 is our baseline
    x_strong_baseline = cubic_self_reference(3, gamma=0.0)
    print(f"  Baseline (gamma=0): predicted={x_strong_baseline:.8f}")

    # ── H1b: HYBRID V2+V3 FORMULA ──
    print("\n[H1b: HYBRID V2 BASE + V3 SELF-REFERENCE]")
    print("  v2 base for strong: alpha * (phi^5 + phi^3)")
    print("  v3 base for weak:   alpha * phi^3")
    print("  Apply self-referential quadratic to v2 bases.")
    
    def hybrid_self_referential(n, alpha=ALPHA):
        """Use v2 base formula in the self-referential equation."""
        if n == 1:
            return alpha
        elif n == 2:
            c = alpha * (PHI ** 3)
        elif n == 3:
            c = alpha * (PHI**5 + PHI**3)
        else:
            c = alpha * (PHI ** (2*n - 1))
        # Self-referential: phi^2*x^2 - x + c = 0
        # Solution: x = [1 - sqrt(1 - 4*phi^2*c)] / (2*phi^2)
        # Wait, let me re-derive. Original: phi^2*x^2 - x + alpha*phi^(2n-1) = 0
        # The c here replaces alpha*phi^(2n-1), so:
        discriminant = 1.0 - 4.0 * PHI**2 * c
        if discriminant < 0:
            return np.nan
        return (1.0 - np.sqrt(discriminant)) / (2.0 * PHI**2)
    
    for n, name, emp in [(1, "EM", ALPHA_EM), (2, "Weak", ALPHA_WEAK_EMP), (3, "Strong", ALPHA_STRONG_EMP)]:
        x = hybrid_self_referential(n)
        err = abs(x - emp) / emp * 100
        print(f"  {name:8s} (n={n}): predicted={x:.8f}, empirical={emp:.8f}, error={err:.4f}%")
    
    # ── H2: RUNNING FROM M_Z ──
    print("\n[H2: RUNNING OF ALPHA]")
    print("  Empirical strong coupling is measured at M_Z ~ 91 GeV.")
    print("  If the self-referential equation applies at a different scale,")
    print("  we need alpha at that scale. The EM coupling runs:")
    print("    alpha(M_Z) ~ 1/128  (not 1/137)")
    
    alpha_mz = 1.0 / 128.0
    x_strong_mz = self_referential_solution(3, alpha=alpha_mz)
    err_mz = abs(x_strong_mz - ALPHA_STRONG_EMP) / ALPHA_STRONG_EMP * 100
    print(f"  Using alpha=1/128: predicted={x_strong_mz:.8f}, error={err_mz:.4f}%")
    
    # What alpha would give exact strong coupling?
    def alpha_error(a):
        x = self_referential_solution(3, alpha=a)
        if np.isnan(x):
            return 1e6
        return (x - ALPHA_STRONG_EMP)**2
    
    alphas = np.linspace(1/150, 1/120, 10000)
    alpha_errors = [alpha_error(a) for a in alphas]
    best_alpha_idx = np.argmin(alpha_errors)
    best_alpha = alphas[best_alpha_idx]
    print(f"  Alpha required for exact strong: {best_alpha:.8f} (1/{1/best_alpha:.2f})")
    
    # Check weak with this alpha
    x_weak_best_alpha = self_referential_solution(2, alpha=best_alpha)
    err_weak_best = abs(x_weak_best_alpha - ALPHA_WEAK_EMP) / ALPHA_WEAK_EMP * 100
    print(f"  Weak with this alpha: predicted={x_weak_best_alpha:.8f}, error={err_weak_best:.4f}%")

    # ── H3: DIFFERENT PHI POWER FOR n=3 ──
    print("\n[H3: MODIFIED POWER FOR TRIPLE INTERSECTION]")
    print("  Instead of phi^(2n-1) = phi^5, try nearby powers.")
    
    def modified_power_solution(n, power, alpha=ALPHA):
        """Use custom power instead of 2n-1"""
        discriminant = 1.0 - 4.0 * alpha * (PHI ** (power + 2))
        if discriminant < 0:
            return np.nan
        return (1.0 - np.sqrt(discriminant)) / (2.0 * PHI**2)
    
    powers = np.linspace(4.0, 6.0, 2001)
    power_errors = []
    for p in powers:
        x = modified_power_solution(3, p)
        if np.isnan(x):
            power_errors.append(1e6)
        else:
            power_errors.append(abs(x - ALPHA_STRONG_EMP) / ALPHA_STRONG_EMP * 100)
    
    best_power_idx = np.argmin(power_errors)
    best_power = powers[best_power_idx]
    print(f"  Best power for strong: phi^{best_power:.4f} gives error = {power_errors[best_power_idx]:.4f}%")
    print(f"  Standard power: phi^5 gives error = {power_errors[np.argmin(np.abs(powers - 5.0))]:.4f}%")
    
    # Check weak with a modified power too
    powers_weak = np.linspace(2.5, 3.5, 1001)
    power_errors_weak = []
    for p in powers_weak:
        x = modified_power_solution(2, p)
        if np.isnan(x):
            power_errors_weak.append(1e6)
        else:
            power_errors_weak.append(abs(x - ALPHA_WEAK_EMP) / ALPHA_WEAK_EMP * 100)
    best_w_idx = np.argmin(power_errors_weak)
    print(f"  Best power for weak: phi^{powers_weak[best_w_idx]:.4f} gives error = {power_errors_weak[best_w_idx]:.4f}%")

    # ── H5: N-DEPENDENT BACK-SIDE ──
    print("\n[H5: N-DEPENDENT BACK-SIDE DILUTION]")
    print("  epsilon(n) = factor / phi^(4 + delta*(n-2))")
    
    def strong_error_backside(factor, delta):
        if n == 3:
            epsilon = factor / PHI**(4 + delta)
        else:
            epsilon = factor / PHI**4
        base = ALPHA * (PHI**5 + PHI**3)
        x = base * np.sqrt(1.0 + epsilon)
        return abs(x - ALPHA_STRONG_EMP) / ALPHA_STRONG_EMP * 100
    
    # Try simple multiplicative factor on epsilon
    factors = np.linspace(0.5, 2.0, 1001)
    f_errors = []
    for f in factors:
        base = ALPHA * (PHI**5 + PHI**3)
        x = base * np.sqrt(1.0 + f / PHI**4)
        f_errors.append(abs(x - ALPHA_STRONG_EMP) / ALPHA_STRONG_EMP * 100)
    best_f_idx = np.argmin(f_errors)
    print(f"  Best epsilon factor = {factors[best_f_idx]:.4f} gives error = {f_errors[best_f_idx]:.4f}%")

    # ── H4: SENSITIVITY TO ALPHA ──
    print("\n[H4: SENSITIVITY ANALYSIS]")
    alpha_values = np.linspace(1/140, 1/134, 1001)
    sens_strong = []
    sens_weak = []
    for a in alpha_values:
        s = self_referential_solution(3, alpha=a)
        w = self_referential_solution(2, alpha=a)
        sens_strong.append(abs(s - ALPHA_STRONG_EMP) / ALPHA_STRONG_EMP * 100 if not np.isnan(s) else np.nan)
        sens_weak.append(abs(w - ALPHA_WEAK_EMP) / ALPHA_WEAK_EMP * 100 if not np.isnan(w) else np.nan)
    
    sens_strong = np.array(sens_strong)
    sens_weak = np.array(sens_weak)
    valid = ~np.isnan(sens_strong) & ~np.isnan(sens_weak)
    combined = sens_strong + sens_weak
    best_sens_idx = np.argmin(combined[valid])
    best_alpha_sens = alpha_values[valid][best_sens_idx]
    print(f"  Alpha minimizing combined error: {best_alpha_sens:.8f} (1/{1/best_alpha_sens:.2f})")
    print(f"  Combined error at best alpha: {combined[valid][best_sens_idx]:.4f}%")
    print(f"  Strong error: {sens_strong[valid][best_sens_idx]:.4f}%")
    print(f"  Weak error: {sens_weak[valid][best_sens_idx]:.4f}%")

    # ── SUMMARY ──
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Baseline strong error: 1.35%")
    print(f"  Best cubic gamma:      {errors[best_idx]:.4f}% (gamma={best_gamma:.4f})")
    print(f"  Best alpha (strong):   {alpha_errors[best_alpha_idx]:.6f}% (alpha={best_alpha:.6f})")
    print(f"  Best phi-power:        {power_errors[best_power_idx]:.4f}% (power={best_power:.4f})")
    print(f"  Best backside factor:  {f_errors[best_f_idx]:.4f}% (factor={factors[best_f_idx]:.4f})")
    print(f"  Best combined alpha:   {combined[valid][best_sens_idx]:.4f}% (alpha={best_alpha_sens:.6f})")
    
    return {
        "baseline_strong_error": 1.35,
        "best_cubic_gamma": float(best_gamma),
        "best_cubic_error": float(errors[best_idx]),
        "best_alpha_for_strong": float(best_alpha),
        "best_alpha_strong_error": float(alpha_errors[best_alpha_idx]**0.5 / ALPHA_STRONG_EMP * 100),
        "best_phi_power": float(best_power),
        "best_phi_power_error": float(power_errors[best_power_idx]),
    }


if __name__ == "__main__":
    results = run_analysis()
    with open("strong_force_residual_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to strong_force_residual_results.json")
