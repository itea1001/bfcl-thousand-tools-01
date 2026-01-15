import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Data from evaluation results
pool_sizes = [0, 16, 32, 64, 128, 256, 512]

# Parallel category
parallel_data = {
    'GPT-4o': [94.0, 91.0, 90.0, 88.0, 86.5, 77.0, 65.5],
    'GPT-4o-mini': [91.0, 83.0, 82.0, 80.0, 70.0, 58.5, 50.5],
    'Grok-4': [89.0, 88.0, 85.5, 85.5, 81.5, 78.0, 66.5],
    'Grok-3-beta': [96.5, 92.0, 91.0, 88.0, 84.5, 79.0, 66.5],
    'Grok-3-mini': [89.0, 83.5, 88.5, 86.0, 78.0, 65.5, 47.0]
}

# Multiple category
multiple_data = {
    'GPT-4o': [93.5, 90.5, 90.5, 91.5, 86.0, 85.0, 80.0],
    'GPT-4o-mini': [92.5, 87.5, 82.5, 81.5, 70.5, 62.0, 48.5],
    'Grok-4': [91.0, 89.5, 89.5, 88.5, 89.0, 86.5, 76.0],
    'Grok-3-beta': [96.0, 91.5, 91.5, 89.0, 87.5, 82.5, 73.5],
    'Grok-3-mini': [92.0, 90.5, 93.5, 91.0, 89.0, 81.0, 60.0]
}

# Parallel_multiple category
parallel_multiple_data = {
    'GPT-4o': [86.0, 87.5, 85.0, 83.0, 77.5, 69.0, 60.5],
    'GPT-4o-mini': [90.0, 84.0, 79.5, 73.5, 59.5, 56.0, 34.0],
    'Grok-4': [82.0, 76.0, 73.5, 71.0, 68.0, 63.5, 49.0],
    'Grok-3-beta': [92.0, 90.5, 89.0, 81.0, 79.5, 74.0, 62.0],
    'Grok-3-mini': [87.5, 86.5, 81.5, 79.0, 74.0, 54.0, 33.0]
}

# Color scheme for models
colors = {
    'GPT-4o': '#10A37F',
    'GPT-4o-mini': '#7FCCBA',
    'Grok-4': '#E84142',
    'Grok-3-beta': '#FF6B6B',
    'Grok-3-mini': '#FFA07A'
}

# Line styles for better differentiation
line_styles = {
    'GPT-4o': '-',
    'GPT-4o-mini': '--',
    'Grok-4': '-',
    'Grok-3-beta': '-.',
    'Grok-3-mini': ':'
}

# Markers
markers = {
    'GPT-4o': 'o',
    'GPT-4o-mini': 's',
    'Grok-4': '^',
    'Grok-3-beta': 'd',
    'Grok-3-mini': 'v'
}

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('LLM Function-Calling Performance Across Task Types and Pool Sizes', 
             fontsize=16, fontweight='bold', y=0.995)

# Plot 1: Parallel
ax1 = axes[0, 0]
for model, accuracies in parallel_data.items():
    ax1.plot(pool_sizes, accuracies, 
             color=colors[model], 
             linestyle=line_styles[model],
             marker=markers[model],
             linewidth=2,
             markersize=8,
             label=model)
