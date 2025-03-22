#!/bin/bash

echo -e "\n\n-----Getting a list of passing tests..."
python agentless/test/run_regression_tests.py --run_id generate_regression_tests \
                                              --output_file results/swe-bench-lite/passing_tests.jsonl \
                                              --target_id=django__django-10914

#############################################

echo -e "\n\n-----Removing any tests which should not be ran..."
python agentless/test/select_regression_tests.py --passing_tests results/swe-bench-lite/passing_tests.jsonl \
                                                 --output_folder results/swe-bench-lite/select_regression \
                                                 --target_id=django__django-10914

#############################################

echo -e "\n\n-----Running tests..."
folder=results/swe-bench-lite/repair_sample_1
for num in {0..9..1}; do
    run_id_prefix=$(basename $folder); 
    python agentless/test/run_regression_tests.py --regression_tests results/swe-bench-lite/select_regression/output.jsonl \
                                                  --predictions_path="${folder}/output_${num}_processed.jsonl" \
                                                  --run_id="${run_id_prefix}_regression_${num}" --num_workers 10 \
                                                  --target_id=django__django-10914;
done

#############################################

echo -e "\n\n-----Generating reproduction tests..."
python agentless/test/generate_reproduction_tests.py --max_samples 40 \
                                                     --output_folder results/swe-bench-lite/reproduction_test_samples \
                                                     --num_threads 10 \
                                                     --target_id=django__django-10914

#############################################

echo -e "\n\n-----Executing generated tests..."
for st in {0..36..4}; do   en=$((st + 3));   
        echo "Processing ${st} to ${en}";   
        for num in $(seq $st $en); do     
            echo "Processing ${num}";     
            python agentless/test/run_reproduction_tests.py --run_id="reproduction_test_generation_filter_sample_${num}" \
                                                            --test_jsonl="results/swe-bench-lite/reproduction_test_samples/output_${num}_processed_reproduction_test.jsonl" \
                                                            --num_workers 6 \
                                                            --testing \
                                                            --target_id=django__django-10914;
done & done

#############################################

echo -e "\n\n-----Performing majority vote..."
python agentless/test/generate_reproduction_tests.py --max_samples 40 \
                                                     --output_folder results/swe-bench-lite/reproduction_test_samples \
                                                     --output_file reproduction_tests.jsonl \
                                                     --select \
                                                     --target_id=django__django-10914

#############################################

echo -e "\n\n-----Evaluating the generated patches..."
folder=results/swe-bench-lite/repair_sample_1
for num in {0..9..1}; do
    run_id_prefix=$(basename $folder); 
    python agentless/test/run_reproduction_tests.py --test_jsonl results/swe-bench-lite/reproduction_test_samples/reproduction_tests.jsonl \
                                                    --predictions_path="${folder}/output_${num}_processed.jsonl" \
                                                    --run_id="${run_id_prefix}_reproduction_${num}" --num_workers 10 \
                                                    --target_id=django__django-10914;
done

#############################################

echo -e "\n\n-----Selecting the final patch for submission..."
python agentless/repair/rerank.py --patch_folder results/swe-bench-lite/repair_sample_1/,results/swe-bench-lite/repair_sample_2/,results/swe-bench-lite/repair_sample_3/,results/swe-bench-lite/repair_sample_4/ \
                                  --num_samples 40 \
                                  --deduplicate \
                                  --regression \
                                  --reproduction