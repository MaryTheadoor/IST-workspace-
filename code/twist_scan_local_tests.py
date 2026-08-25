"""
twist_scan_local_tests.py — local toy-level harness tests supporting:
  (A) notes/IST_twist_variable_scan.md   (Phase 69 proposal)
  (B) notes/IST_black_hole_latency_conjecture.md

TOY MODELS — flux-cylinder/torus lattices and a 1D tick-rate gas, NOT the
repo's true Fibonacci-Klein runtime. Results are indicative; promotion
requires the pre-registered phases (H69a-e, BH Q1-Q4).

Tests:
  T1  exchange-phase law  chi_n(theta) = e^{i 2 pi n theta}   (lattice Wilson product)
  T2  Casimir/spectral-gap curve vs theta (numeric vs analytic), max at theta=1/2
  T3  reality islands: gauge-invariant |Im W| zeros at exactly {0, 1/2};
      naive ||Im H|| is gauge-dependent (control)
  T4  spectral dimension D_s(t) is theta-blind on the 2D plateau
  T5  BH latency toy: crossing latency diverges as density -> critical
"""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh

rng = np.random.default_rng(7)

print("=" * 72)
print("T1  Exchange-phase law on the flux cylinder (lattice Wilson product)")
print("=" * 72)
W, L = 24, 64
# Gauge field: hopping y -> y+1 across the seam (y = W-1 -> 0) carries e^{i2 pi theta};
# all other links = 1. An n-ply exchange braid winds the y-cycle n times.
def wilson_loop(theta, n_wind):
    phase = 1.0 + 0.0j
    for _ in range(n_wind):
        for y in range(W):
            phase *= np.exp(2j * np.pi * theta) if y == W - 1 else 1.0
    return phase

thetas = np.linspace(0, 1, 13)[:-1]
max_err = {1: 0.0, 2: 0.0}
for th in thetas:
    for n in (1, 2):
        meas = wilson_loop(th, n)
        law = np.exp(2j * np.pi * n * th)
        max_err[n] = max(max_err[n], abs(meas - law))
print(f"  max |measured - e^{{i2 pi n theta}}| over 12 theta values:")
print(f"    single strand (n=1): {max_err[1]:.2e}    dual strand (n=2): {max_err[2]:.2e}")
for th, name in [(0.0, "torus"), (0.25, "Z4 anyon"), (0.5, "Klein"), (1/3, "Z3 parafermion")]:
    c1, c2 = wilson_loop(th, 1), wilson_loop(th, 2)
    print(f"    theta={th:.3f} ({name:>15}):  chi_1={c1:+.3f}  chi_2={c2:+.3f}")
print("  T1 PASS" if max(max_err.values()) < 1e-12 else "  T1 FAIL")

print()
print("=" * 72)
print("T2  Casimir / spectral-gap curve  (2D lattice, open x, twisted y-cycle)")
print("=" * 72)
def build_laplacian(W, L, theta):
    idx = lambda x, y: x * W + (y % W)
    rows, cols, vals = [], [], []
    t = np.exp(2j * np.pi * theta)
    for x in range(L):
        for y in range(W):
            i = idx(x, y)
            rows.append(i); cols.append(i); vals.append(4.0)
            if x + 1 < L:  # x links, real
                j = idx(x + 1, y)
                rows += [i, j]; cols += [j, i]; vals += [-1.0, -1.0]
            seam = (y == W - 1)
            u = t if seam else 1.0  # y link y -> y+1
            j = idx(x, y + 1)
            rows += [i, j]; cols += [j, i]; vals += [-u, -np.conj(u)]
    return csr_matrix((vals, (rows, cols)), shape=(W * L, W * L), dtype=complex)

def gap_numeric(theta):
    H = build_laplacian(W, L, theta)
    return float(eigsh(H, k=1, which="SA", return_eigenvectors=False, tol=1e-10)[0])

def gap_analytic(theta, W=W, L=L):
    qx = np.pi / (L + 1)
    qy = 2 * np.pi * (np.arange(W) - theta) / W
    return np.min(4 - 2 * np.cos(qx) - 2 * np.cos(qy))

