"""Orchestration: load -> compute QC metrics -> filter -> (optional plot).

On ``main`` this fails at the first stub (``compute_qc_metrics``), which is
expected. Once the QC stubs are implemented it runs end to end.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import anndata as ad

from . import io, qc

# Default QC thresholds. These are placeholders — part of the workshop is
# justifying and documenting the thresholds a change should use, in a spec.
DEFAULT_MIN_GENES = 200
DEFAULT_MAX_PCT_MT = 10.0


@dataclass
class PipelineResult:
    """Outcome of a pipeline run."""

    adata: ad.AnnData
    n_cells_before: int
    n_cells_after: int
    thresholds: dict = field(default_factory=dict)


def run(
    adata: ad.AnnData | None = None,
    *,
    min_genes: int = DEFAULT_MIN_GENES,
    max_pct_mt: float = DEFAULT_MAX_PCT_MT,
) -> PipelineResult:
    """Run the mini QC pipeline.

    Parameters
    ----------
    adata
        Dataset to process. If ``None``, the synthetic fixture is loaded via
        :func:`scrna.io.load_data`.
    min_genes, max_pct_mt
        Thresholds passed to :func:`scrna.qc.filter_cells`.

    Returns
    -------
    PipelineResult
        The filtered dataset plus before/after cell counts and the thresholds
        used.
    """
    if adata is None:
        adata = io.load_data()

    n_before = adata.n_obs

    adata = qc.compute_qc_metrics(adata)
    filtered = qc.filter_cells(adata, min_genes=min_genes, max_pct_mt=max_pct_mt)

    return PipelineResult(
        adata=filtered,
        n_cells_before=n_before,
        n_cells_after=filtered.n_obs,
        thresholds={"min_genes": min_genes, "max_pct_mt": max_pct_mt},
    )


if __name__ == "__main__":
    result = run()
    print(
        f"Filtered {result.n_cells_before} -> {result.n_cells_after} cells "
        f"with thresholds {result.thresholds}"
    )
