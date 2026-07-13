"""Smoke test — the setup verification target. MUST pass on `main`.

Confirms the environment is sane: the package imports, the synthetic fixture
loads, and it has the expected shape and annotation. This is what `make verify`
and `scripts/verify.py` run.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp

import scrna
from scrna import io


def test_package_imports():
    assert hasattr(scrna, "io")
    assert hasattr(scrna, "qc")
    assert hasattr(scrna, "plots")
    assert hasattr(scrna, "pipeline")


def test_fixture_loads_with_expected_shape():
    adata = io.load_data()
    # The synthetic fixture is ~500 cells x 300 genes.
    assert adata.n_obs == 500
    assert adata.n_vars == 300


def test_fixture_has_expected_obs_columns():
    adata = io.load_data()
    assert "cell_type" in adata.obs.columns
    # Microglia are the focus of the workshop's mini-report.
    assert "microglia" in set(adata.obs["cell_type"].astype(str))


def test_fixture_has_mitochondrial_genes():
    adata = io.load_data()
    mt_genes = [g for g in adata.var_names if g.upper().startswith("MT-")]
    assert len(mt_genes) > 0, "fixture should contain MT- genes for QC"


def test_fixture_counts_are_nonnegative_integers():
    adata = io.load_data()
    x = adata.X
    values = x.data if sp.issparse(x) else np.asarray(x)
    assert (values >= 0).all()
