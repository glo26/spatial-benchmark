"""
Model wrappers for the SpatialEval benchmark.

This module provides wrapper classes for different LLM APIs to standardize
the interface for the evaluation harness.
"""

from spatialeval.models.base import BaseModel
from spatialeval.models.openai_model import OpenAIModel
from spatialeval.models.anthropic_model import AnthropicModel

__all__ = [
    "BaseModel",
    "OpenAIModel",
    "AnthropicModel",
]
