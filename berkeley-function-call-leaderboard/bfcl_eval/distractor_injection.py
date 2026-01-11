"""
Utility functions for injecting distractor functions into test cases
to scale the number of available functions dynamically.
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any
import copy

# Path to the function pool
FUNCTION_POOL_PATH = Path(__file__).parent.parent.parent / "data" / "function_pool" / "all_unique_functions.json"


def load_function_pool() -> List[Dict[str, Any]]:
    """
    Load the pool of unique functions that can be used as distractors.
    Returns a list of function definitions.
    """
    if not FUNCTION_POOL_PATH.exists():
        raise FileNotFoundError(
            f"Function pool not found at {FUNCTION_POOL_PATH}. "
            "Please run scripts/extract_functions.py first to generate the function pool."
        )
    
    with open(FUNCTION_POOL_PATH, 'r') as f:
        data = json.load(f)
    
    # Extract just the function definitions (without metadata)
    return [item['function'] for item in data]


def inject_distractor_functions(
    test_entries: List[Dict[str, Any]],
    num_distractors: int,
    random_seed: int = 42
) -> List[Dict[str, Any]]:
    """
    Inject distractor functions into each test entry to increase the function pool size.
    
    Args:
        test_entries: List of test entries from BFCL dataset
        num_distractors: Number of distractor functions to add to each test case
        random_seed: Random seed for reproducibility
        
    Returns:
        Modified test entries with additional distractor functions
    """
    if num_distractors <= 0:
        return test_entries
    
    random.seed(random_seed)
    
    # Load the function pool
    function_pool = load_function_pool()
    
    modified_entries = []
    
    for entry in test_entries:
        # Deep copy to avoid modifying original
        modified_entry = copy.deepcopy(entry)
        
        # Get existing functions
        existing_functions = modified_entry.get('function', [])
        
        if not existing_functions:
            # No functions in this entry, skip
            modified_entries.append(modified_entry)
            continue
        
        # Get names of existing functions to avoid duplicates
        existing_func_names = {func['name'] for func in existing_functions}
        
        # Filter out functions that are already in the test case
        candidate_distractors = [
            func for func in function_pool
            if func['name'] not in existing_func_names
        ]
        
        if len(candidate_distractors) < num_distractors:
            print(
                f"Warning: Not enough unique distractor functions available for test {entry.get('id', 'unknown')}. "
                f"Requested {num_distractors}, but only {len(candidate_distractors)} available. "
                f"Using all available distractors."
            )
            num_to_sample = len(candidate_distractors)
        else:
            num_to_sample = num_distractors
        
        # Sample distractor functions
        distractors = random.sample(candidate_distractors, num_to_sample)
        
        # Add distractors to the function list
        modified_entry['function'] = existing_functions + distractors
        
        # Shuffle to randomize order (so ground truth isn't always first)
        random.shuffle(modified_entry['function'])
        
        # Add metadata about the injection
        modified_entry['_num_distractors_injected'] = num_to_sample
        modified_entry['_original_num_functions'] = len(existing_functions)
        modified_entry['_total_functions'] = len(modified_entry['function'])
        
        modified_entries.append(modified_entry)
    
    return modified_entries

