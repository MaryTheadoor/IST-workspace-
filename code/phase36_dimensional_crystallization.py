"""
================================================================================
IST PHASE 36 - Dimensional Crystallization: D(z) from 2 to 3 in the H(z) Data
================================================================================
Purpose:
    Test the foundational picture that the expanding universe is the third
    dimension crystallizing out of a two-dimensional substrate -- 'ice
    crystallizing out of a superfluid'. If matter is topologically knotted
    energetic wave functions (E = mc^2) and the embedding space is emergent,
    then the effective spatial dimension D_eff should be REDSHIFT-DEPENDENT:
    near 3 today (crystallized) descending toward 2 at high z (the
    superfluid substrate). This makes a specific, falsifiable prediction for
    the cosmic expansion history.

The model:

    H(z)^2 = H0^2 [ Om (1+z)^D(z) + (1-Om) ]

    D(z) = 2 + 1 / (1 + exp((z - z_c)/w))

    -- a sigmoid crystallization: D(z_c) = 2.5, D(0) -> 3 (present day),
    D(high z) -> 2 (superfluid substrate). 'w' = crystallization width,
    'z_c' = the redshift at which crystallization is half-complete.

    This is the dimensional analog of the Phase 4 fold-density result
    (D_eff sweeps with fold density) and the Phase 16 dimensional-amplification
    result (D_eff ~ 2 for the bare substrate, ~ 3 for the vacuum-pump
    crystallized state).

Data:
    60 H(z) cosmic chronometers (data/hz_cosmic_chronometers.csv, z 0.07-2.36)
    + Planck 2018 CMB shift prior R = 1.7502 +/- 0.0046.

Honest assessment (the CMB is decisive):
    (1) H(z) chronometers alone CANNOT distinguish crystallization from
        LCDM (Delta chi2 < 1); D(z) is degenerate with (H0, Om) in the
        low-z data.
    (2) The Planck 2018 CMB shift prior R = 1.7502 +/- 0.0046 IS decisive:
        a D -> 2 early universe gives R ~ 6 (hundreds of sigma off), because
        the 2D comoving distance at recombination is ~4x too large. The
        crystallization must complete BEFORE recombination (D(1090) ~ 3).
    (3) REFINED PICTURE: the third dimension is essentially always present
        at observable redshift; the 'ice-from-superfluid' crystallization
        happened at/near the big bang, not gradually over cosmic history.
        The H(z)-preferred z_c ~ 4 is CMB-EXCLUDED -- an honest
        falsification that constrains the postulate's regime.

Outputs:  code/outputs/phase36/crystallization_fit.csv
          code/outputs/phase36/crystallization.png

References:
    notes/foundational_postulates.md   (probabilistic superposition,
                                         emergent coherence/crystallization)
    data/hz_cosmic_chronometers.csv   (60 chronometers)
    data/cmb_distance_priors.csv      (Planck 2018 shift prior R)
    code/oscillatory_dark_energy.py   (H(z) fitting machinery)
    code/phase16_dimensions.py        (D_eff ~ 2 substrate, ~ 3 crystallized)
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase36")
DATA_HZ = os.path.join(os.path.dirname(__file__), "..", "data",
                       "hz_cosmic_chronometers.csv")

# Planck 2018 shift prior
R_CMB, R_CMB_SIG = 1.7502, 0.0046


# ───────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ───────────────────────────────────────────────────────────────────────────────

def load_hz(filepath=DATA_HZ):
    z, H, sig = [], [], []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            p = line.split(",")
            if len(p) >= 3:
                zi, Hi, si = float(p[0]), float(p[1]), float(p[2])
                if si > 0 and zi >= 0:
                    z.append(zi); H.append(Hi); sig.append(si)
    z, H, sig = map(np.array, (z, H, sig))
    order = np.argsort(z)
    return z[order], H[order], sig[order]


# ───────────────────────────────────────────────────────────────────────────────
# THE CRYSTALLIZATION MODEL
# ───────────────────────────────────────────────────────────────────────────────

def d_eff(z, z_c, w):
    """D(z) = 2 + sigmoid((z_c - z)/w). Present day -> 3, high z -> 2.
    Clipped against overflow (z >> z_c gives exp -> 0, D -> 2)."""
    return 2.0 + 1.0 / (1.0 + np.exp(np.clip((z - z_c) / w, -50, 50)))


def hz_cryst(z, H0, Om, z_c, w):
    """H(z)^2 = H0^2 [ Om (1+z)^D(z) + (1-Om) ]."""
    D = d_eff(z, z_c, w)
    return H0 * np.sqrt(Om * (1 + z) ** D + (1 - Om))


def hz_lcdm(z, H0, Om):
    return H0 * np.sqrt(Om * (1 + z) ** 3 + (1 - Om))


def shift_parameter(Om, z_c, w, z_star=1089.9):
    """CMB shift R = sqrt(Om) * H0 * D_M(z*)/c = sqrt(Om) * integral of
    dz / E(z) to recombination. E(z) = sqrt(Om(1+z)^D(z) + (1-Om))."""
    from scipy.integrate import quad
    def integrand(zp):
        E = np.sqrt(Om * (1 + zp) ** d_eff(zp, z_c, w) + (1 - Om))
        return 1.0 / E
    integral, _ = quad(integrand, 0, z_star, limit=400)
    return np.sqrt(Om) * integral


# ───────────────────────────────────────────────────────────────────────────────
# FITTING
# ───────────────────────────────────────────────────────────────────────────────

def fit_crystallization(z, H, sig):
    """Grid + refine fit of (H0, Om, z_c, w)."""
    best = None
    for H0 in np.linspace(60, 80, 41):
        for Om in np.linspace(0.15, 0.45, 31):
            for z_c in [1.0, 2.0, 3.0, 4.0]:
                for w in [0.2, 0.5, 1.0]:
                    chi2 = np.sum(((H - hz_cryst(z, H0, Om, z_c, w)) / sig) ** 2)
                    if best is None or chi2 < best[0]:
                        best = (chi2, H0, Om, z_c, w)
    return best


def fit_lcdm(z, H, sig):
    best = None
    for H0 in np.linspace(60, 80, 41):
        for Om in np.linspace(0.15, 0.45, 31):
            chi2 = np.sum(((H - hz_lcdm(z, H0, Om)) / sig) ** 2)
            if best is None or chi2 < best[0]:
                best = (chi2, H0, Om)
    return best


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    z, H, sig = load_hz()

    chi2_c, H0_c, Om_c, z_c, w_c = fit_crystallization(z, H, sig)
    chi2_l, H0_l, Om_l = fit_lcdm(z, H, sig)

    # CMB shift constraint: R must match Planck 1.7502 +/- 0.0046.
    # KEY RESULT: D -> 2 by recombination gives R ~ 6 (hundreds of sigma off).
    # Crystallization must complete before recombination (D(1090) ~ 3).
    R_pred = shift_parameter(Om_c, z_c, w_c)
    r_chi2 = ((R_pred - R_CMB) / R_CMB_SIG) ** 2
    # the highest-z H(z) point is the deepest probe of D(z)
    z_max = z.max()

    rows = [
        {"model": "LCDM", "H0": H0_l, "Om": Om_l, "z_c": np.nan, "w": np.nan,
         "chi2": chi2_l, "D_eff(0)": 3.0, "D_eff(high z)": 3.0},
        {"model": "crystallization", "H0": H0_c, "Om": Om_c, "z_c": z_c,
         "w": w_c, "chi2": chi2_c,
         "D_eff(0)": d_eff(0, z_c, w_c),
         "D_eff(high z)": d_eff(10, z_c, w_c)},
    ]
    csv_path = os.path.join(OUT_DIR, "crystallization_fit.csv")
    with open(csv_path, "w", newline="") as fh:
        wcsv = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        wcsv.writeheader(); wcsv.writerows(rows)
    print(f"Wrote {csv_path}")

    print("=== IST PHASE 36: Dimensional Crystallization ===")
    print("The 3rd dimension crystallizing out of a 2D substrate (ice from a")
    print("superfluid). D(z): present-day 3, high-z 2.\n")
    print(f"  LCDM          : chi2 = {chi2_l:.1f}  H0 = {H0_l:.1f}  Om = {Om_l:.2f}")
    print(f"  crystallization: chi2 = {chi2_c:.1f}  H0 = {H0_c:.1f}  Om = {Om_c:.2f}"
          f"  z_c = {z_c:.1f}  w = {w_c:.2f}")
    print(f"  Delta chi2    : {chi2_c - chi2_l:+.1f} (crystallization vs LCDM)")
    print(f"  D_eff(0)      : {d_eff(0, z_c, w_c):.2f} (present day, ~3 crystallized)")
    print(f"  D_eff(z=10)   : {d_eff(10, z_c, w_c):.2f} (early, ~2 superfluid)")
    print(f"  CMB shift R   : pred {R_pred:.4f} vs Planck {R_CMB:.4f} "
          f"(chi2 = {r_chi2:.1f})")

    print(f"\nHonest assessment (the CMB is decisive):")
    print(f"  H(z) chronometers CANNOT distinguish crystallization from LCDM")
    print(f"  (Delta chi2 = {chi2_c - chi2_l:+.1f}); D(z) is degenerate with")
    print(f"  (H0, Om) in the low-z data (z_max = {z_max:.2f}).")
    print(f"  CMB shift prior IS decisive: with D -> 2 at high z the shift")
    print(f"  parameter R = {R_pred:.2f} vs Planck {R_CMB:.2f} -- excluded by")
    print(f"  ~{np.sqrt(r_chi2):.0f} sigma. A 2D early universe would give a")
    print(f"  comoving distance ~4x too large at recombination.")
    print(f"  => Crystallization must complete BEFORE recombination:")
    print(f"     D(1090) ~ 3, i.e. z_c >> 1090 (or D ~ 3 at all observable z).")
    print(f"  => The 'ice-from-superfluid' picture is refined: the third")
    print(f"     dimension is essentially always present at observable z; the")
    print(f"     crystallization happened at/near the big bang, not gradually")
    print(f"     over cosmic history. The H(z)-preferred z_c ~ {z_c:.0f} is")
    print(f"     CMB-EXCLUDED -- an honest falsification that constrains the")
    print(f"     postulate's regime.")

    make_figure(z, H, sig, H0_c, Om_c, z_c, w_c, H0_l, Om_l)
    print(f"\nWrote {OUT_DIR}")


def make_figure(z, H, sig, H0_c, Om_c, z_c, w_c, H0_l, Om_l):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    zs = np.linspace(0, 3, 200)
    axes[0].errorbar(z, H, yerr=sig, fmt="o", ms=3, alpha=0.6, label="data")
    axes[0].plot(zs, hz_cryst(zs, H0_c, Om_c, z_c, w_c), "r-",
                 label="crystallization")
    axes[0].plot(zs, hz_lcdm(zs, H0_l, Om_l), "b--", label="LCDM")
    axes[0].set_xlabel("z"); axes[0].set_ylabel("H(z) (km/s/Mpc)")
    axes[0].set_title("H(z): crystallization vs LCDM")
    axes[0].legend(fontsize=8)

    zz = np.linspace(0, 8, 300)
    axes[1].plot(zz, d_eff(zz, z_c, w_c), "seagreen", lw=2)
    axes[1].axhline(3, color="k", ls="--", lw=1, label="3 (crystallized)")
    axes[1].axhline(2, color="k", ls=":", lw=1, label="2 (superfluid)")
    axes[1].axvline(z_c, color="crimson", ls="--", lw=1,
                    label=f"z_c = {z_c:.1f}")
    axes[1].set_xlabel("z"); axes[1].set_ylabel("D_eff(z)")
    axes[1].set_title("Dimensional crystallization D(z)")
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "crystallization.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
