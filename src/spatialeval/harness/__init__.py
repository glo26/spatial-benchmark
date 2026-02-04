"""
Evaluation harness for the SpatialEval benchmark.

This module provides the core evaluation logic for running LLMs against
the benchmark tasks and computing scores.
"""

from spatialeval.harness.evaluator import Evaluator
from spatialeval.harness.metrics import (
    compute_accuracy,
    compute_reasoning_score,
    compute_efficiency_score,
    compute_spatialeval_score,
)

__all__ = [
    "Evaluator",
    "compute_accuracy",
    "compute_reasoning_score",
    "compute_efficiency_score",
    "compute_spatialeval_score",
]
