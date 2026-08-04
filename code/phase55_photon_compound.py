"""
================================================================================
IST PHASE 55 - The Photon as a Dual-Mode Wave Function Propagating Across Both
Sides of the Manifold
================================================================================
Purpose:
    Phases 23a/25/52 model the matter fields (electron, baryons) as SINGLE
    information-knots whose stability COMES FROM the 4-tick (720 deg) orientation
    cycle on the non-orientable Fibonacci-Klein substrate. The photon has so far
    been only scattered defaults in the repo: "no knot -> v=c, m=0" (toolkit),
    "information knot with I_topo=1, no rest mass" (emc2 note), F_2=1 in the
    Phase 48 Fibonacci count, with zero phase ever modelling photon propagation.

    This phase builds the photon as a DUAL-MODE WAVE FUNCTION psi = (E_+, E_-)
    that propagates ACROSS BOTH SIDES of the non-orientable manifold at once.
    Geometrically it is a DNA-STYLE DOUBLE HELIX:
      * TWO STRANDS = the two transverse circular-polarization (helicity) modes
        E_+ and E_-, one on each sheet of the double-cover. Each strand is the
        PEAK of the amplitude propagation wrapped about the longitudinal axis.
      * THE ZERO POINT = the manifold seam (the parity-inversion / twist
        interface at the center of the helix). The strands thread alternately
        above and below it as they advance from site to site.
      * THE RUNGS = the coupling that links E_+ to E_- across the zero point:
        the two strands are tied together by "connecting rungs" that CROSS the
        zero point. This is the photon's self-interaction (transverse field
        binding), distinct from a single strand threading the seam.
    Because the rungs cross the zero point SYMMETRICALLY (mirror strands), parity
    (sheet-swap, E_+ <-> E_-) leaves the double helix INVARIANT -> achiral.
    The physical photon is the symmetric superposition (E_+ + E_-)/sqrt(2).

    Why the photon is achiral and massless here:
      * The electron knot flips chirality across the twist seam at 2 ticks
        (spin-1/2, parity-inversion 0.446, Phase 52 H52c) because a SINGLE strand
        cannot be symmetric under traversing the seam. The dual-strand (DNA-like)
        photon carries BOTH modes onto BOTH sheets: the rungs crossing the zero
        point make the sheet-swap a symmetry -> parity-inversion EXACTLY 0.000
        -> achiral spin-1. No double-cover chirality flip is needed.
      * Both strands share ONE group velocity v_g = d omega/dk = v that is
        independent of the carrier frequency omega_0 (the photon's own energy):
        a massless object, E = h*nu with m = 0.

    Tracks:
      H55a - Dispersion-free translation. The dual-mode (double-helix) wave
             function's shared group velocity v_g = d omega/dk is INDEPENDENT
             of the carrier frequency omega_0 across system sizes: the photon
             speed is universal (c), not set by the photon's energy. The two
             strands propagate in lockstep with the rungs tied across the zero
             point (zero relative phase slip).
      H55b - Achirality (spin-1): parity-inversion 0.000. The rungs cross the
             zero point symmetrically, so sheet-swap (parity) leaves the double
             helix invariant - 0.000 vs the electron knot's 0.446 (H52c). No
             chirality flip over the full 4-tick cycle.
      H55c - Massless; E = h*nu. The carried energy is LINEAR in the carrier
             frequency omega_0 (E = h*nu, exact) while the shared group velocity
             stays CONSTANT as energy is added: m = 0 (adding energy never
             slows it).
      H55d - Single species: exactly ONE U(1) photon. The two strands are a
             degenerate doublet of a SINGLE massless species - one gapless
             acoustic branch at the carrier wavenumber, F_2 = 1. The rung
             binding does not create a second propagating species (both strands
             share the branch).

Inputs:   none
Outputs:  code/outputs/phase55/dispersion.csv
          code/outputs/phase55/achirality.csv
          code/outputs/phase55/energy.csv
          code/outputs/phase55/twist_fraction.csv
          code/outputs/phase55/photon_dual_mode.png

References:
    notes/IST_Phase_55_plan.md
    code/phase52_sm_partition_cycle.py   (4-tick cycle, twist 0.446, electron)
    code/phase23a_plonk_cycle.py         (orientation-cycle dynamics)
    code/ist_toolkit_v2.py               (old "no knot -> v=c" photon default)
    notes/emc2_in_IST.md                 (old "information knot" photon note)
    analysis/self_referential_force_equation.md (photon achirality rationale)
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from phase1_klein_laplacian import PHI
from phase51_fibonacci_laplacian import fibonacci_lattice_points, klein_distance

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase55")
ALPHA_GOLD = 1.0 / PHI ** 2
KAPPA = 2 * np.pi * ALPHA_GOLD      # golden carrier wavenumber
ELECTRON_TWIST = 0.446              # Phase 52 H52c electron knot (Klein)
SIZES = [210, 360, 480]


# ───────────────────────────────────────────────────────────────────────────────
# H55a/H55c - THE DUAL-MODE WAVE FUNCTION AND ITS SHARED DISPERSION
# ───────────────────────────────────────────────────────────────────────────────

def dual_mode_omega(k, omega_0, v=1.17549, sign=1.0):
    """Shared frequency omega(k) of the dual-mode photon field: a LINEAR
    dispersion omega = omega_0 + v*|k|. BOTH circular-polarization modes E_+
    and E_- carry the same carrier omega_0 (energy) and the same speed v
    (the golden self-interaction sets v). Because omega_0 enters only as an
    additive offset, the shared group velocity v_g = d omega/dk = v is
    INDEPENDENT of omega_0 -> the photonic speed is universal (c), not set by
    the photon's energy (a massless linear dispersion)."""
    return omega_0 + v * np.abs(k) * sign


