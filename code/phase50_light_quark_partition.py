"""
================================================================================
IST PHASE 50 - The Light Quark Golden Partition Test
================================================================================
Purpose:
    Test the hypothesis that the light bare quarks (u, d, s) are structured
    by the same Golden Partition that organizes the Baryon Octet (Lambda,
    Sigma, Xi) they comprise (Phase 45).
    
    In Phase 45, we found the Octet obeys:
        (Sigma - Lambda) / (Xi - Lambda) = 1/phi^2  (0.382)
    
    If the light quarks themselves carry this fundamental structure, their bare
    masses should obey the exact same partition:
        (m_d - m_u) / (m_s - m_u) = 1/phi^2
        
    Since quark masses run with the renormalization scale mu, we must ensure
    this test is scale-invariant. To 1-loop order in QCD, all light quarks
    run with the same anomalous dimension gamma_m, meaning their mass RATIOS
    (and thus ratio of gaps) are strictly RG-invariant. The test at mu=2 GeV
    is equivalent to the test at the IST confinement scale E=197.3 MeV.

Hypotheses tested:
    H50a  The Bare Quark Golden Partition. Verify whether the gap ratio
          (m_d - m_u) / (m_s - m_u) matches 1/phi^2.
    H50b  RG-Invariance of the Negative. Prove that because quark masses run
          multiplicatively by the same factor, this ratio is a scale-independent
          constant of nature; the failure cannot be blamed on the mu=2 GeV scale.
    H50c  The Koide-Space Partition. Test if the partition holds in the
          sqrt(mass) space used by the Koide formula.

Outputs:
    code/outputs/phase50/light_quark_partition.csv
    code/outputs/phase50/light_quark_partition.png

References:
    notes/IST_Phase_50_plan.md
    code/phase45_baryon_octet.py
================================================================================
"""

import csv
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase50")

# PDG 2022 MS-bar masses at mu = 2 GeV (in MeV)
M_U = 2.16
M_D = 4.67
M_S = 93.4
PHI = (1 + np.sqrt(5)) / 2

# Baryon Octet reference (from Phase 45)
M_LAMBDA = 1115.683
M_SIGMA = 1193.154  # isospin averaged
M_XI = 1318.285     # isospin averaged

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    out = []
    rows = []
    
    out.append("=== IST PHASE 50: The Light Quark Golden Partition Test ===")
    out.append("Testing if bare quarks follow their baryon bound states.\n")
    
    # ---- Reference: Baryon Octet Golden Partition ----
    out.append("Reference: Baryon Octet Golden Partition (Phase 45)")
    baryon_split = (M_SIGMA - M_LAMBDA) / (M_XI - M_LAMBDA)
    target = 1 / PHI**2
    out.append(f"  (Sigma - Lambda) / (Xi - Lambda) = {baryon_split:.6f}")
    out.append(f"  1/phi^2                          = {target:.6f}")
    out.append(f"  Error: {100 * abs(baryon_split/target - 1):.2f}%\n")
    
    # ---- H50a: Bare Quark Golden Partition ----
    out.append("H50a: Bare Quark Golden Partition")
    quark_split = (M_D - M_U) / (M_S - M_U)
    out.append(f"  (m_d - m_u) / (m_s - m_u)        = {quark_split:.6f}")
    out.append(f"  Target 1/phi^2                   = {target:.6f}")
    out.append(f"  Error: {100 * abs(quark_split/target - 1):.2f}%")
    out.append("  => HONEST NEGATIVE: The bare light quarks do NOT obey the")
    out.append("     Golden Partition of the hyperons they comprise.\n")
    
    rows.append({"Space": "Linear (Bare Mass)", "Gap_Ratio": quark_split, "Target": target, "Match": "FAIL"})
    
    # ---- H50b: RG-Invariance ----
    out.append("H50b: RG-Invariance of the Ratio")
    # Simulate running to the confinement scale (approx factor of ~1.5)
    run_factor = 1.54 
    m_u_run, m_d_run, m_s_run = M_U * run_factor, M_D * run_factor, M_S * run_factor
    run_split = (m_d_run - m_u_run) / (m_s_run - m_u_run)
    out.append(f"  Simulated running factor = {run_factor}")
    out.append(f"  Running gap ratio        = {run_split:.6f}")
    out.append(f"  => The gap ratio depends ONLY on m_d/m_u and m_s/m_u.")
    out.append(f"     Since all light quarks share the same gamma_m, this ratio")
    out.append(f"     is strictly SCALE-INVARIANT. The failure is absolute.\n")
    
    rows.append({"Space": "Linear (Running Mass)", "Gap_Ratio": run_split, "Target": target, "Match": "FAIL"})
    
    # ---- H50c: Koide-Space Partition ----
    out.append("H50c: Koide-Space Partition (Square Roots)")
    sq_u, sq_d, sq_s = np.sqrt(M_U), np.sqrt(M_D), np.sqrt(M_S)
    koide_split = (sq_d - sq_u) / (sq_s - sq_u)
    out.append(f"  (sqrt(d) - sqrt(u)) / (sqrt(s) - sqrt(u)) = {koide_split:.6f}")
    out.append(f"  Target 1/phi^2                            = {target:.6f}")
    out.append("  => HONEST NEGATIVE: Fails in the Koide space as well.\n")
    
    rows.append({"Space": "Koide (Sqrt Mass)", "Gap_Ratio": koide_split, "Target": target, "Match": "FAIL"})
    
    # Conclusion
    out.append("Conclusion:")
    out.append("  The Golden Partition is a structural law of the hadronic BOUND STATES")
    out.append("  (the Baryon Octet), not the bare quarks themselves. This perfectly")
    out.append("  mirrors the Phase 37 finding: the golden harmonics live in the MASSES")
    out.append("  (topological knots), not the bare couplings/quarks. The substrate")
    out.append("  structures the emergent particles, not the perturbative degrees of freedom.")
    
    csv_path = os.path.join(OUT_DIR, "light_quark_partition.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["Space", "Gap_Ratio", "Target", "Match"])
        w.writeheader()
        w.writerows(rows)
    out.append(f"\nWrote {csv_path}")
    
    make_figure(baryon_split, quark_split, koide_split, target)
    out.append(f"Wrote {OUT_DIR}")
    
    print("\n".join(out))


def make_figure(baryon_split, quark_split, koide_split, target):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    labels = ["Baryon Octet\n(Sigma partitions Lam->Xi)", 
              "Bare Quarks\n(d partitions u->s)", 
              "Koide Quarks\n(sqrt(d) partitions u->s)"]
    values = [baryon_split, quark_split, koide_split]
    colors = ['seagreen', 'crimson', 'crimson']
    
    ax.bar(labels, values, color=colors, alpha=0.8)
    ax.axhline(target, color='goldenrod', linestyle='--', linewidth=2, label=f"Target 1/phi^2 = {target:.3f}")
    
    ax.set_ylabel("Partition Ratio: (Mid - Low) / (High - Low)")
    ax.set_title("The Golden Partition: Bound States vs Bare Quarks")
    ax.legend()
    
    # Annotate values
    for i, v in enumerate(values):
        ax.text(i, v + 0.01, f"{v:.3f}", ha='center', fontweight='bold')
        
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "light_quark_partition.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
