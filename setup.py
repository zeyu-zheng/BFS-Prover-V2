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

from setuptools import find_packages, setup

setup(
    name="BFS-Prover",
    packages=find_packages(),
    version="2.0",
    install_requires=[
        "tqdm",
        "loguru",
        "transformers==4.53.2",
        "tensorboard",
        "openai",
        "rank_bm25",
        "lean-dojo==2.1.3",
        "sentencepiece",
        "ray==2.47.1",
        "torch==2.7.1",
        "vllm==0.10.0",
    ],
)
