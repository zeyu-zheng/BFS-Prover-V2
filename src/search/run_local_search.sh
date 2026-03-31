# Copyright 2025 XXXXXXXXX Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Best-First Search Script
# Proves theorems in parallel using Best-First Search

python src/search/main.py \
    --model_path /PATH/TO/YOUR/PROVER_MODEL \
    --max_num_batched_tokens 1024 \
    --max_num_seqs 128 \
    --file_path /PATH/TO/YOUR/DOJO_JSONL \
    --theorem_type test \
    --plan_file /PATH/TO/YOUR/PLAN_FILE \
    --num_tac_gen 4 \
    --num_provers 128 \
    --timeout_per_theorem 600 \
    --num_gpus_per_tac_gen 2 \
    --num_cpus_per_prover 1 \
    --pass_k 512 \
    --n_sampling_search 4 \
    --sampling_temperature 1.3 \
    --sampling_top_p 1.0 \
    --max_tokens 2048 \
    --depth_reward 2.0 \
    --vllm_timeout 60 \
    --tactic_timeout 12 \
    --local_save_dir results > src/search/search.log 2>&1
