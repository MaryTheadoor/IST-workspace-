"""
================================================================================
IST PHASE 63 - The c1 Normalization Resolution (the IXPE Gate's Required
Derivation)
================================================================================
Purpose:
    Phase 62's gate verdict produced a required derivation: the physical
    normalization of the golden parity-even coupling c1 = alpha/phi^2
    (Phase 56), now constrained by the observed 2-4 keV vacuum-resonance (VR)
    dip in magnetar 1E 1547.0-5408 to near-QED strength. The 52.3x reading
    (same dimensionless slot as QED's alpha^2) is excluded. The template is
    the Phase 49 result: physical normalizations are fixed by the phase space
    that is actually paid, and the data select the counting.

    The physics. QED's one-loop coefficient c1_QED = alpha^2/(90 m_e^4)
    (Phase 62-verified kinematic structure). The framework's c1 = alpha/phi^2
    must acquire its 1/M^4 scale from the loop mass the substrate actually
    pays:
        c1_IST,phys = (alpha/phi^2)/(90 M_assoc^4)
        R = c1_IST/c1_QED = 52.33 * (m_e/M_assoc)^4
    The IXPE VR anchor (E_VR = 3 keV midpoint, band 2-4 keV, E_VR ~ 1/sqrt R)
    implies R in [0.5625, 2.25], i.e. M_assoc in [1.12, 1.59] MeV.

    The pre-registered candidate reading: the electron mass formula pays the
    associator suppression phi^2 (M_P/m_e = (12 pi^5/phi^2) alpha^-9) -- the
    same golden factor that scales the parity-even coupling -- so the vacuum
    loop pays it too: M_assoc = phi^2 m_e = 1.338 MeV. Predicted:
    R = 52.33/phi^8 = 1.114, E_VR = 2.84 keV, |Delta n| = (4/3)*1.114 =
    1.485x QED, decoupling ~ 147 R* -- all inside the IXPE anchors.

    Tracks:
      H63a - The normalization map. R(M) = 52.33 (m_e/M)^4 from c1 = alpha/phi^2
             and c1_QED = alpha^2/90m_e^4. The 52.3x reading (M = m_e) is the
             excluded branch (i) of the Phase 62 gate.
      H63b - The IXPE-implied band. E_VR = 3 keV / sqrt(R); observed band
             2-4 keV -> R in [0.5625, 2.25] -> M_assoc in [1.12, 1.59] MeV.
      H63c - The candidate-scale table: m_e (R=52.3, E_VR=0.41 keV - excluded);
             2 m_e (R=3.27, 1.66 keV - out); phi^2 m_e (R=1.114, 2.84 keV -
             IN); m_n - m_p = 1.293 MeV (R=1.28, 2.66 keV - IN); sqrt(m_e m_mu)
             = 7.35 MeV (R=1.2e-3 - out); m_pi (out).
      H63d - The framework rationale and the prediction. The associator
             suppression phi^2 paid by the electron mass formula is the same
             golden factor the vacuum loop pays -> M_assoc = phi^2 m_e ->
             c1_IST = 1.114x QED, E_VR = 2.84 keV, |dn| = 1.485x QED
             (sign-flipped), decoupling ~147 R*. Falsifiable the moment |dn|
             is extracted or the dip centroid is measured.
      H63e - The honest status. Empirically anchored, not yet first-
             principles: why the loop pays exactly phi^2 remains open. The
             52.3x 4WM enhancement (Phase 56 H56b) stays gated; the surviving
             parity-even 4WM magnitude becomes 1.114x QED; the c2/c1 = 0
             registration proceeds in the structural form.

Inputs:   none
Outputs:  code/outputs/phase63/normalization_map.csv
          code/outputs/phase63/candidate_scales.csv
          code/outputs/phase63/phi2_reading.csv
          code/outputs/phase63/c1_normalization.png

References:
    notes/IST_Phase_63_plan.md            (the plan, pre-registered)
    notes/phase49_internal_memo.md        (the normalization template)
    code/phase62_ixpe_vb_gate.py          (the gate: VR anchor, decoupling)
    code/phase56_four_wave_mixing.py      (c1 = alpha/phi^2 claim)
    Stewart et al. 2026, arXiv:2509.19446 (the IXPE data)
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from phase1_klein_laplacian import PHI
from phase62_ixpe_vb_gate import (C1_IST_RATIO, decoupling_radius,
                                  vr_energy)

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase63")

# ── physical constants ────────────────────────────────────────────────────────
ALPHA = 7.2973525693e-3
M_E = 0.51099895            # MeV (CODATA electron mass)
M_MU = 105.6583755          # MeV
M_NP_DIFF = 1.29333236      # MeV (m_n - m_p, CODATA 2018)
M_PI0 = 134.9768            # MeV (neutral pion)
E0_VR = 3.0                 # keV - VR dip midpoint anchor
E_BAND = (2.0, 4.0)         # keV - the observed band (Stewart et al.)

R_52 = C1_IST_RATIO         # 52.33 = 1/(alpha phi^2)
QED_DECOUPLING = 136.2      # R* (Phase 62, QED)
PHI8 = PHI ** 8


# ───────────────────────────────────────────────────────────────────────────────
# H63a - THE NORMALIZATION MAP
# ───────────────────────────────────────────────────────────────────────────────

def ratio_R(M_assoc_MeV):
    """R = c1_IST/c1_QED = 52.33 * (m_e/M_assoc)^4 for the golden coupling
    c1 = alpha/phi^2 normalized at the loop mass M_assoc (the QED kinematic
    structure 1/90 held fixed, Phase 62-verified)."""
    return R_52 * (M_E / M_assoc_MeV) ** 4


def vr_energy_keV(R):
    """VR (vacuum-resonance) energy for coupling ratio R:
    E_VR = 3 keV / sqrt(R) (Lai-Ho scaling, anchored at the observed dip)."""
    return E0_VR / np.sqrt(R)


# ───────────────────────────────────────────────────────────────────────────────
# H63b - THE IXPE-IMPLIED BAND
# ───────────────────────────────────────────────────────────────────────────────

def ixpe_implied_band():
    """Invert the observed 2-4 keV VR band into the allowed ranges for R and
    M_assoc. E_VR = 3/sqrt(R) in [2, 4] -> R in [(3/4)^2, (3/2)^2]; then
    M_assoc = m_e (52.33/R)^(1/4)."""
    R_lo = (E0_VR / E_BAND[1]) ** 2
    R_hi = (E0_VR / E_BAND[0]) ** 2
    M_lo = M_E * (R_52 / R_hi) ** 0.25
    M_hi = M_E * (R_52 / R_lo) ** 0.25
    return {"R_lo": R_lo, "R_hi": R_hi, "M_lo_MeV": M_lo, "M_hi_MeV": M_hi}


# ───────────────────────────────────────────────────────────────────────────────
# H63c - THE CANDIDATE-SCALE TABLE
# ───────────────────────────────────────────────────────────────────────────────

def candidate_scales():
    """The framework's candidate loop scales, scored against the IXPE band."""
    cands = [
        ("m_e", M_E, "electron mass (the QED loop)"),
        ("2 m_e", 2 * M_E, "pair-production threshold"),
        ("phi^2 m_e", PHI ** 2 * M_E, "golden-doubled electron (associator)"),
        ("m_n - m_p", M_NP_DIFF, "neutron-proton mass difference"),
        ("sqrt(m_e m_mu)", np.sqrt(M_E * M_MU), "geometric e-mu mean"),
        ("m_pi0", M_PI0, "pion scale"),
    ]
    rows = []
    for name, M, note in cands:
        R = ratio_R(M)
        evr = vr_energy_keV(R)
        in_band = E_BAND[0] < evr < E_BAND[1]
        rows.append({"candidate": name, "M_MeV": round(M, 4),
                     "R": round(R, 4), "E_VR_keV": round(evr, 3),
                     "in_2_4_keV_band": bool(in_band), "note": note})
    return rows


