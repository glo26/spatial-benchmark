#!/usr/bin/env python3
"""
SpatialEval Benchmark Dataset Generator
Generates 2,250 tasks across 6 categories and 3 difficulty levels.
"""

import json
import random
import math
import os
from typing import Dict, List, Any

random.seed(42)  # For reproducibility

# Task distribution: 375 tasks per category, 125 per difficulty level
TASKS_PER_CATEGORY = 375
TASKS_PER_DIFFICULTY = 125

def generate_coordinate_understanding_tasks() -> Dict[str, List[Dict]]:
    """Generate Coordinate Understanding (CU) tasks."""
    tasks = {"easy": [], "medium": [], "hard": []}
    
    # Easy: Basic coordinate identification and quadrant determination
    for i in range(TASKS_PER_DIFFICULTY):
        x, y = random.randint(-100, 100), random.randint(-100, 100)
        quadrant = 1 if x > 0 and y > 0 else 2 if x < 0 and y > 0 else 3 if x < 0 and y < 0 else 4
        tasks["easy"].append({
            "id": f"CU-E-{i+1:03d}",
            "category": "coordinate_understanding",
            "difficulty": "easy",
            "task_type": "quadrant_identification",
            "question": f"Given the point ({x}, {y}) in a Cartesian coordinate system, which quadrant does this point lie in?",
            "answer": quadrant,
            "reasoning_steps": 2
        })
    
    # Medium: Coordinate transformations and GPS conversions
    for i in range(TASKS_PER_DIFFICULTY):
        lat = round(random.uniform(25.0, 49.0), 6)
        lon = round(random.uniform(-125.0, -67.0), 6)
        offset_lat = round(random.uniform(-0.01, 0.01), 6)
        offset_lon = round(random.uniform(-0.01, 0.01), 6)
        new_lat = round(lat + offset_lat, 6)
        new_lon = round(lon + offset_lon, 6)
        tasks["medium"].append({
            "id": f"CU-M-{i+1:03d}",
            "category": "coordinate_understanding",
            "difficulty": "medium",
            "task_type": "gps_transformation",
            "question": f"A GPS coordinate is located at ({lat}, {lon}). If we apply an offset of ({offset_lat}, {offset_lon}), what are the new coordinates?",
            "answer": {"latitude": new_lat, "longitude": new_lon},
            "reasoning_steps": 3
        })
    
    # Hard: Multi-step coordinate reasoning with polygon containment
    for i in range(TASKS_PER_DIFFICULTY):
        # Generate a simple polygon (rectangle)
        x1, y1 = random.randint(0, 50), random.randint(0, 50)
        x2, y2 = x1 + random.randint(10, 50), y1 + random.randint(10, 50)
        # Generate test point
        px, py = random.randint(0, 100), random.randint(0, 100)
        inside = x1 <= px <= x2 and y1 <= py <= y2
        tasks["hard"].append({
            "id": f"CU-H-{i+1:03d}",
            "category": "coordinate_understanding",
            "difficulty": "hard",
            "task_type": "polygon_containment",
            "question": f"A rectangular region is defined by corners ({x1}, {y1}) and ({x2}, {y2}). Is the point ({px}, {py}) inside this region?",
            "polygon": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
            "test_point": {"x": px, "y": py},
            "answer": inside,
            "reasoning_steps": 5
        })
    
    return tasks


