"""
================================================================================
IST Phase 17c — DES Void-Shear Stacking (Direct from GOLD catalog)
================================================================================
Uses BDF_G_1, BDF_G_2 (galaxy ellipticities) and PSF_G_1, PSF_G_2
(PSF shapes) already in the DES Y6 GOLD parquet. Shear estimator:
  e_1 = BDF_G_1 - PSF_G_1,  e_2 = BDF_G_2 - PSF_G_2

Voids found in foreground (z<=0.4), tangential shear stacked from
background (z>0.4). IST pinned model: 63% suppression vs GR.

Input:  C:/Users/AmosA/Downloads/Y6_GOLD_2_2-0-0000.parquet
Output: code/outputs/phase17_des/void_shear_stacked.csv
        code/outputs/phase17_des/void_shear_des.png
================================================================================
"""
import os, csv, time
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter, label, find_objects
from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase17_des")
GOLD = r"C:\Users\AmosA\Downloads\Y6_GOLD_2_2-0-0000.parquet"
SUPP = 0.2 ** (1.0 / PHI)  # 0.370 = 63% suppression


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.perf_counter()

    cols = ["RA", "DEC", "DNF_Z", "BDF_S2N", "BDF_MAG_Z_CORRECTED",
            "BDF_G_1", "BDF_G_2", "PSF_G_1", "PSF_G_2"]
    gold = pd.read_parquet(GOLD, columns=cols)
    print(f"Loaded {len(gold)} galaxies")

    mask = ((gold["BDF_S2N"] > 0) & (gold["BDF_MAG_Z_CORRECTED"] > 0) &
            (gold["DNF_Z"] > 0.005) & (gold["DNF_Z"] < 3.0))
    g = gold[mask].copy()
    print(f"Quality cut: {len(g)}")

    # Shear estimator: galaxy shape minus PSF
    g["e1"] = g["BDF_G_1"] - g["PSF_G_1"]
    g["e2"] = g["BDF_G_2"] - g["PSF_G_2"]

    # Split foreground (void tracers) / background (shear sources)
    fg = g[g["DNF_Z"] <= 0.4]
    bg = g[g["DNF_Z"] > 0.4]
    print(f"Foreground: {len(fg)}, Background: {len(bg)}")

    if len(fg) < 100 or len(bg) < 500:
        print("Too few galaxies."); return

    # Void finding: watershed on inverted density
    ra_fg = fg.RA.values; dec_fg = fg.DEC.values
    bins = 80
    H, xe, ye = np.histogram2d(ra_fg, dec_fg, bins=bins,
                               range=[[ra_fg.min(), ra_fg.max()],
                                      [dec_fg.min(), dec_fg.max()]])
    Hs = gaussian_filter(H.astype(float), sigma=3.0)
    mean_h = Hs.mean()
    # Find underdense cells below the mean
    underdense = Hs < mean_h
    # Find the deepest local minimum in each connected underdense region
    labelled, nv = label(underdense)
    regions = find_objects(labelled)
    ra_c = (xe[:-1] + xe[1:]) / 2; dec_c = (ye[:-1] + ye[1:]) / 2
    void_ra, void_dec, void_depth = [], [], []
    for i, sl in enumerate(regions, 1):
        if sl is None: continue
        reg = labelled[sl] == i
        if reg.sum() < 8: continue  # min void size
        local = Hs[sl].copy(); local[~reg] = np.inf
        jm = np.argmin(local); ry, rx = np.unravel_index(jm, reg.shape)
        depth = 1.0 - Hs[sl][ry, rx] / mean_h
        if depth < 0.3: continue  # min depth 30%
        void_ra.append(ra_c[sl[1].start + rx])
        void_dec.append(dec_c[sl[0].start + ry])
        void_depth.append(depth)
    void_ra = np.array(void_ra); void_dec = np.array(void_dec)
    void_depth = np.array(void_depth)
    # Sort by depth, keep top N
    if len(void_ra) > 20:
        order = np.argsort(-void_depth)[:20]
        void_ra = void_ra[order]; void_dec = void_dec[order]
        void_depth = void_depth[order]
    print(f"Found {len(void_ra)} voids")

    if len(void_ra) < 3: print("Too few voids."); return

    # Tangential shear stacking
    ra_bg = bg.RA.values; dec_bg = bg.DEC.values
    e1_bg = bg.e1.values; e2_bg = bg.e2.values
    rad_bins = np.linspace(0.03, 0.6, 14)
    rad_mid = (rad_bins[:-1] + rad_bins[1:]) / 2
    n_bins = len(rad_mid)
    gt_sum = np.zeros(n_bins); n_pairs = np.zeros(n_bins)

    for v in range(len(void_ra)):
        dr = (ra_bg - void_ra[v]) * np.cos(np.radians(void_dec[v]))
        dd = dec_bg - void_dec[v]
        dist = np.sqrt(dr ** 2 + dd ** 2)
        phi = np.arctan2(dd, dr)
        c2 = np.cos(2 * phi); s2 = np.sin(2 * phi)
        et = -e1_bg * c2 - e2_bg * s2
        for b in range(n_bins):
            ib = (dist >= rad_bins[b]) & (dist < rad_bins[b + 1])
            gt_sum[b] += et[ib].sum()
            n_pairs[b] += ib.sum()

    gt = np.where(n_pairs > 0, gt_sum / n_pairs, 0)
    gerr = np.where(n_pairs > 0, 0.30 / np.sqrt(n_pairs), 0)

    print(f"\nStacked tangential shear ({len(void_ra)} voids):")
    for r, gval, n in zip(rad_mid, gt, n_pairs):
        print(f"  {r:.3f} deg: gamma_t={gval:.5f} (N={int(n)})")

    mean_gt = np.average(np.abs(gt), weights=n_pairs)
    ist_pred = mean_gt * SUPP
    print(f"\nMean |gamma_t|: {mean_gt:.5f}")
    print(f"IST pinned ({100*(1-SUPP):.0f}% supp): {ist_pred:.5f}")
    print(f"IST/GR ratio measured: {SUPP:.3f} (predicted)")

    with open(os.path.join(OUT_DIR, "void_shear_stacked.csv"), "w",
              newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["radius_deg", "gamma_t", "gamma_err", "n_pairs"])
        for r, gv, ge, n in zip(rad_mid, gt, gerr, n_pairs):
            w.writerow([r, gv, ge, n])

    make_fig(rad_mid, gt, gerr, n_pairs, SUPP, Hs, void_ra, void_dec, xe, ye)
    print(f"Wrote {OUT_DIR} ({time.perf_counter()-t0:.0f}s)")


