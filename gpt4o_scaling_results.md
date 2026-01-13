# GPT-4o Scaling Experiment Results

**Model:** gpt-4o-2024-11-20  
**Test Category:** simple_python  
**Date:** 2026-01-12  
**Researcher:** Marcus Sullivan

## Complete Scaling Curve

| Pool Size | Distractors | Total Tests | Correct | Accuracy | vs Baseline | vs gpt-4o-mini |
|-----------|-------------|-------------|---------|----------|-------------|----------------|
| 0         | 0           | 400         | 296     | 74.00%   | --          | +3.75%         |
| 16        | 15          | 400         | 280     | 70.00%   | -4.00%      | +3.00%         |
| 32        | 31          | 400         | 278     | 69.50%   | -4.50%      | +3.25%         |
| 64        | 63          | 400         | 279     | 69.75%   | -4.25%      | +6.50%         |
| 128       | 127         | 400         | 277     | 69.25%   | -4.75%      | +9.00%         |
| 256       | 255         | 400         | 260     | 65.00%   | -9.00%      | +9.50%         |
| 512       | 511         | 400         | 252     | 63.00%   | -11.00%     | +15.00%        |
| 1024      | 1023        | --          | --      | N/A      | --          | CONTEXT LIMIT  |

## Key Findings

### 1. Superior Baseline Performance
- GPT-4o baseline: 74.00%
- GPT-4o-mini baseline: 70.25%
- **+3.75% advantage** even without distractors

### 2. Much Better Robustness to Distractors
- GPT-4o at pool 512: 63.00% (11% drop from baseline)
- GPT-4o-mini at pool 512: 48.00% (22% drop from baseline)
- **GPT-4o is 2x more robust** to distractor functions

### 3. Consistent Performance in Mid-Range
- From pools 16-128, GPT-4o maintains ~69-70% accuracy
- Only ~1% variation across this range
- Suggests strong function discrimination capability

### 4. Graceful Degradation Pattern
- GPT-4o: Stable until pool 256, then moderate decline
- GPT-4o-mini: Continuous degradation, accelerating after pool 128
- **GPT-4o maintains >60% accuracy at 512 functions**

### 5. Same Context Window Limitation
- Both models hit context limit at 1024 functions
- Practical limit is ~512 functions for both architectures

## Model Comparison Summary

### Absolute Performance Gap
- Smallest gap: +3.00% at pool 16
- Largest gap: +15.00% at pool 512
- **Gap widens with scale** - GPT-4o's advantage increases as task difficulty grows

### Degradation Patterns
- GPT-4o: Flat until pool 128, then linear decline
- GPT-4o-mini: Continuous non-linear decline throughout

### Critical Thresholds
**GPT-4o:**
- Minor impact zone: 0-128 functions (~5% drop)
- Moderate impact zone: 128-512 functions (~11% drop total)

**GPT-4o-mini:**
- Minor impact zone: 0-32 functions (~4% drop)
- Severe impact zone: 128-512 functions (~22% drop total)

## Implications

1. **Model Selection for Production**
   - For <100 functions: Both models acceptable, GPT-4o-mini more cost-effective
   - For 100-500 functions: GPT-4o strongly recommended
   - For >500 functions: Both hit context limits, need alternative approaches

2. **Function Pool Management**
   - GPT-4o can handle 2-3x more functions than GPT-4o-mini before significant degradation
   - GPT-4o-mini requires aggressive function filtering above 128 functions
   - GPT-4o maintains acceptable performance up to 256 functions without filtering

3. **Architectural Differences**
   - GPT-4o appears to have better attention mechanisms for function discrimination
   - The flat performance from 16-128 suggests better handling of long contexts
   - GPT-4o's reasoning capabilities may help filter irrelevant functions

4. **Cost-Performance Tradeoff**
   - GPT-4o costs ~20x more than GPT-4o-mini per token
   - At pool 512: GPT-4o is 15% more accurate (63% vs 48%)
   - **Worth the cost for critical applications** with large function sets

## Next Steps

1. Test Claude Sonnet 4 (reported larger context window)
2. Investigate function filtering/ranking strategies for both models
3. Analyze which function characteristics cause confusion
4. Test with parallel and multiple function call scenarios

---

**Pipeline Validated:** ✓  
**Evaluation Method:** LLM Judge (GPT-4o)  
**All Data Files:** Available in `eval_results_gpt4o_pool*.json`

