"""
================================================================================
IST PHASE 23a — Plonk-Scale Orientation Cycle
================================================================================
Implements the 4-tick orientation cycle on the Klein bottle's 720°
double-cover. Oscillators placed on a Fibonacci (golden-angle) lattice
for correlated phase-position ordering. Each plonk tick advances
orientation through one quarter of the full Klein cycle, with
chirality flipping at twist crossings.

Components:
  * Fibonacci lattice on Klein bottle (golden-angle spiral)
  * 4-state orientation tracker {0,1,2,3}
  * Chirality sign: +1 (original side), -1 (twist-flipped)
  * Phase evolution per tick: dtheta/dtau = omega_0 + coupling
  * Golden-filter coupling: boost for golden-ratio phase separations
  * 720° verification: chirality restored after 4-tick cycle

Output: code/outputs/phase23a/orientation_cycle.csv
        code/outputs/phase23a/plonk_cycle.png
================================================================================
"""
import csv, os, time
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import numpy as np
from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase23a")
ALPHA_GOLD = 1.0 / PHI ** 2
TOL = 0.25


class PlonkOscillator:
    """Oscillator on the Klein bottle with 4-state orientation tracker."""
    __slots__ = ("u", "v", "phase", "orientation", "chirality", "amp")
    def __init__(self, u, v, phase, amp=0.5):
        self.u = float(u); self.v = float(v)
        self.phase = float(phase) % (2*np.pi)
        self.orientation = 0   # 0,1,2,3
        self.chirality = 1     # +1 or -1
        self.amp = float(amp)


def fibonacci_lattice(N, golden_angle=None):
    """Place N points on Klein bottle using golden-angle spiral.
    Returns list of (u,v, phase) where phase = position on spectral circle."""
    if golden_angle is None:
        golden_angle = 2 * np.pi * ALPHA_GOLD
    points = []
    for i in range(N):
        theta = (i * golden_angle) % (2*np.pi)
        # map to unit square Klein coords
        u = theta / (2*np.pi)          # meridian coord [0,1)
        z = 1.0 - (2.0*i + 1.0) / N
        phi = np.arccos(max(min(z, 1), -1))
        v = phi / np.pi                # longitude coord [0,1)
        # Möbius twist: v → v + u/2 mod 1
        v_twisted = (v + u * 0.5) % 1.0
        phase = 2*np.pi * u            # spectral phase from meridian
        points.append(PlonkOscillator(u, v_twisted, phase))
    return points


def klein_distance(u1, v1, u2, v2):
    """Geodesic distance on Klein bottle [0,1)^2 with twist identification."""
    u1, v1 = np.atleast_1d(u1), np.atleast_1d(v1)
    u2, v2 = np.atleast_1d(u2), np.atleast_1d(v2)
    du = np.abs(u1[:,None] - u2[None,:])
    dv = np.abs(v1[:,None] - v2[None,:])
    d2 = du**2 + dv**2
    for su in [1.0, -1.0]:
        d2 = np.minimum(d2, (du+su)**2 + dv**2)
    for sv in [1.0, -1.0]:
        d2 = np.minimum(d2, du**2 + (dv+sv)**2)
    for su in [1.0, -1.0]:
        for sv in [1.0, -1.0]:
            d2 = np.minimum(d2, (du+su)**2 + (dv+sv)**2)
    # twist: (u1,v1) ~ (-u2, v2+0.5)
    for su in [0.0, 1.0, -1.0]:
        for sv in [0.0, 1.0, -1.0]:
            d2t = (u1[:,None]+u2[None,:]+su)**2 + (v1[:,None]-v2[None,:]+0.5+sv)**2
            d2 = np.minimum(d2, d2t)
    return np.sqrt(np.maximum(d2, 0.0))


