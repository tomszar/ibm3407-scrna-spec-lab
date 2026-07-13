"""Quality-control metrics and cell filtering.

Both functions are STUBS on ``main``. Students implement them by writing a
precise spec (with OpenSpec) and letting the local model apply it. The
acceptance test lives in ``tests/test_qc.py``.

The docstrings below are the contract: they state intent, parameters, and
returns clearly enough to write a spec against. Do not weaken them.
"""

from __future__ import annotations

import anndata as ad
import numpy as np
import scipy.sparse as sp


def _as_dense_counts(adata: ad.AnnData) -> np.ndarray:
    """Return ``adata.X`` as a dense float array (the fixture is small)."""
    x = adata.X
    return x.toarray() if sp.issparse(x) else np.asarray(x)


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
    counts = _as_dense_counts(adata)

    n_genes = (counts > 0).sum(axis=1)
    total_counts = counts.sum(axis=1)

    is_mt = np.array(
        [name.upper().startswith("MT-") for name in adata.var_names]
    )
    mt_counts = (
        counts[:, is_mt].sum(axis=1) if is_mt.any() else np.zeros_like(total_counts)
    )

    with np.errstate(divide="ignore", invalid="ignore"):
        pct_counts_mt = np.where(
            total_counts > 0, 100.0 * mt_counts / total_counts, 0.0
        )

    adata.obs["n_genes"] = np.asarray(n_genes).ravel().astype(int)
    adata.obs["total_counts"] = np.asarray(total_counts).ravel().astype(float)
    adata.obs["pct_counts_mt"] = np.asarray(pct_counts_mt).ravel().astype(float)
    return adata


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
    if "n_genes" not in adata.obs or "pct_counts_mt" not in adata.obs:
        adata = compute_qc_metrics(adata.copy())

    keep = (adata.obs["n_genes"] >= min_genes) & (
        adata.obs["pct_counts_mt"] <= max_pct_mt
    )
    return adata[keep.to_numpy()].copy()
