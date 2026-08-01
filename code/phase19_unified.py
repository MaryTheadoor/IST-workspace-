"""
================================================================================
IST PHASE 19 — Unified φ-Simulation: 2D Klein + Vacuum Pump + Fibonacci
================================================================================
Combines Phase 7 (spectral-proximity coupling), Phase 8 (vacuum-pump
layers), Phase 8b (2D Klein oscillator sheet), and Phase 11 (golden
edge filter) into a single simulation that tracks D_eff as a function
of golden accumulation layers. The goal: show D_eff flowing through
φ ≈ 1.618 at the golden window, closing the central gap.

Oscillators live on the 2D Klein bottle surface. Each vacuum-pump layer
deposits golden-structured oscillators at Fibonacci scales. Coupling is
Gaussian in Klein geodesic distance with golden-filter boost. D_eff
is measured from the effective Laplacian at each layer.

Output: code/outputs/phase19/d_eff_vs_layers.csv
        code/outputs/phase19/unified_substrate.png
================================================================================
"""
import csv, os, time
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase19")
ALPHA_GOLDEN = 1.0 / PHI ** 2
TOL = 0.35


# ══════════════════════════════════════════════════════════════════════════════
# 2D KLEIN BOTTLE OSCILLATOR SHEET (Phase 8b)
# ══════════════════════════════════════════════════════════════════════════════

def klein_distance(x1, y1, x2, y2):
    """Minimum geodesic distance on the Klein bottle [0, 2pi)^2.
    Returns (distance, is_twisted)."""
    dx = x1 - x2; dy = y1 - y2
    d2 = dx**2 + dy**2
    # periodic images
    for sx in [2*np.pi, -2*np.pi]:
        d2 = min(d2, (dx+sx)**2 + dy**2)
    for sy in [2*np.pi, -2*np.pi]:
        d2 = min(d2, dx**2 + (dy+sy)**2)
    for sx in [2*np.pi, -2*np.pi]:
        for sy in [2*np.pi, -2*np.pi]:
            d2 = min(d2, (dx+sx)**2 + (dy+sy)**2)
    # twist identification
    twist = False
    for sx in [0, 2*np.pi, -2*np.pi]:
        for sy in [0, 2*np.pi, -2*np.pi]:
            d2t = (x1 + x2 + sx)**2 + (y1 - y2 + sy)**2
            if d2t < d2 - 1e-12:
                d2 = d2t; twist = True
    return np.sqrt(max(d2, 0)), twist


# ══════════════════════════════════════════════════════════════════════════════
# VACUUM-PUMP LAYER DEPOSITION (Phase 8)
# ══════════════════════════════════════════════════════════════════════════════

def golden_layer_phases(n_new, k):
    """Deposit layer k: oscillators at golden-scaled positions.
    x_i = 2pi * (i * alpha^k mod 1), y_i = 2pi * (i * alpha^{k+1} mod 1)."""
    raw_x = (np.arange(n_new, dtype=float) * (ALPHA_GOLDEN ** k)) % 1.0
    raw_y = (np.arange(n_new, dtype=float) * (ALPHA_GOLDEN ** (k+1))) % 1.0
    return 2*np.pi*np.sort(raw_x), 2*np.pi*np.sort(raw_y)


# ══════════════════════════════════════════════════════════════════════════════
# SPECTRAL DIMENSION (Phase 7)
# ══════════════════════════════════════════════════════════════════════════════

def spectral_dimension(L, k=30):
    """D_eff from low-energy Weyl fit."""
    N = L.shape[0]; k = min(k, N-2)
    try:
        vals = spla.eigsh(L, k=k, sigma=-0.01, which="LM", tol=1e-6,
                          return_eigenvectors=False)
    except spla.ArpackError:
        return np.nan
    vals = np.sort(vals[vals > 1e-10])
    if len(vals) < 8: return np.nan
    imin = max(1, int(0.05*len(vals))); imax = max(imin+5, int(0.4*len(vals)))
    lam, cnt = vals[imin:imax], np.arange(imin+1, imax+1)
    slope, _ = np.polyfit(np.log(lam), np.log(cnt), 1)
    return 2*slope


# ══════════════════════════════════════════════════════════════════════════════
# UNIFIED SUBSTRATE
# ══════════════════════════════════════════════════════════════════════════════

