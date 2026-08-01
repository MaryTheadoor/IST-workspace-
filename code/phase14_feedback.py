"""
================================================================================
IST PHASE 14 - Fold-Density Feedback: Self-Regulating G_eff at Golden Window
================================================================================
Purpose:
    Dynamical feedback mechanism where fold density self-regulates at the
    golden window. The ODE:
        df/dt = gamma * (D_eff(f) - phi) * f
    drives f toward the fixed point where D_eff(f) = phi (f ~ 4.2).
    When D_eff > phi (under-folded), f increases (more golden structure).
    When D_eff < phi (over-folded), f decreases (less saturation).

    D_eff(f) is obtained from the Phase 4 fold-scan data (interpolated).
    The resulting G_eff(f) = f^(1/D_eff(f)) is pinned at the golden-window
    exponent 1/phi at equilibrium.

Inputs:   code/outputs/phase4/geff_vs_rho.csv (Phase 4 fold scan)
Outputs:  code/outputs/phase14/feedback_trajectory.csv
          code/outputs/phase14/feedback_trajectory.png

References:
    IST_Project_Implementation_Plan.md (Priority 4)
    code/phase4_variable_g.py           (Phase 4 fold scan)
    code/phase13_dynamical_rg.py        (dynamical RG, D_eff ~ 1.65)
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase14")


# ───────────────────────────────────────────────────────────────────────────────
# D_eff(f) FROM PHASE 4 FOLD-SCAN DATA
# ───────────────────────────────────────────────────────────────────────────────

def load_phase4_d_eff():
    """Load the Phase 4 fold-scan csv and compute D_eff(f) anchor points."""
    path = os.path.join(os.path.dirname(__file__), "outputs", "phase4",
                        "geff_vs_rho.csv")
    fs, gs = [], []
    with open(path) as fh:
        for row in csv.DictReader(fh):
            fs.append(float(row["fold_factor"]))
            gs.append(float(row["g_eff_norm"]))
    fs = np.array(fs)
    gs = np.array(gs)
    lf, lg = np.log(fs), np.log(gs)
    slopes = np.diff(lg) / np.diff(lf)
    f_mid = np.sqrt(fs[:-1] * fs[1:])
    d_eff = 1.0 / slopes
    return f_mid, d_eff


def d_eff_of_f(f, f_anchors, d_anchors):
    """Interpolate D_eff(f) from Phase 4 data, with asymptotic extension."""
    scalar = np.ndim(f) == 0
    f = np.atleast_1d(np.asarray(f, dtype=float))
    log_f = np.log(f)
    fa_ext = np.concatenate([[1.0], f_anchors, [100.0]])
    da_ext = np.concatenate([[4.5], d_anchors, [1.05]])
    result = np.interp(log_f, np.log(fa_ext), da_ext)
    return float(result[0]) if scalar else result


# ───────────────────────────────────────────────────────────────────────────────
# FEEDBACK ODE
# ───────────────────────────────────────────────────────────────────────────────

def feedback_ode(f, f_anchors, d_anchors, gamma):
    """df/dt = gamma * (D_eff(f) - phi) * f."""
    d = d_eff_of_f(f, f_anchors, d_anchors)
    return gamma * (d - PHI) * f


def integrate_feedback(f0, f_anchors, d_anchors, gamma, dt, n_steps):
    """Euler integration of the fold-density feedback ODE."""
    f = np.empty(n_steps)
    D = np.empty(n_steps)
    G = np.empty(n_steps)
    f[0] = f0
    D[0] = d_eff_of_f(f0, f_anchors, d_anchors)
    G[0] = f0 ** (1.0 / D[0])
    for i in range(n_steps - 1):
        f[i + 1] = f[i] + dt * feedback_ode(f[i], f_anchors, d_anchors, gamma)
        f[i + 1] = np.clip(f[i + 1], 1.0, 20.0)
        D[i + 1] = d_eff_of_f(f[i + 1], f_anchors, d_anchors)
        G[i + 1] = f[i + 1] ** (1.0 / D[i + 1])
    return f, D, G


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    f_anchors, d_anchors = load_phase4_d_eff()

    gamma = 0.3
    dt = 0.02
    n_steps = 1200

    results = {}
    for label, f0 in [("from void (f=1.5)", 1.5),
                      ("from sheet (f=12)", 12.0),
                      ("near golden (f=4)", 4.0)]:
        f, D, G = integrate_feedback(f0, f_anchors, d_anchors,
                                     gamma, dt, n_steps)
        results[label] = (f, D, G)
        print(f"{label:28s}: f = {f0:.1f} -> {f[-1]:.2f}, "
              f"D_eff = {D[0]:.3f} -> {D[-1]:.3f}, "
              f"G exponent = {1/D[0]:.3f} -> {1/D[-1]:.3f}")

    # save trajectory for middle case
    f, D, G = results["near golden (f=4)"]
    with open(os.path.join(OUT_DIR, "feedback_trajectory.csv"), "w",
              newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["t", "f", "D_eff", "G_eff"])
        for i in range(0, n_steps, 20):
            writer.writerow([i * dt, f[i], D[i], G[i]])

    make_figure(results, f_anchors, d_anchors, gamma)
    print(f"Wrote {OUT_DIR}")


def make_figure(results, f_anchors, d_anchors, gamma):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    colors = {"from void (f=1.5)": "steelblue",
              "from sheet (f=12)": "crimson",
              "near golden (f=4)": "seagreen"}

    ax = axes[0, 0]
    f_dense = np.linspace(1.1, 16, 200)
    D_dense = d_eff_of_f(f_dense, f_anchors, d_anchors)
    ax.plot(f_dense, D_dense, "k-", lw=2, label=r"$D_{\rm eff}(f)$ (Phase 4)")
    ax.axhline(PHI, color="gray", ls="--", label=r"$\varphi$")
    ax.axhline(1.65, color="seagreen", ls=":", label="Phase 13 pinned D_eff")
    # fixed point
    f_star = f_dense[np.argmin(np.abs(D_dense - PHI))]
    ax.axvline(f_star, color="gray", ls=":", label=f"f*={f_star:.2f}")
    ax.set_xscale("log")
    ax.set_xlabel("fold density f")
    ax.set_ylabel(r"$D_{\rm eff}$")
    ax.set_title("A. D_eff(f) and golden-window fixed point")
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    for label, (f, D, G) in results.items():
        t = np.arange(len(f)) * 0.02
        ax.plot(t, f, color=colors[label], lw=1.5, label=label)
    ax.axhline(f_star, color="gray", ls="--", label=f"f*={f_star:.2f}")
    ax.set_xlabel("time")
    ax.set_ylabel("fold density f")
    ax.set_title("B. f(t): convergence to golden window")
    ax.legend(fontsize=7)

    ax = axes[1, 0]
    for label, (f, D, G) in results.items():
        ax.plot(D, G, color=colors[label], lw=1.5, marker=".", ms=2,
                label=label, markevery=50)
    # reference power laws
    f_ref = np.linspace(1, 16, 100)
    ax.plot(d_eff_of_f(f_ref, f_anchors, d_anchors),
            f_ref ** (1 / PHI), "k--", lw=1,
            label=r"$G \propto f^{1/\varphi}$")
    ax.set_xlabel(r"$D_{\rm eff}$")
    ax.set_ylabel(r"$G_{\rm eff}$")
    ax.set_xlim(1, 4)
    ax.set_title("C. G_eff vs D_eff: convergence to golden coupling")
    ax.legend(fontsize=7)

    ax = axes[1, 1]
    f_phase = np.linspace(1.1, 16, 200)
    dfdt = feedback_ode(f_phase, f_anchors, d_anchors, gamma)
    ax.plot(f_phase, dfdt, "k-", lw=2, label=r"$df/dt$")
    ax.axhline(0, color="gray", ls=":")
    ax.axvline(f_star, color="gray", ls="--", label=f"f*={f_star:.2f}")
    # mark stable/unstable
    ax.fill_between(f_phase[f_phase < f_star], 0,
                    dfdt[f_phase < f_star], alpha=0.2, color="seagreen",
                    label="attracted upward")
    ax.fill_between(f_phase[f_phase > f_star], 0,
                    dfdt[f_phase > f_star], alpha=0.2, color="crimson",
                    label="attracted downward")
    ax.set_xscale("log")
    ax.set_xlabel("fold density f")
    ax.set_ylabel(r"$df/dt$")
    ax.set_title("D. Phase portrait: stable fixed point")
    ax.legend(fontsize=7)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "feedback_trajectory.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
