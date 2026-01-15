#!/bin/bash

source /home/mingxuanl/miniconda3/etc/profile.d/conda.sh
conda activate bfcl-thousand-03
cd /home/mingxuanl/mingxuanl/simulation/marcussullivan/bfcl-thousand-tools-01/berkeley-function-call-leaderboard
export OPENAI_API_KEY=sk-svcacct-YTWyBnrCVylFHrAmtm7hT3BlbkFJ86XwFnwus57NHGek99xT

# Output file for results
RESULTS_FILE="/home/mingxuanl/mingxuanl/simulation/marcussullivan/bfcl-thousand-tools-01/all_models_category_results.txt"
echo "All Models Category Scaling Evaluation Results" > $RESULTS_FILE
echo "===============================================" >> $RESULTS_FILE
echo "" >> $RESULTS_FILE

MODELS=("gpt-4o-mini-2024-07-18" "gpt-4o-2024-11-20" "grok-4-0709" "grok-3-beta" "grok-3-mini-beta")
CATEGORIES=("parallel" "multiple" "parallel_multiple")
POOLS=(0 16 32 64 128 256 512)

for model in "${MODELS[@]}"; do
    echo "Model: $model" >> $RESULTS_FILE
    echo "---" >> $RESULTS_FILE
    
    for category in "${CATEGORIES[@]}"; do
        echo "  Category: $category" >> $RESULTS_FILE
        
        for pool in "${POOLS[@]}"; do
            # Copy the specific pool file to the standard location
            cp result/$model/non_live/${category}_scaling/pool${pool}.json result/$model/non_live/BFCL_v4_${category}_result.json
            
            # Run evaluation and capture accuracy
            OUTPUT=$(python -m bfcl_eval evaluate --model $model --test-category $category 2>&1)
            ACCURACY=$(echo "$OUTPUT" | grep "Accuracy:" | tail -1 | sed 's/.*Accuracy: \([0-9.]*\)%.*/\1/')
            
            echo "    Pool $pool: $ACCURACY%" >> $RESULTS_FILE
        done
        echo "" >> $RESULTS_FILE
    done
    echo "" >> $RESULTS_FILE
done

echo "Evaluation complete! Results saved to $RESULTS_FILE"
cat $RESULTS_FILE


