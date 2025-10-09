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

import json
import ray

from typing import Optional, Dict, List, Tuple
from loguru import logger
from lean_dojo import TacticState, Theorem, ProofFinished, ProofGivenUp

from proof_tree import validate_proof


class PlanManager:
    """Simple plan manager that loads plans from a JSON file."""
    def __init__(self, plan_file: Optional[str]):
        self.plan_file = plan_file
        self._plans_cache = {}
        if plan_file:
            with open(plan_file, "r") as f:
                self._plans_cache = json.load(f)

    def get_plan(self, theorem_name: str) -> Optional[List[str]]:
        """Get plans for theorem."""
        theorem_data = self._plans_cache.get(theorem_name)
        if theorem_data and "plan" in theorem_data:
            return theorem_data["plan"]
        return None

@ray.remote
class ProgressCache:
    """Caching, tracking, and managing progress of plan execution."""

    def __init__(self):
        self.registry: Dict[str, Dict] = {}

    def ping(self) -> str:
        return "ok"
    
    def initialize(self, theorem: Theorem, num_subgoals: int, replace: bool = False):
        """Initialize progress tracking for a theorem."""
        key = theorem.full_name
        if key not in self.registry or replace:
            self.registry[key] = {
                'progress': 0,
                'proof': [[] for _ in range(num_subgoals + 1)],
                'proof_stats': [[] for _ in range(num_subgoals + 1)],
                'preference_pairs': [[] for _ in range(num_subgoals + 1)],
            }
            logger.info(f"Initialized progress for {key} with {num_subgoals + 1} steps")
    
    def update(self, theorem: Theorem, step_index: int, 
               proof: Optional[Tuple[Tuple[str, str]]], proof_stats: Optional[Tuple[Tuple[float, float]]], preference_pairs: Optional[Tuple[Tuple[str, str, str]]]):
        """Update progress for a state."""
        key = theorem.full_name
        if key not in self.registry:
            return
        
        progress_info = self.registry[key]
        current_progress = progress_info['progress']
        num_steps = len(progress_info['proof'])

        # If the step is the next step to be solved, validate the trajectory
        if step_index == current_progress:
            # Build the trajectory for validation
            validation_trajectory = []
            for i in range(step_index):
                _, plan_step = progress_info['proof'][i][0]
                validation_trajectory.extend([plan_step, "sorry"])
            proof_trajectory = [tactic for _, tactic in proof]
            validation_trajectory.extend(proof_trajectory)

            is_valid = validate_proof(theorem, validation_trajectory, (TacticState, ProofFinished, ProofGivenUp), focus_mode=True)

            # If the trajectory is valid, update the progress
            if is_valid:
                progress_info['proof'][step_index] = proof
                progress_info['proof_stats'][step_index] = proof_stats
                progress_info['preference_pairs'][step_index] = preference_pairs
                progress_info['progress'] = step_index + 1
                logger.info(f"Progress update: solved {step_index + 1}/{num_steps} goals.")
    
    def get_progress(self, theorem: Theorem) -> int:
        """Get the current progress of a theorem."""
        key = theorem.full_name
        if key not in self.registry:
            return 0
        return self.registry[key]['progress']

    def get_proof_data(self, theorem: Theorem) -> Tuple[Tuple[str, str], Tuple[float, float], Tuple[str, str, str]]:
        """Get the current proof data of a theorem."""
        key = theorem.full_name
        if key not in self.registry:
            return None, None, None
        proof, proof_stats, preference_pairs = [], [], []
        for i in range(len(self.registry[key]['proof'])):
            proof.extend(self.registry[key]['proof'][i] or [])
            proof_stats.extend(self.registry[key]['proof_stats'][i] or [])
            preference_pairs.extend(self.registry[key]['preference_pairs'][i] or [])
        return tuple(proof), tuple(proof_stats), tuple(preference_pairs)
