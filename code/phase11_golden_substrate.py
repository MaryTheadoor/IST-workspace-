"""
================================================================================
IST PHASE 11 - Golden-Filtered Klein Vector Substrate
================================================================================
Purpose:
    Integrate the Phase 8 vacuum-pump golden filter into the Phase 10
    Klein vector substrate. Each of the 4 neighbour edges per cell has
    a dynamic coupling weight determined by the golden-ratio phase filter:

      * golden-resonant (separation ~137.5 deg) -> weight = 1.0
      * neutral (neither golden nor rational)    -> weight = 0.3
      * rational (p/q for q <= 5)                -> weight = 0.0

    Every cell's phase rotates by the golden angle 2pi/phi^2 per plonk
    tick (the golden attractor). The weighted, signed neighbour sum
    drives the directed-number cross-component dynamics (up/down
    competition, zero absorption). The golden weights create structured
    coupling patterns that select for golden-phase configurations over
    time -- the vacuum-pump's frequency-domain selection operating on
    the full 2D Klein vector field.

    Architecture: GPU-ready (all array ops; single-function update).
    When CuPy is available, swap `np` -> `cp` and the same code runs.

Inputs:   none
Outputs:  code/outputs/phase11/golden_field_evolution.png
          code/outputs/phase11/golden_substrate_trajectory.csv

References:
    code/phase10_gpu_substrate.py           (base vector substrate)
    code/phase8_vacuum_pump_threshold.py    (golden filter)
    code/phase6_phi_attractor.py            (golden rotation)
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import label

from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase11")
ALPHA_GOLDEN = 1.0 / PHI ** 2
TOL = 0.35


# ───────────────────────────────────────────────────────────────────────────────
# GOLDEN-FILTERED KLEIN VECTOR SUBSTRATE
# ───────────────────────────────────────────────────────────────────────────────

class KleinGoldenSubstrate:
    """2D vector field on the Klein bottle with per-edge golden-filter coupling.

    State: (n, n, 3) directed-number amplitudes.
    Phase: (n,) continuous golden-angle rotation per tick.
    Update: s(t+1) = tanh(W_golden(t) @ s(t) + noise)
    """

    def __init__(self, n=128, noise_std=0.015, gain=0.8, seed=1):
        self.n = n
        self.noise_std = noise_std
        self.gain = gain
        rng = np.random.default_rng(seed)

        self.state = rng.random((n, n, 3)) / 2.0
        # initial phases: random, the golden attractor creates resonance over time
        self.phase = 2 * np.pi * rng.random((n, n))
        self.step_count = 0

    # ── golden weight computation (per-edge) ────────────────────────────

    def _phase_diff(self, a, b):
        """Angular separation on [0, 2pi)."""
        d = np.abs(a - b)
        return np.minimum(d, 2 * np.pi - d)

    def _gold_weight(self, d_phase):
        """Coupling weight: 1.0 golden, 0.3 default, 0.0 rational.
        Golden check runs LAST so it cannot be overwritten by rational."""
        w = np.full_like(d_phase, 0.3)
        for p, q in [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4),
                     (1, 5), (2, 5), (3, 5), (4, 5)]:
            w[np.abs(d_phase - 2 * np.pi * p / q) < TOL] = 0.0
        for tgt in [2 * np.pi * ALPHA_GOLDEN,
                    2 * np.pi * (1 - ALPHA_GOLDEN)]:
            w[np.abs(d_phase - tgt) < TOL] = 1.0
        return w

    def _edge_weights(self):
        """Compute the 4 directional weight matrices for the current phases."""
        p = self.phase
        n = self.n
        # right / left (periodic x)
        w_r = self._gold_weight(self._phase_diff(p, np.roll(p, -1, axis=1)))
        w_l = self._gold_weight(self._phase_diff(p, np.roll(p, 1, axis=1)))
        # y-up interior
        d_up = np.zeros_like(p)
        d_up[:-1] = self._phase_diff(p[:-1], p[1:])
        # y-down interior
        d_dn = np.zeros_like(p)
        d_dn[1:] = self._phase_diff(p[1:], p[:-1])
        # twist seam y-up: bottom row -> top row reversed
        d_up[-1] = self._phase_diff(p[-1], p[0, ::-1])
        # twist seam y-down: top row -> bottom row reversed
        d_dn[0] = self._phase_diff(p[0], p[-1, ::-1])
        return self._gold_weight(d_up), self._gold_weight(d_dn), w_r, w_l

    # ── update ──────────────────────────────────────────────────────────

    def step(self):
        s = self.state
        n = self.n
        w_up, w_dn, w_r, w_l = self._edge_weights()

        def neigh(x, w_up, w_dn, w_r, w_l, sign_up, sign_dn):
            """Weighted, signed neighbour sum for a scalar field."""
            hx = np.zeros_like(x)
            hx += w_r * np.roll(x, -1, axis=1)   # right
            hx += w_l * np.roll(x, 1, axis=1)    # left
            # y-up (interior, untwisted)
            hx[:-1] += w_up[:-1] * x[1:]
            # y-down (interior, untwisted)
            hx[1:] += w_dn[1:] * x[:-1]
            # twist seam (signed):
            # bottom row y-up -> top row x-reversed, sign = -1
            hx[-1] += sign_up * w_up[-1] * x[0, ::-1]
            # top row y-down -> bottom row x-reversed, sign = -1
            hx[0] += sign_dn * w_dn[0] * x[-1, ::-1]
            return hx

        up, dn, zr = s[:, :, 0], s[:, :, 1], s[:, :, 2]

        h_up = neigh(up, w_up, w_dn, w_r, w_l, -1.0, -1.0)
        h_dn = neigh(dn, w_up, w_dn, w_r, w_l, -1.0, -1.0)
        h_zr = neigh(zr, w_up, w_dn, w_r, w_l, -1.0, -1.0)

        # cross-component coupling (up/down inhibition)
        cross = 0.25
        h_up += cross * neigh(-dn, w_up, w_dn, w_r, w_l, -1.0, -1.0)
        h_dn += cross * neigh(-up, w_up, w_dn, w_r, w_l, -1.0, -1.0)
        h_zr += cross * neigh(up * dn, w_up, w_dn, w_r, w_l, -1.0, -1.0)

        g = self.gain / 4.0
        noise = self.noise_std * np.random.randn(n, n, 3)
        self.state[:, :, 0] = np.tanh(g * h_up + noise[:, :, 0])
        self.state[:, :, 1] = np.tanh(g * h_dn + noise[:, :, 1])
        self.state[:, :, 2] = np.tanh(g * h_zr + noise[:, :, 2])

        # golden attractor: phase rotation + drift toward golden neighbors
        self.phase = (self.phase + 2 * np.pi * ALPHA_GOLDEN) % (2 * np.pi)

        # drift: maintain golden separation (not alignment)
        w_up, w_dn, w_r, w_l = self._edge_weights()
        for wt, roll_x, roll_y in [(w_r, -1, 0)]:
            nbr_phase = np.roll(np.roll(self.phase, roll_x, axis=1),
                               roll_y, axis=0)
            drift_mask = wt > 0.5
            t1 = (nbr_phase - 2 * np.pi * ALPHA_GOLDEN) % (2 * np.pi)
            t2 = (nbr_phase + 2 * np.pi * ALPHA_GOLDEN) % (2 * np.pi)
            d1 = np.minimum(np.abs(self.phase - t1),
                            2 * np.pi - np.abs(self.phase - t1))
            d2 = np.minimum(np.abs(self.phase - t2),
                            2 * np.pi - np.abs(self.phase - t2))
            target = np.where(d1 < d2, t1, t2)
            self.phase[drift_mask] = (0.97 * self.phase[drift_mask]
                + 0.03 * target[drift_mask]) % (2 * np.pi)

        self.step_count += 1

    # ── observables ─────────────────────────────────────────────────────

    def total_information(self):
        return float(np.abs(self.state).sum())

    def golden_fraction(self):
        """Fraction of edges that are golden-resonant."""
        w_up, w_dn, w_r, w_l = self._edge_weights()
        all_w = np.concatenate([w_up.ravel(), w_dn.ravel(),
                                w_r.ravel(), w_l.ravel()])
        return float(np.mean(all_w > 0.5))

    def spatial_entropy(self):
        amp = np.sqrt(np.sum(self.state ** 2, axis=-1)).ravel()
        amp = amp[amp > 1e-9]
        if len(amp) < 2:
            return 0.0
        p = amp / amp.sum()
        return -float(np.sum(p * np.log(p + 1e-12)))

    def twist_correlation(self):
        bot = self.state[-1]
        top_rev = self.state[0, ::-1]
        return float((bot * top_rev).sum(axis=-1).mean())

    def pattern_count(self, threshold=0.4):
        amp = np.sqrt(np.sum(self.state ** 2, axis=-1))
        mask = amp > threshold
        s = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        _, nc = label(mask, structure=s)
        return int(nc)

    def run(self, n_steps=2000, record_every=20):
        rows = []
        for t in range(n_steps):
            self.step()
            if t % record_every == 0:
                rows.append({
                    "step": t + 1,
                    "total_info": self.total_information(),
                    "golden_frac": self.golden_fraction(),
                    "entropy": self.spatial_entropy(),
                    "twist_corr": self.twist_correlation(),
                    "patterns": self.pattern_count(),
                })
        return rows


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    sub = KleinGoldenSubstrate(n=128, noise_std=0.02, gain=3.0)
    rows = sub.run(n_steps=2500)

    with open(os.path.join(OUT_DIR, "golden_substrate_trajectory.csv"), "w",
              newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("step   total_info  gold_frac  entropy  twist_corr  patterns")
    for r in rows[-6:]:
        print(f"{r['step']:5d}  {r['total_info']:9.1f}  "
              f"{r['golden_frac']:8.3f}  {r['entropy']:6.3f}  "
              f"{r['twist_corr']:9.4f}  {r['patterns']:7d}")

    init, final = rows[0], rows[-1]
    print(f"\nGolden fraction: {init['golden_frac']:.3f} -> "
          f"{final['golden_frac']:.3f}")
    print(f"Twist correlation: {init['twist_corr']:.4f} -> "
          f"{final['twist_corr']:.4f}")
    print(f"Entropy: {init['entropy']:.3f} -> {final['entropy']:.3f}")

    make_figure(rows, sub)
    print(f"Wrote {OUT_DIR}")


def make_figure(rows, sub):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    ts = [r["step"] for r in rows]

    ax = axes[0, 0]
    ax.plot(ts, [r["total_info"] for r in rows], "-", color="seagreen",
            lw=2, label="total info")
    ax.plot(ts, [r["patterns"] for r in rows], "-", color="steelblue",
            label="patterns")
    ax.set_xlabel("plonk tick"); ax.set_ylabel("value")
    ax.set_title("A. Total information and patterns")
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    ax.plot(ts, [r["golden_frac"] for r in rows], "-", color="crimson",
            lw=2, label="golden fraction")
    ax.axhline(0.3, color="gray", ls="--", label="default coupling 0.3")
    ax.set_xlabel("plonk tick"); ax.set_ylabel("fraction")
    ax.set_title("B. Golden-resonant edge fraction")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    ax.plot(ts, [r["twist_corr"] for r in rows], "-", color="crimson",
            lw=2, label="twist correlation")
    ax.axhline(0, color="gray", ls=":")
    ax.set_xlabel("plonk tick"); ax.set_ylabel("correlation")
    ax.set_title("C. Twist-seam antipodal correlation")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    amp = np.sqrt(np.sum(sub.state ** 2, axis=-1))
    im = ax.imshow(amp, cmap="inferno", aspect="equal", origin="lower")
    fig.colorbar(im, ax=ax, fraction=0.046)
    ax.set_title(f"D. Final amplitude (t = {sub.step_count})")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "golden_field_evolution.png"),
                dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
