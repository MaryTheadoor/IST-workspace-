"""
preprocess_lss.py — Convert Galaxy Catalogs to IST Associator Threads
========================================================================
Maps COSMOS-Web galaxy overdensity and stellar mass data into
directed number threads, computing associator charge Xi and
topological information I_topo for each galaxy.

Master equation (galaxy scale, negligible time crystal):
  M_eff = M_baryon + (alpha/phi^2) * Xi

Therefore:
  I_topo = M_baryon * l_gal / (hbar/c)
  Xi     = (M_eff - M_baryon) * (phi^2/alpha) * l_gal / (hbar/c)

Input:  code/outputs/data/cosmos_web_galaxies_z*.csv
Output: code/outputs/data/lss_threads.json
"""

import os
import sys
import csv
import json
import glob
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from directed_numbers import (
    DirectedNumber, DirectedZero, Thread, TemporalThread,
    PHI, ALPHA,
)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "data")
INPUT_GLOB = os.path.join(OUTPUT_DIR, "cosmos_web_galaxies_z*.csv")
OUTPUT_JSON = os.path.join(OUTPUT_DIR, "lss_threads.json")

# Physical constants
M_SOLAR = 1.989e30  # kg
HBAR = 1.054571817e-34
C = 2.99792458e8
G = 6.67430e-11

MPC = 3.0857e22  # m
KPC = 3.0857e19  # m

# Galaxy scale parameters
L_GAL = 3.0 * KPC  # characteristic scale ~ 3 kpc (typical disk scale length)
F_TOPO = 1.5  # Klein bottle topology factor for halo


def baryon_mass_to_itopo(mass_kg, length_scale=L_GAL):
    """Convert baryonic mass to topological information I_topo.

    I_topo = M_baryon * l / (hbar/c)
    """
    return mass_kg * length_scale / (HBAR / C)


def compute_xi_from_overdensity(log_mass, log_density, z):
    """Compute associator charge Xi from galaxy properties.

    Uses the master equation:
      M_eff = M_baryon + (alpha/phi^2) * Xi

    The effective mass M_eff is the dynamical mass inferred from
    the local overdensity. For a galaxy in a region with overdensity
    log(1+delta), the excess mass is:

      M_excess = M_baryon * (exp(log_density) - 1)

    Then:
      Xi = M_excess * l_gal / (hbar/c) * (phi^2/alpha)
    """
    mass_kg = 10**log_mass * M_SOLAR

    # Excess mass from environmental overdensity
    if log_density > 0:
        excess_fraction = np.exp(log_density) - 1
    else:
        excess_fraction = log_density  # linear for underdense

    # Cap at reasonable values
    excess_fraction = np.clip(excess_fraction, 0, 100)

    M_excess = mass_kg * excess_fraction

    # Convert to Xi
    xi = M_excess * L_GAL / (HBAR / C) * PHI**2 / ALPHA

    return max(xi, 0)


def galaxy_to_thread(log_mass, log_density, z, ra, dec, index=0):
    """Convert a single galaxy to an IST Thread.

    The thread encodes:
      - Primary: I_topo (baryonic information) as UP amplitude
      - Secondary: Xi (associator charge) as DOWN amplitude
      - The ratio Xi/I_topo indicates the dark matter fraction
    """
    mass_kg = 10**log_mass * M_SOLAR
    I_topo = baryon_mass_to_itopo(mass_kg)
    Xi = compute_xi_from_overdensity(log_mass, log_density, z)

    thread = Thread(time_index=index)

    # Baryonic information (positive, manifest)
    dn_baryon = DirectedNumber(np.log10(max(I_topo, 1)), "up")
    thread.push(dn_baryon)

    # Associator charge (dark matter binding)
    if Xi > 0:
        dn_xi = DirectedNumber(np.log10(Xi), "down")
        thread.push(dn_xi)

    # Environmental quenching flag
    if log_density > 0.5 and z < 1.2:
        # Quenched: compressed state
        dn_quench = DirectedZero(
            memory=DirectedNumber(abs(log_density), "down")
        )
        thread.push(dn_quench)

    metadata = {
        "index": index,
        "ra": ra,
        "dec": dec,
        "z": z,
        "log_mass": log_mass,
        "log_density": log_density,
        "I_topo": I_topo,
        "log10_I_topo": np.log10(max(I_topo, 1)),
        "Xi": Xi,
        "log10_Xi": np.log10(max(Xi, 1)) if Xi > 0 else 0,
        "Xi_over_I_topo": Xi / I_topo if I_topo > 0 else 0,
        "n_elements": len(thread.elements),
        "total_info": thread.info_total(),
        "quenched": log_density > 0.5 and z < 1.2,
    }

    return thread, metadata


