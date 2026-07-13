"""Acceptance test for the QC change.

- On `main` the QC stubs raise ``NotImplementedError``, so this test **xfails**.
- On `solution` (and after a student implements the stubs) it **passes**.

The xfail is applied dynamically: if the stubs are implemented, the test runs
for real and must pass; if not, it is an expected failure. So the same file
gives the right result on both branches with no edits.
"""

from __future__ import annotations

import pytest

from scrna import io, qc

MIN_GENES = 200
MAX_PCT_MT = 10.0


def _qc_implemented() -> bool:
    """True if the QC stubs have been implemented (don't raise NotImplementedError)."""
    try:
        adata = io.load_data()
        qc.compute_qc_metrics(adata)
    except NotImplementedError:
        return False
    except Exception:
        # Any other error means it's implemented but broken — let the test run
        # and report the real failure rather than masking it as xfail.
        return True
    return True


# Not xfail when implemented -> genuine PASS on `solution`. Xfail when the stub
# is unimplemented -> expected failure on `main`.
requires_qc = pytest.mark.xfail(
    not _qc_implemented(),
    reason="QC stubs not implemented on main (NotImplementedError)",
    raises=NotImplementedError,
    strict=True,
)


@requires_qc
def test_compute_qc_metrics_adds_expected_columns():
    adata = io.load_data()
    out = qc.compute_qc_metrics(adata)

    for col in ("n_genes", "total_counts", "pct_counts_mt"):
        assert col in out.obs.columns

    # Shape is unchanged by computing metrics.
    assert out.n_obs == adata.n_obs
    assert out.n_vars == adata.n_vars

    # Percentages are in a sane range.
    assert (out.obs["pct_counts_mt"] >= 0).all()
    assert (out.obs["pct_counts_mt"] <= 100).all()


@requires_qc
def test_filter_cells_removes_cells_by_threshold():
    adata = io.load_data()
    n_before = adata.n_obs

    filtered = qc.filter_cells(adata, min_genes=MIN_GENES, max_pct_mt=MAX_PCT_MT)

    # Cells may be removed but never added.
    assert filtered.n_obs < n_before, "some low-quality cells should be removed"
    assert filtered.n_obs > 0, "not everything should be filtered out"

    # Genes are unchanged.
    assert filtered.n_vars == adata.n_vars

    # QC metrics are present on the result...
    for col in ("n_genes", "pct_counts_mt"):
        assert col in filtered.obs.columns

    # ...and every surviving cell actually satisfies both thresholds.
    assert (filtered.obs["n_genes"] >= MIN_GENES).all()
    assert (filtered.obs["pct_counts_mt"] <= MAX_PCT_MT).all()


@requires_qc
def test_filter_cells_does_not_mutate_input():
    adata = io.load_data()
    n_before = adata.n_obs
    _ = qc.filter_cells(adata, min_genes=MIN_GENES, max_pct_mt=MAX_PCT_MT)
    # The original object still has all its cells.
    assert adata.n_obs == n_before
