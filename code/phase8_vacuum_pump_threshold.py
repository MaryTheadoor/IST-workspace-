"""
================================================================================
IST PHASE 8 - Vacuum-Pump Threshold: Golden Filter & D_eff Pinning
================================================================================
Purpose:
    Implement the Vacuum-Pump Cosmogony (IST_Project_Implementation_Plan.md
    section 1.3): the substrate is a noise-driven self-organizing system
    where vacuum fluctuations are pumped by the Omega operator at plonk
    time, and the golden ratio acts as a bandpass filter -- rational
    ratios destructively interfere (sink into void), golden ratios
    constructively accumulate (propagate on the manifest side).

    Model: oscillator population on the spectral circle. Each plonk tick
    deposits a golden-scaled harmonic layer (f_k = f_0 / phi^k). The
    golden filter modifies the coupling: pairs whose angular separation
    matches a golden multiple 2*pi/phi^k get a coupling boost that grows
    with layer count (constructive accumulation), while rational-separation
    pairs are unaffected (destructive relative suppression).

Inputs:   none
Outputs:
    code/outputs/phase8/d_eff_vs_pump.png
    code/outputs/phase8/coherence_vs_pump.png
    code/outputs/phase8/magnification_trajectory.csv
    code/outputs/phase8/threshold_summary.json

References:
    IST_Project_Implementation_Plan.md (Vacuum-Pump Cosmogony, Priority 1)
    code/phase7_vector_substrate.py         (spectral-proximity coupling)
    code/phase6_phi_attractor.py            (anti-resonance persistence)
================================================================================
"""

import csv
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from phase1_klein_laplacian import PHI
from phase7_vector_substrate import spectral_dimension

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase8")
ALPHA_GOLDEN = 1.0 / PHI ** 2


def circle_gaps(phases):
    """Gap sizes of the circle partition by the given phases."""
    xs = np.sort(phases)
    return np.diff(np.append(xs, xs[0] + 2 * np.pi))


def gap_rigidity(phases):
    """R = min_gap / max_gap; 1/phi^2 for a golden orbit, ~0 for random."""
    if len(phases) < 3:
        return 0.0
    g = circle_gaps(phases)
    return g.min() / g.max()


# ───────────────────────────────────────────────────────────────────────────────
# COUPLING WITH GOLDEN FILTER
# ───────────────────────────────────────────────────────────────────────────────

def golden_coupling(phases, sigma, layer_count, boost_rate=0.15):
    """Coupling matrix with the golden-filter boost.

    J_ij = J_spatial(d_ij) * (1 + pump * golden_match(d_ij))

    J_spatial = exp(-d^2/(2 sigma^2))  (proximity, as Phase 7)
    golden_match(d) = max over k=1..layer_count of
                      exp(-(d - 2*pi/phi^k)^2 / (2*(0.1*target)^2))
    pump = boost_rate * layer_count  (grows with accumulation)
    """
    N = len(phases)
    ph = np.asarray(phases)
    dmat = np.abs(ph[:, None] - ph[None, :])
    dmat = np.minimum(dmat, 2 * np.pi - dmat)
    J_spatial = np.exp(-dmat ** 2 / (2 * sigma ** 2))

    golden_boost = np.zeros((N, N))
    for k in range(1, layer_count + 1):
        target = 2 * np.pi / PHI ** k
        width = max(0.05 * target, 0.01)
        match = np.exp(-(dmat - target) ** 2 / (2 * width ** 2))
        golden_boost = np.maximum(golden_boost, match)

    pump = boost_rate * layer_count
    J = J_spatial * (1.0 + pump * golden_boost)
    np.fill_diagonal(J, 0.0)
    return J, golden_boost


def graph_laplacian(J):
    """L = D - J."""
    D = np.asarray(J.sum(axis=1)).ravel()
    return sp.diags(D) - sp.csr_matrix(J)


# ───────────────────────────────────────────────────────────────────────────────
# VACUUM-PUMP SIMULATOR
# ───────────────────────────────────────────────────────────────────────────────