# ───────────────────────────────────────────────────────────────────────────────
# H63d - THE PHI^2 READING AND ITS PREDICTIONS
# ───────────────────────────────────────────────────────────────────────────────

def phi2_reading():
    """The pre-registered candidate: M_assoc = phi^2 m_e. The vacuum loop pays
    the same associator suppression phi^2 that the electron mass formula pays
    (M_P/m_e = (12 pi^5/phi^2) alpha^-9). Predicted observables vs the IXPE
    anchors."""
    M = PHI ** 2 * M_E
    R = ratio_R(M)                     # = 52.33/phi^8 = 1.114
    evr = vr_energy_keV(R)
    dn_ratio = (4.0 / 3.0) * R         # |dn| = (4/3) R x QED (c2 = 0, sign flipped)
    r_dec = QED_DECOUPLING * abs(dn_ratio) ** (1.0 / 5.0)
    return {
        "M_assoc_MeV": M,
        "R": R,
        "E_VR_keV": evr,
        "delta_n_ratio_vs_QED": dn_ratio,
        "decoupling_Rstar": r_dec,
        "E_VR_in_band": bool(E_BAND[0] < evr < E_BAND[1]),
        "decoupling_in_30_300": bool(30.0 < r_dec < 300.0),
        "R_close_to_unity": bool(0.5 < R < 2.0),
    }


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ---- H63a/b: the map and the band --------------------------------------
    band = ixpe_implied_band()
    print("=== H63a/b: the normalization map and the IXPE-implied band ===")
    print(f"  R(M) = {R_52:.3f} * (m_e/M)^4")
    print(f"  IXPE VR band 2-4 keV -> R in [{band['R_lo']:.4f}, "
          f"{band['R_hi']:.4f}], M_assoc in [{band['M_lo_MeV']:.3f}, "
          f"{band['M_hi_MeV']:.3f}] MeV")
    map_rows = []
    for M in np.logspace(np.log10(0.4), np.log10(30), 60):
        R = ratio_R(M)
        map_rows.append({"M_MeV": M, "R": R, "E_VR_keV": vr_energy_keV(R)})
    with open(os.path.join(OUT_DIR, "normalization_map.csv"),
              "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(map_rows[0].keys()))
        w.writeheader()
        w.writerows(map_rows)

    # ---- H63c: candidate scales ---------------------------------------------
    cand_rows = candidate_scales()
    print("\n=== H63c: candidate loop scales vs the 2-4 keV band ===")
    for r in cand_rows:
        print(f"  {r['candidate']:>14}: M = {r['M_MeV']:7.3f} MeV -> "
              f"R = {r['R']:8.4f}, E_VR = {r['E_VR_keV']:7.2f} keV "
              f"(in band: {r['in_2_4_keV_band']})  [{r['note']}]")
    with open(os.path.join(OUT_DIR, "candidate_scales.csv"),
              "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cand_rows[0].keys()))
        w.writeheader()
        w.writerows(cand_rows)

    # ---- H63d: the phi^2 reading --------------------------------------------
    ph = phi2_reading()
    print("\n=== H63d: the phi^2 m_e reading (pre-registered candidate) ===")
    print(f"  M_assoc = phi^2 m_e = {ph['M_assoc_MeV']:.4f} MeV")
    print(f"  R = c1_IST/c1_QED = {ph['R']:.4f} (= 52.33/phi^8)")
    print(f"  E_VR = {ph['E_VR_keV']:.2f} keV (band 2-4: "
          f"{ph['E_VR_in_band']})")
    print(f"  |dn| = {ph['delta_n_ratio_vs_QED']:.3f} x QED (sign-flipped)")
    print(f"  decoupling radius = {ph['decoupling_Rstar']:.1f} R* "
          f"(band 30-300: {ph['decoupling_in_30_300']})")
    ph_rows = [{"quantity": k, "value": v if not isinstance(v, bool) else v}
               for k, v in ph.items()]
    with open(os.path.join(OUT_DIR, "phi2_reading.csv"),
              "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["quantity", "value"])
        w.writeheader()
        w.writerows(ph_rows)

    # ---- H63e: honest status ------------------------------------------------
    print("\n=== H63e: the honest status ===")
    print("  * The IXPE band selects M_assoc ~ [1.1, 1.6] MeV.")
    print("  * phi^2 m_e = 1.338 MeV sits inside it, with R = 1.114 -- the")
    print("    same golden factor the electron mass formula already pays.")
    print("  * The 52.3x enhancement (Phase 56 H56b) stays GATED; the surviving")
    print("    parity-even magnitude claim becomes 1.114x QED.")
    print("  * OPEN: why the loop pays exactly phi^2 remains an outstanding")
    print("    derivation (associator amplitude, registry item).")

    make_figure(band, cand_rows, ph)
    print(f"\nWrote {OUT_DIR}")


def make_figure(band, cand_rows, ph):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A: R(M) with the IXPE band and candidates (H63a/b/c)
    ax = axes[0, 0]
    Ms = np.logspace(np.log10(0.4), np.log10(30), 200)
    Rs = [ratio_R(M) for M in Ms]
    ax.loglog(Ms, Rs, color="royalblue", label=r"$R(M) = 52.33\,(m_e/M)^4$")
    ax.axhspan(band["R_lo"], band["R_hi"], color="seagreen", alpha=0.2,
               label="IXPE band")
    for r in cand_rows:
        inb = r["in_2_4_keV_band"]
        ax.plot(r["M_MeV"], r["R"], "o", color="seagreen" if inb else "crimson",
                markersize=8)
        ax.annotate(r["candidate"], (r["M_MeV"], r["R"]),
                    textcoords="offset points", xytext=(0, 8), fontsize=7,
                    ha="center")
    ax.set_xlabel(r"$M_{\rm assoc}$ [MeV]")
    ax.set_ylabel(r"$R = c_{1,\rm IST}/c_{1,\rm QED}$")
    ax.set_title("A. The normalization map and the IXPE-implied band (H63a-c)")
    ax.legend(fontsize=8)

    # B: E_VR(R) with the observed band (H63b)
    ax = axes[0, 1]
    Rs = np.logspace(-2, 2, 200)
    ax.loglog(Rs, [vr_energy_keV(R) for R in Rs], color="goldenrod")
    ax.axhspan(2, 4, color="seagreen", alpha=0.2, label="observed 2-4 keV dip")
    for r in cand_rows:
        inb = r["in_2_4_keV_band"]
        ax.plot(r["R"], r["E_VR_keV"], "o", color="seagreen" if inb else "crimson",
                markersize=8)
    ax.set_xlabel("R")
    ax.set_ylabel("E_VR [keV]")
    ax.set_title("B. VR energy vs coupling ratio (H63b)")
    ax.legend(fontsize=8)

    # C: the phi^2 reading -- all observables inside their bands (H63d)
    ax = axes[1, 0]
    ax.axis("off")
    lines = [
        "PHI^2 READING: M_assoc = phi^2 m_e = 1.338 MeV",
        "",
        f"R = c1_IST/c1_QED = {ph['R']:.4f}  (52.33/phi^8)",
        f"E_VR = {ph['E_VR_keV']:.2f} keV   (band 2-4 keV: {ph['E_VR_in_band']})",
        f"|dn| = {ph['delta_n_ratio_vs_QED']:.3f} x QED (sign-flipped)",
        f"decoupling = {ph['decoupling_Rstar']:.0f} R*  (30-300: "
        f"{ph['decoupling_in_30_300']})",
        "",
        "all observables inside the IXPE anchors",
        "falsifiable when |dn| is extracted",
    ]
    ax.text(0.5, 0.5, "\n".join(lines), ha="center", va="center", fontsize=10,
            bbox=dict(boxstyle="round", fc="palegreen"))
    ax.set_title("C. The phi^2 m_e reading (H63d)")

    # D: honest status (H63e)
    ax = axes[1, 1]
    ax.axis("off")
    lines = [
        "HONEST STATUS (H63e)",
        "",
        "IXPE band -> M_assoc in [1.1, 1.6] MeV",
        "phi^2 m_e inside it: R = 1.114",
        "same golden factor the electron",
        "mass formula already pays",
        "",
        "52.3x enhancement: GATED (unchanged)",
        "surviving parity-even 4WM: 1.114x QED",
        "",
        "OPEN: why the loop pays exactly phi^2",
        "(associator amplitude derivation)",
    ]
    ax.text(0.5, 0.5, "\n".join(lines), ha="center", va="center", fontsize=10,
            bbox=dict(boxstyle="round", fc="lightgoldenrodyellow"))
    ax.set_title("D. The normalization verdict (H63e)")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "c1_normalization.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
