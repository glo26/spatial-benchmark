"""
Command-line interface for SpatialEval.
"""

import argparse
import json
import sys
from pathlib import Path


def main():
    """Main entry point for the SpatialEval CLI."""
    parser = argparse.ArgumentParser(
        description="SpatialEval: A Comprehensive Benchmark for 2D Spatial Reasoning in LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Info command
    info_parser = subparsers.add_parser("info", help="Display benchmark information")

    # Evaluate command
    eval_parser = subparsers.add_parser("evaluate", help="Run evaluation on a model")
    eval_parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model identifier (e.g., gpt-5.2, claude-3, gemini-1.5)",
    )
    eval_parser.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help="Path to the data directory",
    )
    eval_parser.add_argument(
        "--output",
        type=str,
        default="results.json",
        help="Path to save the results",
    )
    eval_parser.add_argument(
        "--max-tasks",
        type=int,
        default=None,
        help="Maximum number of tasks to evaluate",
    )

    args = parser.parse_args()

    if args.command == "info":
        print_info()
    elif args.command == "evaluate":
        print("Evaluation harness coming soon!")
        print(f"Model: {args.model}")
        print(f"Output: {args.output}")
    else:
        parser.print_help()


def print_info():
    """Print benchmark information."""
    info = """
╔══════════════════════════════════════════════════════════════════════╗
║                         SpatialEval v1.0.0                           ║
╠══════════════════════════════════════════════════════════════════════╣
║  A Comprehensive Benchmark for 2D Spatial Reasoning in LLMs          ║
╠══════════════════════════════════════════════════════════════════════╣
║  Categories:                                                         ║
║    • Coordinate Understanding (CU)                                   ║
║    • Navigation & Pathfinding (NP)                                   ║
║    • Real Estate Analysis (RE)                                       ║
║    • Network Infrastructure (NI)                                     ║
║    • Geometric Reasoning (GR)                                        ║
║    • Distance Computation (DC)                                       ║
╠══════════════════════════════════════════════════════════════════════╣
║  Total Tasks: 2,250 (375 per category × 6 categories)                ║
║  Difficulty Levels: Easy, Medium, Hard                               ║
╠══════════════════════════════════════════════════════════════════════╣
║  Scoring:                                                            ║
║    • Accuracy:  50%                                                  ║
║    • Reasoning: 30%                                                  ║
║    • Efficiency: 20%                                                 ║
╠══════════════════════════════════════════════════════════════════════╣
║  Website: https://github.com/glo26/spatial-benchmark                 ║
║  Paper:   https://arxiv.org/abs/XXXX.XXXXX                           ║
╚══════════════════════════════════════════════════════════════════════╝
    """
    print(info)


if __name__ == "__main__":
    main()
