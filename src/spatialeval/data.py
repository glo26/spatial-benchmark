"""
Data loading utilities for the SpatialEval benchmark.

This module provides functions to load the benchmark dataset from local files
or from the Hugging Face Hub.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union

CATEGORIES = [
    "coordinate_understanding",
    "navigation_pathfinding",
    "real_estate",
    "network_infrastructure",
    "geometric_reasoning",
    "distance_computation",
]

DIFFICULTIES = ["easy", "medium", "hard"]


def load_dataset(
    data_dir: Optional[Union[str, Path]] = None,
    categories: Optional[List[str]] = None,
    difficulties: Optional[List[str]] = None,
) -> Dict[str, Dict[str, List[dict]]]:
    """
    Load the SpatialEval benchmark dataset.

    Args:
        data_dir: Path to the data directory. If None, uses the default path.
        categories: List of categories to load. If None, loads all categories.
        difficulties: List of difficulties to load. If None, loads all difficulties.

    Returns:
        A nested dictionary: {category: {difficulty: [tasks]}}

    Example:
        >>> dataset = load_dataset()
        >>> print(len(dataset["coordinate_understanding"]["easy"]))
        125
    """
    if data_dir is None:
        # Default to the data directory relative to this file
        data_dir = Path(__file__).parent.parent.parent / "data"
    else:
        data_dir = Path(data_dir)

    if categories is None:
        categories = CATEGORIES
    if difficulties is None:
        difficulties = DIFFICULTIES

    dataset = {}
    for category in categories:
        if category not in CATEGORIES:
            raise ValueError(f"Unknown category: {category}. Valid categories: {CATEGORIES}")
        dataset[category] = {}
        for difficulty in difficulties:
            if difficulty not in DIFFICULTIES:
                raise ValueError(
                    f"Unknown difficulty: {difficulty}. Valid difficulties: {DIFFICULTIES}"
                )
            task_file = data_dir / category / difficulty / "tasks.json"
            if task_file.exists():
                with open(task_file, "r") as f:
                    dataset[category][difficulty] = json.load(f)
            else:
                dataset[category][difficulty] = []

    return dataset


def load_category(
    category: str,
    data_dir: Optional[Union[str, Path]] = None,
    difficulties: Optional[List[str]] = None,
) -> Dict[str, List[dict]]:
    """
    Load a single category from the SpatialEval benchmark.

    Args:
        category: The category to load (e.g., "coordinate_understanding").
        data_dir: Path to the data directory. If None, uses the default path.
        difficulties: List of difficulties to load. If None, loads all difficulties.

    Returns:
        A dictionary: {difficulty: [tasks]}

    Example:
        >>> tasks = load_category("navigation_pathfinding")
        >>> print(len(tasks["hard"]))
        125
    """
    dataset = load_dataset(data_dir=data_dir, categories=[category], difficulties=difficulties)
    return dataset[category]


def get_task_count(dataset: Dict[str, Dict[str, List[dict]]]) -> int:
    """
    Count the total number of tasks in a loaded dataset.

    Args:
        dataset: A dataset dictionary returned by load_dataset().

    Returns:
        The total number of tasks.
    """
    count = 0
    for category_data in dataset.values():
        for tasks in category_data.values():
            count += len(tasks)
    return count
