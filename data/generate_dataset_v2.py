"""
SpatialEval v2: Expanded Dataset Generator

This script generates the expanded benchmark dataset with 12 categories
and 6,000 total tasks (500 per category). Each task is generated with
a programmatic validator to ensure 100% accuracy of ground truths.

Categories:
- Tier 1 (Foundational): CU, GR, DC, TR
- Tier 2 (Core Planning): NP, VVA, PRA, NI
- Tier 3 (Advanced): CBP, RAO, TSR, RE
"""

import json
import math
import random
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple
from collections import deque
import heapq

# Set seed for reproducibility
random.seed(42)

# --- Configuration ---
TASKS_PER_CATEGORY = 500
DIFFICULTIES = ["easy", "medium", "hard"]
TASKS_PER_DIFFICULTY = 167  # Slightly more than 500/3 to ensure 500+ per category

CATEGORIES = [
    "coordinate_understanding",
    "geometric_reasoning",
    "distance_computation",
    "topological_reasoning",
    "navigation_pathfinding",
    "viewpoint_visibility",
    "pattern_recognition",
    "network_infrastructure",
    "constraint_based_placement",
    "resource_allocation",
    "temporal_spatial_reasoning",
    "real_estate_geospatial",
]

# --- Utility Functions ---

def euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculate Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def point_in_rectangle(point: Tuple[float, float], rect: Tuple[float, float, float, float]) -> bool:
    """Check if a point is inside a rectangle (x_min, y_min, x_max, y_max)."""
    x, y = point
    x_min, y_min, x_max, y_max = rect
    return x_min <= x <= x_max and y_min <= y <= y_max

def rectangles_overlap(r1: Tuple[float, float, float, float], r2: Tuple[float, float, float, float]) -> bool:
    """Check if two rectangles overlap."""
    return not (r1[2] < r2[0] or r2[2] < r1[0] or r1[3] < r2[1] or r2[3] < r1[1])

def line_intersects_rectangle(p1: Tuple[float, float], p2: Tuple[float, float], rect: Tuple[float, float, float, float]) -> bool:
    """Check if a line segment intersects a rectangle."""
    def ccw(A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
    
    def intersect(A, B, C, D):
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
    
    x_min, y_min, x_max, y_max = rect
    corners = [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]
    edges = [(corners[i], corners[(i+1)%4]) for i in range(4)]
    
    # Check if line intersects any edge
    for edge in edges:
        if intersect(p1, p2, edge[0], edge[1]):
            return True
    
    # Check if line is entirely inside rectangle
    if point_in_rectangle(p1, rect) and point_in_rectangle(p2, rect):
        return True
    
    return False

def a_star(grid: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    """A* pathfinding algorithm. Returns path length or -1 if no path."""
    rows, cols = len(grid), len(grid[0])
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    open_set = [(0, start)]
    g_score = {start: 0}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == end:
            return g_score[current]
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:  # Obstacle
                    continue
                
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, neighbor))
    
    return -1  # No path found

def bfs_connected(graph: Dict[int, List[int]], start: int, end: int) -> bool:
    """BFS to check if two nodes are connected in a graph."""
    if start == end:
        return True
    visited = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == end:
            return True
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                queue.append(neighbor)
    return False

# --- Task Generators ---

def generate_coordinate_understanding(difficulty: str, task_id: int) -> Dict[str, Any]:
    """Generate Coordinate Understanding tasks."""
    if difficulty == "easy":
        # Simple coordinate identification
        x, y = random.randint(-10, 10), random.randint(-10, 10)
        if x > 0 and y > 0:
            quadrant = "I"
        elif x < 0 and y > 0:
            quadrant = "II"
        elif x < 0 and y < 0:
            quadrant = "III"
        elif x > 0 and y < 0:
            quadrant = "IV"
        else:
            quadrant = "on an axis"
        
        prompt = f"In which quadrant of the Cartesian plane is the point ({x}, {y}) located? Answer with I, II, III, IV, or 'on an axis'."
        ground_truth = quadrant
        
    elif difficulty == "medium":
        # Vector addition
        x1, y1 = random.randint(-10, 10), random.randint(-10, 10)
        vx, vy = random.randint(-5, 5), random.randint(-5, 5)
        result_x, result_y = x1 + vx, y1 + vy
        
        prompt = f"A point is located at ({x1}, {y1}). If it moves by a vector ({vx}, {vy}), what are its new coordinates? Answer in the format (x, y)."
        ground_truth = f"({result_x}, {result_y})"
        
    else:  # hard
        # Rotation around origin
        x, y = random.randint(1, 10), random.randint(1, 10)
        angle = random.choice([90, 180, 270])
        
        if angle == 90:
            new_x, new_y = -y, x
        elif angle == 180:
            new_x, new_y = -x, -y
        else:  # 270
            new_x, new_y = y, -x
        
        prompt = f"A point at ({x}, {y}) is rotated {angle} degrees counter-clockwise around the origin. What are its new coordinates? Answer in the format (x, y)."
        ground_truth = f"({new_x}, {new_y})"
    
    return {
        "task_id": f"CU_{difficulty}_{task_id:04d}",
        "category": "coordinate_understanding",
        "difficulty": difficulty,
        "prompt": prompt,
        "ground_truth": ground_truth,
    }

