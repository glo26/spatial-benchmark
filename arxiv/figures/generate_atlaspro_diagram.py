#!/usr/bin/env python3
"""
Generate a space-efficient block diagram for AtlasPro AI 60 use cases
Layout: 5 industry blocks, each with 3x4 or 3x5 grid of use cases
All grayscale for black and white printing
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Define the 60 use cases by industry
industries = {
    "TELECOM / FIBER (15)": [
        "Premises breakdown",
        "Fiber availability",
        "Route file parsing",
        "Build cost estimate",
        "Unserved locations",
        "Pole availability",
        "Splice point plan",
        "Failure impact",
        "SPOF exposure",
        "Optimal routing",
        "As-built compare",
        "BEAD compliance",
        "Bottleneck analysis",
        "Expansion plan",
        "Make-ready timeline"
    ],
    "UTILITIES (10)": [
        "Wildfire risk",
        "PSPS impact",
        "Cascade risk",
        "Vegetation encroach",
        "Outage prediction",
        "Crew dispatch",
        "Inspection backlog",
        "CPUC compliance",
        "Underground priority",
        "Load forecast"
    ],
    "GOVERNMENT (13)": [
        "Construction impact",
        "Signal optimization",
        "Congestion hotspots",
        "Emergency routing",
        "Event traffic pred",
        "Bridge inspection",
        "Water main impact",
        "Pavement condition",
        "Permit status",
        "Venue readiness",
        "Crime hotspots",
        "Patrol optimization",
        "911 response time"
    ],
    "RETAIL (10)": [
        "Shrinkage analysis",
        "ORC pattern detect",
        "Camera blind spots",
        "LP investment ROI",
        "Risk period predict",
        "Staffing optimize",
        "Floor layout design",
        "Curbside efficiency",
        "Store comparison",
        "Inventory forecast"
    ],
    "CONSTRUCTION (12)": [
        "Hazard zone monitor",
        "Safety compliance",
        "OSHA reporting",
        "Contractor safety",
        "Fall hazard areas",
        "Progress tracking",
        "As-built vs design",
        "Completion predict",
        "Material forecast",
        "Equipment utilization",
        "Daily reporting",
        "Insurance status"
    ]
}

# Technology mapping (MCP vs GNN)
tech_mapping = {
    "TELECOM / FIBER (15)": ["MCP", "MCP", "MCP", "MCP", "MCP", "MCP", "MCP", "GNN", "GNN", "GNN", "MCP", "MCP", "GNN", "GNN", "MCP"],
    "UTILITIES (10)": ["GNN", "GNN", "GNN", "MCP", "GNN", "GNN", "MCP", "MCP", "GNN", "GNN"],
    "GOVERNMENT (13)": ["GNN", "GNN", "MCP", "GNN", "GNN", "MCP", "GNN", "MCP", "MCP", "GNN", "MCP", "GNN", "MCP"],
    "RETAIL (10)": ["MCP", "GNN", "MCP", "MCP", "MCP", "MCP", "GNN", "MCP", "MCP", "MCP"],
    "CONSTRUCTION (12)": ["MCP", "MCP", "MCP", "MCP", "MCP", "MCP", "MCP", "MCP", "MCP", "MCP", "MCP", "MCP"]
}

# Create figure with tight layout
fig, axes = plt.subplots(1, 5, figsize=(16, 6))
fig.suptitle('AtlasPro AI: 60 Validated Use Cases Across 5 Industries', fontsize=14, fontweight='bold', y=0.98)

# Colors for grayscale printing
mcp_color = '#E8E8E8'  # Light gray for MCP
gnn_color = '#B0B0B0'  # Darker gray for GNN
border_color = '#404040'  # Dark gray for borders
text_color = '#000000'  # Black text

for idx, (industry, use_cases) in enumerate(industries.items()):
    ax = axes[idx]
    ax.set_xlim(0, 3)
    ax.set_ylim(0, max(5, (len(use_cases) + 2) // 3 + 1))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Industry title
    ax.text(1.5, ax.get_ylim()[1] - 0.3, industry, ha='center', va='top', 
            fontsize=8, fontweight='bold', color=text_color)
    
    # Calculate grid dimensions
    n_cases = len(use_cases)
    n_cols = 3
    n_rows = (n_cases + n_cols - 1) // n_cols
    
    # Draw use case blocks
    box_width = 0.9
    box_height = 0.55
    start_y = ax.get_ylim()[1] - 0.8
    
    techs = tech_mapping[industry]
    
    for i, (use_case, tech) in enumerate(zip(use_cases, techs)):
        row = i // n_cols
        col = i % n_cols
        
        x = col * 1.0 + 0.05
        y = start_y - row * 0.65
        
        # Choose color based on technology
        color = mcp_color if tech == "MCP" else gnn_color
        
        # Draw rectangle
        rect = patches.FancyBboxPatch(
            (x, y - box_height), box_width, box_height,
            boxstyle="round,pad=0.02,rounding_size=0.05",
            facecolor=color, edgecolor=border_color, linewidth=0.5
        )
        ax.add_patch(rect)
        
        # Add text (wrap long text)
        text = use_case
        if len(text) > 14:
            # Split into two lines
            words = text.split()
            mid = len(words) // 2
            line1 = ' '.join(words[:mid])
            line2 = ' '.join(words[mid:])
            ax.text(x + box_width/2, y - box_height/2, f"{line1}\n{line2}", 
                    ha='center', va='center', fontsize=5, color=text_color)
        else:
            ax.text(x + box_width/2, y - box_height/2, text, 
                    ha='center', va='center', fontsize=5.5, color=text_color)

# Add legend at bottom
legend_y = -0.08
fig.text(0.35, legend_y, '■ MCP (Spatial Tools)', fontsize=9, ha='center', 
         bbox=dict(boxstyle='round', facecolor=mcp_color, edgecolor=border_color))
fig.text(0.65, legend_y, '■ GNN (Network Intelligence)', fontsize=9, ha='center',
         bbox=dict(boxstyle='round', facecolor=gnn_color, edgecolor=border_color))

# Add summary stats
fig.text(0.5, -0.14, 'Total: 60 Use Cases | MCP: 38 (63%) | GNN: 22 (37%)', 
         fontsize=9, ha='center', style='italic')

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig('figure_atlaspro_usecases.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.savefig('figure_atlaspro_usecases.pdf', bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("Generated: figure_atlaspro_usecases.png and .pdf")
