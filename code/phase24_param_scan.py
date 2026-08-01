"""
================================================================================
IST PHASE 24 — Parameter Scan: Plonk-Scale Substrate Optimization
================================================================================
Vary omega_0, gain, sigma, TOL, and N across ranges to find the
regime where stable knots maximize, golden-phase coherence peaks,
and the field remains unsaturated (mean_amp < 1). One-at-a-time
sweeps with defaults held at Phase 23a baseline.

Output: code/outputs/phase24/param_scan.csv, param_scan.png
================================================================================
"""
import csv, os, time
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import numpy as np
from phase1_klein_laplacian import PHI
from phase23a_plonk_cycle import (
    PlonkOscillator, PlonkSubstrate, fibonacci_lattice
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase24")

# Defaults from Phase 23a
DEF = {"omega_0": 0.3, "gain": 0.8, "sigma": 0.15, "TOL": 0.25, "N": 200}


def run_config(n_cycles=40, **kwargs):
    """Run a single configuration and return final metrics."""
    cfg = {**DEF, **kwargs}
    oscs = fibonacci_lattice(cfg["N"])
    sub = PlonkSubstrate(oscs, omega_0=cfg["omega_0"], gain=cfg["gain"],
                         sigma=cfg["sigma"])
    # Override TOL in the module
    import phase23a_plonk_cycle as p23
    old_tol = p23.TOL
    p23.TOL = cfg["TOL"]

    stable_hist, gold_hist, amp_hist = [], [], []
    for cyc in range(n_cycles):
        phases_before = np.array([o.phase for o in sub.oscillators])
        for _ in range(4):
            sub.plonk_tick()
        phases_after = np.array([o.phase for o in sub.oscillators])
        diff = np.minimum(np.abs(phases_after - phases_before),
                          2*np.pi - np.abs(phases_after - phases_before))
        stable_hist.append(np.sum(diff < 0.1))
        gold_hist.append(sub.golden_phase_fraction())
        amp_hist.append(np.mean([o.amp for o in sub.oscillators]))

    p23.TOL = old_tol
    last10 = slice(-10, None)
    return {
        **cfg,
        "stable_mean": np.mean(stable_hist[last10]),
        "stable_std": np.std(stable_hist[last10]),
        "golden_mean": np.mean(gold_hist[last10]),
        "golden_std": np.std(gold_hist[last10]),
        "amp_mean": np.mean(amp_hist[last10]),
        "amp_std": np.std(amp_hist[last10]),
    }


def sweep(param_name, values, label=None):
    """Sweep one parameter, return list of result dicts."""
    results = []
    for v in values:
        kwargs = {param_name: v}
        r = run_config(**kwargs)
        results.append({**r, "sweep_param": param_name, "sweep_value": v,
                        "sweep_label": label or param_name})
    return results


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.perf_counter()
    all_rows = []
    sweeps = [
        ("omega_0", [0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.2]),
        ("gain",    [0.2, 0.4, 0.6, 0.8, 1.0, 1.3, 1.6]),
        ("sigma",   [0.05, 0.08, 0.12, 0.15, 0.20, 0.28, 0.40]),
        ("TOL",     [0.08, 0.12, 0.18, 0.25, 0.35, 0.50]),
        ("N",       [80, 120, 160, 200, 280]),
    ]

    for name, values in sweeps:
        print(f"\nSweeping {name}: {values}")
        results = sweep(name, values)
        all_rows.extend(results)
        for r in results:
            print(f"  {name}={r['sweep_value']:5.2f}: "
                  f"stable={r['stable_mean']:5.1f} "
                  f"golden={r['golden_mean']:.3f} "
                  f"amp={r['amp_mean']:.3f}")

    with open(os.path.join(OUT_DIR, "param_scan.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(all_rows[0].keys()))
        w.writeheader(); w.writerows(all_rows)

    make_figure(all_rows)
    print(f"\nTotal: {time.perf_counter()-t0:.0f}s. Wrote {OUT_DIR}")


def make_figure(all_rows):
    params = ["omega_0", "gain", "sigma", "TOL", "N"]
    fig, axes = plt.subplots(5, 3, figsize=(14, 18))

    for row_idx, param in enumerate(params):
        pts = [r for r in all_rows if r["sweep_param"] == param]
        pts.sort(key=lambda r: r["sweep_value"])
        xs = [r["sweep_value"] for r in pts]

        ax = axes[row_idx, 0]
        ax.plot(xs, [r["stable_mean"] for r in pts], "o-",
                color="seagreen", lw=2, ms=6)
        ax.set_xlabel(param); ax.set_ylabel("stable knots")
        ax.set_title(f"Stable knots vs {param}")

        ax = axes[row_idx, 1]
        ax.plot(xs, [r["golden_mean"] for r in pts], "o-",
                color="crimson", lw=2, ms=6)
        ax.set_xlabel(param); ax.set_ylabel("golden fraction")
        ax.set_title(f"Golden fraction vs {param}")

        ax = axes[row_idx, 2]
        ax.plot(xs, [r["amp_mean"] for r in pts], "o-",
                color="steelblue", lw=2, ms=6)
        ax.axhline(1.0, color="gray", ls=":")
        ax.set_xlabel(param); ax.set_ylabel("mean amplitude")
        ax.set_title(f"Amplitude vs {param}")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "param_scan.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
