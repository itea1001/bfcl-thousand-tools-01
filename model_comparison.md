# Model Comparison: GPT-4o vs GPT-4o-mini

**Test Category:** simple_python  
**Date:** 2026-01-12  
**Researcher:** Marcus Sullivan

## Side-by-Side Accuracy Comparison

| Pool Size | Distractors | GPT-4o Accuracy | GPT-4o-mini Accuracy | Difference | GPT-4o vs Baseline | GPT-4o-mini vs Baseline |
|-----------|-------------|-----------------|----------------------|------------|-------------------|------------------------|
| 0         | 0           | 74.00%          | 70.25%              | +3.75%     | --                | --                     |
| 16        | 15          | 70.00%          | 67.00%              | +3.00%     | -4.00%            | -3.25%                 |
| 32        | 31          | 69.50%          | 66.25%              | +3.25%     | -4.50%            | -4.00%                 |
| 64        | 63          | 69.75%          | 63.25%              | +6.50%     | -4.25%            | -7.00%                 |
| 128       | 127         | 69.25%          | 60.25%              | +9.00%     | -4.75%            | -10.00%                |
| 256       | 255         | 68.00%          | 55.50%              | +12.50%    | -6.00%            | -14.75%                |
| 512       | 511         | 63.00%          | 48.00%              | +15.00%    | -11.00%           | -22.25%                |
| 1024      | 1023        | N/A*            | N/A*                | --         | (context limit)   | (context limit)        |

*Both models exceeded context window at 1024 functions

## Key Findings

### Performance Differences
- **Baseline advantage**: GPT-4o starts 3.75% higher (74% vs 70.25%)
- **Robustness gap widens**: Difference grows from 3% to 15% as pool size increases
- **Critical threshold**: GPT-4o maintains ~70% through pool 128, while GPT-4o-mini drops to 60%

### Degradation Patterns
- **GPT-4o**: Relatively stable (-4 to -6%) until pool 256, then larger drop at 512 (-11% total)
- **GPT-4o-mini**: Accelerating degradation, especially severe beyond pool 128 (-22% total at 512)

### Robustness Factor
At pool 512:
- GPT-4o: 63% (15% drop from baseline)
- GPT-4o-mini: 48% (22% drop from baseline)
- **GPT-4o is ~2x more robust** (retains 85% of baseline vs 68% for gpt-4o-mini)

### Context Window
Both models hit the same practical limit at 1024 functions despite GPT-4o's theoretically larger context window. This suggests the constraint may be about token count in the formatted tool descriptions rather than raw context capacity.

## Implications

1. **Cost-performance tradeoff**: GPT-4o costs ~20x more but provides ~2x better robustness in large function pools
2. **Use case guidance**: 
   - Small pools (<128 functions): GPT-4o-mini acceptable
   - Large pools (>256 functions): GPT-4o recommended
3. **System design**: Both models need function filtering/ranking for 500+ tool scenarios


