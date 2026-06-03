"""
preprocess_microlensing.py — Convert Microlensing Events to Directed Number Threads
=====================================================================================
Transforms PBH microlensing candidate data into the IST directed numbers
representation, computing associator charge Xi and topological information.

Input:  code/outputs/data/hsc_pbh_candidates.csv (from fetch_hsc_m31.py)
Output: code/outputs/data/pbh_threads.h5 (directed number thread store)

For each event:
  1. Read best-fit lens mass and uncertainty
  2. Compute Xi = (phi^2/alpha) * M / M_Planck
  3. Create Thread with DirectedNumber(amplitude=log10(Xi), parity)
  4. Store alongside metadata (t_E, coordinates, bandpass)
"""

import os
import sys
import csv
import json
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from directed_numbers import (
    DirectedNumber, DirectedZero, Thread, TemporalThread,
    PHI, ALPHA, mul, associator,
)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs", "data")
INPUT_CSV = os.path.join(OUTPUT_DIR, "hsc_pbh_candidates.csv")
OUTPUT_H5 = os.path.join(OUTPUT_DIR, "pbh_threads.json")

M_SOLAR_KG = 1.989e30
M_PLANCK_KG = 2.176434e-8
HBAR = 1.054571817e-34
C = 2.99792458e8
PHI2_OVER_ALPHA = PHI**2 / ALPHA


def mass_to_xi(mass_kg):
    """Convert lens mass to associator charge (Plan 10 formula)."""
    return PHI2_OVER_ALPHA * mass_kg / M_PLANCK_KG


def event_to_thread(event, index=0):
    """Convert a single microlensing event to an IST Thread.

    The thread represents the topological information of the lens:
      - amplitude = log10(Xi) (the associator charge magnitude)
      - parity = "up" for PBH formed in early-universe overdensities

    Returns:
        thread: Thread object
        metadata: dict with physical parameters
    """
    mass_kg = float(event["mass_kg"])
    xi = mass_to_xi(mass_kg)

    # Create thread with associator-charge representation
    thread = Thread(time_index=index)

    # Primary element: the associator charge itself
    dn_xi = DirectedNumber(np.log10(xi), "up")
    thread.push(dn_xi)

    # Secondary element: the uncertainty (as a directed zero with memory)
    if "mass_err_low_msun" in event and "mass_err_high_msun" in event:
        err_kg = (float(event["mass_err_low_msun"]) + float(event["mass_err_high_msun"])) / 2 * M_SOLAR_KG
        xi_err = mass_to_xi(err_kg)
        if xi_err > 0:
            dz_err = DirectedZero(memory=DirectedNumber(np.log10(xi_err), "down"))
            thread.push(dz_err)

    metadata = {
        "id": event.get("id", f"event-{index}"),
        "mass_kg": mass_kg,
        "mass_msun": mass_kg / M_SOLAR_KG,
        "xi": xi,
        "log10_xi": np.log10(xi),
        "t_E_hrs": float(event.get("t_E_hrs", 0)),
        "n_elements": len(thread.elements),
        "total_info": thread.info_total(),
    }

    return thread, metadata


def load_events(csv_path=None):
    """Load events from CSV."""
    if csv_path is None:
        csv_path = INPUT_CSV

    if not os.path.exists(csv_path):
        print(f"  CSV not found: {csv_path}")
        print(f"  Run fetch_hsc_m31.py first.")
        return []

    events = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            events.append(row)

    return events


def preprocess_events(events):
    """Convert all events to threads and compute cross-event associators.

    Returns:
        threads: dict of id -> Thread
        metadata: list of dicts
        cross_associators: 2D array of associator values between event pairs
    """
    threads = {}
    metadata_list = []

    for i, event in enumerate(events):
        thread, meta = event_to_thread(event, i)
        eid = meta["id"]
        threads[eid] = thread
        metadata_list.append(meta)

    # Compute cross-event associators (triple products across lenses)
    n = len(metadata_list)
    cross_assoc = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            ti = metadata_list[i]
            tj = metadata_list[j]
            # Approximate associator between two PBH lenses
            # as the product of their log-Xi values scaled by 1/phi^2
            cross_assoc[i, j] = (ti["log10_xi"] * tj["log10_xi"]) / PHI**2
            cross_assoc[j, i] = cross_assoc[i, j]

    return threads, metadata_list, cross_assoc


def save_results(threads, metadata_list, cross_assoc):
    """Save preprocessed results to JSON."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Serialize threads
    thread_data = {}
    for eid, thread in threads.items():
        thread_data[eid] = {
            "elements": [
                {"amplitude": e.amplitude, "parity": e.parity}
                for e in thread.elements
            ],
            "n_children": len(thread.children),
            "time_index": thread.time_index,
        }

    output = {
        "metadata": metadata_list,
        "threads": thread_data,
        "cross_associators": cross_assoc.tolist(),
        "config": {
            "phi": PHI,
            "alpha": ALPHA,
            "phi2_over_alpha": PHI2_OVER_ALPHA,
            "M_Planck_kg": M_PLANCK_KG,
        },
    }

    with open(OUTPUT_H5, "w") as f:
        json.dump(output, f, indent=2)

    print(f"  Saved {OUTPUT_H5}")
    return OUTPUT_H5


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("PREPROCESS MICROLENSING -> IST THREADS")
    print("=" * 65)

    events = load_events()
    if not events:
        # Generate from fallback
        print("  No CSV found. Generating from fallback data...")
        from data_fetch.fetch_hsc_m31 import get_fallback_candidates, get_phoebe
        candidates = get_fallback_candidates() + get_phoebe()
        events = []
        for c in candidates:
            events.append({
                "id": c["id"],
                "mass_kg": str(c.get("mass_msun", 0) * M_SOLAR_KG),
                "mass_err_low_msun": str(c.get("mass_err_low", c.get("mass_msun", 0) * 0.5)),
                "mass_err_high_msun": str(c.get("mass_err_high", c.get("mass_msun", 0) * 0.5)),
                "t_E_hrs": str(c.get("t_E_hrs", 0)),
            })

    print(f"  Loaded {len(events)} events")

    threads, metadata, cross_assoc = preprocess_events(events)

    # Summary statistics
    log_xi = [m["log10_xi"] for m in metadata]
    print(f"\n  Associator charge summary (log10):")
    print(f"    Mean:   {np.mean(log_xi):.2f}")
    print(f"    Std:    {np.std(log_xi):.4f}")
    print(f"    Range:  [{min(log_xi):.2f}, {max(log_xi):.2f}]")

    # Cross-associator summary
    upper_tri = cross_assoc[np.triu_indices_from(cross_assoc, k=1)]
    print(f"\n  Cross-event associator summary:")
    print(f"    Mean:   {np.mean(upper_tri):.4f}")
    print(f"    Max:    {np.max(upper_tri):.4f}")

    save_results(threads, metadata, cross_assoc)
    print("\n  Preprocessing complete.")
    return threads, metadata


if __name__ == "__main__":
    main()