def generate_navigation_pathfinding_tasks() -> Dict[str, List[Dict]]:
    """Generate Navigation & Pathfinding (NP) tasks."""
    tasks = {"easy": [], "medium": [], "hard": []}
    
    # Easy: Simple direction following
    directions = ["north", "south", "east", "west"]
    for i in range(TASKS_PER_DIFFICULTY):
        start_x, start_y = random.randint(0, 10), random.randint(0, 10)
        steps = []
        x, y = start_x, start_y
        for _ in range(random.randint(2, 4)):
            d = random.choice(directions)
            dist = random.randint(1, 5)
            steps.append({"direction": d, "distance": dist})
            if d == "north": y += dist
            elif d == "south": y -= dist
            elif d == "east": x += dist
            elif d == "west": x -= dist
        
        tasks["easy"].append({
            "id": f"NP-E-{i+1:03d}",
            "category": "navigation_pathfinding",
            "difficulty": "easy",
            "task_type": "direction_following",
            "question": f"Starting at position ({start_x}, {start_y}), follow these directions: {steps}. What is the final position?",
            "start": {"x": start_x, "y": start_y},
            "steps": steps,
            "answer": {"x": x, "y": y},
            "reasoning_steps": len(steps) + 1
        })
    
    # Medium: Shortest path in a simple grid
    for i in range(TASKS_PER_DIFFICULTY):
        start = (random.randint(0, 5), random.randint(0, 5))
        end = (random.randint(5, 10), random.randint(5, 10))
        manhattan_dist = abs(end[0] - start[0]) + abs(end[1] - start[1])
        tasks["medium"].append({
            "id": f"NP-M-{i+1:03d}",
            "category": "navigation_pathfinding",
            "difficulty": "medium",
            "task_type": "shortest_path_manhattan",
            "question": f"In a grid where you can only move horizontally or vertically, what is the shortest path length from {start} to {end}?",
            "start": start,
            "end": end,
            "answer": manhattan_dist,
            "reasoning_steps": 4
        })
    
    # Hard: A* pathfinding with obstacles
    for i in range(TASKS_PER_DIFFICULTY):
        grid_size = 10
        start = (0, 0)
        end = (grid_size - 1, grid_size - 1)
        # Generate some obstacles
        num_obstacles = random.randint(5, 15)
        obstacles = set()
        while len(obstacles) < num_obstacles:
            obs = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
            if obs != start and obs != end:
                obstacles.add(obs)
        
        # Simple BFS to find path length
        from collections import deque
        queue = deque([(start, 0)])
        visited = {start}
        path_length = -1
        while queue:
            (cx, cy), dist = queue.popleft()
            if (cx, cy) == end:
                path_length = dist
                break
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size and (nx, ny) not in visited and (nx, ny) not in obstacles:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), dist + 1))
        
        tasks["hard"].append({
            "id": f"NP-H-{i+1:03d}",
            "category": "navigation_pathfinding",
            "difficulty": "hard",
            "task_type": "astar_pathfinding",
            "question": f"In a {grid_size}x{grid_size} grid with obstacles at {list(obstacles)}, find the shortest path length from {start} to {end} using only horizontal and vertical moves.",
            "grid_size": grid_size,
            "start": start,
            "end": end,
            "obstacles": list(obstacles),
            "answer": path_length,
            "reasoning_steps": 8
        })
    
    return tasks


def generate_real_estate_tasks() -> Dict[str, List[Dict]]:
    """Generate Real Estate Spatial Analysis (RE) tasks."""
    tasks = {"easy": [], "medium": [], "hard": []}
    
    # Easy: Property area calculation
    for i in range(TASKS_PER_DIFFICULTY):
        width = random.randint(50, 200)
        length = random.randint(50, 200)
        area = width * length
        tasks["easy"].append({
            "id": f"RE-E-{i+1:03d}",
            "category": "real_estate",
            "difficulty": "easy",
            "task_type": "area_calculation",
            "question": f"A rectangular property has dimensions {width} ft x {length} ft. What is the total area in square feet?",
            "dimensions": {"width": width, "length": length},
            "answer": area,
            "reasoning_steps": 2
        })
    
    # Medium: Proximity analysis
    property_types = ["school", "hospital", "park", "shopping center", "fire station"]
    for i in range(TASKS_PER_DIFFICULTY):
        property_loc = (round(random.uniform(0, 10), 2), round(random.uniform(0, 10), 2))
        amenities = []
        for pt in property_types:
            loc = (round(random.uniform(0, 10), 2), round(random.uniform(0, 10), 2))
            dist = round(math.sqrt((property_loc[0] - loc[0])**2 + (property_loc[1] - loc[1])**2), 2)
            amenities.append({"type": pt, "location": loc, "distance": dist})
        
        closest = min(amenities, key=lambda x: x["distance"])
        tasks["medium"].append({
            "id": f"RE-M-{i+1:03d}",
            "category": "real_estate",
            "difficulty": "medium",
            "task_type": "proximity_analysis",
            "question": f"A property is located at {property_loc}. Given the following amenities: {[(a['type'], a['location']) for a in amenities]}, which amenity is closest to the property?",
            "property_location": property_loc,
            "amenities": amenities,
            "answer": closest["type"],
            "reasoning_steps": 6
        })
    
    # Hard: Zoning compliance with multiple constraints
    for i in range(TASKS_PER_DIFFICULTY):
        lot_size = random.randint(5000, 20000)
        setback_front = random.randint(20, 40)
        setback_side = random.randint(5, 15)
        max_coverage = random.uniform(0.3, 0.6)
        proposed_building = {
            "width": random.randint(30, 80),
            "length": random.randint(40, 100),
            "front_setback": random.randint(15, 45),
            "side_setback": random.randint(3, 20)
        }
        building_area = proposed_building["width"] * proposed_building["length"]
        coverage = building_area / lot_size
        
        compliant = (proposed_building["front_setback"] >= setback_front and 
                    proposed_building["side_setback"] >= setback_side and 
                    coverage <= max_coverage)
        
        tasks["hard"].append({
            "id": f"RE-H-{i+1:03d}",
            "category": "real_estate",
            "difficulty": "hard",
            "task_type": "zoning_compliance",
            "question": f"A lot of {lot_size} sq ft has zoning requirements: front setback {setback_front} ft, side setback {setback_side} ft, max coverage {max_coverage:.0%}. A proposed building is {proposed_building['width']}x{proposed_building['length']} ft with {proposed_building['front_setback']} ft front setback and {proposed_building['side_setback']} ft side setback. Is this compliant?",
            "lot_size": lot_size,
            "zoning": {"front_setback": setback_front, "side_setback": setback_side, "max_coverage": max_coverage},
            "proposed_building": proposed_building,
            "answer": compliant,
            "reasoning_steps": 7
        })
    
    return tasks