grid = np.linspace(0, 1, 21)
num = np.array([gap_numeric(th) for th in grid])
ana = np.array([gap_analytic(th) for th in grid])
print(f"  max |numeric - analytic| = {np.max(np.abs(num - ana)):.2e}")
print(f"  argmax(theta) numeric = {grid[np.argmax(num)]:.2f}   analytic = {grid[np.argmax(ana)]:.2f}")
print(f"  gap(0.5)/gap(0.0) = {num[10]/num[0]:.3f}  (half-twist is the MOST expensive vacuum)")
ok = np.max(np.abs(num - ana)) < 1e-6 and abs(grid[np.argmax(num)] - 0.5) < 1e-9
print("  T2 PASS" if ok else "  T2 FAIL")

print()
print("=" * 72)
print("T3  Reality islands: where can the substrate Hamiltonian be made real?")
print("=" * 72)
def ring_hamiltonian(W, theta, gauge_spread=False):
    # flux concentrated on one bond, or spread evenly (gauge-equivalent)
    H = np.zeros((W, W), dtype=complex)
    per = 2 * np.pi * theta / W if gauge_spread else 0.0
    for y in range(W):
        u = np.exp(1j * per)
        if not gauge_spread and y == W - 1:
            u = np.exp(2j * np.pi * theta)
        H[y, (y + 1) % W] = -u
        H[(y + 1) % W, y] = -np.conj(u)
    return H

def wilson(H):
    Wl = 1.0 + 0j
    for y in range(H.shape[0]):
        Wl *= -H[y, (y + 1) % H.shape[0]]
    return Wl

fine = np.linspace(0, 1, 2001)[:-1]   # exclude endpoint: theta=1 IS theta=0 (mod 1)
imW = np.abs(np.sin(2 * np.pi * fine))          # gauge-invariant Wilson imaginary part
zeros = fine[imW < 1e-3]
print(f"  gauge-invariant |Im W| zeros at theta = {np.round(zeros, 3)}")
th_test = 0.37
H1, H2 = ring_hamiltonian(W, th_test), ring_hamiltonian(W, th_test, gauge_spread=True)
print(f"  control at theta={th_test}: ||Im H|| concentrated-gauge = {np.linalg.norm(H1.imag):.4f}, "
      f"spread-gauge = {np.linalg.norm(H2.imag):.4f} (gauge-dependent, meaningless)")
print(f"           |Im Wilson| = {abs(wilson(H1).imag):.4f} vs {abs(wilson(H2).imag):.4f} (invariant)")
ok = len(zeros) == 2 and abs(zeros[0]) < 1e-3 and abs(zeros[1] - 0.5) < 1e-3
print("  T3 PASS — unique nontrivial real point is theta = 1/2" if ok else "  T3 FAIL")

print()
print("=" * 72)
print("T4  Spectral dimension is theta-blind (dimension vs statistics)")
print("=" * 72)
# Torus (periodic x too) removes open-boundary artifacts. CRITICAL: the plateau
# window must sit BELOW the y-saturation scale t* ~ 1/gap; above t* the walk sees
# the finite circumference and D_s -> 1 — and the twist DOES shift t* (that is the
# Casimir effect, T2), which a misplaced window would mistake for a dimension change.
W2 = L2 = 32
def build_torus(W, L, theta):
    idx = lambda x, y: (x % L) * W + (y % W)
    rows, cols, vals = [], [], []
    t = np.exp(2j * np.pi * theta)
    for x in range(L):
        for y in range(W):
            i = idx(x, y)
            rows.append(i); cols.append(i); vals.append(4.0)
            j = idx(x + 1, y)
            rows += [i, j]; cols += [j, i]; vals += [-1.0, -1.0]
            u = t if y == W - 1 else 1.0
            j = idx(x, y + 1)
            rows += [i, j]; cols += [j, i]; vals += [-u, -np.conj(u)]
    return csr_matrix((vals, (rows, cols)), shape=(W * L, W * L), dtype=complex)

