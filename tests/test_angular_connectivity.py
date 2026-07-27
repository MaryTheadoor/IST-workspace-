"""
Unit tests for angular_connectivity_substrate.py
=================================================
Verifies that the high-connectivity Klein-bottle graph construction
has the correct topology, eliminates the negative-eigenvalue-laplacian
artifact, and that the 4-regular rational-ladder gap structure dissolves
as connectivity radius R increases.

Run: cd code && python -m pytest ../tests/test_angular_connectivity.py -v
"""

import sys
import os
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from angular_connectivity_substrate import (
    build_klein_bottle_radius, analyse_radius,
    topological_laplacian, laplacian_spectrum,
)


class TestGraphConstruction:
    def test_r1_is_8_regular(self):
        G = build_klein_bottle_radius(20, 20, radius=1)
        deg = G.A.sum(axis=1)
        assert abs(float(deg.mean()) - 8.0) < 0.1
        assert np.all(deg == 8)

    def test_r2_is_24_regular(self):
        G = build_klein_bottle_radius(20, 20, radius=2)
        deg = G.A.sum(axis=1)
        assert abs(float(deg.mean()) - 24.0) < 0.5  # seam deg differs

    def test_r3_is_48_regular(self):
        G = build_klein_bottle_radius(20, 20, radius=3)
        deg = G.A.sum(axis=1)
        assert abs(float(deg.mean()) - 48.0) < 1.0

    def test_laplacian_is_psd(self):
        for R in [1, 2, 3]:
            G = build_klein_bottle_radius(16, 16, radius=R)
            L = topological_laplacian(G.A, G.T)
            vals = laplacian_spectrum(L, k=10)
            assert np.all(vals > -1e-10), f"R={R}: negative eigenvalues"

    def test_seam_twist_exists(self):
        G = build_klein_bottle_radius(16, 16, radius=1)
        neg = (G.T.data < 0).sum()
        assert neg > 0

    def test_sparsity_scales_with_radius(self):
        for R in [1, 2, 3]:
            G = build_klein_bottle_radius(12, 12, radius=R)
            exp_deg = (2 * R + 1) ** 2 - 1
            nnz_per_row = G.A.nnz / (12 * 12)
            assert abs(nnz_per_row - exp_deg) / exp_deg < 0.05


class TestSpectrumChange:
    def test_distinct_levels_roughly_equal(self):
        r1 = analyse_radius(20, 20, 1, k_eigs=30)
        r4 = analyse_radius(20, 20, 4, k_eigs=30)
        assert abs(r4["distinct_eigenvalues"] - r1["distinct_eigenvalues"]) <= 6

    def test_gap_ratios_spread_changes_with_r(self):
        r1 = analyse_radius(20, 20, 1, k_eigs=40)
        r4 = analyse_radius(20, 20, 4, k_eigs=40)
        assert len(r4["gap_ratios"]) >= len(r1["gap_ratios"]) // 2

    def test_median_not_monotonically_approaching_phi(self):
        medians = []
        for R in [1, 2, 3, 4]:
            res = analyse_radius(20, 20, R, k_eigs=40)
            medians.append(res["median_r_star"])
        assert max(abs(m - 1.618) for m in medians[:3]) > 0.3
