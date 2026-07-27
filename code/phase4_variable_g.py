
"""
================================================================================
IST PHASE 4 - G from the Compression Spectrum
================================================================================
Purpose:
    Treat the Compression Operator Psi (v5.3 Eq. 1) as a linear operator on
    the substrate state space, compute its decay spectrum, and identify the
    slowest mode with the gravitational time scale (fold latency). Then build
    a sheet/void fold-density landscape and measure how the effective
    coupling G_eff varies with fold density, testing the IST scaling
    G_eff ~ rho_fold^{1/phi} against what the local substrate realizes.

Inputs:   none (grid size, band geometry, and fold scan are module constants)
Outputs:
    code/outputs/phase4/decay_spectrum.csv    - slowest decay rates, Klein/torus
    code/outputs/phase4/geff_vs_rho.csv       - fold scan: tau, G_eff, regions
    code/outputs/phase4/crossing_time.csv     - nonlinear latency measurement
    code/outputs/phase4/geff_vs_rho.png       - 4-panel summary (300 DPI)

References:
    notes/IST_Research_Plan_Phases_1-5.md   (Phase 4.1-4.3)
    main/ist_v5_3_topology_substrate.md     (sec. 2.3 Psi, sec. 3.2 latency,
                                             sec. 3.5 G ~ rho^{1/D})
    code/phase1_klein_laplacian.py          (substrate graph + Laplacian)
    code/ist_toolkit_v2.py                  (RGFlowSimulator.effective_coupling)

Conventions:
    * Update map (v5.3 sec. 2.3): s_i(t+1) = U_i(theta) tanh(sum_j J_ij s_j).
      Sequential fold updating: a vertex inside an f-fold region advances by
      1/f of a full relaxation step per plonk tick (f sheets are updated
      sequentially), so the explicit map is
          s(t+1) = s(t) + F^{-1} [ tanh(W_norm s(t)) - s(t) ],
      with W_norm = W/4 the degree-normalized signed adjacency and
      F = diag(f_i) the fold field (f_i >= 1).
    * Linearizing at the flat equilibrium s* = 0 (sech^2(0) = 1):
          M_Psi = I - (1/4) F^{-1} L ,
      so mu_k = 1 - gamma_k/4 where gamma_k solves the generalized problem
          L v = gamma F v .
      gamma_k is real and nonnegative (F^{-1/2} L F^{-1/2} is symmetric PSD).
      For uniform fold f == 1, gamma_k = lambda_k, the Phase 1 Laplacian
      spectrum.
    * Slowest mode: gamma_min = smallest gamma. Relaxation rate per tick is
      r = -ln(1 - gamma_min/4) ~ gamma_min/4, hence
          tau_fold = 4 / gamma_min ,   G_eff proportional to tau_fold .
      Torus control: gamma_min = 0 (constant section) -> tau_fold infinite;
      the Klein twist lifts the zero mode (lambda_min = 4 sin^2(pi/2n) > 0),
      so non-orientability is the substrate's infrared regulator.
    * Fold density rho_fold of a region = mean fold field in the region
      (sheets per plonk cell). IST target exponent: G ~ rho^{1/phi} with
      1/phi ~ 0.618; Phase 1.3's measured D_eff = 2 would give rho^{1/2}.
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from phase1_klein_laplacian import (
    PHI, build_klein_bottle_graph, build_torus_graph
)

N_GRID = 64                     # default grid: 64 x 64, N = 4096
BAND_HALF_WIDTH = 4             # sheet band rows [n/2 - w, n/2 + w)
FOLD_SCAN = [1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0]
OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase4")

TARGET_EXPONENT = 1.0 / PHI     # IST prediction: G ~ rho^{1/phi} ~ rho^0.618
D2_EXPONENT = 0.5               # what Phase 1.3's D_eff = 2 would imply
ZERO_TOL = 1e-10


# ───────────────────────────────────────────────────────────────────────────────
# FOLDED SUBSTRATE & DECAY SPECTRUM (Phase 4.1-4.2)
# ───────────────────────────────────────────────────────────────────────────────

class FoldedSubstrate:
    """Klein bottle (or torus control) substrate with a fold-density field.

    The fold field f_i >= 1 counts weave sheets stacked at vertex i (fold
    density in sheets per plonk cell). A central band of rows carries
    fold_factor; the void background carries f = 1.
    """

    def __init__(self, n, twisted=True, band=None, fold_factor=1.0):
        if n < 8:
            raise ValueError("grid too small; need n >= 8")
        build = build_klein_bottle_graph if twisted else build_torus_graph
        self.graph = build(n, n)
        self.n = n
        self.twisted = twisted
        self.band = band
        self.fold_factor = fold_factor

        fold = np.ones(n * n)
        if band is not None:
            fold[self.band_mask()] = fold_factor
        self.fold = fold

        self.L = self.graph.laplacian()
        # Symmetric form of the decay operator F^{-1} L:
        # L v = gamma F v  <=>  F^{-1/2} L F^{-1/2} w = gamma w
        finv_sqrt = sp.diags(1.0 / np.sqrt(fold))
        self.S = (finv_sqrt @ self.L @ finv_sqrt).tocsr()
        self.W_norm = self.graph.W / 4.0

    def band_mask(self):
        """Vertex mask of the central sheet band."""
        if self.band is None:
            return np.zeros(self.n * self.n, dtype=bool)
        j0, j1 = self.band
        j = self.graph.coords[:, 1]
        return (j >= j0) & (j < j1)

    def void_window(self):
        """Vertex mask of a void comparison window: same size as the band,
        adjacent to it, so regional latencies compare equal-size patches."""
        if self.band is None:
            return np.zeros(self.n * self.n, dtype=bool)
        j0, j1 = self.band
        w = j1 - j0
        j = self.graph.coords[:, 1]
        return (j >= j0 - w) & (j < j0)

    # ── Spectra ──────────────────────────────────────────────────────────

    def decay_spectrum(self, k=8, return_eigenvectors=False):
        """Smallest k generalized decay rates gamma_k (L v = gamma F v)."""
        k = min(k, self.S.shape[0] - 2)
        out = spla.eigsh(self.S, k=k, sigma=-1e-6, which="LM", tol=1e-12,
                         return_eigenvectors=return_eigenvectors)
        if return_eigenvectors:
            vals, vecs = out
            order = np.argsort(vals)
            return vals[order], vecs[:, order]
        return np.sort(out)

    def mu_spectrum(self, k=8):
        """Eigenvalues mu_k = 1 - gamma_k/4 of the linearized Psi map."""
        return 1.0 - self.decay_spectrum(k) / 4.0

    def gamma_min(self):
        """Slowest decay rate (smallest gamma). Zero for the torus."""
        return max(self.decay_spectrum(k=2)[0], 0.0)

    def tau_fold(self):
        """Fold latency tau = 4 / gamma_min (inf if gamma_min ~ 0)."""
        g = self.gamma_min()
        return np.inf if g < ZERO_TOL else 4.0 / g

    def slowest_mode_profile(self):
        """Physical slowest mode v = F^{-1/2} w reshaped to the grid."""
        _, vecs = self.decay_spectrum(k=1, return_eigenvectors=True)
        w = vecs[:, 0]
        v = w / np.sqrt(self.fold)
        return (v / np.max(np.abs(v))).reshape(self.n, self.n)

    def regional_tau(self, mask):
        """Fold latency of a sub-region: smallest Dirichlet eigenvalue of
        the decay operator restricted to the masked vertices."""
        idx = np.flatnonzero(mask)
        if len(idx) < 4:
            raise ValueError("region too small for a Dirichlet spectrum")
        S_sub = self.S[idx][:, idx]
        k = min(4, len(idx) - 2)
        g = spla.eigsh(S_sub, k=k, sigma=-1e-6, which="LM", tol=1e-12,
                       return_eigenvectors=False)
        g_min = max(np.sort(g)[0], 0.0)
        return np.inf if g_min < ZERO_TOL else 4.0 / g_min

    # ── Nonlinear Psi dynamics (validation of the linear theory) ─────────

    def psi_step(self, s):
        """One tick of the explicit map s + F^{-1}(tanh(W_norm s) - s)."""
        return s + (np.tanh(self.W_norm @ s) - s) / self.fold


def central_band(n, half_width=BAND_HALF_WIDTH):
    """Rows [n/2 - w, n/2 + w) of the central sheet."""
    return (n // 2 - half_width, n // 2 + half_width)


def g_eff_normalized(fold_scan, taus):
    """G_eff(f) normalized to the void value f = 1 (G proportional to tau)."""
    taus = np.asarray(taus, dtype=float)
    return taus / taus[0]


def fit_loglog_exponent(rhos, g_values):
    """Least-squares slope of log G vs log rho (the measured 1/D)."""
    x = np.log(np.asarray(rhos, dtype=float))
    y = np.log(np.asarray(g_values, dtype=float))
    slope, _ = np.polyfit(x, y, 1)
    return slope


# ───────────────────────────────────────────────────────────────────────────────
# NONLINEAR VALIDATION (Phase 4.2): decay and crossing-time measurements
# ───────────────────────────────────────────────────────────────────────────────

def simulate_decay(sub, s0, n_steps, projector=None):
    """Run the nonlinear Psi map and return an amplitude history.

    Without a projector, records the L2 norm ||s(t)||. With a projector
    (unit vector, e.g. the slowest mode), records |<projector, s(t)>| —
    isolating a single modal decay rate from the multi-scale relaxation.
    """
    s = s0.copy()
    amps = np.empty(n_steps)
    for t in range(n_steps):
        amps[t] = np.linalg.norm(s) if projector is None \
            else abs(projector @ s)
        s = sub.psi_step(s)
    return amps


def fit_relaxation_time(times, norms, frac_start=0.5):
    """Fit tau from the late-time log-slope of ||s(t)|| (slowest mode)."""
    i0 = int(frac_start * len(times))
    slope, _ = np.polyfit(times[i0:], np.log(norms[i0:]), 1)
    return -1.0 / slope


def crossing_time(sub, n_steps, threshold=1e-3):
    """Latency measurement: a ring perturbation uniform along the longitude
    is placed on the row just below the band; return the first tick at which
    the row just above the band reaches `threshold` of the initial
    amplitude, or np.nan if it never does. The ring's longitudinal
    translation symmetry (preserved by the glide-reflection seam) reduces
    the dynamics to meridian diffusion, so this measures the update depth
    required for information to cross the fold structure.
    """
    n = sub.n
    j0, j1 = sub.band
    s = np.zeros(n * n)
    s[sub.graph.coords[:, 1] == j0 - 1] = 1.0
    detect = np.flatnonzero(sub.graph.coords[:, 1] == j1)
    peak = 1.0
    for t in range(n_steps):
        s = sub.psi_step(s)
        if np.max(np.abs(s[detect])) >= threshold * peak:
            return t + 1
    return np.nan


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER (Phase 4.3): sheet/void scan and exponent measurement
# ───────────────────────────────────────────────────────────────────────────────

def run_scan(n=N_GRID, fold_scan=FOLD_SCAN, twisted=True):
    """Scan fold factor of the central band; record latency and G_eff."""
    rows = []
    for f in fold_scan:
        sub = FoldedSubstrate(n, twisted=twisted, band=central_band(n),
                              fold_factor=f)
        tau = sub.tau_fold()
        tau_sheet = sub.regional_tau(sub.band_mask())
        tau_void = sub.regional_tau(sub.void_window())
        rows.append({
            "fold_factor": f,
            "gamma_min": sub.gamma_min(),
            "tau_fold": tau,
            "tau_sheet": tau_sheet,
            "tau_void": tau_void,
        })
    taus = [r["tau_fold"] for r in rows]
    g_norm = g_eff_normalized(fold_scan, taus)
    for r, g in zip(rows, g_norm):
        r["g_eff_norm"] = g
        r["g_sheet_over_void"] = r["tau_sheet"] / r["tau_void"]
    return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    n = N_GRID

    # ── 4.2: slowest mode, Klein vs torus control ────────────────────────
    klein_flat = FoldedSubstrate(n, twisted=True)
    torus_flat = FoldedSubstrate(n, twisted=False)
    g_klein = klein_flat.gamma_min()
    g_torus = torus_flat.gamma_min()
    print("Slowest mode (flat substrate, f = 1):")
    print(f"  Klein: gamma_min = {g_klein:.6e}   "
          f"tau_fold = {klein_flat.tau_fold():.1f} ticks")
    print(f"  Torus: gamma_min = {g_torus:.6e}   "
          f"tau_fold = {torus_flat.tau_fold()}  (IR divergent)")
    print(f"  analytic Klein gap 4 sin^2(pi/2n)  = {4*np.sin(np.pi/(2*n))**2:.6e}")

    with open(os.path.join(OUT_DIR, "decay_spectrum.csv"), "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["k", "gamma_klein", "gamma_torus"])
        gk = klein_flat.decay_spectrum(k=20)
        gt = torus_flat.decay_spectrum(k=20)
        for k in range(20):
            writer.writerow([k, gk[k], gt[k]])
    print(f"Wrote {os.path.join(OUT_DIR, 'decay_spectrum.csv')}")

    # ── 4.3: fold scan, sheet vs void ────────────────────────────────────
    rows = run_scan(n)
    exponent = fit_loglog_exponent([r["fold_factor"] for r in rows],
                                   [r["g_eff_norm"] for r in rows])
    # Asymptotic check: local slope between the two largest fold factors
    asym = fit_loglog_exponent([rows[-2]["fold_factor"], rows[-1]["fold_factor"]],
                               [rows[-2]["g_eff_norm"], rows[-1]["g_eff_norm"]])
    suppression = 100.0 * (1.0 - 1.0 / rows[-1]["g_sheet_over_void"])

    with open(os.path.join(OUT_DIR, "geff_vs_rho.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {os.path.join(OUT_DIR, 'geff_vs_rho.csv')}")

    print("\nFold scan (central band, Klein):")
    print("    f   |  gamma_min  |  tau_fold |  G/G_void | sheet/void")
    for r in rows:
        print(f"  {r['fold_factor']:5.1f} | {r['gamma_min']:.6e} | "
              f"{r['tau_fold']:9.1f} | {r['g_eff_norm']:8.3f} | "
              f"{r['g_sheet_over_void']:7.3f}")
    print(f"\nMeasured exponent d log G / d log rho = {exponent:.3f}")
    print(f"  IST target 1/phi = {TARGET_EXPONENT:.3f}; "
          f"D = 2 prediction   = {D2_EXPONENT:.3f}")
    print(f"  asymptotic local slope (f = 12 -> 16) = {asym:.3f}")
    print(f"  void suppression at f = 16: {suppression:.1f}% "
          f"(IST phenomenology ~ 76%)")

    # ── Nonlinear validation: crossing time through the band ─────────────
    cross_rows = []
    for f in [1.0, 2.0, 4.0, 8.0, 16.0]:
        sub = FoldedSubstrate(n, twisted=True, band=central_band(n),
                              fold_factor=f)
        t_cross = crossing_time(sub, n_steps=20000)
        cross_rows.append({"fold_factor": f, "t_cross": t_cross})
        print(f"  crossing time f = {f:5.1f}: {t_cross}")
    t0 = cross_rows[0]["t_cross"]
    for r in cross_rows:
        r["g_eff_cross"] = r["t_cross"] / t0
    with open(os.path.join(OUT_DIR, "crossing_time.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(cross_rows[0].keys()))
        writer.writeheader()
        writer.writerows(cross_rows)
    print(f"Wrote {os.path.join(OUT_DIR, 'crossing_time.csv')}")

    # Nonlinear decay at f = 4: fitted tau vs linear prediction. Projecting
    # the nonlinear trajectory onto the slowest mode isolates gamma_min from
    # faster modes (the raw norm is contaminated at the ~30% level by the
    # second mode on this grid). Initial condition: slowest mode plus small
    # noise, so the projection stays positive on the semilog plot.
    sub4 = FoldedSubstrate(n, twisted=True, band=central_band(n), fold_factor=4.0)
    tau_pred = sub4.tau_fold()
    _, vecs = sub4.decay_spectrum(k=1, return_eigenvectors=True)
    v_slow = vecs[:, 0] / np.sqrt(sub4.fold)
    v_slow = v_slow / np.linalg.norm(v_slow)
    n_steps = int(3 * tau_pred)
    rng = np.random.default_rng(7)
    s0 = v_slow + 0.02 * rng.normal(size=n * n)
    amps = simulate_decay(sub4, s0, n_steps, projector=v_slow)
    times = np.arange(n_steps)
    tau_num = fit_relaxation_time(times, amps, frac_start=0.3)
    print(f"\nNonlinear decay (f = 4): tau_pred = {tau_pred:.1f}, "
          f"tau_num = {tau_num:.1f} ({100*tau_num/tau_pred:.1f}%)")

    make_figure(klein_flat, torus_flat, rows, exponent, asym,
                cross_rows, sub4, times, amps, tau_pred)


def make_figure(klein_flat, torus_flat, rows, exponent, asym,
                cross_rows, sub4, times, amps, tau_pred):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A: decay spectra, Klein vs torus
    ax = axes[0, 0]
    gk = klein_flat.decay_spectrum(k=20)
    gt = torus_flat.decay_spectrum(k=20)
    ax.plot(np.arange(20), gk, "o-", color="crimson",
            label=f"Klein ($\\gamma_{{min}}$ = {gk[0]:.2e})")
    ax.plot(np.arange(20), gt, "s-", color="steelblue",
            label=f"Torus ($\\gamma_{{min}}$ = {gt[0]:.1e})")
    ax.set_xlabel(r"mode index $k$")
    ax.set_ylabel(r"decay rate $\gamma_k$")
    ax.set_title("A. Compression spectrum: twist lifts the zero mode")
    ax.legend(fontsize=8)

    # B: G_eff vs fold density (modal latency + crossing-time cross-check)
    ax = axes[0, 1]
    fs = np.array([r["fold_factor"] for r in rows])
    gs = np.array([r["g_eff_norm"] for r in rows])
    ax.loglog(fs, gs, "o-", color="crimson",
              label=f"modal latency (slope {exponent:.3f})")
    cf = np.array([r["fold_factor"] for r in cross_rows], dtype=float)
    cg = np.array([r["g_eff_cross"] for r in cross_rows])
    c_slope = fit_loglog_exponent(cf, cg)
    ax.loglog(cf, cg, "^--", color="seagreen",
              label=f"crossing time (slope {c_slope:.3f})")
    rho = np.linspace(1, 16, 100)
    ax.loglog(rho, rho ** TARGET_EXPONENT, "--", color="gray",
              label=r"IST target $\rho^{1/\varphi}$ (0.618)")
    ax.loglog(rho, rho ** D2_EXPONENT, ":", color="steelblue",
              label=r"$D=2$: $\rho^{1/2}$")
    ax.loglog(rho, rho, "-.", color="k", alpha=0.4,
              label=r"asymptotic $\rho^{1}$")
    ax.set_xlabel(r"fold density $\rho_{\rm fold}$ (sheets per cell)")
    ax.set_ylabel(r"$G_{\rm eff} / G_{\rm void}$")
    ax.set_title("B. Effective coupling vs fold density")
    ax.legend(fontsize=8)

    # C: slowest-mode profile in the sheet/void landscape (f = 4)
    ax = axes[1, 0]
    profile = sub4.slowest_mode_profile()
    im = ax.imshow(np.abs(profile), origin="lower", cmap="inferno")
    n = sub4.n
    j0, j1 = sub4.band
    ax.axhline(j0 - 0.5, color="cyan", ls="--", lw=1)
    ax.axhline(j1 - 0.5, color="cyan", ls="--", lw=1)
    ax.set_title(f"C. Slowest mode $|$v$|$ (band f = {sub4.fold_factor:g})")
    ax.set_xlabel("longitude $i$")
    ax.set_ylabel("meridian $j$")
    fig.colorbar(im, ax=ax, fraction=0.046)

    # D: nonlinear validation — slowest-mode decay vs linear prediction
    ax = axes[1, 1]
    ax.semilogy(times, amps, "-", color="crimson", lw=1,
                label=r"nonlinear $|\langle v_1, s(t)\rangle|$ (f = 4)")
    ax.semilogy(times, amps[0] * np.exp(-times / tau_pred), "--",
                color="gray", label=rf"linear prediction $\tau = {tau_pred:.0f}$")
    ax.set_xlabel(r"plonk tick $t$")
    ax.set_ylabel(r"slowest-mode amplitude")
    ax.legend(fontsize=8, loc="upper right")
    ax.set_title("D. Nonlinear validation of the linearized decay")

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "geff_vs_rho.png")
    fig.savefig(path, dpi=300)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
