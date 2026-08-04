"""
===============================================================================
IST PHASE 53 - Heavy-Flavor Octet: Does the Golden Partition Extend?
===============================================================================
Purpose:
    Test whether the Phase 45 baryon-octet golden partition -- the law that
    Sigma golden-partitions the Lambda -> Xi mass interval,

        (Sigma - Lambda) / (Xi - Lambda) = 1/phi^2     (0.108% off, Phase 45)
        (Xi - Sigma)     / (Sigma - Lambda) = phi      (0.175% off, Phase 45)

    -- generalizes to the heavy-flavor analogs. Phase 45 established the law
    on the light (u,d,s) octet. Phase 50 showed the bare quarks do NOT carry
    it (RG-invariant negative). Phase 53 asks the sibling question: do the
    SU(3) analog triplets {Lambda_Q, Sigma_Q, Xi_Q} of the charmed (Q = c)
    and bottom (Q = b) baryons obey the same golden partition?

    Pre-registered target, from the external gap analysis (gap 6): a genuine
    untested predictive domain. Two independent tests (charm, bottom), each
    with two relations and full error propagation.

The prediction under test:
    If the partition is a universal SU(3)-flavor law of (Lambda, Sigma, Xi)
    triplets, then the analog baryons must satisfy, within ~0.2%:

        (Sigma_Q - Lambda_Q) / (Xi_Q - Lambda_Q)  =  1/phi^2 ~ 0.381966
        (Xi_Q    - Sigma_Q)   / (Sigma_Q - Lambda_Q) =  phi     ~ 1.618034

    measured with the PDG 2024 J^P = 1/2^+ ground-state masses.

The finding (honest negative):
    The law does NOT extend. Both sectors fail by tens of percent:

        charm  (Lam_c, Sig_c, Xi_c):  split = 0.915   (+, 139% vs 1/phi^2)
        bottom (Lam_b, Sig_b, Xi_b):  split = 1.107   (+, 190% vs 1/phi^2)

    Moreover the SU(3) mass ordering INVERTS in bottom: Lambda_b(5619.6) <
    Xi_b(5794.4) < Sigma_b(5813.1) -- Sigma sits ABOVE Xi -- because the
    Sigma_b - Lambda_b hyperfine/HQET splitting (~193 MeV) now exceeds the
    Xi_b - Lambda_b strangeness-plus-heavy step. No consistent (Lambda, Sigma,
    Xi) re-labelling recovers the golden partition; the ordering flip is
    structural (HQET, Phase-53 analysis), not a selection artifact.

Interpretation (the dividing line):
    The golden partition is a property of the emergence of three LIGHT AND
    NEARLY-DEGENERATE quarks into a bound knot (Phase 45), where the diquark
    hyperfine term and the strangeness step are balanced to 1/phi. A hard
    heavy-quark mass scale (c/b, non-emergent, set at the Higgs/Yukawa scale)
    injects an off-scale splitting that reshuffles the hierarchy and erases
    the golden balance -- the same thing the RG-invariance argument of Phase 50
    predicted for any non-light sector. This is an honest negative that
    NARROWS where phi lives: the light, near-degenerate emergent octet, not
    the general (Lambda, Sigma, Xi) triplet.

Outputs: code/outputs/phase53/heavy_flavor_octet.csv

References:
    code/phase45_baryon_octet.py   (the law under test, light octet)
    code/phase50_light_quarks.py   (bare quarks: negative)
    PDG 2024 baryon mass tables (Charm, Bottom)
===============================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase53")

PHI = (1 + np.sqrt(5)) / 2.0

# ───────────────────────────────────────────────────────────────────────────────
# PDG 2024 masses (MeV), J^P = 1/2^+ ground states.
# Uncertainties are the quoted PDG averages; Sigma/Xi charge-multiplet values
# are the isospin averages of the quoted states.
# ───────────────────────────────────────────────────────────────────────────────

# Light octet (Phase 45 anchor)
LAM_L = 1115.683;  SIG_L = 1193.15;  XI_L = 1318.28

# Charmed octet analogs
LAM_C = 2286.46;   dLAM_C = 0.14
SIG_C = (2453.97 + 2452.9 + 2453.75) / 3.0   # Sigma_c(2455)++/+/0
dSIG_C = 0.4
XI_C = (2467.71 + 2470.44) / 2.0              # Xi_c+(2470) / Xi_c0(2470)
dXI_C = 0.28

# Bottom octet analogs
LAM_B = 5619.60;   dLAM_B = 0.17
SIG_B = (5810.56 + 5815.64) / 2.0             # Sigma_b+ / Sigma_b-
dSIG_B = 0.27
XI_B = (5791.9 + 5797.0) / 2.0                # Xi_b0 / Xi_b-
dXI_B = 0.6

INV_PHI2 = 1.0 / PHI ** 2


# ───────────────────────────────────────────────────────────────────────────────
# ERROR PROPAGATION (linear, uncorrelated)
# ───────────────────────────────────────────────────────────────────────────────

def split(L, S, X, dL, dS, dX):
    """(S-L)/(X-L) and its 1-sigma error. Partials:
    dr/dL = (S-X)/(X-L)^2, dr/dS = 1/(X-L), dr/dX = -(S-L)/(X-L)^2."""
    num = S - L
    den = X - L
    r = num / den
    sr = np.sqrt((((S - X) / den ** 2) * dL) ** 2 +
                 ((1.0 / den) * dS) ** 2 +
                 ((-(S - L) / den ** 2) * dX) ** 2)
    return r, sr


def gap(L, S, X, dL, dS, dX):
    """(X-S)/(S-L) and its 1-sigma error. Partials:
    dg/dX = 1/(S-L), dg/dS = -(X-L)/(S-L)^2, dg/dL = (X-S)/(S-L)^2."""
    num = X - S
    den = S - L
    g = num / den
    sg = np.sqrt((((X - S) / den ** 2) * dL) ** 2 +
                 ((-(X - L) / den ** 2) * dS) ** 2 +
                 ((1.0 / den) * dX) ** 2)
    return g, sg


# ───────────────────────────────────────────────────────────────────────────────
# H53a: do charm and bottom split like 1/phi^2?
# ───────────────────────────────────────────────────────────────────────────────

def flavor_splits():
    """Returns dict of {flavor: (split, sigma, target)} for light/charm/bottom."""
    out = {}
    out["light"] = ((SIG_L - LAM_L) / (XI_L - LAM_L), 0.0, INV_PHI2)
    out["charm"] = split(LAM_C, SIG_C, XI_C, dLAM_C, dSIG_C, dXI_C) + (INV_PHI2,)
    out["bottom"] = split(LAM_B, SIG_B, XI_B, dLAM_B, dSIG_B, dXI_B) + (INV_PHI2,)
    return out


def flavor_gaps():
    """Returns dict of {flavor: (gap, sigma, target=phi)} for light/charm/bottom."""
    out = {}
    out["light"] = ((XI_L - SIG_L) / (SIG_L - LAM_L), 0.0, PHI)
    out["charm"] = gap(LAM_C, SIG_C, XI_C, dLAM_C, dSIG_C, dXI_C) + (PHI,)
    out["bottom"] = gap(LAM_B, SIG_B, XI_B, dLAM_B, dSIG_B, dXI_B) + (PHI,)
    return out


def ordering(flavor):
    """Return 'inverted' if Sigma sits above Xi (breaks the Lambda<Sigma<Xi
    assumption used to assign the golden partition), else 'normal'."""
    L, S, X = {
        "light": (LAM_L, SIG_L, XI_L),
        "charm": (LAM_C, SIG_C, XI_C),
        "bottom": (LAM_B, SIG_B, XI_B),
    }[flavor]
    if S > X:
        return "INVERTED (Sigma > Xi)"
    return "normal (Lambda < Sigma < Xi)"


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    splits = flavor_splits()
    gaps = flavor_gaps()

    rows = []
    for fl in ("light", "charm", "bottom"):
        s, ss, st = splits[fl]
        g, gs, gt = gaps[fl]
        rows.append({
            "flavor": fl,
            "split (Sig-Lam)/(Xi-Lam)": round(s, 4),
            "sigma": round(ss, 4),
            "target 1/phi^2": round(st, 4),
            "split err %": round(abs(s / st - 1) * 100, 2),
            "gap (Xi-Sig)/(Sig-Lam)": round(g, 4),
            "target phi": round(gt, 4),
            "gap err %": round(abs(g / gt - 1) * 100, 2),
            "ordering": ordering(fl),
        })

    csv_path = os.path.join(OUT_DIR, "heavy_flavor_octet.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"Wrote {csv_path}")

    print("=== IST PHASE 53: Heavy-Flavor Octet - Does the Golden Partition Extend? ===")
    print("Phase 45 law:  (Sig-Lam)/(Xi-Lam) = 1/phi^2,  (Xi-Sig)/(Sig-Lam) = phi\n")
    print(f"{'flavor':<7}{'mass (Lam,Sig,Xi)':<28}{'split':<8}{'vs 1/phi^2':<12}{'gap':<8}")
    masses = {
        "light": (LAM_L, SIG_L, XI_L),
        "charm": (LAM_C, SIG_C, XI_C),
        "bottom": (LAM_B, SIG_B, XI_B),
    }
    for fl in ("light", "charm", "bottom"):
        L, S, X = masses[fl]
        s, ss, _ = splits[fl]
        g, gs, _ = gaps[fl]
        print(f"{fl:<7}{f'{L:.1f},{S:.1f},{X:.1f}':<28}{s:<8.4f}"
              f"{abs(s/INV_PHI2-1)*100:<8.2f}%  +/-{ss:.3f}"
              f"{'':2}{g:<7.3f}  {ordering(fl)}")

    print("\n  H53a-a: charm split   = %.4f  (target %.4f, %.1f%% off, %.0f sigma)"
          % (splits['charm'][0], INV_PHI2, abs(splits['charm'][0]/INV_PHI2-1)*100,
             abs(splits['charm'][0]-INV_PHI2)/splits['charm'][1]))
    c_gap = gaps['charm']
    print("  H53a-b: charm gap     = %.4f  (target %.4f, %.1f%% off, %.0f sigma)"
          % (c_gap[0], PHI, abs(c_gap[0]/PHI-1)*100, abs(c_gap[0]-PHI)/c_gap[1]))
    print("  H53b-a: bottom split  = %.4f  (target %.4f, %.1f%% off, %.0f sigma)"
          % (splits['bottom'][0], INV_PHI2, abs(splits['bottom'][0]/INV_PHI2-1)*100,
             abs(splits['bottom'][0]-INV_PHI2)/splits['bottom'][1]))
    b_gap = gaps['bottom']
    print("  H53b-b: bottom gap    = %.4f  (target %.4f, %.1f%% off, %.0f sigma)  [ordering INVERTED]"
          % (b_gap[0], PHI, abs(b_gap[0]/PHI-1)*100, abs(b_gap[0]-PHI)/b_gap[1]))

    # verdict: does any flavor obey the partition within the 0.2% Phase-45 bar?
    def obeys(fl):
        s, ss, _ = splits[fl]
        g, gs, _ = gaps[fl]
        return abs(s / INV_PHI2 - 1) < 0.002 and abs(g / PHI - 1) < 0.002

    for fl in ("light", "charm", "bottom"):
        print(f"  {fl:<7} obeys partition (0.2% bar)?  {obeys(fl)}")
    verdict = (obeys("light") and not obeys("charm") and not obeys("bottom"))
    print(f"\n  {'PASS: partition is LIGHT-OCTET SPECIFIC (heavy flavor excluded)'
           if verdict else 'UNEXPECTED: re-check'}")

    make_figure(splits)

    return rows


def make_figure(splits):
    fig, ax = plt.subplots(figsize=(8, 5))
    fls = ["light", "charm", "bottom"]
    vals = [splits[f][0] for f in fls]
    tgt = INV_PHI2
    colors = ["seagreen" if f == "light" else "crimson" for f in fls]
    ax.bar(fls, vals, color=colors)
    ax.axhline(tgt, color="k", ls="--", lw=1.5, label=f"1/phi^2 = {tgt:.5f}")
    for fl, v in zip(fls, vals):
        ax.text(fl, v, f"{v:.3f}", ha="center", va="bottom")
    ax.set_ylabel("(Sigma-Lambda)/(Xi-Lambda)")
    ax.set_title("Phase 53: golden partition is light-octet specific")
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "heavy_flavor_octet.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()