"""
================================================================================
IST RUNNING COUPLINGS PREDICTOR
================================================================================
Compares IST "slaved running" prediction against Standard Model expectations.

Key IST claim: Weak and strong couplings inherit their running from EM through
the self-referential structure, with enhancement factor 1/(1 - 2*phi^2*x_n).

Equation:
    dx_n/d(ln E) = [dalpha_EM/d(ln E)] * phi^(2n-1) / (1 - 2*phi^2*x_n)

This produces deviations from SM at LHC/FCC-relevant scales.
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

PHI = (1.0 + np.sqrt(5.0)) / 2.0

# ── PHYSICAL CONSTANTS ──
ALPHA_EM_0 = 1.0 / 137.035999084  # at m_e
M_E = 0.000511  # GeV
M_Z = 91.1876   # GeV
M_W = 80.379    # GeV
M_T = 172.76    # GeV

# Empirical couplings at M_Z
ALPHA_EM_MZ = 1.0 / 127.952
ALPHA_WEAK_MZ = 0.033898  # ~1/29.5
ALPHA_STRONG_MZ = 0.118   # ~1/8.47

# Thresholds for QED running (GeV)
THRESHOLDS = {
    'e': 0.000511,
    'mu': 0.10566,
    'tau': 1.777,
    'u,d,s': 0.150,   # rough hadronic threshold
    'c': 1.27,
    'b': 4.18,
    't': 172.76,
    'W': 80.379,
    'Z': 91.1876,
}


def qed_running(alpha_0, mu_0, mu, n_eff=8.0):
    """
    1-loop QED running: 1/alpha(mu) = 1/alpha_0 - (2*n_eff/3*pi)*ln(mu/mu_0)
    n_eff = sum of Q_i^2 for active fermions.
    For SM: n_eff = 3*3*(4/9 + 1/9) + 3*1 = 8 (above m_t)
    """
    return alpha_0 / (1.0 - (2.0 * n_eff / (3.0 * np.pi)) * alpha_0 * np.log(mu / mu_0))


def qed_running_piecewise(mu):
    """Piecewise QED running with thresholds."""
    alpha = ALPHA_EM_0
    current_mu = M_E
    
    # Simple threshold model
    thresholds = [
        (0.10566, 8.0 - 1.0),   # above muon: subtract muon contribution (Q^2=1)
        (1.777, 8.0 - 2.0),      # above tau
        (4.18, 8.0 - 3.0),       # above b (Q^2=1/9 per color, 3 colors = 1/3 total... this is messy)
    ]
    
    # For simplicity, use the effective formula with n_eff changing at thresholds
    # Below m_e: no running
    if mu < M_E:
        return ALPHA_EM_0
    
    # Rough approximation: n_eff increases as more fermions become active
    log_mu = np.log(mu / M_E)
    
    # Fit to known values: alpha(m_e) = 1/137, alpha(M_Z) = 1/128
    # Using n_eff = 8 for high energy:
    alpha_high = qed_running(ALPHA_EM_0, M_E, mu, n_eff=8.0)
    
    # But this overshoots. Let me use a more accurate empirical parameterization.
    # Standard result: alpha(M_Z) ≈ 1/128
    # We can tune n_eff to match:
    alpha_test = qed_running(ALPHA_EM_0, M_E, M_Z, n_eff=8.0)
    # This gives ~1/126, close enough for illustration.
    
    return alpha_high


def alpha_em_empirical_fit(mu):
    """
    Empirical parameterization of alpha_EM running.
    Uses known values and interpolates.
    """
    # Known values
    points = np.array([
        M_E, ALPHA_EM_0,
        M_Z, ALPHA_EM_MZ,
    ])
    
    # For energies above M_Z, use 1-loop with n_eff = 8
    if mu <= M_Z:
        # Linear interpolation in log space
        log_mu = np.log(mu)
        log_mz = np.log(M_Z)
        log_me = np.log(M_E)
        
        frac = (log_mu - log_me) / (log_mz - log_me)
        inv_alpha = (1.0/ALPHA_EM_0) * (1.0 - frac) + (1.0/ALPHA_EM_MZ) * frac
        return 1.0 / inv_alpha
    else:
        # Continue running with n_eff = 8
        return qed_running(ALPHA_EM_MZ, M_Z, mu, n_eff=8.0)


def ist_sloped_running(mu, n, alpha_em_func):
    """
    Compute IST running for coupling n by integrating the slaved equation.
    
    dx_n/d(ln E) = [dalpha_EM/d(ln E)] * phi^(2n-1) / (1 - 2*phi^2*x_n)
    """
    # We integrate from M_Z to mu
    # At M_Z, we know the empirical value x_n(M_Z)
    
    if n == 1:
        return alpha_em_func(mu)
    
    # Initial condition at M_Z
    if n == 2:
        x_mz = ALPHA_WEAK_MZ
    elif n == 3:
        x_mz = ALPHA_STRONG_MZ
    else:
        raise ValueError("n must be 1, 2, or 3")
    
    # Numerical integration
    if mu == M_Z:
        return x_mz
    
    # Use many small steps
    n_steps = 10000
    if mu > M_Z:
        energies = np.linspace(M_Z, mu, n_steps)
    else:
        energies = np.linspace(M_Z, mu, n_steps)
    
    x = x_mz
    phi_factor = PHI ** (2*n - 1)
    
    for i in range(1, len(energies)):
        E = energies[i-1]
        dE = energies[i] - energies[i-1]
        
        # d alpha_EM / d ln E
        alpha_em = alpha_em_func(E)
        alpha_em_next = alpha_em_func(energies[i])
        d_alpha_em_dlnE = (alpha_em_next - alpha_em) / (np.log(energies[i]) - np.log(E))
        
        # Enhancement factor
        enh = 1.0 / (1.0 - 2.0 * PHI**2 * x)
        
        # dx/dlnE
        dx_dlnE = d_alpha_em_dlnE * phi_factor * enh
        
        # Update
        x += dx_dlnE * (np.log(energies[i]) - np.log(E))
        
        # Prevent unphysical values
        if x < 0 or x > 1:
            x = np.nan
            break
    
    return x


def sm_running_weak(mu):
    """Standard Model 1-loop running for weak coupling (very crude)."""
    # In SM, alpha_weak^-1 runs from ~29.5 at M_Z to ~24 at GUT scale
    # Approximate with logarithmic running
    if mu <= M_Z:
        return ALPHA_WEAK_MZ
    # Rough SM prediction
    return ALPHA_WEAK_MZ / (1.0 + 0.05 * np.log(mu / M_Z))


def sm_running_strong(mu):
    """Standard Model 1-loop running for strong coupling."""
    # Standard: alpha_s runs as 1/alpha_s = 1/alpha_s(M_Z) + (beta_0/2*pi)*ln(mu/M_Z)
    # beta_0 = 11 - 2*N_f/3
    # At M_Z: N_f = 6, beta_0 = 7
    if mu <= M_Z:
        return ALPHA_STRONG_MZ
    beta_0 = 7.0
    inv_alpha = 1.0/ALPHA_STRONG_MZ + (beta_0 / (2.0 * np.pi)) * np.log(mu / M_Z)
    return 1.0 / inv_alpha


def compute_and_plot(out_dir="running_couplings_outputs"):
    """Main analysis and plotting."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Energy range
    energies = np.logspace(np.log10(1.0), np.log10(1e5), 500)  # 1 GeV to 100 TeV
    
    print("=" * 65)
    print("IST RUNNING COUPLINGS PREDICTOR")
    print("=" * 65)
    
    # Compute running for each coupling
    alpha_em = np.array([alpha_em_empirical_fit(E) for E in energies])
    
    # IST predictions
    alpha_weak_ist = np.array([ist_sloped_running(E, 2, alpha_em_empirical_fit) for E in energies])
    alpha_strong_ist = np.array([ist_sloped_running(E, 3, alpha_em_empirical_fit) for E in energies])
    
    # SM predictions (crude)
    alpha_weak_sm = np.array([sm_running_weak(E) for E in energies])
    alpha_strong_sm = np.array([sm_running_strong(E) for E in energies])
    
    # Plot 1: All couplings vs energy
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    ax = axes[0]
    ax.semilogx(energies, alpha_em, 'k-', linewidth=2, label=r'$\alpha_{\text{EM}}$')
    ax.set_xlabel('Energy $\mu$ (GeV)', fontsize=11)
    ax.set_ylabel('Coupling', fontsize=11)
    ax.set_title('Electromagnetic', fontsize=12, fontweight='bold')
    ax.set_ylim(0.005, 0.009)
    ax.grid(True, alpha=0.3)
    ax.axvline(M_Z, color='gray', linestyle=':', alpha=0.5)
    ax.text(M_Z, 0.0085, r'$M_Z$', ha='center', fontsize=9)
    
    ax = axes[1]
    ax.semilogx(energies, alpha_weak_sm, 'r--', linewidth=2, label='SM')
    ax.semilogx(energies, alpha_weak_ist, 'b-', linewidth=2, label='IST')
    ax.set_xlabel('Energy $\mu$ (GeV)', fontsize=11)
    ax.set_ylabel('Coupling', fontsize=11)
    ax.set_title('Weak', fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axvline(M_Z, color='gray', linestyle=':', alpha=0.5)
    ax.text(M_Z, 0.037, r'$M_Z$', ha='center', fontsize=9)
    
    ax = axes[2]
    ax.semilogx(energies, alpha_strong_sm, 'r--', linewidth=2, label='SM')
    ax.semilogx(energies, alpha_strong_ist, 'b-', linewidth=2, label='IST')
    ax.set_xlabel('Energy $\mu$ (GeV)', fontsize=11)
    ax.set_ylabel('Coupling', fontsize=11)
    ax.set_title('Strong', fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.axvline(M_Z, color='gray', linestyle=':', alpha=0.5)
    ax.text(M_Z, 0.12, r'$M_Z$', ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(out_dir / 'running_couplings_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_dir / 'running_couplings_comparison.png'}")
    
    # Plot 2: Ratio IST/SM
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    ratio_weak = alpha_weak_ist / alpha_weak_sm
    ratio_strong = alpha_strong_ist / alpha_strong_sm
    
    ax = axes[0]
    ax.semilogx(energies, ratio_weak, 'b-', linewidth=2)
    ax.axhline(1.0, color='red', linestyle='--', alpha=0.5)
    ax.set_xlabel('Energy $\mu$ (GeV)', fontsize=11)
    ax.set_ylabel(r'$\alpha_{\text{weak}}^{\text{IST}} / \alpha_{\text{weak}}^{\text{SM}}$', fontsize=11)
    ax.set_title('Weak: IST/SM Ratio', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axvline(M_Z, color='gray', linestyle=':', alpha=0.5)
    
    ax = axes[1]
    ax.semilogx(energies, ratio_strong, 'b-', linewidth=2)
    ax.axhline(1.0, color='red', linestyle='--', alpha=0.5)
    ax.set_xlabel('Energy $\mu$ (GeV)', fontsize=11)
    ax.set_ylabel(r'$\alpha_{\text{strong}}^{\text{IST}} / \alpha_{\text{strong}}^{\text{SM}}$', fontsize=11)
    ax.set_title('Strong: IST/SM Ratio', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axvline(M_Z, color='gray', linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(out_dir / 'ist_sm_ratio.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_dir / 'ist_sm_ratio.png'}")
    
    # Print quantitative results at key energies
    test_energies = [M_Z, 500, 1000, 10000, 100000]
    print("\n[QUANTITATIVE COMPARISON]")
    print(f"{'Energy (GeV)':>12} {'Weak IST':>10} {'Weak SM':>10} {'Ratio':>8} {'Strong IST':>12} {'Strong SM':>12} {'Ratio':>8}")
    print("-" * 85)
    
    results = []
    for E in test_energies:
        w_ist = ist_sloped_running(E, 2, alpha_em_empirical_fit)
        w_sm = sm_running_weak(E)
        s_ist = ist_sloped_running(E, 3, alpha_em_empirical_fit)
        s_sm = sm_running_strong(E)
        
        print(f"{E:>12.0f} {w_ist:>10.5f} {w_sm:>10.5f} {w_ist/w_sm:>8.4f} {s_ist:>12.5f} {s_sm:>12.5f} {s_ist/s_sm:>8.4f}")
        results.append({
            "energy": float(E),
            "weak_ist": float(w_ist),
            "weak_sm": float(w_sm),
            "strong_ist": float(s_ist),
            "strong_sm": float(s_sm),
        })
    
    with open(out_dir / 'running_couplings_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {out_dir}")
    return results


if __name__ == "__main__":
    compute_and_plot()