def generate_network_infrastructure_tasks() -> Dict[str, List[Dict]]:
    """Generate Network Infrastructure (NI) tasks."""
    tasks = {"easy": [], "medium": [], "hard": []}
    
    # Easy: Cable length calculation
    for i in range(TASKS_PER_DIFFICULTY):
        segments = []
        total_length = 0
        for _ in range(random.randint(3, 6)):
            length = random.randint(100, 1000)
            segments.append(length)
            total_length += length
        
        tasks["easy"].append({
            "id": f"NI-E-{i+1:03d}",
            "category": "network_infrastructure",
            "difficulty": "easy",
            "task_type": "cable_length",
            "question": f"A fiber route has the following segment lengths (in feet): {segments}. What is the total cable length needed?",
            "segments": segments,
            "answer": total_length,
            "reasoning_steps": len(segments)
        })
    
    # Medium: Network topology analysis
    for i in range(TASKS_PER_DIFFICULTY):
        num_nodes = random.randint(5, 10)
        edges = []
        # Create a connected graph
        for j in range(1, num_nodes):
            parent = random.randint(0, j-1)
            edges.append((parent, j))
        # Add some extra edges
        for _ in range(random.randint(1, 3)):
            a, b = random.randint(0, num_nodes-1), random.randint(0, num_nodes-1)
            if a != b and (a, b) not in edges and (b, a) not in edges:
                edges.append((a, b))
        
        # Find node with most connections
        degree = [0] * num_nodes
        for a, b in edges:
            degree[a] += 1
            degree[b] += 1
        max_degree_node = degree.index(max(degree))
        
        tasks["medium"].append({
            "id": f"NI-M-{i+1:03d}",
            "category": "network_infrastructure",
            "difficulty": "medium",
            "task_type": "topology_analysis",
            "question": f"In a network with {num_nodes} nodes and edges {edges}, which node has the most connections?",
            "num_nodes": num_nodes,
            "edges": edges,
            "answer": max_degree_node,
            "reasoning_steps": 5
        })
    
    # Hard: Failure cascade analysis
    for i in range(TASKS_PER_DIFFICULTY):
        num_nodes = random.randint(8, 15)
        # Create a tree structure (each node except root has one parent)
        parents = [-1] + [random.randint(0, j-1) for j in range(1, num_nodes)]
        customers = [random.randint(10, 100) for _ in range(num_nodes)]
        
        # Calculate customers affected if a node fails (all descendants)
        def count_affected(node):
            total = customers[node]
            for j in range(num_nodes):
                if parents[j] == node:
                    total += count_affected(j)
            return total
        
        failed_node = random.randint(1, num_nodes - 1)
        affected = count_affected(failed_node)
        
        tasks["hard"].append({
            "id": f"NI-H-{i+1:03d}",
            "category": "network_infrastructure",
            "difficulty": "hard",
            "task_type": "failure_cascade",
            "question": f"In a network tree with {num_nodes} nodes, parent relationships {list(enumerate(parents))}, and customer counts {list(enumerate(customers))}, how many customers are affected if node {failed_node} fails?",
            "num_nodes": num_nodes,
            "parents": parents,
            "customers": customers,
            "failed_node": failed_node,
            "answer": affected,
            "reasoning_steps": 10
        })
    
    return tasks


