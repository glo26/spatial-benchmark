#!/usr/bin/env python3
"""Generate placeholder results figure for SpatialEval paper."""

import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

NAVY_DARK = '#1a365d'
NAVY_MED = '#2c5282'
NAVY_LIGHT = '#4299e1'
GRAY = '#718096'
RED_ACCENT = '#c53030'

fig, ax = plt.subplots(figsize=(10, 6))

models = ['GPT-5.2', 'Claude 3', 'Gemini 1.5', 'Grok', 'DeepSeek']
categories = ['CU', 'NP', 'RE', 'NI', 'GR', 'DC']

data = np.zeros((5, 6))

x = np.arange(len(categories))
width = 0.15

colors = [NAVY_DARK, NAVY_MED, NAVY_LIGHT, GRAY, RED_ACCENT]
hatches = ['', '//', 'xx', '..', '\\\\']

for i, (model, color, hatch) in enumerate(zip(models, colors, hatches)):
    offset = (i - 2) * width
    bars = ax.bar(x + offset, data[i], width, label=model, color=color, 
                 edgecolor='black', linewidth=0.5, hatch=hatch)

ax.set_xlabel('Task Category', fontweight='bold')
ax.set_ylabel('Accuracy Score', fontweight='bold')
ax.set_title('Model Performance Across Task Categories\n(Placeholder - Results Pending)', 
            fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(title='Model', loc='upper right', ncol=2)
ax.set_ylim(0, 1.0)

ax.text(2.5, 0.5, 'RESULTS PENDING\nExperiments to be conducted', 
       ha='center', va='center', fontsize=16, fontweight='bold',
       color=GRAY, alpha=0.7,
       bbox=dict(boxstyle='round', facecolor='white', edgecolor=GRAY, alpha=0.8))

plt.tight_layout()
plt.savefig('/home/ubuntu/spatial-benchmark/arxiv/figures/figure4_results_placeholder.png', dpi=300, bbox_inches='tight')
plt.close()
print("Created: figure4_results_placeholder.png")