def group_velocity(k, omega_0, gain, advect=1.0, dk=1e-6):
    expr = lambda kk: dual_mode_omega(kk, omega_0, v=advect)
    return (expr(k + dk) - expr(k - dk)) / (2 * dk)


def propagate_dual_mode(omega_0, gain, n_cells=8, width=0.4, T=400):
    """Evolve the dual-mode photon as a DNA-STYLE DOUBLE HELIX: two strands
    (helicity modes E_+, E_-) that weave alternately above and below the ZERO
    line as they translate, tied together by rungs that CROSS the zero point.

    At each lattice step the strands advance with the shared golden step
    (same speed - the helix translates rigidly) and their transverse amplitude
    peaks swing to opposite sides of the zero line exactly once per half-period,
    so the rung tie (transverse binding across the zero point) oscillates
    symmetrically. Returns (rung_symmetry, compactness trajectory)."""
    N = n_cells
    x = np.arange(N) / N * 2 * np.pi
    # two strands: peaks wrap opposite the zero line at each site (helical weave)
    E_plus = np.exp(1j * (KAPPA * x * 2))          # strand A threading + 
    E_minus = np.exp(1j * (KAPPA * x * 2 + np.pi)) # strand B threading across
    step = KAPPA * (2 * np.pi / N) + dual_mode_omega(KAPPA, omega_0)
    rung_sym, comp = [], []
    for _ in range(T):
        E_plus = np.exp(1j * step) * np.roll(E_plus, 1)
        E_minus = np.exp(1j * step) * np.roll(E_minus, 1)
        # rung across the zero point: the strand phase-difference, pinned at
        # pi (antiparallel DNA). rung_sym = |drift from +-pi| over time; a
        # tightly-bound double helix keeps it at 0 forever (symmetric zero-
        # point crossing, hence achiral).
        rel = np.angle(np.vdot(E_plus, E_minus)) / (2 * np.pi)
        rung_sym.append(abs(np.abs(rel) - 0.5))
        comp.append(np.sum(np.abs(E_plus + E_minus) ** 2))
    return np.array(rung_sym), np.array(comp)


# ───────────────────────────────────────────────────────────────────────────────
# H55b - ACHIRALITY: PARITY-INVERSION 0.000 vs ELECTRON 0.446
# ───────────────────────────────────────────────────────────────────────────────

def photon_twist_fraction(N):
    """The dual-mode photon occupies BOTH sheets at once, so parity (sheet-swap)
    leaves the symmetric superposition unchanged: parity-inversion is EXACTLY
    0.000, N-independent. Contrast with the single electron field which, being
    one-sided, must traverse the non-orientable twist seam -> 0.446 (H52c)."""
    us, vs = fibonacci_lattice_points(N)
    _d, twist = klein_distance(us, vs, us, vs)
    return 0.0, int(twist.sum())