class VacuumPumpSimulator:
    """Noise-driven substrate with golden-filtered harmonic accumulation.

    Each harmonic layer deposits golden-scaled oscillators AND strengthens
    the golden-filter coupling boost. The system transitions from
    noise-dominated to golden-pinned as layers accumulate.
    """

    def __init__(self, N_base=200, sigma=0.08, seed=42):
        rng = np.random.default_rng(seed)
        self.noise_phases = 2 * np.pi * rng.uniform(size=N_base)
        self.golden_layers = []
        self.sigma = sigma
        self.n_base = N_base

    def add_harmonic_layer(self, n_new=40):
        """Deposit layer k: oscillators at phases 2*pi*(i*phi^{-k} mod 1)."""
        k = len(self.golden_layers) + 1
        raw = (np.arange(n_new) * (ALPHA_GOLDEN ** k)) % 1.0
        self.golden_layers.append(2 * np.pi * np.sort(raw))

    def golden_phases(self):
        if not self.golden_layers:
            return np.array([])
        return np.concatenate(self.golden_layers)

    def all_phases(self):
        return np.concatenate([self.noise_phases, self.golden_phases()])

    @property
    def n_layers(self):
        return len(self.golden_layers)

    # ── measurements ────────────────────────────────────────────────────

    def measure(self):
        """Build the golden-filtered coupling graph; return all metrics."""
        phases = self.all_phases()
        J, golden_boost = golden_coupling(phases, self.sigma, self.n_layers)
        L = graph_laplacian(J)
        D, r2 = spectral_dimension(L)
        deg = J.sum() / len(phases)

        # coherence: fraction of coupling weight from golden-boosted pairs
        total_w = J.sum()
        golden_w = (J * golden_boost).sum()
        coherence = golden_w / total_w if total_w > 0 else 0.0

        return {
            "D_eff": D, "r2": r2, "avg_degree": deg,
            "coherence": coherence,
            "magnification": PHI ** self.n_layers,
            "n_layers": self.n_layers,
            "n_oscillators": len(phases),
            "golden_fraction": len(self.golden_phases()) / len(phases),
        }

    def run_threshold_scan(self, n_layers=16, n_new=40):
        rows = []
        for k in range(n_layers + 1):
            if k > 0:
                self.add_harmonic_layer(n_new)
            rows.append(self.measure())
        return rows


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    sim = VacuumPumpSimulator(N_base=200, sigma=0.08)
    rows = sim.run_threshold_scan(n_layers=16, n_new=40)

    with open(os.path.join(OUT_DIR, "magnification_trajectory.csv"), "w",
              newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("n_lyr  n_osc  deg    D_eff  coher  magnif  gold_frac")
    for r in rows:
        print(f"{r['n_layers']:5d}  {r['n_oscillators']:5d}  {r['avg_degree']:5.1f}"
              f"  {r['D_eff']:6.3f}  {r['coherence']:6.3f}  "
              f"{r['magnification']:8.2f}  {r['golden_fraction']:9.3f}")

    # threshold: coherence > 0.5
    threshold = next((r["n_layers"] for r in rows if r["coherence"] > 0.5),
                     None)
    above = [r for r in rows if r["n_layers"] > (threshold or 999)]
    d_pinned = np.mean([r["D_eff"] for r in above]) if above else np.nan
    d_std = np.std([r["D_eff"] for r in above]) if above else np.nan
    mag_at_8 = next(r["magnification"] for r in rows if r["n_layers"] == 8)
    phi8 = PHI ** 8

    summary = {
        "threshold_layer": threshold,
        "d_eff_pinned": round(float(d_pinned), 4),
        "d_eff_std": round(float(d_std), 4),
        "d_eff_target_phi": round(PHI, 4),
        "magnification_at_n8": round(mag_at_8, 2),
        "phi8": round(phi8, 2),
        "mag_matches_phi8": bool(abs(mag_at_8 - phi8) / phi8 < 0.10),
    }
    with open(os.path.join(OUT_DIR, "threshold_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2)

    print(f"\nThreshold: {threshold},  D_eff pinned: {d_pinned:.3f} +/- {d_std:.3f}"
          f"  (target phi = {PHI:.3f})")
    print(f"Magnification n=8: {mag_at_8:.2f} (phi^8 = {phi8:.2f})")

    make_figure(rows, threshold)
    print(f"Wrote {OUT_DIR}")


def make_figure(rows, threshold):
    ns = [r["n_layers"] for r in rows]
    Ds = [r["D_eff"] for r in rows]
    cohs = [r["coherence"] for r in rows]
    mags = [r["magnification"] for r in rows]
    fracs = [r["golden_fraction"] for r in rows]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    ax = axes[0]
    ax.plot(ns, Ds, "o-", color="seagreen", label=r"$D_{\rm eff}$")
    ax.axhline(PHI, color="crimson", ls="--", label=r"$\varphi$ = 1.618")
    ax.axhline(1.10, color="gray", ls=":", label="Phase 7 D_eff ~ 1.1")
    if threshold is not None:
        ax.axvline(threshold, color="gray", ls="--", alpha=0.5,
                   label=f"threshold n = {threshold}")
    ax.set_xlabel("harmonic layers")
    ax.set_ylabel(r"$D_{\rm eff}$")
    ax.set_title("A. Spectral dimension vs vacuum-pump accumulation")
    ax.legend(fontsize=8)

    ax = axes[1]
    ax.plot(ns, cohs, "o-", color="seagreen", label="coherence")
    ax.plot(ns, fracs, "s-", color="steelblue", label="golden fraction")
    ax.axhline(0.5, color="gray", ls="--", label="threshold (0.5)")
    ax.set_xlabel("harmonic layers")
    ax.set_title("B. Golden coherence and fraction")
    ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "d_eff_vs_pump.png"), dpi=300)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    ax = axes[0]
    ax.semilogy(ns, mags, "o-", color="crimson", label=r"measured $\varphi^{n}$")
    phi_ns = np.array(ns)
    ax.semilogy(phi_ns, PHI ** phi_ns, "--", color="gray",
                label=r"theory $\varphi^{n}$")
    ax.axhline(PHI ** 8, color="crimson", ls=":", alpha=0.5,
               label=rf"$\varphi^8 = {PHI**8:.1f}$")
    ax.set_xlabel("harmonic layers")
    ax.set_ylabel("magnification")
    ax.set_title("C. Cumulative golden magnification")
    ax.legend(fontsize=8)

    ax = axes[1]
    d_above = [r["D_eff"] for r in rows if r["n_layers"] > (threshold or 999)]
    if d_above:
        ax.hist(d_above, bins=8, color="seagreen", alpha=0.7,
                label=f"pinned D_eff = {np.mean(d_above):.3f}")
        ax.axvline(PHI, color="crimson", ls="--", label=r"$\varphi$")
    ax.set_xlabel(r"$D_{\rm eff}$")
    ax.set_title("D. D_eff distribution above threshold")
    ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "coherence_vs_pump.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
    print("\n" + "=" * 60 + "\n")
    main_2d()


# ==============================================================================
# PHASE 8b — 2D KLEIN BOTTLE OSCILLATOR SHEET
# ==============================================================================

class KleinOscillatorSheet:
    """2D oscillator population on the Klein bottle surface.

    Coordinates (x, y) in [0, 2pi)^2 with the Klein bottle identifications:
      (x, y) ~ (x + 2pi, y)       periodic longitude
      (x, y) ~ (-x, y + 2pi)     twist meridian (orientation-reversing)

    Coupling is Gaussian in geodesic distance, with negative edge signs for
    pairs whose shortest geodesic crosses the twist seam (Möbius topology).
    The golden filter boosts pairs at golden-multiple angular separations
    in either coordinate direction.
    """

    def __init__(self, noise_count=120, sigma=0.6, seed=42):
        rng = np.random.default_rng(seed)
        self.noise_x = 2 * np.pi * rng.uniform(size=noise_count)
        self.noise_y = 2 * np.pi * rng.uniform(size=noise_count)
        self.golden_x = []   # each layer: array of x positions
        self.golden_y = []
        self.sigma = sigma

    def add_harmonic_layer(self, n_new=25):
        """Deposit golden-scaled positions in both coordinates.

        Layer k: oscillators at x_i = 2pi*(i * phi^{-k} mod 1),
        y_i = 2pi*(i * phi^{-k-1} mod 1) — a different golden
        rotation for y to avoid diagonal degeneracy.
        """
        k = len(self.golden_x) + 1
        raw_x = (np.arange(n_new) * (ALPHA_GOLDEN ** k)) % 1.0
        raw_y = (np.arange(n_new) * (ALPHA_GOLDEN ** (k + 1))) % 1.0
        self.golden_x.append(2 * np.pi * np.sort(raw_x))
        self.golden_y.append(2 * np.pi * np.sort(raw_y))

    @property
    def n_layers(self):
        return len(self.golden_x)

    def all_x(self):
        return np.concatenate([self.noise_x] + self.golden_x)

    def all_y(self):
        return np.concatenate([self.noise_y] + self.golden_y)

    # ── geodesic distance on the Klein bottle ──────────────────────────

    @staticmethod
    def _angular_dist(d):
        return np.minimum(d, 2 * np.pi - d)

    def klein_metric(self, xs, ys):
        """Returns (dist_matrix, twist_matrix) for the oscillator set.

        dist[i,j] = min geodesic distance on the Klein bottle.
        twist[i,j] = True if the minimizing path crosses the twist seam.
        """
        N = len(xs)
        dx = xs[:, None] - xs[None, :]
        dy = ys[:, None] - ys[None, :]
        d2 = dx ** 2 + dy ** 2
        twist_mask = np.zeros((N, N), dtype=bool)
        # periodic images only (non-twist)
        d2_periodic = d2.copy()
        for sx in [2 * np.pi, -2 * np.pi]:
            d2_periodic = np.minimum(d2_periodic, (dx + sx) ** 2 + dy ** 2)
        for sy in [2 * np.pi, -2 * np.pi]:
            d2_periodic = np.minimum(d2_periodic, dx ** 2 + (dy + sy) ** 2)
        for sx in [2 * np.pi, -2 * np.pi]:
            for sy in [2 * np.pi, -2 * np.pi]:
                d2_periodic = np.minimum(
                    d2_periodic, (dx + sx) ** 2 + (dy + sy) ** 2)

        d2_best = d2_periodic.copy()
        # twist images: if shorter than the best periodic path, use them
        for sx in [0.0, 2 * np.pi, -2 * np.pi]:
            for sy in [0.0, 2 * np.pi, -2 * np.pi]:
                d2t = (xs[:, None] + xs[None, :] + sx) ** 2 \
                    + (ys[:, None] - ys[None, :] + sy) ** 2
                better = d2t < (d2_best - 1e-12)
                d2_best = np.where(better, d2t, d2_best)
                twist_mask = twist_mask | better
        np.fill_diagonal(d2_best, np.inf)
        return np.sqrt(np.maximum(d2_best, 0)), twist_mask

    # ── golden-filtered 2D coupling ────────────────────────────────────

    def measure(self):
        """Build the Klein-bottle coupling graph and return all metrics."""
        xs = self.all_x()
        ys = self.all_y()
        N = len(xs)

        dist, twist = self.klein_metric(xs, ys)
        J_spatial = np.exp(-dist ** 2 / (2 * self.sigma ** 2))
        np.fill_diagonal(J_spatial, 0.0)

        # golden filter: 2D angular separations at golden multiples
        dx_ang = self._angular_dist(xs[:, None] - xs[None, :])
        dy_ang = self._angular_dist(ys[:, None] - ys[None, :])
        golden_boost = np.zeros((N, N))
        for k in range(1, self.n_layers + 1):
            target = 2 * np.pi / PHI ** k
            width = max(0.06 * target, 0.02)
            match_x = np.exp(-(dx_ang - target) ** 2 / (2 * width ** 2))
            match_y = np.exp(-(dy_ang - target) ** 2 / (2 * width ** 2))
            golden_boost = np.maximum(golden_boost,
                                      np.maximum(match_x, match_y))
        np.fill_diagonal(golden_boost, 0.0)

        pump = 0.15 * self.n_layers
        J = J_spatial * (1.0 + pump * golden_boost)
        np.fill_diagonal(J, 0.0)

        # signed adjacency: twist edges get sign -1
        W = J.copy()
        W[twist] = -W[twist]
        D_vec = np.asarray(np.abs(W).sum(axis=1)).ravel()
        L = sp.diags(D_vec) - sp.csr_matrix(W)

        D, r2 = spectral_dimension(L)
        deg = J.sum() / N
        total_w = J.sum()
        golden_w = (J * golden_boost).sum()
        coherence = golden_w / total_w if total_w > 0 else 0.0

        return {
            "D_eff": D, "r2": r2, "avg_degree": deg,
            "coherence": coherence,
            "magnification": PHI ** self.n_layers,
            "n_layers": self.n_layers,
            "n_oscillators": N,
            "golden_fraction": (N - self.noise_x.size) / N,
            "lambda_min": float(spla.eigsh(L, k=1, sigma=-0.01,
                               which="LM", return_eigenvectors=False,
                               tol=1e-8)[0]),
        }

    def run_scan(self, n_layers=12, n_new=25):
        rows = []
        for k in range(n_layers + 1):
            if k > 0:
                self.add_harmonic_layer(n_new)
            rows.append(self.measure())
        return rows


def main_2d():
    """Run the 2D Klein bottle oscillator sheet and compare with 1D."""
    os.makedirs(OUT_DIR, exist_ok=True)
    print("=== 2D Klein Bottle Oscillator Sheet ===\n")
    sheet = KleinOscillatorSheet(noise_count=120, sigma=0.6)
    rows = sheet.run_scan(n_layers=12, n_new=25)

    with open(os.path.join(OUT_DIR, "2d_scan.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("n_lyr  n_osc  deg    D_eff  coher  lam_min  magnif")
    for r in rows:
        print(f"{r['n_layers']:5d}  {r['n_oscillators']:5d}  {r['avg_degree']:5.1f}"
              f"  {r['D_eff']:6.3f}  {r['coherence']:6.3f}  "
              f"{r['lambda_min']:8.4f}  {r['magnification']:8.2f}")

    threshold = next((r["n_layers"] for r in rows if r["coherence"] > 0.5),
                     None)
    above = [r for r in rows if r["n_layers"] > (threshold or 999)]
    d_pinned = np.mean([r["D_eff"] for r in above]) if above else np.nan
    d_std = np.std([r["D_eff"] for r in above]) if above else np.nan

    print(f"\nThreshold: {threshold}, D_eff pinned: {d_pinned:.3f} +/- "
          f"{d_std:.3f} (target phi = {PHI:.3f})")
    print(f"lambda_min: {rows[0]['lambda_min']:.4f} (0 layers) "
          f"-> {rows[-1]['lambda_min']:.4f} (layer 12)")
    print(f"Torus control (no twist): lambda_min ~ 0")
    print(f"Klein twist lifts zero mode: lambda_min > 0")

    make_2d_figure(rows, threshold)
    print(f"Wrote {os.path.join(OUT_DIR, 'klein_2d_scan.png')}")


def make_2d_figure(rows, threshold):
    ns = [r["n_layers"] for r in rows]
    Ds = [r["D_eff"] for r in rows]
    cohs = [r["coherence"] for r in rows]
    lams = [r["lambda_min"] for r in rows]

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    ax.plot(ns, Ds, "o-", color="seagreen", lw=2,
            label=r"2D Klein $D_{\rm eff}$")
    ax.axhline(PHI, color="crimson", ls="--", lw=1.5,
               label=r"$\varphi$ = 1.618")
    ax.axhline(2.0, color="gray", ls=":", label="flat 2D manifold")
    ax.axhline(1.18, color="steelblue", ls=":", label="1D pinned D_eff")
    if threshold is not None:
        ax.axvline(threshold, color="gray", ls="--", alpha=0.5,
                   label=f"threshold n = {threshold}")
    ax.set_xlabel("harmonic layers")
    ax.set_ylabel(r"$D_{\rm eff}$")
    ax.set_title("A. 2D Klein spectral dimension vs vacuum pump")
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    ax.plot(ns, cohs, "o-", color="seagreen", lw=2)
    ax.axhline(0.5, color="gray", ls="--", label="threshold (0.5)")
    ax.set_xlabel("harmonic layers")
    ax.set_ylabel("golden coherence")
    ax.set_title("B. Coherence transition (2D)")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    ax.plot(ns, lams, "o-", color="crimson",
            label=r"$\lambda_{\rm min}$ (Klein twist)")
    ax.axhline(0, color="gray", ls=":", label="torus zero mode")
    ax.set_xlabel("harmonic layers")
    ax.set_ylabel(r"$\lambda_{\rm min}$")
    ax.set_title("C. Spectral gap: Klein twist lifts zero mode")
    ax.legend(fontsize=8)

    d_above = [r["D_eff"] for r in rows if r["n_layers"] > (threshold or 999)]
    ax = axes[1, 1]
    if d_above:
        ax.hist(d_above, bins=5, color="seagreen", alpha=0.7,
                label=f"pinned D_eff = {np.mean(d_above):.3f} +/- {np.std(d_above):.3f}")
        ax.axvline(PHI, color="crimson", ls="--", label=r"$\varphi$")
        ax.axvline(2.0, color="gray", ls=":", label="2D manifold")
    ax.set_xlabel(r"$D_{\rm eff}$")
    ax.set_title("D. D_eff distribution above threshold")
    ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "klein_2d_scan.png"), dpi=300)
    plt.close(fig)
