"""
================================================================================
IST PHASE 26 — Multi-Partite Entanglement on Klein Bottle
================================================================================
Extends Phase 23b's 2-party entanglement to 3-party and 4-party
clusters. Searches for oscillators mutually connected by short twist
geodesics (substrate-adjacent but spatially separated in Euclidean
projection). Measures:

  1. 3-tangle (genuine tripartite entanglement) via phase correlations
  2. Anti-symmetry pattern (color-singlet / GHZ state)
  3. Comparison to random triples as null test
  4. Scaling with associator charge proxy

The proton's 3-quark structure maps naturally: three oscillators with
mutual twist geodesics form a color-singlet-like cluster whose
entanglement pattern is invariant under cyclic permutations.

Output: code/outputs/phase26/entanglement_clusters.csv
        code/outputs/phase26/multipartite_entanglement.png
================================================================================
"""
import csv, os, time, itertools, ast
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import numpy as np
from phase1_klein_laplacian import PHI
from phase23a_plonk_cycle import (
    PlonkOscillator, PlonkSubstrate, fibonacci_lattice, klein_distance,
    ALPHA_GOLD
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase26")


def find_klein_clusters(sub, max_klein_d=0.15, min_euclid_ratio=2.0, top_n=30):
    """Find oscillators mutually connected by short Klein geodesics.
    Exhaustive for 3-clusters; 4-clusters grown from 3-clusters."""
    N = sub.N
    us = np.array([o.u for o in sub.oscillators])
    vs = np.array([o.v for o in sub.oscillators])

    klein_d = np.zeros((N, N))
    euclid_d = np.zeros((N, N))
    for i in range(N):
        for j in range(i+1, N):
            kd, _ = klein_distance(us[i:i+1], vs[i:i+1], us[j:j+1], vs[j:j+1])
            kd = float(kd[0,0])
            ed = np.sqrt((us[i]-us[j])**2 + (vs[i]-vs[j])**2)
            klein_d[i,j] = klein_d[j,i] = kd
            euclid_d[i,j] = euclid_d[j,i] = ed

    # 3-clusters: exhaustive
    clusters = []
    for i in range(N):
        for j in range(i+1, N):
            if klein_d[i,j] >= max_klein_d: continue
            for k in range(j+1, N):
                if (klein_d[i,k] < max_klein_d and klein_d[j,k] < max_klein_d):
                    avg_k = (klein_d[i,j]+klein_d[i,k]+klein_d[j,k])/3
                    avg_e = (euclid_d[i,j]+euclid_d[i,k]+euclid_d[j,k])/3
                    if avg_e / max(avg_k, 1e-9) >= min_euclid_ratio:
                        clusters.append((3, (i,j,k), avg_k, avg_e))

    # 4-clusters: grow from 3-clusters
    for _, combo, _, _ in clusters[:200]:  # use top 3-clusters
        for m in range(N):
            if m in combo: continue
            if all(klein_d[m, c] < max_klein_d for c in combo):
                full = tuple(sorted(combo + (m,)))
                avg_k = np.mean([klein_d[i,j] for i,j in itertools.combinations(full,2)])
                avg_e = np.mean([euclid_d[i,j] for i,j in itertools.combinations(full,2)])
                if avg_e / max(avg_k, 1e-9) >= min_euclid_ratio:
                    clusters.append((4, full, avg_k, avg_e))

    clusters.sort(key=lambda c: -(c[3]/max(c[2],1e-9)))
    return clusters[:top_n]


def three_tangle_over_time(sub, indices, n_ticks=20):
    """3-tangle from phase coherence over time: |<exp(i sum)>|
    over n_ticks samples. Low variance = genuinely tripartite-entangled."""
    samples = []
    for _ in range(n_ticks):
        for _ in range(4):
            sub.plonk_tick()
        phases = np.array([sub.oscillators[i].phase for i in indices])
        samples.append(np.exp(1j * phases.sum()))
    return abs(np.mean(samples))


def pairwise_corr_over_time(sub, indices, n_ticks=20):
    """Mean pairwise phase correlation over time."""
    corrs = []
    for _ in range(n_ticks):
        for _ in range(4):
            sub.plonk_tick()
        phases = np.array([sub.oscillators[i].phase for i in indices])
        pw = [np.cos(phases[i]-phases[j]) for i,j in itertools.combinations(range(len(phases)),2)]
        corrs.append(np.mean(pw))
    return np.mean(corrs)


def random_triple_null(sub, n_samples=500):
    """Null distribution of 3-tangle from random triples."""
    phases_all = np.array([o.phase for o in sub.oscillators])
    nulls = []
    for _ in range(n_samples):
        idx = np.random.choice(sub.N, 3, replace=False)
        nulls.append(three_tangle(phases_all[idx]))
    return np.array(nulls)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.perf_counter()

    # Build substrate, run for a few cycles to develop correlations
    oscs = fibonacci_lattice(200)
    sub = PlonkSubstrate(oscs, omega_0=0.3, gain=0.8, sigma=0.15)
    for _ in range(20):
        for _ in range(4):
            sub.plonk_tick()

    # Find clusters
    clusters = find_klein_clusters(sub, max_klein_d=0.15, min_euclid_ratio=2.0,
                                   top_n=30)
    print(f"Found {len(clusters)} multi-partite Klein clusters")
    for sz, combo, kd, ed in clusters[:8]:
        print(f"  size={sz} indices={combo} klein_d={kd:.3f} "
              f"euclid_d={ed:.3f} ratio={ed/max(kd,1e-9):.1f}")

    # Measure entanglement over time for top clusters
    rows = []
    for sz, combo, kd, ed in clusters:
        t3 = three_tangle_over_time(sub, combo, n_ticks=20)
        pw = pairwise_corr_over_time(sub, combo, n_ticks=20)
        rows.append({
            "size": sz, "indices": str(combo),
            "klein_d": kd, "euclid_d": ed,
            "euclid_klein_ratio": ed / max(kd, 1e-9),
            "three_tangle": t3,
            "mean_pairwise_corr": pw,
        })

    # Null: random triples, same temporal measurement
    phases_all = np.array([o.phase for o in sub.oscillators])
    null_3t = []
    for _ in range(100):
        idx = np.random.choice(sub.N, 3, replace=False)
        null_3t.append(three_tangle_over_time(sub, idx.tolist(), n_ticks=10))
    null_mean = np.mean(null_3t); null_std = np.std(null_3t)

    # Compare clusters vs null
    t3_clusters = [r["three_tangle"] for r in rows if r["size"] == 3]
    if t3_clusters:
        print(f"\n3-tangle: cluster mean={np.mean(t3_clusters):.3f}, "
              f"null mean={null_mean:.3f}+/-{null_std:.3f}")
        sig = [(t - null_mean)/null_std for t in t3_clusters]
        print(f"  Cluster significances: {[f'{s:.1f}sigma' for s in sig[:5]]}")

    # Anti-symmetry check: for 3-clusters, is exp(i(phi1+phi2+phi3)) ~ 0?
    # (GHZ state has three-tangle = 1, but we want the color-singlet pattern
    #  where the sum of phases is pi, giving exp(i sum) = -1)
    for r in rows[:5]:
        if r["size"] == 3:
            phases = phases_all[list(ast.literal_eval(r["indices"]))]
            sum_phase = phases.sum() % (2*np.pi)
            anti_sym = abs(np.exp(1j*sum_phase) + 1)
            print(f"  cluster {r['indices']}: sum_phase={sum_phase:.3f} "
                  f"anti_symmetry={anti_sym:.3f}")

    with open(os.path.join(OUT_DIR, "entanglement_clusters.csv"), "w",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    make_figure(rows, null_3t, sub)
    print(f"Wrote {OUT_DIR} ({time.perf_counter()-t0:.0f}s)")


def make_figure(rows, null_3t, sub):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0,0]
    sizes = [r["size"] for r in rows]
    ratios = [r["euclid_klein_ratio"] for r in rows]
    ax.scatter(sizes, ratios, c="steelblue", s=40)
    ax.set_xlabel("cluster size"); ax.set_ylabel("Euclidean/Klein ratio")
    ax.set_title("A. Klein cluster candidates")

    ax = axes[0,1]
    ax.hist(null_3t, bins=25, color="steelblue", alpha=0.7,
            label=f"null (n={len(null_3t)})")
    t3s = [r["three_tangle"] for r in rows if r["size"] == 3]
    for t in t3s:
        ax.axvline(t, color="crimson", lw=1.5, alpha=0.7)
    ax.set_xlabel("3-tangle"); ax.set_ylabel("count")
    ax.set_title("B. Three-tangle (clusters vs null)")
    ax.legend(fontsize=8)

    ax = axes[1,0]
    # Pairwise correlation vs Klein distance
    klein_ds = [r["klein_d"] for r in rows]
    pw_corrs = [r["mean_pairwise_corr"] for r in rows]
    sz_colors = ["crimson" if r["size"]==3 else "seagreen" for r in rows]
    ax.scatter(klein_ds, pw_corrs, c=sz_colors, s=40)
    ax.set_xlabel("mean Klein distance"); ax.set_ylabel("mean pairwise corr")
    ax.set_title("C. Correlation vs substrate proximity")

    ax = axes[1,1]
    us = [o.u for o in sub.oscillators]; vs = [o.v for o in sub.oscillators]
    ax.scatter(us, vs, c="gray", s=3, alpha=0.3)
    # Highlight top 3 clusters
    for r in rows[:3]:
        idx_arr = np.array(list(ast.literal_eval(r["indices"])))
        ax.scatter(us[idx_arr], vs[idx_arr], s=60, edgecolors="crimson",
                   facecolors="none", lw=2)
    ax.set_xlabel("u (meridian)"); ax.set_ylabel("v (longitude)")
    ax.set_title(f"D. Top clusters ({len(rows)} found)")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "multipartite_entanglement.png"),
                dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
