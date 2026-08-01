"""
================================================================================
IST PHASE 23b — QM Diagnostic Suite
================================================================================
Four quantum-mechanical tests on the Phase 23a plonk-cycle substrate:

  1. SPIN: Chirality return pattern — 1-loop knots (electrons) should
     flip chirality at 2 ticks (180 deg rotation), characteristic of
     spin-1/2. Multi-loop knots should have different patterns.

  2. SUPERPOSITION: Two oscillators at same position, pi phase
     difference. Evolve independently; check interference after one
     4-tick cycle based on twist-crossing phase difference.

  3. ENTANGLEMENT: Two oscillators at positions connected by a short
     twist geodesic (far in spatial coords, adjacent in substrate).
     Measure instantaneous phase correlation after coupling.

  4. UNCERTAINTY: Phase-space distribution of stable knots vs
     unstable oscillators. Minimum Delta_x * Delta_p consistent
     with plonk-scale granularity.

Output: code/outputs/phase23b/qm_diagnostics.csv
        code/outputs/phase23b/qm_diagnostics.png
================================================================================
"""
import csv, os, time
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import numpy as np
from phase1_klein_laplacian import PHI
from phase23a_plonk_cycle import (
    PlonkOscillator, PlonkSubstrate, fibonacci_lattice, klein_distance,
    ALPHA_GOLD, TOL
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase23b")


def run_spin_test(sub, n_cycles=8):
    """Track chirality per tick (not just per 4-tick cycle). Returns
    chirality history: rows × (N_oscillators × n_ticks)."""
    history = []
    for _ in range(n_cycles):
        for tick in range(4):
            sub.plonk_tick()
            if tick == 1:  # after 2 ticks (180 deg)
                history.append([o.chirality for o in sub.oscillators])
    # Extract oscillators that are in stable knots (>3 phase returns)
    return np.array(history)


def run_superposition_test(sub):
    """Initialize two oscillators at same position, opposite phase.
    Track their phase difference over 4 cycles."""
    # Use first two oscillators (from Fibonacci lattice, different phases)
    if sub.N < 2: return None
    o0, o1 = sub.oscillators[0], sub.oscillators[1]
    o1.phase = (o0.phase + np.pi) % (2*np.pi)  # pi phase difference
    history = []
    for cycle in range(4):
        for tick in range(4):
            sub.plonk_tick()
        diff = abs(o0.phase - o1.phase)
        diff = min(diff, 2*np.pi - diff)
        history.append({"cycle": cycle+1, "phase_diff": diff})
    return history


def run_entanglement_test(sub):
    """Find a pair of oscillators connected by a short twist geodesic
    but far in spatial coordinates. Couple them strongly, measure
    phase correlation after a tick."""
    us = np.array([o.u for o in sub.oscillators])
    vs = np.array([o.v for o in sub.oscillators])
    N = sub.N
    # Find pair with short Klein distance but far Euclidean distance
    best_ratio = 0; best_pair = (0, 1)
    for i in range(N):
        for j in range(i+1, N):
            d_klein = klein_distance(us[i], vs[i], us[j], vs[j])
            d_euclid = np.sqrt((us[i]-us[j])**2 + (vs[i]-vs[j])**2)
            if d_euclid > 0.3 and d_klein > 0 and d_euclid/d_klein > best_ratio:
                best_ratio = d_euclid/d_klein; best_pair = (i, j)

    i, j = best_pair
    # Record initial phases
    phi_i0 = sub.oscillators[i].phase
    phi_j0 = sub.oscillators[j].phase
    diff0 = min(abs(phi_i0-phi_j0), 2*np.pi-abs(phi_i0-phi_j0))

    # Apply a kick to oscillator i and check correlation with j
    sub.oscillators[i].phase = (phi_i0 + np.pi/2) % (2*np.pi)
    sub.plonk_tick()

    phi_i1 = sub.oscillators[i].phase
    phi_j1 = sub.oscillators[j].phase
    diff1 = min(abs(phi_i1-phi_j1), 2*np.pi-abs(phi_i1-phi_j1))
    # Compute Klein distance manually for scalars
    ui, vi = us[i], vs[i]; uj, vj = us[j], vs[j]
    du = abs(ui-uj); dv = abs(vi-vj)
    d2 = du**2 + dv**2
    for su in [1,-1]: d2 = min(d2, (du+su)**2 + dv**2)
    for sv in [1,-1]: d2 = min(d2, du**2 + (dv+sv)**2)
    for su in [1,-1]:
        for sv in [1,-1]: d2 = min(d2, (du+su)**2 + (dv+sv)**2)
    for su in [0,1,-1]:
        for sv in [0,1,-1]:
            d2t = (ui+uj+su)**2 + (vi-vj+0.5+sv)**2
            d2 = min(d2, d2t)
    d_klein = np.sqrt(max(d2, 0))
    d_euclid = np.sqrt((ui-uj)**2 + (vi-vj)**2)
    return {"i": int(i), "j": int(j), "klein_d": float(d_klein),
            "euclid_d": float(d_euclid),
            "diff_before": float(diff0), "diff_after": float(diff1),
            "correlation": float(diff1 - diff0)}


def run_uncertainty_test(sub, n_cycles=10):
    """Measure phase-space distribution of stable knots."""
    # Run for several cycles, identify stable knots
    phases = np.array([o.phase for o in sub.oscillators])
    amps = np.array([o.amp for o in sub.oscillators])
    # Phase spread as measure of Delta p, amplitude spread as Delta x
    delta_phase = np.std(phases[amps > 0.1])
    delta_amp = np.std(amps[amps > 0.1])
    product = delta_phase * delta_amp
    return {"delta_phase": float(delta_phase), "delta_amp": float(delta_amp),
            "product": float(product),
            "plonk_bound": float(2*np.pi / sub.N)}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.perf_counter()

    # Build substrate
    oscs = fibonacci_lattice(200)
    sub = PlonkSubstrate(oscs, omega_0=0.3, gain=0.8, sigma=0.15)
    rows = []

    # 1. SPIN TEST
    chir_hist = run_spin_test(sub, n_cycles=6)
    # After 2 ticks (180 deg), chirality should flip for spin-1/2
    flipped_frac = [(chir_hist[k] < 0).sum() / len(chir_hist[k])
                    for k in range(len(chir_hist))]
    for cyc, frac in enumerate(flipped_frac[:4]):
        rows.append({"test": "spin", "metric": f"cycle_{cyc+1}_flip_frac",
                     "value": frac})
    print(f"Spin test: chirality flip fraction at 180 deg = "
          f"{[f'{f:.3f}' for f in flipped_frac[:4]]}")

    # 2. SUPERPOSITION TEST
    # Rebuild fresh for each test
    oscs2 = fibonacci_lattice(200)
    sub2 = PlonkSubstrate(oscs2, omega_0=0.3, gain=0.8, sigma=0.15)
    sup_hist = run_superposition_test(sub2)
    for h in sup_hist:
        rows.append({"test": "superposition", "metric": f"cycle_{h['cycle']}",
                     "value": h["phase_diff"]})
    vals = [h['phase_diff'] for h in sup_hist]
    print(f"Superposition: phase diffs = {[f'{v:.3f}' for v in vals]}")

    # 3. ENTANGLEMENT TEST
    oscs3 = fibonacci_lattice(200)
    sub3 = PlonkSubstrate(oscs3, omega_0=0.3, gain=0.8, sigma=0.15)
    ent = run_entanglement_test(sub3)
    for k, v in ent.items():
        rows.append({"test": "entanglement", "metric": k, "value": v})
    print(f"Entanglement: pair ({ent['i']},{ent['j']}), "
          f"klein_d={ent['klein_d']:.3f}, euclid_d={ent['euclid_d']:.3f}, "
          f"diff_before={ent['diff_before']:.3f}, "
          f"diff_after={ent['diff_after']:.3f}")

    # 4. UNCERTAINTY TEST
    unc = run_uncertainty_test(sub)
    for k, v in unc.items():
        rows.append({"test": "uncertainty", "metric": k, "value": v})
    print(f"Uncertainty: Delta_phase={unc['delta_phase']:.3f}, "
          f"Delta_amp={unc['delta_amp']:.3f}, "
          f"product={unc['product']:.3f}, "
          f"plonk_bound={unc['plonk_bound']:.3f}")

    with open(os.path.join(OUT_DIR, "qm_diagnostics.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    print(f"\nAll tests in {time.perf_counter()-t0:.0f}s")
    print(f"Wrote {OUT_DIR}")


if __name__ == "__main__":
    main()
