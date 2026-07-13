"""Download and downsample a real SEA-AD snRNA-seq subset for optional use.

SEA-AD (Seattle Alzheimer's Disease Brain Cell Atlas) is available through CZ
CELLxGENE Discover. This script pulls a SEA-AD dataset via the
``cellxgene-census`` API, downsamples it to a few thousand cells, and writes
``data/sea_ad_subset.h5ad`` (which is **gitignored** — real data is never
committed).

This is entirely optional. The workshop runs on the committed synthetic fixture;
students only need this if they want to point the analysis at real data.

Requirements (NOT in the core requirements.txt — heavy dependency stack):

    pip install cellxgene-census

Usage:

    python scripts/make_subset.py --n-cells 3000
    python scripts/make_subset.py --list          # just list SEA-AD datasets

-------------------------------------------------------------------------------
NOTE: This script was NOT executed end to end during scaffolding — the full
download is large and requires network access to the CELLxGENE Census. Its
structure and the census API calls were validated against the current
cellxgene-census docs, but verify interactively before relying on it. Pin
CENSUS_VERSION to a released version for reproducibility; "stable" is used by
default here for convenience.
-------------------------------------------------------------------------------
"""

from __future__ import annotations

import argparse
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = _REPO_ROOT / "data" / "sea_ad_subset.h5ad"

# Pin to a released census version (e.g. "2025-01-30") for full reproducibility.
CENSUS_VERSION = "stable"
ORGANISM = "Homo sapiens"
SEED = 3407


def _find_sea_ad_datasets(census):
    """Return the census datasets table rows whose collection is SEA-AD."""
    datasets = census["census_info"]["datasets"].read().concat().to_pandas()
    mask = datasets["collection_name"].str.contains("SEA-AD", case=False, na=False)
    return datasets.loc[mask].sort_values("dataset_total_cell_count")


def list_datasets() -> None:
    import cellxgene_census

    with cellxgene_census.open_soma(census_version=CENSUS_VERSION) as census:
        sea_ad = _find_sea_ad_datasets(census)
        if sea_ad.empty:
            print("No SEA-AD datasets found in this census version.")
            return
        cols = ["dataset_id", "dataset_title", "dataset_total_cell_count"]
        print(sea_ad[cols].to_string(index=False))


def make_subset(n_cells: int) -> None:
    import cellxgene_census
    import numpy as np

    with cellxgene_census.open_soma(census_version=CENSUS_VERSION) as census:
        sea_ad = _find_sea_ad_datasets(census)
        if sea_ad.empty:
            raise SystemExit(
                "No SEA-AD datasets found. Run with --list against a different "
                "CENSUS_VERSION, or check the collection name."
            )

        # Pick the smallest SEA-AD dataset to keep the download modest.
        dataset_id = sea_ad.iloc[0]["dataset_id"]
        title = sea_ad.iloc[0]["dataset_title"]
        print(f"Using smallest SEA-AD dataset: {title} ({dataset_id})")

        adata = cellxgene_census.get_anndata(
            census=census,
            organism=ORGANISM,
            obs_value_filter=f"dataset_id == '{dataset_id}'",
            column_names={
                "obs": [
                    "cell_type",
                    "tissue",
                    "disease",
                    "sex",
                    "assay",
                    "dataset_id",
                ]
            },
        )

    print(f"Downloaded {adata.n_obs} cells x {adata.n_vars} genes.")

    # Downsample cells deterministically.
    if adata.n_obs > n_cells:
        rng = np.random.default_rng(SEED)
        idx = rng.choice(adata.n_obs, size=n_cells, replace=False)
        idx.sort()
        adata = adata[idx].copy()

    # Name genes by symbol so they line up with the synthetic fixture's var_names
    # (MT- prefixes, marker symbols). The census stores symbols in feature_name.
    if "feature_name" in adata.var.columns:
        adata.var_names = adata.var["feature_name"].astype(str)
        adata.var_names_make_unique()

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    adata.write_h5ad(OUT_PATH)
    print(
        f"Wrote {OUT_PATH.relative_to(_REPO_ROOT)} "
        f"({adata.n_obs} cells x {adata.n_vars} genes). "
        "This file is gitignored and must not be committed."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--n-cells",
        type=int,
        default=3000,
        help="Number of cells to keep after downsampling (default: 3000).",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available SEA-AD datasets and exit (no download).",
    )
    args = parser.parse_args()

    if args.list:
        list_datasets()
    else:
        make_subset(args.n_cells)


if __name__ == "__main__":
    main()
