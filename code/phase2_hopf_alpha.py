
"""
================================================================================
IST PHASE 2 - Deriving α from Hopf Fiber Geometry
================================================================================
Purpose:
    Build a discrete Hopf fibration S^1 -> S^3 -> S^2 as a principal U(1)
    bundle over a latitude-longitude base, verify its topology (Chern number,
    spectral dimension ~ 3), and compute the Kaluza-Klein fine-structure
    constant alpha = 4 / R_f^2 as a function of the fiber topology. The
    topological minimum (fiber_period = 3) gives a raw alpha ~ 17.5; the
    observed alpha ~ 1/137 requires an additional projection/magnification
    factor whose size is compared to the RG fixed-point predictions from
    Phase 1.

Inputs:   none (grid and fiber parameters are hardcoded / swept)
Outputs:
    code/outputs/phase2/alpha_sensitivity.png  - alpha vs fiber topology
    code/outputs/phase2/alpha_sensitivity.csv  - sweep data

References:
    notes/IST_Research_Plan_Phases_1-5.md   (Phase 2)
    main/ist_v5_3_topology_substrate.md     (§3.6.1 Hopf fibration + alpha)
    code/ist_toolkit_v2.py                  (ALPHA, ALPHA_INV, PHI)
    code/phase1_rg_flow.py                  (spectral_dimension helper)

Conventions:
    * Base S^2 is a latitude-longitude cellulation with a single vertex at
      each pole and n_lon vertices on each intermediate latitude circle.
    * Fiber over each base vertex is a discrete circle with fiber_period points.
    * Hopf connection 1-form discretized as
          A = (chern/2)(1 - cos theta) d phi
      so that parallel transport around a latitude theta circle rotates the
      fiber by chern*pi*(1 - cos theta).
    * All edges have unit plonk length; the fiber circumference is therefore
      fiber_period plonk units and the fiber radius is R_f = fiber_period/(2pi).
================================================================================
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp

from phase1_rg_flow import spectral_dimension
from ist_toolkit_v2 import ALPHA, ALPHA_INV, PHI

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase2")


def _theta(i_lat, n_lat):
    """Polar angle of latitude index i_lat in [0, n_lat-1]."""
    return np.pi * i_lat / (n_lat - 1)


class DiscreteHopfFibration:
    """Principal S^1 bundle over a discrete S^2 base.

    Parameters
    ----------
    n_lat : int
        Number of latitude divisions, including both poles (>= 3).
    n_lon : int
        Number of longitude divisions on each intermediate circle (>= 3).
    fiber_period : int
        Number of vertices on each S^1 fiber (>= 2).
    chern : int
        Chern number of the bundle (total twist over S^2).
    """

    def __init__(self, n_lat, n_lon, fiber_period, chern=1):
        if n_lat < 3 or n_lon < 3 or fiber_period < 2:
            raise ValueError("invalid discrete Hopf parameters")
        self.n_lat = n_lat
        self.n_lon = n_lon
        self.fiber_period = fiber_period
        self.chern = chern
        self.n_base = 2 + (n_lat - 2) * n_lon
        self.n_total = self.n_base * fiber_period

        self._build_base_indexing()
        self._build_adjacency()

    def _build_base_indexing(self):
        """Map (i_lat, i_lon) to a single base vertex id."""
        self.base_id = {}
        self.base_id[(0, 0)] = 0                     # north pole
        self.base_id[(self.n_lat - 1, 0)] = self.n_base - 1  # south pole
        for i_lat in range(1, self.n_lat - 1):
            for i_lon in range(self.n_lon):
                bid = 1 + (i_lat - 1) * self.n_lon + i_lon
                self.base_id[(i_lat, i_lon)] = bid

    def _bid(self, i_lat, i_lon):
        return self.base_id[(i_lat, i_lon % self.n_lon) if i_lat not in (0, self.n_lat - 1) else (i_lat, 0)]

    def _vid(self, bid, k):
        return bid * self.fiber_period + (k % self.fiber_period)

    def _shift_lon(self, i_lat):
        """Fiber shift for one eastward longitude step at latitude i_lat."""
        theta = _theta(i_lat, self.n_lat)
        phase = self.chern * np.pi * (1.0 - np.cos(theta)) / self.n_lon
        return int(round(self.fiber_period * phase / (2.0 * np.pi)))

    def _add_edge(self, edges, u, v):
        if u == v:
            return
        edges.append((u, v))
        edges.append((v, u))

    def _build_adjacency(self):
        edges = set()
        for i_lat in range(self.n_lat):
            for i_lon in range(self.n_lon):
                bid = self._bid(i_lat, i_lon)
                # S^1 fiber cycle at this base point
                for k in range(self.fiber_period):
                    edges.add(frozenset({self._vid(bid, k), self._vid(bid, k + 1)}))

                if i_lat in (0, self.n_lat - 1):
                    continue

                # Longitude edges (twisted by the Hopf connection)
                dk = self._shift_lon(i_lat)
                bid_east = self._bid(i_lat, i_lon + 1)
                for k in range(self.fiber_period):
                    edges.add(frozenset({self._vid(bid, k), self._vid(bid_east, k + dk)}))

                # Latitude edges (untwisted, meridional)
                if i_lat == 1:
                    bid_north = self._bid(0, 0)
                    for k in range(self.fiber_period):
                        edges.add(frozenset({self._vid(bid, k), self._vid(bid_north, k)}))
                else:
                    bid_north = self._bid(i_lat - 1, i_lon)
                    for k in range(self.fiber_period):
                        edges.add(frozenset({self._vid(bid, k), self._vid(bid_north, k)}))

        pairs = [tuple(e) for e in edges]
        rows, cols = [], []
        for u, v in pairs:
            rows.extend([u, v])
            cols.extend([v, u])
        data = np.ones(len(rows))
        self.A = sp.csr_matrix((data, (rows, cols)), shape=(self.n_total, self.n_total))
        degrees = np.asarray(self.A.sum(axis=1)).ravel()
        self.L = sp.diags(degrees) - self.A

    def laplacian(self):
        return self.L

    def chern_number(self):
        """Total holonomy north-to-south / fiber_period (continuum definition).

        The holonomy around a latitude circle theta is
            H(theta) = fiber_period * chern * (1 - cos theta) / 2 .
        Integrating from the north pole (H=0) to the south pole (H=fiber_period*chern)
        gives Chern number = (H_north - H_south) / fiber_period = -chern.
        """
        H_north = 0
        H_south = round(self.fiber_period * self.chern * (1.0 - np.cos(np.pi)) / 2.0)
        return abs(int(round((H_north - H_south) / self.fiber_period)))

    def fiber_radius(self):
        """Fiber radius in plonk units for a circular fiber."""
        return self.fiber_period / (2.0 * np.pi)

    def alpha_raw(self):
        """Kaluza-Klein alpha from the bare fiber radius."""
        Rf = self.fiber_radius()
        return 4.0 / (Rf * Rf)

    def alpha_inverse_raw(self):
        return 1.0 / self.alpha_raw()


def sweep(fiber_periods=None, n_lat=7, n_lon=12, chern=1):
    """Sweep fiber_period and collect topology/alpha data."""
    if fiber_periods is None:
        fiber_periods = np.arange(1, 31)
    rows = []
    for fp in fiber_periods:
        if fp < 2:
            continue
        h = DiscreteHopfFibration(n_lat, n_lon, fp, chern)
        D, r2, _, _ = spectral_dimension(h.laplacian(), window_low=0.1, window_high=0.5)
        rows.append({
            "fiber_period": fp,
            "chern": chern,
            "n_base": h.n_base,
            "n_total": h.n_total,
            "cher_number_computed": h.chern_number(),
            "spectral_dim": D,
            "spectral_dim_r2": r2,
            "fiber_radius": h.fiber_radius(),
            "alpha_raw": h.alpha_raw(),
            "alpha_inv_raw": h.alpha_inverse_raw(),
        })
    return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    rows = sweep(n_lat=7, n_lon=12, chern=1)
    csv_path = os.path.join(OUT_DIR, "alpha_sensitivity.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {csv_path}")

    # Reference values
    fp3 = next(r for r in rows if r["fiber_period"] == 3)
    Rf_obs = 2.0 / np.sqrt(ALPHA)
    fp_needed = int(round(2.0 * np.pi * Rf_obs))
    magnification = Rf_obs / fp3["fiber_radius"]

    print(f"\nObserved alpha^{-1} = {ALPHA_INV:.9f}")
    print(f"Observed fiber radius R_f = 2/sqrt(alpha) = {Rf_obs:.3f} plonk units")
    print(f"Topological minimum fiber_period = 3 -> R_f = {fp3['fiber_radius']:.4f}")
    print(f"Raw alpha^{-1} at fiber_period=3 = {fp3['alpha_inv_raw']:.3f}")
    print(f"Magnification factor needed = {magnification:.2f}")
    print(f"Fiber period needed to match observed alpha = ~{fp_needed}")
    print(f"phi^8 = {PHI**8:.2f}  |  magnification / phi^8 = {magnification / PHI**8:.3f}")

    make_figure(rows, Rf_obs, fp_needed)


def make_figure(rows, Rf_obs, fp_needed):
    fps = np.array([r["fiber_period"] for r in rows])
    alpha_inv_raw = np.array([r["alpha_inv_raw"] for r in rows])
    Rf = np.array([r["fiber_radius"] for r in rows])

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    ax = axes[0]
    ax.plot(fps, alpha_inv_raw, "o-", color="steelblue", label=r"raw $\alpha^{-1} = (p/2\pi)^2/4$")
    ax.axhline(ALPHA_INV, color="crimson", ls="--", label=f"observed $\\alpha^{{-1}}$ = {ALPHA_INV:.3f}")
    ax.axvline(3, color="k", ls=":", alpha=0.5, label="topological minimum $p=3$")
    ax.axvline(fp_needed, color="crimson", ls=":", alpha=0.5, label=f"required $p \\approx {fp_needed}$")
    ax.set_xlabel("fiber period $p$ (plonk units)")
    ax.set_ylabel(r"raw $\alpha^{-1}$")
    ax.set_title(r"A. Raw Kaluza-Klein $\alpha^{-1}$ vs fiber topology")
    ax.set_yscale("log")
    ax.legend(fontsize=8)

    ax = axes[1]
    ax.plot(fps, Rf, "o-", color="steelblue", label=r"$R_f = p/(2\pi)$")
    ax.axhline(Rf_obs, color="crimson", ls="--", label=f"observed $R_f$ = {Rf_obs:.2f}")
    ax.axvline(3, color="k", ls=":", alpha=0.5)
    ax.axvline(fp_needed, color="crimson", ls=":", alpha=0.5)
    ax.set_xlabel("fiber period $p$ (plonk units)")
    ax.set_ylabel(r"fiber radius $R_f$ (plonk units)")
    ax.set_title("B. Fiber radius vs fiber topology")
    ax.legend(fontsize=8)

    fig.tight_layout()
    path = os.path.join(OUT_DIR, "alpha_sensitivity.png")
    fig.savefig(path, dpi=300)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
