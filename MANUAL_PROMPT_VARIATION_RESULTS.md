# Manual Prompt Variation Test Results

## Objective
Test whether format sensitivity changes as the number of distractor functions increases by comparing model performance across different prompt formats at baseline (pool 0) vs high distraction (pool 512).

## Methodology
- **Model**: gpt-4o-mini-2024-07-18
- **Formats Tested**: 
  - JSON (baseline format)
  - JSON Tagged (with `<tool_call>` wrapper)
  - XML (structured XML format)
- **Pool Sizes**: 0 (baseline), 512 (high distraction)
- **Sample Size**: 20 test cases per configuration
- **Total Tests**: 120 API calls (3 formats × 2 pool sizes × 20 samples)

## Results

### API Call Success Rate
All 120 tests completed successfully:
- Pool 0, JSON: 20/20 successful
- Pool 0, JSON Tagged: 20/20 successful
- Pool 0, XML: 20/20 successful
- Pool 512, JSON: 20/20 successful
- Pool 512, JSON Tagged: 20/20 successful
- Pool 512, XML: 20/20 successful

### Sample Responses

**Pool 0 - JSON Format:**
```json
{"function_name": "calculate_triangle_area", "parameters": {"base": 10, "height": 5}}
```

**Pool 0 - XML Format:**
```xml
<function_call>
    <name>calculate_triangle_area</name>
    <arguments>
        <arg name="base" type="int">10</arg>
        <arg name="height" type="int">5</arg>
    </arguments>
</function_call>
```

**Pool 512 - JSON Format:**
```json
{"function_name": "generate_dna_sequence", "parameters": {"length": 100, "preferences": ["G", "C"]}}
```

**Pool 512 - XML Format:**
```xml
<function_call>
    <name>generate_DNA_sequence</name>
    <arguments>
        <arg name="length" type="integer">100</arg>
        <arg name="preferences" type="array">["G", "C"]</arg>
    </arguments>
</function_call>
```

## Key Observations

1. **Format Compliance**: The model successfully generated responses in all three formats at both pool sizes, indicating it can follow format instructions regardless of the number of available functions.

2. **Response Structure**: All responses maintained proper structure:
   - JSON responses used correct key-value format
   - XML responses included proper tags and type attributes
   - Tagged formats correctly wrapped content in `<tool_call>` tags

3. **Next Steps Needed**: 
   - Parse and evaluate response correctness against ground truth
   - Calculate accuracy metrics for each format × pool size combination
   - Determine if certain formats degrade more than others with increased distractors

## Limitations

This initial test confirms the model can *generate* all formats, but doesn't yet measure *correctness*. A full evaluation pipeline would need to:
- Parse each response format
- Compare selected functions against ground truth
- Check parameter accuracy
- Calculate format-specific accuracy scores

## Files Generated
- `manual_prompt_variation_results.json`: Raw results with all 120 test responses
- `scripts/manual_prompt_variation_test.py`: Test script used for this experiment