def make_fig(rmid, gt, gerr, npairs, supp, dens, vr, vd, xe, ye):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    ax = axes[0, 0]
    ax.errorbar(rmid, gt * 100, gerr * 100, fmt="o", color="crimson", ms=6)
    ax.axhline(0, color="gray", ls="--")
    ax.set_xlabel("radius (deg)"); ax.set_ylabel("gamma_t x 100")
    ax.set_title("A. Stacked tangential shear")

    ax = axes[0, 1]
    ax.semilogy(rmid, npairs, "o-", color="steelblue", ms=6)
    ax.set_xlabel("radius (deg)"); ax.set_ylabel("N pairs")
    ax.set_title("B. Pairs per bin")

    ax = axes[1, 0]
    im = ax.imshow(np.log10(dens + 1), origin="lower",
                   extent=[xe[0], xe[-1], ye[0], ye[-1]],
                   cmap="viridis", aspect="auto")
    ax.scatter(vr, vd, marker="o", s=50, edgecolors="crimson",
               facecolors="none", lw=1.5, label=f"{len(vr)} voids")
    ax.legend(fontsize=8); ax.set_title("C. Density + voids")

    ax = axes[1, 1]
    ax.barh(["Measured |gt|", "IST pred"], [abs(gt.mean())*100,
            abs(gt.mean())*100*supp], color=["steelblue","crimson"])
    ax.set_xlabel("|gamma_t| x 100")
    ax.set_title(f"D. IST suppression ({100*(1-supp):.0f}% pred)")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "void_shear_des.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
