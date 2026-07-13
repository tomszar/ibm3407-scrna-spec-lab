"""Generate the committed synthetic fixture: data/synthetic/fixture.h5ad.

Deterministic (seeded) so the committed file is reproducible. Roughly 500 cells
x 300 genes of raw counts, with a realistic ``cell_type`` annotation (including
microglia and other cortical types) and a handful of ``MT-`` prefixed genes so
percent-mitochondrial QC is meaningful.

The generated file is committed to the repo — clone-and-go needs no generation
step that could fail. Re-run this only if you intend to change the fixture; then
re-run the tests and commit the new file.

Usage:
    python scripts/generate_synthetic_fixture.py
"""

from __future__ import annotations

from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd

SEED = 3407  # course number, for luck
N_CELLS = 500
N_GENES = 300
N_MT_GENES = 12

_REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = _REPO_ROOT / "data" / "synthetic" / "fixture.h5ad"

# A few real-ish cortical cell types. Microglia are the focus of the workshop's
# QC-and-marker mini-report. Weights sum to 1.
CELL_TYPES = {
    "microglia": 0.20,
    "excitatory_neuron": 0.35,
    "inhibitory_neuron": 0.20,
    "astrocyte": 0.15,
    "oligodendrocyte": 0.10,
}

# A couple of canonical microglia markers, placed as named genes so the marker
# dot-plot exercise has something specific to show.
MICROGLIA_MARKERS = ["CSF1R", "P2RY12", "CX3CR1"]


def _make_var_names(n_genes: int, n_mt: int, markers: list[str]) -> list[str]:
    """Build gene symbols: some MT- genes, the named markers, then GENExxxx."""
    names = [f"MT-ND{i + 1}" for i in range(n_mt)]
    names += list(markers)
    remaining = n_genes - len(names)
    names += [f"GENE{i:04d}" for i in range(remaining)]
    return names[:n_genes]


def generate() -> ad.AnnData:
    rng = np.random.default_rng(SEED)

    var_names = _make_var_names(N_GENES, N_MT_GENES, MICROGLIA_MARKERS)
    is_mt = np.array([name.upper().startswith("MT-") for name in var_names])
    marker_idx = [var_names.index(m) for m in MICROGLIA_MARKERS]

    # Assign a cell type to each cell.
    types = list(CELL_TYPES)
    weights = np.array(list(CELL_TYPES.values()))
    cell_type = rng.choice(types, size=N_CELLS, p=weights)

    # Per-cell "size factor" so cells differ in total counts (some low-quality).
    size_factor = rng.lognormal(mean=0.0, sigma=0.5, size=N_CELLS)

    # Baseline per-gene expression rate; MT genes get a modestly higher baseline
    # so pct_counts_mt has a realistic spread. Tuned so most healthy cells sit a
    # few percent MT (well under a typical 10% threshold) while the injected
    # low-quality cells below clearly exceed it.
    base_rate = rng.gamma(shape=2.5, scale=1.0, size=N_GENES)
    base_rate[is_mt] *= 1.1

    counts = np.zeros((N_CELLS, N_GENES), dtype=np.int32)
    for i in range(N_CELLS):
        lam = base_rate * size_factor[i]
        counts[i] = rng.poisson(lam)

    # Make microglia markers specific to microglia so the dot plot is meaningful.
    micro_mask = cell_type == "microglia"
    for gi in marker_idx:
        counts[micro_mask, gi] += rng.poisson(15.0, size=micro_mask.sum())
        counts[~micro_mask, gi] = rng.poisson(0.3, size=(~micro_mask).sum())

    # Inject a batch of clearly low-quality cells (few genes / high MT) so QC
    # filtering visibly removes something.
    n_bad = 40
    bad_idx = rng.choice(N_CELLS, size=n_bad, replace=False)
    for i in bad_idx:
        keep = rng.choice(N_GENES, size=rng.integers(5, 30), replace=False)
        row = np.zeros(N_GENES, dtype=np.int32)
        row[keep] = rng.poisson(2.0, size=keep.size)
        row[is_mt] += rng.poisson(8.0, size=is_mt.sum())  # high MT fraction
        counts[i] = row

    obs = pd.DataFrame(
        {"cell_type": pd.Categorical(cell_type)},
        index=[f"cell_{i:04d}" for i in range(N_CELLS)],
    )
    var = pd.DataFrame(
        {"mt": is_mt},
        index=pd.Index(var_names, name="gene_symbol"),
    )

    adata = ad.AnnData(X=counts, obs=obs, var=var)
    adata.uns["synthetic"] = True
    adata.uns["seed"] = SEED
    return adata


def main() -> None:
    adata = generate()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    adata.write_h5ad(OUT_PATH)
    print(
        f"Wrote {OUT_PATH.relative_to(_REPO_ROOT)}  "
        f"({adata.n_obs} cells x {adata.n_vars} genes, "
        f"{int(adata.var['mt'].sum())} MT genes)"
    )


if __name__ == "__main__":
    main()