def generate_geometric_reasoning_tasks() -> Dict[str, List[Dict]]:
    """Generate Geometric Reasoning (GR) tasks."""
    tasks = {"easy": [], "medium": [], "hard": []}
    
    # Easy: Basic shape properties
    shapes = ["circle", "square", "rectangle", "triangle"]
    for i in range(TASKS_PER_DIFFICULTY):
        shape = random.choice(shapes)
        if shape == "circle":
            radius = random.randint(1, 20)
            area = round(math.pi * radius ** 2, 2)
            question = f"What is the area of a circle with radius {radius}?"
            params = {"radius": radius}
        elif shape == "square":
            side = random.randint(1, 20)
            area = side ** 2
            question = f"What is the area of a square with side length {side}?"
            params = {"side": side}
        elif shape == "rectangle":
            width, height = random.randint(1, 20), random.randint(1, 20)
            area = width * height
            question = f"What is the area of a rectangle with width {width} and height {height}?"
            params = {"width": width, "height": height}
        else:  # triangle
            base, height = random.randint(1, 20), random.randint(1, 20)
            area = 0.5 * base * height
            question = f"What is the area of a triangle with base {base} and height {height}?"
            params = {"base": base, "height": height}
        
        tasks["easy"].append({
            "id": f"GR-E-{i+1:03d}",
            "category": "geometric_reasoning",
            "difficulty": "easy",
            "task_type": "area_calculation",
            "shape": shape,
            "question": question,
            "parameters": params,
            "answer": area,
            "reasoning_steps": 2
        })
    
    # Medium: Spatial relationships
    relations = ["inside", "outside", "overlapping", "adjacent"]
    for i in range(TASKS_PER_DIFFICULTY):
        # Two rectangles
        r1 = {"x1": random.randint(0, 5), "y1": random.randint(0, 5)}
        r1["x2"] = r1["x1"] + random.randint(3, 8)
        r1["y2"] = r1["y1"] + random.randint(3, 8)
        
        r2 = {"x1": random.randint(0, 10), "y1": random.randint(0, 10)}
        r2["x2"] = r2["x1"] + random.randint(3, 8)
        r2["y2"] = r2["y1"] + random.randint(3, 8)
        
        # Determine relationship
        if r2["x1"] >= r1["x1"] and r2["y1"] >= r1["y1"] and r2["x2"] <= r1["x2"] and r2["y2"] <= r1["y2"]:
            relation = "inside"
        elif r1["x2"] < r2["x1"] or r2["x2"] < r1["x1"] or r1["y2"] < r2["y1"] or r2["y2"] < r1["y1"]:
            relation = "outside"
        else:
            relation = "overlapping"
        
        tasks["medium"].append({
            "id": f"GR-M-{i+1:03d}",
            "category": "geometric_reasoning",
            "difficulty": "medium",
            "task_type": "spatial_relationship",
            "question": f"Rectangle A has corners ({r1['x1']}, {r1['y1']}) and ({r1['x2']}, {r1['y2']}). Rectangle B has corners ({r2['x1']}, {r2['y1']}) and ({r2['x2']}, {r2['y2']}). What is the spatial relationship between A and B?",
            "rectangle_a": r1,
            "rectangle_b": r2,
            "answer": relation,
            "reasoning_steps": 5
        })
    
    # Hard: Complex polygon operations
    for i in range(TASKS_PER_DIFFICULTY):
        # Generate a simple convex polygon (pentagon)
        center_x, center_y = 50, 50
        radius = random.randint(20, 40)
        num_vertices = 5
        vertices = []
        for j in range(num_vertices):
            angle = 2 * math.pi * j / num_vertices
            x = round(center_x + radius * math.cos(angle), 2)
            y = round(center_y + radius * math.sin(angle), 2)
            vertices.append((x, y))
        
        # Calculate approximate area using shoelace formula
        n = len(vertices)
        area = 0
        for j in range(n):
            x1, y1 = vertices[j]
            x2, y2 = vertices[(j + 1) % n]
            area += x1 * y2 - x2 * y1
        area = round(abs(area) / 2, 2)
        
        tasks["hard"].append({
            "id": f"GR-H-{i+1:03d}",
            "category": "geometric_reasoning",
            "difficulty": "hard",
            "task_type": "polygon_area",
            "question": f"Calculate the area of a polygon with vertices at {vertices} using the shoelace formula.",
            "vertices": vertices,
            "answer": area,
            "reasoning_steps": 8
        })
    
    return tasks


