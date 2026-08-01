from phase8_vacuum_pump_threshold import *

sim = VacuumPumpSimulator(N_base=100, sigma=0.1, seed=7)
rows = sim.run_threshold_scan(n_layers=12, n_new=30)
for r in rows:
    if r["n_layers"] in [0, 3, 5, 8, 10, 11, 12]:
        print("n={:2d} D_eff={:.3f} coh={:.3f}".format(
            r["n_layers"], r["D_eff"], r["coherence"]))