def load_galaxies(glob_pattern=None):
    """Load galaxy catalogs from all redshift bins."""
    if glob_pattern is None:
        glob_pattern = INPUT_GLOB

    files = sorted(glob.glob(glob_pattern))
    if not files:
        print(f"  No galaxy catalogs found matching: {glob_pattern}")
        print(f"  Run fetch_cosmos_web.py first.")
        return []

    all_galaxies = []
    for f in files:
        z_info = os.path.basename(f).replace("cosmos_web_galaxies_z", "").replace(".csv", "")
        print(f"  Loading {f} ({len(open(f).readlines()) - 1} galaxies)")

        with open(f, "r") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                row["source_file"] = f
                all_galaxies.append(row)

    return all_galaxies


def preprocess_galaxies(galaxies, max_galaxies=10000):
    """Convert galaxies to IST threads.

    For large catalogs, sample to max_galaxies to keep memory manageable.
    """
    if len(galaxies) > max_galaxies:
        indices = np.random.choice(len(galaxies), max_galaxies, replace=False)
        galaxies = [galaxies[i] for i in indices]
        print(f"  Subsampled to {max_galaxies} galaxies")

    threads = {}
    metadata_list = []

    for i, gal in enumerate(galaxies):
        log_mass = float(gal["log_mass"])
        log_density = float(gal["log_density"])
        z = float(gal["z"])
        ra = float(gal["ra"])
        dec = float(gal["dec"])

        thread, meta = galaxy_to_thread(log_mass, log_density, z, ra, dec, i)
        threads[i] = thread
        metadata_list.append(meta)

    return threads, metadata_list


def compute_environmental_stats(metadata_list):
    """Compute statistics split by environment and redshift."""
    quenched = [m for m in metadata_list if m["quenched"]]
    star_forming = [m for m in metadata_list if not m["quenched"]]

    stats = {
        "n_total": len(metadata_list),
        "n_quenched": len(quenched),
        "n_star_forming": len(star_forming),
        "quenched_fraction": len(quenched) / len(metadata_list),
    }

    if quenched:
        stats["quenched_mean_Xi_over_I"] = np.mean([m["Xi_over_I_topo"] for m in quenched])
        stats["quenched_mean_log_mass"] = np.mean([m["log_mass"] for m in quenched])

    if star_forming:
        stats["sf_mean_Xi_over_I"] = np.mean([m["Xi_over_I_topo"] for m in star_forming])
        stats["sf_mean_log_mass"] = np.mean([m["log_mass"] for m in star_forming])

    return stats


def save_results(metadata_list, stats):
    """Save preprocessed galaxy results and environmental statistics."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save full metadata
    output = {
        "n_galaxies": len(metadata_list),
        "metadata": metadata_list[:500],  # Top 500 for preview
        "environmental_stats": stats,
        "config": {
            "phi": PHI,
            "alpha": ALPHA,
            "L_gal_kpc": L_GAL / KPC,
            "f_topo": F_TOPO,
        },
    }

    with open(OUTPUT_JSON, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"  Saved {OUTPUT_JSON}")

    # Save stats separately
    stats_path = os.path.join(OUTPUT_DIR, "lss_environmental_stats.json")
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"  Saved {stats_path}")

    return OUTPUT_JSON


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("PREPROCESS LSS -> IST THREADS")
    print("=" * 65)

    galaxies = load_galaxies()
    if not galaxies:
        print("\n  No data found. Generating synthetic galaxy catalog...")
        from data_fetch.fetch_cosmos_web import (
            generate_synthetic_density_map,
            generate_galaxy_catalog,
            save_galaxy_catalog,
        )
        # Generate one redshift bin
        density_map, _ = generate_synthetic_density_map(200, 0.5, 1.2, seed=42)
        galaxies_raw = generate_galaxy_catalog(density_map, 0.5, 1.2, seed=100)
        save_galaxy_catalog(galaxies_raw, 0.5, 1.2)
        galaxies = galaxies_raw
        print(f"  Generated {len(galaxies)} synthetic galaxies")

    print(f"\n  Total galaxies loaded: {len(galaxies)}")
    threads, metadata = preprocess_galaxies(galaxies, max_galaxies=5000)

    stats = compute_environmental_stats(metadata)

    print(f"\n  Environmental statistics:")
    print(f"    Total galaxies:     {stats['n_total']}")
    print(f"    Quenched:           {stats['n_quenched']} ({stats['quenched_fraction']:.1%})")
    print(f"    Star-forming:       {stats['n_star_forming']}")

    if "quenched_mean_Xi_over_I" in stats:
        print(f"    Quenched <Xi/I>:    {stats['quenched_mean_Xi_over_I']:.4f}")
        print(f"    SF <Xi/I>:          {stats['sf_mean_Xi_over_I']:.4f}")

    # IST prediction: quenched galaxies should have HIGHER Xi/I ratio
    # (more associator charge per unit baryonic mass -> stronger binding)
    if "quenched_mean_Xi_over_I" in stats and "sf_mean_Xi_over_I" in stats:
        ratio = stats["quenched_mean_Xi_over_I"] / stats["sf_mean_Xi_over_I"]
        print(f"    Quenched/SF Xi ratio: {ratio:.2f}x")
        print(f"    IST prediction: >1.0 (associator binding = quenching)")

    save_results(metadata, stats)
    print("\n  Preprocessing complete.")
    return threads, metadata


if __name__ == "__main__":
    main()
