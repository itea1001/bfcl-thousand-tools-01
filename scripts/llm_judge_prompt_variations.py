import json
import os
import sys
from pathlib import Path
from openai import OpenAI

client = OpenAI()

def load_test_data_json(test_file):
    """Load test data from JSONL file"""
    data = []
    with open(test_file) as f:
        for line in f:
            data.append(json.loads(line))
    return data

def load_results(result_file):
    """Load model results from JSONL file"""
    with open(result_file) as f:
        return [json.loads(line) for line in f]

def evaluate_with_llm_judge(question, ground_truth, prediction):
    """Use GPT-4o-mini as judge to evaluate semantic equivalence"""
    prompt = f"""You are evaluating whether two function calls achieve the same goal.

Question: {question}

Ground Truth Function Call: {json.dumps(ground_truth, indent=2)}

Predicted Function Call: {prediction}

Are these two function calls semantically equivalent (achieve the same goal)?
Respond with only "YES" or "NO" and a brief explanation."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        answer = response.choices[0].message.content.strip()
        return answer.startswith("YES") or answer.startswith("Yes")
    except Exception as e:
        print(f"Error calling LLM judge: {e}", flush=True)
        return False

# Load possible answers for ground truth (JSONL format)
baseline_possible = []
with open('berkeley-function-call-leaderboard/bfcl_eval/data/possible_answer/BFCL_v4_simple_python.json') as f:
    for line in f:
        baseline_possible.append(json.loads(line))
baseline_gt_map = {item['id']: item['ground_truth'] for item in baseline_possible}

pool512_possible = []
with open('berkeley-function-call-leaderboard/bfcl_eval/data/possible_answer/BFCL_v4_simple_python_pool512.json') as f:
    for line in f:
        pool512_possible.append(json.loads(line))
pool512_gt_map = {item['id']: item['ground_truth'] for item in pool512_possible}

# Configurations to evaluate
configs = [
    ("baseline_json", "berkeley-function-call-leaderboard/bfcl_eval/data/BFCL_v4_simple_python.json", 
     "berkeley-function-call-leaderboard/result_simple_baseline_res_fmt=json_doc_fmt=json/gpt-4o-mini-2024-07-18/non_live/BFCL_v4_simple_python_result.json",
     baseline_gt_map),
    ("baseline_json_tagged", "berkeley-function-call-leaderboard/bfcl_eval/data/BFCL_v4_simple_python.json",
     "berkeley-function-call-leaderboard/result_simple_baseline_res_fmt=json_tagged_doc_fmt=json/gpt-4o-mini-2024-07-18/non_live/BFCL_v4_simple_python_result.json",
     baseline_gt_map),
    ("baseline_xml", "berkeley-function-call-leaderboard/bfcl_eval/data/BFCL_v4_simple_python.json",
     "berkeley-function-call-leaderboard/result_simple_baseline_res_fmt=xml_doc_fmt=xml/gpt-4o-mini-2024-07-18/non_live/BFCL_v4_simple_python_result.json",
     baseline_gt_map),
    ("pool512_json", "data/scaled_tests/simple_python_pool512.json",
     "berkeley-function-call-leaderboard/result_simple_pool512_res_fmt=json_doc_fmt=json/gpt-4o-mini-2024-07-18/non_live/BFCL_v4_simple_python_result.json",
     pool512_gt_map),
    ("pool512_json_tagged", "data/scaled_tests/simple_python_pool512.json",
     "berkeley-function-call-leaderboard/result_simple_pool512_res_fmt=json_tagged_doc_fmt=json/gpt-4o-mini-2024-07-18/non_live/BFCL_v4_simple_python_result.json",
     pool512_gt_map),
    ("pool512_xml", "data/scaled_tests/simple_python_pool512.json",
     "berkeley-function-call-leaderboard/result_simple_pool512_res_fmt=xml_doc_fmt=xml/gpt-4o-mini-2024-07-18/non_live/BFCL_v4_simple_python_result.json",
     pool512_gt_map),
]

all_results = {}

for config_name, test_file, result_file, gt_map in configs:
    print(f"\n{'='*70}", flush=True)
    print(f"Evaluating: {config_name}", flush=True)
    print(f"{'='*70}", flush=True)
    
    tests = load_test_data_json(test_file)
    results = load_results(result_file)
    
    # Create result map by ID
    result_map = {r['id']: r for r in results}
    
    correct = 0
    total = len(tests)
    
    for i, test in enumerate(tests):
        if (i + 1) % 50 == 0:
            print(f"Progress: {i+1}/{total}", flush=True)
        
        test_id = test['id']
        if test_id not in result_map:
            print(f"Warning: No result for test ID {test_id}", flush=True)
            continue
            
        question = test['question']
        ground_truth = gt_map.get(test_id, [])
        prediction = result_map[test_id]['result']
        
        is_correct = evaluate_with_llm_judge(question, ground_truth, prediction)
        if is_correct:
            correct += 1
    
    accuracy = correct / total if total > 0 else 0
    all_results[config_name] = {
        'correct': correct,
        'total': total,
        'accuracy': accuracy
    }
    
    print(f"\nResults for {config_name}:", flush=True)
    print(f"  Correct: {correct}/{total}", flush=True)
    print(f"  Accuracy: {accuracy:.2%}", flush=True)

# Save results
with open('prompt_variation_llm_judge_results.json', 'w') as f:
    json.dump(all_results, f, indent=2)

print(f"\n{'='*70}", flush=True)
print("FINAL SUMMARY", flush=True)
print(f"{'='*70}", flush=True)
for name, res in all_results.items():
    print(f"{name:25s}: {res['accuracy']:.2%} ({res['correct']}/{res['total']})", flush=True)

