import matplotlib.pyplot as plt
import json

# Data for all models (pools 0-512, excluding 1024 due to context limits for most models)
pool_sizes = [0, 16, 32, 64, 128, 256, 512]

# Grok models
grok4_data = [72.25, 72.00, 69.00, 69.50, 69.50, 66.50, 65.50]
grok3beta_data = [73.00, 70.25, 71.50, 70.00, 68.75, 66.00, 62.75]
grok3mini_data = [66.00, 64.25, 62.25, 64.00, 63.50, 59.00, 45.00]

# GPT models
gpt4o_data = [74.00, 70.00, 69.50, 69.75, 69.25, 68.00, 63.00]
gpt4omini_data = [70.25, 67.00, 66.25, 63.25, 60.25, 55.50, 48.00]

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: All 5 models together
ax1.plot(pool_sizes, grok4_data, marker='o', linestyle='-', linewidth=2, color='#FF6B35', label='Grok-4')
ax1.plot(pool_sizes, grok3beta_data, marker='s', linestyle='-', linewidth=2, color='#F7931E', label='Grok-3-beta')
ax1.plot(pool_sizes, grok3mini_data, marker='^', linestyle='--', linewidth=2, color='#FDC830', label='Grok-3-mini-beta')
ax1.plot(pool_sizes, gpt4o_data, marker='D', linestyle='-', linewidth=2, color='#4ECDC4', label='GPT-4o')
ax1.plot(pool_sizes, gpt4omini_data, marker='x', linestyle='--', linewidth=2, color='#95E1D3', label='GPT-4o-mini')

ax1.set_title('Function Calling Accuracy vs. Pool Size: All Models', fontsize=14, fontweight='bold')
ax1.set_xlabel('Number of Functions in Pool', fontsize=12)
ax1.set_ylabel('Accuracy (%)', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.set_xticks(pool_sizes)
ax1.set_ylim(40, 80)
ax1.legend(loc='lower left', fontsize=10)

# Plot 2: Grok family comparison
ax2.plot(pool_sizes, grok4_data, marker='o', linestyle='-', linewidth=2, color='#FF6B35', label='Grok-4')
ax2.plot(pool_sizes, grok3beta_data, marker='s', linestyle='-', linewidth=2, color='#F7931E', label='Grok-3-beta')
ax2.plot(pool_sizes, grok3mini_data, marker='^', linestyle='--', linewidth=2, color='#FDC830', label='Grok-3-mini-beta')

ax2.set_title('Grok Family Performance Comparison', fontsize=14, fontweight='bold')
ax2.set_xlabel('Number of Functions in Pool', fontsize=12)
ax2.set_ylabel('Accuracy (%)', fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.set_xticks(pool_sizes)
ax2.set_ylim(40, 80)
ax2.legend(loc='lower left', fontsize=10)

plt.tight_layout()
plt.savefig('all_models_comparison.png', dpi=300, bbox_inches='tight')
print("Comparison plot saved to all_models_comparison.png")

# Create a degradation comparison plot
fig2, ax3 = plt.subplots(1, 1, figsize=(12, 7))

# Calculate degradation from baseline for each model
grok4_deg = [(grok4_data[0] - x) for x in grok4_data]
grok3beta_deg = [(grok3beta_data[0] - x) for x in grok3beta_data]
grok3mini_deg = [(grok3mini_data[0] - x) for x in grok3mini_data]
gpt4o_deg = [(gpt4o_data[0] - x) for x in gpt4o_data]
gpt4omini_deg = [(gpt4omini_data[0] - x) for x in gpt4omini_data]

ax3.plot(pool_sizes, grok4_deg, marker='o', linestyle='-', linewidth=2, color='#FF6B35', label='Grok-4')
ax3.plot(pool_sizes, grok3beta_deg, marker='s', linestyle='-', linewidth=2, color='#F7931E', label='Grok-3-beta')
ax3.plot(pool_sizes, grok3mini_deg, marker='^', linestyle='--', linewidth=2, color='#FDC830', label='Grok-3-mini-beta')
ax3.plot(pool_sizes, gpt4o_deg, marker='D', linestyle='-', linewidth=2, color='#4ECDC4', label='GPT-4o')
ax3.plot(pool_sizes, gpt4omini_deg, marker='x', linestyle='--', linewidth=2, color='#95E1D3', label='GPT-4o-mini')

ax3.set_title('Performance Degradation from Baseline vs. Pool Size', fontsize=14, fontweight='bold')
ax3.set_xlabel('Number of Functions in Pool', fontsize=12)
ax3.set_ylabel('Accuracy Drop from Baseline (%)', fontsize=12)
ax3.grid(True, linestyle='--', alpha=0.7)
ax3.set_xticks(pool_sizes)
ax3.set_ylim(-2, 25)
ax3.legend(loc='upper left', fontsize=10)
ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.5)

plt.tight_layout()
plt.savefig('degradation_comparison.png', dpi=300, bbox_inches='tight')
print("Degradation plot saved to degradation_comparison.png")

