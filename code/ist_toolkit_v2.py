
"""
================================================================================
INFORMATION SUBSTRATE THEORY (IST) - Computational Toolkit v2.0
================================================================================
A Python module for simulating and analyzing the IST framework.

NEW IN v2.0:
  - Electron mass derivation from single-loop topology
  - Zitterbewegung as loop circulation frequency
  - Fine structure constant as geometric ratio: α = r_e/ƛ_C
  - Complete mass hierarchy visualization
  - Speed-of-light mechanism formalized

Core Physics:
  MASS = Light trapped in topological knots
  The energy moves at c internally, but the knot creates apparent inertia.

  Photon:    No knot → v = c, m = 0
  Electron:  1 Möbius loop → v < c, m = m_e  
  Proton:    3 intertwined quark loops → v < c, m = m_p

Physical Constants (CODATA 2018):
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.signal import find_peaks
import mpmath as mp
from sympy import primepi, prime

# ───────────────────────────────────────────────────────────────────────────────
# PHYSICAL CONSTANTS
# ───────────────────────────────────────────────────────────────────────────────

PHI = (1 + np.sqrt(5)) / 2  # Golden ratio ≈ 1.618033988749895
ALPHA_INV = 137.035999084   # Fine-structure constant inverse
ALPHA = 1 / ALPHA_INV       # ≈ 0.0072973525693
M_PLANCK = 1.220890e19      # Planck mass in GeV/c²
M_PROTON = 0.93827208816    # Proton mass in GeV/c²
M_ELECTRON = 0.51099895000e-3  # Electron mass in GeV/c²
M_NEUTRON = 0.93956542052   # Neutron mass in GeV/c²

# Geometric constants
R_E_CLASSICAL = 2.8179403227e-15  # Classical electron radius (m)
LAMBDA_C_E = 2.4263102389e-12     # Electron Compton wavelength (m)
LAMBDA_BAR_C_E = 3.8615926796e-13 # Reduced Compton wavelength (m)

# ───────────────────────────────────────────────────────────────────────────────
# MODULE 1: Directed Number Algebra
# ───────────────────────────────────────────────────────────────────────────────

class DirectedNumber:
    """IST directed number algebra with non-associative multiplication."""

    def __init__(self, a_up=0.0, a_down=0.0, a_zero=0.0):
        self.a_up = float(a_up)
        self.a_down = float(a_down)
        self.a_zero = float(a_zero)

    def __repr__(self):
        return f"D({self.a_up:.4f}↑, {self.a_down:.4f}↓, {self.a_zero:.4f}⁰)"

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return DirectedNumber(self.a_up + other, self.a_down + other, self.a_zero + other)
        return DirectedNumber(self.a_up + other.a_up, self.a_down + other.a_down, self.a_zero + other.a_zero)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return DirectedNumber(self.a_up * other, self.a_down * other, self.a_zero * other)
        up_product = self.a_up * other.a_up
        down_product = self.a_down * other.a_down
        cross_product = self.a_up * other.a_down + self.a_down * other.a_up
        zero_product = cross_product
        if abs(self.a_zero) > 1e-10 and abs(other.a_zero) > 1e-10:
            P_r = np.random.choice([-1, 1])
            zero_product += self.a_zero * other.a_zero * P_r
        return DirectedNumber(up_product, down_product, zero_product)

    def omega(self):
        """Compression operator Ω."""
        return DirectedNumber(0, 0, self.information())

    def omega_inv(self, deterministic=False):
        """Expansion operator Ω⁻¹."""
        I = self.a_zero
        if deterministic or np.random.random() < 0.5:
            return DirectedNumber(I, 0, 0)
        else:
            return DirectedNumber(0, I, 0)

    def information(self):
        return self.a_up + self.a_down + self.a_zero

    def associator(self, b, c):
        left = (self * b) * c
        right = self * (b * c)
        return left + DirectedNumber(-right.a_up, -right.a_down, -right.a_zero)

    def to_array(self):
        return np.array([self.a_up, self.a_down, self.a_zero])


# ───────────────────────────────────────────────────────────────────────────────
# MODULE 2: RG Flow Simulator
# ───────────────────────────────────────────────────────────────────────────────

class RGFlowSimulator:
    """Renormalization Group flow to golden ratio fixed point."""

    def __init__(self, D_initial=2.0, g_coupling=1.0):
        self.D_initial = D_initial
        self.g = g_coupling
        self.PHI = PHI

    def beta_function(self, D):
        lam = 1 / self.PHI**2
        return -lam * (D - self.PHI)

    def flow(self, ln_mu_max=10.0, num_steps=5000, method='runge_kutta'):
        ln_mu = np.linspace(0, ln_mu_max, num_steps)
        D = np.zeros(num_steps)
        D[0] = self.D_initial
        dt = ln_mu[1] - ln_mu[0]
        for i in range(1, num_steps):
            if method == 'euler':
                D[i] = D[i-1] + self.beta_function(D[i-1]) * dt
            elif method == 'runge_kutta':
                k1 = self.beta_function(D[i-1])
                k2 = self.beta_function(D[i-1] + 0.5*k1*dt)
                k3 = self.beta_function(D[i-1] + 0.5*k2*dt)
                k4 = self.beta_function(D[i-1] + k3*dt)
                D[i] = D[i-1] + (k1 + 2*k2 + 2*k3 + k4) * dt / 6
        return ln_mu, D

    def convergence_time(self, tolerance=1e-6):
        lam = 1 / self.PHI**2
        D_diff = abs(self.D_initial - self.PHI)
        if D_diff < tolerance:
            return 0.0
        return -np.log(tolerance / D_diff) / lam

    @staticmethod
    def effective_coupling(rho_fold, D=None):
        if D is None:
            D = PHI
        return rho_fold ** (1.0 / D)


# ───────────────────────────────────────────────────────────────────────────────
# MODULE 3: Particle Mass Calculator
# ───────────────────────────────────────────────────────────────────────────────

class ParticleMass:
    """IST particle mass derivations from topological mode counting."""

    @staticmethod
    def proton_mass_ratio():
        """M_P/m_p = (2/φ²) × α⁻⁹  [18 modes: 3 quarks × 6 directions]"""
        return (2.0 / PHI**2) * (ALPHA ** (-9))

    @staticmethod
    def proton_mass_prediction():
        return M_PLANCK / ParticleMass.proton_mass_ratio()

    @staticmethod
    def proton_accuracy():
        ratio_pred = ParticleMass.proton_mass_ratio()
        ratio_obs = M_PLANCK / M_PROTON
        accuracy = (1.0 - abs(ratio_pred - ratio_obs) / ratio_obs) * 100
        return ratio_pred, ratio_obs, accuracy

    @staticmethod
    def electron_mass_ratio():
        """M_P/m_e = (12π⁵/φ²) × α⁻⁹  [single chiral loop, 2 spin modes]"""
        return (12 * np.pi**5 / PHI**2) * (ALPHA ** (-9))

    @staticmethod
    def electron_mass_prediction():
        return M_PLANCK / ParticleMass.electron_mass_ratio()

    @staticmethod
    def electron_accuracy():
        ratio_pred = ParticleMass.electron_mass_ratio()
        ratio_obs = M_PLANCK / M_ELECTRON
        accuracy = (1.0 - abs(ratio_pred - ratio_obs) / ratio_obs) * 100
        return ratio_pred, ratio_obs, accuracy

    @staticmethod
    def mass_ratio_proton_to_electron():
        """m_p/m_e = 6π⁵ ≈ 1836  [empirical formula]"""
        return 6 * np.pi**5

    @staticmethod
    def fine_structure_from_geometry():
        """α = r_e / ƛ_C  [geometric ratio of electron loop]"""
        return R_E_CLASSICAL / LAMBDA_BAR_C_E

    @staticmethod
    def general_mass_formula(n_modes, projection_factor):
        return projection_factor * (ALPHA ** (-n_modes / 2))


# ───────────────────────────────────────────────────────────────────────────────
# MODULE 4: Visualization Tools
# ───────────────────────────────────────────────────────────────────────────────

def plot_rg_flow(initial_conditions=None, save_path=None):
    if initial_conditions is None:
        initial_conditions = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(initial_conditions)))
    for D0, color in zip(initial_conditions, colors):
        sim = RGFlowSimulator(D0)
        ln_mu, D = sim.flow(ln_mu_max=10, num_steps=2000)
        ax.plot(ln_mu, D, color=color, alpha=0.8, linewidth=1.5, label=f'D₀ = {D0}')
    ax.axhline(y=PHI, color='red', linestyle='--', linewidth=2, label=f'φ = {PHI:.4f}')
    ax.set_xlabel('ln(μ/μ₀)', fontsize=12)
    ax.set_ylabel('Fractal Dimension D', fontsize=12)
    ax.set_title('RG Flow to Golden Ratio Fixed Point', fontsize=13, fontweight='bold')
    ax.legend(); ax.grid(True, alpha=0.3)
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show(); return fig

def plot_hopf_fiber(n_fibers=12, save_path=None):
    fig = plt.figure(figsize=(14, 5))
    ax1 = fig.add_subplot(131, projection='3d')
    colors = plt.cm.hsv(np.linspace(0, 1, n_fibers))
    for i in range(n_fibers):
        theta_f = np.pi * i / n_fibers
        phi_f = 2 * np.pi * i / n_fibers
        eta = theta_f / 2
        t = np.linspace(0, 2*np.pi, 100)
        x1 = np.cos(eta) * np.cos(phi_f + t)
        x2 = np.cos(eta) * np.sin(phi_f + t)
        x3 = np.sin(eta) * np.cos(t)
        x4 = np.sin(eta) * np.sin(t)
        denom = 1 - x4 + 1e-10
        X, Y, Z = x1/denom, x2/denom, x3/denom
        ax1.plot(X, Y, Z, color=colors[i], alpha=0.6, linewidth=1.5)
    ax1.set_title(f'Hopf Fibration S³ → S²\n({n_fibers} Fibers)')
    ax1.set_xlim([-3, 3]); ax1.set_ylim([-3, 3]); ax1.set_zlim([-3, 3])

    ax2 = fig.add_subplot(132, projection='3d')
    u, v = np.meshgrid(np.linspace(0, 2*np.pi, 50), np.linspace(0, np.pi, 50))
    ax2.plot_surface(np.sin(v)*np.cos(u), np.sin(v)*np.sin(u), np.cos(v), alpha=0.2, color='cyan')
    for i in range(n_fibers):
        theta_f = np.pi * i / n_fibers
        phi_f = 2 * np.pi * i / n_fibers
        ax2.scatter([np.sin(theta_f)*np.cos(phi_f)], [np.sin(theta_f)*np.sin(phi_f)], [np.cos(theta_f)], color=colors[i], s=50)
    ax2.set_title('S² Base Space')

    ax3 = fig.add_subplot(133, projection='3d')
    u_m, v_m = np.meshgrid(np.linspace(0, 2*np.pi, 100), np.linspace(-0.5, 0.5, 20))
    R = 2
    x_m = (R + v_m * np.cos(u_m/2)) * np.cos(u_m)
    y_m = (R + v_m * np.cos(u_m/2)) * np.sin(u_m)
    z_m = v_m * np.sin(u_m/2)
    ax3.plot_surface(x_m, y_m, z_m, alpha=0.7, cmap='coolwarm')
    ax3.set_title('Möbius Strip')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show(); return fig


# ───────────────────────────────────────────────────────────────────────────────
# MODULE 5: Utility Functions
# ───────────────────────────────────────────────────────────────────────────────

def ist_summary():
    """Print a summary of key IST predictions and measurements."""
    print("=" * 65)
    print("INFORMATION SUBSTRATE THEORY - SUMMARY")
    print("=" * 65)

    # Proton mass
    ratio_pred, ratio_obs, accuracy = ParticleMass.proton_accuracy()
    print(f"\n[PROTON MASS]")
    print(f"  Formula: M_P/m_p = (2/φ²) × α⁻⁹")
    print(f"  Predicted: {ratio_pred:.6e}")
    print(f"  Observed:  {ratio_obs:.6e}")
    print(f"  Accuracy:  {accuracy:.4f}%")

    # Electron mass
    ratio_pred_e, ratio_obs_e, accuracy_e = ParticleMass.electron_accuracy()
    print(f"\n[ELECTRON MASS]")
    print(f"  Formula: M_P/m_e = (12π⁵/φ²) × α⁻⁹")
    print(f"  Predicted: {ratio_pred_e:.6e}")
    print(f"  Observed:  {ratio_obs_e:.6e}")
    print(f"  Accuracy:  {accuracy_e:.4f}%")
    print(f"  Equivalent: m_p/m_e = 6π⁵ ≈ {ParticleMass.mass_ratio_proton_to_electron():.2f}")

    # Fine structure
    alpha_geom = ParticleMass.fine_structure_from_geometry()
    print(f"\n[FINE-STRUCTURE CONSTANT]")
    print(f"  α = r_e/ƛ_C = {alpha_geom:.10f}")
    print(f"  Actual α = {ALPHA:.10f}")
    print(f"  This is a geometric ratio—no free parameters!")

    # RG flow
    print(f"\n[RG FLOW]")
    print(f"  Fixed point: D = φ ≈ {PHI:.4f}")
    print(f"  Stability eigenvalue: λ = 1/φ² ≈ {1/PHI**2:.4f}")

    print("\n" + "=" * 65)


# ───────────────────────────────────────────────────────────────────────────────
# MODULE 6: Topological Horizon (Black Hole)
# ───────────────────────────────────────────────────────────────────────────────

class TopologicalHorizon:
    """Black hole horizon as a non-orientable topological space (Klein bottle) within IST.

    Models the horizon as an information-density surface whose topology
    determines entropy, ringdown, and information leakage.

    Parameters
    ----------
    topology : str
        One of "sphere", "torus", "klein_bottle".
    twist_param : float
        Twist parameter for Klein bottle (dimensionless).
    radius : float
        Schwarzschild radius in Planck units.
    mesh_resolution : int
        Number of points per dimension for the mesh.
    """

    L_PLANCK = 1.616255e-35       # Planck length (m)
    T_PLANCK = 5.391247e-44       # Planck time (s)

    def __init__(self, topology="klein_bottle", twist_param=1.0, radius=10.0, mesh_resolution=50):
        self.topology = topology
        self.twist_param = twist_param
        self.radius = radius
        self.mesh_resolution = mesh_resolution
        self.info_density_grid = None
        self._mesh = None
        self._vertices = None
        self._faces = None

    # ── Mesh Construction ──────────────────────────────────────────────────

    def build_mesh(self):
        """Construct a triangulated surface mesh for the chosen topology.

        Returns
        -------
        vertices : ndarray (N, 3)
        faces : ndarray (M, 3)
        """
        n = self.mesh_resolution
        u = np.linspace(0, 2 * np.pi, n)
        v = np.linspace(0, 2 * np.pi, n)
        u, v = np.meshgrid(u, v, indexing="ij")

        if self.topology == "sphere":
            x = self.radius * np.sin(v) * np.cos(u)
            y = self.radius * np.sin(v) * np.sin(u)
            z = self.radius * np.cos(v)

        elif self.topology == "torus":
            R = self.radius
            r = R / 3
            x = (R + r * np.cos(v)) * np.cos(u)
            y = (R + r * np.cos(v)) * np.sin(u)
            z = r * np.sin(v)

        elif self.topology == "klein_bottle":
            R = self.radius
            twist = self.twist_param
            x = (R + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)) * np.cos(u)
            y = (R + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)) * np.sin(u)
            z = np.sin(u / 2) * np.sin(v) + np.cos(u / 2) * np.sin(2 * v)
            x *= twist

        else:
            raise ValueError(f"Unknown topology: {self.topology}")

        points = np.stack([x.ravel(), y.ravel(), z.ravel()], axis=1)
        faces = []
        for i in range(n - 1):
            for j in range(n - 1):
                i0 = i * n + j
                i1 = i0 + 1
                i2 = (i + 1) * n + j
                i3 = i2 + 1
                faces.append([i0, i1, i2])
                faces.append([i1, i3, i2])

        self._vertices = points
        self._faces = np.array(faces)

        nx, ny = x.shape
        self.info_density_grid = np.ones((nx, ny)) * 0.5

        return self._vertices, self._faces

    # ── Entropy Calculation ────────────────────────────────────────────────

    def surface_area(self):
        if self._vertices is None:
            self.build_mesh()
        v = self._vertices
        f = self._faces
        tri = v[f]
        a = tri[:, 1] - tri[:, 0]
        b = tri[:, 2] - tri[:, 0]
        normals = np.cross(a, b)
        area = 0.5 * np.sum(np.linalg.norm(normals, axis=1))
        return area

    def compute_entropy(self):
        """Corrected Bekenstein-Hawking entropy for the given topology.

        S = A / (4 ℓ_P²) × f(topology)

        where f(sphere) = 1, f(torus) = 1, f(klein_bottle) = 1 + |twist_param|.
        """
        A = self.surface_area()
        S_bh = A / (4 * self.L_PLANCK**2)

        topo_factor = {"sphere": 1.0, "torus": 1.0, "klein_bottle": 1.0 + abs(self.twist_param)}
        S = S_bh * topo_factor.get(self.topology, 1.0)
        return S

    # ── Information Density Evolution ──────────────────────────────────────

    def evolve_info(self, dt, diffusion_coeff=0.01):
        """Evolve info density using a diffusion-like IST Hamiltonian.

        Uses finite-difference Laplacian on the parametric grid with
        periodic boundary conditions and a Klein-bottle sign flip on twist.
        """
        if self.info_density_grid is None:
            self.build_mesh()

        rho = self.info_density_grid.copy()
        n = self.mesh_resolution

        lap = (
            np.roll(rho, -1, axis=0) + np.roll(rho, 1, axis=0)
            + np.roll(rho, -1, axis=1) + np.roll(rho, 1, axis=1)
            - 4 * rho
        ) / (2 * np.pi / n)**2

        if self.topology == "klein_bottle":
            lap *= (1.0 + 0.1 * self.twist_param * np.sin(np.linspace(0, 2 * np.pi, n))[:, None])

        rho_new = rho + diffusion_coeff * lap * dt
        rho_new = np.clip(rho_new, 0, 1)

        leakage = (1.0 - rho_new.mean() / rho.mean()) if rho.mean() > 0 else 0.0

        self.info_density_grid = rho_new
        return leakage

    # ── Ringdown Waveform ──────────────────────────────────────────────────

    def waveform_signal(self, duration=100.0, dt=0.1, mode_l=2, mode_m=0):
        """Compute ringdown gravitational-wave Fourier modes.

        Models the horizon oscillation as a damped sinusoid whose
        frequency and damping depend on topology.

        Returns
        -------
        t : ndarray
        signal : ndarray
        freqs : ndarray
        spectrum : ndarray
        """
        t = np.arange(0, duration, dt)

        M = self.radius * self.L_PLANCK / (2 * 1.0)
        omega_qnm = 1.0 / (3 * np.sqrt(3) * M)
        tau = 4 * M

        if self.topology == "klein_bottle":
            omega_qnm *= 1.0 + 0.05 * self.twist_param
            tau *= 1.0 + 0.1 * abs(self.twist_param)

        if self.topology == "sphere":
            omega_qnm *= 1.0
        elif self.topology == "torus":
            omega_qnm *= 1.1

        signal = np.exp(-t / tau) * np.sin(omega_qnm * t)
        signal[:int(10 / dt)] *= np.linspace(0, 1, int(10 / dt))

        n_fft = len(signal)
        spectrum = np.abs(np.fft.rfft(signal))
        freqs = np.fft.rfftfreq(n_fft, d=dt)

        return t, signal, freqs, spectrum


# ───────────────────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ist_summary()
    print("\n✓ IST Toolkit v2.0 loaded successfully")
