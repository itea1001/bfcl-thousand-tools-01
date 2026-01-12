#!/usr/bin/env python3
"""
LLM Judge-based evaluation for semantic equivalence checking.
Uses GPT-4o to determine if two function calls are semantically equivalent.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

JUDGE_MODEL = "gpt-4o"
JUDGE_TEMPERATURE = 0.0


JUDGE_SYSTEM_PROMPT = """You are an expert evaluator for function calling tasks. Your job is to determine if a predicted function call is semantically equivalent to the ground truth function call.

Two function calls are considered semantically equivalent if they would achieve the same goal, even if:
- The function names are different (e.g., 'calculate_area' vs 'compute_area')
- The parameter names are slightly different but have the same meaning
- The values/arguments are the same or equivalent

However, they are NOT equivalent if:
- They call fundamentally different functions
- They have different parameter values that would lead to different results
- Key required parameters are missing

You will receive:
1. The user's question/request
2. The ground truth function call (the correct answer)
3. The predicted function call (what the model generated)

Respond with a JSON object containing:
- "equivalent": true or false
- "reasoning": brief explanation of your decision
"""


def call_judge(
    question: str,
    ground_truth: Dict[str, Any],
    prediction: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Call GPT-4o judge to determine if prediction is semantically equivalent to ground truth.
    
    Args:
        question: The user's question/request
        ground_truth: The ground truth function call
        prediction: The predicted function call
        
    Returns:
        Dictionary with 'equivalent' (bool) and 'reasoning' (str)
    """
    user_prompt = f"""
User Question: {question}

Ground Truth Function Call:
{json.dumps(ground_truth, indent=2)}

Predicted Function Call:
{json.dumps(prediction, indent=2)}

Are these function calls semantically equivalent? Respond with JSON only.
"""
    
    try:
        response = client.chat.completions.create(
            model=JUDGE_MODEL,
            temperature=JUDGE_TEMPERATURE,
            messages=[
                {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"Error calling judge: {e}")
        return {"equivalent": False, "reasoning": f"Error: {str(e)}"}


def evaluate_single_test(
    test_case: Dict[str, Any],
    model_prediction: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Evaluate a single test case using LLM judge.
    
    Args:
        test_case: Test case from the dataset (contains question, ground_truth, etc.)
        model_prediction: Model's predicted function call
        
    Returns:
        Evaluation result with score and details
    """
    # Extract question (handle nested structure)
    question_data = test_case.get('question', [[]])
    if isinstance(question_data, list) and len(question_data) > 0:
        if isinstance(question_data[0], list) and len(question_data[0]) > 0:
            question = question_data[0][0].get('content', '')
        else:
            question = str(question_data)
    else:
        question = str(question_data)
    
    # Get ground truth (the correct function from the test case)
    ground_truth_functions = test_case.get('function', [])
    ground_truth_answer = test_case.get('ground_truth', [])
    
    # For simple_python, ground_truth should contain the correct function name and parameters
    if not ground_truth_answer:
        # If no ground_truth field, use the function definitions as reference
        ground_truth_answer = ground_truth_functions[0] if ground_truth_functions else {}
    
    # Call the judge
    judge_result = call_judge(question, ground_truth_answer, model_prediction)
    
    return {
        'test_id': test_case.get('id', 'unknown'),
        'equivalent': judge_result.get('equivalent', False),
        'reasoning': judge_result.get('reasoning', ''),
        'question': question,
        'ground_truth': ground_truth_answer,
        'prediction': model_prediction
    }


def evaluate_predictions(
    test_file: Path,
    predictions_file: Path,
    output_file: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Evaluate all predictions for a test set using LLM judge.
    
    Args:
        test_file: Path to test set JSONL file
        predictions_file: Path to model predictions JSONL file
        output_file: Optional path to save detailed results
        
    Returns:
        Summary statistics
    """
    # Load test cases
    test_cases = []
    with open(test_file, 'r') as f:
        for line in f:
            if line.strip():
                test_cases.append(json.loads(line))
    
    # Load predictions
    predictions = []
    with open(predictions_file, 'r') as f:
        for line in f:
            if line.strip():
                predictions.append(json.loads(line))
    
    # Create mapping of test_id to prediction
    pred_map = {p['test_id']: p['prediction'] for p in predictions}
    
    # Evaluate each test case
    results = []
    num_correct = 0
    num_total = 0
    
    for test_case in test_cases:
        test_id = test_case['id']
        
        if test_id not in pred_map:
            print(f"Warning: No prediction found for test {test_id}")
            continue
        
        prediction = pred_map[test_id]
        result = evaluate_single_test(test_case, prediction)
        
        results.append(result)
        num_total += 1
        if result['equivalent']:
            num_correct += 1
        
        # Print progress
        if num_total % 10 == 0:
            print(f"Evaluated {num_total}/{len(test_cases)} tests...")
    
    # Calculate summary statistics
    accuracy = num_correct / num_total if num_total > 0 else 0.0
    summary = {
        'total_tests': num_total,
        'correct': num_correct,
        'incorrect': num_total - num_correct,
        'accuracy': accuracy
    }
    
    # Save detailed results if requested
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump({
                'summary': summary,
                'results': results
            }, f, indent=2)
        print(f"Detailed results saved to: {output_file}")
    
    return summary


def main():
    """Example usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Evaluate model predictions using LLM judge')
    parser.add_argument('--test-file', type=str, required=True,
                        help='Path to test set JSONL file')
    parser.add_argument('--predictions-file', type=str, required=True,
                        help='Path to model predictions JSONL file')
    parser.add_argument('--output-file', type=str, default=None,
                        help='Path to save detailed results JSON')
    
    args = parser.parse_args()
    
    test_file = Path(args.test_file)
    predictions_file = Path(args.predictions_file)
    output_file = Path(args.output_file) if args.output_file else None
    
    print(f"Evaluating predictions...")
    print(f"Test file: {test_file}")
    print(f"Predictions file: {predictions_file}")
    print(f"Using judge model: {JUDGE_MODEL}")
    print()
    
    summary = evaluate_predictions(test_file, predictions_file, output_file)
    
    print("\n=== Evaluation Summary ===")
    print(f"Total tests: {summary['total_tests']}")
    print(f"Correct: {summary['correct']}")
    print(f"Incorrect: {summary['incorrect']}")
    print(f"Accuracy: {summary['accuracy']:.2%}")


if __name__ == "__main__":
    main()
