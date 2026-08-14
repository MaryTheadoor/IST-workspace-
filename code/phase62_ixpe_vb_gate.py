"""
================================================================================
IST PHASE 62 - The IXPE Vacuum-Birefringence Gate (Stewart et al. 2026)
================================================================================
Purpose:
    Stewart et al. 2026 (arXiv 2509.19446, Nature; IXPE+NICER+Parkes) report the
    strongest evidence yet for QED vacuum birefringence (VB) in magnetar
    1E 1547.0-5408 (B ~ 2.2e14 G ~ 5 B_cr): phase-averaged PD 65+/-8% at 2 keV
    (peaking 82+/-15%), a PD depression across 2-4 keV attributed to mode
    conversion at the QED vacuum resonance (VR), RVM-consistent PA swings, and
    radiative-transfer fits where VB-on crushes VB-off (Q/I chi2/dof 19.0/4 vs
    106.8/4). The absolute Delta n is NOT extracted as a clean number (the
    authors say so: model-dependent, single source).

    This is the flagship prediction's first empirical neighbor: vacuum
    birefringence and four-wave mixing are the SAME two Heisenberg-Euler
    coefficients c1, c2 of  L_quartic = c1*(F^2)^2 + c2*(F.F~)^2, and Phase 56
    predicts c2/c1 = 0 (QED: 7/4). This phase computes the gate:
    what does the achiral vacuum (c2 = 0) predict for the magnetar VB
    observables, and what do the IXPE data say about it?

    The core physics (derived here by exact quadratic expansion of the two
    invariants around a pure-B background, verified against the canonical
    literature):

        (F^2)^2    ->  c1 [ 8 B^2 (B_f^2 - E_f^2) + 16 (B.B_f)^2 ]
        (F.F~)^2   ->  16 c2 (E_f.B)^2

    where (E_f, B_f) are the probe field's electric/magnetic vectors. On-shell
    B_f^2 = E_f^2 and the two photon eigenmodes decouple cleanly by invariant:

        n(E || B) - 1 = 16 * c2 * B^2 * sin^2(theta_B)
        n(E _|_ B) - 1 = 16 * c1 * B^2 * sin^2(theta_B)

    QED (c1 = alpha^2/90 m^4, c2 = (7/4) c1) reproduces the canonical
    (14/45, 8/45)(alpha^2/m^4) B^2 sin^2(theta) with ratio 7/4 = c2/c1.
    Consequence: c2 = 0 does NOT kill VB -- it makes the E||B mode
    non-refractive (index EXACTLY 1, at all angles) while the E_|_B mode
    keeps the c1 shift. Delta n = n_|| - n_|_ = (alpha B^2/45 pi)[(7/2) c2r
    - 2 c1r] in B_cr units. At perpendicular incidence E||B is the O-mode
    (surface-dominant in the magnetar), E_|_B the X-mode.

    Two-branch normalization question: Phase 56 claims c1_IST = alpha/phi^2
    (vs QED c1 = alpha^2 in the same dimensionless slot; "IST/QED coupling
    ~ 52.3"), but the PHYSICAL c1 carries the 1/(90 m^4) kinematic structure.
    Branch (i): c1_IST = 52.3 * c1_QED physically -> |Delta n| ~ 70x QED.
    Branch (ii): c1_IST ~ c1_QED (only c2 = 0) -> |Delta n| = (4/3) QED.

    Tracks:
      H62a - The mode algebra (verification). Exact quadratic expansion ->
             eigenmode decoupling -> (i) n(E||B) proportional to c2 ONLY and
             n(E_|_B) to c1 ONLY (exact at all theta); (ii) QED reproduces the
             canonical (14/45, 8/45)(alpha^2/m^4) B^2 sin^2(theta); (iii)
             c2 = 0 -> n(E||B) = 1 EXACTLY.
      H62b - The magnetar observable. For 1E 1547.0-5408 (B_surf ~ 2.2e14 G,
             B/B_cr ~ 5, R* = 12 km, E = 2-4 keV, dipole field): accumulated
             VB phase + mode-decoupling radius (QED must land in the paper's
             30-300 R* statement); the VR energy (E_VR ~ 1/sqrt(vacuum
             coefficient), Lai-Ho scaling) anchored at the observed 2-4 keV
             dip; for QED and for IST branches (i) and (ii).
      H62c - The structural discriminator survives. c2 = 0 -> n(E||B) = 1 at
             all angles: no E||B-mode vacuum resonance, no E||B-mode locking.
             Normalization-independent; untested by current data (the paper
             does not extract Delta n; single source).
      H62d - The registration gate. (1) c2/c1 = 0 registerable in the
             structural (mode-resolved) form; (2) the 52.3x 4WM enhancement
             (Phase 56 H56b) GATED OFF pending the physical c1 normalization,
             because the 2-4 keV dip constrains c1 to near-QED strength;
             (3) registry records the constraint, the branch table, and the
             derivation gap.

Inputs:   none
Outputs:  code/outputs/phase62/mode_algebra.csv
          code/outputs/phase62/magnetar_observables.csv
          code/outputs/phase62/registration_gate.csv
          code/outputs/phase62/ixpe_vb_gate.png

References:
    notes/IST_Phase_62_plan.md            (the plan, pre-registered)
    Stewart et al. 2026, arXiv:2509.19446 (IXPE magnetar VB)
    code/phase56_four_wave_mixing.py      (c1 = alpha/phi^2, c2/c1 = 0 claim)
    Canonical: n_|| - 1 = (14/45)(alpha^2/m^4) B^2 sin^2(theta);
               n_|_ - 1 = (8/45)(alpha^2/m^4) B^2 sin^2(theta)
               (Tsai & Erber 1975; arXiv:0711.1337; hal-03294255)
    Lai & Ho 2003 (vacuum resonance / mode conversion)
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase62")

# ── physical constants ────────────────────────────────────────────────────────
ALPHA = 7.2973525693e-3
B_CR = 4.414e13              # G  (QED critical field)
MAGNETAR_B = 2.2e14          # G  (1E 1547.0-5408 equatorial surface field)
R_STAR = 12e3                # m
E_BAND = (2.0, 4.0)          # keV - the observed VR dip band
HBC = 1.97327e-7             # eV*m  (hbar*c)
QED_C2_C1 = 7.0 / 4.0
C1_QED = ALPHA ** 2 / 90.0   # alpha^2/90 m^4 (natural units, m = 1)
C1_IST_RATIO = 1.0 / (ALPHA * PHI ** 2)   # Phase 56: c1_ist/c1_qed = 1/(a phi^2)

# 3d Levi-Civita (contravariant, eps[0,1,2] = +1)
LEVI3 = np.zeros((3, 3, 3))
LEVI3[0, 1, 2] = LEVI3[1, 2, 0] = LEVI3[2, 0, 1] = 1.0
LEVI3[0, 2, 1] = LEVI3[2, 1, 0] = LEVI3[1, 0, 2] = -1.0


# ───────────────────────────────────────────────────────────────────────────────
# H62a - THE MODE ALGEBRA: EXACT QUADRATIC EXPANSION AROUND A PURE-B BACKGROUND
# ───────────────────────────────────────────────────────────────────────────────

def probe_fields(kvec, evec):
    """Probe field strength f^mu,nu = i(k^mu e^nu - k^nu e^mu) of a plane-wave
    photon (kvec = (omega, kx, ky, kz) contravariant, evec polarization
    contravariant, e.k = 0). Returns the probe electric/magnetic 3-vectors
    E_f^i = f^0i and B_f^i = (1/2) eps^{ijk} f^jk."""
    f = 1j * (np.outer(kvec, evec) - np.outer(evec, kvec))
    E_f = f[0, 1:4]
    B_f = 0.5 * np.einsum("ijk,jk->i", LEVI3, f[1:4, 1:4])
    return E_f, B_f


def quadratic_lagrangian(c1, c2, B_mag, theta, kvec, evec):
    """Quadratic-in-probe part of L = c1 (F^2)^2 + c2 (F.F~)^2 around a pure
    magnetic background B = B_mag z_hat (k at angle theta to z). Exact:
        (F^2)^2    ->  c1 [ 8 B^2 (B_f^2 - E_f^2) + 16 (B.B_f)^2 ]
        (F.F~)^2   ->  16 c2 (E_f.B)^2
    (terms beyond quadratic in the probe do not affect linear dispersion)."""
    E_f, B_f = probe_fields(kvec, evec)
    B_vec = np.array([0.0, 0.0, B_mag])
    Bf2 = B_f @ B_f
    Ef2 = E_f @ E_f
    BdotBf = B_vec @ B_f
    EdotB = E_f @ B_vec
    return c1 * (8.0 * B_mag ** 2 * (Bf2 - Ef2) + 16.0 * BdotBf ** 2) \
        + 16.0 * c2 * EdotB ** 2


def mode_index_shifts(c1, c2, B_mag, theta):
    """The two photon eigenmode index shifts n - 1, derived from the exact
    quadratic expansion. The mode frequencies solve the perturbed dispersion;
    with the free dispersion and B_f^2 = E_f^2 on-shell (verified internally),
    the shift is  n - 1 = - L_quad / omega^2  per unit polarization (omega = 1,
    e^2 = 1). Polarizations:
        e_par  = (0, cos th, 0, -sin th)  - E in the k-B plane (E||B at 90 deg)
        e_perp = (0, 0, 1, 0)            - E _|_ B at all theta
    Returns (n_par - 1, n_perp - 1)."""
    kvec = np.array([1.0, np.sin(theta), 0.0, np.cos(theta)])
    e_par = np.array([0.0, np.cos(theta), 0.0, -np.sin(theta)])
    e_perp = np.array([0.0, 0.0, 1.0, 0.0])
    shifts = []
    for evec in (e_par, e_perp):
        Lq = quadratic_lagrangian(c1, c2, B_mag, theta, kvec, evec)
        shifts.append(-np.real(Lq) / 1.0)       # omega = 1, e^2 = 1
    return shifts[0], shifts[1]


def on_shell_check(B_mag, theta):
    """Internal consistency check: the free probe invariants vanish on-shell
    (B_f^2 - E_f^2 = 0 for a plane wave with omega = |k|)."""
    kvec = np.array([1.0, np.sin(theta), 0.0, np.cos(theta)])
    e = np.array([0.0, 0.0, 1.0, 0.0])
    E_f, B_f = probe_fields(kvec, e)
    return float(np.real((B_f @ B_f) - (E_f @ E_f)))


def qed_canonical(B_mag, theta):
    """Canonical QED one-loop weak-field indices (verification target):
    n_par - 1 = (14/45)(alpha^2/m^4) B^2 sin^2(theta),
    n_perp - 1 = (8/45)(alpha^2/m^4) B^2 sin^2(theta)."""
    s2 = np.sin(theta) ** 2
    return ((14.0 / 45.0) * ALPHA ** 2 * B_mag ** 2 * s2,
            (8.0 / 45.0) * ALPHA ** 2 * B_mag ** 2 * s2)


def verify_mode_algebra(B_mag=1.0, angles=(0.2, 0.6, 1.0, 1.3)):
    """Compare the derived index shifts against the canonical QED numbers
    (c1, c2 = QED values), and check the decoupling ratio 7/4 = c2/c1."""
    rows = []
    for th in angles:
        n_par, n_perp = mode_index_shifts(C1_QED, QED_C2_C1 * C1_QED,
                                          B_mag, th)
        c_par, c_perp = qed_canonical(B_mag, th)
        rows.append({
            "theta": round(th, 4),
            "derived_npar": n_par,
            "canonical_npar": c_par,
            "derived_nperp": n_perp,
            "canonical_nperp": c_perp,
            "ratio_derived": round(n_par / n_perp, 4),
            "ratio_canonical": round(c_par / c_perp, 4),
            "onshell_invariant": on_shell_check(B_mag, th),
        })
    return rows


def achiral_mode_algebra(c1_ratio=1.0, B_mag=1.0, angles=(0.2, 0.6, 1.0, 1.3)):
    """The IST (c2 = 0) prediction: n_par = 1 EXACTLY at all angles, n_perp - 1
    = 16 c1_ist B^2 sin^2(theta)."""
    c1 = C1_QED * c1_ratio
    rows = []
    for th in angles:
        n_par, n_perp = mode_index_shifts(c1, 0.0, B_mag, th)
        rows.append({
            "theta": round(th, 4),
            "n_par_minus_1": n_par,
            "n_perp_minus_1": n_perp,
            "n_par_is_one": bool(abs(n_par) < 1e-15),
        })
    return rows


# ───────────────────────────────────────────────────────────────────────────────
# H62b - THE MAGNETAR OBSERVABLE
# ───────────────────────────────────────────────────────────────────────────────

def delta_n_surface(c1_ratio, c2_ratio):
    """Delta n = n_par - n_perp at the magnetar surface (theta = 90 deg),
    in B_cr units:
        Delta n = (alpha b^2 / 45 pi) [ (7/2) c2_ratio - 2 c1_ratio ]."""
    b = MAGNETAR_B / B_CR
    return (ALPHA * b ** 2 / (45.0 * np.pi)) * (3.5 * c2_ratio - 2.0 * c1_ratio)


def accumulated_phase(c1_ratio, c2_ratio, E_keV=2.0):
    """Total radial accumulated VB phase for the magnetar dipole
    B(r) = B_surf (R*/r)^3 at theta = 90 deg:
        dPhi = omega * Int_R*^inf Delta n_surf (R*/r)^6 dr
             = omega * Delta n_surf * R* / 5.
    Returns dPhi in radians."""
    omega = E_keV * 1e3 / HBC
    return omega * delta_n_surface(c1_ratio, c2_ratio) * R_STAR / 5.0


def decoupling_radius(c1_ratio, c2_ratio, E_keV=2.0):
    """Radius (in R*) where the residual accumulated phase drops to 1 rad:
    dPhi(r) = dPhi_total (R*/r)^5 = 1  ->  r/R* = dPhi_total^(1/5)."""
    dphi = accumulated_phase(c1_ratio, c2_ratio, E_keV)
    return abs(dphi) ** (1.0 / 5.0)


def vr_energy(c1_ratio, E0_keV=3.0):
    """Vacuum-resonance (mode-conversion) energy for coupling scale c1_ratio.
    Lai-Ho scaling: E_VR ~ 1/sqrt(vacuum coefficient) for the E_|_B mode
    (the surviving resonance channel; the E||B channel vanishes for c2 = 0).
    Anchored at E0 (the observed 2-4 keV dip midpoint)."""
    return E0_keV / np.sqrt(c1_ratio)


# ───────────────────────────────────────────────────────────────────────────────
# H62c/H62d - THE GATE
# ───────────────────────────────────────────────────────────────────────────────

def registration_gate():
    """Verdict table: QED vs IST branch (ii) (c1 ~ QED, c2 = 0) vs IST branch
    (i) (c1 = 52.3x QED, c2 = 0), for the magnetar observables, against the
    IXPE anchors (decoupling 30-300 R*; VR dip 2-4 keV)."""
    rows = []
    for name, c1r, c2r in [("QED", 1.0, 1.0),
                           ("IST branch (ii): c2=0, c1~QED", 1.0, 0.0),
                           ("IST branch (i): c2=0, c1=52.3x", C1_IST_RATIO, 0.0)]:
        dn = delta_n_surface(c1r, c2r)
        r_dec = decoupling_radius(c1r, c2r)
        vr = vr_energy(c1r)
        dec_ok = 30.0 < r_dec < 300.0
        vr_ok = E_BAND[0] < vr < E_BAND[1]
        rows.append({
            "model": name, "c1_ratio": round(c1r, 3),
            "c2_ratio": c2r,
            "delta_n_surface": round(dn, 5),
            "decoupling_radius_Rstar": round(r_dec, 1),
            "decoupling_in_30_300": bool(dec_ok),
            "vr_energy_keV": round(vr, 2),
            "vr_in_2_4_keV": bool(vr_ok),
        })
    return rows


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ---- H62a: mode algebra verification ------------------------------------
    print("=== H62a: mode algebra vs canonical QED ===")
    rows_a = verify_mode_algebra()
    for r in rows_a:
        print(f"  theta={r['theta']:.2f}: derived n_par={r['derived_npar']:.6e} "
              f"vs canonical {r['canonical_npar']:.6e}; n_perp "
              f"{r['derived_nperp']:.6e} vs {r['canonical_nperp']:.6e}; "
              f"ratio {r['ratio_derived']:.4f} vs {r['ratio_canonical']:.4f}; "
              f"on-shell check {r['onshell_invariant']:.1e}")
    with open(os.path.join(OUT_DIR, "mode_algebra.csv"),
              "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows_a[0].keys()))
        w.writeheader()
        w.writerows(rows_a)

    print("\n=== H62a: achiral vacuum (c2 = 0) ===")
    rows_a2 = achiral_mode_algebra()
    for r in rows_a2:
        print(f"  theta={r['theta']:.2f}: n_par - 1 = {r['n_par_minus_1']:.2e} "
              f"(non-refractive: {r['n_par_is_one']}), "
              f"n_perp - 1 = {r['n_perp_minus_1']:.6e}")

    # ---- H62b: magnetar observables -----------------------------------------
    print("\n=== H62b: magnetar 1E 1547.0-5408 (B = 2.2e14 G, R* = 12 km) ===")
    b = MAGNETAR_B / B_CR
    print(f"  B/B_cr = {b:.2f}")
    obs_rows = []
    for name, c1r, c2r in [("QED", 1.0, 1.0),
                           ("IST (ii) c2=0, c1~QED", 1.0, 0.0),
                           ("IST (i) c2=0, c1=52.3x", C1_IST_RATIO, 0.0)]:
        dn = delta_n_surface(c1r, c2r)
        phi = accumulated_phase(c1r, c2r)
        r_dec = decoupling_radius(c1r, c2r)
        vr = vr_energy(c1r)
        obs_rows.append({"model": name, "c1_ratio": c1r, "c2_ratio": c2r,
                         "delta_n_surface": dn, "accumulated_phase_rad": phi,
                         "decoupling_radius_Rstar": r_dec,
                         "vr_energy_keV": vr})
        print(f"  {name}: Delta n(surf) = {dn:.3e}, accumulated phase = "
              f"{phi:.2e} rad, decoupling radius = {r_dec:.0f} R*, "
              f"VR energy = {vr:.2f} keV")
    with open(os.path.join(OUT_DIR, "magnetar_observables.csv"),
              "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(obs_rows[0].keys()))
        w.writeheader()
        w.writerows(obs_rows)

    gate_rows = registration_gate()
    with open(os.path.join(OUT_DIR, "registration_gate.csv"),
              "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(gate_rows[0].keys()))
        w.writeheader()
        w.writerows(gate_rows)

    print("\n=== H62c/H62d: the registration gate ===")
    print("  anchors: decoupling radius 30-300 R*; VR dip 2-4 keV (observed)")
    for r in gate_rows:
        print(f"  {r['model']}: r_dec = {r['decoupling_radius_Rstar']} R* "
              f"(in band: {r['decoupling_in_30_300']}), "
              f"VR = {r['vr_energy_keV']} keV (in band: {r['vr_in_2_4_keV']})")
    print("\n  GATE VERDICT:")
    print("  (1) c2/c1 = 0 (structural): SURVIVES -- n(E||B) = 1 exactly at all")
    print("      angles; no E||B-mode vacuum resonance; normalization-")
    print("      independent; untested by current data (no |Delta n| extracted).")
    print("  (2) c1 = 52.3x QED (Phase 56 H56b reading): TENSION -- the VR dip")
    print("      moves to ~0.3-0.6 keV, contradicting the observed 2-4 keV dip;")
    print("      gated OFF pending a physical c1 normalization derivation.")
    print("  (3) c1 ~ QED (branch ii): CONSISTENT -- 4/3 Delta n magnitude,")
    print("      decoupling ~145 R* (QED ~136), VR unchanged.")

    make_figure(rows_a, gate_rows)
    print(f"\nWrote {OUT_DIR}")


def make_figure(rows_a, gate_rows):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A: derived vs canonical mode indices (H62a)
    ax = axes[0, 0]
    th = [r["theta"] for r in rows_a]
    ax.plot(th, [r["canonical_npar"] for r in rows_a], "o--", color="royalblue",
            label=r"canonical $n_\parallel - 1$ (14/45)")
    ax.plot(th, [r["derived_npar"] for r in rows_a], "o", color="skyblue",
            markerfacecolor="none", label=r"derived $n_\parallel - 1$")
    ax.plot(th, [r["canonical_nperp"] for r in rows_a], "s--", color="crimson",
            label=r"canonical $n_\perp - 1$ (8/45)")
    ax.plot(th, [r["derived_nperp"] for r in rows_a], "s", color="salmon",
            markerfacecolor="none", label=r"derived $n_\perp - 1$")
    ax.set_xlabel(r"$\theta_B$ (rad)")
    ax.set_ylabel(r"index shift (units of $\alpha^2 B^2/m^4$)")
    ax.set_title(r"A. Mode algebra: derived vs canonical QED (ratio 7/4 = $c_2/c_1$)")
    ax.legend(fontsize=8)

    # B: decoupling radius vs c1 scale + paper's 30-300 R* band (H62b)
    ax = axes[0, 1]
    cr = np.logspace(-1, 2, 100)
    rdec = [decoupling_radius(c, 1.0) for c in cr]
    ax.semilogx(cr, rdec, color="royalblue", label="QED-mode coupling")
    ax.axhspan(30, 300, color="seagreen", alpha=0.2,
               label="paper: 30-300 R* decoupling")
    ax.axvline(1.0, color="black", ls=":", lw=1, label="QED c1")
    ax.axvline(C1_IST_RATIO, color="crimson", ls=":",
               label=r"$c_1=52.3\times$ (Phase 56)")
    ax.set_xlabel(r"$c_1 / c_{1,\rm QED}$")
    ax.set_ylabel(r"decoupling radius ($R_*$)")
    ax.set_title("B. Decoupling radius vs c1 scale (H62b)")
    ax.legend(fontsize=8)

    # C: VR energy vs c1 scale + observed 2-4 keV band (H62b)
    ax = axes[1, 0]
    evr = [vr_energy(c) for c in cr]
    ax.semilogx(cr, evr, color="goldenrod")
    ax.axhspan(2, 4, color="seagreen", alpha=0.2, label="observed 2-4 keV dip")
    ax.axvline(1.0, color="black", ls=":", lw=1, label="QED c1")
    ax.axvline(C1_IST_RATIO, color="crimson", ls=":", label="52.3x c1")
    ax.set_xlabel(r"$c_1 / c_{1,\rm QED}$")
    ax.set_ylabel("VR (mode-conversion) energy [keV]")
    ax.set_title("C. Vacuum-resonance energy: 2-4 keV pins c1 ~ QED (H62b)")
    ax.legend(fontsize=8)

    # D: the gate verdict (H62c/H62d)
    ax = axes[1, 1]
    ax.axis("off")
    lines = [
        "GATE VERDICT (Stewart et al. 2026)",
        "",
        "c2/c1 = 0 (structural): SURVIVES",
        "  n(E||B) = 1 exactly at all angles",
        "  no E||B vacuum resonance",
        "  normalization-independent; untested",
        "",
        "c1 = 52.3x QED (H56b reading): TENSION",
        "  VR dip -> ~0.4 keV (obs: 2-4 keV)",
        "  gated OFF pending c1 normalization",
        "",
        "c1 ~ QED (branch ii): CONSISTENT",
        "  |dn| = (4/3) QED, r_dec ~ 145 R*",
    ]
    ax.text(0.5, 0.5, "\n".join(lines), ha="center", va="center", fontsize=10,
            bbox=dict(boxstyle="round", fc="lightgoldenrodyellow"))
    ax.set_title("D. Registration gate (H62d)")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "ixpe_vb_gate.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
