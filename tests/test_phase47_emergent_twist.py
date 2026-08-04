"""
Unit tests for phase47_emergent_twist.py -- IST Phase 47
==========================================================
Tests the derivation of the theta = 1/2 fractional twist from the
U(1) embedding of the discrete Klein bottle's Z2 holonomy.

Run: cd code && python -m pytest ../tests/test_phase47_emergent_twist.py -v
"""

import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from phase47_emergent_twist import (
    build_substrate_links,
    compute_wilson_loop,
    extract_twist
)

class TestH47aU1Embedding:
    def test_klein_meridian_holonomy_is_minus_one(self):
        m_links, _ = build_substrate_links(10, 10, orientable=False)
        W = compute_wilson_loop(m_links)
        assert np.isclose(W.real, -1.0)
        assert np.isclose(W.imag, 0.0)

    def test_klein_extracts_half_twist(self):
        m_links, _ = build_substrate_links(10, 10, orientable=False)
        W = compute_wilson_loop(m_links)
        theta = extract_twist(W)
        assert np.isclose(theta, 0.5)


class TestH47bGridIndependence:
    def test_twist_invariant_across_grid_sizes(self):
        grids = [(3, 3), (10, 10), (21, 34), (100, 100)]
        for n_mer, n_lon in grids:
            m_links, _ = build_substrate_links(n_mer, n_lon, orientable=False)
            theta = extract_twist(compute_wilson_loop(m_links))
            assert np.isclose(theta, 0.5)


class TestH47cSU2DoubleCoverReduction:
    def test_klein_longitude_is_trivial(self):
        _, l_links = build_substrate_links(10, 10, orientable=False)
        W = compute_wilson_loop(l_links)
        theta = extract_twist(W)
        assert np.isclose(theta, 0.0)


class TestH47dOrientableContrast:
    def test_torus_meridian_is_trivial(self):
        m_links, _ = build_substrate_links(10, 10, orientable=True)
        W = compute_wilson_loop(m_links)
        assert np.isclose(W.real, 1.0)
        assert np.isclose(W.imag, 0.0)
        
    def test_torus_extracts_zero_twist(self):
        m_links, _ = build_substrate_links(10, 10, orientable=True)
        theta = extract_twist(compute_wilson_loop(m_links))
        assert np.isclose(theta, 0.0)
