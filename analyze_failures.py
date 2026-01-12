#!/usr/bin/env python3
"""
Analyze failure modes in pool 512 predictions.
Categorizes failures into: wrong function, hallucinated function, parameter errors, etc.
"""

import json
from collections import defaultdict

def load_ground_truth_functions(pool512_file):
    """Load the set of available functions from the test data."""
    # For now, we'll extract from eval results
    return set()

def categorize_failure(result):
    """
    Categorize a failure based on the reasoning.
    Returns: category string
    """
    reasoning = result['reasoning'].lower()
    pred_func = result.get('prediction', {}).get('name', '')
    
    # Ground truth is a list, get first function name
    gt = result.get('ground_truth', [])
    if isinstance(gt, list) and len(gt) > 0:
        gt_func = list(gt[0].keys())[0] if isinstance(gt[0], dict) else ''
    else:
        gt_func = ''
    
    # Check for completely wrong function (unrelated task)
    if 'unrelated' in reasoning or 'different task' in reasoning:
        return 'wrong_function'
    
    # Check for hallucinated/non-existent function
    if 'does not exist' in reasoning or 'hallucinated' in reasoning:
        return 'hallucinated'
    
    # Check for missing parameters
    if 'missing' in reasoning:
        return 'missing_params'
    
    # Check for wrong parameters
    if 'incorrect' in reasoning or 'wrong' in reasoning:
        return 'wrong_params'
    
    # Check for different but similar function
    if 'different function' in reasoning:
        return 'different_function'
    
    # Default: parameter/detail issue
    return 'param_issue'

def analyze_failures(eval_file, predictions_file):
    """Main analysis function."""
    
    # Load data
    with open(eval_file, 'r') as f:
        eval_data = json.load(f)
    
    with open(predictions_file, 'r') as f:
        predictions = [json.loads(line) for line in f if line.strip()]
    
    # Create prediction lookup
    pred_map = {p['test_id']: p for p in predictions}
    
    # Analyze failures
    failure_categories = defaultdict(list)
    
    for result in eval_data['results']:
        if not result['equivalent']:
            category = categorize_failure(result)
            
            # Extract ground truth function name
            gt = result.get('ground_truth', [])
            if isinstance(gt, list) and len(gt) > 0:
                gt_name = list(gt[0].keys())[0] if isinstance(gt[0], dict) else ''
            else:
                gt_name = ''
            
            failure_categories[category].append({
                'test_id': result['test_id'],
                'ground_truth': gt_name,
                'prediction': result.get('prediction', {}).get('name', ''),
                'reasoning': result['reasoning'][:200]
            })
    
    # Print summary
    print("=" * 70)
    print("FAILURE ANALYSIS - Pool 512 (gpt-4o-mini)")
    print("=" * 70)
    print(f"\nTotal tests: {eval_data['summary']['total_tests']}")
    print(f"Correct: {eval_data['summary']['correct']} ({eval_data['summary']['accuracy']:.1%})")
    print(f"Failed: {eval_data['summary']['incorrect']}")
    print()
    
    print("Failure Mode Breakdown:")
    print("-" * 70)
    
    sorted_categories = sorted(failure_categories.items(), key=lambda x: len(x[1]), reverse=True)
    
    for category, failures in sorted_categories:
        pct = len(failures) / eval_data['summary']['incorrect'] * 100
        print(f"\n{category.replace('_', ' ').title()}: {len(failures)} ({pct:.1f}%)")
        
        # Show 3 examples
        for i, example in enumerate(failures[:3]):
            print(f"  Example {i+1}:")
            print(f"    Test: {example['test_id']}")
            print(f"    Ground truth: {example['ground_truth']}")
            print(f"    Predicted: {example['prediction']}")
            print(f"    Reason: {example['reasoning']}")
    
    print("\n" + "=" * 70)
    
    # Key insights
    print("\nKEY INSIGHTS:")
    print("-" * 70)
    
    total_failures = eval_data['summary']['incorrect']
    
    # Calculate percentages
    wrong_func = len(failure_categories.get('wrong_function', []))
    hallucinated = len(failure_categories.get('hallucinated', []))
    param_issues = sum(len(v) for k, v in failure_categories.items() 
                       if 'param' in k)
    
    print(f"• Wrong function selected (unrelated task): {wrong_func} ({wrong_func/total_failures*100:.1f}%)")
    print(f"• Hallucinated functions: {hallucinated} ({hallucinated/total_failures*100:.1f}%)")
    print(f"• Parameter issues (correct function): {param_issues} ({param_issues/total_failures*100:.1f}%)")
    print()
    print("Primary issue: ", end="")
    if param_issues > wrong_func + hallucinated:
        print("Model picks correct/similar functions but makes parameter errors")
    elif wrong_func > param_issues:
        print("Model struggles with function selection (retrieval problem)")
    else:
        print("Mixed issues with both retrieval and parameter accuracy")

if __name__ == "__main__":
    analyze_failures('eval_results_pool512.json', 'predictions_pool512.jsonl')

