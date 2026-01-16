#!/usr/bin/env python3
"""
Manual test for prompt variation sensitivity across different pool sizes.
Tests if format sensitivity changes when more distractor functions are present.
"""

import json
import os
import sys
from pathlib import Path
from openai import OpenAI

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "berkeley-function-call-leaderboard"))
from bfcl_eval.constants.prompt_variations import (
    JSON_FORMAT_INSTRUCTION,
    JSON_TAGGED_FORMAT_INSTRUCTION,
    XML_FORMAT_INSTRUCTION,
)

# Test configuration
MODEL = "gpt-4o-mini-2024-07-18"
NUM_SAMPLES = 400  # Test on 400 samples per configuration
TEMPERATURE = 0.001

# Format variations to test
FORMATS = {
    "json": JSON_FORMAT_INSTRUCTION,
    "json_tagged": JSON_TAGGED_FORMAT_INSTRUCTION,
    "xml": XML_FORMAT_INSTRUCTION,
}

def load_test_data(pool_size):
    """Load test data for a given pool size."""
    if pool_size == 0:
        filepath = Path(__file__).parent.parent / "berkeley-function-call-leaderboard/bfcl_eval/data/BFCL_v4_simple_python.json"
    else:
        filepath = Path(__file__).parent.parent / f"data/scaled_tests/simple_python_pool{pool_size}.json"
    
    # Try loading as JSONL first (baseline format)
    data = []
    with open(filepath, 'r') as f:
        first_line = f.readline()
        f.seek(0)
        try:
            # Try as JSONL
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        except:
            # Fall back to JSON array
            f.seek(0)
            data = json.load(f)
    
    return data[:NUM_SAMPLES]  # Take first N samples

def create_prompt(test_case, format_instruction):
    """Create a prompt with the given format instruction."""
    base_prompt = """You are an expert in composing functions. You are given a question and a set of possible functions. Based on the question, you will need to make one or more function/tool calls to achieve the purpose.
If none of the functions can be used, point it out. If the given question lacks the parameters required by the function, also point it out.
You should only return the function calls in your response.
"""
    
    system_prompt = base_prompt + format_instruction
    
    # Format the available functions
    functions_str = "\n\n".join([
        f"Function: {func['name']}\n{func.get('description', '')}\nParameters: {json.dumps(func.get('parameters', {}), indent=2)}"
        for func in test_case.get('function', [])
    ])
    
    user_message = f"""Here are the available functions:

{functions_str}

Question: {test_case['question']}"""
    
    return system_prompt, user_message

def run_single_test(client, test_case, format_name, format_instruction):
    """Run a single test with the given format."""
    system_prompt, user_message = create_prompt(test_case, format_instruction)
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=TEMPERATURE,
        )
        
        result = response.choices[0].message.content
        return {
            "test_id": test_case.get('id'),
            "format": format_name,
            "response": result,
            "success": True
        }
    except Exception as e:
        return {
            "test_id": test_case.get('id'),
            "format": format_name,
            "error": str(e),
            "success": False
        }

def main():
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set")
        return
    
    client = OpenAI()
    
    results = []
    
    print("="*70)
    print("MANUAL PROMPT VARIATION TEST")
    print("="*70)
    print(f"Model: {MODEL}")
    print(f"Samples per config: {NUM_SAMPLES}")
    print(f"Formats: {list(FORMATS.keys())}")
    print(f"Pool sizes: [0, 512]")
    print("="*70 + "\n")
    
    for pool_size in [0, 512]:
        print(f"\n{'#'*70}")
        print(f"# Testing pool size: {pool_size}")
        print(f"{'#'*70}\n")
        
        # Load test data
        test_data = load_test_data(pool_size)
        print(f"Loaded {len(test_data)} test cases")
        
        for format_name, format_instruction in FORMATS.items():
            print(f"\n  Testing format: {format_name}")
            
            for i, test_case in enumerate(test_data):
                result = run_single_test(client, test_case, format_name, format_instruction)
                result['pool_size'] = pool_size
                results.append(result)
                
                if (i + 1) % 5 == 0:
                    print(f"    Completed {i + 1}/{len(test_data)} tests")
    
    # Save results
    output_file = Path(__file__).parent.parent / "manual_prompt_variation_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print("Results saved to:", output_file)
    print("="*70)
    
    # Quick summary
    print("\nSummary:")
    for pool_size in [0, 512]:
        for format_name in FORMATS.keys():
            pool_format_results = [r for r in results if r['pool_size'] == pool_size and r['format'] == format_name]
            success_count = sum(1 for r in pool_format_results if r['success'])
            print(f"  Pool {pool_size:3d}, {format_name:12s}: {success_count}/{len(pool_format_results)} successful")

if __name__ == "__main__":
    main()

