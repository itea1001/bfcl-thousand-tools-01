import matplotlib.pyplot as plt
import numpy as np

# Data for GPT-4o-mini
gpt4o_mini_data = {
    'parallel': [91.00, 83.00, 82.00, 80.00, 70.00, 58.50, 50.50],
    'multiple': [92.50, 87.50, 82.50, 81.50, 70.50, 62.00, 48.50],
    'parallel_multiple': [90.00, 84.00, 79.50, 73.50, 59.50, 56.00, 34.00]
}

# Data for GPT-4o
gpt4o_data = {
    'parallel': [94.00, 91.00, 90.00, 88.00, 86.50, 77.00, 65.50],
    'multiple': [93.50, 90.50, 90.50, 91.50, 86.00, 85.00, 80.00],
    'parallel_multiple': [86.00, 87.50, 85.00, 83.00, 77.50, 69.00, 60.50]
}

pool_sizes = [0, 16, 32, 64, 128, 256, 512]

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: GPT-4o-mini
colors_mini = ['#FF6B6B', '#4ECDC4', '#45B7D1']
for i, (category, values) in enumerate(gpt4o_mini_data.items()):
    ax1.plot(pool_sizes, values, marker='o', linewidth=2.5, markersize=8, 
             label=category.replace('_', ' ').title(), color=colors_mini[i])

ax1.set_xlabel('Number of Distractor Functions (Pool Size)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
ax1.set_title('GPT-4o-mini: Category Scaling Performance', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11, loc='upper right')
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_ylim([0, 100])
ax1.set_xscale('symlog')
ax1.set_xticks(pool_sizes)
ax1.set_xticklabels(pool_sizes)

# Plot 2: GPT-4o
colors_4o = ['#E74C3C', '#16A085', '#2980B9']
for i, (category, values) in enumerate(gpt4o_data.items()):
    ax2.plot(pool_sizes, values, marker='s', linewidth=2.5, markersize=8,
             label=category.replace('_', ' ').title(), color=colors_4o[i])

ax2.set_xlabel('Number of Distractor Functions (Pool Size)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
ax2.set_title('GPT-4o: Category Scaling Performance', fontsize=14, fontweight='bold')
ax2.legend(fontsize=11, loc='upper right')
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_ylim([0, 100])
ax2.set_xscale('symlog')
ax2.set_xticks(pool_sizes)
ax2.set_xticklabels(pool_sizes)

plt.tight_layout()
plt.savefig('category_scaling_comparison.png', dpi=300, bbox_inches='tight')
print("Saved: category_scaling_comparison.png")

# Create second figure: Direct comparison per category
fig2, axes = plt.subplots(1, 3, figsize=(18, 5))

categories = ['parallel', 'multiple', 'parallel_multiple']
category_titles = ['Parallel', 'Multiple', 'Parallel Multiple']

for idx, (category, title) in enumerate(zip(categories, category_titles)):
    ax = axes[idx]
    ax.plot(pool_sizes, gpt4o_mini_data[category], marker='o', linewidth=2.5, markersize=8,
            label='GPT-4o-mini', color='#FF6B6B')
    ax.plot(pool_sizes, gpt4o_data[category], marker='s', linewidth=2.5, markersize=8,
            label='GPT-4o', color='#2980B9')
    
    ax.set_xlabel('Pool Size', fontsize=11, fontweight='bold')
    ax.set_ylabel('Accuracy (%)', fontsize=11, fontweight='bold')
    ax.set_title(f'{title} Category', fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_ylim([0, 100])
    ax.set_xscale('symlog')
    ax.set_xticks(pool_sizes)
    ax.set_xticklabels(pool_sizes)

plt.tight_layout()
plt.savefig('category_by_category_comparison.png', dpi=300, bbox_inches='tight')
print("Saved: category_by_category_comparison.png")

# Create third figure: Degradation comparison
fig3, ax = plt.subplots(figsize=(12, 7))

x = np.arange(len(categories))
width = 0.35

mini_degradation = [
    gpt4o_mini_data['parallel'][0] - gpt4o_mini_data['parallel'][-1],
    gpt4o_mini_data['multiple'][0] - gpt4o_mini_data['multiple'][-1],
    gpt4o_mini_data['parallel_multiple'][0] - gpt4o_mini_data['parallel_multiple'][-1]
]

gpt4o_degradation = [
    gpt4o_data['parallel'][0] - gpt4o_data['parallel'][-1],
    gpt4o_data['multiple'][0] - gpt4o_data['multiple'][-1],
    gpt4o_data['parallel_multiple'][0] - gpt4o_data['parallel_multiple'][-1]
]

bars1 = ax.bar(x - width/2, mini_degradation, width, label='GPT-4o-mini', color='#FF6B6B', alpha=0.8)
bars2 = ax.bar(x + width/2, gpt4o_degradation, width, label='GPT-4o', color='#2980B9', alpha=0.8)

ax.set_xlabel('Category', fontsize=12, fontweight='bold')
ax.set_ylabel('Performance Degradation (Pool 0 → 512, %)', fontsize=12, fontweight='bold')
ax.set_title('Performance Degradation Comparison Across Categories', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(category_titles)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, linestyle='--', axis='y')

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('category_degradation_comparison.png', dpi=300, bbox_inches='tight')
print("Saved: category_degradation_comparison.png")

print("\nAll plots generated successfully!")