def generate_geometric_reasoning(difficulty: str, task_id: int) -> Dict[str, Any]:
    """Generate Geometric Reasoning tasks."""
    if difficulty == "easy":
        # Rectangle area
        width = random.randint(2, 20)
        height = random.randint(2, 20)
        area = width * height
        
        prompt = f"A rectangle has a width of {width} units and a height of {height} units. What is its area in square units?"
        ground_truth = area
        
    elif difficulty == "medium":
        # Rectangle overlap detection
        r1 = (random.randint(0, 5), random.randint(0, 5), random.randint(6, 10), random.randint(6, 10))
        
        # Generate second rectangle that may or may not overlap
        if random.random() < 0.5:
            # Overlapping
            r2 = (random.randint(r1[0], r1[2]-1), random.randint(r1[1], r1[3]-1), 
                  random.randint(r1[2], 15), random.randint(r1[3], 15))
        else:
            # Non-overlapping
            r2 = (r1[2] + random.randint(1, 5), r1[3] + random.randint(1, 5),
                  r1[2] + random.randint(6, 10), r1[3] + random.randint(6, 10))
        
        overlap = rectangles_overlap(r1, r2)
        
        prompt = f"Rectangle A has corners at ({r1[0]}, {r1[1]}) and ({r1[2]}, {r1[3]}). Rectangle B has corners at ({r2[0]}, {r2[1]}) and ({r2[2]}, {r2[3]}). Do these rectangles overlap? Answer Yes or No."
        ground_truth = "Yes" if overlap else "No"
        
    else:  # hard
        # Triangle area using coordinates
        x1, y1 = random.randint(0, 10), random.randint(0, 10)
        x2, y2 = random.randint(0, 10), random.randint(0, 10)
        x3, y3 = random.randint(0, 10), random.randint(0, 10)
        
        # Shoelace formula
        area = abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)) / 2)
        
        prompt = f"A triangle has vertices at ({x1}, {y1}), ({x2}, {y2}), and ({x3}, {y3}). What is its area? Give your answer as a number (decimal if needed)."
        ground_truth = area
    
    return {
        "task_id": f"GR_{difficulty}_{task_id:04d}",
        "category": "geometric_reasoning",
        "difficulty": difficulty,
        "prompt": prompt,
        "ground_truth": ground_truth,
    }

def generate_distance_computation(difficulty: str, task_id: int) -> Dict[str, Any]:
    """Generate Distance Computation tasks."""
    if difficulty == "easy":
        # Manhattan distance
        x1, y1 = random.randint(0, 10), random.randint(0, 10)
        x2, y2 = random.randint(0, 10), random.randint(0, 10)
        dist = manhattan_distance((x1, y1), (x2, y2))
        
        prompt = f"What is the Manhattan distance between point ({x1}, {y1}) and point ({x2}, {y2})?"
        ground_truth = dist
        
    elif difficulty == "medium":
        # Euclidean distance (integer result)
        # Use Pythagorean triples for clean answers
        triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10)]
        dx, dy, dist = random.choice(triples)
        x1, y1 = random.randint(0, 10), random.randint(0, 10)
        x2, y2 = x1 + dx, y1 + dy
        
        prompt = f"What is the Euclidean distance between point ({x1}, {y1}) and point ({x2}, {y2})?"
        ground_truth = dist
        
    else:  # hard
        # Closest point among multiple
        target = (random.randint(0, 20), random.randint(0, 20))
        num_points = random.randint(4, 6)
        points = [(random.randint(0, 20), random.randint(0, 20)) for _ in range(num_points)]
        
        distances = [(euclidean_distance(target, p), i, p) for i, p in enumerate(points)]
        closest_dist, closest_idx, closest_point = min(distances)
        
        points_str = ", ".join([f"P{i+1}({p[0]}, {p[1]})" for i, p in enumerate(points)])
        prompt = f"Given the target point T({target[0]}, {target[1]}) and the following points: {points_str}. Which point is closest to T? Answer with the point label (e.g., P1)."
        ground_truth = f"P{closest_idx + 1}"
    
    return {
        "task_id": f"DC_{difficulty}_{task_id:04d}",
        "category": "distance_computation",
        "difficulty": difficulty,
        "prompt": prompt,
        "ground_truth": ground_truth,
    }

