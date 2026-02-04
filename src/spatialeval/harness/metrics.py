"""
Scoring metrics for the SpatialEval benchmark.

This module contains functions for computing the three core metrics:
Accuracy, Reasoning Quality, and Efficiency.
"""

import re
from typing import Any, Union


def compute_accuracy(response: str, ground_truth: Any) -> float:
    """
    Compute the accuracy score for a single response.

    This function performs a flexible match between the model's response and
    the ground truth. It handles numeric answers, string answers, and lists.

    Args:
        response: The model's response string.
        ground_truth: The correct answer.

    Returns:
        A score between 0.0 and 1.0.
    """
    # Normalize the response
    response_lower = response.lower().strip()

    # Handle numeric ground truths
    if isinstance(ground_truth, (int, float)):
        # Try to extract a number from the response
        numbers = re.findall(r"-?\d+\.?\d*", response)
        if numbers:
            # Check the last number mentioned (often the final answer)
            for num_str in reversed(numbers):
                try:
                    extracted_num = float(num_str)
                    # Allow for small floating point tolerance
                    if abs(extracted_num - ground_truth) < 1e-6:
                        return 1.0
                    # Partial credit for being close
                    if ground_truth != 0:
                        relative_error = abs(extracted_num - ground_truth) / abs(ground_truth)
                        if relative_error < 0.01:  # Within 1%
                            return 0.9
                        if relative_error < 0.05:  # Within 5%
                            return 0.7
                except ValueError:
                    continue
        return 0.0

    # Handle string ground truths
    if isinstance(ground_truth, str):
        gt_lower = ground_truth.lower().strip()
        if gt_lower in response_lower:
            return 1.0
        # Check for exact match at the end (common answer format)
        if response_lower.endswith(gt_lower):
            return 1.0
        return 0.0

    # Handle list ground truths (multiple acceptable answers)
    if isinstance(ground_truth, list):
        for gt in ground_truth:
            if compute_accuracy(response, gt) > 0.5:
                return 1.0
        return 0.0

    return 0.0


def compute_reasoning_score(response: str) -> float:
    """
    Compute the reasoning quality score for a response.

    This is a heuristic-based score that evaluates the quality of the
    reasoning chain in the response. In a full implementation, this
    would use an LLM-as-a-Judge approach.

    Args:
        response: The model's response string.

    Returns:
        A score between 0.0 and 1.0.
    """
    score = 0.5  # Base score

    # Reward for showing work / step-by-step reasoning
    reasoning_indicators = [
        "first", "second", "then", "next", "therefore", "thus",
        "because", "since", "step", "calculate", "compute",
        "the formula", "using", "applying", "we get", "we have",
    ]
    response_lower = response.lower()
    indicator_count = sum(1 for ind in reasoning_indicators if ind in response_lower)
    score += min(indicator_count * 0.05, 0.3)

    # Reward for mathematical notation
    if re.search(r"\d+\s*[\+\-\*\/\=]\s*\d+", response):
        score += 0.1

    # Reward for structured output
    if re.search(r"(answer|result|solution)[\s:]+", response_lower):
        score += 0.1

    return min(score, 1.0)


def compute_efficiency_score(response: str) -> float:
    """
    Compute the efficiency score for a response.

    This metric rewards concise, well-structured responses and penalizes
    overly verbose or repetitive answers.

    Args:
        response: The model's response string.

    Returns:
        A score between 0.0 and 1.0.
    """
    word_count = len(response.split())

    # Ideal range: 50-200 words for a spatial reasoning task
    if 50 <= word_count <= 200:
        return 1.0
    elif word_count < 50:
        # Too short might indicate lack of reasoning
        return max(0.5, word_count / 50)
    else:
        # Penalize verbosity
        return max(0.3, 1.0 - (word_count - 200) / 500)


def compute_spatialeval_score(
    accuracy: float,
    reasoning: float,
    efficiency: float,
    weights: tuple = (0.5, 0.3, 0.2),
) -> float:
    """
    Compute the overall SpatialEval score.

    The score is a weighted average of the three component metrics.

    Args:
        accuracy: The accuracy score (0-1).
        reasoning: The reasoning quality score (0-1).
        efficiency: The efficiency score (0-1).
        weights: A tuple of weights for (accuracy, reasoning, efficiency).

    Returns:
        The overall SpatialEval score (0-100).
    """
    w_acc, w_reas, w_eff = weights
    score = (accuracy * w_acc + reasoning * w_reas + efficiency * w_eff) * 100
    return round(score, 2)
