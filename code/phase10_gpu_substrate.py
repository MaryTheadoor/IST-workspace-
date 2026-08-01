"""
================================================================================
IST PHASE 10 - Klein Vector Substrate: Continuous Directed-Number Field
================================================================================
Purpose:
    A 2D doubly-stochastic vector matrix on the Klein bottle -- the actual
    substrate dynamics, not a cellular-automaton approximation. Each cell
    carries a 3-component directed-number state (up, down, zero amplitudes).
    The update rule is the IST compression operator with tanh nonlinearity:

        s(t+1) = tanh( W @ s(t) + noise )

    where W is the signed 4-neighbour coupling matrix (Klein twist at the
    meridian seam, edges crossing the twist get sign -1). Vacuum noise
    injection at each tick provides the plonk-time drive. The doubly
    stochastic property (row/col |W| sum = 1) conserves total information
    modulo the tanh saturation.

    Random initial vector oscillations seed the field; emergent persistent
    patterns are tracked over many plonk ticks.

Inputs:   none
Outputs:  code/outputs/phase10/vector_field_evolution.png
          code/outputs/phase10/substrate_trajectory.csv

References:
    IST_Project_Implementation_Plan.md (Priority 3-6)
    main/ist_v5_3_topology_substrate.md  (Eq. 1: Compression Operator)
    code/phase1_klein_laplacian.py       (Klein topology)
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

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase10")


# ───────────────────────────────────────────────────────────────────────────────
# KLEIN VECTOR SUBSTRATE
# ───────────────────────────────────────────────────────────────────────────────

class KleinVectorSubstrate:
    """2D continuous vector field on the Klein bottle.

    State shape: (n, n, 3) -- (up_amp, down_amp, zero_amp) per cell.
    Update: s(t+1) = tanh(W @ s(t) + noise)
    W: Chebyshev-radius-R signed coupling (degree (2R+1)^2 - 1)
       with Klein twist at the y-meridian seam.
    """

    def __init__(self, n=128, noise_std=0.02, gain=1.5, seed=1):
        self.n = n
        self.noise_std = noise_std
        self.gain = gain
        rng = np.random.default_rng(seed)

        # random vector oscillations
        self.state = rng.random((n, n, 3))
        # normalise to ~0.5 mean amplitude
        self.state /= 3.0

        self.step_count = 0

    def step(self):
        """One plonk tick: 4-neighbour signed Klein coupling with
        directed-number cross-component coupling (up suppresses down,
        down suppresses up, zero absorbs cross-coupling)."""
        s = self.state
        n = self.n
        up, dn, zr = s[:, :, 0], s[:, :, 1], s[:, :, 2]

        def neigh(x):
            """Signed neighbour sum for a scalar field on the Klein grid."""
            hx = np.zeros_like(x)
            hx += np.roll(x, -1, axis=1) + np.roll(x, 1, axis=1)
            hx[:-1] += x[1:]; hx[1:] += x[:-1]
            hx[-1] += -x[0, ::-1]; hx[0] += -x[-1, ::-1]
            return hx

        h_up = neigh(up)
        h_dn = neigh(dn)
        h_zr = neigh(zr)

        # cross-coupling: up suppressed by down, down suppressed by up
        # zero component absorbs the cross-coupling energy
        cross = 0.3
        h_up += cross * neigh(-dn)   # down neighbours reduce up
        h_dn += cross * neigh(-up)   # up neighbours reduce down
        h_zr += cross * neigh(up * dn)  # zero absorbs up-down product

        g = self.gain / 4.0
        h_up *= g; h_dn *= g; h_zr *= g

        noise = self.noise_std * np.random.randn(n, n, 3)
        self.state[:, :, 0] = np.tanh(h_up + noise[:, :, 0])
        self.state[:, :, 1] = np.tanh(h_dn + noise[:, :, 1])
        self.state[:, :, 2] = np.tanh(h_zr + noise[:, :, 2])
        self.step_count += 1

    # ── observables ─────────────────────────────────────────────────────

    def total_information(self):
        """Sum of absolute amplitudes (information magnitude)."""
        return float(np.abs(self.state).sum())

    def mean_amplitude(self):
        return float(self.state.mean())

    def spatial_entropy(self):
        """Shannon entropy of the spatial amplitude distribution."""
        amp = np.sqrt(np.sum(self.state ** 2, axis=-1)).ravel()
        amp = amp[amp > 1e-9]
        if len(amp) < 2:
            return 0.0
        p = amp / amp.sum()
        return -float(np.sum(p * np.log(p + 1e-12)))

    def twist_correlation(self):
        """Mean correlation across the Klein twist seam:
        < s[n-1-i, 0] · s[i, n-1] > -- should be negative for
        anti-podal balance (the Klein identification)."""
        bot = self.state[-1]        # row n-1
        top_rev = self.state[0, ::-1]  # row 0, x reversed
        corr = (bot * top_rev).sum(axis=-1).mean()
        return float(corr)

    def antipodal_balance(self):
        """Global signed sum (should be ~0 for balanced substrate)."""
        return float(self.state.sum() / self.n ** 2)

    def pattern_count(self, threshold=0.3):
        """Number of connected regions with amplitude > threshold."""
        amp = np.sqrt(np.sum(self.state ** 2, axis=-1))
        mask = amp > threshold
        s = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        _, nc = label(mask, structure=s)
        return int(nc)

    def component_fractions(self):
        """Fraction of total amplitude in up, down, zero channels."""
        total = self.state.sum()
        if total < 1e-9:
            return np.zeros(3)
        return self.state.sum(axis=(0, 1)) / total

    def run(self, n_steps=2000, record_every=20):
        rows = []
        for t in range(n_steps):
            self.step()
            if t % record_every == 0:
                rows.append({
                    "step": t + 1,
                    "total_info": self.total_information(),
                    "mean_amp": self.mean_amplitude(),
                    "entropy": self.spatial_entropy(),
                    "twist_corr": self.twist_correlation(),
                    "patterns": self.pattern_count(),
                    "up_frac": self.component_fractions()[0],
                    "down_frac": self.component_fractions()[1],
                    "zero_frac": self.component_fractions()[2],
                })
        return rows


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    n_steps = 3000
    sub = KleinVectorSubstrate(n=128, noise_std=0.015, gain=1.4)
    rows = sub.run(n_steps=n_steps)

    with open(os.path.join(OUT_DIR, "substrate_trajectory.csv"), "w",
              newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("step   total_info  entrop  twist_corr  patterns  up/dn/zr")
    for r in rows[-6:]:
        print(f"{r['step']:5d}  {r['total_info']:9.1f}  "
              f"{r['entropy']:6.3f}  {r['twist_corr']:9.4f}  "
              f"{r['patterns']:7d}  "
              f"{r['up_frac']:.2f}/{r['down_frac']:.2f}/{r['zero_frac']:.2f}")

    final = rows[-1]
    init = rows[0]
    print(f"\nTotal info: {init['total_info']:.1f} -> {final['total_info']:.1f}")
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
            lw=1, label="patterns")
    ax.set_xlabel("plonk tick")
    ax.set_ylabel("value")
    ax.set_title("A. Total information and pattern count")
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    ax.plot(ts, [r["twist_corr"] for r in rows], "-", color="crimson",
            lw=2, label="twist correlation")
    ax.axhline(0, color="gray", ls=":")
    ax.set_xlabel("plonk tick")
    ax.set_ylabel("correlation")
    ax.set_title("B. Twist-seam correlation (antipodal balance)")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    ax.plot(ts, [r["up_frac"] for r in rows], "-", color="royalblue",
            lw=1, label="up")
    ax.plot(ts, [r["down_frac"] for r in rows], "-", color="crimson",
            lw=1, label="down")
    ax.plot(ts, [r["zero_frac"] for r in rows], "-", color="gray",
            lw=1, label="zero")
    ax.set_xlabel("plonk tick")
    ax.set_ylabel("fraction")
    ax.set_title("C. Channel fractions (up/down/zero)")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    amp = np.sqrt(np.sum(sub.state ** 2, axis=-1))
    im = ax.imshow(amp, cmap="inferno", aspect="equal", origin="lower")
    fig.colorbar(im, ax=ax, fraction=0.046)
    ax.set_title(f"D. Final amplitude (t = {sub.step_count})")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "vector_field_evolution.png"),
                dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
