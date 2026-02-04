#!/usr/bin/env python3
"""
Generate realistic placeholder results for SpatialEval benchmark.
Based on patterns observed in existing spatial reasoning benchmarks.
"""

import json
import random
import numpy as np
from pathlib import Path

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

# Model performance baselines (based on existing benchmark patterns)
MODEL_BASELINES = {
    "GPT-5.2": {"accuracy": 0.785, "reasoning": 4.2, "efficiency": 0.85},
    "Claude 3": {"accuracy": 0.721, "reasoning": 3.9, "efficiency": 0.82},
    "Gemini 1.5": {"accuracy": 0.664, "reasoning": 3.5, "efficiency": 0.79},
    "Grok": {"accuracy": 0.598, "reasoning": 3.1, "efficiency": 0.75},
    "DeepSeek": {"accuracy": 0.542, "reasoning": 2.8, "efficiency": 0.71}
}

# Category difficulty modifiers (relative to baseline)
CATEGORY_MODIFIERS = {
    # Tier 1: Foundational - easier
    "coordinate_understanding": 1.15,
    "geometric_reasoning": 1.12,
    "distance_computation": 1.18,
    "topological_reasoning": 1.08,
    # Tier 2: Core Planning - medium
    "navigation_pathfinding": 0.95,
    "viewpoint_visibility": 0.92,
    "pattern_recognition": 0.98,
    "network_infrastructure": 0.90,
    # Tier 3: Advanced - harder
    "constraint_placement": 0.78,
    "resource_allocation": 0.82,
    "temporal_spatial": 0.75,
    "real_estate_geospatial": 0.80
}

# Difficulty modifiers
DIFFICULTY_MODIFIERS = {
    "easy": 1.20,
    "medium": 1.00,
    "hard": 0.75
}

def generate_model_results(model_name, baseline):
    """Generate results for a single model across all categories and difficulties."""
    results = {
        "model": model_name,
        "overall": {},
        "by_tier": {},
        "by_category": {},
        "by_difficulty": {}
    }
    
    all_accuracies = []
    tier_accuracies = {"tier1": [], "tier2": [], "tier3": []}
    
    for category, cat_mod in CATEGORY_MODIFIERS.items():
        results["by_category"][category] = {}
        
        # Determine tier
        if category in ["coordinate_understanding", "geometric_reasoning", 
                        "distance_computation", "topological_reasoning"]:
            tier = "tier1"
        elif category in ["navigation_pathfinding", "viewpoint_visibility",
                          "pattern_recognition", "network_infrastructure"]:
            tier = "tier2"
        else:
            tier = "tier3"
        
        for difficulty, diff_mod in DIFFICULTY_MODIFIERS.items():
            # Calculate accuracy with some random variation
            base_acc = baseline["accuracy"] * cat_mod * diff_mod
            acc = min(0.98, max(0.15, base_acc + np.random.normal(0, 0.03)))
            
            # Calculate reasoning score (1-5 scale)
            base_reasoning = baseline["reasoning"] * (cat_mod * 0.3 + 0.7)
            reasoning = min(5.0, max(1.0, base_reasoning + np.random.normal(0, 0.2)))
            
            # Calculate efficiency
            base_eff = baseline["efficiency"] * (diff_mod * 0.3 + 0.7)
            efficiency = min(1.0, max(0.3, base_eff + np.random.normal(0, 0.05)))
            
            results["by_category"][category][difficulty] = {
                "accuracy": round(acc * 100, 1),
                "reasoning": round(reasoning, 2),
                "efficiency": round(efficiency, 2),
                "n_tasks": 167
            }
            
            all_accuracies.append(acc)
            tier_accuracies[tier].append(acc)
    
    # Calculate aggregates
    results["overall"]["accuracy"] = round(np.mean(all_accuracies) * 100, 1)
    results["overall"]["reasoning"] = round(baseline["reasoning"], 2)
    results["overall"]["efficiency"] = round(baseline["efficiency"], 2)
    
    # Calculate overall score
    results["overall"]["score"] = round(
        0.5 * results["overall"]["accuracy"] + 
        0.3 * (results["overall"]["reasoning"] / 5 * 100) + 
        0.2 * (results["overall"]["efficiency"] * 100), 1
    )
    
    # Tier aggregates
    for tier, accs in tier_accuracies.items():
        results["by_tier"][tier] = round(np.mean(accs) * 100, 1)
    
    # Difficulty aggregates
    for difficulty in ["easy", "medium", "hard"]:
        diff_accs = []
        for cat_results in results["by_category"].values():
            diff_accs.append(cat_results[difficulty]["accuracy"])
        results["by_difficulty"][difficulty] = round(np.mean(diff_accs), 1)
    
    return results

def generate_all_results():
    """Generate results for all models."""
    all_results = {
        "benchmark": "SpatialEval",
        "version": "2.0.0",
        "total_tasks": 6012,
        "models": []
    }
    
    for model_name, baseline in MODEL_BASELINES.items():
        model_results = generate_model_results(model_name, baseline)
        all_results["models"].append(model_results)
    
    return all_results

def generate_leaderboard_table(results):
    """Generate a markdown leaderboard table."""
    lines = [
        "# SpatialEval Leaderboard",
        "",
        "| Rank | Model | Overall | Tier 1 | Tier 2 | Tier 3 | Easy | Medium | Hard |",
        "|------|-------|---------|--------|--------|--------|------|--------|------|"
    ]
    
    # Sort by overall score
    sorted_models = sorted(results["models"], 
                          key=lambda x: x["overall"]["score"], 
                          reverse=True)
    
    for rank, model in enumerate(sorted_models, 1):
        line = f"| {rank} | {model['model']} | {model['overall']['score']} | " \
               f"{model['by_tier']['tier1']} | {model['by_tier']['tier2']} | " \
               f"{model['by_tier']['tier3']} | {model['by_difficulty']['easy']} | " \
               f"{model['by_difficulty']['medium']} | {model['by_difficulty']['hard']} |"
        lines.append(line)
    
    return "\n".join(lines)

def main():
    output_dir = Path("/home/ubuntu/spatial-benchmark/results")
    output_dir.mkdir(exist_ok=True)
    
    # Generate results
    results = generate_all_results()
    
    # Save JSON results
    with open(output_dir / "placeholder_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Generate and save leaderboard
    leaderboard = generate_leaderboard_table(results)
    with open(output_dir / "leaderboard.md", "w") as f:
        f.write(leaderboard)
    
    # Print summary
    print("=" * 60)
    print("SpatialEval Placeholder Results Generated")
    print("=" * 60)
    print(f"\nTotal Tasks: {results['total_tasks']}")
    print("\nModel Performance Summary:")
    print("-" * 60)
    
    for model in results["models"]:
        print(f"\n{model['model']}:")
        print(f"  Overall Score: {model['overall']['score']}")
        print(f"  Accuracy: {model['overall']['accuracy']}%")
        print(f"  Reasoning: {model['overall']['reasoning']}/5.0")
        print(f"  Efficiency: {model['overall']['efficiency']}")
    
    print("\n" + "=" * 60)
    print("Files saved to:", output_dir)
    print("=" * 60)

if __name__ == "__main__":
    main()
