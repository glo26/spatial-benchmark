#!/usr/bin/env python3
"""Regenerate figures with proper dimensions for academic paper."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Set style for academic papers
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.dpi'] = 300

# Figure 1: Framework Overview (horizontal flow diagram)
def create_framework_figure():
    fig, ax = plt.subplots(figsize=(10, 3))
    
    # Define boxes
    boxes = [
        ('Task Input\n(JSON)', 0.05, 0.4, 0.12, 0.4, '#E8E8E8'),
        ('LLM Agent\n(5 Models)', 0.22, 0.4, 0.12, 0.4, '#D0D0D0'),
        ('Response\nParser', 0.39, 0.4, 0.12, 0.4, '#E8E8E8'),
        ('Multi-Faceted\nEvaluator', 0.56, 0.4, 0.14, 0.4, '#C0C0C0'),
        ('Leaderboard\n& Analysis', 0.77, 0.4, 0.14, 0.4, '#B0B0B0'),
    ]
    
    for label, x, y, w, h, color in boxes:
        rect = mpatches.FancyBboxPatch((x, y), w, h, 
                                        boxstyle="round,pad=0.02,rounding_size=0.02",
                                        facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, label, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Add arrows
    arrow_style = dict(arrowstyle='->', color='black', lw=1.5)
    for i in range(len(boxes) - 1):
        x1 = boxes[i][1] + boxes[i][3]
        x2 = boxes[i+1][1]
        y = boxes[i][2] + boxes[i][4] / 2
        ax.annotate('', xy=(x2, y), xytext=(x1, y), arrowprops=arrow_style)
    
    # Add tier labels below
    ax.text(0.5, 0.15, 'SpatialOps Benchmark Framework', ha='center', va='center', 
            fontsize=12, fontweight='bold')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('figure1_framework.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created figure1_framework.png")

# Figure 2: Task Distribution
def create_distribution_figure():
    fig, ax = plt.subplots(figsize=(10, 4))
    
    categories = ['CU', 'GR', 'DC', 'TR', 'NP', 'VVA', 'PRA', 'NI', 'CBP', 'RAO', 'TSR', 'RE']
    full_names = [
        'Coordinate\nUnderstanding', 'Geometric\nReasoning', 'Distance\nComputation',
        'Topological\nReasoning', 'Navigation\nPathfinding', 'Viewpoint\nVisibility',
        'Pattern\nRecognition', 'Network\nInfrastructure', 'Constraint\nPlacement',
        'Resource\nAllocation', 'Temporal\nSpatial', 'Real Estate\nGeospatial'
    ]
    
    easy = [167] * 12
    medium = [167] * 12
    hard = [167] * 12
    
    x = np.arange(len(categories))
    width = 0.25
    
    bars1 = ax.bar(x - width, easy, width, label='Easy', color='#404040', edgecolor='black')
    bars2 = ax.bar(x, medium, width, label='Medium', color='#808080', edgecolor='black')
    bars3 = ax.bar(x + width, hard, width, label='Hard', color='#C0C0C0', edgecolor='black')
    
    ax.set_xlabel('Task Category', fontweight='bold')
    ax.set_ylabel('Number of Tasks', fontweight='bold')
    ax.set_title('Distribution of 6,012 Tasks Across 12 Categories and 3 Difficulty Levels', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=8)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 220)
    
    # Add tier separators
    ax.axvline(x=3.5, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
    ax.axvline(x=7.5, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
    
    # Add tier labels
    ax.text(1.5, 205, 'Tier 1: Foundational', ha='center', fontsize=8, fontstyle='italic')
    ax.text(5.5, 205, 'Tier 2: Core Planning', ha='center', fontsize=8, fontstyle='italic')
    ax.text(9.5, 205, 'Tier 3: Advanced', ha='center', fontsize=8, fontstyle='italic')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('figure2_task_distribution.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created figure2_task_distribution.png")

if __name__ == '__main__':
    create_framework_figure()
    create_distribution_figure()
    print("All figures regenerated successfully!")
