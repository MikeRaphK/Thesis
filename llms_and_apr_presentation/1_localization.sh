#!/bin/bash

echo -e "\n\n-----Localizing to suspicious files..."
python agentless/fl/localize.py --file_level \
                                --output_folder results/swe-bench-lite/file_level \
                                --num_threads 10 \
                                --skip_existing \
                                --target_id=django__django-10914

python agentless/fl/localize.py --file_level \
                                --irrelevant \
                                --output_folder results/swe-bench-lite/file_level_irrelevant \
                                --num_threads 10 \
                                --skip_existing \
                                --target_id=django__django-10914

python agentless/fl/retrieve.py --index_type simple \
                                --filter_type given_files \
                                --filter_file results/swe-bench-lite/file_level_irrelevant/loc_outputs.jsonl \
                                --output_folder results/swe-bench-lite/retrievel_embedding \
                                --persist_dir embedding/swe-bench_simple \
                                --num_threads 10 \
                                --target_id=django__django-10914

python agentless/fl/combine.py  --retrieval_loc_file results/swe-bench-lite/retrievel_embedding/retrieve_locs.jsonl \
                                --model_loc_file results/swe-bench-lite/file_level/loc_outputs.jsonl \
                                --top_n 3 \
                                --output_folder results/swe-bench-lite/file_level_combined

#############################################

echo -e "\n\n-----Localizing to related elements..."
python agentless/fl/localize.py --related_level \
                                --output_folder results/swe-bench-lite/related_elements \
                                --top_n 3 \
                                --compress_assign \
                                --compress \
                                --start_file results/swe-bench-lite/file_level_combined/combined_locs.jsonl \
                                --num_threads 10 \
                                --skip_existing \
                                --target_id=django__django-10914

#############################################

echo -e "\n\n-----Localizing to edit locations..."
python agentless/fl/localize.py --fine_grain_line_level \
                                --output_folder results/swe-bench-lite/edit_location_samples \
                                --top_n 3 \
                                --compress \
                                --temperature 0.8 \
                                --num_samples 4 \
                                --start_file results/swe-bench-lite/related_elements/loc_outputs.jsonl \
                                --num_threads 10 \
                                --skip_existing \
                                --target_id=django__django-10914

#############################################

echo -e "\n\n-----Separating the individual sets of edit locations..."
python agentless/fl/localize.py --merge \
                                --output_folder results/swe-bench-lite/edit_location_individual \
                                --top_n 3 \
                                --num_samples 4 \
                                --start_file results/swe-bench-lite/edit_location_samples/loc_outputs.jsonl \
                                --target_id=django__django-10914