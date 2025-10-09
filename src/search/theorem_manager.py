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

from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass
from loguru import logger
from lean_dojo import trace, is_available_in_cache, Theorem, LeanGitRepo


class TheoremType(Enum):
    """Enum to represent the type of a theorem."""

    VALID = "valid"
    TEST = "test"
    GENERIC = "generic"


@dataclass
class TypedTheorem:
    """Dataclass to store a theorem and its type."""

    theorem: Theorem
    theorem_type: TheoremType


class Tracer:
    """Helper class to trace LeanGitRepo objects."""

    @staticmethod
    def trace_repo(repo: LeanGitRepo) -> None:
        """Trace a LeanGitRepo object if it has not been traced before."""

        if not isinstance(repo, LeanGitRepo):
            raise ValueError(f"Expected a LeanGitRepo object, got {repo}")

        if not is_available_in_cache(repo):
            logger.info(f"{repo} has not been traced, tracing now")
            trace(repo)

        else:
            rel_cache_dir = repo.get_cache_dirname() / repo.name
            logger.info(f"{repo} is already traced, cache found in {rel_cache_dir}")

    @staticmethod
    def trace_theorems(theorems: List[Theorem]) -> None:
        """Trace all repos that the theorems belong to."""

        for t in theorems:
            if not isinstance(t, Theorem):
                raise ValueError(f"Expected a Theorem object, got {t}")
        all_repos = {t.repo for t in theorems}
        logger.info(f"Found {len(all_repos)} repos: {all_repos}")
        for repo in all_repos:
            Tracer.trace_repo(repo)


class TheoremLoader:
    """Helper class to load theorems from a list of TypedTheorem objects."""

    @staticmethod
    def load_theorems_by_type(
        typed_theorems: List[TypedTheorem], theorem_type: TheoremType
    ) -> List[Theorem]:
        theorems = [t.theorem for t in typed_theorems if t.theorem_type == theorem_type]
        logger.info(f"Loaded {len(theorems)} {theorem_type.value} theorems")
        Tracer.trace_theorems(theorems)
        return theorems


class JsonlFields:
    """Class to store the required and optional fields in a JSONL file."""

    REQUIRED = ["url", "commit", "full_name", "file_path"]
    OPTIONAL = ["split"]


@dataclass
class JsonLine:
    url: str
    commit: str
    full_name: str
    file_path: str
    split: Optional[str] = None

    def to_typed_theorem(self) -> TypedTheorem:
        theorem = Theorem(
            repo=LeanGitRepo(url=self.url, commit=self.commit),
            full_name=self.full_name,
            file_path=self.file_path,
        )
        theorem_type = TheoremType(self.split) if self.split else TheoremType.GENERIC
        return TypedTheorem(theorem=theorem, theorem_type=theorem_type)


class TheoremManager:
    """Class to manage the loading of theorems from a JSONL file."""

    SPLIT_TYPES = [theorem_type.value for theorem_type in TheoremType]

    def __init__(self, file_path: str, lines_cap: Optional[int] = None) -> None:
        self.file_path = file_path
        self.ignored_fields = set()
        self.lines_cap = lines_cap
        self._theorems: List[TypedTheorem] = self._load_theorems()
        logger.info(f"Found {len(self._theorems)} theorems from {file_path}")
        if self.ignored_fields:
            logger.warning(
                f"Ignored fields in {file_path}: {sorted(self.ignored_fields)}"
            )

    def _load_theorems(self) -> List[TypedTheorem]:
        """Load the theorems from a JSONL file."""

        json_lines: List[JsonLine] = self._read_jsonl_file()
        return [json_line.to_typed_theorem() for json_line in json_lines]

    def _read_jsonl_file(self) -> List[JsonLine]:
        """Read a JSONL file and return a list of lines that are dictionaries."""

        json_lines: List[JsonLine] = []
        with open(self.file_path, "r") as f:
            for line in f:
                try:
                    line = json.loads(line)
                    self._verify_fields(line)
                    json_lines.append(
                        JsonLine(
                            url=line["url"],
                            commit=line["commit"],
                            full_name=line["full_name"],
                            file_path=line["file_path"],
                            split=line.get("split"),
                        )
                    )

                except json.JSONDecodeError as ex:
                    logger.warning(f"Failed to parse line {line} with exception {ex}")

                except ValueError as ex:
                    logger.warning(f"Failed to verify line {line} with exception {ex}")

                if self.lines_cap is not None and len(json_lines) >= self.lines_cap:
                    logger.warning(
                        f"DEBUG MODE is on: reached cap of {self.lines_cap} lines in {self.file_path}"
                    )
                    return json_lines
        return json_lines

    def _verify_fields(self, line: Dict[str, str]) -> None:
        """Verify the fields in a JSONL line."""

        if not isinstance(line, dict):
            raise ValueError(f"Expected a dict, got {line}")

        for field in JsonlFields.REQUIRED:
            if field not in line:
                raise ValueError(f"Missing required field {field} in {line}")

        if "split" in line and line["split"] not in self.SPLIT_TYPES:
            raise ValueError(f"Split type can only be {self.SPLIT_TYPES}, got {line}")

        for field in line.keys():
            if field not in JsonlFields.REQUIRED + JsonlFields.OPTIONAL:
                self.ignored_fields.add(field)

    def get_test(self) -> List[Theorem]:
        """Return the theorems for testing."""

        return TheoremLoader.load_theorems_by_type(
            typed_theorems=self._theorems, theorem_type=TheoremType.TEST
        )

    def get_valid(self) -> List[Theorem]:
        """Return the theorems for validation."""

        return TheoremLoader.load_theorems_by_type(
            typed_theorems=self._theorems, theorem_type=TheoremType.VALID
        )

    def get_generic(self) -> List[Theorem]:
        """Return the theorems for expert iteration."""

        return TheoremLoader.load_theorems_by_type(
            typed_theorems=self._theorems, theorem_type=TheoremType.GENERIC
        )