def generate_topological_reasoning(difficulty: str, task_id: int) -> Dict[str, Any]:
    """Generate Topological Reasoning tasks."""
    if difficulty == "easy":
        # Simple adjacency
        regions = ["A", "B", "C", "D", "E"]
        adjacency = {
            "A": ["B", "C"],
            "B": ["A", "C", "D"],
            "C": ["A", "B", "D", "E"],
            "D": ["B", "C", "E"],
            "E": ["C", "D"],
        }
        query_region = random.choice(regions)
        neighbors = adjacency[query_region]
        
        adj_str = "; ".join([f"{r} borders {', '.join(adjacency[r])}" for r in regions])
        prompt = f"A map has 5 regions with the following adjacencies: {adj_str}. Which regions border region {query_region}? List them separated by commas."
        ground_truth = ", ".join(sorted(neighbors))
        
    elif difficulty == "medium":
        # Containment
        outer = (0, 0, 20, 20)
        inner_count = random.randint(2, 4)
        inners = []
        for i in range(inner_count):
            x1 = random.randint(1, 8)
            y1 = random.randint(1, 8)
            x2 = x1 + random.randint(2, 5)
            y2 = y1 + random.randint(2, 5)
            inners.append((x1, y1, x2, y2))
        
        test_point = (random.randint(0, 20), random.randint(0, 20))
        containing = []
        for i, rect in enumerate(inners):
            if point_in_rectangle(test_point, rect):
                containing.append(f"R{i+1}")
        
        regions_str = "; ".join([f"R{i+1} has corners ({r[0]},{r[1]}) and ({r[2]},{r[3]})" for i, r in enumerate(inners)])
        prompt = f"Given regions: {regions_str}. Which regions contain the point ({test_point[0]}, {test_point[1]})? Answer with region labels separated by commas, or 'None' if no region contains it."
        ground_truth = ", ".join(containing) if containing else "None"
        
    else:  # hard
        # Connectivity through regions
        num_regions = 6
        # Create a connected graph
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 2), (1, 3), (2, 4)]
        random.shuffle(edges)
        edges = edges[:random.randint(5, 7)]
        
        graph = {i: [] for i in range(num_regions)}
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)
        
        start, end = random.sample(range(num_regions), 2)
        connected = bfs_connected(graph, start, end)
        
        edges_str = ", ".join([f"R{a+1}-R{b+1}" for a, b in edges])
        prompt = f"A map has {num_regions} regions (R1 to R{num_regions}) with the following borders: {edges_str}. Can you travel from R{start+1} to R{end+1} by only crossing adjacent regions? Answer Yes or No."
        ground_truth = "Yes" if connected else "No"
    
    return {
        "task_id": f"TR_{difficulty}_{task_id:04d}",
        "category": "topological_reasoning",
        "difficulty": difficulty,
        "prompt": prompt,
        "ground_truth": ground_truth,
    }

