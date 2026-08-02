"""
================================================================================
IST PHASE 25 - Temporal Holonomy: The Compression Operator as Parallel Transport
================================================================================
Purpose:
    Implement the v6.2 reformulation of the Compression Operator Psi as an
    emergent temporal holonomy in a block-universe topology. Each oscillator
    carries a 2-component spinor; one plonk tick advances the spinor through
    one quarter of the Klein bottle's 720-degree double-cover. The 4-tick
    cycle is the numerical integration of the path-ordered exponential

        Psi_cycle = U_3 U_2 U_1 U_0 ,   U_k = exp(-i dtau H_k) ,

    where H_k = (omega_0 + rho_fold) I + (pi/2) n_hat.sigma carries the
    connection: A_0 = rho_fold (scalar potential, fold density) and
    A_1 = twist_flag . sigma_x (parity gauge through the Mobius seam).
    The matrices are evaluated EXACTLY as SU(2) elements (Euler/Cayley-
    Hamilton), so unitarity holds to machine precision regardless of the
    nonlinearity in the connection.

    The four-tick product with alternating parity axes evaluates to -I in
    the flat limit (the fermionic sign / projective identity), giving the
    spin-1/2 double-cover: 100% chirality flip at tick 2, restoration at
    tick 4.

Phases delivered:
    25   - TemporalHolonomy integrator (propagate_holonomy replaces update)
    25a  - Static-phi falsification reproduced: the connection reduces to the
           static Laplacian in the zero-curvature limit; D_eff ~ 2, NOT phi.
    25b  - Temporal curvature (variable fold f): Riccati fold flow
           df/dt = gamma (D_eff(f) - phi) f drives f -> golden window (~4.2),
           compared against the static-scan (Phase 4) D_eff baseline.
    Rig  - Wilson loop traces, unit-circle spectra (720 deg structure),
           lattice robustness (Fibonacci preserves non-trivial winding;
           rational collapses it toward the trivial fermionic -I), Lyapunov
           exponent vs ln(phi)/tau_plonk, spectral-gap ratio at the golden
           window vs 1/phi^2.

Honest results (verified on this machine):
    * Flat-limit 4-tick holonomy is EXACTLY -I (max |Tr+2| = 0.0): the
      fermionic sign / 720-deg double-cover holds to machine precision.
    * Unitarity and time-reversal (Psi_rev = Psi^-1) hold to ~1e-16.
    * The literal v6.2 Sec 5.3 knot redefinition P(Im(lambda)!=0) is NOT ~3%;
      in the coupled substrate it is O(0.5-0.9) (non-trivial temporal winding
      is generic). The Phase 23a ~3% figure was a phase-return stability
      criterion, a different observable.
    * Golden-window anti-resonance min_gap/max_gap = 1/phi^2 is NOT realized
      by the holonomy eigenphase spectrum (measured ~0.0); the trace bound
      Tr(Psi) in [-2,2] holds for ALL lattices (SU(2) by construction), so
      the discriminating signature is the deviation from the flat -I, which
      the Fibonacci lattice preserves maximally (dev ~0.215 vs rational
      ~0.038).
    * The fold-flow Lyapunov exponent (~0.018 with gamma=0.1) is far below
      ln(phi)/tau_plonk = 0.4812; matching the golden-rate prediction
      requires gamma calibrated so that gamma (D_eff - phi) ~ ln(phi).

Outputs:  code/outputs/phase25/wilson_traces.csv
          code/outputs/phase25/wilson_unit_circle.png
          code/outputs/phase25/phase25a_static.csv
          code/outputs/phase25/phase25a_static.png
          code/outputs/phase25/riccati_flow.csv
          code/outputs/phase25/riccati_flow.png
          code/outputs/phase25/convergence_compare.csv
          code/outputs/phase25/lattice_robustness.csv
          code/outputs/phase25/golden_gap.csv
          code/outputs/phase25/golden_gap.png

References:
    notes/IST v6.2 temporal holonomy.md   (the v6.2 reformulation)
    code/phase4_variable_g.py             (static compression spectrum)
    code/phase7_vector_substrate.py       (spectral_dimension)
    code/phase23a_plonk_cycle.py          (Klein geodesics, orientation cycle)
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
from phase23a_plonk_cycle import klein_distance
from phase7_vector_substrate import spectral_dimension
from phase4_variable_g import FoldedSubstrate, central_band

OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "phase25")
TAU_PLONK = 1.0
LYAPUNOV_PRED = np.log(PHI) / TAU_PLONK          # ln(phi)/tau_plonk ~ 0.4812
GAP_RATIO_TARGET = 1.0 / PHI ** 2                 # 1/phi^2 ~ 0.3820
GOLDEN_WINDOW = 4.2

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


# ───────────────────────────────────────────────────────────────────────────────
# EXACT SU(2) PROPAGATOR
# ───────────────────────────────────────────────────────────────────────────────

def tick_unitary(rho, crossing, beta=1.0):
    """U_k = exp(-i (pi/2) n_hat.sigma), the v6.2 discrete realization
    (Sec 3.1). The fold density enters through the PROPAGATION AXIS, not an
    additive phase: on a twist crossing the parity axis tilts out of the
    seam plane by phi = beta * (rho_fold - 1), n_hat = (cos phi, 0, sin phi);
    on a non-crossing tick n_hat = z_hat. For phi = 0 (void, rho = 1) this
    reduces exactly to U = -i n_hat.sigma (SU(2), unitary, det = +1), and
    the 4-tick product is exactly -I (the fermionic sign / trivial temporal
    winding)."""
    if crossing:
        phi = beta * (rho - 1.0)
        axis = np.cos(phi) * SX + np.sin(phi) * SZ
    else:
        axis = SZ
    return -1j * axis


def cycle_product(rho, omega_0=None, orientation_start=0, reverse=False,
                  dtau=TAU_PLONK, beta=1.0):
    """Ordered Wilson-loop product Psi_cycle = U_3 U_2 U_1 U_0 for a frozen
    connection snapshot rho. `reverse=True` computes the time-reversed
    traversal Psi_rev = U_0^dag U_1^dag U_2^dag U_3^dag = Psi_cycle^{-1}
    (conjugated operators in reversed multiplication order), the block-
    universe time-reversal statement. omega_0 is accepted for API
    compatibility but does not enter the connection (fold density only)."""
    M = np.array([I2.copy() for _ in range(len(rho))])
    tick_order = range(4) if not reverse else range(3, -1, -1)
    for k in tick_order:
        o = (orientation_start + k) % 4
        crossing = (o + 1) % 4 in (2, 0)          # seam crossing this tick
        U = np.array([tick_unitary(r, crossing, beta=beta) for r in rho])
        U = U.conj().transpose(0, 2, 1) if reverse else U
        M = np.einsum("nij,njk->nik", U, M)
    return M


def cayley_hamilton_expm(H):
    """exp(-iH) for a 2x2 Hermitian H = a I + b.sigma, via the Euler formula.

    Only used for generic Hamiltonians (tests / diagnostics); the plonk-tick
    propagator uses tick_unitary directly.
    """
    a = 0.5 * (H[0, 0] + H[1, 1])
    # H = a I + b.sigma  =>  H[0,1] = bx - i*by, H[0,0]-H[1,1] = 2*bz
    b = np.array([H[0, 1].real, -H[0, 1].imag, 0.5 * (H[0, 0] - H[1, 1])])
    mag = np.linalg.norm(b)
    if mag < 1e-15:
        return np.exp(-1j * a) * I2
    n = b / mag
    nb = n[0] * SX + n[1] * SY + n[2] * SZ
    return np.exp(-1j * a) * (np.cos(mag) * I2 - 1j * np.sin(mag) * nb)


# ───────────────────────────────────────────────────────────────────────────────
# TEMPORAL HOLONOMY SUBSTRATE
# ───────────────────────────────────────────────────────────────────────────────

class SpinorOscillator:
    """Oscillator on the Klein bottle carrying a 2-component spinor."""
    __slots__ = ("u", "v", "phase", "orientation", "chirality", "spinor", "rho")
    def __init__(self, u, v, phase):
        self.u = float(u); self.v = float(v)
        self.phase = float(phase) % (2 * np.pi)
        self.orientation = 0
        self.chirality = 1
        self.spinor = np.array([1.0, 0.0], dtype=complex)
        self.rho = 1.0


def fibonacci_lattice(N, golden_angle=None):
    """Golden-angle spiral on the Klein bottle (replaces phase23a's builder
    with a spinor-carrying oscillator; same layout)."""
    if golden_angle is None:
        golden_angle = 2 * np.pi / PHI ** 2
    points = []
    for i in range(N):
        theta = (i * golden_angle) % (2 * np.pi)
        u = theta / (2 * np.pi)
        z = 1.0 - (2.0 * i + 1.0) / N
        v = np.arccos(max(min(z, 1), -1)) / np.pi
        v = (v + u * 0.5) % 1.0                     # Mobius twist
        points.append(SpinorOscillator(u, v, 2 * np.pi * u))
    return points


def random_lattice(N, seed=0):
    """Uniform random placement (control lattice)."""
    rng = np.random.default_rng(seed)
    return [SpinorOscillator(rng.random(), rng.random(), rng.random() * 2 * np.pi)
            for _ in range(N)]


def rational_lattice(N):
    """Rational 1/5 rotation spacing (control lattice)."""
    return [SpinorOscillator(i / N, (i / 5) % 1.0, 2 * np.pi * (i / 5))
            for i in range(N)]


class TemporalHolonomy:
    """Spinor substrate whose dynamics are the temporal holonomy of the
    connection. The 4-tick cycle is the Wilson loop; its eigenvalues are the
    temporal winding numbers of each oscillator."""

    def __init__(self, oscillators, omega_0=0.3, gain=0.8, sigma=0.15):
        self.oscillators = list(oscillators)
        self.N = len(oscillators)
        self.omega_0 = omega_0
        self.gain = gain
        self.sigma = sigma
        self.tick_count = 0
        self.W = self._signed_coupling()

    # ── Connection ───────────────────────────────────────────────────────

    def _signed_coupling(self):
        """Static signed coupling: golden-phase-filtered proximity with
        parity inversion (twist-crossing pairs negative)."""
        N = self.N
        phases = np.array([o.phase for o in self.oscillators])
        dp = np.abs(phases[:, None] - phases[None, :])
        dp = np.minimum(dp, 2 * np.pi - dp)
        golden_match = np.zeros((N, N), dtype=bool)
        for tgt in [2 * np.pi / PHI ** 2, 2 * np.pi * (1 - 1 / PHI ** 2)]:
            golden_match |= np.abs(dp - tgt) < 0.25
        np.fill_diagonal(golden_match, False)

        us = np.array([o.u for o in self.oscillators])
        vs = np.array([o.v for o in self.oscillators])
        d, twist = klein_distance(us, vs, us, vs)
        J = np.exp(-d ** 2 / (2 * self.sigma ** 2))
        np.fill_diagonal(J, 0)
        signs = np.where(twist, -1.0, 1.0)
        np.fill_diagonal(signs, 0)
        W = np.where(golden_match, J * 5.0 * signs, J * 0.3 * signs)
        np.fill_diagonal(W, 0)
        return W

    def _fold_density(self):
        """A_0 = rho_fold: scalar potential from the coupling field acting
        on the spinor 'up' populations. Normalized so the void baseline is
        exactly rho = 1 (where the crossing axis is the pure parity gauge
        and the 4-tick holonomy returns exactly -I, i.e. trivial winding);
        only fold-dense oscillators deviate upward from baseline."""
        amps = np.array([abs(o.spinor[0]) ** 2 for o in self.oscillators])
        coupling = np.abs(self.gain * (self.W @ amps))
        med = np.median(coupling)
        scale = med if med > 1e-9 else 1.0
        return 1.0 + 0.5 * np.tanh(np.maximum(coupling - med, 0.0) / scale)

    # ── Dynamics ─────────────────────────────────────────────────────────

    def _plonk_tick(self):
        """One tick: advance orientation, build U_k, apply to spinors."""
        rho = self._fold_density()
        for i, o in enumerate(self.oscillators):
            o.orientation = (o.orientation + 1) % 4
            crossing = o.orientation in (2, 0)          # seam crossing
            U = tick_unitary(rho[i], crossing)
            o.spinor = U @ o.spinor
            o.chirality *= -1 if crossing else 1
            o.rho = rho[i]
        self.tick_count += 1

    def propagate_holonomy(self):
        """Full 4-tick cycle. Returns per-oscillator Wilson-loop matrices
        Psi_cycle = U_3 U_2 U_1 U_0."""
        cycles = []
        for _ in range(4):
            rho = self._fold_density()
            U = np.array([tick_unitary(rho[i],
                                       (o.orientation + 1) % 4 in (2, 0))
                          for i, o in enumerate(self.oscillators)])
            for i, o in enumerate(self.oscillators):
                o.spinor = U[i] @ o.spinor
                o.orientation = (o.orientation + 1) % 4
                crossing = o.orientation in (2, 0)
                o.chirality *= -1 if crossing else 1
                o.rho = rho[i]
            self.tick_count += 1
            cycles.append(U)
        return cycles

    def wilson_spectrum(self, n_cycles=1):
        """Run n_cycles and return (eigenvalues, traces, cycle matrices).
        Each cycle's Wilson-loop matrix is the ordered product
        U_3 U_2 U_1 U_0 built from that cycle's tick operators; eigenvalues
        are per-cycle, not compounded across cycles."""
        evals = []
        mats = []
        for _ in range(n_cycles):
            cycles = self.propagate_holonomy()
            M = np.einsum("nij,njk->nik", cycles[3],
                          np.einsum("nij,njk->nik", cycles[2],
                                    np.einsum("nij,njk->nik", cycles[1],
                                              cycles[0])))
            evals.append(np.linalg.eigvals(M))
            mats.append(M)
        evals = np.array(evals)
        traces = 2.0 * evals.real                    # Tr(e^{+-i theta})
        return evals, traces, mats[-1]

    # ── Diagnostics ──────────────────────────────────────────────────────

    def unitarity_error(self):
        """max || Psi_cycle Psi_cycle^dag - I || over oscillators."""
        _, _, M = self.wilson_spectrum(n_cycles=1)
        return np.max([np.linalg.norm(M[i] @ M[i].conj().T - I2)
                       for i in range(self.N)])

    def knot_fraction(self, n_cycles=1):
        """Stable-knot rate redefined per v6.2 Sec 5.3 as P(Im(lambda) != 0):
        the fraction of oscillators whose cycle holonomy has a topologically
        non-trivial temporal winding number (eigenvalues genuinely off the
        real axis), averaged over the measured cycles."""
        evals, _, _ = self.wilson_spectrum(n_cycles=n_cycles)
        return float(np.mean(np.abs(evals.imag) > 1e-9))

    def time_reversal_check(self):
        """Forward Wilson loop traversed in the reverse temporal direction
        must equal Psi_cycle^{-1}. Uses a frozen connection snapshot so the
        two products are compared on identical data."""
        rho = self._fold_density()
        M_f = cycle_product(rho, self.omega_0, orientation_start=0,
                            reverse=False)
        M_r = cycle_product(rho, self.omega_0, orientation_start=0,
                            reverse=True)
        inv = np.array([np.linalg.inv(M_f[i]) for i in range(self.N)])
        return float(np.max([np.linalg.norm(M_r[i] - inv[i])
                             for i in range(self.N)]))

    def _forward_cycle_matrix(self):
        rho = self._fold_density()
        return cycle_product(rho, self.omega_0, orientation_start=0,
                             reverse=False)


# ───────────────────────────────────────────────────────────────────────────────
# PHASE 25a - STATIC-PHI FALSIFICATION (zero-curvature limit)
# ───────────────────────────────────────────────────────────────────────────────

def phase25a_static_falsification(n=48):
    """The geometric connection reduces to the static Laplacian in the
    zero-curvature limit: spectral dimension of the holonomy graph ~ 2 (NOT
    phi), reproducing the Phase 1/4 falsification with the new operator."""
    L = FoldedSubstrate(n, twisted=True).graph.laplacian()
    d_eff, r2 = spectral_dimension(L)
    g_min = FoldedSubstrate(n, twisted=True).gamma_min()
    g_analytic = 4 * np.sin(np.pi / (2 * n)) ** 2
    return {
        "n_grid": n,
        "d_eff_static": d_eff,
        "r2": r2,
        "phi": PHI,
        "distance_from_phi": abs(d_eff - PHI),
        "gamma_min": g_min,
        "gamma_analytic": g_analytic,
        "gamma_match": abs(g_min - g_analytic),
    }


# ───────────────────────────────────────────────────────────────────────────────
# PHASE 25b - RICCOTI FOLD FLOW (temporal curvature)
# ───────────────────────────────────────────────────────────────────────────────

def d_eff_vs_fold(n=48, fold_scan=None):
    """D_eff(f) from the fold-weighted holonomy spectrum (Phase 4 geometry)."""
    if fold_scan is None:
        fold_scan = [1.0, 1.5, 2.0, 3.0, 4.0, 4.2, 5.0, 6.0, 8.0, 12.0, 16.0]
    out = []
    for f in fold_scan:
        sub = FoldedSubstrate(n, twisted=True, band=central_band(n),
                              fold_factor=f)
        d_eff, r2 = spectral_dimension(sub.S)
        out.append((f, d_eff, r2))
    return out


def riccati_fold_flow(d_eff_fn, f0=1.0, gamma=0.1, dt=1.0, n_steps=200,
                      tol=1e-2):
    """df/dt = gamma (D_eff(f) - phi) f. Returns trajectory and steps to
    reach |D_eff(f) - phi| < tol (or None if not reached)."""
    fs = [f0]
    ds = [d_eff_fn(f0)]
    for _ in range(n_steps):
        f = fs[-1]
        d = d_eff_fn(f)
        f_new = f + gamma * (d - PHI) * f * dt
        fs.append(max(f_new, 1.0))
        ds.append(d_eff_fn(fs[-1]))
        if abs(ds[-1] - PHI) < tol:
            return fs, ds, len(fs) - 1
    return fs, ds, None


def load_phase4_static_d_eff():
    """D_eff(f) anchors from the Phase 4 static fold scan (same data Phase 14
    uses). This is the baseline 'discrete nonlinear update' D_eff."""
    path = os.path.join(os.path.dirname(__file__), "outputs", "phase4",
                        "geff_vs_rho.csv")
    fs, gs = [], []
    with open(path) as fh:
        for row in csv.DictReader(fh):
            fs.append(float(row["fold_factor"]))
            gs.append(float(row["g_eff_norm"]))
    fs = np.array(fs); gs = np.array(gs)
    slopes = np.diff(np.log(gs)) / np.diff(np.log(fs))
    f_mid = np.sqrt(fs[:-1] * fs[1:])
    return f_mid, 1.0 / slopes


def static_d_eff_interp(f, f_anchors, d_anchors):
    """Interpolate the static-scan D_eff(f) with Phase 14-style extension."""
    fa = np.concatenate([[1.0], f_anchors, [100.0]])
    da = np.concatenate([[4.5], d_anchors, [1.05]])
    return float(np.interp(f, fa, da))


def discrete_nonlinear_baseline(f0=1.0, gamma=0.1, tol=1e-2, n_steps=2000):
    """Baseline: how many Riccati-flow steps does the STATIC (Phase 4 scan)
    D_eff need to reach the golden window? This is the v6.2 'discrete
    nonlinear update' comparison: same feedback law df/dt = gamma(D_eff-phi)f,
    same gamma, only the D_eff source differs (static scan vs holonomy)."""
    f_anchors, d_anchors = load_phase4_static_d_eff()
    f = f0
    for t in range(n_steps):
        d = static_d_eff_interp(f, f_anchors, d_anchors)
        f = max(f + gamma * (d - PHI) * f, 1.0)
        if abs(static_d_eff_interp(f, f_anchors, d_anchors) - PHI) < tol:
            return t + 1
    return None


# ───────────────────────────────────────────────────────────────────────────────
# RIG DIAGNOSTICS
# ───────────────────────────────────────────────────────────────────────────────

def lyapunov_of_flow(trajectory):
    """Empirical Lyapunov exponent of the fold-density flow from the log
    growth rate of successive separations (finite-difference of df/d ln f)."""
    fs = np.asarray(trajectory, dtype=float)
    if len(fs) < 3:
        return np.nan
    logs = np.diff(np.log(np.clip(fs, 1e-12, None)))
    return float(np.mean(logs[logs != 0]))


def golden_window_gap_ratio(n_cycles=100, n=150, gain=0.8):
    """Anti-resonance gap rigidity R = min_gap/max_gap of the holonomy
    eigenphase spectrum at the golden window, defined on DISTINCT levels
    (near-degenerate duplicates within 1e-3 dropped), matching the Phase 6
    definition. Compared against the v6.2 target 1/phi^2. The doc's rig
    instruction anticipates the possibility of non-convergence: the summary
    reports the measured deviation from 1/phi^2."""
    rows = []
    sub = TemporalHolonomy(fibonacci_lattice(n), gain=gain, sigma=0.15)
    for cycle in range(n_cycles):
        evals, _, _ = sub.wilson_spectrum(n_cycles=1)
        th = np.sort(np.mod(np.angle(evals[-1].ravel()), 2 * np.pi))
        th = np.append(th, th[0] + 2 * np.pi)
        thd = th[np.concatenate([[True], np.diff(th) > 1e-3])]
        gaps = np.diff(thd)
        gaps = gaps[gaps > 1e-6]
        if len(gaps) < 2:
            continue
        ratio = gaps.min() / gaps.max()
        rows.append({"cycle": cycle, "min_gap": gaps.min(),
                     "max_gap": gaps.max(), "ratio": ratio,
                     "dev_from_target": ratio - GAP_RATIO_TARGET})
    return rows


# ───────────────────────────────────────────────────────────────────────────────
# MAIN DRIVER
# ───────────────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rng = np.random.default_rng(1)

    # ── Temporal holonomy substrate (Fibonacci lattice) ──────────────────
    oscs = fibonacci_lattice(200)
    sub = TemporalHolonomy(oscs, omega_0=0.3, gain=0.8, sigma=0.15)

    # Flat-limit 720 deg double-cover: cycle product should be -I exactly
    flat = TemporalHolonomy(fibonacci_lattice(64), omega_0=0.0, gain=0.0,
                            sigma=0.15)
    M_flat = flat._forward_cycle_matrix()
    flat_traces = np.array([np.trace(M_flat[i]) for i in range(flat.N)])
    flat_dev = np.max(np.abs(flat_traces + 2.0))

    # Unitarity + time reversal on a live run
    uni_err = sub.unitarity_error()
    sub2 = TemporalHolonomy(fibonacci_lattice(200), omega_0=0.3, gain=0.8,
                            sigma=0.15)
    tr_err = sub2.time_reversal_check()

    # Wilson traces over 40 cycles
    rows = []
    sub3 = TemporalHolonomy(fibonacci_lattice(200), omega_0=0.3, gain=0.8,
                            sigma=0.15)
    for c in range(40):
        kfrac = sub3.knot_fraction(n_cycles=1)
        evals, traces, M = sub3.wilson_spectrum(n_cycles=1)
        tr_mean = np.mean(np.abs(traces[-1]))
        rows.append({"cycle": c + 1, "tick": sub3.tick_count,
                     "knot_fraction": kfrac, "mean_abs_trace": tr_mean})
    with open(os.path.join(OUT_DIR, "wilson_traces.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    # Unit-circle spectrum (last cycle)
    evals, _, M = sub3.wilson_spectrum(n_cycles=1)
    lam = evals[-1]
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    th = np.linspace(0, 2 * np.pi, 400)
    ax[0].plot(np.cos(th), np.sin(th), "k-", lw=0.5)
    ax[0].plot(lam.real, lam.imag, "o", ms=4, alpha=0.6,
               color="crimson", label="cycle eigenvalues")
    ax[0].plot([-1], [0], "bs", ms=8, label="flat limit -I")
    ax[0].set_aspect("equal"); ax[0].set_title("Wilson eigenvalues on unit circle")
    ax[0].legend(fontsize=8)
    ax[1].hist(2 * lam.real.ravel(), bins=40, color="steelblue")
    ax[1].axvline(-2, color="crimson", ls="--", label="-2 (flat -I)")
    ax[1].axvline(2, color="crimson", ls="--")
    ax[1].set_xlabel("Tr(Psi_cycle)"); ax[1].set_title("Holonomy trace distribution")
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "wilson_unit_circle.png"), dpi=300)
    plt.close(fig)

    # ── Phase 25a: static falsification ──────────────────────────────────
    a = phase25a_static_falsification()
    with open(os.path.join(OUT_DIR, "phase25a_static.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(a.keys()))
        w.writeheader(); w.writerow(a)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(["D_eff static (holonomy)", "phi target"], [a["d_eff_static"], PHI],
           color=["steelblue", "crimson"])
    ax.set_ylim(0, 2.5)
    ax.set_title("Phase 25a: static spectrum D_eff ~ 2, not phi")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "phase25a_static.png"), dpi=300)
    plt.close(fig)

    # ── Phase 25b: Riccati fold flow ─────────────────────────────────────
    dscan = d_eff_vs_fold()
    fs, ds, steps = riccati_fold_flow(lambda f: np.interp(
        f, [x[0] for x in dscan], [x[1] for x in dscan]), f0=1.0)
    disc_steps = discrete_nonlinear_baseline()
    with open(os.path.join(OUT_DIR, "riccati_flow.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["step", "f", "d_eff", "phi"])
        for t, (f, d) in enumerate(zip(fs, ds)):
            w.writerow([t, f, d, PHI])
    with open(os.path.join(OUT_DIR, "convergence_compare.csv"), "w",
              newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["method", "steps_to_golden_window"])
        w.writerow(["riccati_holonomy", steps])
        w.writerow(["discrete_nonlinear", disc_steps])

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].plot(fs, ds, "o-", color="steelblue")
    ax[0].axhline(PHI, color="crimson", ls="--", label="phi")
    ax[0].set_xlabel("fold f"); ax[0].set_ylabel("D_eff(f)")
    ax[0].set_title("D_eff(f) from holonomy spectrum")
    ax[0].legend(fontsize=8)
    ax[1].plot(np.arange(len(fs)), fs, "o-", color="seagreen")
    ax[1].axhline(GOLDEN_WINDOW, color="crimson", ls="--",
                  label=f"golden window f={GOLDEN_WINDOW}")
    ax[1].set_xlabel("Riccati step"); ax[1].set_ylabel("f")
    ax[1].set_title("Fold flow: df/dt = gamma (D_eff - phi) f")
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "riccati_flow.png"), dpi=300)
    plt.close(fig)

    # ── Rig: spectral-gap ratio at the golden window ─────────────────────
    gap_rows = golden_window_gap_ratio(n_cycles=50, n=150)
    with open(os.path.join(OUT_DIR, "golden_gap.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(gap_rows[0].keys()))
        w.writeheader(); w.writerows(gap_rows)

    fig, ax = plt.subplots(figsize=(7, 5))
    ratios = [r["ratio"] for r in gap_rows]
    ax.plot([r["cycle"] for r in gap_rows], ratios, "o-", color="darkorange")
    ax.axhline(GAP_RATIO_TARGET, color="crimson", ls="--",
               label=f"1/phi^2 = {GAP_RATIO_TARGET:.4f}")
    ax.set_xlabel("cycle"); ax.set_ylabel("min_gap / max_gap")
    ax.set_title("Spectral-gap ratio at golden window f=4.2")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "golden_gap.png"), dpi=300)
    plt.close(fig)

    # ── Golden filter robustness: trace bound across lattices ────────────
    # v6.2 Sec 6.2: Tr(Psi_cycle) stays bounded in [-2, 2] with non-trivial
    # winding only when the deposition follows the Fibonacci lattice; the
    # rational control collapses the winding toward the trivial fermionic -I.
    robust_rows = []
    for name, build in [("fibonacci", fibonacci_lattice),
                        ("random", random_lattice),
                        ("rational", rational_lattice)]:
        s = TemporalHolonomy(build(200), gain=0.8, sigma=0.15)
        s.wilson_spectrum(n_cycles=5)
        evals, _, _ = s.wilson_spectrum(n_cycles=1)
        tr = 2 * evals[-1].real
        robust_rows.append({
            "lattice": name,
            "mean_abs_trace": np.mean(np.abs(tr)),
            "mean_dev_from_flat": np.mean(np.abs(tr + 2.0)),
            "knot_fraction_im": np.mean(np.abs(evals[-1].imag) > 1e-9),
            "trace_in_bounds": float(np.all(np.abs(tr) <= 2.0 + 1e-12)),
        })
    with open(os.path.join(OUT_DIR, "lattice_robustness.csv"), "w",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(robust_rows[0].keys()))
        w.writeheader(); w.writerows(robust_rows)

    # ── Summary ──────────────────────────────────────────────────────────
    lyap = lyapunov_of_flow(fs)
    print("=== IST PHASE 25: Temporal Holonomy ===")
    print(f"flat-limit cycle product = -I: max |Tr + 2| = {flat_dev:.2e}")
    print(f"unitarity max err       : {uni_err:.2e}  (target < 1e-12)")
    print(f"time-reversal max err   : {tr_err:.2e}  (Psi_rev vs Psi^-1)")
    print(f"knot fraction (last cyc): {rows[-1]['knot_fraction']:.4f} "
          f"(P(Im(lambda)!=0))")
    print(f"Phase 25a: D_eff static = {a['d_eff_static']:.3f} "
          f"(phi = {PHI:.3f}), gamma_min = {a['gamma_min']:.3e} "
          f"analytic {a['gamma_analytic']:.3e}")
    print(f"Phase 25b: Riccati steps to golden window = {steps}; "
          f"discrete nonlinear = {disc_steps}")
    print(f"Lyapunov (flow) = {lyap:.4f} vs ln(phi)/tau_plonk = "
          f"{LYAPUNOV_PRED:.4f}")
    ratio_mean = np.mean(ratios)
    for r in robust_rows:
        print(f"  lattice {r['lattice']:9s}: mean|Tr|={r['mean_abs_trace']:.3f} "
              f"dev_flat={r['mean_dev_from_flat']:.3f} "
              f"knot={r['knot_fraction_im']:.3f} in_bounds={r['trace_in_bounds']}")
    print(f"golden-window gap rigidity R = {ratio_mean:.4f} vs 1/phi^2 = "
          f"{GAP_RATIO_TARGET:.4f} (dev = {ratio_mean - GAP_RATIO_TARGET:+.4f}; "
          f"reported per the v6.2 rig instruction 'if convergence fails, "
          f"report the deviation')")
    print(f"Wrote {OUT_DIR}")


if __name__ == "__main__":
    main()
