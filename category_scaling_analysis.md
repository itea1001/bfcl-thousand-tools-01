# Category Scaling Analysis: GPT-4o vs GPT-4o-mini

## Overview
This analysis compares GPT-4o and GPT-4o-mini performance across three additional Python single-turn categories (parallel, multiple, parallel_multiple) as the number of distractor functions increases from 0 to 512.

## Results Summary

### GPT-4o-mini Performance

| Pool Size | Parallel | Multiple | Parallel Multiple |
|-----------|----------|----------|-------------------|
| 0         | 91.00%   | 92.50%   | 90.00%            |
| 16        | 83.00%   | 87.50%   | 84.00%            |
| 32        | 82.00%   | 82.50%   | 79.50%            |
| 64        | 80.00%   | 81.50%   | 73.50%            |
| 128       | 70.00%   | 70.50%   | 59.50%            |
| 256       | 58.50%   | 62.00%   | 56.00%            |
| 512       | 50.50%   | 48.50%   | 34.00%            |

**Degradation (Pool 0 → 512):**
- Parallel: -40.50%
- Multiple: -44.00%
- Parallel Multiple: -56.00%

### GPT-4o Performance

| Pool Size | Parallel | Multiple | Parallel Multiple |
|-----------|----------|----------|-------------------|
| 0         | 94.00%   | 93.50%   | 86.00%            |
| 16        | 91.00%   | 90.50%   | 87.50%            |
| 32        | 90.00%   | 90.50%   | 85.00%            |
| 64        | 88.00%   | 91.50%   | 83.00%            |
| 128       | 86.50%   | 86.00%   | 77.50%            |
| 256       | 77.00%   | 85.00%   | 69.00%            |
| 512       | 65.50%   | 80.00%   | 60.50%            |

**Degradation (Pool 0 → 512):**
- Parallel: -28.50%
- Multiple: -13.50%
- Parallel Multiple: -25.50%

## Key Findings

### 1. Category Difficulty
Both models show different baseline performance across categories:
- **Easiest**: Multiple (92.50% mini, 93.50% GPT-4o at pool 0)
- **Hardest**: Parallel Multiple (90.00% mini, 86.00% GPT-4o at pool 0)

### 2. Degradation Patterns
**GPT-4o-mini:**
- Shows severe degradation, especially in parallel_multiple (-56%)
- Falls below 50% at pool 512 for multiple (48.50%) and parallel_multiple (34.00%)
- More sensitive to distractor functions across all categories

**GPT-4o:**
- Much more robust, maintaining >60% accuracy at pool 512 across all categories
- Best resilience in multiple category (-13.50% degradation only)
- Shows 2-3x better retention than mini in complex scenarios

### 3. Category-Specific Observations

**Parallel:**
- GPT-4o maintains 65.50% at pool 512
- GPT-4o-mini drops to 50.50%
- 15% gap at highest pool size

**Multiple:**
- GPT-4o remarkably resilient: 80% at pool 512
- GPT-4o-mini struggles: 48.50% at pool 512
- Largest performance gap (31.5%) at pool 512

**Parallel Multiple:**
- Most challenging category for both models
- GPT-4o: 60.50% at pool 512
- GPT-4o-mini: 34% at pool 512
- 26.5% gap, indicating complexity compounds distractor impact

### 4. Comparison with Simple Python
Comparing to simple_python results from previous experiments:
- **Simple Python degradation**: GPT-4o (-23.5%), GPT-4o-mini (-45%)
- **Parallel degradation**: GPT-4o (-28.5%), GPT-4o-mini (-40.5%)
- **Multiple degradation**: GPT-4o (-13.5%), GPT-4o-mini (-44%)
- **Parallel Multiple degradation**: GPT-4o (-25.5%), GPT-4o-mini (-56%)

Pattern: GPT-4o shows more consistent performance across categories, while GPT-4o-mini degrades significantly more in complex multi-call scenarios.

## Conclusions

1. **GPT-4o's advantage increases with complexity**: The performance gap between GPT-4o and GPT-4o-mini widens as pool size increases, from ~3% at pool 0 to 15-31.5% at pool 512.

2. **Category complexity matters**: Parallel multiple tasks show the steepest degradation for both models, suggesting that combining multiple function calls with parallel execution creates compounding difficulty.

3. **Multiple category resilience**: GPT-4o shows exceptional performance on multiple function calls (80% at pool 512), suggesting strong reasoning capabilities for sequential multi-step tasks even with many distractors.

4. **Practical implications**: For production systems with large tool sets:
   - GPT-4o recommended for complex multi-call scenarios
   - GPT-4o-mini may struggle with >256 tools in parallel_multiple tasks
   - Simple and multiple categories are more robust to distractor functions than parallel variants

