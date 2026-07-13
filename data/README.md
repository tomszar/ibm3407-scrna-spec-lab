# Data

## What's committed

- **`synthetic/fixture.h5ad`** — a tiny, deterministic synthetic dataset
  (~500 cells × 300 genes) with raw counts, a `cell_type` annotation (including
  microglia), and a handful of `MT-` genes. This is what the analysis and the
  tests use by default, so **everything runs offline with no download**.

  Regenerate it with:

  ```bash
  python scripts/generate_synthetic_fixture.py
  ```

## Real data (optional, never committed)

The real Seattle Alzheimer's Disease Brain Cell Atlas (**SEA-AD**) snRNA-seq data
is large and is **never committed to this repo**. If you want to run the analysis
against real data, download and downsample a subset yourself:

```bash
pip install cellxgene-census        # heavy; not in requirements.txt
python scripts/make_subset.py --list        # see available SEA-AD datasets
python scripts/make_subset.py --n-cells 3000
```

This writes `data/sea_ad_subset.h5ad`, which is **gitignored**. Point the
analysis at it with `scrna.io.load_data("data/sea_ad_subset.h5ad")`.

> SEA-AD is distributed through CZ CELLxGENE Discover. `scripts/make_subset.py`
> uses the `cellxgene-census` API. See the note at the top of that script — it
> was not run end to end during scaffolding, so verify interactively.