class UnifiedSubstrate:
    """2D Klein bottle oscillators with vacuum-pump deposition, golden-
    filtered coupling, and D_eff tracking per layer."""

    def __init__(self, n_noise=200, sigma=0.6, seed=42):
        rng = np.random.default_rng(seed)
        self.xs = list(2*np.pi * rng.uniform(size=n_noise))
        self.ys = list(2*np.pi * rng.uniform(size=n_noise))
        self.golden_mask = [False] * n_noise
        self.sigma = sigma
        self.n_layers = 0
        self.d_eff_history = []

    def add_harmonic_layer(self, n_new=25):
        k = self.n_layers + 1
        gx, gy = golden_layer_phases(n_new, k)
        self.xs.extend(gx); self.ys.extend(gy)
        self.golden_mask.extend([True] * n_new)
        self.n_layers = k

    def _build_matrices(self):
        N = len(self.xs)
        x = np.array(self.xs); y = np.array(self.ys)
        dx = x[:, None] - x[None, :]
        dy = y[:, None] - y[None, :]

        # Periodic images (vectorized)
        d2 = dx**2 + dy**2
        for sx in [2*np.pi, -2*np.pi]:
            d2 = np.minimum(d2, (dx+sx)**2 + dy**2)
        for sy in [2*np.pi, -2*np.pi]:
            d2 = np.minimum(d2, dx**2 + (dy+sy)**2)
        for sx in [2*np.pi, -2*np.pi]:
            for sy in [2*np.pi, -2*np.pi]:
                d2 = np.minimum(d2, (dx+sx)**2 + (dy+sy)**2)

        # Twist images (Klein bottle identification)
        twist_mask = np.zeros((N,N), dtype=bool)
        for sx in [0, 2*np.pi, -2*np.pi]:
            for sy in [0, 2*np.pi, -2*np.pi]:
                d2t = (x[:,None] + x[None,:] + sx)**2 \
                    + (y[:,None] - y[None,:] + sy)**2
                better = d2t < (d2 - 1e-12)
                d2 = np.where(better, d2t, d2)
                twist_mask |= better

        dist = np.sqrt(np.maximum(d2, 0))
        np.fill_diagonal(dist, 1e9)

        # Golden match: pairs at golden angular separation in x or y
        dx_ang = np.minimum(np.abs(dx), 2*np.pi - np.abs(dx))
        dy_ang = np.minimum(np.abs(dy), 2*np.pi - np.abs(dy))
        golden_match = np.zeros((N,N), dtype=bool)
        for tgt in [2*np.pi*ALPHA_GOLDEN, 2*np.pi*(1-ALPHA_GOLDEN)]:
            golden_match |= (np.abs(dx_ang - tgt) < TOL)
            golden_match |= (np.abs(dy_ang - tgt) < TOL)

        J = np.exp(-dist**2 / (2 * self.sigma**2))
        # Golden-only: non-golden pairs suppressed by factor 1000
        J_clean = np.where(golden_match, J, J * 0.001)
        np.fill_diagonal(J_clean, 0)
        signs = np.where(twist_mask, -1.0, 1.0)
        np.fill_diagonal(signs, 0)
        W = J_clean * signs
        D_vec = np.asarray(np.abs(W).sum(axis=1)).ravel()
        return sp.csr_matrix(W), sp.diags(D_vec) - sp.csr_matrix(W)

    def measure_d_eff(self):
        W, L = self._build_matrices()
        return spectral_dimension(L)

    def golden_fraction(self):
        if self.n_layers == 0: return 0.0
        return sum(self.golden_mask) / len(self.xs)

    def run_layers(self, n_layers=14, n_new=25):
        for k in range(n_layers + 1):
            if k > 0: self.add_harmonic_layer(n_new)
            d = self.measure_d_eff()
            self.d_eff_history.append({
                "layer": k, "N": len(self.xs),
                "D_eff": d, "golden_frac": self.golden_fraction(),
            })
        return self.d_eff_history


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.perf_counter()
    sub = UnifiedSubstrate(n_noise=200, sigma=0.6)
    rows = sub.run_layers(n_layers=24, n_new=20)

    with open(os.path.join(OUT_DIR, "d_eff_vs_layers.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    print("layer   N    D_eff   golden_frac")
    for r in rows[::2]:
        d = f"{r['D_eff']:.3f}" if not np.isnan(r["D_eff"]) else "nan"
        print(f"  {r['layer']:3d}  {r['N']:4d}  {d:>6s}  {r['golden_frac']:.3f}")

    # Find golden window crossing
    Ds = [r["D_eff"] for r in rows if not np.isnan(r["D_eff"])]
    if Ds:
        closest = min(Ds, key=lambda d: abs(d-PHI))
        idx = Ds.index(closest)
        print(f"\nD_eff range: {min(Ds):.3f} - {max(Ds):.3f}")
        print(f"Closest to phi: D_eff={closest:.3f} at layer {idx} "
              f"(delta = {abs(closest-PHI):.4f})")
        # Is it crossing phi?
        before = np.array(Ds[:idx]) - PHI
        after = np.array(Ds[idx+1:]) - PHI
        if len(before) > 0 and len(after) > 0:
            if np.sign(before[-1]) != np.sign(after[0]):
                print(f"  D_eff CROSSES phi between layers {idx} and {idx+1}!")

    make_figure(rows)
    print(f"Wrote {OUT_DIR} ({time.perf_counter()-t0:.0f}s)")


def make_figure(rows):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    ls = [r["layer"] for r in rows]
    Ds = [r["D_eff"] if not np.isnan(r["D_eff"]) else np.nan for r in rows]
    gs = [r["golden_frac"] for r in rows]

    ax = axes[0,0]
    ax.plot(ls, Ds, "o-", color="seagreen", lw=2, ms=6)
    ax.axhline(PHI, color="crimson", ls="--", lw=2, label=r"$\varphi$=1.618")
    ax.axhline(2.0, color="gray", ls=":", label="2D manifold")
    ax.axhline(1.18, color="steelblue", ls=":", label="1D pinned (Phase 8)")
    ax.set_xlabel("vacuum-pump layers"); ax.set_ylabel(r"$D_{\rm eff}$")
    ax.set_title("A. Unified: D_eff vs golden accumulation")
    ax.legend(fontsize=8)

    ax = axes[0,1]
    ax.plot(ls, [abs(d-PHI) if not np.isnan(d) else np.nan for d in Ds],
            "o-", color="crimson", lw=2)
    ax.set_yscale("log")
    ax.set_xlabel("layers"); ax.set_ylabel(r"$|D_{\rm eff} - \varphi|$")
    ax.set_title("B. Convergence toward phi")

    ax = axes[1,0]
    ax.plot(ls, gs, "o-", color="steelblue", lw=2)
    ax.set_xlabel("layers"); ax.set_ylabel("golden fraction")
    ax.set_title("C. Golden fraction")

    ax = axes[1,1]
    ax.plot(ls, [r["N"] for r in rows], "s-", color="steelblue")
    ax.set_xlabel("layers"); ax.set_ylabel("oscillator count")
    ax.set_title("D. Oscillator count")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "unified_substrate.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