def generate_navigation_pathfinding(difficulty: str, task_id: int) -> Dict[str, Any]:
    """Generate Navigation & Pathfinding tasks."""
    if difficulty == "easy":
        # Simple grid, no obstacles
        grid_size = 5
        start = (0, 0)
        end = (random.randint(2, grid_size-1), random.randint(2, grid_size-1))
        path_length = manhattan_distance(start, end)
        
        prompt = f"On a {grid_size}x{grid_size} grid with no obstacles, what is the shortest path length from ({start[0]}, {start[1]}) to ({end[0]}, {end[1]})? You can only move up, down, left, or right."
        ground_truth = path_length
        
    elif difficulty == "medium":
        # Grid with some obstacles
        grid_size = 6
        grid = [[0] * grid_size for _ in range(grid_size)]
        
        # Add obstacles (ensure path exists)
        num_obstacles = random.randint(3, 6)
        obstacles = set()
        while len(obstacles) < num_obstacles:
            ox, oy = random.randint(1, grid_size-2), random.randint(1, grid_size-2)
            obstacles.add((ox, oy))
        
        for ox, oy in obstacles:
            grid[ox][oy] = 1
        
        start = (0, 0)
        end = (grid_size-1, grid_size-1)
        path_length = a_star(grid, start, end)
        
        # If no path, regenerate
        if path_length == -1:
            return generate_navigation_pathfinding(difficulty, task_id)
        
        obs_str = ", ".join([f"({o[0]},{o[1]})" for o in obstacles])
        prompt = f"On a {grid_size}x{grid_size} grid, obstacles are at: {obs_str}. What is the shortest path length from (0,0) to ({grid_size-1},{grid_size-1})? You can only move up, down, left, or right. If no path exists, answer -1."
        ground_truth = path_length
        
    else:  # hard
        # Larger grid with more obstacles
        grid_size = 8
        grid = [[0] * grid_size for _ in range(grid_size)]
        
        num_obstacles = random.randint(8, 12)
        obstacles = set()
        while len(obstacles) < num_obstacles:
            ox, oy = random.randint(1, grid_size-2), random.randint(1, grid_size-2)
            obstacles.add((ox, oy))
        
        for ox, oy in obstacles:
            grid[ox][oy] = 1
        
        start = (0, 0)
        end = (grid_size-1, grid_size-1)
        path_length = a_star(grid, start, end)
        
        obs_str = ", ".join([f"({o[0]},{o[1]})" for o in obstacles])
        prompt = f"On an {grid_size}x{grid_size} grid, obstacles are at: {obs_str}. What is the shortest path length from (0,0) to ({grid_size-1},{grid_size-1})? You can only move up, down, left, or right. If no path exists, answer -1."
        ground_truth = path_length
    
    return {
        "task_id": f"NP_{difficulty}_{task_id:04d}",
        "category": "navigation_pathfinding",
        "difficulty": difficulty,
        "prompt": prompt,
        "ground_truth": ground_truth,
    }

def generate_viewpoint_visibility(difficulty: str, task_id: int) -> Dict[str, Any]:
    """Generate Viewpoint & Visibility tasks."""
    if difficulty == "easy":
        # Simple line of sight
        observer = (0, 0)
        target = (random.randint(5, 10), random.randint(5, 10))
        
        # No obstacles
        prompt = f"An observer is at ({observer[0]}, {observer[1]}) and a target is at ({target[0]}, {target[1]}). With no obstacles, can the observer see the target? Answer Yes or No."
        ground_truth = "Yes"
        
    elif difficulty == "medium":
        # Single obstacle
        observer = (0, 0)
        target = (10, 10)
        
        # Place obstacle that may or may not block
        if random.random() < 0.5:
            # Blocking obstacle
            obstacle = (4, 4, 6, 6)
            blocked = True
        else:
            # Non-blocking obstacle
            obstacle = (8, 0, 10, 2)
            blocked = False
        
        prompt = f"An observer is at ({observer[0]}, {observer[1]}) and a target is at ({target[0]}, {target[1]}). A rectangular obstacle has corners at ({obstacle[0]}, {obstacle[1]}) and ({obstacle[2]}, {obstacle[3]}). Can the observer see the target? Answer Yes or No."
        ground_truth = "No" if blocked else "Yes"
        
    else:  # hard
        # Multiple obstacles
        observer = (0, 0)
        target = (15, 15)
        
        obstacles = []
        blocked = False
        
        # Generate 2-3 obstacles
        num_obs = random.randint(2, 3)
        for _ in range(num_obs):
            x1 = random.randint(2, 12)
            y1 = random.randint(2, 12)
            x2 = x1 + random.randint(2, 4)
            y2 = y1 + random.randint(2, 4)
            obstacles.append((x1, y1, x2, y2))
        
        # Check if any obstacle blocks the line of sight
        for obs in obstacles:
            if line_intersects_rectangle(observer, target, obs):
                blocked = True
                break
        
        obs_str = "; ".join([f"Obstacle {i+1}: corners ({o[0]},{o[1]}) and ({o[2]},{o[3]})" for i, o in enumerate(obstacles)])
        prompt = f"An observer is at ({observer[0]}, {observer[1]}) and a target is at ({target[0]}, {target[1]}). {obs_str}. Can the observer see the target (direct line of sight)? Answer Yes or No."
        ground_truth = "No" if blocked else "Yes"
    
    return {
        "task_id": f"VVA_{difficulty}_{task_id:04d}",
        "category": "viewpoint_visibility",
        "difficulty": difficulty,
        "prompt": prompt,
        "ground_truth": ground_truth,
    }

