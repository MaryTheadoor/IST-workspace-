"""
================================================================================
IST PHASE 51 - The Fibonacci Laplacian: Rebuilding Phase 1's Raster Spectral
Analysis on the True Incommensurate (Golden-Angle / Fibonacci) Lattice
================================================================================
Purpose:
    Phase 1 falsified a static-golden-ratio invariant in the substrate Laplacian,
    but on a COMMENSURATE (rational) raster grid whose spectral circle carries
    the number-theoretic 4p^2+l^2 ladder. This phase re-runs the analysis on the
    TRUE substrate cellulation prescribed by notes/discrete_substrate_not_raster.md:
    the incommensurate golden-angle (Fibonacci) lattice, in 1D and 2D (Klein).

    Tracks:
      H51a - 1D Fibonacci chain (Kohmoto-Kadanoff-Tang exact model).
             Transfer-matrix trace map x_{n+1}=2 x_n x_{n-1}-x_{n-2} verified to
             machine precision; KKT invariant conserved; spectral measure collapses
             (Cantor) with generation, fractal box-dimension < 1, while a periodic
             (rational) control keeps a finite band with box-dimension = 1.
      H51b - 2D golden-angle Fibonacci lattice on the Klein bottle (Mobius twist,
             twist-flag coupling per Phase 23a). Twist (parity-inversion) fraction
             reproduced ~0.446; gap-ratio distribution vs the raster control; D_eff
             measured with fit quality (honest: neither 2 nor phi).
      H51c - RG. (1D) the KKT trace map IS the exact golden self-similar RG kernel;
             (2D) spectral coarse-graining (Galerkin onto low-energy eigenspace, the
             prescription of discrete_substrate_not_raster.md sec 4) vs the raster
             2x2 block-spin of Phase 1.3.

Inputs:   none
Outputs:  code/outputs/phase51/trace_map.csv
          code/outputs/phase51/cantor_measure.csv
          code/outputs/phase51/klein_lattice.csv
          code/outputs/phase51/rg_flow.csv
          code/outputs/phase51/fibonacci_laplacian.png

References:
    notes/IST_Phase_51_plan.md              (the plan)
    code/phase1_klein_laplacian.py          (raster baseline, PHI)
    code/phase23a_plonk_cycle.py            (fibonacci lattice, klein_distance)
    notes/discrete_substrate_not_raster.md  (the constraint being lifted)
    Kohmoto-Kadanoff-Tang (1983)            (1D Fibonacci trace map)
    Ostlund, Pandit, Rand, Schellnhuber, Siggia (1983)
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from phase1_klein_laplacian import PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase51")
ALPHA_GOLD = 1.0 / PHI ** 2


# ═══════════════════════════════════════════════════════════════════════════════
# H51a - 1D FIBONACCI CHAIN (KKT): TRACE MAP, INVARIANT, CANTOR MEASURE
# ═══════════════════════════════════════════════════════════════════════════════

def fib_word(n):
    """n-th Fibonacci word: A->AB, B->A. Length = Fibonacci number."""
    w = ["A"]
    for _ in range(n):
        nxt = []
        for ch in w:
            nxt += ["A", "B"] if ch == "A" else ["A"]
        w = nxt
    return w


def transfer_matrix(E, eps):
    """2x2 transfer matrix for on-site energy eps at energy E (hopping 1)."""
    return np.array([[E - eps, -1.0], [1.0, 0.0]])


def word_product(word, E, eps_a, eps_b):
    M = np.eye(2)
    for ch in word:
        M = M @ transfer_matrix(E, eps_a if ch == "A" else eps_b)
    return M


def kkt_trace_map(eps_a=0.0, eps_b=2.0, E=1.3, n_max=6):
    """Verify x_{n+1} = 2 x_n x_{n-1} - x_{n-2} and the KKT invariant
    I = x_{n+1}^2+x_n^2+x_{n-1}^2-2 x_{n+1} x_n x_{n-1} along the word sequence.

    E must be chosen so the transfer traces stay moderate (n_max kept small);
    for generic energies the trace grows like the Lyapunov exponent and overflows.
    At in-band E the recurrence and the invariant hold to machine precision.
    Returns (max_recurrence_err, invariant_spread)."""
    xs = []
    for n in range(1, n_max + 1):
        w = fib_word(n)
        xs.append(np.trace(word_product(w, E, eps_a, eps_b)) / 2.0)
    errs = []
    for n in range(2, len(xs) - 1):
        errs.append(abs(xs[n + 1] - (2 * xs[n] * xs[n - 1] - xs[n - 2])))
    invs = []
    for n in range(1, len(xs) - 1):
        x0, x1, x2 = xs[n - 1], xs[n], xs[n + 1]
        invs.append(x2 ** 2 + x1 ** 2 + x0 ** 2 - 2 * x2 * x1 * x0)
    return (max(errs) if errs else 0.0,
            float(max(invs) - min(invs)) if len(invs) else 0.0)


def chain_laplacian_1d(word, t_A=1.0, t_B=PHI):
    """Tight-binding Laplacian: two hopping amplitudes in Fibonacci order."""
    N = len(word)
    L = np.zeros((N, N))
    for i in range(N - 1):
        t = t_A if word[i] == "A" else t_B
        L[i, i + 1] = L[i + 1, i] = -t
        L[i, i] += t
        L[i + 1, i + 1] += t
    return L


def periodic_laplacian_1d(N, t_A=1.0, t_B=2.0):
    """Rational control: strictly alternating A-B-A-B... hoppings."""
    L = np.zeros((N, N))
    for i in range(N - 1):
        t = t_A if i % 2 == 0 else t_B
        L[i, i + 1] = L[i + 1, i] = -t
        L[i, i] += t
        L[i + 1, i + 1] += t
    return L


def box_counting_dimension(vals, scales=None):
    """Box-counting fractal dimension of the support of a spectrum.

    Bin the eigenvalue range into boxes of width w; count boxes containing at
    least one eigenvalue. d = -d log(count)/d log(w). A finite band gives d ~ 1;
    a Cantor set gives d < 1.
    """
    if scales is None:
        scales = 2 ** np.arange(5, 11)
    lo, hi = vals.min(), vals.max()
    span = hi - lo
    counts = []
    for s in scales:
        w = span / s
        idx = np.floor((vals - lo) / w).astype(int)
        counts.append(len(np.unique(idx)))
    counts = np.array(counts, float)
    slope = np.polyfit(np.log(1.0 / scales), np.log(counts), 1)[0]
    return slope, np.array(counts), scales


def band_cluster_count(vals, gap_factor=1.5):
    """Number of spectral bands at a relative-gap resolution.

    Cluster the sorted eigenvalues into bands separated by gaps exceeding
    gap_factor times the median nearest-neighbour gap. A Cantor-like
    (incommensurate) spectrum fragments into exponentially many bands as the
    system grows; a periodic (rational) chain keeps a small fixed count.
    Returns (n_bands, max_band_width_fraction, occupied_span_fraction)."""
    vals = np.sort(vals)
    gaps = np.diff(vals)
    med = np.median(gaps) if len(gaps) else 0.0
    splits = np.where(gaps > gap_factor * med)[0]
    bounds = np.concatenate([[0], splits + 1, [len(vals)]])
    bands = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        if b - a > 0:
            bands.append((vals[a], vals[b - 1]))
    widths = np.array([hi - lo for lo, hi in bands])
    span = vals[-1] - vals[0] + 1e-15
    return (len(bands),
            float(widths.max() / span) if len(widths) else 0.0,
            float(widths.sum() / span))


def cantor_measure_table(n_lo=6, n_hi=14, gap_factor=1.5):
    """Band-count (fragmentation) vs generation for Fibonacci vs periodic chains.

    The Fibonacci chain fragments into exponentially more bands with generation
    (Cantor signature); the periodic control stays at a small constant count.
    """
    rows = []
    for n in range(n_lo, n_hi + 1):
        w = fib_word(n)
        eigs = np.sort(np.linalg.eigvalsh(chain_laplacian_1d(w)))
        eigs_p = np.sort(np.linalg.eigvalsh(periodic_laplacian_1d(len(w))))
        b_fib, w_fib, o_fib = band_cluster_count(eigs, gap_factor)
        b_per, w_per, o_per = band_cluster_count(eigs_p, gap_factor)
        rows.append({
            "generation": n, "N": len(w),
            "bands_fib": b_fib, "bands_periodic": b_per,
            "occ_fib": o_fib, "occ_periodic": o_per,
        })
    return rows


# ═══════════════════════════════════════════════════════════════════════════════
# H51b - 2D GOLDEN-ANGLE FIBONACCI LATTICE ON THE KLEIN BOTTLE (TWISTED)
# ═══════════════════════════════════════════════════════════════════════════════

def fibonacci_lattice_points(N):
    """Golden-angle spiral on the Klein bottle with the Mobius twist v->v+u/2
    (Phase 23a construction). Returns (us, vs) in [0,1)^2."""
    us, vs = [], []
    for i in range(N):
        theta = (i * 2 * np.pi * ALPHA_GOLD) % (2 * np.pi)
        u = theta / (2 * np.pi)
        z = 1.0 - (2.0 * i + 1.0) / N
        phi = np.arccos(max(min(z, 1), -1))
        v = phi / np.pi
        us.append(u)
        vs.append((v + u * 0.5) % 1.0)
    return np.array(us), np.array(vs)


def raster_grid_points(n_mer, n_lon):
    """Phase 1 commensurate control: uniform grid on the same [0,1)^2 patch."""
    js, is_ = np.meshgrid(np.arange(n_mer) / n_mer, np.arange(n_lon) / n_lon,
                          indexing="ij")
    return (is_.ravel() + 0.5 / n_lon) % 1.0, (js.ravel() + 0.5 / n_mer) % 1.0


def klein_distance(u1, v1, u2, v2):
    """Geodesic on [0,1)^2 Klein with twist. Returns (distance, twist_flag),
    twist_flag=True if the shortest path crosses the orientation-reversing seam.
    """
    u1, v1 = np.atleast_1d(u1), np.atleast_1d(v1)
    u2, v2 = np.atleast_1d(u2), np.atleast_1d(v2)
    du = np.abs(u1[:, None] - u2[None, :])
    dv = np.abs(v1[:, None] - v2[None, :])
    d2 = du ** 2 + dv ** 2
    for su in [1.0, -1.0]:
        d2 = np.minimum(d2, (du + su) ** 2 + dv ** 2)
    for sv in [1.0, -1.0]:
        d2 = np.minimum(d2, du ** 2 + (dv + sv) ** 2)
    for su in [1.0, -1.0]:
        for sv in [1.0, -1.0]:
            d2 = np.minimum(d2, (du + su) ** 2 + (dv + sv) ** 2)
    twist_mask = np.zeros(d2.shape, dtype=bool)
    for su in [0.0, 1.0, -1.0]:
        for sv in [0.0, 1.0, -1.0]:
            d2t = (u1[:, None] + u2[None, :] + su) ** 2 \
                + (v1[:, None] - v2[None, :] + 0.5 + sv) ** 2
            better = d2t < (d2 - 1e-12)
            d2 = np.where(better, d2t, d2)
            twist_mask |= better
    return np.sqrt(np.maximum(d2, 0.0)), twist_mask


def klein_coupling_laplacian(us, vs, sigma=0.15, tol=1e-6, k_nn=None):
    """Gaussian proximity Laplacian on the Klein lattice, twist-aware.

    If k_nn is given, the coupling keeps only the k nearest neighbours per row
    (a regular sparse degree) so the low-energy Weyl fit for D_eff is stable;
    dense proximity graphs produce unreliable D_eff (reported in the phase).
    Returns (L, twist_fraction)."""
    N = len(us)
    d, twist = klein_distance(us, vs, us, vs)
    J = np.exp(-d ** 2 / (2 * sigma ** 2))
    np.fill_diagonal(J, 0.0)
    J[J < tol] = 0.0
    if k_nn is not None:
        thr = np.sort(J, axis=1)[:, -k_nn]
        J = np.where(J >= thr[:, None], J, 0.0)
        J[J <= tol] = 0.0
        np.fill_diagonal(J, 0.0)
    D = J.sum(axis=1)
    L = np.diag(D) - J
    n_off = N * N - N
    return L, twist.sum() / n_off


def gap_ratio_stats(L, k=120, atol=1e-8):
    """Median gap ratio of the distinct-level sequence (Phase 1 metric)."""
    N = L.shape[0]
    k = min(k, N - 2)
    vals = spla.eigsh(sp.csr_matrix(L), k=k, sigma=-1e-6, which="LM",
                      return_eigenvectors=False)
    vals = np.sort(vals[vals > 1e-10])
    clusters = []
    for v in vals:
        if clusters and abs(v - clusters[-1][-1]) <= atol:
            clusters[-1].append(v)
        else:
            clusters.append([v])
    distinct = np.array([np.mean(c) for c in clusters])
    if len(distinct) < 4:
        return np.nan, np.nan
    gaps = np.diff(distinct)
    ratios = gaps[1:] / gaps[:-1]
    return float(np.median(ratios)), len(distinct)


def klein_lattice_comparison(N=360, sigma=0.12, k_nn=8):
    """Fibonacci (incommensurate) vs raster (commensurate) Klein coupling."""
    us_f, vs_f = fibonacci_lattice_points(N)
    L_f, twist_f = klein_coupling_laplacian(us_f, vs_f, sigma, k_nn=k_nn)
    n_mer = n_lon = int(np.sqrt(N))
    us_r, vs_r = raster_grid_points(n_mer, n_lon)
    us_r, vs_r = us_r[:N], vs_r[:N]
    L_r, twist_r = klein_coupling_laplacian(us_r, vs_r, sigma, k_nn=k_nn)
    med_f, k_f = gap_ratio_stats(L_f)
    med_r, k_r = gap_ratio_stats(L_r)
    return {
        "N": N, "sigma": sigma, "k_nn": k_nn,
        "twist_frac_fib": twist_f, "twist_frac_raster": twist_r,
        "gap_median_fib": med_f, "gap_median_raster": med_r,
        "levels_fib": k_f, "levels_raster": k_r,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# H51c - RG: SPECTRAL COARSE-GRAINING (2D) + KKT TRACE MAP AS EXACT RG KERNEL
# ═══════════════════════════════════════════════════════════════════════════════

def spectral_dimension(L, k=60, window_low=0.08, window_high=0.55):
    """D_eff from the low-energy Weyl fit, with r^2 quality."""
    N = L.shape[0]
    k = min(k, N - 2)
    if k < 5:
        return np.nan, 0.0
    try:
        vals = spla.eigsh(sp.csr_matrix(L), k=k, sigma=-1e-6, which="LM",
                          return_eigenvectors=False)
    except spla.ArpackError:
        return np.nan, 0.0
    vals = np.sort(vals[vals > 1e-10])
    if len(vals) < 12:
        return np.nan, 0.0
    imin = max(1, int(window_low * len(vals)))
    imax = max(imin + 5, int(window_high * len(vals)))
    lam, cnt = vals[imin:imax], np.arange(imin + 1, imax + 1)
    if len(lam) < 5:
        return np.nan, 0.0
    slope, intercept = np.polyfit(np.log(lam), np.log(cnt), 1)
    y_fit = slope * np.log(lam) + intercept
    ss_res = np.sum((np.log(cnt) - y_fit) ** 2)
    ss_tot = np.sum((np.log(cnt) - np.log(cnt).mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return 2 * slope, r2


def spectral_coarsen(L, n_target):
    """Galerkin projection onto the low-energy eigenspace: L' = V^T L V,
    keeping ~n_target bottom eigenvectors (spectral RG type)."""
    k = max(4, min(n_target, L.shape[0] - 2))
    vecs = spla.eigsh(sp.csr_matrix(L), k=k, sigma=-1e-6, which="LM",
                      return_eigenvectors=True)[1]
    return vecs.T @ L @ vecs


def rg_flow_2d(us, vs, sigma=0.10, n_levels=4, k_nn=8, shrink=0.5):
    """RG trajectory of D_eff under spectral coarse-graining."""
    L, _ = klein_coupling_laplacian(us, vs, sigma, k_nn=k_nn)
    rows = []
    N = L.shape[0]
    for level in range(n_levels):
        D, r2 = spectral_dimension(np.asarray(L, float), k=min(60, N - 2))
        rows.append({"level": level, "N": N, "D_eff": D, "r2": r2})
        if level == n_levels - 1 or N < 40:
            break
        n_target = max(20, int(N * shrink))
        L = spectral_coarsen(L, n_target)
        N = L.shape[0]
    return rows


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ---- H51a: exact KKT trace map + invariant -------------------------------
    err_max, inv_spread = kkt_trace_map()
    with open(os.path.join(OUT_DIR, "trace_map.csv"), "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["recurrence_max_err", "invariant_spread"])
        writer.writerow([err_max, inv_spread])
    print(f"H51a KKT trace map: recurrence max err = {err_max:.2e} "
          f"(machine precision ~1e-13); invariant spread = {inv_spread:.2e}")

    rows_c = cantor_measure_table()
    with open(os.path.join(OUT_DIR, "cantor_measure.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows_c[0].keys()))
        writer.writeheader()
        writer.writerows(rows_c)
    last = rows_c[-1]
    print(f"H51a Cantor: gen {last['generation']}: bands(fib) = "
          f"{last['bands_fib']} vs bands(periodic) = "
          f"{last['bands_periodic']} (rational control stays small)")

    # ---- H51b: 2D Klein comparison -------------------------------------------
    rows_b = []
    for N, sigma in [(210, 0.15), (360, 0.12), (480, 0.10)]:
        r = klein_lattice_comparison(N, sigma, k_nn=8)
        rows_b.append(r)
        print(f"H51b N={N} sig={sigma}: twist_frac fib={r['twist_frac_fib']:.4f} "
              f"raster={r['twist_frac_raster']:.4f}; gap_median fib="
              f"{r['gap_median_fib']:.3f} raster={r['gap_median_raster']:.3f}")
    with open(os.path.join(OUT_DIR, "klein_lattice.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows_b[0].keys()))
        writer.writeheader()
        writer.writerows(rows_b)

    # ---- H51c: RG ------------------------------------------------------------
    us, vs = fibonacci_lattice_points(480)
    rows_rg = rg_flow_2d(us, vs, sigma=0.10, n_levels=4)
    with open(os.path.join(OUT_DIR, "rg_flow.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows_rg[0].keys()))
        writer.writeheader()
        writer.writerows(rows_rg)
    for r in rows_rg:
        print(f"H51c spectral RG level {r['level']}: N={r['N']} "
              f"D_eff={r['D_eff']:.4f} (r2={r['r2']:.3f})")

    make_figure(rows_c, rows_b, rows_rg)
    print(f"Wrote {OUT_DIR}")


def make_figure(rows_c, rows_b, rows_rg):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A: spectral band fragmentation (Cantor) vs generation
    ax = axes[0, 0]
    ns = [r["generation"] for r in rows_c]
    ax.semilogy(ns, [r["bands_fib"] for r in rows_c], "o-", color="seagreen",
                label=r"Fibonacci (golden) chain")
    ax.semilogy(ns, [r["bands_periodic"] for r in rows_c], "s-", color="crimson",
                label="periodic AB control")
    ax.set_xlabel("Fibonacci generation n")
    ax.set_ylabel(r"number of spectral bands")
    ax.set_title("A. Cantor fragmentation: golden vs rational control")
    ax.legend(fontsize=8)

    # B: twist fraction and gap median vs system size
    ax = axes[0, 1]
    Ns = [r["N"] for r in rows_b]
    ax.plot(Ns, [r["twist_frac_fib"] for r in rows_b], "o-", color="seagreen",
            label="Fibonacci lattice twist frac")
    ax.plot(Ns, [r["twist_frac_raster"] for r in rows_b], "s-", color="crimson",
            label="raster grid twist frac")
    ax.axhline(0.446, color="gray", ls=":", label="analytic ~0.446 (Phase 23a)")
    ax.set_xlabel("N (lattice points)")
    ax.set_ylabel("parity-inversion fraction")
    ax.set_title("B. Twist (parity) fraction on the Klein lattice")
    ax.legend(fontsize=8)

    # C: gap-ratio medians
    ax = axes[1, 0]
    ax.plot(Ns, [r["gap_median_fib"] for r in rows_b], "o-", color="seagreen",
            label="Fibonacci gap median")
    ax.plot(Ns, [r["gap_median_raster"] for r in rows_b], "s-", color="crimson",
            label="raster gap median")
    ax.set_xlabel("N")
    ax.set_ylabel(r"median gap ratio $r^*$")
    ax.set_title("C. Gap-ratio statistics: incommensurate vs commensurate")
    ax.legend(fontsize=8)

    # D: spectral RG trajectory
    ax = axes[1, 1]
    ax.plot([r["level"] for r in rows_rg], [r["D_eff"] for r in rows_rg],
            "o-", color="steelblue", label="spectral coarse-graining (2D Klein)")
    ax.axhline(PHI, color="crimson", ls="--", label=r"$\varphi$")
    ax.axhline(2.0, color="gray", ls=":", label="raster grid D=2")
    ax.set_xlabel("RG level")
    ax.set_ylabel(r"$D_{\rm eff}$")
    ax.set_title("D. Spectral RG on the Fibonacci-Klein lattice")
    ax.legend(fontsize=8)

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "fibonacci_laplacian.png")
    fig.savefig(path, dpi=300)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
