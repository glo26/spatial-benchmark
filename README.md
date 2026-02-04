# SpatialEval: A Comprehensive Benchmark for 2D Spatial Reasoning in Large Language Models

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![NeurIPS 2026](https://img.shields.io/badge/NeurIPS-2026-purple.svg)](https://neurips.cc/)

## Overview

**SpatialEval** is a comprehensive benchmark designed to rigorously assess the 2D spatial reasoning capabilities of Large Language Models (LLMs). Unlike existing benchmarks that focus on abstract grid-world scenarios, SpatialEval tests models on practical, real-world spatial problems encountered in domains such as urban planning, logistics, and engineering.

## Key Features

- **Six Diverse Task Categories**: Coordinate Understanding, Navigation & Pathfinding, Real Estate Spatial Analysis, Network Infrastructure, Geometric Reasoning, and Distance Computation
- **2,250 Carefully Curated Tasks**: Spanning three difficulty levels (Easy, Medium, Hard)
- **Multi-Faceted Evaluation**: Beyond accuracy—assessing reasoning quality and efficiency
- **Real-World Grounding**: Tasks derived from practical applications and real data

## Task Categories

| Category | Code | Description |
|----------|------|-------------|
| Coordinate Understanding | CU | Cartesian/Polar coordinates, GPS reasoning, transformations |
| Navigation & Pathfinding | NP | A* algorithm, shortest path, multi-waypoint routing |
| Real Estate Analysis | RE | Property boundaries, proximity queries, zoning compliance |
| Network Infrastructure | NI | Cable routing, network topology, connectivity analysis |
| Geometric Reasoning | GR | Shape recognition, area/perimeter, spatial relationships |
| Distance Computation | DC | Euclidean, Manhattan, geodesic distances |

## Evaluated Models

- OpenAI GPT-5.2
- Anthropic Claude 3 (Opus)
- Google Gemini 1.5 (Pro)
- xAI Grok-1.5
- DeepSeek-V2

## Repository Structure

```
spatial-benchmark/
├── arxiv/                    # Paper source files
│   ├── spatialeval.tex       # Main LaTeX file
│   ├── references.bib        # Bibliography
│   ├── neurips_2023.sty      # NeurIPS style file
│   └── figures/              # Paper figures
├── data/                     # Benchmark dataset (coming soon)
├── evaluation/               # Evaluation scripts (coming soon)
└── README.md
```

## Citation

If you use SpatialEval in your research, please cite:

```bibtex
@inproceedings{spatialeval2026,
  title={SpatialEval: A Comprehensive Benchmark for 2D Spatial Reasoning in Large Language Models},
  author={Anonymous},
  booktitle={Advances in Neural Information Processing Systems (NeurIPS) Datasets and Benchmarks Track},
  year={2026}
}
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Status

**Draft v1** - Paper structure and methodology complete. Experimental results pending.
