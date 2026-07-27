"""
Unit tests for phase1_rg_flow.py — IST Phase 1.3
==================================================
Block-spin Galerkin coarse-graining, spectral-dimension extraction, and
RG-flow diagnostics.

Run: cd code && python -m pytest ../tests/test_phase1_rg_flow.py -v
"""

import sys
import os

import numpy as np
import scipy.sparse as sp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase1_rg_flow import (
    block_prolongation, coarsen_laplacian, rg_flow_laplacians,
    spectral_dimension, solis_beta, solis_flow, PHI,
)
from phase1_klein_laplacian import build_torus_graph, build_klein_bottle_graph


# ── Block-Spin Coarse-Graining ────────────────────────────────────────────────

class TestBlockSpin:
    def test_prolongation_shape_and_partition(self):
        P, (ncm, ncl) = block_prolongation(8, 8)
        assert P.shape == (64, 16)
        # every fine vertex belongs to exactly one coarse block
        assert np.allclose(P.sum(axis=1), 1.0)
        # each coarse block has exactly 4 fine vertices
        assert np.allclose(P.sum(axis=0), 4.0)

    def test_coarsen_halves_dimensions(self):
        g = build_torus_graph(16, 16)
        Lc, ncm, ncl = coarsen_laplacian(g.laplacian(), 16, 16)
        assert ncm == 8 and ncl == 8
        assert Lc.shape == (64, 64)

    def test_rg_flow_levels(self):
        levels = rg_flow_laplacians(n_start=32, n_levels=4, twisted=False)
        assert len(levels) == 4
        for lvl in levels:
            assert lvl["n_mer"] == 32 // (2 ** lvl["level"])


# ── Spectral Dimension Extraction ─────────────────────────────────────────────

class TestSpectralDimension:
    def test_1d_path_is_one(self):
        N = 128
        # Positive semidefinite path-graph Laplacian L = D - A
        diags = [-np.ones(N - 1), 2 * np.ones(N), -np.ones(N - 1)]
        L = sp.diags(diags, [-1, 0, 1])
        D, r2, _, _ = spectral_dimension(L, window_low=0.1, window_high=0.6)
        assert abs(D - 1.0) < 0.15, f"expected ~1, got {D}"
        assert r2 > 0.95

    def test_2d_torus_is_two(self):
        g = build_torus_graph(32, 32)
        D, r2, _, _ = spectral_dimension(g.laplacian())
        assert abs(D - 2.0) < 0.15, f"expected ~2, got {D}"
        assert r2 > 0.95

    def test_2d_klein_is_two(self):
        g = build_klein_bottle_graph(32, 32)
        D, r2, _, _ = spectral_dimension(g.laplacian())
        assert abs(D - 2.0) < 0.15, f"expected ~2, got {D}"
        assert r2 > 0.95


# ── Topology Preservation Under Coarsening ───────────────────────────────────

class TestTopologyUnderCoarsening:
    def test_torus_zero_mode_preserved(self):
        # Galerkin P * 1_c = 1_f, so the constant mode survives
        levels = rg_flow_laplacians(n_start=16, n_levels=3, twisted=False)
        for lvl in levels:
            vals = np.linalg.eigh(lvl["L"].toarray())[0]
            assert vals[0] < 1e-10

    def test_klein_no_zero_mode_preserved(self):
        # Twisted bundle has no constant section; coarse should stay massive
        levels = rg_flow_laplacians(n_start=16, n_levels=3, twisted=True)
        for lvl in levels:
            vals = np.linalg.eigh(lvl["L"].toarray())[0]
            assert vals[0] > 1e-4


# ── Solis Phenomenological Beta Function ──────────────────────────────────────

class TestSolisModel:
    def test_beta_zero_at_phi(self):
        assert abs(solis_beta(PHI)) < 1e-12

    def test_flow_converges_to_phi(self):
        for D0 in [1.2, 2.5, 3.0]:
            D_inf = solis_flow(D0, 50.0)
            assert abs(D_inf - PHI) < 1e-6

    def test_beta_sign(self):
        assert solis_beta(2.0) < 0  # above phi -> driven down
        assert solis_beta(1.0) > 0  # below phi -> driven up
