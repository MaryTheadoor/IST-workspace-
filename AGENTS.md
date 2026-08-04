# IST-workspace AGENTS.md

Research repo for Information Substrate Theory (IST). All work happens here;
the `opencode` repo in the parent dir is unrelated tooling.

## Running code & tests (non-obvious)

- Tests live in `tests/` but add `../code` to `sys.path` at the top of each
  file. **Pytest must be run from `code/`**, not the repo root:
  `cd code && python -m pytest ../tests/ -q`. Running from root breaks imports.
- Always use the system Python (3.14, numpy/scipy/matplotlib installed). No venv.
- Full suite is ~150s. Run individual phase tests with
  `python -m pytest ../tests/test_phaseN_*.py -q` from `code/`.

## Phase conventions

- A "phase" = `code/phaseN_*.py` + `tests/test_phaseN_*.py` +
  outputs in `code/outputs/phaseN/` + a row in the phase map.
- Phase numbers in code/outputs are NOT contiguous with commit history
  (e.g. 26 before 27-41) — always check `code/outputs/` before assuming.
- The phase map lives in THREE places that must stay in sync:
  `README.md`, `main/cross_phase_synthesis.md`, and
  `main/synthesis_paper.md` (§8.1x sections). When adding a phase, update all
  three (and `notes/retrospective_cross_analysis.md` for cross-phase insights).
- **Only `main/cross_phase_synthesis.md` has the complete phase table.**
  `main/synthesis_paper.md`'s summary table is frozen at Phase 41 (it was never
  extended past Phase 41); do not add rows there for Phases 42+. The paper's
  §8.1x prose sections DO get new letters (8.1s, 8.1t, ...), and the paper's
  older rows' status cells (e.g. row 34 "OCTET OPEN") get edited in place.

## Cross-phase numerical traps (learned the hard way)

- **Mass towers are linked**: the baryon E-ladder `m=(4+k/2·3/2)E` and the
  lepton tower `M_P/m=(V/φ²)α⁻⁹` both reproduce the proton; solving E from
  the α-tower gives 197.43 MeV vs ℏc/1fm = 197.33 (0.05% agreement). Don't
  treat them as independent.
- **CHSH maximal-violation settings** are (a,a',b,b') = (0, π/2, π/4, 3π/4)
  giving S = 2√2. The naive (0, π/4, π/8, 3π/8) gives only |S|=2.39.
- **Gap entropy must be normalized** by ln(N) (max entropy) to be
  size-independent; a pure golden orbit at Fibonacci N has normalized entropy
  near 0.99, NOT low — the ORDER signal is the DROP relative to the noise
  state, not the absolute value.
- **Use a non-noble irrational (e.g. √2−1) as the collapse/decay control**,
  not a rational like 1/3 — low-denominator rationals grid-lock on the
  spectral circle and show artificially low entropy.
- **Klein `klein_distance` returns (distance, twist_flag)**; the twist flag is
  essential for parity-inverted coupling (44.6% negative entries).
- **The `m_t` α_s reference 0.090 is scheme-specific**: exact 2-loop QCD
  running from α_s(M_Z)=0.118 gives α_s(m_t)≈0.108 (+19.6%). Check reference
  systematics (scheme/scale convention) before trusting any residual at m_t.
- **A "tested" hypothesis can be dead code**: Phase 42's "b1 golden cast" used
  `0.0*k1`, so its CSV row was bit-identical to "exact b0". When a phase
  claims a hypothesis was evaluated, assert its output differs from the base
  model (e.g. `f_b1(5) != f_exact_b0(5)`).

## Performance (GPU is a dead end here)

- **GPU is NOT viable**: the GTX 1050 is Pascal (CC 6.1) and the CUDA 13
  driver dropped Pascal kernel support; installed `cupy 14.1.1` targets CUDA
  13 and fails ("Failed to find CUDA headers"). Don't attempt GPU
  acceleration for the phase scripts.
- **Use numba `@njit(cache=True)` for hot loops** — it works on the system
  Python 3.14 (numba 0.66) and is the practical speedup. Sequential
  RGE/integration loops are not GPU-parallelizable anyway.

## README phase sections are NOT strictly numeric

The README's phase section order is not phase-number order: the "highlights"
sections for the newest closed phases (Phase 44 BAO, Phase 45 octet) sit in a
cluster between the Phase 36 and Phase 37 sections, while the strictly-ordered
36→46 numeric sequence continues below. When adding a phase section, match the
theme cluster (highlights vs numeric), not "after the last number".

## Commit convention for a finished phase

- Implementation: `feat: Phase N <title> (HNa-e, ...)` — one commit for the
  code + outputs + tests + plan.
- Phase-map sync: a separate `docs: sync phase map with Phase N (...)` commit.
- Full suite must be green (`cd code && python -m pytest ../tests/ -q`, ~170s,
  567+ tests) before the feat commit; the doc commit is a fast follow.

## Scoring a "closure" / "irreducible residual" claim

Always test the target against the credible **ranges** (`REF_RANGES`), not just
single PDG numbers. A residual is only honestly "irreducible" if it persists
with all references free inside their ranges (see Phase 46 H46c/H46d, which
survives single- AND two-parameter scans).

## Windows / shell quirks

- `git push` writes progress to stderr; in PowerShell this appears as a
  `RemoteException` but the push succeeds. Check `git log`/`git status` rather
  than the exit code.
- **Multiline `python -c "..."` fails in PowerShell** ("ScriptBlock should only
  be specified as a value of the Command parameter"). Put multi-statement
  probes in a scratch `.py` (e.g. `code/_scratchN.py`) and run that; delete it
  before committing. One-liners via `python -c` are fine.
- File encodings: source files may contain non-ASCII (φ, °) — keep new files
  UTF-8. Some old `code/*.py` files have mojibake in comments (e.g.
  `phase13_dynamical_rg.py`) — don't "fix" them casually.
