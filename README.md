# SpatialOps

<p align="center">
  <img src="arxiv/figures/figure1_framework.png" width="80%" alt="SpatialOps Framework">
</p>

<p align="center">
  <a href="https://arxiv.org/abs/XXXX.XXXXX"><img src="https://img.shields.io/badge/Paper-arXiv-red?style=for-the-badge" alt="Paper"></a>
  <a href="https://huggingface.co/datasets/spatialops/spatialops"><img src="https://img.shields.io/badge/Dataset-HuggingFace-yellow?style=for-the-badge" alt="Dataset"></a>
  <a href="#leaderboard"><img src="https://img.shields.io/badge/Leaderboard-Live-blue?style=for-the-badge" alt="Leaderboard"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-green?style=for-the-badge" alt="License"></a>
</p>

**SpatialOps** is a comprehensive benchmark for evaluating 2D spatial planning and reasoning capabilities in Large Language Models. It comprises **6,012 procedurally generated tasks** across **12 categories**, organized into three tiers of increasing complexity, with **100% ground-truth accuracy**.

---

## News

- **[Feb 2026]** SpatialOps released with 12 categories and 6,012 tasks
- **[Target]** NeurIPS 2026 Datasets and Benchmarks Track

---

## Leaderboard

Performance is measured by the **SpatialOps Score**, a weighted combination of Answer Accuracy (50%), Reasoning Quality (30%), and Efficiency (20%).

| Rank | Model | Score | Accuracy | Tier 1 | Tier 2 | Tier 3 | Easy | Medium | Hard |
|:----:|:------|:-----:|:--------:|:------:|:------:|:------:|:----:|:------:|:----:|
| 1 | GPT-5.2 | **78.4** | 72.5% | 85.2 | 72.1 | 60.3 | 87.5 | 72.5 | 57.6 |
| 2 | Claude 3 | 73.8 | 67.9% | 80.1 | 67.8 | 55.6 | 82.3 | 67.9 | 53.2 |
| 3 | Gemini 1.5 | 68.2 | 62.7% | 74.5 | 62.4 | 51.2 | 76.8 | 62.7 | 48.5 |
| 4 | Grok | 61.8 | 56.3% | 68.3 | 56.1 | 45.8 | 69.5 | 56.3 | 43.2 |
| 5 | DeepSeek | 56.0 | 49.9% | 62.1 | 50.2 | 40.5 | 63.2 | 49.9 | 38.1 |

*Results are placeholder values pending actual API evaluation runs.*

---

## Quick Start

### Installation

```bash
pip install spatialops
```

### Basic Usage

```python
from spatialops import SpatialOpsDataset, Evaluator

# Load dataset
dataset = SpatialOpsDataset()

# Run evaluation
evaluator = Evaluator(model="gpt-5.2")
results = evaluator.evaluate(dataset)

print(f"Overall Score: {results['overall_score']}")
```

### Command Line

```bash
# Evaluate on all tasks
spatialops evaluate --model gpt-5.2 --output results.json

# Evaluate specific category
spatialops evaluate --model gpt-5.2 --category navigation_pathfinding
```

---

## Benchmark Overview

### Task Categories (12 Total)

**Tier 1: Foundational Concepts**

| Code | Category | Description |
|:-----|:---------|:------------|
| CU | Coordinate Understanding | Cartesian coordinates, quadrants, transformations |
| GR | Geometric Reasoning | Shapes, area, perimeter, intersection |
| DC | Distance Computation | Euclidean, Manhattan, geodesic distances |
| TR | Topological Reasoning | Adjacency, connectivity, containment |

**Tier 2: Core Planning**

| Code | Category | Description |
|:-----|:---------|:------------|
| NP | Navigation and Pathfinding | A* algorithm, shortest path, grid navigation |
| VVA | Viewpoint and Visibility | Line-of-sight, obstacle blocking |
| PRA | Pattern Recognition | Clusters, centroids, collinearity |
| NI | Network Infrastructure | Connectivity, hop count, failure analysis |

**Tier 3: Advanced Optimization**

| Code | Category | Description |
|:-----|:---------|:------------|
| CBP | Constraint-Based Placement | Multi-constraint object placement |
| RAO | Resource Allocation | Coverage optimization |
| TSR | Temporal-Spatial Reasoning | Moving objects, trajectories |
| RE | Real Estate and Geospatial | Zoning, proximity, site selection |

### Dataset Statistics

| Metric | Value |
|:-------|------:|
| Total Tasks | 6,012 |
| Categories | 12 |
| Difficulty Levels | 3 |
| Tasks per Category | 501 |
| Ground-Truth Accuracy | 100% |

### Evaluation Methodology

SpatialOps uses a multi-faceted evaluation approach:

```
Score = 0.5 × Accuracy + 0.3 × Reasoning + 0.2 × Efficiency
```

- **Answer Accuracy (50%)**: Correctness of the final answer
- **Reasoning Quality (30%)**: LLM-as-a-Judge evaluation of reasoning chain
- **Efficiency (20%)**: Conciseness of the reasoning process

---

## Repository Structure

```
spatial-benchmark/
├── arxiv/                      # Paper materials
│   ├── spatialeval.tex         # Main paper
│   ├── references_full.bib     # Bibliography (1000+ references)
│   └── figures/                # Figures
├── data/                       # Dataset (6,012 tasks)
│   ├── [category]/             # Per-category folders
│   │   ├── easy/tasks.json
│   │   ├── medium/tasks.json
│   │   └── hard/tasks.json
│   └── dataset_summary.json
├── src/spatialops/             # Python package
│   ├── data.py                 # Data loading
│   ├── harness/                # Evaluation harness
│   └── models/                 # Model wrappers
├── results/                    # Evaluation results
├── docs/                       # Documentation
│   ├── CODEBOOK.md             # Data dictionary
│   └── METHODOLOGY.md          # Detailed methodology
├── tests/                      # Test suite
├── pyproject.toml              # Package config
└── LICENSE                     # Apache 2.0
```

---

## Documentation

- [Code Book](docs/CODEBOOK.md): Complete data dictionary
- [Contributing](CONTRIBUTING.md): How to contribute
- [Changelog](CHANGELOG.md): Version history

---

## Citation

```bibtex
@inproceedings{spatialops2026,
  title={SpatialOps: A Benchmark for 2D Spatial Planning and Reasoning in Large Language Models},
  author={Anonymous},
  booktitle={NeurIPS Datasets and Benchmarks Track},
  year={2026}
}
```

---

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

The dataset is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## Acknowledgments

We thank the developers of AgentBench, SWE-bench, MMLU, BIG-bench, and PRISM for inspiring the design of this benchmark. This work builds upon the theoretical framework presented in "From Perception to Action: Spatial AI Agents and World Models" (Felicia et al., 2026).
