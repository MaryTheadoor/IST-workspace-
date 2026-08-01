"""
================================================================================
IST Phase 17b — Count-in-Cells Void Statistics from DES Y6 GOLD
================================================================================
Robust void detection via galaxy underdensity in 2D cells. No explicit
void finder needed. Measures P(void) — the fraction of cells below a
density threshold — and compares to the IST pinned model prediction
of enhanced void depth (63% suppression of G vs GR).

Input:  C:/Users/AmosA/Downloads/Y6_GOLD_2_2-0-0000.parquet
Output: code/outputs/phase17_des/void_statistics.csv
        code/outputs/phase17_des/count_in_cells.png
================================================================================
"""
import os, csv, time
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter
from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase17_des")
DATA = r"C:\Users\AmosA\Downloads\Y6_GOLD_2_2-0-0000.parquet"
SUPP_FACTOR = 0.2 ** (1.0 / PHI)  # 0.370 = 63% suppression


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.perf_counter()
    pf = pd.read_parquet(DATA, columns=["RA", "DEC", "DNF_Z",
                                         "BDF_S2N", "BDF_MAG_Z_CORRECTED"])
    mask = ((pf["BDF_S2N"] > 0) & (pf["BDF_MAG_Z_CORRECTED"] > 0) &
            (pf["DNF_Z"] > 0.005) & (pf["DNF_Z"] < 3.0))
    q = pf[mask]
    print(f"{len(q)} galaxies after quality cut")

    # Split by redshift
    fg = q[q["DNF_Z"] <= 0.4]
    ra = fg.RA.values; dec = fg.DEC.values
    print(f"{len(fg)} foreground (z<=0.4) galaxies for void statistics")

    # Count in cells: bin into N_cell x N_cell grid
    N_cell = 40
    H, xedges, yedges = np.histogram2d(ra, dec, bins=N_cell,
                                       range=[[ra.min(), ra.max()],
                                              [dec.min(), dec.max()]])
    # Mean and RMS
    mean_n = H.mean()
    std_n = H.std()
    print(f"Mean per cell: {mean_n:.1f}, std: {std_n:.1f}")

    # Underdensity distribution
    delta = (H - mean_n) / mean_n  # density contrast per cell
    delta = delta[~np.isnan(delta)]
    void_cells = delta < -0.5
    n_voids = void_cells.sum()
    void_depth = delta[void_cells].mean()
    print(f"Cells below -0.5 density: {n_voids} "
          f"(depth = {void_depth:.3f})")

    # IST prediction: the gravitational coupling G is suppressed
    # G_eff/G_N = supp_factor = 0.37 for D=phi at delta=-0.8
    # This means the mass deficit is effectively smaller ->
    # the count deficit should also be suppressed
    # Expected void depth: delta_IST = delta_GR * supp_factor
    gr_depth = delta[delta < -0.2].mean()
    ist_pred = gr_depth * SUPP_FACTOR
    print(f"GR-averaged depth (<-0.2): {gr_depth:.3f}")
    print(f"IST pinned prediction: {ist_pred:.3f} "
          f"(suppression = {SUPP_FACTOR:.3f})")
    print(f"Measured void depth (<-0.5): {void_depth:.3f}")
    print(f"Ratio (measured/GR): {void_depth/gr_depth:.3f}")

    # Save statistics
    with open(os.path.join(OUT_DIR, "void_statistics.csv"), "w",
              newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["statistic", "value"])
        w.writerow(["n_cells", N_cell])
        w.writerow(["n_void_cells", n_voids])
        w.writerow(["void_depth_measured", void_depth])
        w.writerow(["gr_average_depth", gr_depth])
        w.writerow(["ist_suppression", SUPP_FACTOR])
        w.writerow(["ist_predicted_depth", ist_pred])
        w.writerow(["depth_ratio_measured_gr", void_depth / gr_depth])

    make_figure(H, delta, N_cell, mean_n, SUPP_FACTOR,
                xedges, yedges, void_cells)
    print(f"Wrote {OUT_DIR} ({time.perf_counter()-t0:.0f}s)")


def make_figure(H, delta, N, mean_n, supp, xedges, yedges, void_cells):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    im = ax.imshow(np.log10(H + 1), origin="lower",
                   extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
                   cmap="viridis", aspect="auto")
    fig.colorbar(im, ax=ax, label="log10(count)", fraction=0.046)
    ax.set_title(f"A. Galaxy density ({N}x{N} grid)")

    ax = axes[0, 1]
    ax.hist(delta, bins=30, color="steelblue", alpha=0.7,
            label=f"all cells (mean={delta.mean():.2f})")
    ax.axvline(delta[delta < -0.5].mean(), color="crimson", ls="--",
               lw=2, label=f"void depth = {delta[delta<-0.5].mean():.3f}")
    ax.axvline(delta[delta < -0.2].mean() * supp, color="seagreen",
               ls="--", lw=2,
               label=f"IST pred = {delta[delta<-0.2].mean()*supp:.3f}")
    ax.set_xlabel("density contrast"); ax.set_ylabel("count")
    ax.set_title("B. Density contrast distribution")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    depths = sorted(delta[delta < 0])
    cumulative = np.arange(1, len(depths) + 1) / len(depths)
    ax.semilogy(-np.array(depths), cumulative, "-", color="crimson", lw=2)
    ax.set_xlabel("void depth |delta|"); ax.set_ylabel("cumulative fraction")
    ax.set_title("C. Void depth function")

    ax = axes[1, 1]
    # Mark void cells on the map
    vmap = np.zeros_like(H, dtype=float)
    vmap[void_cells.reshape(H.shape)] = 1
    ax.imshow(vmap, cmap="Reds", origin="lower", aspect="auto",
              extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
    ax.set_title(f"D. Void cells (< -0.5, n={void_cells.sum()})")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "count_in_cells.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
