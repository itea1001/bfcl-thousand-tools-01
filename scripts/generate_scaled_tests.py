#!/usr/bin/env python3
"""
Generate scaled test datasets with varying numbers of available functions.
For each test case from BFCL, we create versions with different function pool sizes.
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any
import copy

# Define paths
PROJECT_ROOT = Path(__file__).parent.parent
BFCL_DATA_DIR = PROJECT_ROOT / "berkeley-function-call-leaderboard" / "bfcl_eval" / "data"
FUNCTION_POOL_FILE = PROJECT_ROOT / "data" / "function_pool" / "all_unique_functions.json"
OUTPUT_DIR = PROJECT_ROOT / "data" / "scaled_tests"

# Function pool sizes to generate
POOL_SIZES = [16, 32, 64, 128, 256, 512, 1024]

# Base test categories to use (start with simple python)
BASE_TEST_CATEGORY = "BFCL_v4_simple_python.json"

# Random seed for reproducibility
RANDOM_SEED = 42


def load_jsonl(file_path: Path) -> List[Dict[str, Any]]:
    """Load JSONL file (one JSON object per line)."""
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def save_jsonl(data: List[Dict[str, Any]], file_path: Path):
    """Save data as JSONL file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')


def load_function_pool() -> List[Dict[str, Any]]:
    """Load the unique function pool."""
    with open(FUNCTION_POOL_FILE, 'r') as f:
        data = json.load(f)
    # Extract just the functions (without metadata)
    return [item['function'] for item in data]


def generate_scaled_test_set(
    base_tests: List[Dict[str, Any]],
    all_functions: List[Dict[str, Any]],
    pool_size: int,
    num_tests: int = 100
) -> List[Dict[str, Any]]:
    """
    Generate a test set with a specific function pool size.
    
    For each test:
    - Keep the original question and ground truth function
    - Add (pool_size - 1) random distractor functions
    """
    scaled_tests = []
    
    # Sample test cases (limit to num_tests for efficiency)
    selected_tests = random.sample(base_tests, min(num_tests, len(base_tests)))
    
    for idx, original_test in enumerate(selected_tests):
        # Copy the test case
        new_test = copy.deepcopy(original_test)
        
        # Get the original function(s)
        original_functions = new_test.get('function', [])
        num_original = len(original_functions)
        
        # We need to add (pool_size - num_original) distractor functions
        num_distractors = pool_size - num_original
        
        if num_distractors > 0:
            # Sample random functions as distractors
            # Avoid duplicates with original functions
            original_func_names = {f['name'] for f in original_functions}
            candidate_distractors = [
                f for f in all_functions 
                if f['name'] not in original_func_names
            ]
            
            if len(candidate_distractors) >= num_distractors:
                distractors = random.sample(candidate_distractors, num_distractors)
                # Add distractors to function list
                new_test['function'] = original_functions + distractors
                
                # Shuffle so ground truth isn't always first
                random.shuffle(new_test['function'])
            else:
                print(f"Warning: Not enough unique functions for pool size {pool_size}, skipping test {original_test['id']}")
                continue
        
        # Update test ID to indicate pool size
        new_test['id'] = f"{original_test['id']}_pool{pool_size}"
        new_test['pool_size'] = pool_size
        
        scaled_tests.append(new_test)
    
    return scaled_tests


def main():
    """Generate all scaled test sets."""
    random.seed(RANDOM_SEED)
    
    print("Loading function pool...")
    all_functions = load_function_pool()
    print(f"Loaded {len(all_functions)} unique functions")
    
    print(f"\nLoading base test category: {BASE_TEST_CATEGORY}")
    base_test_path = BFCL_DATA_DIR / BASE_TEST_CATEGORY
    base_tests = load_jsonl(base_test_path)
    print(f"Loaded {len(base_tests)} test cases")
    
    # Generate scaled test sets for each pool size
    for pool_size in POOL_SIZES:
        print(f"\nGenerating tests with pool size: {pool_size}")
        
        scaled_tests = generate_scaled_test_set(
            base_tests=base_tests,
            all_functions=all_functions,
            pool_size=pool_size,
            num_tests=100  # Sample 100 tests per pool size
        )
        
        print(f"  Generated {len(scaled_tests)} test cases")
        
        # Save to file
        output_file = OUTPUT_DIR / f"simple_python_pool{pool_size}.json"
        save_jsonl(scaled_tests, output_file)
        print(f"  Saved to: {output_file}")
    
    print("\n=== Summary ===")
    print(f"Generated scaled test sets for pool sizes: {POOL_SIZES}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

