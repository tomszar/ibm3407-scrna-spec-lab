"""Data loading. This module is implemented — students do not change it."""

from __future__ import annotations

from pathlib import Path

import anndata as ad

# Path to the committed synthetic fixture, resolved relative to this file so it
# works no matter what the current working directory is.
_REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FIXTURE = _REPO_ROOT / "data" / "synthetic" / "fixture.h5ad"


def load_data(path: str | Path | None = None) -> ad.AnnData:
    """Load a single-cell dataset from an ``.h5ad`` file.

    Parameters
    ----------
    path
        Path to an ``.h5ad`` file. If ``None`` (the default), the committed
        synthetic fixture at ``data/synthetic/fixture.h5ad`` is loaded, so the
        analysis runs offline with no setup.

    Returns
    -------
    anndata.AnnData
        The loaded dataset. ``adata.X`` holds raw counts; ``adata.obs`` carries
        cell-level annotation (including a ``cell_type`` column); ``adata.var``
        carries gene metadata (gene symbols in the index).

    Raises
    ------
    FileNotFoundError
        If the resolved path does not exist.
    """
    resolved = Path(path) if path is not None else DEFAULT_FIXTURE
    if not resolved.exists():
        raise FileNotFoundError(
            f"No .h5ad file at {resolved}. "
            "Generate the fixture with "
            "`python scripts/generate_synthetic_fixture.py`, or pass a path to "
            "an existing file."
        )
    return ad.read_h5ad(resolved)
