"""
Tests for the metrics module.
"""

import pytest
from spatialops.harness.metrics import (
    compute_accuracy,
    compute_reasoning_score,
    compute_efficiency_score,
    compute_spatialops_score,
)


class TestComputeAccuracy:
    """Tests for the compute_accuracy function."""

    def test_exact_numeric_match(self):
        """Test exact numeric match."""
        assert compute_accuracy("The answer is 42", 42) == 1.0
        assert compute_accuracy("42", 42) == 1.0

    def test_numeric_in_text(self):
        """Test extracting numbers from text."""
        response = "After calculating, I found that the distance is 15.5 meters."
        assert compute_accuracy(response, 15.5) == 1.0

    def test_string_match(self):
        """Test string matching."""
        assert compute_accuracy("The point is in Quadrant I", "Quadrant I") == 1.0
        assert compute_accuracy("quadrant i", "Quadrant I") == 1.0  # Case insensitive

    def test_list_ground_truth(self):
        """Test with multiple acceptable answers."""
        assert compute_accuracy("The answer is yes", ["yes", "true", "correct"]) == 1.0
        assert compute_accuracy("The answer is true", ["yes", "true", "correct"]) == 1.0

    def test_no_match(self):
        """Test when there's no match."""
        assert compute_accuracy("I don't know", 42) == 0.0
        assert compute_accuracy("The answer is 100", 42) == 0.0


class TestComputeReasoningScore:
    """Tests for the compute_reasoning_score function."""

    def test_base_score(self):
        """Test that a minimal response gets the base score."""
        score = compute_reasoning_score("42")
        assert 0.4 <= score <= 0.6

    def test_step_by_step_reasoning(self):
        """Test that step-by-step reasoning is rewarded."""
        response = "First, I calculate the distance. Then, I apply the formula. Therefore, the answer is 42."
        score = compute_reasoning_score(response)
        assert score > 0.6

    def test_mathematical_notation(self):
        """Test that mathematical notation is rewarded."""
        response = "The calculation is 10 + 5 = 15. Therefore, the answer is 15."
        score = compute_reasoning_score(response)
        assert score > 0.5


class TestComputeEfficiencyScore:
    """Tests for the compute_efficiency_score function."""

    def test_optimal_length(self):
        """Test that optimal length responses get high scores."""
        response = " ".join(["word"] * 100)  # 100 words
        assert compute_efficiency_score(response) == 1.0

    def test_too_short(self):
        """Test that very short responses are penalized."""
        response = "42"
        score = compute_efficiency_score(response)
        assert score < 1.0

    def test_too_long(self):
        """Test that very long responses are penalized."""
        response = " ".join(["word"] * 500)  # 500 words
        score = compute_efficiency_score(response)
        assert score < 1.0


class TestComputeSpatialEvalScore:
    """Tests for the compute_spatialops_score function."""

    def test_perfect_scores(self):
        """Test with perfect component scores."""
        score = compute_spatialops_score(1.0, 1.0, 1.0)
        assert score == 100.0

    def test_zero_scores(self):
        """Test with zero component scores."""
        score = compute_spatialops_score(0.0, 0.0, 0.0)
        assert score == 0.0

    def test_weighted_average(self):
        """Test that the weighted average is computed correctly."""
        # Default weights: (0.5, 0.3, 0.2)
        score = compute_spatialops_score(1.0, 0.0, 0.0)
        assert score == 50.0  # 1.0 * 0.5 * 100

        score = compute_spatialops_score(0.0, 1.0, 0.0)
        assert score == 30.0  # 1.0 * 0.3 * 100

        score = compute_spatialops_score(0.0, 0.0, 1.0)
        assert score == 20.0  # 1.0 * 0.2 * 100
