# Makefile for the IBM3407 scRNA spec lab.
# Windows users without `make` can use the python equivalents noted below.

PYTHON ?= python

.PHONY: help verify test data fixture clean

help:
	@echo "Targets:"
	@echo "  make verify   Run the smoke test and print an OK line (python scripts/verify.py)"
	@echo "  make test     Run the full test suite (pytest)"
	@echo "  make fixture  Regenerate the synthetic fixture (committed)"
	@echo "  make data     Download + downsample the real SEA-AD subset (optional, needs cellxgene-census)"
	@echo "  make clean    Remove caches and the gitignored real-data subset"

# The single command students run after setup. Mirrors scripts/verify.py.
verify:
	$(PYTHON) scripts/verify.py

test:
	$(PYTHON) -m pytest

fixture:
	$(PYTHON) scripts/generate_synthetic_fixture.py

# Optional: real data. Requires `pip install cellxgene-census` and network.
data:
	$(PYTHON) scripts/make_subset.py

clean:
	rm -rf .pytest_cache **/__pycache__ scrna/__pycache__ tests/__pycache__ scripts/__pycache__
	rm -f data/sea_ad_subset.h5ad
