import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import KDTree
from ist_toolkit_v2 import TopologicalHorizon

os.makedirs("outputs", exist_ok=True)


def seed_knots(grid, n_knots=3, radius_frac=0.15, amp=0.4):
    nx, ny = grid.shape
    for _ in range(n_knots):
        cx = np.random.randint(0, nx)
        cy = np.random.randint(0, ny)
        i, j = np.meshgrid(np.arange(nx), np.arange(ny), indexing="ij")
        d = np.sqrt((i - cx) ** 2 + (j - cy) ** 2)
        grid += amp * np.exp(-(d ** 2) / (2 * (radius_frac * nx) ** 2))
    return np.clip(grid, 0, 1)


def extract_loops(grid, threshold=None):
    if threshold is None:
        threshold = grid.mean() + 2 * grid.std()
    mask = grid > threshold
    nx, ny = grid.shape
    loops = []
    visited = np.zeros_like(mask, dtype=bool)
    for i in range(nx):
        for j in range(ny):
            if mask[i, j] and not visited[i, j]:
                stack = [(i, j)]
                component = []
                while stack:
                    ci, cj = stack.pop()
                    if 0 <= ci < nx and 0 <= cj < ny and mask[ci, cj] and not visited[ci, cj]:
                        visited[ci, cj] = True
                        component.append((ci, cj))
                        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                            ni, nj = ci + di, cj + dj
                            if 0 <= ni < nx and 0 <= nj < ny and mask[ni, nj] and not visited[ni, nj]:
                                stack.append((ni, nj))
                if len(component) > 5:
                    loops.append(component)
    return loops


def param_to_3d(u_idx, v_idx, h):
    R = h.radius
    twist = h.twist_param
    n = h.mesh_resolution
    u = 2 * np.pi * u_idx / n
    v = 2 * np.pi * v_idx / n
    x = (R + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)) * np.cos(u) * twist
    y = (R + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)) * np.sin(u) * twist
    z = np.sin(u / 2) * np.sin(v) + np.cos(u / 2) * np.sin(2 * v)
    return x, y, z


def linking_number(loop1_pts, loop2_pts):
    n1 = len(loop1_pts)
    n2 = len(loop2_pts)
    lk = 0.0
    for i in range(n1):
        a = loop1_pts[i]
        a_next = loop1_pts[(i + 1) % n1]
        da = a_next - a
        mid_a = (a + a_next) / 2
        for j in range(n2):
            b = loop2_pts[j]
            b_next = loop2_pts[(j + 1) % n2]
            db = b_next - b
            mid_b = (b + b_next) / 2
            r = mid_b - mid_a
            r_norm = np.linalg.norm(r)
            if r_norm < 1e-10:
                continue
            triple = np.dot(np.cross(da, db), r)
            lk += triple / (r_norm ** 3)
    return lk / (4 * np.pi)


def run():
    np.random.seed(42)

    h = TopologicalHorizon(topology="klein_bottle", twist_param=1.2, radius=10.0, mesh_resolution=60)
    vertices, faces = h.build_mesh()

    rho = h.info_density_grid.copy()
    rho = seed_knots(rho, n_knots=4, radius_frac=0.1, amp=0.4)
    h.info_density_grid = rho

    loops = extract_loops(rho, threshold=rho.mean() + 1.5 * rho.std())
    print(f"Found {len(loops)} information knots")

    loop_3d = []
    for loop in loops:
        pts = np.array([param_to_3d(u, v, h) for u, v in loop])
        loop_3d.append(pts)

    if len(loop_3d) >= 2:
        lk = linking_number(loop_3d[0], loop_3d[1])
        print(f"Linking number between knot 0 and knot 1: {lk:.4f}")

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection="3d")

    n = h.mesh_resolution
    uu = np.linspace(0, 2 * np.pi, n)
    vv = np.linspace(0, 2 * np.pi, n)
    uug, vvg = np.meshgrid(uu, vv, indexing="ij")

    R = h.radius
    twist = h.twist_param
    X = (R + np.cos(uug / 2) * np.sin(vvg) - np.sin(uug / 2) * np.sin(2 * vvg)) * np.cos(uug) * twist
    Y = (R + np.cos(uug / 2) * np.sin(vvg) - np.sin(uug / 2) * np.sin(2 * vvg)) * np.sin(uug) * twist
    Z = np.sin(uug / 2) * np.sin(vvg) + np.cos(uug / 2) * np.sin(2 * vvg)

    norm = plt.Normalize(rho.min(), rho.max())
    colors = plt.cm.plasma(norm(rho))
    face_grid = np.dstack((X, Y, Z))

    stride = 2
    for i in range(0, n - 1, stride):
        for j in range(0, n - 1, stride):
            idx_i = slice(i, min(i + stride + 1, n))
            idx_j = slice(j, min(j + stride + 1, n))
            Xp = X[idx_i, idx_j]
            Yp = Y[idx_i, idx_j]
            Zp = Z[idx_i, idx_j]
            Cp = rho[idx_i, idx_j]
            ax.plot_surface(Xp, Yp, Zp, facecolors=plt.cm.plasma(norm(Cp)), alpha=0.7, rstride=1, cstride=1, shade=False)

    knot_colors = ["red", "cyan", "lime", "magenta", "yellow", "orange"]
    for idx, pts in enumerate(loop_3d):
        color = knot_colors[idx % len(knot_colors)]
        ax.plot(pts[0], pts[1], pts[2], color=color, linewidth=3, label=f"Knot {idx}")
        ax.scatter(pts[0, 0], pts[1, 0], pts[2, 0], color=color, s=60, marker="o")

    ax.set_title("Klein Bottle Horizon with Information Knots", fontsize=14, fontweight="bold")
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")

    mappable = plt.cm.ScalarMappable(norm=norm, cmap="plasma")
    mappable.set_array(rho)
    cbar = fig.colorbar(mappable, ax=ax, shrink=0.6, pad=0.1)
    cbar.set_label("Information Density", fontsize=11)

    save_path = "outputs/klein_info_knot.png"
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"Saved {save_path}")
    plt.close()


if __name__ == "__main__":
    run()
