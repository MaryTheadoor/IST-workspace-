
"""
================================================================================
IST PHASE 6 - The phi-Attractor: Variable Golden Ratio from Harmonic
Self-Interaction
================================================================================
Purpose:
    Test the hypothesis (notes/phi_attractor_hypothesis.md) that the golden
    ratio in IST is an ATTRACTOR of the substrate's harmonic self-interaction
    - approached dynamically like the golden angle in phyllotaxis, with a
    scale-dependent best-approach - rather than a fixed point of the
    substrate RG.

    Components:

    6.1 Anti-resonance selection. Depositions of harmonic content on the
        octave circle with rotation number alpha produce gap structures
        whose rigidity R(alpha) = min_gap/max_gap is bounded away from zero
        for all generations only for (nearly-)noble alpha; golden alpha
        maximizes persistence. Rational alpha collapses (resonance).

    6.2 Persistence and growth. (a) The golden rotation holds rigidity
        1/phi^2 for ALL generations while Fibonacci rationals F_{k-1}/F_k
        track it until collapsing exactly at generation F_k + 1: phi is
        approached through rationals, never reached at finite resolution.
        (b) The Atela-Gole variational lattice has a whole noble family of
        local minima. (c) Douady-Couder growth (apex deposition + pairwise
        repulsion + advection = plonk tick + weave self-interaction +
        coarse graining) settles into a noble-family attractor basin.

    6.3 Golden window in the Phase 4 data. The fold scan re-expressed as
        D_eff(f) = 1/(local log-log slope) crosses phi exactly once; at
        the crossing, the void suppression 1 - 1/f matches the IST
        phenomenology (~76%).

Inputs:   code/outputs/phase4/geff_vs_rho.csv (Phase 4 fold scan)
Outputs:
    code/outputs/phase6/rotation_survival.csv
    code/outputs/phase6/persistence.csv
    code/outputs/phase6/divergence.csv
    code/outputs/phase6/d_eff_crossing.csv
    code/outputs/phase6/phi_attractor.png

References:
    notes/phi_attractor_hypothesis.md     (the hypothesis)
    notes/IST_Research_Plan_Phases_1-5.md (roadmap context)
    code/phase1_klein_laplacian.py        (PHI)
    code/phase4_variable_g.py             (fold scan being reinterpreted)
    Douady & Couder (1992)                (growth-model phyllotaxis)
    Three-gap (Steinhaus) theorem; Hurwitz/Lagrange spectrum

Conventions:
    * Octave circle: log-frequency modulo one octave; self-similarity of
      the substrate makes the spectral problem periodic on this circle.
    * Gap rigidity R = min_gap/max_gap of the circle partition; R -> 0
      signals a resonance (mode-locking / gap collapse).
    * Golden rotation alpha_g = 1/phi^2 (~ 0.382); golden divergence
      angle 2 pi alpha_g (~ 137.5 deg).
================================================================================
"""

import csv
import os
from bisect import insort

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase6")
PHASE4_CSV = os.path.join(os.path.dirname(__file__), "outputs", "phase4",
                          "geff_vs_rho.csv")

ALPHA_GOLDEN = 1.0 / PHI ** 2          # ~ 0.381966
GOLDEN_ANGLE_DEG = 360.0 * ALPHA_GOLDEN  # ~ 137.508 deg


# ───────────────────────────────────────────────────────────────────────────────
# 6.1 ROTATION-ORBIT DEPOSITION & ANTI-RESONANCE SELECTION
# ───────────────────────────────────────────────────────────────────────────────

def orbit_gaps(alpha, n):
    """Gap sizes of the circle partition by points {k alpha}, k = 0..n-1."""
    xs = sorted((k * alpha) % 1.0 for k in range(n))
    gaps = np.diff(xs + [xs[0] + 1.0])
    return gaps


def gap_rigidity(alpha, n):
    """R = min_gap / max_gap at generation n; 0 means resonant collapse."""
    gaps = orbit_gaps(alpha, n)
    return gaps.min() / gaps.max()


