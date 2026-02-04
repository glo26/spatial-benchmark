# SpatialEval: A Comprehensive Benchmark for 2D Spatial Reasoning in Large Language Models

[![Paper](https://img.shields.io/badge/Paper-arXiv-red)](https://arxiv.org/abs/XXXX.XXXXX)
[![Dataset](https://img.shields.io/badge/Dataset-2250_Tasks-blue)](./data/)
[![License](https://img.shields.io/badge/License-Apache_2.0-green)](LICENSE)

## Overview

**SpatialEval** is a comprehensive benchmark designed to rigorously assess the 2D spatial reasoning capabilities of Large Language Models (LLMs). It evaluates models across six distinct task categories grounded in real-world applications from AtlasPro AI.

## Key Features

- **2,250 Tasks** across 6 categories and 3 difficulty levels
- **Multi-faceted Evaluation**: Accuracy (50%) + Reasoning Quality (30%) + Efficiency (20%)
- **Real-World Grounding**: Tasks derived from 60 validated industry use cases
- **Procedural Generation**: Contamination-resistant dataset design

## Task Categories

| Category | Code | Description |
|----------|------|-------------|
| Coordinate Understanding | CU | Coordinate systems, GPS transformations, polygon containment |
| Navigation & Pathfinding | NP | Direction following, shortest path, A* algorithm |
| Real Estate Analysis | RE | Property area, proximity analysis, zoning compliance |
| Network Infrastructure | NI | Cable routing, topology analysis, failure cascade |
| Geometric Reasoning | GR | Shape properties, spatial relationships, polygon area |
| Distance Computation | DC | Euclidean, Manhattan, geodesic (Haversine) distances |

## Dataset Statistics

| Difficulty | Tasks per Category | Total |
|------------|-------------------|-------|
| Easy | 125 | 750 |
| Medium | 125 | 750 |
| Hard | 125 | 750 |
| **Total** | **375** | **2,250** |

## Models Evaluated

1. **OpenAI GPT-5.2**
2. **Anthropic Claude 3** (Opus)
3. **Google Gemini 1.5** (Pro)
4. **xAI Grok-1.5**
5. **DeepSeek-V2**

## Repository Structure

```
spatial-benchmark/
├── arxiv/                    # Paper source files
│   ├── spatialeval.tex       # Main LaTeX paper
│   ├── spatialeval.pdf       # Compiled PDF
│   ├── references.bib        # Bibliography
│   └── figures/              # Paper figures
├── data/                     # Benchmark dataset
│   ├── coordinate_understanding/
│   ├── navigation_pathfinding/
│   ├── real_estate/
│   ├── network_infrastructure/
│   ├── geometric_reasoning/
│   ├── distance_computation/
│   ├── generate_dataset.py   # Dataset generation script
│   └── dataset_summary.json  # Dataset metadata
└── README.md
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/glo26/spatial-benchmark.git
cd spatial-benchmark

# View dataset summary
cat data/dataset_summary.json

# Example: Load coordinate understanding tasks
python3 -c "import json; tasks = json.load(open('data/coordinate_understanding/easy/tasks.json')); print(f'Loaded {len(tasks)} tasks')"
```

## Citation

```bibtex
@article{spatialeval2026,
  title={SpatialEval: A Comprehensive Benchmark for 2D Spatial Reasoning in Large Language Models},
  author={Anonymous},
  journal={arXiv preprint},
  year={2026}
}
```

## Related Work

This benchmark is informed by the comprehensive taxonomy presented in:

> Felicia, G., Bryant, N., Putra, H., Gazali, A., Lobo, E., & Rojas, E. (2026). *From Perception to Action: Spatial AI Agents and World Models*. arXiv:2602.01644.

## License

This project is licensed under the Apache 2.0 License.

---

**Target Venue**: NeurIPS 2026 Datasets & Benchmarks Track
