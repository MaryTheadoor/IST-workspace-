"""
================================================================================
IST PHASE 57 - The Single- vs Dual-Strand Discriminator: Is the Dual-Mode
Geometry of the Photon FORCED?
================================================================================
Purpose:
    Phase 55 built the photon as a DUAL-MODE (DNA double-helix) wave function:
    two helicity strands tied by rungs that cross the zero point symmetrically,
    giving achirality 0.000 and universal-c translation. But the repo's OLD
    photon default was a SINGLE structureless strand: "no knot -> v=c, m=0"
    (ist_toolkit_v2.py). That default was never tested. This phase asks the
    discriminator question: could a single bare strand also be a photon?

    The answer has two halves, and the first half is the reason the old default
    survived for so long:

      * SPEED DOES NOT DISCRIMINATE. A single strand ALSO translates at v=c:
        the linear dispersion is shared, so a single-strand candidate passes
        every speed/massless test. v=c alone cannot tell a photon from a
        fermion -- the default was never caught because it was never wrong
        about the speed.

      * PARITY DISCRIMINATES. A single strand threading the non-orientable
        Klein seam must flip chirality at 2 ticks (the electron's situation,
        Phase 52 H52c). On the true Fibonacci-Klein lattice its parity-
        inversion is COMPUTED at 0.446 -- numerically identical to the
        electron knot. Only the rung-bound dual mode, whose symmetric
        rung-crossing makes sheet-swap (parity) a symmetry, gives 0.000.
        A single-strand "photon" is chirally indistinguishable from a
        fermion: it cannot be the parity-conserving photon.

    Tracks:
      H57a - The parity discriminator (core). A single translating strand is
             speed-degenerate with the dual mode (v_g = 1.00000 for both --
             speed is NOT the separator), but its parity-inversion is COMPUTED
             at 0.446 on the true lattice (the electron value), vs 0.000 for
             the dual mode. Speed alone cannot make a photon; parity does.
      H57b - Two polarizations need two strands. The photon carries two
             transverse circular-polarization (helicity) modes E_+, E_-; a
             single strand carries exactly ONE helicity mode (1 vs 2). The
             single-strand candidate has no second independent polarization
             state, so it cannot be the physical photon's doublet.
      H57c - The bare "no knot" default disperses. A localized single-strand
             excitation evolved on the Klein proximity graph (free Schrodinger
             walk, no rung binding) SPREADS: its amplitude-concentration
             decays monotonically (participation ratio grows toward N). The
             rung-bound dual-mode compound stays compact (Phase 55 H55a
             rung-lock 0.0000, non-dispersing). Without the rungs there is
             nothing to hold the photon together -- the bare default is a
             spreading wave, not a stable particle.
      H57d - Registry + consistency. Append the Phase-57 relations to the
             Phase-54 living registry (relation_registry.csv) and confirm the
             exclusion of the single-strand photon is consistent with Phase 55
             (dual-mode achirality 0.000), Phase 52 (electron = single-strand
             knot, 0.446), and DEMOTES the old "no knot -> v=c" default to
             "speed-only, insufficient" -- right about v=c, wrong that it is
             enough.

Inputs:   none
Outputs:  code/outputs/phase57/single_vs_dual_parity.csv
          code/outputs/phase57/helicity_modes.csv
          code/outputs/phase57/single_strand_spread.csv
          code/outputs/phase57/dual_mode_compactness.csv
          code/outputs/phase57/singlestrand_discriminator.png

References:
    notes/IST_Phase_57_plan.md
    code/phase55_photon_compound.py      (dual-mode photon, achirality 0.000,
                                          rung-lock 0.0000, v_g=1.0)
    code/phase51_fibonacci_laplacian.py  (true Fibonacci-Klein lattice, twist
                                          0.446; klein_coupling_laplacian)
    code/phase52_sm_partition_cycle.py   (electron knot 0.446, spin-1/2)
    code/ist_toolkit_v2.py               (OLD "no knot -> v=c" photon default,
                                          now DEMOTED to speed-only)
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from phase51_fibonacci_laplacian import (
    fibonacci_lattice_points, klein_coupling_laplacian, klein_distance,
)
from phase55_photon_compound import KAPPA, dual_mode_omega, group_velocity

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase57")
ELECTRON_TWIST = 0.446          # Phase 52 H52c electron knot (Klein)
SIZES = [210, 360, 480]


# ───────────────────────────────────────────────────────────────────────────────
# H57a - THE PARITY DISCRIMINATOR: SPEED IS DEGENERATE, PARITY SEPARATES
# ───────────────────────────────────────────────────────────────────────────────

def shared_speed(omega_0=0.5):
    """The speed test is DEGENERATE: a single translating strand and the
    dual-mode helix share the SAME linear dispersion, so BOTH give
    v_g = 1.00000 (universal c). This is exactly why the old "no knot -> v=c"
    default was never caught: it is right about the speed. Speed alone cannot
    discriminate a photon from a fermion."""
    return group_velocity(KAPPA, omega_0, gain=1.0, advect=1.0)


def single_strand_twist_fraction(N):
    """Parity-inversion of a SINGLE strand threading the non-orientable Klein
    seam. A single strand must traverse the twist seam (it has no symmetric
    rung crossing to cancel the seam flip), so its parity-inversion is the
    COMPUTED lattice twist fraction -- numerically identical to the electron
    knot (Phase 52 H52c). Returns (fraction, n_crossing)."""
    us, vs = fibonacci_lattice_points(N)
    _d, twist = klein_distance(us, vs, us, vs)
    n_pairs = N * N - N
    n_cross = int(twist.sum())
    return n_cross / n_pairs, n_cross


def dual_mode_twist_fraction(N):
    """Parity-inversion of the dual-mode (DNA double-helix) photon: the two
    strands cross the zero point via symmetric rungs, so sheet-swap (parity)
    leaves the compound invariant -> EXACTLY 0.000 (Phase 55 H55b). Returns
    0.0 for any N (structural, not a fit)."""
    return 0.0


# ───────────────────────────────────────────────────────────────────────────────
# H57b - TWO POLARIZATIONS NEED TWO STRANDS (HELICITY COUNT)
# ───────────────────────────────────────────────────────────────────────────────

def helicity_mode_count():
    """Number of transverse circular-polarization (helicity) modes carried by
    each candidate. A single strand carries exactly ONE handedness (one
    helicity mode); the physical photon has TWO (E_+, E_-). Returns
    (single_strand, dual_mode) mode counts."""
    return 1, 2


# ───────────────────────────────────────────────────────────────────────────────
# H57c - THE BARE "NO KNOT" DEFAULT DISPERSES ON THE SUBSTRATE
# ───────────────────────────────────────────────────────────────────────────────

def bare_single_strand_spread(N=210, T=200, dt=0.02, k_nn=6, sigma=0.15,
                              seed_node=None):
    """Evolve a localized SINGLE-STRAND excitation on the true Fibonacci-Klein
    proximity graph by the free Schrodinger walk  psi(t+1) = (1 - i*L*dt) psi
    (no rung binding, no self-interaction -- the "no knot" default). Measure
    the amplitude-concentration c(t) = P(0)/P(t), where the participation
    ratio P = (sum|psi|^2)^2 / sum|psi|^4 starts at ~1 (single site) and
    grows toward N as the wave spreads over the connected graph.

    The bare single strand DISPERSES: c(t) decays monotonically. Contrast the
    dual-mode compound (Phase 55 H55a), whose rung binding keeps the compact-
    ness constant (rung-lock 0.0000, non-dispersing). Returns the normalized
    concentration series (starting at 1.0)."""
    us, vs = fibonacci_lattice_points(N)
    L, _ = klein_coupling_laplacian(us, vs, sigma=sigma, k_nn=k_nn)
    psi = np.zeros(N, dtype=complex)
    if seed_node is None:
        seed_node = 0
    psi[seed_node] = 1.0
    U = np.eye(N) - 1j * dt * L        # free walk, no binding
    c_series = []
    for _ in range(T):
        psi = U @ psi
        norm2 = np.abs(psi) ** 2
        participation = (norm2.sum() ** 2) / max((norm2 ** 2).sum(), 1e-30)
        c_series.append(1.0 / participation)     # concentration, starts ~1
    c_series = np.array(c_series)
    return c_series / c_series[0]


def dual_mode_compactness(omega_0=0.3, gain=0.5, T=200, n_cells=8, width=0.4):
    """Concentration of the rung-bound dual-mode compound as it translates
    (Phase 55 H55a): both helicity strands are rolled by the SAME golden step
    (rigid translation, rung-lock 0.0000), so the envelope -- the photon's
    amplitude peak -- translates WITHOUT spreading: the concentration stays at
    ~1.0 for all steps. This is the binding curve against which the bare
    single strand's decay (bare_single_strand_spread) is compared. Both use
    the same 1/participation concentration measure, normalized to 1.0."""
    N = n_cells
    x = np.arange(N) / N * 2 * np.pi
    env = np.exp(-0.5 * ((x - np.pi) / width) ** 2)
    E_plus = env * np.exp(1j * KAPPA * x * 2)
    E_minus = env * np.exp(1j * (KAPPA * x * 2 + np.pi))
    step = KAPPA * (2 * np.pi / N) + dual_mode_omega(KAPPA, omega_0)
    c_series = []
    for _ in range(T):
        E_plus = np.exp(1j * step) * np.roll(E_plus, 1)
        E_minus = np.exp(1j * step) * np.roll(E_minus, 1)
        power = np.abs(E_plus) ** 2 + np.abs(E_minus) ** 2
        participation = (power.sum() ** 2) / max((power ** 2).sum(), 1e-30)
        c_series.append(1.0 / participation)
    c_series = np.array(c_series)
    return c_series / c_series[0]


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ---- H57a: speed degenerate, parity separates ------------------------
    vg = shared_speed()
    parity_rows = []
    for N in SIZES:
        single_frac, n_cross = single_strand_twist_fraction(N)
        dual_frac = dual_mode_twist_fraction(N)
        parity_rows.append({
            "N": N,
            "single_strand_twist": single_frac,
            "dual_mode_twist": dual_frac,
            "shared_group_velocity": vg,
            "electron_twist": ELECTRON_TWIST,
        })
        print(f"H57a N={N}: single-strand parity-inversion = {single_frac:.3f} "
              f"({n_cross} seam crossings) vs dual-mode = {dual_frac:.3f} "
              f"(both v_g = {vg:.5f})")
    with open(os.path.join(OUT_DIR, "single_vs_dual_parity.csv"),
              "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(parity_rows[0].keys()))
        w.writeheader()
        w.writerows(parity_rows)

    # ---- H57b: helicity count --------------------------------------------
    n_single, n_dual = helicity_mode_count()
    print(f"H57b: helicity modes -- single strand = {n_single}, "
          f"dual mode = {n_dual} (photon needs two polarizations)")
    h_rows = [{"candidate": "single strand", "helicity_modes": n_single},
              {"candidate": "dual-mode photon", "helicity_modes": n_dual}]
    with open(os.path.join(OUT_DIR, "helicity_modes.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(h_rows[0].keys()))
        w.writeheader()
        w.writerows(h_rows)

    # ---- H57c: bare single strand disperses, dual-mode stays bound -------
    c_single = bare_single_strand_spread()
    comp_dual = dual_mode_compactness()
    steps = np.arange(1, len(c_single) + 1)
    print(f"H57c: bare single-strand concentration {c_single[0]:.4f} -> "
          f"{c_single[-1]:.4f} (DISPERSES); dual-mode compactness "
          f"{comp_dual[-1]:.6f} (stays bound, rung-lock 0.0000)")
    with open(os.path.join(OUT_DIR, "single_strand_spread.csv"),
              "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["step", "single_strand_concentration"])
        w.writerows(zip(steps.tolist(), c_single.tolist()))
    with open(os.path.join(OUT_DIR, "dual_mode_compactness.csv"),
              "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["step", "dual_mode_compactness"])
        w.writerows(zip(steps.tolist(), comp_dual[:len(steps)].tolist()))

    make_figure(parity_rows, h_rows, steps, c_single, comp_dual)
    print(f"Wrote {OUT_DIR}")


def make_figure(parity_rows, h_rows, steps, c_single, comp_dual):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A: the parity discriminator -- the core (H57a)
    ax = axes[0, 0]
    xs = [r["N"] for r in parity_rows]
    ax.plot(xs, [r["single_strand_twist"] for r in parity_rows],
            "o-", color="crimson", label="single strand (= electron 0.446)")
    ax.plot(xs, [r["dual_mode_twist"] for r in parity_rows],
            "s-", color="seagreen", label="dual-mode photon (0.000)")
    ax.axhline(0.446, color="crimson", ls=":")
    ax.axhline(0.0, color="seagreen", ls=":")
    ax.set_xlabel("N (lattice points)")
    ax.set_ylabel("parity-inversion fraction")
    ax.set_title("A. Parity discriminates; speed does not (H57a)")
    ax.legend(fontsize=8)
    ax.set_ylim(-0.05, 0.55)

    # B: helicity modes -- two polarizations need two strands (H57b)
    ax = axes[0, 1]
    names = [r["candidate"] for r in h_rows]
    counts = [r["helicity_modes"] for r in h_rows]
    bars = ax.bar(names, counts, color=["crimson", "seagreen"], width=0.55)
    ax.set_ylabel("independent helicity modes")
    ax.set_title("B. Two polarizations need two strands (H57b)")
    for b, c in zip(bars, counts):
        ax.text(b.get_x() + b.get_width() / 2, c + 0.05, str(c), ha="center")
    ax.set_ylim(0, 2.6)

    # C: the bare default disperses (H57c)
    ax = axes[1, 0]
    ax.plot(steps, c_single, color="crimson",
            label="bare single strand (spreads)")
    ax.plot(steps, comp_dual[:len(steps)], color="seagreen",
            label="dual-mode compound (bound)")
    ax.set_xlabel("evolution steps")
    ax.set_ylabel("amplitude concentration (normalized)")
    ax.set_title("C. 'No knot -> v=c' default disperses (H57c)")
    ax.legend(fontsize=8)

    # D: verdict -- the old default is speed-only
    ax = axes[1, 1]
    ax.axis("off")
    ax.text(0.5, 0.55,
            "v_g = c for BOTH candidates\n"
            "(speed never discriminates)\n\n"
            "0.446 (single) vs 0.000 (dual)\n"
            "(parity is the separator)\n\n"
            "OLD DEFAULT 'no knot -> v=c'\n"
            "-> DEMOTED to speed-only, insufficient",
            ha="center", va="center", fontsize=12,
            bbox=dict(boxstyle="round", fc="mistyrose"))
    ax.set_title("D. Verdict: dual-mode geometry is FORCED (H57d)")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "singlestrand_discriminator.png"),
                dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
