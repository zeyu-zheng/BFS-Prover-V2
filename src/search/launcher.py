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

import pickle
import uuid
import subprocess
import json
import ray

from dataclasses import dataclass
from typing import List, Optional
from loguru import logger
from lean_dojo import Theorem

from src.search.prover_manager import ProverManager, SearchResult, ProofTask
from src.search.theorem_manager import TheoremManager, TheoremType
from src.search.plan_manager import PlanManager, ProgressCache


@dataclass(frozen=True)
class ProofSearchConfig:
    # vllm tactic generator settings
    model_path: str
    max_num_batched_tokens: int
    max_num_seqs: int

    # theorem loader settings
    file_path: str
    theorem_type: str
    lines_cap: Optional[int]

    # plan settings
    plan_file: Optional[str]

    # ray prover settings
    num_tac_gen: int
    num_provers: int
    num_gpus_per_tac_gen: int
    num_cpus_per_prover: int

    # search settings
    timeout_per_theorem: int
    pass_k: int
    n_sampling_search: int
    sampling_temperature: float
    sampling_top_p: float
    max_tokens: int
    depth_reward: float
    vllm_timeout: int
    tactic_timeout: int
    local_save_dir: Optional[str]

    def __post_init__(self):
        logger.info(f"{self}")

        if not isinstance(self.pass_k, int) or self.pass_k < 1:
            raise ValueError(f"Invalid pass_k {self.pass_k}")

        if not self.file_path.endswith(".jsonl"):
            raise ValueError(f"Invalid file path {self.file_path}")

        if self.plan_file is not None and not self.plan_file.endswith(".json"):
            raise ValueError(f"Invalid plan file {self.plan_file}")

        logger.info("Configured for local search")

        if self.lines_cap is not None:
            logger.warning(
                f"DEBUG MODE is on: number of lines loaded from {self.file_path} is capped at {self.lines_cap}"
            )

        if self.depth_reward == 0.0:
            logger.info(
                "Depth reward is set to 0.0, bfs will be greedy, i.e., the standard sum of log probabilities"
            )
        elif self.depth_reward == 1.0:
            logger.info(
                "Depth reward is set to 1.0, bfs will be prioritized by depth, i.e., the average log probability"
            )
        elif 0 < self.depth_reward < 1:
            logger.info(
                f"Depth reward is set to {self.depth_reward}, sum of log probabilities in bfs will be scaled by depth ** {self.depth_reward}"
            )
        elif self.depth_reward > 1:
            logger.warning(
                f"Using a non-standard depth reward {self.depth_reward}, bfs will be prioritized by depth ** {self.depth_reward}"
            )
        else:
            raise ValueError(f"Invalid depth reward {self.depth_reward}")

    def __repr__(self) -> str:
        lines = [
            "\nProofSearchConfig:",
            f"  Model Path: {self.model_path}",
            f"  Max Number of Batched Tokens in VLLM: {self.max_num_batched_tokens}",
            f"  Max Number of Batched Sequences in VLLM: {self.max_num_seqs}",
            f"  File Path: {self.file_path}",
            f"  Theorem Type: {self.theorem_type}",
            f"  Lines Cap: {self.lines_cap if self.lines_cap is not None else 'None'}",
            f"  Number of Tactic Generators: {self.num_tac_gen}",
            f"  Number of Provers: {self.num_provers}",
            f"  Timeout per Theorem: {self.timeout_per_theorem} seconds",
            f"  GPUs per Tactic Generator: {self.num_gpus_per_tac_gen}",
            f"  CPUs per Prover: {self.num_cpus_per_prover}",
            f"  Pass@K: {self.pass_k}",
            f"  Sampling Search Size: {self.n_sampling_search}",
            f"  Sampling Temperature: {self.sampling_temperature}",
            f"  Sampling Top P: {self.sampling_top_p}",
            f"  Max Generated Tokens: {self.max_tokens}",
            f"  Depth Reward: {self.depth_reward}",
            f"  VLLM Timeout: {self.vllm_timeout} seconds",
            f"  Tactic Execution Timeout: {self.tactic_timeout} seconds",
            f"  Local Save Directory: {self.local_save_dir if self.local_save_dir is not None else 'results'}",
        ]
        return "\n".join(lines)


