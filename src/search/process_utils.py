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

import asyncio, threading, time, psutil

from typing import Any
from loguru import logger


class LeanCPUTimedOut(TimeoutError):
    def __init__(self, limit_type: str, cpu_elapsed: float,
                 wall_elapsed: float, limit_value: float, killed_hard: bool):
        super().__init__(
            f"{limit_type}-time limit exceeded "
            f"(cpu={cpu_elapsed:.6f}s / wall={wall_elapsed:.3f}s ≥ {limit_value})"
        )
        self.limit_type   = limit_type
        self.cpu_elapsed  = cpu_elapsed
        self.wall_elapsed = wall_elapsed
        self.limit_value  = limit_value
        self.killed_hard = killed_hard

class DojoRestartRequired(Exception):
    """Raised when dojo needs to be restarted, requiring search to restart from beginning."""
    pass

def clean_old_dojo(dojo):
    try:
        if hasattr(dojo, 'proc') and dojo.proc:
            dojo.proc.close(force=True)
            dojo.__exit__(None, None, None)
            #dojo.proc = None   
    except Exception as e:
        logger.warning(f"Failed cleaning up dead dojo (expected): {e}")

def _kill_tree(proc: psutil.Process):
    try:
        for c in proc.children(recursive=True):
            _kill_tree(c)
        proc.kill()
    except psutil.NoSuchProcess:
        pass

def _cpu_tree(proc: psutil.Process) -> float:
    """user+sys CPU seconds, including all child processes; returns 0 if process disappeared"""
    try:
        u, s = proc.cpu_times()[:2]
        total = u + s
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return 0.0
    
    try:
        children = proc.children(recursive=True)
    except psutil.NoSuchProcess:
        return total
    
    for c in children:
        try:
            u, s = c.cpu_times()[:2]
            total += u + s
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return total

def _safe_set_exc(fut: asyncio.Future, exc: BaseException):
    if not fut.done():
        fut.set_exception(exc)

def _safe_set_result(fut: asyncio.Future, val: Any = None):
    if not fut.done():
        fut.set_result(val)
    
async def run_tac_cpu_timeout(
    dojo,
    state,
    tactic: str,
    focus_mode: bool = False,
    *,
    cpu_sec_limit: float = 3.0,
    wall_sec_limit: float = 30.0,
    poll_interval: float = 0.5,
):
    """
    • Monitor Lean subprocess CPU and wall time; if either exceeds limit ➜ kill process tree ➜ raise LeanCPUTimedOut
    • Return dojo.run_tac result or raise exception; no background threads/Futures left behind
    """
    tac = "focus " + tactic if focus_mode else tactic # Tactic only applies to the current goal when using plans
    
    try:
        lean_proc = psutil.Process(dojo.proc.pid)
    except psutil.NoSuchProcess:
        # Process already gone, run tactic anyway to get proper error
        return await asyncio.to_thread(dojo.run_tac, state, tac)
    
    start_cpu  = _cpu_tree(lean_proc)
    start_wall = time.perf_counter()

    loop        = asyncio.get_running_loop()
    monitor_fut = loop.create_future()
    stop_evt    = threading.Event()

    def _monitor(dojo=dojo, lean_proc=lean_proc):
        try:
            baseline: dict[int, float] = {}
            retired_total = 0.0

            def snapshot_tree() -> dict[int, float]:
                out = {}
                for p in [lean_proc, *lean_proc.children(recursive=True)]:
                    try:
                        u, s = p.cpu_times()[:2]
                        out[p.pid] = u + s
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                return out

            baseline = snapshot_tree()

            while not stop_evt.wait(poll_interval):
                if not lean_proc.is_running():
                    loop.call_soon_threadsafe(_safe_set_result, monitor_fut)
                    break

                cur = snapshot_tree()

                for pid in list(baseline.keys()):
                    if pid not in cur:
                        retired_total += baseline.pop(pid)

                acc_cpu = retired_total
                for pid, cur_cpu in cur.items():
                    base = baseline.get(pid, cur_cpu)
                    acc_cpu += cur_cpu - base
                    baseline[pid] = base

                wall_now = time.perf_counter() - start_wall
                if acc_cpu >= cpu_sec_limit or wall_now >= wall_sec_limit:
                    limit_type  = "cpu" if acc_cpu >= cpu_sec_limit else "wall"
                    limit_value = cpu_sec_limit if limit_type == "cpu" else wall_sec_limit
                    _kill_tree(lean_proc)
                    exc = LeanCPUTimedOut(limit_type, acc_cpu, wall_now,
                                        limit_value, killed_hard=True)
                    loop.call_soon_threadsafe(_safe_set_exc, monitor_fut, exc)
                    break

        except LeanCPUTimedOut as exc:
            loop.call_soon_threadsafe(_safe_set_exc, monitor_fut, exc)

        except psutil.Error:
            loop.call_soon_threadsafe(_safe_set_result, monitor_fut)

    mon_thread = threading.Thread(target=_monitor, daemon=True)
    mon_thread.start()

    tactic_task = asyncio.create_task(
        asyncio.to_thread(dojo.run_tac, state, tac)
    )
    tactic_task.add_done_callback(lambda t: t.exception() if not t.cancelled() else None)

    try:
        done, _ = await asyncio.wait(
            {tactic_task, monitor_fut},
            return_when=asyncio.FIRST_COMPLETED,
        )

        if monitor_fut in done and monitor_fut.exception():
            exc = monitor_fut.exception()
            try:
                await tactic_task
            except OSError:
                pass
            raise exc

        result = await tactic_task
        _safe_set_result(monitor_fut)
        await monitor_fut
        return result

    finally:
        stop_evt.set()
        mon_thread.join(timeout=0.1)