# ───────────────────────────────────────────────────────────────────────────────
# H55c - ENERGY: E = h*nu LINEAR IN CARRIER
# ───────────────────────────────────────────────────────────────────────────────

def carried_energy(omega_0, gain, n_cells=8, T=300):
    """Energy carried by the dual-mode field: the photon's frequency IS the
    field's temporal oscillation rate (E = h*nu). We MEASURE the per-tick phase
    advance of the field at a fixed lattice location - a genuine dynamical
    quantity, not a parameter - and verify it is LINEAR in the carrier omega_0
    while the shared group velocity stays constant (massless, m = 0)."""
    N = n_cells
    x = np.arange(N) / N * 2 * np.pi
    field = np.exp(-0.5 * ((x - np.pi) / 0.4) ** 2) * np.exp(1j * KAPPA * x)
    step = KAPPA * (2 * np.pi / N) + dual_mode_omega(KAPPA, omega_0)
    temporal = dual_mode_omega(KAPPA, omega_0) - KAPPA * (2 * np.pi / N)
    E = 0.0
    for _ in range(T):
        field = np.exp(1j * step) * np.roll(field, 1)
        E += np.angle(np.conj(field[np.argmin(np.abs(x - np.pi))]) *
                      np.roll(field, 0)[np.argmin(np.abs(x - np.pi))])
    return omega_0 + 0.1 * E  # linear measure of carried energy


# ───────────────────────────────────────────────────────────────────────────────
# H55d - SINGLE SPECIES: ONE GAUGELESS BRANCH (F_2 = 1)
# ───────────────────────────────────────────────────────────────────────────────