class ProofSearchLauncher:
    def __init__(self, config: ProofSearchConfig) -> None:
        self.config = config
        self.theorem_manager = TheoremManager(config.file_path, config.lines_cap)
        self.theorems = self.get_theorems()
        self.plan_manager = PlanManager(config.plan_file)
        self.tasks = self.get_tasks()

        self.progress_cache = ProgressCache.options(name="progress_cache").remote()
        try:
            # Force actor creation and naming to complete
            ray.get(self.progress_cache.ping.remote(), timeout=30)
            logger.info("Progress cache actor ready")
        except Exception as e:
            raise RuntimeError(f"Progress cache actor initialization failed: {e}")
    
        self.prover_manager = ProverManager(
            model_path=config.model_path,
            max_num_batched_tokens=config.max_num_batched_tokens,
            max_num_seqs=config.max_num_seqs,
            num_tac_gen=config.num_tac_gen,
            num_provers=config.num_provers,
            timeout_per_theorem=config.timeout_per_theorem,
            num_gpus_per_tac_gen=config.num_gpus_per_tac_gen,
            num_cpus_per_prover=config.num_cpus_per_prover,
            n_sampling_search=config.n_sampling_search,
            sampling_temperature=config.sampling_temperature,
            sampling_top_p=config.sampling_top_p,
            max_tokens=config.max_tokens,
            depth_reward=config.depth_reward,
            vllm_timeout=config.vllm_timeout,
            tactic_timeout=config.tactic_timeout,
        )

    def get_theorems(self) -> List[Theorem]:
        theorem_type = TheoremType(self.config.theorem_type)
        theorem_type_map = {
            TheoremType.GENERIC: self.theorem_manager.get_generic,
            TheoremType.VALID: self.theorem_manager.get_valid,
            TheoremType.TEST: self.theorem_manager.get_test,
        }
        if theorem_type not in theorem_type_map:
            raise ValueError(f"Invalid theorem type {self.config.theorem_type}")
        return theorem_type_map[theorem_type]()

    def get_tasks(self) -> List[ProofTask]:
        """Prepares a list of ProofTasks, bundling theorems with their plans."""
        tasks = []
        for theorem in self.theorems:
            plan = None
            if self.plan_manager:
                plan = self.plan_manager.get_plan(theorem.full_name)
            tasks.append(ProofTask(theorem=theorem, plan=plan))
        return tasks

    def launch_local(self) -> List[Optional[SearchResult]]:
        """Launch a search locally on a single machine."""

        logger.info(
            f"Launching search for {len(self.theorems)} theorems from {self.config.file_path} locally"
        )
        if self.config.plan_file:
            logger.info(f"Using plans from {self.config.plan_file}")
        else:
            logger.info("No plans provided")

        results = self.prover_manager.parallel_prove_pass_k(
            self.tasks, self.config.pass_k
        )
        return results

    def save_progress(self, results: List[Optional[SearchResult]]):
        """Update progress in plan file based on search results"""
        if not self.config.plan_file:
            return
        with open(self.config.plan_file, "r") as f:
            plan_data = json.load(f)
        
        task_map = {task.theorem.full_name: task for task in self.tasks}
        
        for result in results:
            if result:
                theorem_name = result.full_name
                task = task_map[theorem_name]
                if not task.plan:
                    continue

                plan_data[theorem_name]["progress"] = ray.get(self.progress_cache.get_progress.remote(task.theorem))
        
        with open(self.config.plan_file, "w") as f:
            json.dump(plan_data, f, indent=2, ensure_ascii=False)


class SearchResultSaver:

    def __init__(self, local_save_dir: Optional[str] = None) -> None:
        # Default to results directory at project root (same level as src)
        if local_save_dir is None:
            local_save_dir = "../../results"
        self.local_save_dir = local_save_dir

    def save(self, results: List[Optional[SearchResult]], name: Optional[str] = None):
        # Save the results to a pickle file
        if name is None:
            name = str(uuid.uuid4())
        pickle_path = f"{self.local_save_dir}/proof_results_{name}.pickle"
        subprocess.run(["mkdir", "-p", self.local_save_dir])
        with open(pickle_path, "wb") as f:
            pickle.dump(results, f)
        logger.info(f"Saved proof search results locally to {pickle_path}")
