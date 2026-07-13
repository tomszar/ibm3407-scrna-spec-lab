"""scrna — a tiny single-cell RNA-seq analysis for the IBM3407 spec-driven lab.

The package is deliberately small: load data (implemented), compute QC metrics
and filter cells (student stubs in ``qc.py``), and a marker dot plot (stub in
``plots.py``). ``pipeline.run`` wires them together.
"""

from importlib.metadata import PackageNotFoundError, version

from . import io, pipeline, plots, qc

try:
    __version__ = version("scrna")
except PackageNotFoundError:  # not installed as a package; running from source
    __version__ = "0.1.0.dev0"

__all__ = ["io", "qc", "plots", "pipeline", "__version__"]