ax1.set_xlabel('Pool Size (Number of Distractor Functions)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Accuracy (%)', fontsize=11, fontweight='bold')
ax1.set_title('Parallel Tasks', fontsize=13, fontweight='bold', pad=10)
ax1.legend(loc='lower left', fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(40, 100)

# Plot 2: Multiple
ax2 = axes[0, 1]
for model, accuracies in multiple_data.items():
    ax2.plot(pool_sizes, accuracies, 
             color=colors[model], 
             linestyle=line_styles[model],
             marker=markers[model],
             linewidth=2,
             markersize=8,
             label=model)
ax2.set_xlabel('Pool Size (Number of Distractor Functions)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Accuracy (%)', fontsize=11, fontweight='bold')
ax2.set_title('Multiple (Sequential) Tasks', fontsize=13, fontweight='bold', pad=10)
ax2.legend(loc='lower left', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(40, 100)

# Plot 3: Parallel_multiple
ax3 = axes[1, 0]
for model, accuracies in parallel_multiple_data.items():
    ax3.plot(pool_sizes, accuracies, 
             color=colors[model], 
             linestyle=line_styles[model],
             marker=markers[model],
             linewidth=2,
             markersize=8,
             label=model)
ax3.set_xlabel('Pool Size (Number of Distractor Functions)', fontsize=11, fontweight='bold')
ax3.set_ylabel('Accuracy (%)', fontsize=11, fontweight='bold')
ax3.set_title('Parallel Multiple (Combined) Tasks', fontsize=13, fontweight='bold', pad=10)
ax3.legend(loc='lower left', fontsize=9)
ax3.grid(True, alpha=0.3)
ax3.set_ylim(30, 100)

# Plot 4: Average across all categories
ax4 = axes[1, 1]
for model in parallel_data.keys():
    avg_accuracies = [
        (parallel_data[model][i] + multiple_data[model][i] + parallel_multiple_data[model][i]) / 3
        for i in range(len(pool_sizes))
    ]
    ax4.plot(pool_sizes, avg_accuracies, 
             color=colors[model], 
             linestyle=line_styles[model],
             marker=markers[model],
             linewidth=2,
             markersize=8,
             label=model)
ax4.set_xlabel('Pool Size (Number of Distractor Functions)', fontsize=11, fontweight='bold')
ax4.set_ylabel('Average Accuracy (%)', fontsize=11, fontweight='bold')
ax4.set_title('Average Across All Task Types', fontsize=13, fontweight='bold', pad=10)
ax4.legend(loc='lower left', fontsize=9)
ax4.grid(True, alpha=0.3)
ax4.set_ylim(40, 100)

plt.tight_layout()
plt.savefig('/home/mingxuanl/mingxuanl/simulation/marcussullivan/bfcl-thousand-tools-01/comprehensive_model_comparison.png', 
            dpi=300, bbox_inches='tight')
print("Plot saved: comprehensive_model_comparison.png")

# Create a second figure focusing on degradation rates
fig2, ax = plt.subplots(figsize=(12, 7))

degradation_data = {
    'Parallel': [
        ('GPT-4o', 28.5),
        ('GPT-4o-mini', 40.5),
        ('Grok-4', 22.5),
        ('Grok-3-beta', 30.0),
        ('Grok-3-mini', 42.0)
    ],
    'Multiple': [
        ('GPT-4o', 13.5),
        ('GPT-4o-mini', 44.0),
        ('Grok-4', 15.0),
        ('Grok-3-beta', 22.5),
        ('Grok-3-mini', 32.0)
    ],
    'Parallel Multiple': [
        ('GPT-4o', 25.5),
        ('GPT-4o-mini', 56.0),
        ('Grok-4', 33.0),
        ('Grok-3-beta', 30.0),
        ('Grok-3-mini', 54.5)
    ]
}

x = range(5)
width = 0.25
models = ['GPT-4o', 'GPT-4o-mini', 'Grok-4', 'Grok-3-beta', 'Grok-3-mini']

for i, (category, data) in enumerate(degradation_data.items()):
    values = [d[1] for d in data]
    offset = (i - 1) * width
    bars = ax.bar([xi + offset for xi in x], values, width, 
                   label=category, alpha=0.8)

ax.set_xlabel('Model', fontsize=12, fontweight='bold')
ax.set_ylabel('Accuracy Degradation (Pool 0 → Pool 512)', fontsize=12, fontweight='bold')
ax.set_title('Performance Degradation by Model and Task Type', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(models, rotation=15, ha='right')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')
ax.axhline(y=30, color='red', linestyle='--', alpha=0.5, linewidth=1)
ax.text(4.2, 31, 'Moderate degradation threshold', fontsize=9, color='red')

plt.tight_layout()
plt.savefig('/home/mingxuanl/mingxuanl/simulation/marcussullivan/bfcl-thousand-tools-01/degradation_comparison.png', 
            dpi=300, bbox_inches='tight')
print("Plot saved: degradation_comparison.png")

print("\nVisualization complete!")
print("Generated files:")
print("  - comprehensive_model_comparison.png")
print("  - degradation_comparison.png")

