# BFCL Thousand Tools - Scaling Experiment Results

**Model:** gpt-4o-mini-2024-07-18  
**Test Category:** simple_python  
**Date:** 2026-01-11  
**Researcher:** Marcus Sullivan

## Complete Scaling Curve (Validated)

| Pool Size | Distractors | Total Tests | Correct | Accuracy | vs Baseline | vs Previous |
|-----------|-------------|-------------|---------|----------|-------------|-------------|
| 0         | 0           | 400         | 281     | 70.25%   | --          | --          |
| 16        | 15          | 400         | 268     | 67.00%   | -3.25%      | -3.25%      |
| 32        | 31          | 400         | 265     | 66.25%   | -4.00%      | -0.75%      |
| 64        | 63          | 400         | 253     | 63.25%   | -7.00%      | -3.00%      |
| 128       | 127         | 400         | 241     | 60.25%   | -10.00%     | -3.00%      |
| 256       | 255         | 400         | 222     | 55.50%   | -14.75%     | -4.75%      |
| 512       | 511         | 400         | 192     | 48.00%   | -22.25%     | -7.50%      |
| 1024      | 1023        | --          | --      | N/A      | --          | CONTEXT LIMIT |

## Key Findings

### 1. Non-Linear Performance Degradation
- Baseline accuracy: 70.25%
- Pool 512 accuracy: 48.00% (22.25% absolute drop)
- Degradation accelerates with scale

### 2. Accelerating Decline Pattern
- First doubling (0→16): -3.25%
- Second doubling (16→32): -0.75%
- Third doubling (32→64): -3.00%
- Fourth doubling (64→128): -3.00%
- Fifth doubling (128→256): -4.75%
- Sixth doubling (256→512): -7.50%

### 3. Context Window Constraint
- Pool 1024 (1023 distractors) exceeded gpt-4o-mini's context window
- Error: "Your input exceeds the context window of this model"
- Practical limit appears to be ~512 functions for this model

### 4. Critical Thresholds
- **Minor degradation zone**: 0-32 functions (~4% drop)
- **Moderate degradation zone**: 32-128 functions (~10% drop total)
- **Severe degradation zone**: 128-512 functions (~22% drop total)
- **Context limit**: Beyond 512 functions

## Implications

1. **Model Selection**: Models with larger context windows needed for 1000+ function scenarios
2. **System Design**: Function filtering/ranking critical for large tool sets
3. **Performance Expectations**: ~50% accuracy ceiling with 500+ functions
4. **Evaluation Methodology**: Validated that LLM judge evaluation works across all pool sizes

## Next Steps (Recommended)

1. Test models with larger context windows (GPT-4, Claude 3.5)
2. Investigate function filtering/ranking strategies
3. Analyze which types of functions cause most confusion
4. Test with other test categories (parallel, multiple functions, etc.)

---

**Pipeline Validated:** ✓  
**Evaluation Method:** LLM Judge (GPT-4o)  
**All Data Files:** Available in `eval_results_pool*.json`
