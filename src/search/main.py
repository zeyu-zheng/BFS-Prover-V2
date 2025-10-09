# Copyright 2025 Bytedance Ltd. and/or its affiliates
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

import argparse

from theorem_manager import TheoremType
from launcher import (
    ProofSearchLauncher,
    ProofSearchConfig,
    SearchResultSaver,
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Prove theorems in parallel using BFS-Prover's tree search pipeline"
    )
    parser.add_argument(
        "--model_path",
        type=str,
        required=True,
        help="Path to the huggingface model checkpoint",
    )
    parser.add_argument(
        "--max_num_batched_tokens",
        type=int,
        default=8192,
        help="Maximum number of tokens in a vllm batch",
    )
    parser.add_argument(
        "--max_num_seqs",
        type=int,
        default=256,
        help="Maximum number of sequences in a vllm batch",
    )
    parser.add_argument(
        "--file_path",
        type=str,
        required=True,
        help="Path to the JSONL file containing theorems to prove",
    )
    parser.add_argument(
        "--theorem_type",
        type=str,
        required=True,
        choices=[t.value for t in TheoremType],
        help="Type of theorems to load",
    )
    parser.add_argument(
        "--lines_cap",
        type=int,
        default=None,
        help="Debug only: cap on the number of json lines to load",
    )
    parser.add_argument(
        "--plan_file",
        type=str,
        default=None,
        help="Path to the JSON file containing proof plans",
    )
    parser.add_argument(
        "--num_tac_gen",
        type=int,
        default=8,
        help="Number of tactic generators hosted by vllm",
    )
    parser.add_argument(
        "--num_provers",
        type=int,
        default=96,
        help="Number of parallel provers launched",
    )
    parser.add_argument(
        "--timeout_per_theorem",
        type=int,
        default=600,
        help="Timeout for each theorem search in seconds",
    )
    parser.add_argument(
        "--num_gpus_per_tac_gen",
        type=int,
        default=1,
        help="Number of dedicated GPUs assigned to each tactic generator",
    )
    parser.add_argument(
        "--num_cpus_per_prover",
        type=int,
        default=1,
        help="Number of dedicated CPUs assigned to each prover",
    )
    parser.add_argument(
        "--pass_k",
        type=int,
        default=1,
        help="Total number of attempts to prove a theorem",
    )
    parser.add_argument(
        "--n_sampling_search",
        type=int,
        default=16,
        help="Number of samples in the sampling search with temperature",
    )
    parser.add_argument(
        "--sampling_temperature",
        type=float,
        default=0.7,
        help="Temperature for sampling search",
    )
    parser.add_argument(
        "--sampling_top_p",
        type=float,
        default=1.0,
        help="Top-p for sampling search",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=2048,
        help="Maximum number of tokens in a model-generated tactic",
    )
    parser.add_argument(
        "--depth_reward",
        type=float,
        default=0.0,
        help="Depth reward for best first search",
    )
    parser.add_argument(
        "--vllm_timeout",
        type=int,
        default=60,
        help="Timeout for vllm requests in seconds",
    )
    parser.add_argument(
        "--tactic_timeout",
        type=int,
        default=10,
        help="Timeout for tactic generation in seconds",
    )
    parser.add_argument(
        "--local_save_dir",
        type=str,
        default=None,
        help="Local directory to save proof search results (default: ../../results)",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    config = ProofSearchConfig(**vars(args))
    launcher = ProofSearchLauncher(config)
    saver = SearchResultSaver(config.local_save_dir)

    results = launcher.launch_local()
    launcher.save_progress(results)
    saver.save(results=results)


if __name__ == "__main__":
    main()
