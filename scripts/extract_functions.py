#!/usr/bin/env python3
"""
Extract all unique functions from BFCL dataset and analyze the function pool.
"""

import json
import hashlib
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any

# Define paths
BFCL_DATA_DIR = Path(__file__).parent.parent / "berkeley-function-call-leaderboard" / "bfcl_eval" / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "function_pool"

# Test categories to extract from
TEST_CATEGORIES = [
    "BFCL_v4_simple_python.json",
    "BFCL_v4_multiple.json",
    "BFCL_v4_parallel.json",
    "BFCL_v4_parallel_multiple.json",
    "BFCL_v4_live_simple.json",
    "BFCL_v4_live_multiple.json",
    "BFCL_v4_live_parallel.json",
    "BFCL_v4_live_parallel_multiple.json",
]


def load_jsonl(file_path: Path) -> List[Dict[str, Any]]:
    """Load JSONL file (one JSON object per line)."""
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def function_hash(func: Dict[str, Any]) -> str:
    """Create a hash for a function to identify duplicates."""
    # Use name and parameters as unique identifier
    key_info = {
        "name": func.get("name", ""),
        "description": func.get("description", ""),
        "parameters": func.get("parameters", {})
    }
    func_str = json.dumps(key_info, sort_keys=True)
    return hashlib.md5(func_str.encode()).hexdigest()


def extract_all_functions():
    """Extract all unique functions from BFCL test files."""
    unique_functions = {}  # hash -> function
    function_sources = defaultdict(list)  # hash -> list of (category, test_id)
    
    print("Extracting functions from BFCL test categories...")
    
    for category_file in TEST_CATEGORIES:
        file_path = BFCL_DATA_DIR / category_file
        if not file_path.exists():
            print(f"  Warning: {category_file} not found, skipping")
            continue
        
        test_entries = load_jsonl(file_path)
        print(f"  Processing {category_file}: {len(test_entries)} test cases")
        
        for entry in test_entries:
            test_id = entry.get("id", "unknown")
            functions = entry.get("function", [])
            
            for func in functions:
                func_hash_val = function_hash(func)
                
                # Store unique function
                if func_hash_val not in unique_functions:
                    unique_functions[func_hash_val] = func
                
                # Track source
                function_sources[func_hash_val].append((category_file, test_id))
    
    print(f"\nTotal unique functions extracted: {len(unique_functions)}")
    
    # Save results
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save unique functions
    functions_list = []
    for func_hash, func in unique_functions.items():
        func_with_meta = {
            "hash": func_hash,
            "function": func,
            "sources": function_sources[func_hash]
        }
        functions_list.append(func_with_meta)
    
    output_file = OUTPUT_DIR / "all_unique_functions.json"
    with open(output_file, 'w') as f:
        json.dump(functions_list, f, indent=2)
    
    print(f"Saved unique functions to: {output_file}")
    
    # Statistics
    print("\n=== Function Statistics ===")
    print(f"Total unique functions: {len(unique_functions)}")
    
    # Count functions by category
    category_counts = defaultdict(int)
    for func_hash, sources in function_sources.items():
        for category, _ in sources:
            category_counts[category] += 1
    
    print("\nFunctions per category (may have duplicates across categories):")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count}")
    
    return unique_functions, function_sources


if __name__ == "__main__":
    extract_all_functions()

