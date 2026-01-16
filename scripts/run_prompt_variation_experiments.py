#!/usr/bin/env python3
"""
Run prompt variation experiments on scaled test sets.
Tests if format sensitivity changes with more distractor functions.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../berkeley-function-call-leaderboard'))

from pathlib import Path
import subprocess

# Add the BFCL path
BFCL_DIR = Path(__file__).parent.parent / "berkeley-function-call-leaderboard"

# Configuration
MODEL = "gpt-4o-mini-2024-07-18"
VARIATIONS = [
    ("json", "json"),           # Baseline
    ("json_tagged", "json"),    # Tagged (known to hurt OpenAI)
    ("xml", "xml"),             # Different format
]
POOL_SIZES = [0, 128, 512]  # baseline, moderate, high

def run_experiment(pool_size, res_fmt, doc_fmt):
    """Run one experiment configuration"""
    
    # Determine test category
    if pool_size == 0:
        test_cat = "BFCL_v4_simple_python"
        pool_name = "baseline"
    else:
        test_cat = f"BFCL_v4_simple_python_pool{pool_size}"
        pool_name = f"pool{pool_size}"
    
    result_dir = f"result_{pool_name}_{res_fmt}_{doc_fmt}"
    score_dir = f"score_{pool_name}_{res_fmt}_{doc_fmt}"
    
    variation_str = f"res_fmt={res_fmt},doc_fmt={doc_fmt}"
    
    print(f"\n{'='*70}")
    print(f"Pool: {pool_name}, Format: {res_fmt}+{doc_fmt}")
    print(f"{'='*70}")
    
    # Run generation
    gen_cmd = [
        sys.executable, "-m", "bfcl_eval", "generate",
        "--model", MODEL,
        "--test-category", test_cat,
        "--prompt-variation", variation_str,
        "--result-dir", result_dir,
        "--num-threads", "8",
        "--allow-overwrite"
    ]
    
    print(f"Running generation...")
    try:
        result = subprocess.run(
            gen_cmd,
            cwd=BFCL_DIR,
            capture_output=True,
            text=True,
            timeout=1800
        )
        if result.returncode != 0:
            print(f"Generation failed: {result.stderr[:500]}")
            return None
    except Exception as e:
        print(f"Generation error: {e}")
        return None
    
    # Run evaluation
    eval_cmd = [
        sys.executable, "-m", "bfcl_eval", "evaluate",
        "--model", MODEL,
        "--test-category", test_cat,
        "--prompt-variation", variation_str,
        "--result-dir", result_dir,
        "--score-dir", score_dir
    ]
    
    print(f"Running evaluation...")
    try:
        result = subprocess.run(
            eval_cmd,
            cwd=BFCL_DIR,
            capture_output=True,
            text=True,
            timeout=900
        )
        if result.returncode != 0:
            print(f"Evaluation failed: {result.stderr[:500]}")
            return None
        
        # Extract accuracy from output
        for line in result.stdout.split('\n'):
            if 'accuracy' in line.lower() or '%' in line:
                print(f"Result: {line.strip()}")
        
        return result_dir
    except Exception as e:
        print(f"Evaluation error: {e}")
        return None

def main():
    print("\n" + "="*70)
    print("PROMPT VARIATION × SCALING EXPERIMENTS")
    print("="*70)
    print(f"Model: {MODEL}")
    print(f"Variations: {len(VARIATIONS)}")
    print(f"Pool sizes: {len(POOL_SIZES)}")
    print(f"Total: {len(VARIATIONS) * len(POOL_SIZES)} experiments")
    print("="*70 + "\n")
    
    results = []
    
    for pool in POOL_SIZES:
        print(f"\n{'#'*70}")
        print(f"# POOL SIZE: {pool}")
        print(f"{'#'*70}\n")
        
        for res_fmt, doc_fmt in VARIATIONS:
            result = run_experiment(pool, res_fmt, doc_fmt)
            results.append({
                'pool': pool,
                'res_fmt': res_fmt,
                'doc_fmt': doc_fmt,
                'result_dir': result
            })
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    successful = sum(1 for r in results if r['result_dir'] is not None)
    print(f"Completed: {successful}/{len(results)} experiments")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()


