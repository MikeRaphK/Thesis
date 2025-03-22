#!/bin/bash

echo -e "\n\n-----Generating the patches..."
python agentless/repair/repair.py --loc_file results/swe-bench-lite/edit_location_individual/loc_merged_0-0_outputs.jsonl \
                                  --output_folder results/swe-bench-lite/repair_sample_1 \
                                  --loc_interval \
                                  --top_n=3 \
                                  --context_window=10 \
                                  --max_samples 10  \
                                  --cot \
                                  --diff_format \
                                  --gen_and_process \
                                  --num_threads 2 \
                                  --target_id=django__django-10914