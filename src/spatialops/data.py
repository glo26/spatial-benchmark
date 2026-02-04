"""
Data loading utilities for the SpatialEval v2 benchmark.

This module provides functions to load the benchmark dataset from local files
or from the Hugging Face Hub.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union
from dataclasses import dataclass

# Define the 12 categories organized by tier
TIER_1_CATEGORIES = [
    "coordinate_understanding",
    "geometric_reasoning",
    "distance_computation",
    "topological_reasoning",
]

TIER_2_CATEGORIES = [
    "navigation_pathfinding",
    "viewpoint_visibility",
    "pattern_recognition",
    "network_infrastructure",
]

TIER_3_CATEGORIES = [
    "constraint_based_placement",
    "resource_allocation",
    "temporal_spatial_reasoning",
    "real_estate_geospatial",
]

CATEGORIES = TIER_1_CATEGORIES + TIER_2_CATEGORIES + TIER_3_CATEGORIES

CATEGORY_CODES = {
    "coordinate_understanding": "CU",
    "geometric_reasoning": "GR",
    "distance_computation": "DC",
    "topological_reasoning": "TR",
    "navigation_pathfinding": "NP",
    "viewpoint_visibility": "VVA",
    "pattern_recognition": "PRA",
    "network_infrastructure": "NI",
    "constraint_based_placement": "CBP",
    "resource_allocation": "RAO",
    "temporal_spatial_reasoning": "TSR",
    "real_estate_geospatial": "RE",
}

DIFFICULTIES = ["easy", "medium", "hard"]


@dataclass
class Task:
    """Represents a single SpatialEval task."""
    task_id: str
    category: str
    difficulty: str
    prompt: str
    ground_truth: Union[str, int, float]
    
    @property
    def category_code(self) -> str:
        return CATEGORY_CODES.get(self.category, "UNK")
    
    @property
    def tier(self) -> int:
        if self.category in TIER_1_CATEGORIES:
            return 1
        elif self.category in TIER_2_CATEGORIES:
            return 2
        elif self.category in TIER_3_CATEGORIES:
            return 3
        return 0


def load_dataset(
    data_dir: Optional[Union[str, Path]] = None,
    categories: Optional[List[str]] = None,
    difficulties: Optional[List[str]] = None,
    tier: Optional[int] = None,
) -> Dict[str, Dict[str, List[dict]]]:
    """
    Load the SpatialEval v2 benchmark dataset.

    Args:
        data_dir: Path to the data directory. If None, uses the default path.
        categories: List of categories to load. If None, loads all categories.
        difficulties: List of difficulties to load. If None, loads all difficulties.
        tier: If specified, loads only categories from this tier (1, 2, or 3).

    Returns:
        A nested dictionary: {category: {difficulty: [tasks]}}

    Example:
        >>> dataset = load_dataset()
        >>> print(len(dataset["coordinate_understanding"]["easy"]))
        167
    """
    if data_dir is None:
        # Default to the data directory relative to this file
        data_dir = Path(__file__).parent.parent.parent / "data"
    else:
        data_dir = Path(data_dir)

    # Determine which categories to load
    if tier is not None:
        if tier == 1:
            cats_to_load = TIER_1_CATEGORIES
        elif tier == 2:
            cats_to_load = TIER_2_CATEGORIES
        elif tier == 3:
            cats_to_load = TIER_3_CATEGORIES
        else:
            raise ValueError(f"Invalid tier: {tier}. Must be 1, 2, or 3.")
    elif categories is not None:
        cats_to_load = categories
    else:
        cats_to_load = CATEGORIES

    if difficulties is None:
        difficulties = DIFFICULTIES

    dataset = {}
    for category in cats_to_load:
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
        167
    """
    dataset = load_dataset(data_dir=data_dir, categories=[category], difficulties=difficulties)
    return dataset[category]


def load_tier(
    tier: int,
    data_dir: Optional[Union[str, Path]] = None,
    difficulties: Optional[List[str]] = None,
) -> Dict[str, Dict[str, List[dict]]]:
    """
    Load all categories from a specific tier.

    Args:
        tier: The tier to load (1, 2, or 3).
        data_dir: Path to the data directory. If None, uses the default path.
        difficulties: List of difficulties to load. If None, loads all difficulties.

    Returns:
        A nested dictionary: {category: {difficulty: [tasks]}}

    Example:
        >>> tier1_tasks = load_tier(1)
        >>> print(list(tier1_tasks.keys()))
        ['coordinate_understanding', 'geometric_reasoning', 'distance_computation', 'topological_reasoning']
    """
    return load_dataset(data_dir=data_dir, tier=tier, difficulties=difficulties)


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


def get_dataset_summary(dataset: Dict[str, Dict[str, List[dict]]]) -> Dict:
    """
    Get a summary of the loaded dataset.

    Args:
        dataset: A dataset dictionary returned by load_dataset().

    Returns:
        A summary dictionary with counts by category, difficulty, and tier.
    """
    summary = {
        "total_tasks": 0,
        "by_category": {},
        "by_difficulty": {"easy": 0, "medium": 0, "hard": 0},
        "by_tier": {1: 0, 2: 0, 3: 0},
    }
    
    for category, difficulties in dataset.items():
        cat_total = 0
        for difficulty, tasks in difficulties.items():
            task_count = len(tasks)
            cat_total += task_count
            summary["by_difficulty"][difficulty] += task_count
        
        summary["by_category"][category] = cat_total
        summary["total_tasks"] += cat_total
        
        # Determine tier
        if category in TIER_1_CATEGORIES:
            summary["by_tier"][1] += cat_total
        elif category in TIER_2_CATEGORIES:
            summary["by_tier"][2] += cat_total
        elif category in TIER_3_CATEGORIES:
            summary["by_tier"][3] += cat_total
    
    return summary
