# Workshop steps

Student-facing steps for the two Friday sessions. Do [SETUP.md](SETUP.md) first;
run `make verify` and get the OK line before Friday 1.

Throughout, you drive the change through opencode with your local model, using
OpenSpec's commands. The goal each time: **a spec precise enough that the local
model implements it correctly**, verified by the tests.

---

## Friday 1 — propose, audit, apply

1. **Sync.** `git pull` for the latest.
2. **Init OpenSpec** if you haven't: `openspec init`.
3. **Pick a change** from the menu below (unsure? take the default).

#### Menu: pick a change

Choose one, or **propose your own** — this list is a floor, not a ceiling. It's
here so nobody is blocked at the start. Items get harder going down: unsure? take
the **default**; comfortable with Python? pick further down. Each is **one
function with one checkable acceptance criterion** — keep your change that small,
or the local model won't finish it in the session.

1. **QC metrics and filtering** — *default.* Compute genes-per-cell and percent
   mitochondrial counts, then filter cells on stated thresholds. Stubs exist in
   `scrna/qc.py`. *Acceptance:* `tests/test_qc.py` passes.
2. **Filter by cell population** — subset to microglia, or drop populations below
   a minimum cell count. *Acceptance:* the returned object contains only the
   intended `cell_type` groups, and no cells were added.
3. **Marker dotplot** — plot marker genes for a cell type across the fixture's
   `cell_type` groups. Stub exists in `scrna/plots.py`. *Acceptance:* the
   function returns a `matplotlib` Figure with one row per marker and one column
   per group.
4. **Gene-level filtering** — drop genes detected in fewer than *N* cells. *(No
   stub — write the function from scratch.)* *Acceptance:* every gene in the
   result is detected in at least *N* cells, and no cells were removed.
5. **QC summary table** — write cell counts before and after filtering, plus
   per-population counts, to disk. *(No stub.)* *Acceptance:* a table file is
   written whose numbers match the fixture.
6. **Normalization and log-transform** — as an explicit, parameterized step.
   *(No stub.)* *Acceptance:* after the step, each cell's total normalized counts
   equals the chosen target sum (before the log), within tolerance.

> Items 4–6 have no stubs on purpose: creating the function from nothing is a
> stronger test of your spec than filling in a blank.

Once you've picked, run the cycle:

4. **Propose your change.** In opencode, e.g. for the default:
   ```
   /opsx:propose add a QC filtering step to scrna/qc.py that computes per-cell
   metrics and filters cells by minimum genes and maximum percent mitochondrial
   counts, with documented thresholds
   ```
5. **Audit the draft** — this is the real work. Ask of the generated spec:
   - Are the requirements **testable**? Could someone write a test from them?
   - Are the **thresholds justified** (why 200 genes? why 10% MT?), or arbitrary?
   - What is the **acceptance criterion** — how do you *know* it's done?
   - Look at the acceptance for your change (e.g. `tests/test_qc.py` for the
     default) to see what it must satisfy.
6. **Revise the spec by hand.** Tighten anything vague. Pin the thresholds and
   say why.
7. **Apply.** Start `/opsx:apply` and let the local model implement against your
   spec.

## Between sessions

- Let **apply** finish.
- Verify: `make verify` and `pytest`. The QC acceptance test in
  `tests/test_qc.py` should now **pass** (it xfails on a fresh `main`).
- **Close the gaps** the local model left — small fixes are expected with a weak
  model. If it's badly stuck, you can check out the `solution` branch to keep
  moving, but try to finish your own first.
- **Archive** the finished change: `/opsx:archive`.
- **Draft a second spec** from a real methods paragraph (bring one from a paper
  you're reading) — e.g. a marker dot plot via `scrna.plots.marker_dotplot`, or a
  different QC rule.

## Friday 2 — peer review, revise, apply

1. **Swap specs** with a partner.
2. **Peer-review** each other's spec for **ambiguity and testability**: where
   could the model go wrong? What's underspecified? Is the acceptance criterion
   real?
3. **Revise** based on the review.
4. **Apply and verify** the revised change: `/opsx:apply`, then `make verify` and
   `pytest`.
5. **Short discussion:** what made a spec succeed or fail with a weak local
   model?

---

### The loop, in one line

**propose → audit → revise → apply → verify → archive.** The spec is the
artifact you're being graded on — the code is what a weak model produces from it.