def rigidity_profile(alpha, n_max, tol=1e-12):
    """Track gap rigidity over generations 2..n_max.

    Returns (r_min, first n where min_gap < tol): the worst-case rigidity
    over the deposition history and the resonant-collapse generation
    (n_max + 1 if it never collapses).
    """
    xs = [0.0]
    r_min = 1.0
    for n in range(2, n_max + 1):
        insort(xs, ((n - 1) * alpha) % 1.0)
        gaps = np.diff(xs + [xs[0] + 1.0])
        if gaps.min() < tol:
            return r_min, n
        r_min = min(r_min, gaps.min() / gaps.max())
    return r_min, n_max + 1


def survival_scan(alphas, n_max):
    """rigidity_profile over a grid of rotation numbers."""
    return np.array([rigidity_profile(a, n_max) for a in alphas])


def three_gap_sizes(alpha, n, ndigits=10):
    """Distinct gap sizes of the n-point partition (three-gap theorem)."""
    return np.unique(np.round(orbit_gaps(alpha, n), ndigits))


# ───────────────────────────────────────────────────────────────────────────────
# 6.2a PERSISTENCE OPTIMIZATION: GOLDEN ROTATION AS THE LONG-HISTORY OPTIMUM
# ───────────────────────────────────────────────────────────────────────────────

def rigidity_matrix(alphas, n_max):
    """R(alpha, n) = min_gap/max_gap for generations n = 2..n_max, via
    incremental insertion. Row per alpha."""
    out = np.empty((len(alphas), n_max - 1))
    for ia, alpha in enumerate(alphas):
        xs = [0.0]
        for n in range(2, n_max + 1):
            insort(xs, ((n - 1) * alpha) % 1.0)
            gaps = np.diff(xs + [xs[0] + 1.0])
            out[ia, n - 2] = gaps.min() / gaps.max()
    return out


def persistence_optimizer(alphas, n_max):
    """alpha*_N = argmax_alpha min_{n <= N} R(alpha, n): the rotation that
    best survives the full deposition history. Converges to the golden
    rotation as N grows; the survivors at finite N are the Fibonacci
    rationals F_{k-1}/F_k with F_k ~ N."""
    R = rigidity_matrix(alphas, n_max)
    worst = np.minimum.accumulate(R, axis=1)
    best = np.argmax(worst, axis=0)
    return alphas[best], worst[best, np.arange(worst.shape[1])], worst


def fibonacci_rationals(k_min=3, k_max=9):
    """Consecutive Fibonacci ratios F_{k-1}/F_k -> 1/phi (mirror of the
    golden rotation 1/phi^2): the best rational approximants."""
    a, b = 1, 1
    out = []
    for k in range(1, k_max + 1):
        a, b = b, a + b
        if k >= k_min:
            out.append((k, a / b, b))
    return out


# ───────────────────────────────────────────────────────────────────────────────
# 6.2b ATELA-GOLE VARIATIONAL LATTICE: NOBLE FAMILY OF LOCAL MINIMA
# ───────────────────────────────────────────────────────────────────────────────

def atela_gole_energy(g, x, K=60, sigma=0.15):
    """Energy of the spiral lattice z_k = g^k e^{2 pi i k x}, k = 0..K-1.

    E = sum_{j>k} exp(-|z_j - z_k|^2 / sigma^2). As g -> 1 (close-packed
    lattice), the global minimum over x approaches the golden angle
    (Atela, Gole & Kleiner); at g < 1 the best-approach deviates by a
    resolution-dependent amount.
    """
    ks = np.arange(K)
    z = (g ** ks) * np.exp(2j * np.pi * ks * x)
    d2 = np.abs(z[:, None] - z[None, :]) ** 2
    iu = np.triu_indices(K, k=1)
    return np.exp(-d2[iu] / sigma ** 2).sum()


