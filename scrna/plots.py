"""Plotting. Contains one STUB — the secondary change students may pick.

Implementing ``marker_dotplot`` is an alternative to the QC change, not required
in addition to it.
"""

from __future__ import annotations

from collections.abc import Sequence

import anndata as ad
from matplotlib.figure import Figure


def marker_dotplot(
    adata: ad.AnnData,
    groupby: str,
    markers: Sequence[str],
) -> Figure:
    """Draw a marker-gene dot plot grouped by a categorical annotation.

    A dot plot summarises, for each group and each marker gene, two things: the
    fraction of cells in the group expressing the gene (dot size) and the mean
    expression among expressing cells (dot color). It is the standard way to
    sanity-check that marker genes (e.g. microglia markers such as ``CSF1R``,
    ``P2RY12``) are specific to their expected cell type.

    Parameters
    ----------
    adata
        Dataset to plot.
    groupby
        Name of a categorical column in ``adata.obs`` to group cells by
        (e.g. ``"cell_type"``).
    markers
        Marker gene symbols to show, each present in ``adata.var_names``.

    Returns
    -------
    matplotlib.figure.Figure
        The figure containing the dot plot, so the caller can save or display it.
    """
    raise NotImplementedError(
        "Implement marker_dotplot: return a matplotlib Figure with a dot plot "
        "of `markers` grouped by `groupby` (scanpy.pl.dotplot can help)."
    )
