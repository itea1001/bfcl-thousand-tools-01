#!/usr/bin/env python3
"""
Test prompt variations at different pool sizes to see if format sensitivity
interacts with the number of distractor functions.

This script integrates the prompt variation approach with our scaling experiments.
"""

import subprocess
import json
from pathlib import Path
from typing import List, Dict

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
BFCL_DIR = PROJECT_ROOT / "berkeley-function-call-leaderboard"

# Test configuration
MODELS = ["gpt-4o-mini-2024-07-18"]  # Start with mini since it showed most degradation
POOL_SIZES = [0, 128, 512]  # Baseline, moderate, high scaling

# Key format variations to test (subset of the 18 total variations)
# We'll test 5 key combinations to see format sensitivity changes:
VARIATIONS = [
    ("json", "json"),           # Baseline - what we've been using
    ("json_tagged", "json"),    # Tagged response (found to hurt OpenAI models)
    ("xml", "xml"),             # Different format entirely
    ("python", "python"),       # Python format
    ("json", "python"),         # Mixed: json response, python docs
]

CATEGORY = "simple_python"  # Focus on one category for initial testing


def run_generation(model: str, pool_size: int, res_fmt: str, doc_fmt: str) -> Dict:
    """
    Run generation for a specific model, pool size, and format variation.
    Returns metrics about the run.
    """
    variation_str = f"res_fmt={res_fmt},doc_fmt={doc_fmt}"
    result_dir = f"result_pool{pool_size}_{res_fmt}_{doc_fmt}"
    
    # Determine which test file to use
    if pool_size == 0:
        test_category = "BFCL_v4_simple_python"  # Original baseline
    else:
        test_category = f"BFCL_v4_simple_python_pool{pool_size}"
    
    cmd = [
        "python", "-m", "bfcl_eval", "generate",
        "--model", model,
        "--test-category", test_category,
        "--prompt-variation", variation_str,
        "--result-dir", result_dir,
        "--num-threads", "8",
        "--allow-overwrite"
    ]
    
    print(f"\n{'='*70}")
    print(f"Running: pool={pool_size}, res_fmt={res_fmt}, doc_fmt={doc_fmt}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=BFCL_DIR,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        if result.returncode != 0:
            print(f"ERROR: Generation failed with code {result.returncode}")
            print(f"STDERR: {result.stderr}")
            return {"status": "failed", "error": result.stderr}
        
        return {"status": "success"}
        
    except subprocess.TimeoutExpired:
        print("ERROR: Generation timed out after 1 hour")
        return {"status": "timeout"}
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {"status": "error", "error": str(e)}


def run_evaluation(model: str, pool_size: int, res_fmt: str, doc_fmt: str) -> Dict:
    """
    Run evaluation for a specific model, pool size, and format variation.
    Returns accuracy metrics.
    """
    variation_str = f"res_fmt={res_fmt},doc_fmt={doc_fmt}"
    result_dir = f"result_pool{pool_size}_{res_fmt}_{doc_fmt}"
    score_dir = f"score_pool{pool_size}_{res_fmt}_{doc_fmt}"
    
    # Determine which test file to use
    if pool_size == 0:
        test_category = "BFCL_v4_simple_python"
    else:
        test_category = f"BFCL_v4_simple_python_pool{pool_size}"
    
    cmd = [
        "python", "-m", "bfcl_eval", "evaluate",
        "--model", model,
        "--test-category", test_category,
        "--prompt-variation", variation_str,
        "--result-dir", result_dir,
        "--score-dir", score_dir
    ]
    
    print(f"\n{'='*70}")
    print(f"Evaluating: pool={pool_size}, res_fmt={res_fmt}, doc_fmt={doc_fmt}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=BFCL_DIR,
            capture_output=True,
            text=True,
            timeout=1800  # 30 min timeout
        )
        
        if result.returncode != 0:
            print(f"ERROR: Evaluation failed with code {result.returncode}")
            print(f"STDERR: {result.stderr}")
            return {"status": "failed", "error": result.stderr}
        
        # Parse accuracy from output
        output = result.stdout
        accuracy = None
        for line in output.split('\n'):
            if 'accuracy' in line.lower() or 'score' in line.lower():
                # Try to extract percentage
                import re
                match = re.search(r'(\d+\.?\d*)%', line)
                if match:
                    accuracy = float(match.group(1))
                    break
        
        return {
            "status": "success",
            "accuracy": accuracy,
            "output": output
        }
        
    except subprocess.TimeoutExpired:
        print("ERROR: Evaluation timed out")
        return {"status": "timeout"}
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {"status": "error", "error": str(e)}


def main():
    """
    Main experiment: test format variations at different pool sizes.
    """
    print("\n" + "="*70)
    print("PROMPT VARIATION × SCALING EXPERIMENT")
    print("="*70)
    print(f"Models: {MODELS}")
    print(f"Pool sizes: {POOL_SIZES}")
    print(f"Variations: {len(VARIATIONS)}")
    print(f"Total runs: {len(MODELS) * len(POOL_SIZES) * len(VARIATIONS)}")
    print("="*70 + "\n")
    
    # Results storage
    results = []
    
    for model in MODELS:
        print(f"\n{'#'*70}")
        print(f"# MODEL: {model}")
        print(f"{'#'*70}\n")
        
        for pool_size in POOL_SIZES:
            print(f"\n{'-'*70}")
            print(f"POOL SIZE: {pool_size}")
            print(f"{'-'*70}\n")
            
            for res_fmt, doc_fmt in VARIATIONS:
                # Run generation
                gen_result = run_generation(model, pool_size, res_fmt, doc_fmt)
                
                # Run evaluation if generation succeeded
                eval_result = {"status": "skipped"}
                if gen_result["status"] == "success":
                    eval_result = run_evaluation(model, pool_size, res_fmt, doc_fmt)
                
                # Store results
                result_entry = {
                    "model": model,
                    "pool_size": pool_size,
                    "response_format": res_fmt,
                    "doc_format": doc_fmt,
                    "generation": gen_result,
                    "evaluation": eval_result
                }
                results.append(result_entry)
                
                # Print summary
                status = eval_result.get("status", "unknown")
                accuracy = eval_result.get("accuracy", "N/A")
                print(f"\n✓ Completed: pool={pool_size}, {res_fmt}+{doc_fmt}, accuracy={accuracy}%")
    
    # Save results
    output_file = PROJECT_ROOT / "prompt_variation_scaling_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"All experiments complete!")
    print(f"Results saved to: {output_file}")
    print(f"{'='*70}\n")
    
    # Print summary table
    print("\nSUMMARY TABLE")
    print("-" * 70)
    print(f"{'Pool':<8} {'Format':<20} {'Accuracy':<10} {'Status':<10}")
    print("-" * 70)
    for r in results:
        pool = r['pool_size']
        fmt = f"{r['response_format']}+{r['doc_format']}"
        acc = r['evaluation'].get('accuracy', 'N/A')
        status = r['evaluation'].get('status', 'unknown')
        print(f"{pool:<8} {fmt:<20} {acc:<10} {status:<10}")
    print("-" * 70)


if __name__ == "__main__":
    main()

