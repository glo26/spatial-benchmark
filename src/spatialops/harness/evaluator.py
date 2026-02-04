"""
Core Evaluator class for running SpatialEval benchmark evaluations.
"""

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from tqdm import tqdm

from spatialops.data import load_dataset
from spatialops.harness.metrics import (
    compute_accuracy,
    compute_efficiency_score,
    compute_reasoning_score,
    compute_spatialops_score,
)


class Evaluator:
    """
    The main class for evaluating LLMs on the SpatialEval benchmark.

    This class handles loading the dataset, running inference on a model,
    and computing the final scores.

    Attributes:
        model_fn: A callable that takes a prompt string and returns a response string.
        dataset: The loaded benchmark dataset.
        results: A list of evaluation results for each task.

    Example:
        >>> def my_model(prompt: str) -> str:
        ...     # Call your LLM API here
        ...     return "The answer is 42."
        >>> evaluator = Evaluator(model_fn=my_model)
        >>> scores = evaluator.run()
        >>> print(scores["overall_score"])
    """

    def __init__(
        self,
        model_fn: Callable[[str], str],
        data_dir: Optional[Path] = None,
        categories: Optional[List[str]] = None,
        difficulties: Optional[List[str]] = None,
    ):
        """
        Initialize the Evaluator.

        Args:
            model_fn: A callable that takes a prompt and returns a model response.
            data_dir: Path to the data directory.
            categories: List of categories to evaluate on.
            difficulties: List of difficulties to evaluate on.
        """
        self.model_fn = model_fn
        self.dataset = load_dataset(
            data_dir=data_dir, categories=categories, difficulties=difficulties
        )
        self.results: List[Dict[str, Any]] = []

    def run(
        self,
        max_tasks: Optional[int] = None,
        verbose: bool = True,
    ) -> Dict[str, Any]:
        """
        Run the evaluation on the loaded dataset.

        Args:
            max_tasks: Maximum number of tasks to evaluate. If None, evaluates all.
            verbose: Whether to show a progress bar.

        Returns:
            A dictionary containing the overall scores and per-category breakdowns.
        """
        self.results = []
        task_count = 0

        all_tasks = []
        for category, category_data in self.dataset.items():
            for difficulty, tasks in category_data.items():
                for task in tasks:
                    all_tasks.append((category, difficulty, task))

        if max_tasks is not None:
            all_tasks = all_tasks[:max_tasks]

        iterator = tqdm(all_tasks, desc="Evaluating") if verbose else all_tasks

        for category, difficulty, task in iterator:
            prompt = task["prompt"]
            ground_truth = task["ground_truth"]

            # Get model response
            response = self.model_fn(prompt)

            # Compute individual metrics
            accuracy = compute_accuracy(response, ground_truth)
            reasoning = compute_reasoning_score(response)
            efficiency = compute_efficiency_score(response)

            result = {
                "task_id": task["task_id"],
                "category": category,
                "difficulty": difficulty,
                "prompt": prompt,
                "ground_truth": ground_truth,
                "response": response,
                "accuracy": accuracy,
                "reasoning_score": reasoning,
                "efficiency_score": efficiency,
            }
            self.results.append(result)
            task_count += 1

        return self._compute_final_scores()

    def _compute_final_scores(self) -> Dict[str, Any]:
        """Compute the final aggregated scores from individual results."""
        if not self.results:
            return {"error": "No results to compute scores from."}

        total_accuracy = sum(r["accuracy"] for r in self.results) / len(self.results)
        total_reasoning = sum(r["reasoning_score"] for r in self.results) / len(self.results)
        total_efficiency = sum(r["efficiency_score"] for r in self.results) / len(self.results)

        overall_score = compute_spatialops_score(
            total_accuracy, total_reasoning, total_efficiency
        )

        # Per-category breakdown
        category_scores = {}
        for category in self.dataset.keys():
            cat_results = [r for r in self.results if r["category"] == category]
            if cat_results:
                cat_acc = sum(r["accuracy"] for r in cat_results) / len(cat_results)
                cat_reas = sum(r["reasoning_score"] for r in cat_results) / len(cat_results)
                cat_eff = sum(r["efficiency_score"] for r in cat_results) / len(cat_results)
                category_scores[category] = {
                    "accuracy": cat_acc,
                    "reasoning": cat_reas,
                    "efficiency": cat_eff,
                    "score": compute_spatialops_score(cat_acc, cat_reas, cat_eff),
                }

        return {
            "overall_score": overall_score,
            "accuracy": total_accuracy,
            "reasoning": total_reasoning,
            "efficiency": total_efficiency,
            "num_tasks": len(self.results),
            "per_category": category_scores,
        }

    def save_results(self, output_path: Path) -> None:
        """Save the detailed results to a JSON file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=2)
