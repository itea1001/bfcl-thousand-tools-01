# Prompt Variation × Scaling Experiments

## Overview

This experiment tests whether **prompt format sensitivity** interacts with **function pool scaling**.

### Research Question

Do models become more or less sensitive to prompt format variations (JSON vs XML, tagged vs untagged) as we increase the number of distractor functions?

### Motivation

From the BFCL Prompt Variation project, we know:
- Smaller models are 2-3x more sensitive to format variations
- Tagged formats hurt OpenAI models but help Grok models
- Format sensitivity varies by ~8-20pp depending on model size

From our Thousand Tools project, we know:
- Performance degrades as pool size increases
- gpt-4o-mini drops from 92% → 48% (pool 0 → 512)
- Parameter precision is the main failure mode (not retrieval)

**Open question**: Does format sensitivity *change* as cognitive load increases from more distractors?

### Hypotheses

**H1**: Format sensitivity increases with pool size
- As models struggle with more functions, format becomes a heavier burden
- Prediction: Format variation gap widens at pool 512 vs pool 0

**H2**: Format sensitivity decreases with pool size
- Performance degradation dominates; format becomes less significant
- Prediction: All formats converge to lower accuracy at high pool sizes

**H3**: No interaction
- Format and pool size are independent factors
- Prediction: Format effects remain constant across pool sizes

## Experimental Design

### Models
- **gpt-4o-mini-2024-07-18**: Showed highest degradation in scaling experiments

### Pool Sizes
- **0** (baseline): Original BFCL simple_python test set
- **128** (moderate): Mid-range scaling
- **512** (high): Near the breaking point for mini models

### Format Variations (5 key combinations)
1. `json+json` - Our baseline (what we've been using)
2. `json_tagged+json` - Tagged response format (known to hurt OpenAI)
3. `xml+xml` - Different format entirely
4. `python+python` - Python code format
5. `json+python` - Mixed formats

Total: 1 model × 3 pool sizes × 5 variations = **15 runs**

## Expected Results

### If H1 (sensitivity increases):
```
Pool 0:   json=92%, xml=88%  (4pp gap)
Pool 128: json=70%, xml=60%  (10pp gap)
Pool 512: json=48%, xml=30%  (18pp gap)
```

### If H2 (sensitivity decreases):
```
Pool 0:   json=92%, xml=88%  (4pp gap)
Pool 128: json=70%, xml=68%  (2pp gap)
Pool 512: json=48%, xml=47%  (1pp gap)
```

### If H3 (no interaction):
```
Pool 0:   json=92%, xml=88%  (4pp gap)
Pool 128: json=70%, xml=66%  (4pp gap)
Pool 512: json=48%, xml=44%  (4pp gap)
```

## Running the Experiment

### Setup
```bash
cd /home/mingxuanl/mingxuanl/simulation/ryanjones/bfcl-thousand-tools-01
conda activate bfcl-thousand-02

# Ensure scaled test files are linked
ls -la berkeley-function-call-leaderboard/bfcl_eval/data/BFCL_v4_simple_python_pool*.json
```

### Run Full Experiment
```bash
python scripts/run_prompt_variation_scaling.py
```

This will:
1. Generate predictions for all 15 combinations
2. Evaluate each using BFCL's scoring system
3. Save results to `prompt_variation_scaling_results.json`
4. Print summary table

### Expected Runtime
- Generation: ~5-10 min per run × 15 = **1.5-2.5 hours**
- Evaluation: ~2-5 min per run × 15 = **30-75 minutes**
- **Total: 2-3.5 hours**

## Analysis Plan

### Primary Metrics
1. **Accuracy by pool size and format**
2. **Format sensitivity gap** = max_accuracy - min_accuracy for each pool size
3. **Interaction effect**: Compare sensitivity gaps across pool sizes

### Visualization
- Line plot: pool size (x-axis) vs accuracy (y-axis), separate lines per format
- Bar plot: format sensitivity (y-axis) at each pool size (x-axis)
- Heatmap: accuracy as a function of pool size and format

### Statistical Tests
- Two-way ANOVA: pool_size × format → accuracy
- Look for significant interaction term

## File Structure

```
scripts/
  run_prompt_variation_scaling.py  - Main experiment script

berkeley-function-call-leaderboard/bfcl_eval/data/
  BFCL_v4_simple_python.json           - Pool 0 (baseline)
  BFCL_v4_simple_python_pool128.json   - Pool 128
  BFCL_v4_simple_python_pool512.json   - Pool 512

berkeley-function-call-leaderboard/
  result_pool{N}_{res_fmt}_{doc_fmt}/  - Generated predictions
  score_pool{N}_{res_fmt}_{doc_fmt}/   - Evaluation scores

prompt_variation_scaling_results.json  - Consolidated results
```

## Next Steps After Results

1. **Analyze interaction effects** - Which hypothesis is supported?
2. **Extend to GPT-4o** - Does larger model show different pattern?
3. **Test on other categories** - parallel, multiple, parallel_multiple
4. **Deep dive on failures** - How do failure modes differ by format?

## Connection to Other Work

### BFCL Prompt Variation Project
- Repo: https://github.com/itea1001/bfcl-pv-01
- Tested 18 variations × 8 categories × 10+ models
- Found format sensitivity varies 2-3x between model sizes

### Our Thousand Tools Project
- Tested scaling from 0 to 1024 functions
- Found parameter precision (not retrieval) is key failure
- Identified 64-function threshold for degradation onset

**This experiment bridges the two projects** by testing if format effects persist/change under scaling pressure.

## Implementation Notes

### Using BFCL's Prompt Variation System

The BFCL framework supports prompt variations via the `--prompt-variation` flag:
```bash
python -m bfcl_eval generate \
  --model gpt-4o-mini-2024-07-18 \
  --test-category BFCL_v4_simple_python_pool128 \
  --prompt-variation "res_fmt=json_tagged,doc_fmt=json"
```

This modifies:
- **Response format** (res_fmt): How the model is asked to format its output
- **Documentation format** (doc_fmt): How function definitions are presented

### Format Specifications

**Response formats:**
- `json`: Standard JSON function call format
- `json_tagged`: JSON with `<function_call>` tags
- `xml`: XML-style function calls
- `python`: Python function call syntax
- (also: `python_tagged`, `xml_tagged`)

**Doc formats:**
- `json`: JSON schema format (OpenAI style)
- `python`: Python docstring format
- `xml`: XML schema format

### Baseline Comparison

Our standard experiments use `json+json` (implicit default).
This experiment explicitly tests variations to measure sensitivity.

