# CLAUDE.md

Guidance for Claude Code (and any AI agent) working in this repository.

## What this repo is

A **deliberately over-scaffolded dummy repo** for a graduate spec-driven
development workshop (course IBM3407, human genomics). Students drive a **local
LLM via Ollama** (through opencode + OpenSpec) to make small, bounded changes to
a tiny single-cell RNA-seq (scRNA-seq) analysis. Everything runs **offline on
student laptops** across macOS / Windows / Linux.

The analysis is intentionally minimal: two QC functions and one plot. The point
is *bounded, spec-driven changes* — not a complete pipeline. **Do not expand the
analysis** beyond the existing stubs.

## The two-branch model (important)

- **`main`** — the starting point students clone. QC/plot functions are stubs
  that raise `NotImplementedError`. The smoke test **passes**; the QC acceptance
  test **xfails**. This is the intended state of `main`. Do not "fix" the stubs
  on `main`.
- **`solution`** — the QC change fully implemented. `tests/test_qc.py` passes
  here. Reference branch students check out if their local model stalls.

When asked to change behavior, be explicit about which branch you're on. A green
QC test on `main` is a bug; an xfail on `main` is correct.

## Repo layout

```
scrna/            io.py (implemented) · qc.py + plots.py (stubs) · pipeline.py
scripts/          generate_synthetic_fixture.py · make_subset.py · verify.py
data/synthetic/   fixture.h5ad  (committed, tiny, ~500 cells x 300 genes)
tests/            test_smoke.py (passes on main) · test_qc.py (xfails on main)
README / SETUP / WORKSHOP.md
```

## Running things on this machine (NixOS gotcha)

This is a Nix system. There is **no system `pip`**; use a venv created from
`ensurepip`. numpy's C-extensions need `libstdc++.so.6` on the library path,
which the venv Python does not see by default. If imports fail with
`libstdc++.so.6: cannot open shared object file`, prefix commands with:

```bash
export LD_LIBRARY_PATH=$(dirname $(find /nix/store -name 'libstdc++.so.6' -path '*gcc*lib/lib/*' | head -1)):$LD_LIBRARY_PATH
```

Setup used to build this repo:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

This LD_LIBRARY_PATH workaround is **NixOS-specific** and must NOT leak into any
committed doc — students on macOS/Windows/standard Linux don't need it. SETUP.md
stays clean.

## Verification (the one command that must work)

```bash
make verify          # or: python scripts/verify.py   (Windows without make)
```

Prints `Environment OK — the agent can read the repo and run the tests.` on a
clean `main`. Expected test states:

- `main`:     `pytest` → smoke **passes**, QC test **xfails**.
- `solution`: `pytest` → **all pass**.

Always re-run `pytest` on both branches after touching `scrna/`, tests, or the
fixture, and confirm those exact states.

## Constraints (do / don't)

- **Never commit real SEA-AD data or any large `.h5ad`.** Only
  `data/synthetic/fixture.h5ad` is committed; everything else `.h5ad` is
  gitignored. `scripts/make_subset.py` writes the gitignored real subset.
- **Do not run `openspec init` on `main`.** Students do that themselves as part
  of learning the tool. No `openspec/` dir should be committed.
- Keep `cellxgene-census` out of `requirements.txt` (comment only). It's heavy;
  the student install must stay light.
- Keep `SETUP.md` / `WORKSHOP.md` install commands verified against each tool's
  official docs — Ollama, opencode, and OpenSpec install steps move over time.
- The synthetic fixture is deterministic (seeded). If you regenerate it, re-run
  the tests and commit the new file.
