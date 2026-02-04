# SpatialEval: A Comprehensive Benchmark for 2D Spatial Reasoning in Large Language Models

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

**SpatialEval** is a comprehensive benchmark designed to rigorously assess the 2D spatial reasoning capabilities of Large Language Models (LLMs). It introduces **2,250 challenging tasks** across **6 real-world domains**, grounded in high-value industry use cases from AtlasPro AI. SpatialEval moves beyond simple accuracy to evaluate models on a multi-faceted scoring system, providing a holistic view of their spatial intelligence.

This benchmark is designed to address a critical gap in AI evaluation: while LLMs excel at language, their ability to reason about physical space, geometry, and topology remains a significant frontier. SpatialEval provides the community with a robust tool to measure progress and drive the development of more spatially-aware AI agents.

## 📰 News

- **[Feb 2026]**: SpatialEval v1.0 is released! The dataset, paper, and evaluation code are now public.

## 🏆 Leaderboard

Performance is measured by the overall **SpatialEval Score**, a weighted average of Answer Accuracy (50%), Reasoning Quality (30%), and Efficiency (20%).

| Rank | Model | SpatialEval Score | Accuracy | Reasoning | Efficiency | Link |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 🥇 | `[Placeholder]` | `[TBD]` | `[TBD]` | `[TBD]` | `[TBD]` | `[TBD]` |
| 🥈 | `[Placeholder]` | `[TBD]` | `[TBD]` | `[TBD]` | `[TBD]` | `[TBD]` |
| 🥉 | `[Placeholder]` | `[TBD]` | `[TBD]` | `[TBD]` | `[TBD]` | `[TBD]` |

*To submit your model for evaluation, please open a pull request with your results.* 

## 🚀 Quick Start

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

### 3. Run Evaluation (Coming Soon)

The evaluation harness will be containerized using Docker for 100% reproducibility. Instructions will be provided here.

## 📚 Benchmark Design

### Task Categories

| Category | Code | Description |
| :--- | :--- | :--- |
| **Coordinate Understanding** | `CU` | Coordinate systems, GPS transformations, polygon containment |
| **Navigation & Pathfinding** | `NP` | Direction following, shortest path, A* algorithm |
| **Real Estate Analysis** | `RE` | Property area, proximity analysis, zoning compliance |
| **Network Infrastructure** | `NI` | Cable routing, topology analysis, failure cascade |
| **Geometric Reasoning** | `GR` | Shape properties, spatial relationships, polygon area |
| **Distance Computation** | `DC` | Euclidean, Manhattan, geodesic (Haversine) distances |

### Dataset Structure

The dataset is composed of 2,250 tasks, evenly distributed across the 6 categories and 3 difficulty levels (Easy, Medium, Hard). A detailed explanation of the data schema can be found in the [Data Code Book](./docs/CODEBOOK.md).

## 🤝 Community & Contribution

We welcome contributions from the community! Whether it's adding new tasks, improving the evaluation code, or submitting model results, your help is valued.

- **Contribution Guidelines**: Please read our [CONTRIBUTING.md](./CONTRIBUTING.md) for details on how to get started.
- **Issue Tracker**: Found a bug or have a feature request? Please open an issue.
- **Contact**: For other inquiries, please email `spatialeval-team@manus.ai`.

## ✍️ Citation

If you use SpatialEval in your research, please cite our paper:

```bibtex
@inproceedings{spatialeval2026,
  title={{SpatialEval: A Comprehensive Benchmark for 2D Spatial Reasoning in Large Language Models}},
  author={Anonymous},
  booktitle={Advances in Neural Information Processing Systems},
  year={2026}
}
```

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](./LICENSE) file for details.
