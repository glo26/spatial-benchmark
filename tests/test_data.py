"""
Tests for the data loading module.
"""

import pytest
from pathlib import Path

# Note: These tests require the data directory to be present
# They are designed to validate the data loading functionality


def test_categories_constant():
    """Test that the CATEGORIES constant is defined correctly."""
    from spatialops.data import CATEGORIES

    assert len(CATEGORIES) == 6
    assert "coordinate_understanding" in CATEGORIES
    assert "navigation_pathfinding" in CATEGORIES


def test_difficulties_constant():
    """Test that the DIFFICULTIES constant is defined correctly."""
    from spatialops.data import DIFFICULTIES

    assert len(DIFFICULTIES) == 3
    assert "easy" in DIFFICULTIES
    assert "medium" in DIFFICULTIES
    assert "hard" in DIFFICULTIES


def test_load_dataset_invalid_category():
    """Test that loading an invalid category raises an error."""
    from spatialops.data import load_dataset

    with pytest.raises(ValueError, match="Unknown category"):
        load_dataset(categories=["invalid_category"])


def test_load_dataset_invalid_difficulty():
    """Test that loading an invalid difficulty raises an error."""
    from spatialops.data import load_dataset

    with pytest.raises(ValueError, match="Unknown difficulty"):
        load_dataset(difficulties=["impossible"])
