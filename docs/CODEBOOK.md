# SpatialOps Data Code Book

This document provides a complete specification of the SpatialOps dataset schema, task formats, and evaluation criteria.

## Dataset Overview

| Property | Value |
|:---------|:------|
| Total Tasks | 6,012 |
| Categories | 12 |
| Difficulty Levels | 3 (Easy, Medium, Hard) |
| Format | JSON |
| Ground-Truth Accuracy | 100% (programmatically validated) |

## Core Task Schema

Each task in the dataset follows this JSON schema:

```json
{
  "task_id": "string",
  "category": "string",
  "difficulty": "string",
  "prompt": "string",
  "ground_truth": "any",
  "answer_type": "string",
  "metadata": "object"
}
```

### Field Descriptions

| Field | Type | Description |
|:------|:-----|:------------|
| `task_id` | string | Unique identifier (format: `{category}-{difficulty}-{index}`) |
| `category` | string | One of 12 category codes (see below) |
| `difficulty` | string | `easy`, `medium`, or `hard` |
| `prompt` | string | The natural language question |
| `ground_truth` | any | Ground-truth answer (type varies by task) |
| `answer_type` | string | `exact`, `numerical`, `sequence`, or `boolean` |
| `metadata` | object | Task-specific parameters and context |

## Category Codes

| Code | Full Name | Tier |
|:-----|:----------|:-----|
| `CU` | Coordinate Understanding | 1 |
| `GR` | Geometric Reasoning | 1 |
| `DC` | Distance Computation | 1 |
| `TR` | Topological Reasoning | 1 |
| `NP` | Navigation and Pathfinding | 2 |
| `VVA` | Viewpoint and Visibility | 2 |
| `PRA` | Pattern Recognition | 2 |
| `NI` | Network Infrastructure | 2 |
| `CBP` | Constraint-Based Placement | 3 |
| `RAO` | Resource Allocation | 3 |
| `TSR` | Temporal-Spatial Reasoning | 3 |
| `RE` | Real Estate and Geospatial | 3 |

---

## Metadata Schema by Category

### Tier 1: Foundational Concepts

#### 1. Coordinate Understanding (CU)

| Metadata Key | Type | Description |
|:-------------|:-----|:------------|
| `points` | Array[Object] | Named points with `x` and `y` coordinates |
| `polygons` | Array[Object] | Named polygons defined by vertices |
| `query_type` | String | Sub-task type (e.g., `quadrant_identification`) |

#### 2. Geometric Reasoning (GR)

| Metadata Key | Type | Description |
|:-------------|:-----|:------------|
| `shapes` | Array[Object] | Shape definitions with type and vertices |
| `query_type` | String | Sub-task type (e.g., `area_calculation`) |

#### 3. Distance Computation (DC)

| Metadata Key | Type | Description |
|:-------------|:-----|:------------|
| `point_a` | Array[Float] | First point coordinates |
| `point_b` | Array[Float] | Second point coordinates |
| `metric` | String | Distance metric (`euclidean`, `manhattan`, `geodesic`) |

#### 4. Topological Reasoning (TR)

| Metadata Key | Type | Description |
|:-------------|:-----|:------------|
| `regions` | Array[Object] | Region definitions |
| `query_type` | String | Sub-task type (e.g., `adjacency_check`) |

### Tier 2: Core Planning

#### 5. Navigation and Pathfinding (NP)

| Metadata Key | Type | Description |
|:-------------|:-----|:------------|
| `grid_size` | Array[Int] | Grid dimensions `[width, height]` |
| `start_pos` | Array[Int] | Starting coordinates |
| `end_pos` | Array[Int] | Goal coordinates |
| `obstacles` | Array[Array[Int]] | Blocked cell coordinates |
| `algorithm` | String | Algorithm to simulate (`A*`, `dijkstra`) |

#### 6. Viewpoint and Visibility (VVA)

| Metadata Key | Type | Description |
|:-------------|:-----|:------------|
| `observer` | Array[Float] | Observer position |
| `target` | Array[Float] | Target position |
| `obstacles` | Array[Object] | Obstacle definitions |

#### 7. Pattern Recognition (PRA)

| Metadata Key | Type | Description |
|:-------------|:-----|:------------|
| `points` | Array[Array[Float]] | Set of 2D points |
| `query_type` | String | Sub-task type (e.g., `find_centroid`) |