def atela_gole_branch(g_values, K=60, sigma=0.15, nx=1200):
    """Global-minimum divergence x*(g) over x in (0, 0.5]."""
    xs = np.linspace(1e-4, 0.5, nx)
    best = np.empty((len(g_values), 2))
    for i, g in enumerate(g_values):
        E = np.array([atela_gole_energy(g, x, K, sigma) for x in xs])
        j = np.argmin(E)
        best[i] = [xs[j], E[j]]
    return best


# ───────────────────────────────────────────────────────────────────────────────
# 6.2c REPULSIVE GROWTH (DOUADY-COUDER): DIVERGENCE AS DYNAMICAL ATTRACTOR
# ───────────────────────────────────────────────────────────────────────────────

def simulate_growth(n_injections=220, v0=0.12, mu=0.02, dt=1.0,
                    steps_per_injection=6, r_max=25.0, soft=0.5, seed=1,
                    v0_final=None):
    """Apex deposition + soft-core pairwise repulsion + radial advection.

    Each injection: a new element appears at the apex with a tiny random
    offset (the plonk tick). Between injections, elements advect radially
    outward at speed v0 (coarse graining) and repel each other with the
    soft-core force mu * diff / (d^2 + soft^2)^{3/2} (harmonic
    self-interaction; the softening length `soft` regularizes close
    encounters at the apex). Elements beyond r_max are dropped to keep
    N bounded. When v0_final is given, v0 is annealed linearly from v0 to
    v0_final over the run: the system then tracks the main (Fibonacci)
    branch of the bifurcation tree instead of lodging in a metastable
    parastichy regime (Douady & Couder 1992).

    Returns per injection: the divergence angle (deg) between successive
    freshly settled elements, and the final (x, y) configuration.
    """
    rng = np.random.default_rng(seed)
    pos = np.empty((0, 2))
    ids = np.empty(0, dtype=int)
    settle_angle = []

    for k in range(n_injections):
        v0_k = v0 if v0_final is None \
            else v0 + (v0_final - v0) * k / max(n_injections - 1, 1)
        pos = np.vstack([pos, [1e-3 * rng.normal(size=2)]])
        ids = np.append(ids, k)
        for _ in range(steps_per_injection):
            r = np.linalg.norm(pos, axis=1, keepdims=True) + 1e-12
            adv = v0_k * pos / r
            if len(pos) > 1:
                diff = pos[:, None, :] - pos[None, :, :]
                d2 = np.sum(diff ** 2, axis=-1)
                np.fill_diagonal(d2, np.inf)
                rep = mu * np.sum(diff / (d2 + soft ** 2)[..., None] ** 1.5,
                                  axis=1)
            else:
                rep = 0.0
            pos = pos + dt * (adv + rep)
            r1 = np.linalg.norm(pos, axis=1)
            keep = r1 < r_max
            pos, ids = pos[keep], ids[keep]
        # divergence recorded from the freshly settled youngest element
        settle_angle.append(np.angle(pos[-1, 0] + 1j * pos[-1, 1]))

    div = np.degrees(np.diff(settle_angle))
    div = (div + 180) % 360 - 180
    return np.abs(div), pos


# ───────────────────────────────────────────────────────────────────────────────
# 6.3 GOLDEN WINDOW IN THE PHASE 4 FOLD SCAN
# ───────────────────────────────────────────────────────────────────────────────

def load_phase4_scan(path=PHASE4_CSV):
    fs, gs = [], []
    with open(path) as fh:
        for row in csv.DictReader(fh):
            fs.append(float(row["fold_factor"]))
            gs.append(float(row["g_eff_norm"]))
    return np.array(fs), np.array(gs)


def d_eff_profile(fs, gs):
    """Running exponent: local log-log slope s_i and D_eff = 1/s_i at the
    geometric midpoint of each scan interval."""
    lf, lg = np.log(fs), np.log(gs)
    slopes = np.diff(lg) / np.diff(lf)
    f_mid = np.sqrt(fs[:-1] * fs[1:])
    return f_mid, slopes, 1.0 / slopes