def generate_distance_computation_tasks() -> Dict[str, List[Dict]]:
    """Generate Distance Computation (DC) tasks."""
    tasks = {"easy": [], "medium": [], "hard": []}
    
    # Easy: Euclidean distance
    for i in range(TASKS_PER_DIFFICULTY):
        p1 = (random.randint(0, 100), random.randint(0, 100))
        p2 = (random.randint(0, 100), random.randint(0, 100))
        dist = round(math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2), 2)
        
        tasks["easy"].append({
            "id": f"DC-E-{i+1:03d}",
            "category": "distance_computation",
            "difficulty": "easy",
            "task_type": "euclidean_distance",
            "question": f"Calculate the Euclidean distance between points {p1} and {p2}.",
            "point_a": p1,
            "point_b": p2,
            "answer": dist,
            "reasoning_steps": 3
        })
    
    # Medium: Manhattan distance comparison
    for i in range(TASKS_PER_DIFFICULTY):
        origin = (random.randint(0, 50), random.randint(0, 50))
        destinations = []
        for j in range(4):
            dest = (random.randint(0, 100), random.randint(0, 100))
            manhattan = abs(dest[0] - origin[0]) + abs(dest[1] - origin[1])
            destinations.append({"point": dest, "distance": manhattan})
        
        closest = min(destinations, key=lambda x: x["distance"])
        
        tasks["medium"].append({
            "id": f"DC-M-{i+1:03d}",
            "category": "distance_computation",
            "difficulty": "medium",
            "task_type": "manhattan_comparison",
            "question": f"From origin {origin}, which of these points is closest using Manhattan distance: {[d['point'] for d in destinations]}?",
            "origin": origin,
            "destinations": destinations,
            "answer": closest["point"],
            "reasoning_steps": 5
        })
    
    # Hard: Geodesic distance (Haversine formula)
    for i in range(TASKS_PER_DIFFICULTY):
        # Generate two GPS coordinates in the US
        lat1 = round(random.uniform(25.0, 48.0), 4)
        lon1 = round(random.uniform(-124.0, -70.0), 4)
        lat2 = round(random.uniform(25.0, 48.0), 4)
        lon2 = round(random.uniform(-124.0, -70.0), 4)
        
        # Haversine formula
        R = 6371  # Earth's radius in km
        lat1_rad, lat2_rad = math.radians(lat1), math.radians(lat2)
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = round(R * c, 2)
        
        tasks["hard"].append({
            "id": f"DC-H-{i+1:03d}",
            "category": "distance_computation",
            "difficulty": "hard",
            "task_type": "geodesic_distance",
            "question": f"Calculate the geodesic (great-circle) distance in kilometers between GPS coordinates ({lat1}, {lon1}) and ({lat2}, {lon2}) using the Haversine formula.",
            "point_a": {"latitude": lat1, "longitude": lon1},
            "point_b": {"latitude": lat2, "longitude": lon2},
            "answer": distance,
            "reasoning_steps": 8
        })
    
    return tasks


def save_tasks(tasks: Dict[str, List[Dict]], category: str, base_path: str):
    """Save tasks to JSON files."""
    for difficulty, task_list in tasks.items():
        filepath = os.path.join(base_path, category, difficulty, "tasks.json")
        with open(filepath, 'w') as f:
            json.dump(task_list, f, indent=2)
        print(f"Saved {len(task_list)} tasks to {filepath}")


def main():
    base_path = "/home/ubuntu/spatial-benchmark/data"
    
    print("Generating SpatialEval Benchmark Dataset...")
    print("=" * 50)
    
    # Generate all categories
    categories = {
        "coordinate_understanding": generate_coordinate_understanding_tasks,
        "navigation_pathfinding": generate_navigation_pathfinding_tasks,
        "real_estate": generate_real_estate_tasks,
        "network_infrastructure": generate_network_infrastructure_tasks,
        "geometric_reasoning": generate_geometric_reasoning_tasks,
        "distance_computation": generate_distance_computation_tasks,
    }
    
    total_tasks = 0
    for category, generator in categories.items():
        print(f"\nGenerating {category}...")
        tasks = generator()
        save_tasks(tasks, category, base_path)
        category_total = sum(len(t) for t in tasks.values())
        total_tasks += category_total
        print(f"  Total for {category}: {category_total}")
    
    print("\n" + "=" * 50)
    print(f"Total tasks generated: {total_tasks}")
    
    # Create dataset summary
    summary = {
        "name": "SpatialEval",
        "version": "1.0",
        "total_tasks": total_tasks,
        "categories": list(categories.keys()),
        "difficulty_levels": ["easy", "medium", "hard"],
        "tasks_per_category": TASKS_PER_CATEGORY,
        "tasks_per_difficulty": TASKS_PER_DIFFICULTY
    }
    
    with open(os.path.join(base_path, "dataset_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nDataset summary saved to {base_path}/dataset_summary.json")


if __name__ == "__main__":
    main()
