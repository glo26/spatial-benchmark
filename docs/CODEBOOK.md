# SpatialEval Dataset Code Book

This document provides a detailed explanation of the data schema for the SpatialEval benchmark dataset. The dataset is organized into six categories, each with three difficulty levels (easy, medium, hard). All task files are in JSONL format.

## Core Task Schema

Each line in a task file represents a single task object with the following core keys:

| Key | Type | Description |
| :--- | :--- | :--- |
| `task_id` | String | A unique identifier for the task, e.g., `cu-easy-001`. |
| `category` | String | The task category code (e.g., `CU`, `NP`, `RE`, `NI`, `GR`, `DC`). |
| `difficulty` | String | The difficulty level: `easy`, `medium`, or `hard`. |
| `prompt` | String | The natural language question or instruction for the model. |
| `ground_truth` | Any | The correct answer for the task. The data type depends on the task. |
| `metadata` | Object | An object containing task-specific information and parameters. |

---

## Metadata Schema by Category

The structure of the `metadata` object varies by category to accommodate the specific parameters of each task.

### 1. Coordinate Understanding (CU)

**Description:** Tasks related to understanding and manipulating 2D coordinate systems.

| Metadata Key | Type | Description |
| :--- | :--- | :--- |
| `points` | Array[Object] | A list of named points, each with `x` and `y` coordinates. |
| `polygons` | Array[Object] | A list of named polygons, each defined by a list of vertices. |
| `query_type` | String | The specific sub-task, e.g., `quadrant_identification`, `polygon_containment`. |

**Example `metadata`:**
```json
{
  "points": [
    { "name": "A", "x": 5, "y": -3 },
    { "name": "B", "x": -2, "y": 8 }
  ],
  "query_type": "quadrant_identification"
}
```

### 2. Navigation & Pathfinding (NP)

**Description:** Tasks involving finding routes and paths in a 2D grid or graph.

| Metadata Key | Type | Description |
| :--- | :--- | :--- |
| `grid_size` | Array[Int] | The dimensions of the grid, e.g., `[10, 10]`. |
| `start_pos` | Array[Int] | The starting coordinates `[x, y]`. |
| `end_pos` | Array[Int] | The ending coordinates `[x, y]`. |
| `obstacles` | Array[Array[Int]] | A list of coordinates representing blocked cells. |
| `algorithm` | String | The algorithm to be simulated, e.g., `A*`, `manhattan`. |

**Example `metadata`:**
```json
{
  "grid_size": [20, 20],
  "start_pos": [1, 1],
  "end_pos": [18, 15],
  "obstacles": [[5, 5], [5, 6], [5, 7], [6, 7], [7, 7]],
  "algorithm": "A*"
}
```

---

*(This code book is a work in progress and will be expanded with details for all categories.)*

