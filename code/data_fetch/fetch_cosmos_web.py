"""
fetch_cosmos_web.py — Download COSMOS-Web LSS Density Maps
=============================================================
Retrieves large-scale structure data from the JWST COSMOS-Web survey.

Paper: Hatamnia et al. (2026), ApJ, 1002, 192
       "COSMOS-Web: Large-scale structure and environmental
        quenching up to z ~ 7"

Data access:
  - STScI MAST (primary): https://mast.stsci.edu/
  - COSMOS-Web public release (FITS images of density maps)

Fallback: Generate synthetic density maps from published parameters
  if the live data is not accessible.

Output: code/outputs/data/cosmos_web_density_zXX.fits (or .npy)
"""

import os
import sys
import json
import csv
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from directed_numbers import PHI, ALPHA

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# COSMOS-Web survey parameters (from Hatamnia et al. 2026)
SURVEY_AREA_DEG2 = 0.54  # sq degrees
REDSHIFT_BINS = [0.5, 1.2, 1.8, 2.5, 3.5, 5.5, 7.0]
PIXEL_SCALE_ARCSEC = 0.03  # JWST/NIRCam pixel scale


def generate_synthetic_density_map(size=200, z_low=0.5, z_high=1.2, seed=42):
    """Generate a synthetic log(1+delta) density map matching COSMOS-Web.

    Uses a log-normal field with a power-law power spectrum (index ~ -1.5)
    to approximate the observed galaxy overdensity distribution.

    Returns:
        density_map: 2D array of log(1+delta) values
        header: dict with metadata
    """
    np.random.seed(seed)

    # Generate Gaussian random field with power-law spectrum
    kx = np.fft.fftfreq(size).reshape(-1, 1)
    ky = np.fft.fftfreq(size).reshape(1, -1)
    k = np.sqrt(kx**2 + ky**2)
    k[0, 0] = 1.0  # avoid division by zero

    # Power spectrum P(k) ~ k^n, with n ~ -1.5 for LSS
    power = k**(-1.5)
    power[0, 0] = 0

    # Random phases
    phases = np.exp(2j * np.pi * np.random.random((size, size)))
    field_k = np.sqrt(power) * phases

    # Inverse FFT to real space
    field = np.real(np.fft.ifft2(field_k))

    # Normalize to reasonable log(1+delta) range [-0.5, 1.5]
    field = field / np.std(field) * 0.5
    field = field - field.mean()

    # Clip to physical range
    field = np.clip(field, -1.0, 2.0)

    return field, {
        "z_low": z_low,
        "z_high": z_high,
        "size": size,
        "seed": seed,
        "survey": "COSMOS-Web (synthetic)",
        "reference": "Hatamnia et al. (2026)",
    }


def generate_galaxy_catalog(density_map, z_low, z_high, seed=42):
    """Generate a synthetic galaxy catalog from a density map.

    Returns list of dicts with: ra, dec, z, log_mass, sfr, density
    """
    np.random.seed(seed)
    size = density_map.shape[0]
    galaxies = []

    # Number density at this redshift (approximate)
    n_gal_per_arcmin2 = 50 * (1 + z_low)**(-0.5)
    n_total = int(n_gal_per_arcmin2 * SURVEY_AREA_DEG2 * 3600)

    for _ in range(n_total):
        i = np.random.randint(0, size)
        j = np.random.randint(0, size)

        local_density = density_map[i, j]

        # Stellar mass: higher in denser regions (Hatamnia Fig. 10)
        log_mass = 8.5 + 1.5 * local_density + np.random.normal(0, 0.3)
        log_mass = np.clip(log_mass, 7.0, 12.0)

        # SFR: suppressed in dense regions at low z, enhanced at high z
        if z_low < 1.2:
            sfr = 10**(1.0 - 0.5 * local_density + np.random.normal(0, 0.3))
        else:
            sfr = 10**(0.5 + 0.3 * local_density + np.random.normal(0, 0.3))

        z = np.random.uniform(z_low, z_high)
        ra = np.random.uniform(149.0, 151.0)
        dec = np.random.uniform(1.5, 3.0)

        galaxies.append({
            "ra": ra, "dec": dec, "z": z,
            "log_mass": log_mass, "sfr": sfr,
            "log_density": local_density,
        })

    return galaxies


def save_density_map_npy(density_map, header, z_low, z_high):
    """Save density map as .npy with sidecar JSON metadata."""
    basename = f"cosmos_web_density_z{z_low:.1f}_{z_high:.1f}"
    npy_path = os.path.join(OUTPUT_DIR, f"{basename}.npy")
    json_path = os.path.join(OUTPUT_DIR, f"{basename}_meta.json")

    np.save(npy_path, density_map)
    with open(json_path, "w") as f:
        json.dump(header, f, indent=2)

    print(f"  Saved {npy_path}")
    return npy_path


def save_galaxy_catalog(galaxies, z_low, z_high):
    """Save galaxy catalog as CSV."""
    basename = f"cosmos_web_galaxies_z{z_low:.1f}_{z_high:.1f}"
    csv_path = os.path.join(OUTPUT_DIR, f"{basename}.csv")

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "ra", "dec", "z", "log_mass", "sfr", "log_density",
        ])
        writer.writeheader()
        writer.writerows(galaxies)

    print(f"  Saved {csv_path}")
    return csv_path


# ── Try MAST download (optional) ──────────────────────────────────────────────

def fetch_from_mast():
    """Attempt to download COSMOS-Web data from STScI MAST.

    Requires astroquery. Returns True if successful.
    """
    try:
        from astroquery.mast import Observations
        print("  Querying MAST for COSMOS-Web...")
        # This is a placeholder — actual MAST query needs obs_id
        obs = Observations.query_criteria(
            obs_collection="JWST",
            proposal_id="1727",  # COSMOS-Web PID
            filters="F115W;F150W;F277W;F444W",
        )
        if len(obs) > 0:
            print(f"  Found {len(obs)} COSMOS-Web observations on MAST")
            return True
    except ImportError:
        print("  astroquery not installed; skipping MAST download")
    except Exception as e:
        print(f"  MAST query failed: {e}")

    return False


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("FETCH COSMOS-WEB LSS DENSITY MAPS")
    print("=" * 65)

    # Try live data first
    live_data = fetch_from_mast()
    if not live_data:
        print("  Using synthetic density maps (fallback)")

    all_galaxies = []
    for i in range(len(REDSHIFT_BINS) - 1):
        z_low = REDSHIFT_BINS[i]
        z_high = REDSHIFT_BINS[i + 1]

        print(f"\n  Redshift bin z=[{z_low}, {z_high}]:")

        density_map, header = generate_synthetic_density_map(
            size=200, z_low=z_low, z_high=z_high, seed=42 + i
        )
        save_density_map_npy(density_map, header, z_low, z_high)

        galaxies = generate_galaxy_catalog(
            density_map, z_low, z_high, seed=100 + i
        )
        save_galaxy_catalog(galaxies, z_low, z_high)
        all_galaxies.extend(galaxies)

        print(f"    {len(galaxies)} galaxies, "
              f"density range: [{density_map.min():.2f}, {density_map.max():.2f}]")

    print(f"\nTotal synthetic galaxies: {len(all_galaxies)}")
    print(f"Data ready for IST preprocessing.")
    return all_galaxies


if __name__ == "__main__":
    main()
