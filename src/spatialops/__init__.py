"""
SpatialEval: A Comprehensive Benchmark for 2D Spatial Reasoning in LLMs.

This package provides tools for loading, evaluating, and analyzing the
SpatialEval benchmark dataset.
"""

__version__ = "1.0.0"
__author__ = "SpatialEval Team"

from spatialops.data import load_dataset, load_category
from spatialops.harness import Evaluator

__all__ = [
    "__version__",
    "load_dataset",
    "load_category",
    "Evaluator",
]