#### 8. Network Infrastructure (NI)

| Metadata Key | Type | Description |
|:-------------|:-----|:------------|
| `nodes` | Array[Object] | Network node definitions |
| `edges` | Array[Object] | Network edge definitions |
| `query_type` | String | Sub-task type (e.g., `shortest_route`) |

### Tier 3: Advanced Optimization

#### 9. Constraint-Based Placement (CBP)

| Metadata Key | Type | Description |
|:-------------|:-----|:------------|
| `area` | Object | Placement area bounds |
| `objects` | Array[Object] | Objects to place |
| `constraints` | Array[Object] | Placement constraints |

#### 10. Resource Allocation (RAO)

| Metadata Key | Type | Description |
|:-------------|:-----|:------------|
| `area` | Object | Service area bounds |
| `demand_points` | Array[Array[Float]] | Points requiring coverage |
| `num_resources` | Int | Number of resources to place |
| `coverage_radius` | Float | Coverage radius per resource |

#### 11. Temporal-Spatial Reasoning (TSR)

| Metadata Key | Type | Description |
|:-------------|:-----|:------------|
| `objects` | Array[Object] | Moving object definitions |
| `time_range` | Array[Float] | Time interval `[start, end]` |
| `query_type` | String | Sub-task type (e.g., `collision_detection`) |

#### 12. Real Estate and Geospatial (RE)

| Metadata Key | Type | Description |
|:-------------|:-----|:------------|
| `properties` | Array[Object] | Property definitions |
| `zones` | Array[Object] | Zoning definitions |
| `query_type` | String | Sub-task type (e.g., `zoning_compliance`) |

---

## Answer Types

| Type | Description | Evaluation |
|:-----|:------------|:-----------|
| `exact` | Categorical/string answers | Case-insensitive match |
| `numerical` | Numeric answers | Tolerance: 1% relative, 0.01 absolute |
| `sequence` | Ordered lists (paths) | Sequence similarity with partial credit |
| `boolean` | Yes/no answers | Exact boolean match |

---

## Example Tasks

### Coordinate Understanding (Easy)

```json
{
  "task_id": "CU-easy-001",
  "category": "coordinate_understanding",
  "difficulty": "easy",
  "prompt": "In which quadrant is the point (3, -4) located?",
  "ground_truth": "IV",
  "answer_type": "exact",
  "metadata": {
    "points": [{"name": "P", "x": 3, "y": -4}],
    "query_type": "quadrant_identification"
  }
}
```

### Navigation and Pathfinding (Medium)

```json
{
  "task_id": "NP-medium-042",
  "category": "navigation_pathfinding",
  "difficulty": "medium",
  "prompt": "Find the shortest path from (0,0) to (3,3) using A*.",
  "ground_truth": [[0,0], [1,0], [2,0], [2,1], [2,2], [3,2], [3,3]],
  "answer_type": "sequence",
  "metadata": {
    "grid_size": [4, 4],
    "start_pos": [0, 0],
    "end_pos": [3, 3],
    "obstacles": [[0,2], [1,1], [3,2]],
    "algorithm": "A*"
  }
}
```

---

## Evaluation Metrics

### Overall Score Formula

```
Score = 0.5 × Accuracy + 0.3 × (Reasoning / 5 × 100) + 0.2 × (Efficiency × 100)
```

### Reasoning Quality (1-5 Scale)

| Score | Description |
|:------|:------------|
| 5 | Excellent: Clear, correct, complete reasoning |
| 4 | Good: Minor issues but fundamentally sound |
| 3 | Adequate: Some errors but shows understanding |
| 2 | Poor: Significant errors or gaps |
| 1 | Very Poor: Incorrect or incoherent reasoning |

---

## File Structure

```
data/
├── coordinate_understanding/
│   ├── easy/tasks.json
│   ├── medium/tasks.json
│   └── hard/tasks.json
├── geometric_reasoning/
│   └── ...
├── ... (10 more categories)
└── dataset_summary.json
```

---

## Version History

| Version | Date | Changes |
|:--------|:-----|:--------|
| 2.0.0 | Feb 2026 | Expanded to 12 categories, 6,012 tasks |
| 1.0.0 | Jan 2026 | Initial release with 6 categories |