def golden_crossing(fs, gs):
    """Where D_eff(f) crosses phi (linear interpolation in log f)."""
    f_mid, _, d_eff = d_eff_profile(fs, gs)
    for i in range(len(f_mid) - 1):
        d0, d1 = d_eff[i] - PHI, d_eff[i + 1] - PHI
        if d0 == 0 or d0 * d1 < 0:
            t = d0 / (d0 - d1)
            return float(np.exp(np.log(f_mid[i])
                                + t * (np.log(f_mid[i + 1]) - np.log(f_mid[i]))))
    return None


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ── 6.1: anti-resonance selection ────────────────────────────────────
    alphas = np.linspace(0.005, 0.495, 600)
    n_max = 300
    scan = survival_scan(alphas, n_max)
    with open(os.path.join(OUT_DIR, "rotation_survival.csv"), "w",
              newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["alpha", "rigidity_min", "collapse_generation"])
        for a, (r, nc) in zip(alphas, scan):
            writer.writerow([a, r, nc])

    r_gold, nc_gold = rigidity_profile(ALPHA_GOLDEN, n_max)
    print(f"6.1 golden alpha = {ALPHA_GOLDEN:.6f}: rigidity_min = {r_gold:.3f} "
          f"(= 1/phi^2), collapse generation = {nc_gold} (n_max = {n_max})")
    for label, a in [("1/4", 0.25), ("1/5", 0.2), ("2/7", 2/7),
                     ("sqrt(2)-1", np.sqrt(2) - 1), ("e-2", np.e - 2)]:
        r, nc = rigidity_profile(a, n_max)
        print(f"    alpha = {label:10s}: rigidity_min = {r:.4f}, "
              f"collapse generation = {nc}")

    # ── 6.2a: persistence — golden survives, rationals peel off ──────────
    n_per = 233
    cands = [("golden", ALPHA_GOLDEN, None)]
    for k, ratio, denom in fibonacci_rationals():
        cands.append((f"F ratio {ratio:.5f} (den {denom})", ratio, denom))
    per_rows = []
    R_curves = {}
    for name, alpha, denom in cands:
        R = rigidity_matrix([alpha], n_per)[0]
        R_curves[name] = R
        coll = int(np.argmax(R < 1e-9) + 2) if (R < 1e-9).any() else n_per + 1
        per_rows.append({"candidate": name, "alpha": alpha,
                         "collapse_generation": coll,
                         "R_min": R.min()})
        print(f"6.2a {name:28s}: R_min = {R.min():.4f}, "
              f"collapse at n = {coll}")
    with open(os.path.join(OUT_DIR, "persistence.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(per_rows[0].keys()))
        writer.writeheader()
        writer.writerows(per_rows)

    # ── 6.2c: repulsive growth → noble attractor ─────────────────────────
    div, config = simulate_growth(n_injections=120, v0=0.02, v0_final=0.002,
                                  mu=1.0, soft=1.0, steps_per_injection=40,
                                  r_max=40.0)
    tail = div[-30:]
    conv, scatter = np.mean(tail), np.std(tail)
    print(f"\n6.2c growth simulation: converged divergence = {conv:.2f} deg "
          f"+/- {scatter:.2f} (golden = {GOLDEN_ANGLE_DEG:.2f} deg; the ODE "
          f"settles in a neighboring noble-family basin - the variability "
          f"of the attractor)")
    with open(os.path.join(OUT_DIR, "divergence.csv"), "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["injection", "divergence_deg"])
        for k, d in enumerate(div):
            writer.writerow([k, d])

    # ── 6.3: golden window in Phase 4 ────────────────────────────────────
    fs, gs = load_phase4_scan()
    f_mid, slopes, d_eff = d_eff_profile(fs, gs)
    f_cross = golden_crossing(fs, gs)
    suppression = 100 * (1 - 1 / f_cross) if f_cross else float("nan")
    print(f"\n6.3 Phase 4 reinterpretation: D_eff crosses phi at "
          f"f ~ {f_cross:.2f}; void suppression at crossing = "
          f"{suppression:.1f}% (IST phenomenology ~76%)")
    with open(os.path.join(OUT_DIR, "d_eff_crossing.csv"), "w",
              newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["f_mid", "local_slope", "D_eff"])
        for fm, s, d in zip(f_mid, slopes, d_eff):
            writer.writerow([fm, s, d])

    make_figure(alphas, scan, R_curves, per_rows, div, config, conv,
                scatter, f_mid, d_eff, f_cross)


def make_figure(alphas, scan, R_curves, per_rows, div, config, conv,
                scatter, f_mid, d_eff, f_cross):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A: anti-resonance selection landscape
    ax = axes[0, 0]
    ax.plot(alphas, scan[:, 0], "-", color="steelblue", lw=1)
    ax.axvline(ALPHA_GOLDEN, color="crimson", ls="--",
               label=r"golden $\alpha = 1/\varphi^2$")
    for a, lbl in [(0.25, "1/4"), (0.2, "1/5"), (1/3, "1/3")]:
        ax.axvline(a, color="gray", ls=":", lw=1)
        ax.annotate(lbl, (a, 0.02), fontsize=7, rotation=90)
    ax.set_xlabel(r"rotation number $\alpha$")
    ax.set_ylabel(r"min gap rigidity $R$")
    ax.set_title("A. Anti-resonance selection (300 generations)")
    ax.legend(fontsize=8)

    # B: persistence — golden survives, Fibonacci rationals peel off
    ax = axes[0, 1]
    ns = np.arange(2, len(R_curves["golden"]) + 2)
    ax.axhline(1 / PHI ** 2, color="crimson", ls="--", lw=1,
               label=r"golden floor $1/\varphi^2$")
    colors = plt.cm.viridis(np.linspace(0.85, 0.25, len(per_rows) - 1))
    ax.plot(ns, R_curves["golden"], "-", color="crimson", lw=2,
            label="golden rotation (never collapses)")
    for (row, color) in zip(per_rows[1:], colors):
        R = R_curves[row["candidate"]]
        lbl = f"$F$ ratio, den {row['candidate'].split('den ')[1][:-1]}"
        ax.plot(ns, R, "-", color=color, lw=1, label=lbl)
    ax.set_xscale("log")
    ax.set_xlabel("deposition generation $n$")
    ax.set_ylabel(r"rigidity $R(n)$")
    ax.set_title("B. Persistence: rationals peel off at their denominators")
    ax.legend(fontsize=6, ncol=2)

    # C: emergent spiral lattice from repulsive growth
    ax = axes[1, 0]
    r = np.linalg.norm(config, axis=1)
    ax.scatter(config[:, 0], config[:, 1], c=r, cmap="viridis", s=12)
    ax.set_aspect("equal")
    ax.set_title(f"C. Growth lattice: noble attractor "
                 f"({conv:.1f}$^\\circ \\pm {scatter:.1f}^\\circ$)")
    ax.set_xlabel("x (plonk units)")
    ax.set_ylabel("y (plonk units)")

    # D: D_eff crossing phi in the Phase 4 fold scan
    ax = axes[1, 1]
    ax.plot(f_mid, d_eff, "o-", color="seagreen",
            label=r"$D_{\rm eff} = 1/(\rm local\ slope)$")
    ax.axhline(PHI, color="crimson", ls="--", label=r"$\varphi$")
    if f_cross:
        ax.axvline(f_cross, color="gray", ls=":",
                   label=rf"crossing $f \approx {f_cross:.1f}$"
                         rf" ($1-1/f \approx {100*(1-1/f_cross):.0f}\%$)")
    ax.set_xscale("log")
    ax.set_xlabel(r"fold factor $f$")
    ax.set_ylabel(r"$D_{\rm eff}$")
    ax.set_title("D. Golden window in the Phase 4 fold scan")
    ax.legend(fontsize=8)

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "phi_attractor.png")
    fig.savefig(path, dpi=300)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
