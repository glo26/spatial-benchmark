#!/usr/bin/env python3
"""Generate Figure 4: Category Performance Comparison"""

import matplotlib.pyplot as plt
import numpy as np

# Set style for academic paper
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10

# Categories
categories = [
    'CU', 'GR', 'DC', 'TR',  # Tier 1
    'NP', 'VVA', 'PRA', 'NI',  # Tier 2
    'CBP', 'RAO', 'TSR', 'RE'  # Tier 3
]

# Model performance by category (placeholder data)
models = {
    'GPT-5.2': [89, 87, 91, 82, 75, 71, 78, 68, 58, 62, 55, 60],
    'Claude 3': [84, 82, 86, 77, 70, 66, 73, 63, 53, 57, 50, 55],
    'Gemini 1.5': [78, 76, 80, 71, 64, 60, 67, 57, 47, 51, 44, 49],
    'Grok': [72, 70, 74, 65, 58, 54, 61, 51, 41, 45, 38, 43],
    'DeepSeek': [66, 64, 68, 59, 52, 48, 55, 45, 35, 39, 32, 37]
}

# Colors and markers for black-and-white compatibility
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
markers = ['o', 's', '^', 'D', 'v']
linestyles = ['-', '--', '-.', ':', '-']

fig, ax = plt.subplots(figsize=(12, 5))

x = np.arange(len(categories))
width = 0.15

for i, (model, scores) in enumerate(models.items()):
    ax.bar(x + i * width, scores, width, label=model, color=colors[i], 
           edgecolor='black', linewidth=0.5)

# Add tier separators
ax.axvline(x=3.5, color='gray', linestyle='--', linewidth=1, alpha=0.7)
ax.axvline(x=7.5, color='gray', linestyle='--', linewidth=1, alpha=0.7)

# Add tier labels
ax.text(1.5, 95, 'Tier 1\n(Foundational)', ha='center', fontsize=9, style='italic')
ax.text(5.5, 95, 'Tier 2\n(Core Planning)', ha='center', fontsize=9, style='italic')
ax.text(9.5, 95, 'Tier 3\n(Advanced)', ha='center', fontsize=9, style='italic')

ax.set_xlabel('Task Category')
ax.set_ylabel('Accuracy (%)')
ax.set_title('Model Performance Across SpatialEval Task Categories')
ax.set_xticks(x + width * 2)
ax.set_xticklabels(categories)
ax.set_ylim(0, 100)
ax.legend(loc='upper right', ncol=5, fontsize=8)

plt.tight_layout()
plt.savefig('/home/ubuntu/spatial-benchmark/arxiv/figures/figure4_category_performance.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("Figure 4 generated successfully!")