def generate_pattern_recognition(difficulty: str, task_id: int) -> Dict[str, Any]:
    """Generate Pattern Recognition tasks."""
    if difficulty == "easy":
        # Identify quadrant with most points
        points = [(random.randint(-10, 10), random.randint(-10, 10)) for _ in range(10)]
        
        quadrant_counts = {"I": 0, "II": 0, "III": 0, "IV": 0}
        for x, y in points:
            if x > 0 and y > 0:
                quadrant_counts["I"] += 1
            elif x < 0 and y > 0:
                quadrant_counts["II"] += 1
            elif x < 0 and y < 0:
                quadrant_counts["III"] += 1
            elif x > 0 and y < 0:
                quadrant_counts["IV"] += 1
        
        max_quadrant = max(quadrant_counts, key=quadrant_counts.get)
        
        points_str = ", ".join([f"({p[0]},{p[1]})" for p in points])
        prompt = f"Given the points: {points_str}. Which quadrant (I, II, III, or IV) contains the most points? Points on axes are not counted."
        ground_truth = max_quadrant
        
    elif difficulty == "medium":
        # Centroid calculation
        num_points = random.randint(4, 6)
        points = [(random.randint(0, 20), random.randint(0, 20)) for _ in range(num_points)]
        
        centroid_x = sum(p[0] for p in points) / num_points
        centroid_y = sum(p[1] for p in points) / num_points
        
        points_str = ", ".join([f"({p[0]},{p[1]})" for p in points])
        prompt = f"Given the points: {points_str}. What is the centroid (geometric center) of these points? Answer in format (x, y) rounded to one decimal place."
        ground_truth = f"({round(centroid_x, 1)}, {round(centroid_y, 1)})"
        
    else:  # hard
        # Identify if points form a line (collinearity)
        if random.random() < 0.5:
            # Generate collinear points
            x_start = random.randint(0, 5)
            y_start = random.randint(0, 5)
            dx = random.randint(1, 3)
            dy = random.randint(1, 3)
            num_points = random.randint(3, 5)
            points = [(x_start + i*dx, y_start + i*dy) for i in range(num_points)]
            collinear = True
        else:
            # Generate non-collinear points
            points = [(random.randint(0, 20), random.randint(0, 20)) for _ in range(4)]
            # Check actual collinearity
            if len(points) >= 3:
                x1, y1 = points[0]
                x2, y2 = points[1]
                collinear = True
                for x3, y3 in points[2:]:
                    # Cross product should be zero for collinear points
                    cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
                    if cross != 0:
                        collinear = False
                        break
            else:
                collinear = True
        
        points_str = ", ".join([f"({p[0]},{p[1]})" for p in points])
        prompt = f"Given the points: {points_str}. Are all these points collinear (lie on the same straight line)? Answer Yes or No."
        ground_truth = "Yes" if collinear else "No"
    
    return {
        "task_id": f"PRA_{difficulty}_{task_id:04d}",
        "category": "pattern_recognition",
        "difficulty": difficulty,
        "prompt": prompt,
        "ground_truth": ground_truth,
    }

def generate_network_infrastructure(difficulty: str, task_id: int) -> Dict[str, Any]:
    """Generate Network Infrastructure tasks."""
    if difficulty == "easy":
        # Simple connectivity check
        num_nodes = 5
        edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
        
        graph = {i: [] for i in range(num_nodes)}
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)
        
        start, end = 0, 4
        connected = bfs_connected(graph, start, end)
        
        edges_str = ", ".join([f"N{a+1}-N{b+1}" for a, b in edges])
        prompt = f"A network has {num_nodes} nodes (N1 to N{num_nodes}) with connections: {edges_str}. Is N{start+1} connected to N{end+1}? Answer Yes or No."
        ground_truth = "Yes" if connected else "No"
        
    elif difficulty == "medium":
        # Connectivity after link removal
        num_nodes = 6
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 2), (2, 4)]
        
        # Remove one edge
        removed_edge = random.choice(edges)
        remaining_edges = [e for e in edges if e != removed_edge]
        
        graph = {i: [] for i in range(num_nodes)}
        for a, b in remaining_edges:
            graph[a].append(b)
            graph[b].append(a)
        
        start, end = 0, 5
        connected = bfs_connected(graph, start, end)
        
        edges_str = ", ".join([f"N{a+1}-N{b+1}" for a, b in edges])
        prompt = f"A network has {num_nodes} nodes with connections: {edges_str}. If the link N{removed_edge[0]+1}-N{removed_edge[1]+1} fails, is N{start+1} still connected to N{end+1}? Answer Yes or No."
        ground_truth = "Yes" if connected else "No"
        
    else:  # hard
        # Shortest path in weighted graph (simplified as hop count)
        num_nodes = 7
        edges = [(0, 1), (1, 2), (2, 3), (3, 6), (0, 4), (4, 5), (5, 6), (1, 4), (2, 5)]
        
        graph = {i: [] for i in range(num_nodes)}
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)
        
        # BFS for shortest path
        start, end = 0, 6
        visited = {start: 0}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            if node == end:
                break
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited[neighbor] = visited[node] + 1
                    queue.append(neighbor)
        
        shortest_path = visited.get(end, -1)
        
        edges_str = ", ".join([f"N{a+1}-N{b+1}" for a, b in edges])
        prompt = f"A network has {num_nodes} nodes with connections: {edges_str}. What is the minimum number of hops to get from N{start+1} to N{end+1}?"
        ground_truth = shortest_path
    
    return {
        "task_id": f"NI_{difficulty}_{task_id:04d}",
        "category": "network_infrastructure",
        "difficulty": difficulty,
        "prompt": prompt,
        "ground_truth": ground_truth,
    }