class PlonkSubstrate:
    """Oscillator field on Klein bottle with plonk-tick orientation cycle."""

    def __init__(self, oscillators, omega_0=0.3, gain=0.8, sigma=0.15):
        self.oscillators = list(oscillators)
        self.N = len(oscillators)
        self.omega_0 = omega_0
        self.gain = gain
        self.sigma = sigma
        self.tick_count = 0

    def _golden_coupling(self):
        """Coupling strength based on golden-ratio phase separations."""
        N = self.N
        phases = np.array([o.phase for o in self.oscillators])
        dp = np.abs(phases[:,None] - phases[None,:])
        dp = np.minimum(dp, 2*np.pi - dp)
        golden_match = np.zeros((N,N), dtype=bool)
        for tgt in [2*np.pi*ALPHA_GOLD, 2*np.pi*(1-ALPHA_GOLD)]:
            golden_match |= np.abs(dp - tgt) < TOL
        np.fill_diagonal(golden_match, False)
        # Spatial proximity on Klein surface
        us = np.array([o.u for o in self.oscillators])
        vs = np.array([o.v for o in self.oscillators])
        d = klein_distance(us, vs, us, vs)
        J = np.exp(-d**2/(2*self.sigma**2))
        np.fill_diagonal(J, 0)
        # Combine: golden pairs get 5× coupling
        return np.where(golden_match, J*5.0, J*0.3)

    def plonk_tick(self):
        """One plonk tick: phase update + orientation advance + twist check."""
        W = self._golden_coupling()
        phases = np.array([o.phase for o in self.oscillators])
        chir = np.array([o.chirality for o in self.oscillators])
        amps = np.array([o.amp for o in self.oscillators])

        # Phase evolution: omega_0 + coupling from neighbours
        coupling = self.gain * (W @ (chir * amps))
        new_phases = (phases + self.omega_0 + coupling) % (2*np.pi)

        # Update oscillators
        for i, o in enumerate(self.oscillators):
            o.phase = new_phases[i]
            o.orientation = (o.orientation + 1) % 4
            # twist crossing at o=1→2 and o=3→0
            if o.orientation == 2 or o.orientation == 0:
                o.chirality *= -1
            # amplitude feedback
            o.amp = np.tanh(abs(coupling[i]) * 0.5)

        self.tick_count += 1

    def verify_720_cycle(self):
        """After 4 ticks, check which oscillators returned to original chirality."""
        orig_chir = np.array([o.chirality for o in self.oscillators])
        for _ in range(4):
            self.plonk_tick()
        final_chir = np.array([o.chirality for o in self.oscillators])
        returned = (final_chir == orig_chir)
        return returned.sum(), self.N - returned.sum()

    def stable_knots(self, n_cycles=10):
        """Count oscillators whose phases return within tol after each 4-tick cycle."""
        stable = np.zeros(self.N, dtype=bool)
        for _ in range(n_cycles):
            phases_before = np.array([o.phase for o in self.oscillators])
            for _ in range(4):
                self.plonk_tick()
            phases_after = np.array([o.phase for o in self.oscillators])
            diff = np.minimum(np.abs(phases_after - phases_before),
                              2*np.pi - np.abs(phases_after - phases_before))
            stable = stable | (diff < 0.1)
        return stable.sum(), stable

    def golden_phase_fraction(self):
        """Fraction of oscillator pairs at golden-angle phase separation."""
        phases = np.array([o.phase for o in self.oscillators])
        dp = np.abs(phases[:,None] - phases[None,:])
        dp = np.minimum(dp, 2*np.pi - dp)
        golden = np.zeros((self.N, self.N), dtype=bool)
        for tgt in [2*np.pi*ALPHA_GOLD, 2*np.pi*(1-ALPHA_GOLD)]:
            golden |= np.abs(dp - tgt) < TOL
        np.fill_diagonal(golden, False)
        return golden.sum() / (self.N * (self.N-1))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.perf_counter()

    # Fibonacci lattice of oscillators
    oscs = fibonacci_lattice(200)
    sub = PlonkSubstrate(oscs, omega_0=0.3, gain=0.8, sigma=0.15)

    # Verify 720° cycle
    returned, failed = sub.verify_720_cycle()
    print(f"720° cycle verification: {returned}/{sub.N} returned to original "
          f"chirality ({failed} failed)")

    # Run multiple cycles, track stable knots
    cycles = 20
    rows = []
    for c in range(cycles):
        phases_before = np.array([o.phase for o in sub.oscillators])
        orients_before = np.array([o.orientation for o in sub.oscillators])
        for _ in range(4):
            sub.plonk_tick()
        phases_after = np.array([o.phase for o in sub.oscillators])
        diff = np.minimum(np.abs(phases_after - phases_before),
                          2*np.pi - np.abs(phases_after - phases_before))
        n_stable = np.sum(diff < 0.1)
        n_positive = np.sum(np.array([o.chirality for o in sub.oscillators]) > 0)
        golden_frac = sub.golden_phase_fraction()
        rows.append({"cycle": c+1, "tick": sub.tick_count,
                     "n_stable": n_stable, "n_positive_chirality": n_positive,
                     "golden_frac": golden_frac,
                     "mean_amp": np.mean([o.amp for o in sub.oscillators])})

    print(f"\n{cycles} cycles in {time.perf_counter()-t0:.0f}s")
    for r in rows[::3]:
        print(f"  cycle {r['cycle']:2d}: tick={r['tick']:4d} "
              f"stable={r['n_stable']:3d} +chir={r['n_positive_chirality']:3d} "
              f"golden={r['golden_frac']:.3f} amp={r['mean_amp']:.3f}")

    with open(os.path.join(OUT_DIR, "orientation_cycle.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    make_figure(rows, sub)
    print(f"Wrote {OUT_DIR}")


def make_figure(rows, sub):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    cs = [r["cycle"] for r in rows]

    ax = axes[0,0]
    ax.plot(cs, [r["n_stable"] for r in rows], "o-", color="seagreen", lw=2)
    ax.set_xlabel("4-tick cycle"); ax.set_ylabel("stable knots")
    ax.set_title("A. Stable knots vs cycles")

    ax = axes[0,1]
    ax.plot(cs, [r["golden_frac"] for r in rows], "o-", color="crimson", lw=2)
    ax.set_xlabel("4-tick cycle"); ax.set_ylabel("golden fraction")
    ax.set_title("B. Golden phase fraction")

    ax = axes[1,0]
    ax.plot(cs, [r["n_positive_chirality"] for r in rows], "o-",
            color="steelblue", lw=2)
    ax.axhline(sub.N//2, color="gray", ls=":", label=f"N/2={sub.N//2}")
    ax.set_xlabel("4-tick cycle"); ax.set_ylabel("positive chirality count")
    ax.set_title("C. Chirality balance"); ax.legend(fontsize=8)

    ax = axes[1,1]
    us = [o.u for o in sub.oscillators]; vs = [o.v for o in sub.oscillators]
    colors = ["crimson" if o.chirality > 0 else "steelblue"
              for o in sub.oscillators]
    ax.scatter(us, vs, c=colors, s=8, alpha=0.7)
    ax.set_xlabel("u (meridian)"); ax.set_ylabel("v (longitude, twisted)")
    ax.set_title(f"D. Final state (tick {sub.tick_count})")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "plonk_cycle.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
