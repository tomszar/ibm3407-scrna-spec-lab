"""Quality-control metrics and cell filtering.

Both functions are STUBS on ``main``. Students implement them by writing a
precise spec (with OpenSpec) and letting the local model apply it. The
acceptance test lives in ``tests/test_qc.py``.

The docstrings below are the contract: they state intent, parameters, and
returns clearly enough to write a spec against. Do not weaken them.
"""

from __future__ import annotations

import anndata as ad


def compute_qc_metrics(adata: ad.AnnData) -> ad.AnnData:
    """Add per-cell quality-control metrics to ``adata.obs``.

    Computes, for every cell, from the raw counts in ``adata.X``:

    - ``n_genes`` — number of genes with a non-zero count in that cell.
    - ``total_counts`` — total counts summed across all genes in that cell.
    - ``pct_counts_mt`` — percentage of a cell's total counts that come from
      mitochondrial genes, i.e. ``100 * mt_counts / total_counts``. Mitochondrial
      genes are identified by the gene symbol prefix ``MT-`` (case-insensitive)
      in ``adata.var_names``. A cell with zero total counts has
      ``pct_counts_mt == 0``.

    Parameters
    ----------
    adata
        Dataset with raw counts in ``adata.X`` and gene symbols in
        ``adata.var_names``.

    Returns
    -------
    anndata.AnnData
        The same object with ``n_genes``, ``total_counts``, and
        ``pct_counts_mt`` columns added to ``obs``. The number of cells and
        genes is unchanged.
    """
    raise NotImplementedError(
        "Implement compute_qc_metrics: add n_genes, total_counts, and "
        "pct_counts_mt (MT- prefixed genes) to adata.obs."
    )


def filter_cells(
    adata: ad.AnnData,
    min_genes: int,
    max_pct_mt: float,
) -> ad.AnnData:
    """Return a filtered copy keeping only cells that pass QC thresholds.

    A cell is kept when **both** hold:

    - ``n_genes >= min_genes`` (enough genes detected), and
    - ``pct_counts_mt <= max_pct_mt`` (not too much mitochondrial signal).

    If the QC metrics are not already present in ``adata.obs``, compute them
    first with :func:`compute_qc_metrics`.

    Parameters
    ----------
    adata
        Dataset to filter. Not modified in place.
    min_genes
        Minimum number of detected genes a cell must have to be kept.
    max_pct_mt
        Maximum percent mitochondrial counts a cell may have to be kept.

    Returns
    -------
    anndata.AnnData
        A new object containing only the cells that pass both thresholds. Cells
        may be removed but never added; genes are unchanged. The returned object
        carries the QC metric columns in ``obs``.
    """
    raise NotImplementedError(
        "Implement filter_cells: return a copy keeping cells with "
        "n_genes >= min_genes and pct_counts_mt <= max_pct_mt."
    )
