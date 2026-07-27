"""
Unit tests for phase1_klein_laplacian.py — IST Phase 1.1
=========================================================
Topology checks for the discrete Klein bottle graph (Euler characteristic,
non-orientability, seam holonomy), Laplacian properties, and validation of
the numerical spectrum against the closed-form analytic spectrum.

Run: cd code && python -m pytest ../tests/test_phase1_spectrum.py -v
"""

import sys
import os
import numpy as np
import scipy.sparse as sp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_klein_laplacian import (
    SubstrateGraph, build_klein_bottle_graph, build_torus_graph,
    topological_laplacian, laplacian_spectrum,
    analytic_klein_eigenvalues, analytic_torus_eigenvalues,
    distinct_eigenvalues, gap_ratios, PHI,
)


# ── Graph Construction ────────────────────────────────────────────────────────

class TestGraphConstruction:
    def test_vertex_count(self):
        g = build_klein_bottle_graph(8, 12)
        assert g.A.shape == (96, 96)
        assert g.coords.shape == (96, 2)

    def test_four_regular(self):
        g = build_klein_bottle_graph(16, 16)
        degrees = np.asarray(g.A.sum(axis=1)).ravel()
        assert np.all(degrees == 4)

    def test_adjacency_symmetric(self):
        g = build_klein_bottle_graph(8, 16)
        assert (g.A != g.A.T).nnz == 0
        assert (g.W != g.W.T).nnz == 0

    def test_rejects_degenerate_grids(self):
        for bad in [(2, 8), (8, 2), (1, 1)]:
            try:
                build_klein_bottle_graph(*bad)
                assert False, f"should reject {bad}"
            except ValueError:
                pass

    def test_seam_edges_present_only_when_twisted(self):
        assert len(build_klein_bottle_graph(8, 8).seam_edges) == 8
        assert len(build_torus_graph(8, 8).seam_edges) == 0


# ── Topology: Euler Characteristic, Orientability, Holonomy ──────────────────

class TestTopology:
    def test_euler_characteristic_zero(self):
        # chi = 0 is required for both Klein bottle and torus
        for m, n in [(8, 8), (16, 16), (8, 16), (32, 32)]:
            assert build_klein_bottle_graph(m, n).euler_characteristic() == 0
            assert build_torus_graph(m, n).euler_characteristic() == 0

    def test_klein_bottle_non_orientable(self):
        for m, n in [(8, 8), (16, 16), (8, 16)]:
            assert not build_klein_bottle_graph(m, n).is_orientable()

    def test_torus_orientable(self):
        for m, n in [(8, 8), (16, 16), (8, 16)]:
            assert build_torus_graph(m, n).is_orientable()

    def test_meridian_walk_has_odd_twist(self):
        # The self-intersection (seam) cycle: orientation reverses
        g = build_klein_bottle_graph(16, 16)
        for i0 in [0, 3, 7]:
            assert g.walk_twist_product(g.meridian_walk(i0)) == -1

    def test_longitude_walk_has_even_twist(self):
        g = build_klein_bottle_graph(16, 16)
        for j0 in [0, 5, 15]:
            assert g.walk_twist_product(g.longitude_walk(j0)) == +1

    def test_contractible_plaquette_has_even_twist(self):
        # Flatness: no curvature (twist) concentrated on interior faces
        g = build_klein_bottle_graph(16, 16)
        face = g.faces[3 * 16 + 5]  # interior plaquette, away from seam
        assert g.walk_twist_product(face + [face[0]]) == +1

    def test_torus_all_walks_even(self):
        g = build_torus_graph(16, 16)
        assert g.walk_twist_product(g.meridian_walk(0)) == +1
        assert g.walk_twist_product(g.longitude_walk(0)) == +1


# ── Laplacian Properties ──────────────────────────────────────────────────────

class TestLaplacian:
    def test_symmetric(self):
        L = build_klein_bottle_graph(16, 16).laplacian()
        assert (L != L.T).nnz == 0

    def test_torus_has_zero_mode(self):
        L = build_torus_graph(16, 16).laplacian()
        vals = laplacian_spectrum(L, 4)
        assert abs(vals[0]) < 1e-8
        # constants are in the kernel: L @ 1 = 0
        assert np.allclose(L @ np.ones(L.shape[0]), 0, atol=1e-12)

    def test_klein_has_no_zero_mode(self):
        # Twist removes the constant section: lambda_min = 4 sin^2(pi / 2m)
        m = 16
        L = build_klein_bottle_graph(m, m).laplacian()
        vals = laplacian_spectrum(L, 4)
        expected = 4 * np.sin(np.pi / (2 * m)) ** 2
        assert vals[0] > 1e-4
        assert abs(vals[0] - expected) < 1e-9

    def test_custom_coupling_J(self):
        g = build_klein_bottle_graph(8, 8)
        J = sp.csr_matrix(np.ones((64, 64)))
        L = topological_laplacian(g.A, g.T, J * 2.0)
        vals = laplacian_spectrum(L, 2)
        assert vals[0] > 0  # spectrum scales but stays positive


# ── Numerical Spectrum vs Analytic ────────────────────────────────────────────

class TestAnalyticSpectrum:
    def test_klein_spectrum_matches_formula(self):
        for m, n in [(16, 16), (32, 32), (16, 24)]:
            g = build_klein_bottle_graph(m, n)
            vals = laplacian_spectrum(g.laplacian(), 20)
            analytic = analytic_klein_eigenvalues(m, n, 400)
            for v in vals:
                err = np.min(np.abs(analytic - v))
                assert err < 1e-6 * max(1.0, abs(v)), f"no analytic match for {v}"

    def test_torus_spectrum_matches_formula(self):
        m, n = 16, 16
        g = build_torus_graph(m, n)
        vals = laplacian_spectrum(g.laplacian(), 20)
        analytic = analytic_torus_eigenvalues(m, n, 400)
        for v in vals:
            err = np.min(np.abs(analytic - v))
            assert err < 1e-6 * max(1.0, abs(v)), f"no analytic match for {v}"


# ── Spectral Helpers ──────────────────────────────────────────────────────────

class TestSpectralHelpers:
    def test_distinct_eigenvalues_clusters_degeneracies(self):
        vals = np.array([1.0, 1.0 + 1e-12, 2.0, 3.0, 3.0 + 5e-9, 4.5])
        distinct = distinct_eigenvalues(vals)
        assert np.allclose(distinct, [1.0, 2.0, 3.0, 4.5], atol=1e-8)

    def test_gap_ratios(self):
        distinct = np.array([1.0, 4.0, 5.0, 8.0, 9.0])
        gaps, ratios = gap_ratios(distinct)
        assert np.allclose(gaps, [3.0, 1.0, 3.0, 1.0])
        assert np.allclose(ratios, [1.0 / 3.0, 3.0, 1.0 / 3.0])

    def test_golden_ratio_defined(self):
        assert abs(PHI - 1.618033988749895) < 1e-15