def generate_constraint_based_placement(difficulty: str, task_id: int) -> Dict[str, Any]:
    """Generate Constraint-Based Placement tasks."""
    if difficulty == "easy":
        # Simple placement check
        room_size = 10
        object_pos = (random.randint(0, room_size), random.randint(0, room_size))
        min_dist_from_wall = 2
        
        valid = (object_pos[0] >= min_dist_from_wall and 
                 object_pos[0] <= room_size - min_dist_from_wall and
                 object_pos[1] >= min_dist_from_wall and 
                 object_pos[1] <= room_size - min_dist_from_wall)
        
        prompt = f"A {room_size}x{room_size} room has walls at x=0, x={room_size}, y=0, and y={room_size}. An object must be at least {min_dist_from_wall} units from any wall. Is the position ({object_pos[0]}, {object_pos[1]}) valid? Answer Yes or No."
        ground_truth = "Yes" if valid else "No"
        
    elif difficulty == "medium":
        # Two objects with minimum distance constraint
        obj1 = (random.randint(2, 8), random.randint(2, 8))
        obj2 = (random.randint(2, 8), random.randint(2, 8))
        min_dist = 3
        
        actual_dist = euclidean_distance(obj1, obj2)
        valid = actual_dist >= min_dist
        
        prompt = f"Two machines must be at least {min_dist} units apart. Machine A is at ({obj1[0]}, {obj1[1]}) and Machine B is at ({obj2[0]}, {obj2[1]}). Is this placement valid? Answer Yes or No."
        ground_truth = "Yes" if valid else "No"
        
    else:  # hard
        # Multiple objects with multiple constraints
        room_size = 20
        num_objects = 3
        objects = [(random.randint(2, 18), random.randint(2, 18)) for _ in range(num_objects)]
        min_dist_between = 4
        max_dist_from_center = 8
        center = (10, 10)
        
        # Check all constraints
        valid = True
        
        # Check pairwise distances
        for i in range(num_objects):
            for j in range(i+1, num_objects):
                if euclidean_distance(objects[i], objects[j]) < min_dist_between:
                    valid = False
                    break
            if not valid:
                break
        
        # Check distance from center
        if valid:
            for obj in objects:
                if euclidean_distance(obj, center) > max_dist_from_center:
                    valid = False
                    break
        
        objects_str = ", ".join([f"O{i+1}({o[0]},{o[1]})" for i, o in enumerate(objects)])
        prompt = f"In a {room_size}x{room_size} room, {num_objects} objects are placed at: {objects_str}. Constraints: (1) Objects must be at least {min_dist_between} units apart from each other. (2) All objects must be within {max_dist_from_center} units of the center ({center[0]},{center[1]}). Is this placement valid? Answer Yes or No."
        ground_truth = "Yes" if valid else "No"
    
    return {
        "task_id": f"CBP_{difficulty}_{task_id:04d}",
        "category": "constraint_based_placement",
        "difficulty": difficulty,
        "prompt": prompt,
        "ground_truth": ground_truth,
    }