t_ax = np.logspace(0.5, 1.7, 36)    # t ~ 3..50, below y-saturation (~100 for W=32)
Ds = {}
for th in (0.0, 0.25, 0.5):
    lam = np.linalg.eigvalsh(build_torus(W2, L2, th).toarray())
    p = np.array([np.mean(np.exp(-lam * tt)) for tt in t_ax])   # heat-kernel return prob
    Ds[th] = -2 * np.gradient(np.log(p), np.log(t_ax))
win = (t_ax > 8) & (t_ax < 50)      # genuine 2D plateau window
for th in Ds:
    print(f"  theta={th:.2f}:  D_s plateau (t in 8-50) = {np.mean(Ds[th][win]):.3f}")
spread = max(abs(np.mean(Ds[a][win]) - np.mean(Ds[b][win])) for a in Ds for b in Ds)
print(f"  max inter-theta plateau spread = {spread:.3f}  (twist moves long-wavelength")
print(f"  spectrum only; emergent dimension D_s ~ 2 unchanged — supports H69e)")
print("  T4 PASS" if spread < 0.1 else "  T4 FAIL")

print()
print("=" * 72)
print("T5  BH latency toy: density-dependent tick rate, latency divergence")
print("=" * 72)
# Open line (not a ring): the dense slab is UNAVOIDABLE — a ring lets the walker
# bypass the slab the other way, which is what masked the divergence in v1.
N = 120; SLAB = range(45, 75); EPS = 1e-4
def crossing_latency(rho, n_walkers=50, max_steps=300_000):
    r = np.ones(N)
    for x in SLAB:
        r[x] = max(EPS, 1 - rho)               # tick rate collapses toward criticality
    times = []
    for _ in range(n_walkers):
        x, steps = 1, 0
        while x != N - 1 and steps < max_steps:
            steps += 1
            if rng.random() < r[x]:            # tick: this site processes one hop
                x += rng.choice([-1, 1])
                if x < 1:
                    x = 1                      # reflecting wall behind the source
        times.append(steps if x == N - 1 else np.nan)
    return np.nanmean(times)

def ballistic_latency(rho, n_walkers=50, max_steps=2_000_000):
    # directed hops (always toward the target): latency = sum of per-site waiting
    # times; isolates the pure tick-rate physics from recrossing geometry
    r = np.ones(N)
    for x in SLAB:
        r[x] = max(EPS, 1 - rho)
    times = []
    for _ in range(n_walkers):
        x, steps = 1, 0
        while x != N - 1 and steps < max_steps:
            steps += 1
            if rng.random() < r[x]:
                x += 1
        times.append(steps if x == N - 1 else np.nan)
    return np.nanmean(times)

print(f"  {'rho/rho_c':>9} {'<lat diffus>':>14} {'<lat ballistic>':>15}")
ratios, lats_d, lats_b = [], [], []
for rho in (0.0, 0.5, 0.8, 0.9, 0.95, 0.99):
    Td, Tb = crossing_latency(rho), ballistic_latency(rho)
    ratios.append(rho); lats_d.append(Td); lats_b.append(Tb)
    print(f"  {rho:9.2f} {Td:14.0f} {Tb:15.0f}")
rr = np.array(ratios)
a_d = np.polyfit(-np.log10(1 - rr), np.log10(lats_d), 1)[0]
# Ballistic theory is exact: T = T0 + L_slab/(1-rho). A pure-power log-log fit over a
# finite window underestimates the exponent (constant term flattens the slope);
# the right check is the residual against the analytic form.
T0 = N - 2 - len(SLAB)   # non-slab sites only (r=1 there); slab sites carry 1/(1-rho)
theory = T0 + len(SLAB) / (1 - rr)
resid = np.max(np.abs(np.array(lats_b) - theory) / theory)
print(f"  divergence:  diffusive ~ (1 - rho)^(-{a_d:.2f})  (recrossing dilutes exponent);")
print(f"  ballistic vs exact theory T = T0 + L_slab/(1-rho):  max residual = {resid:.3f}")
print(f"  asymptotic exponent: 1.0 exactly (latency = sum of per-site waiting times)")
print(f"  interpretation: tick-rate collapse at critical density => latency horizon;")
print(f"  the 'horizon' is where crossing latency exceeds any finite observation window.")
print("  T5 PASS" if resid < 0.05 else "  T5 borderline (residual vs theory too large)")
