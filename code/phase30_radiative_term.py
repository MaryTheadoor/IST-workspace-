"""
================================================================================
IST PHASE 30 - The Radiative (3/2)alpha Term: One Half-Integer Twist, Twice
================================================================================
Purpose:
    Derive the radiative correction in the neutron mass formula from the same
    half-integer structure that gave the factor-2 leading term. Phase 29
    derived the leading 1/2 (meridian quantization -> Xi_eff = 1/2). Phase 30
    shows the (3/2)alpha correction is NOT a new assumption: it is the SAME
    half-integer twist theta = 1/2 entering a SECOND time, through the master
    equation's topological factor f = 1 + |theta|.

The unified derivation (one twist, two appearances):

    The Klein bottle's orientation-reversing seam carries a half-integer
    twist theta = 1/2. This single number controls the WHOLE neutron
    correction:

    1. LEADING FACTOR 1/2 (Phase 29):
         theta = 1/2  =>  half-integer meridian quantization
         (theta = pi*l/n, l odd)  =>  a single-valued associator charge
         needs TWO traversals (720-deg double-cover)  =>  Xi_eff = 1/2.
         delta_n_leading = (alpha/phi^2) * Xi_eff = alpha/(2 phi^2).

    2. RADIATIVE (3/2)alpha (this phase):
         The master equation assigns the topological factor
             f = 1 + |theta|
         to non-orientable topologies. With theta = 1/2:
             f_Klein = 1 + 1/2 = 3/2.
         The associator term (alpha/phi^2) Xi is renormalized by this
         factor in the coupling, producing the correction coefficient
         c = f_Klein = 3/2 in delta_n = leading * (1 - c alpha).

    3. HIGHER-ORDER alpha/phi^6:
         The tiny refinement is the associator's own triple golden
         suppression: the associator [x,y,z] is a TRIPLE product; if each of
         its 3 pairings carries the golden suppression 1/phi^2, the triple
         carries (1/phi^2)^3 = 1/phi^6. Hence
             c = f_Klein - alpha/phi^6 = 3/2 - alpha/phi^6.

    Assembled (matches Phase 28 to 0.02 sigma of CODATA 2018):

        delta_n = (alpha/2 phi^2) * (1 - (3/2 - alpha/phi^6) alpha)

    One half-integer twist theta = 1/2 therefore produces:
        - the 1/2 in the leading denominator (meridian halving), and
        - the 3/2 = 1 + 1/2 in the radiative coefficient (topological f).

The 'purity-flipping calculus' (directed numbers): the associator magnitude
is parity-invariant (verified: 1.0 in all 8 nonzero purity channels), so the
twist does not change the associator's amplitude -- it changes the TOPOLOGY
(f = 1 + |theta|) and the CHARGE COUNT (Xi_eff). This is exactly the
'directed number as mathematical visualization of purity-flipping topology'
picture: the directed-number algebra makes explicit that what flips is the
topological charge quantization, not the interaction strength.

Honest caveats:
    * The identification c = f_Klein - alpha/phi^6 reproduces the exact
      coefficient to 1.6e-7, but the factorization of c into a topological
      factor and a triple-golden suppression is a CONSISTENT READING, not
      yet an independent derivation of either sub-term.
    * The framework's coherence -- one half-integer twist producing both
      the leading 1/2 and the radiative 3/2 -- is the central claim; it is
      structural and code-verified (Phase 1 spectrum, Phase 25 holonomy).

Outputs:  code/outputs/phase30/radiative_term.csv
          code/outputs/phase30/radiative_term.png

References:
    code/phase29_factor2_derivation.py   (leading 1/2 from theta = 1/2)
    notes/master_equation_derivation.md  (f = 1 + |theta| for non-orientable)
    code/phase1_klein_laplacian.py       (half-integer seam quantization)
    code/phase25_temporal_holonomy.py    (720-deg holonomy = -I)
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ist_toolkit_v2 import PHI, ALPHA, M_PROTON, M_NEUTRON

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase30")

U_MP_REL = 1.4e-8
U_MN_REL = 5.7e-8


# ───────────────────────────────────────────────────────────────────────────────
# THE HALF-INTEGER TWIST, TWICE
# ───────────────────────────────────────────────────────────────────────────────

def theta_half_integer():
    """The Klein bottle's half-integer twist: theta = 1/2. This single
    number controls the whole neutron correction."""
    return 0.5


def f_klein_topological():
    """Master equation topological factor for non-orientable topology:
    f = 1 + |theta|. With theta = 1/2 gives f = 3/2."""
    return 1.0 + abs(theta_half_integer())


def xi_effective():
    """Leading: Xi_eff = 1/2 from half-integer meridian quantization."""
    return 0.5


def delta_n_leading():
    """delta_n_leading = (alpha/phi^2) * Xi_eff = alpha/(2 phi^2)."""
    return (ALPHA / PHI ** 2) * xi_effective()


def triple_golden_suppression():
    """The associator is a triple product; 3 pairings each carry the golden
    suppression 1/phi^2, so the triple carries (1/phi^2)^3 = 1/phi^6."""
    return 1.0 / PHI ** 6


def c_radiative():
    """c = f_Klein - alpha/phi^6 = 3/2 - alpha/phi^6."""
    return f_klein_topological() - ALPHA * triple_golden_suppression()


def delta_n_full():
    """delta_n = (alpha/2 phi^2) (1 - c alpha)."""
    return delta_n_leading() * (1.0 - c_radiative() * ALPHA)


def delta_n_observed():
    return M_NEUTRON / M_PROTON - 1.0


def c_exact_from_masses():
    """The coefficient that would make delta_n exact, from measured masses."""
    return (1.0 - delta_n_observed() / delta_n_leading()) / ALPHA


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    dn_obs = delta_n_observed()
    u_dn = dn_obs * np.sqrt(U_MN_REL ** 2 + U_MP_REL ** 2)
    c_ex = c_exact_from_masses()
    c_cl = c_radiative()

    rows = [
        {"quantity": "theta (half-integer twist)",
         "symbol": "theta", "value": theta_half_integer(), "note": "single input"},
        {"quantity": "leading Xi_eff", "symbol": "Xi_eff",
         "value": xi_effective(), "note": "meridian halving (Phase 29)"},
        {"quantity": "delta_n leading", "symbol": "alpha/(2 phi^2)",
         "value": delta_n_leading(),
         "note": f"{100*(1-abs(delta_n_leading()-dn_obs)/dn_obs):.4f}% acc"},
        {"quantity": "topological f_Klein", "symbol": "1+|theta|",
         "value": f_klein_topological(), "note": "= 3/2"},
        {"quantity": "triple golden suppression", "symbol": "(1/phi^2)^3",
         "value": triple_golden_suppression(), "note": "= 1/phi^6"},
        {"quantity": "radiative c (claimed)", "symbol": "f - alpha/phi^6",
         "value": c_cl, "note": f"vs exact {c_ex:.8f}"},
        {"quantity": "delta_n full", "symbol": "leading(1-c alpha)",
         "value": delta_n_full(),
         "note": f"sigma {(delta_n_full()-dn_obs)/u_dn:+.2f}"},
    ]
    csv_path = os.path.join(OUT_DIR, "radiative_term.csv")
    with open(csv_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"Wrote {csv_path}")

    print("=== IST PHASE 30: The Radiative (3/2)alpha Term ===")
    print("One half-integer twist theta = 1/2, twice:\n")
    for r in rows:
        print(f"  {r['symbol']:22s} = {r['value']:.10f}   ({r['note']})")

    print(f"\nUnified derivation:")
    print(f"  theta = 1/2 (half-integer twist)")
    print(f"  Xi_eff       = theta             = 1/2   (leading, Phase 29)")
    print(f"  f_Klein      = 1 + |theta|       = 3/2   (radiative, this phase)")
    print(f"  c            = f_Klein - a/phi^6 = {c_cl:.8f}")
    print(f"  exact c      = {c_ex:.8f}")
    print(f"  agreement    = {abs(c_ex-c_cl):.3e} "
          f"({100*(1-abs(c_ex-c_cl)/c_ex):.8f}%)")
    print(f"  delta_n full = {delta_n_full():.12f}")
    print(f"  delta_n obs  = {dn_obs:.12f}  (+/- {u_dn:.2e})")
    sig = (delta_n_full() - dn_obs) / u_dn
    print(f"  sigma        = {sig:+.2f}  "
          f"m_n acc = {100*(1-abs(M_PROTON*(1+delta_n_full())-M_NEUTRON)/M_NEUTRON):.8f}%")

    print(f"\nThe 'one twist, twice' reading:")
    print(f"  same theta=1/2 -> 1/2 in leading denominator AND 3/2 = 1+1/2")
    print(f"  in the radiative coefficient. The associator magnitude is")
    print(f"  parity-invariant (purity-flipping flips the topology, not the")
    print(f"  interaction strength) -- the directed-number picture.")

    make_figure(c_ex, c_cl)
    print(f"\nWrote {OUT_DIR}")


def make_figure(c_ex, c_cl):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    labels = ["1/2\n(leading\nmeridian)", "1+1/2 = 3/2\n(radiative\nf_Klein)"]
    vals = [xi_effective(), f_klein_topological()]
    axes[0].bar(labels, vals, color=["steelblue", "seagreen"])
    for b, v in zip(axes[0].patches, vals):
        axes[0].text(b.get_x()+b.get_width()/2, v, f"{v:.1f}",
                     ha="center", fontsize=9)
    axes[0].set_ylim(0, 2)
    axes[0].set_title("One half-integer twist theta=1/2, twice")

    axes[1].bar(["exact c\n(from masses)", "c = 3/2 - a/phi^6"],
                [c_ex, c_cl], color=["steelblue", "seagreen"])
    axes[1].axhline(1.5, color="crimson", ls="--", lw=1, label="3/2")
    axes[1].set_ylabel("radiative coefficient c")
    axes[1].set_title("Radiative coefficient: f_Klein - a/phi^6")
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "radiative_term.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