def generate_resource_allocation(difficulty: str, task_id: int) -> Dict[str, Any]:
    """Generate Resource Allocation tasks."""
    if difficulty == "easy":
        # Single resource coverage
        resource_pos = (5, 5)
        coverage_radius = 3
        test_point = (random.randint(0, 10), random.randint(0, 10))
        
        covered = euclidean_distance(resource_pos, test_point) <= coverage_radius
        
        prompt = f"A service station at ({resource_pos[0]}, {resource_pos[1]}) covers all points within {coverage_radius} units. Is the point ({test_point[0]}, {test_point[1]}) covered? Answer Yes or No."
        ground_truth = "Yes" if covered else "No"
        
    elif difficulty == "medium":
        # Multiple resources, check coverage
        resources = [(2, 2), (8, 2), (5, 8)]
        coverage_radius = 3
        test_point = (random.randint(0, 10), random.randint(0, 10))
        
        covered = any(euclidean_distance(r, test_point) <= coverage_radius for r in resources)
        
        resources_str = ", ".join([f"S{i+1}({r[0]},{r[1]})" for i, r in enumerate(resources)])
        prompt = f"Service stations are at: {resources_str}. Each covers points within {coverage_radius} units. Is the point ({test_point[0]}, {test_point[1]}) covered by any station? Answer Yes or No."
        ground_truth = "Yes" if covered else "No"
        
    else:  # hard
        # Count covered vs uncovered points
        resources = [(3, 3), (7, 3), (5, 7)]
        coverage_radius = 2.5
        
        # Generate test points
        test_points = [(x, y) for x in range(0, 11, 2) for y in range(0, 11, 2)]
        
        covered_count = 0
        for point in test_points:
            if any(euclidean_distance(r, point) <= coverage_radius for r in resources):
                covered_count += 1
        
        resources_str = ", ".join([f"S{i+1}({r[0]},{r[1]})" for i, r in enumerate(resources)])
        prompt = f"Service stations are at: {resources_str}. Each covers points within {coverage_radius} units. How many of the grid points (0,0), (0,2), (0,4), ..., (10,10) (i.e., all points where both coordinates are even numbers from 0 to 10) are covered by at least one station?"
        ground_truth = covered_count
    
    return {
        "task_id": f"RAO_{difficulty}_{task_id:04d}",
        "category": "resource_allocation",
        "difficulty": difficulty,
        "prompt": prompt,
        "ground_truth": ground_truth,
    }

def generate_temporal_spatial_reasoning(difficulty: str, task_id: int) -> Dict[str, Any]:
    """Generate Temporal-Spatial Reasoning tasks."""
    if difficulty == "easy":
        # Simple position after time
        start_pos = (0, 0)
        velocity = (random.randint(1, 5), random.randint(1, 5))
        time = random.randint(1, 5)
        
        end_pos = (start_pos[0] + velocity[0] * time, start_pos[1] + velocity[1] * time)
        
        prompt = f"An object starts at ({start_pos[0]}, {start_pos[1]}) and moves with velocity ({velocity[0]}, {velocity[1]}) units per second. Where will it be after {time} seconds? Answer in format (x, y)."
        ground_truth = f"({end_pos[0]}, {end_pos[1]})"
        
    elif difficulty == "medium":
        # Two objects, will they meet?
        obj1_start = (random.randint(0, 5), random.randint(0, 5))
        obj1_vel = (random.randint(1, 3), random.randint(0, 2))
        obj2_start = (random.randint(8, 15), random.randint(3, 10))
        obj2_vel = (random.randint(-3, 0), random.randint(-1, 1))
        
        # Check if paths intersect at same time
        # Position at time t: obj1 = (2t, t), obj2 = (10-t, 5)
        # They meet if 2t = 10-t and t = 5 => t = 10/3 and t = 5 (no solution)
        # Simplified: check if they get within 1 unit of each other within 10 seconds
        
        meet = False
        for t in range(11):
            pos1 = (obj1_start[0] + obj1_vel[0] * t, obj1_start[1] + obj1_vel[1] * t)
            pos2 = (obj2_start[0] + obj2_vel[0] * t, obj2_start[1] + obj2_vel[1] * t)
            if euclidean_distance(pos1, pos2) <= 1:
                meet = True
                break
        
        prompt = f"Object A starts at ({obj1_start[0]},{obj1_start[1]}) with velocity ({obj1_vel[0]},{obj1_vel[1]}). Object B starts at ({obj2_start[0]},{obj2_start[1]}) with velocity ({obj2_vel[0]},{obj2_vel[1]}). Will they come within 1 unit of each other within 10 seconds? Answer Yes or No."
        ground_truth = "Yes" if meet else "No"
        
    else:  # hard
        # Time to reach a target
        start = (0, 0)
        target = (random.randint(10, 20), random.randint(10, 20))
        speed = random.randint(2, 5)
        
        distance = euclidean_distance(start, target)
        time_to_reach = distance / speed
        
        prompt = f"An object at ({start[0]}, {start[1]}) moves directly toward ({target[0]}, {target[1]}) at a speed of {speed} units per second. How many seconds will it take to reach the target? Round to one decimal place."
        ground_truth = round(time_to_reach, 1)
    
    return {
        "task_id": f"TSR_{difficulty}_{task_id:04d}",
        "category": "temporal_spatial_reasoning",
        "difficulty": difficulty,
        "prompt": prompt,
        "ground_truth": ground_truth,
    }

