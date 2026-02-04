# SpatialEval v2: A Comprehensive Benchmark for 2D Spatial Planning and Reasoning

<p align="center">
  <img src="https://github.com/glo26/spatial-benchmark/blob/main/arxiv/figures/figure1_framework.png?raw=true" width="75%" alt="SpatialEval Framework">
</p>

<p align="center">
  <a href="https://arxiv.org/abs/XXXX.XXXXX" target="_blank">
    <img src="https://img.shields.io/badge/Paper-arXiv-red?style=for-the-badge" alt="Paper">
  </a>
  <a href="https://huggingface.co/datasets/manus-ai/spatialeval" target="_blank">
    <img src="https://img.shields.io/badge/Dataset-Hugging_Face-yellow?style=for-the-badge" alt="Dataset">
  </a>
  <a href="#leaderboard">
    <img src="https://img.shields.io/badge/Leaderboard-View-blue?style=for-the-badge" alt="Leaderboard">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-Apache_2.0-green?style=for-the-badge" alt="License">
  </a>
</p>

**SpatialEval v2** is a comprehensive benchmark designed to rigorously assess the 2D spatial planning and reasoning capabilities of Large Language Models (LLMs). It introduces **6,012 challenging tasks** across **12 real-world domains**, organized into three tiers of increasing complexity and grounded in high-value industry use cases from AtlasPro AI. SpatialEval moves beyond simple accuracy to evaluate models on a multi-faceted scoring system, providing a holistic view of their spatial intelligence.

This benchmark is designed to address a critical gap in AI evaluation: while LLMs excel at language, their ability to reason about physical space, geometry, and topology remains a significant frontier. SpatialEval v2 provides the community with a robust tool to measure progress and drive the development of more spatially-aware AI agents.

## News

- **[Feb 2026]**: SpatialEval v2.0 is released! Expanded to 12 categories and 6,012 tasks with 100% ground-truth accuracy.

## Leaderboard

Performance is measured by the overall **SpatialEval Score**, a weighted average of Answer Accuracy (50%), Reasoning Quality (30%), and Efficiency (20%).

| Rank | Model | SpatialEval Score | Accuracy | Reasoning | Efficiency | Link |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | GPT-5.2 | TBD | TBD | TBD | TBD | TBD |
| 2 | Claude 3 Opus | TBD | TBD | TBD | TBD | TBD |
| 3 | Gemini 1.5 Pro | TBD | TBD | TBD | TBD | TBD |
| 4 | Grok-1 | TBD | TBD | TBD | TBD | TBD |
| 5 | DeepSeek-V2 | TBD | TBD | TBD | TBD | TBD |

*To submit your model for evaluation, please open a pull request with your results.* 

## Quick Start

### 1. Installation

We recommend using a conda environment:

```bash
# Clone the repository
git clone https://github.com/glo26/spatial-benchmark.git
cd spatial-benchmark

# Create and activate conda environment
conda create -n spatialeval python=3.10
conda activate spatialeval

# Install the package
pip install -e .
```

### 2. Download Dataset

The dataset is hosted on Hugging Face and can be downloaded directly:

```python
from datasets import load_dataset

# Load the full dataset
dataset = load_dataset("manus-ai/spatialeval")

# Load a specific category
coord_understanding_tasks = load_dataset("manus-ai/spatialeval", "coordinate_understanding")

print(dataset["test"][0])
```

### 3. Run Evaluation

```python
from spatialeval import Evaluator
from spatialeval.models import OpenAIModel

# 1. Initialize your model
model = OpenAIModel(model_name="gpt-5.2", api_key="YOUR_API_KEY")

# 2. Initialize the evaluator
evaluator = Evaluator(model_fn=model)

# 3. Run the evaluation
scores = evaluator.run()

# 4. Print the results
print(scores)
```

## Benchmark Design

### Task Categories (12 Categories, 3 Tiers)

**Tier 1: Foundational Concepts**

| Category | Code | Description |
| :--- | :--- | :--- |
| Coordinate Understanding | CU | Coordinate systems, GPS transformations, quadrant identification |
| Geometric Reasoning | GR | Shape properties, area/perimeter, intersection, containment |
| Distance Computation | DC | Euclidean, Manhattan, geodesic (Haversine) distances |
| Topological Reasoning | TR | Adjacency, connectivity, containment relationships |

**Tier 2: Core Planning and Analysis**

| Category | Code | Description |
| :--- | :--- | :--- |
| Navigation and Pathfinding | NP | A* algorithm, shortest path, route planning |
| Viewpoint and Visibility | VVA | Line-of-sight analysis with obstacles |
| Pattern Recognition | PRA | Spatial patterns, clusters, outliers, trends |
| Network Infrastructure | NI | Cable routing, topology analysis, failure cascade |

**Tier 3: Advanced Planning and Optimization**

| Category | Code | Description |
| :--- | :--- | :--- |
| Constraint-Based Placement | CBP | Placing objects with spatial/logical constraints |
| Resource Allocation | RAO | Optimizing resource placement for coverage |
| Temporal-Spatial Reasoning | TSR | Reasoning about moving objects over time |
| Real Estate and Geospatial | RE | Zoning compliance, property analysis, site selection |

### Dataset Structure

The dataset is composed of 6,012 tasks, evenly distributed across the 12 categories and 3 difficulty levels (Easy, Medium, Hard). Each task is procedurally generated with a programmatic validator to ensure 100% ground-truth accuracy. A detailed explanation of the data schema can be found in the [Data Code Book](./docs/CODEBOOK.md).

## Community and Contribution

We welcome contributions from the community! Whether it's adding new tasks, improving the evaluation code, or submitting model results, your help is valued.

- **Contribution Guidelines**: Please read our [CONTRIBUTING.md](./CONTRIBUTING.md) for details on how to get started.
- **Issue Tracker**: Found a bug or have a feature request? Please open an issue.
- **Contact**: For other inquiries, please email `spatialeval-team@manus.ai`.

## Citation

If you use SpatialEval in your research, please cite our paper:

```bibtex
@inproceedings{spatialeval2026,
  title={{SpatialEval v2: An Expanded Benchmark for 2D Spatial Planning and Reasoning in Large Language Models}},
  author={Anonymous},
  booktitle={Advances in Neural Information Processing Systems},
  year={2026}
}
```

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](./LICENSE) file for details.