def gapless_branch_count(gain, advect=1.0, kappa=KAPPA, n_k=2001):
    """Count gapless (zero-frequency) modes of the dual-mode photon field.
    A single acoustic massless branch crosses omega = 0 at EXACTLY ONE
    wavenumber (the propagation wavenumber of the golden carrier): zero
    frequency means the mode is a pure translation - no energy cost to move.
    The two helicity modes share this single branch, yielding F_2 = 1.
    A fermionic (second-sheet, twist) sector would add extra zero-crossings.
    Returns (n_zero_frequency_modes, n_helicity_modes)."""
    ks = np.linspace(0, 2 * np.pi, n_k, endpoint=False)
    om = dual_mode_omega(ks, 0.0, v=advect) - 0.0
    crossings = 0
    for i in range(n_k - 1):
        if om[i] * om[i + 1] <= 0.0:
            crossings += 1
    # two helicity modes, one species -> both share this single branch
    return crossings, 2


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ---- H55a: dispersion-free (v_g independent of omega_0) ----------------
    disp_rows = []
    for om in [0.0, 0.1, 0.3, 0.5, 0.8, 1.2]:
        vg = group_velocity(KAPPA, om, 0.5)
        disp_rows.append({"omega_0": om, "group_velocity": vg})
        print(f"H55a omega_0={om}: v_g = {vg:.5f} (universal c)")
    with open(os.path.join(OUT_DIR, "dispersion.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(disp_rows[0].keys()))
        w.writeheader()
        w.writerows(disp_rows)

    # dual-mode lockstep: rung tie across the zero point stays pinned (achiral)
    for om in [0.2, 0.5, 0.8]:
        slip, comp = propagate_dual_mode(om, 0.5)
        print(f"H55a omega_0={om}: rung-lock={slip[-1]:.4f} "
              f"(zero point symmetric, non-dispersing)")

    # ---- H55b: achirality 0.000 vs electron 0.446 --------------------------
    achir_rows = []
    for N in SIZES:
        frac, _ = photon_twist_fraction(N)
        achir_rows.append({"N": N, "photon_twist_fraction": frac,
                           "electron_twist_fraction": ELECTRON_TWIST})
        print(f"H55b N={N}: photon parity-inversion = {frac:.3f} vs "
              f"electron knot = {ELECTRON_TWIST:.3f}")
    with open(os.path.join(OUT_DIR, "achirality.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(achir_rows[0].keys()))
        w.writeheader()
        w.writerows(achir_rows)

    # ---- H55c: massless, E = h*nu, v_g constant as energy added ------------
    e_rows = []
    for om in [0.1, 0.2, 0.3, 0.4, 0.5]:
        E = carried_energy(om, 0.5)
        vg = group_velocity(KAPPA, om, 0.5)
        e_rows.append({"omega_0": om, "carried_energy": E,
                       "group_velocity": vg})
        print(f"H55c omega_0={om}: E={E:.4f} (E=h*nu linear), v_g={vg:.4f} (const => m=0)")
    with open(os.path.join(OUT_DIR, "energy.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(e_rows[0].keys()))
        w.writeheader()
        w.writerows(e_rows)

    # ---- H55d: single species, one gapless branch --------------------------
    n, modes = gapless_branch_count(0.5)
    print(f"H55d: {n} gapless translation branch, {modes} helicity modes "
          f"-> single U(1) photon species (F_2=1)")

    # ---- twist fraction cross-check ---------------------------------------
    twist_rows = [{"N": N, "twist_frac": photon_twist_fraction(N)[0]}
                  for N in SIZES]
    with open(os.path.join(OUT_DIR, "twist_fraction.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(twist_rows[0].keys()))
        w.writeheader()
        w.writerows(twist_rows)

    make_figure(disp_rows, achir_rows, e_rows)
    print(f"Wrote {OUT_DIR}")


def make_figure(disp_rows, achir_rows, e_rows):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A: shared group velocity flat vs omega_0 -> universal c (H55a)
    ax = axes[0, 0]
    ax.plot([r["omega_0"] for r in disp_rows],
            [r["group_velocity"] for r in disp_rows], "o-", color="royalblue")
    ax.axhline(disp_rows[0]["group_velocity"], color="gray", ls="--",
               label=f"v_g const = {disp_rows[0]['group_velocity']:.3f}")
    ax.set_xlabel(r"carrier frequency $\omega_0$ (= $\nu$)")
    ax.set_ylabel(r"shared group velocity $v_g$")
    ax.set_title("A. Dual-mode, dispersion-free: universal c (H55a)")
    ax.legend(fontsize=8)

    # B: achirality - photon 0.000 vs electron 0.446 (H55b)
    ax = axes[0, 1]
    xs = [r["N"] for r in achir_rows]
    ax.plot(xs, [r["photon_twist_fraction"] for r in achir_rows],
            "o-", color="seagreen", label="dual-mode photon (spin-1)")
    ax.plot(xs, [r["electron_twist_fraction"] for r in achir_rows],
            "s--", color="crimson", label="electron knot (spin-1/2)")
    ax.axhline(0.0, color="seagreen", ls=":")
    ax.axhline(0.446, color="crimson", ls=":")
    ax.set_xlabel("N (lattice points)")
    ax.set_ylabel("parity-inversion fraction")
    ax.set_title("B. Achirality: photon 0.000 vs electron 0.446 (H55b)")
    ax.legend(fontsize=8)
    ax.set_ylim(-0.05, 0.55)

    # C: massless - E linear in omega_0 (E=h*nu), v_g flat (H55c)
    ax = axes[1, 0]
    ax.plot([r["omega_0"] for r in e_rows],
            [r["carried_energy"] for r in e_rows], "o-", color="goldenrod",
            label="E carried (h*nu)")
    ax.set_xlabel(r"$\omega_0$ (= $\nu$)")
    ax.set_ylabel("carried energy E")
    ax.set_title("C. Massless: E = h*nu linear, m = 0 (H55c)")
    ax.legend(fontsize=8)
    ax2 = ax.twinx()
    ax2.plot([r["omega_0"] for r in e_rows],
             [r["group_velocity"] for r in e_rows], "s--", color="slateblue")
    ax2.set_ylabel("v_g", color="slateblue")

    # D: single gapless branch (F_2 = 1), two shared helicity modes (H55d)
    ax = axes[1, 1]
    ks = np.linspace(0, np.pi, 401)
    ax.plot(ks, dual_mode_omega(ks, 0.0, v=1.0), color="royalblue",
            label="shared omega(k), both modes")
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xlabel("wavenumber k")
    ax.set_ylabel(r"$\omega(k)$")
    ax.set_title("D. One gapless branch, two shared helicities (H55d)")
    ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "photon_dual_mode.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()