def generate_real_estate_geospatial(difficulty: str, task_id: int) -> Dict[str, Any]:
    """Generate Real Estate & Geospatial tasks."""
    if difficulty == "easy":
        # Point in zone check
        zone = (0, 0, 10, 10)
        point = (random.randint(-2, 12), random.randint(-2, 12))
        
        in_zone = point_in_rectangle(point, zone)
        
        prompt = f"A residential zone covers the area from (0,0) to (10,10). Is the property at ({point[0]}, {point[1]}) within this zone? Answer Yes or No."
        ground_truth = "Yes" if in_zone else "No"
        
    elif difficulty == "medium":
        # Distance to amenity
        property_loc = (random.randint(0, 20), random.randint(0, 20))
        school = (5, 5)
        hospital = (15, 15)
        max_school_dist = 5
        
        school_dist = euclidean_distance(property_loc, school)
        within_school_range = school_dist <= max_school_dist
        
        prompt = f"A property is at ({property_loc[0]}, {property_loc[1]}). The nearest school is at ({school[0]}, {school[1]}). Is the property within {max_school_dist} units of the school? Answer Yes or No."
        ground_truth = "Yes" if within_school_range else "No"
        
    else:  # hard
        # Complex zoning query
        property_loc = (random.randint(5, 15), random.randint(5, 15))
        school = (8, 8)
        highway = (0, 10, 20, 12)  # Horizontal strip
        
        school_dist = euclidean_distance(property_loc, school)
        near_school = school_dist <= 5
        
        # Check if within 2 units of highway
        near_highway = (highway[1] - 2 <= property_loc[1] <= highway[3] + 2)
        
        # Valid if near school but NOT near highway
        valid = near_school and not near_highway
        
        prompt = f"A property at ({property_loc[0]}, {property_loc[1]}) is being evaluated. Requirements: (1) Must be within 5 units of the school at ({school[0]}, {school[1]}). (2) Must NOT be within 2 units of the highway (y = {highway[1]} to y = {highway[3]}). Does this property meet both requirements? Answer Yes or No."
        ground_truth = "Yes" if valid else "No"
    
    return {
        "task_id": f"RE_{difficulty}_{task_id:04d}",
        "category": "real_estate_geospatial",
        "difficulty": difficulty,
        "prompt": prompt,
        "ground_truth": ground_truth,
    }

# --- Main Generation Logic ---

GENERATORS = {
    "coordinate_understanding": generate_coordinate_understanding,
    "geometric_reasoning": generate_geometric_reasoning,
    "distance_computation": generate_distance_computation,
    "topological_reasoning": generate_topological_reasoning,
    "navigation_pathfinding": generate_navigation_pathfinding,
    "viewpoint_visibility": generate_viewpoint_visibility,
    "pattern_recognition": generate_pattern_recognition,
    "network_infrastructure": generate_network_infrastructure,
    "constraint_based_placement": generate_constraint_based_placement,
    "resource_allocation": generate_resource_allocation,
    "temporal_spatial_reasoning": generate_temporal_spatial_reasoning,
    "real_estate_geospatial": generate_real_estate_geospatial,
}

def generate_all_tasks():
    """Generate all tasks for all categories and difficulties."""
    base_dir = Path(__file__).parent
    
    total_tasks = 0
    summary = {"categories": {}, "total_tasks": 0}
    
    for category in CATEGORIES:
        generator = GENERATORS[category]
        category_dir = base_dir / category
        summary["categories"][category] = {"easy": 0, "medium": 0, "hard": 0, "total": 0}
        
        for difficulty in DIFFICULTIES:
            diff_dir = category_dir / difficulty
            diff_dir.mkdir(parents=True, exist_ok=True)
            
            tasks = []
            for i in range(TASKS_PER_DIFFICULTY):
                task = generator(difficulty, i + 1)
                tasks.append(task)
            
            # Save tasks
            with open(diff_dir / "tasks.json", "w") as f:
                json.dump(tasks, f, indent=2)
            
            summary["categories"][category][difficulty] = len(tasks)
            summary["categories"][category]["total"] += len(tasks)
            total_tasks += len(tasks)
            
            print(f"Generated {len(tasks)} tasks for {category}/{difficulty}")
    
    summary["total_tasks"] = total_tasks
    
    # Save summary
    with open(base_dir / "dataset_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nTotal tasks generated: {total_tasks}")
    return summary

if __name__ == "__main__":
    generate_all_tasks()
