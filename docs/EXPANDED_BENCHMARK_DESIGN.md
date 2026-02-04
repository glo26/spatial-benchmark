# SpatialEval v2: Expanded Benchmark Design (12 Categories)

This document outlines the expanded design for SpatialEval v2, increasing the number of categories from 6 to 12 to provide a more comprehensive and challenging benchmark for 2D spatial planning and reasoning.

## Guiding Principles

- **Depth and Breadth:** Cover a wider spectrum of spatial reasoning tasks, from foundational concepts to complex, multi-step planning and optimization.
- **Real-World Relevance:** Ensure each new category is grounded in practical, real-world applications (e.g., logistics, urban planning, robotics, GIS).
- **Progressive Difficulty:** Maintain a clear difficulty gradient (Easy, Medium, Hard) within each category.
- **100% Accuracy:** Implement rigorous validation and programmatic checks to ensure the ground truth for every generated task is verifiably correct.

## Expanded Category Structure (12 Total)

The benchmark is now organized into three tiers: **Foundational Concepts**, **Core Planning & Analysis**, and **Advanced Planning & Optimization**.

### Tier 1: Foundational Concepts

These categories test the model's understanding of the basic building blocks of spatial reasoning.

| ID | Category | Code | Description | Example Task |
|:---|:---|:---|:---|:---|
| 1 | **Coordinate Understanding** | CU | Tests understanding of Cartesian and geographic coordinate systems, transformations, and relative positioning. | *Given a point (3,4) and a vector (-2,1), what is the new coordinate?* |
| 2 | **Geometric Reasoning** | GR | Tests knowledge of shapes, properties (area, perimeter), and spatial relationships (intersection, containment). | *Do these two described rectangles overlap?* |
| 3 | **Distance Computation** | DC | Tests the ability to calculate various distance metrics (Euclidean, Manhattan, Geodesic) between points. | *What is the Manhattan distance between (1,1) and (5,4)?* |
| 4 | **Topological Reasoning** | TR | **(New)** Tests understanding of spatial relationships like adjacency, connectivity, and containment, independent of precise coordinates. | *Given a map of regions, which regions border Region C?* |

### Tier 2: Core Planning & Analysis

These categories require applying foundational concepts to solve common analysis and planning problems.

| ID | Category | Code | Description | Example Task |
|:---|:---|:---|:---|:---|
| 5 | **Navigation & Pathfinding** | NP | Tests algorithmic reasoning for finding optimal paths, such as A* or Dijkstra's, in grid or graph-based environments. | *Find the shortest path from A to B on a grid with obstacles.* |
| 6 | **Viewpoint & Visibility** | VVA | **(New)** Tests the ability to determine visibility (line-of-sight) in a 2D environment with obstacles. | *From which locations on this map can you see the radio tower at (X,Y)?* |
| 7 | **Pattern Recognition** | PRA | **(New)** Tests the ability to identify spatial patterns, clusters, outliers, or trends in a set of 2D data points. | *Is there a statistically significant cluster of events in the northeast quadrant?* |
| 8 | **Network Infrastructure** | NI | Tests analysis of network topologies, such as finding the shortest cable route or identifying points of failure. | *If the link between node 3 and 5 is broken, can node 1 still reach node 7?* |

### Tier 3: Advanced Planning & Optimization

These categories involve complex, multi-step reasoning, often with constraints and optimization objectives.

| ID | Category | Code | Description | Example Task |
|:---|:---|:---|:---|:---|
| 9 | **Constraint-Based Placement** | CBP | **(New)** Tests the ability to place objects in a 2D space while satisfying a set of complex spatial and logical constraints. | *Arrange 5 machines in a factory layout, ensuring none are within 2m of each other and all are within 5m of the main conveyor belt.* |
| 10 | **Resource Allocation** | RAO | **(New)** Tests optimization problems, such as placing a limited number of resources to maximize coverage or service area. | *Given 3 ambulance stations, where should they be placed to minimize the average response time to all city blocks?* |
| 11 | **Temporal-Spatial Reasoning** | TSR | **(New)** Tests reasoning about objects moving or changing their spatial properties over time. | *Two vehicles start at different points and move with given velocities. Will their paths intersect within the next 10 seconds?* |
| 12 | **Real Estate & Geospatial** | RE | Tests complex, multi-step analysis of geospatial data, such as zoning laws, property valuation, and site selection. | *Find all residential properties within 500m of a school but not within 100m of a major highway.* |

## Next Steps

1.  **Dataset Expansion:** The dataset will be significantly expanded to support these 12 categories, aiming for a total of **6,000 tasks** (500 per category).
2.  **Generation Script:** The `generate_dataset.py` script will be updated to include procedural generation logic for the 6 new categories.
3.  **Validation:** Each task generator will include a `validator` function that programmatically solves the task to generate a 100% accurate ground truth.
