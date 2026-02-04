# Research Notes for SpatialEval Enhancement

## Spatial Survey Paper (arXiv:2602.01644)
**Title:** From Perception to Action: Spatial AI Agents and World Models
**Authors:** Gloria Felicia, Nolan Bryant, Handi Putra, Ayaan Gazali, Eliel Lobo, Esteban Rojas (AtlasPro AI)
**Date:** February 2, 2026

### Key Contributions:
1. Unified three-axis taxonomy connecting agentic AI components (memory, planning, tool use) with spatial intelligence domains
2. Comprehensive analysis of 742 cited works from 2,000+ papers
3. Three key findings:
   - Hierarchical memory systems important for long-horizon spatial tasks
   - GNN-LLM integration promising for structured spatial reasoning
   - World models essential for safe deployment across micro-to-macro spatial scales

### Taxonomy Axes:
**Axis 1: Spatial Task**
- Navigation (meso-to-macro scale)
- Scene Understanding
- Manipulation (micro-to-meso scale)
- Geospatial Analysis (macro scale)

**Axis 2: Agentic Capability**
- Memory (short-term, long-term, episodic, spatial)
- Planning (reactive, hierarchical, search-based, world model-based)
- Tool Use & Action (API integration, code generation, physical action)

**Axis 3: Spatial Scale**
- Micro-spatial (<1m): Pose estimation, grasping, fine manipulation
- Meso-spatial (1m-100m): Room navigation, building exploration
- Macro-spatial (>100m): City-scale planning, satellite imagery, infrastructure networks

### Six Grand Challenges Identified:
1. Unified cross-scale representation
2. Grounded long-horizon planning
3. Safety guarantees
4. Sim-to-real transfer
5. Multi-agent coordination
6. Edge deployment

---

## AtlasPro AI Use Cases (60 Total)

### Summary by Industry:
| Industry | MCP (Spatial) | GNN (Network) | Total |
|----------|---------------|---------------|-------|
| Telecom/Fiber | 9 | 6 | 15 |
| Utilities | 3 | 7 | 10 |
| Government/Smart Cities | 6 | 7 | 13 |
| Retail | 8 | 2 | 10 |
| Construction/Industrial | 12 | 0 | 12 |
| **TOTAL** | **38** | **22** | **60** |

### Key Pattern:
"Given [spatial context], tell me [insight] or do [action]"
- MCP tools: 63% of use cases (KML/KMZ parsing, geospatial queries, compliance, reporting)
- GNN: 37% requiring topology reasoning (failure analysis, cascade prediction, route optimization)

### Use Case Categories Mapped to SpatialEval:
1. **Coordinate Understanding (CU)**: Polygon queries, premises breakdown, GPS coordinates
2. **Navigation & Pathfinding (NP)**: Optimal routing, A* algorithm, traffic optimization
3. **Real Estate Analysis (RE)**: Property analysis, zoning, BEAD compliance
4. **Network Infrastructure (NI)**: Fiber routing, splice points, failure analysis, cascade risk
5. **Geometric Reasoning (GR)**: Polygon analysis, area calculations, boundary detection
6. **Distance Computation (DC)**: Route miles, proximity queries, coverage analysis

---

## Citation for Survey Paper:
```bibtex
@article{felicia2026perception,
  title={From Perception to Action: Spatial AI Agents and World Models},
  author={Felicia, Gloria and Bryant, Nolan and Putra, Handi and Gazali, Ayaan and Lobo, Eliel and Rojas, Esteban},
  journal={arXiv preprint arXiv:2602.01644},
  year={2026}
}
```
