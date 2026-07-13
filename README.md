# ibm3407-scrna-spec-lab

> **New here? Start with [SETUP.md](SETUP.md)** — install the tools, clone, and
> verify your environment before the first session.

A small, deliberately over-scaffolded single-cell RNA-seq (scRNA-seq) repo for
the **IBM3407** graduate workshop on **spec-driven development**. You'll drive a
**local LLM** (via Ollama + [opencode](https://opencode.ai) +
[OpenSpec](https://github.com/Fission-AI/OpenSpec)) to make small, bounded
changes to this analysis — everything runs **offline on your own laptop**.

## The deliverable

A small, reproducible **microglia QC-and-marker mini-report**: load a
single-cell dataset, compute per-cell quality-control (QC) metrics, filter out
low-quality cells with **documented, justified thresholds**, and (optionally)
show that microglia markers behave as expected on a dot plot.

The analysis is intentionally tiny. The skill being practiced is writing a
**precise specification** that a weak local model can implement correctly — not
building a full pipeline.

## Repo layout

```
scrna/                 the analysis package
  io.py                load_data() — implemented, don't change
  qc.py                compute_qc_metrics(), filter_cells() — STUBS you implement
  plots.py             marker_dotplot() — STUB (alternative change)
  pipeline.py          load -> metrics -> filter -> (plot) orchestration
scripts/
  generate_synthetic_fixture.py   builds the committed synthetic dataset
  make_subset.py                  downloads a real SEA-AD subset (optional)
  verify.py                       cross-platform `make verify`
data/
  synthetic/fixture.h5ad          committed tiny dataset — offline default
  README.md                       how to get the real subset
tests/
  test_smoke.py        environment check — passes on main
  test_qc.py           acceptance for the QC change — xfails on main
```

On a fresh clone (`main`), the QC/plot functions are **stubs that raise
`NotImplementedError`**. Your job is to make them real by specifying the change
first.

## Verify your setup

One command, after following [SETUP.md](SETUP.md):

```bash
make verify           # or:  python scripts/verify.py   (Windows without make)
```

It runs the smoke test and prints:

```
Environment OK — the agent can read the repo and run the tests.
```

Run the tests directly with `pytest`:

- On `main`: the smoke tests **pass**; the QC acceptance test **xfails** (the
  stub isn't implemented yet). This is the expected starting state.
- Once you implement the QC change, `tests/test_qc.py` **passes**.

## The OpenSpec cycle

Spec-driven development runs a short loop, and the workshop maps onto it:

1. **Propose** — describe the bounded change as a spec (`/opsx:propose`). For us:
   a QC filtering step with documented thresholds and a testable acceptance
   criterion.
2. **Audit & revise** — read the draft. Are the requirements testable? Are the
   thresholds justified? Tighten the spec by hand.
3. **Apply** — let the local model implement against the spec (`/opsx:apply`).
4. **Verify** — `make verify` and `pytest`; close any gaps the local model left.
5. **Archive** — fold the finished change back in (`/opsx:archive`) and move on
   to the next spec.

Step-by-step student instructions for the two sessions are in
[WORKSHOP.md](WORKSHOP.md).

## Branches

- **`main`** — the starting point. Stubs unimplemented; smoke passes, QC xfails.
- **`solution`** — the QC change fully implemented, `test_qc.py` passes. Check it
  out only if your local model stalls mid-week and you need to keep moving for
  peer review.

## Stuck?

If your environment check fails, re-read [SETUP.md](SETUP.md). If a stub is the
problem, that's the point — write a sharper spec.
