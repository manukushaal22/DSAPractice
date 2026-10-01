"""Spawns the child runner and relays its NDJSON stream.

The submitted code is written to a throwaway temp file, never into the problem
folder. `child_runner` substitutes that file for `solution.py` at import time, so
running code from the browser leaves the repo untouched.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import AsyncIterator, Optional

SERVER_DIR = Path(__file__).resolve().parent
CHILD_RUNNER = SERVER_DIR / "child_runner.py"
REPO_ROOT = SERVER_DIR.parents[1]

# Kill a child that ignores the stream closing (a thread stuck in a long C-level
# call can outlive dsakit's abort injection).
KILL_GRACE_SECONDS = 3.0


def _child_env() -> dict:
    env = dict(os.environ)
    env["PYTHONUNBUFFERED"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["NO_COLOR"] = "1"
    # child_runner imports tests.py as a module (the CLI runs it as __main__, which is
    # never cached). Without this it would drop a tests.pyc into the problem folder -
    # a write into a directory this app promises never to touch.
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # Never let an ambient override silently change the budgets the tests declare.
    env.pop("DSAKIT_TIME_LIMIT_MS", None)
    env.pop("DSAKIT_MEMORY_LIMIT_MB", None)
    return env


def _line(payload: dict) -> bytes:
    return (json.dumps(payload) + "\n").encode("utf-8")


async def _drain(stream) -> bytes:
    try:
        return await stream.read()
    except Exception:
        return b""


async def stream_run(problem_dir: Path, code: str) -> AsyncIterator[bytes]:
    """Yield NDJSON lines from a run of ``code`` against ``problem_dir``'s tests.

    Terminates the child if the consumer stops reading (Stop pressed, tab closed).
    """
    workdir = Path(tempfile.mkdtemp(prefix="lcp-run-"))
    solution_file = workdir / "solution.py"
    proc: Optional[asyncio.subprocess.Process] = None
    stderr_task: Optional[asyncio.Task] = None
    saw_terminal_event = False

    try:
        solution_file.write_text(code, encoding="utf-8")

        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            str(CHILD_RUNNER),
            str(problem_dir),
            str(solution_file),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(REPO_ROOT),
            env=_child_env(),
        )
        assert proc.stdout is not None and proc.stderr is not None
        stderr_task = asyncio.create_task(_drain(proc.stderr))

        while True:
            # Perf fixtures can produce long lines; readline's default limit is 64 KiB
            # and the child truncates well below that, so this is safe.
            raw = await proc.stdout.readline()
            if not raw:
                break
            stripped = raw.strip()
            if not stripped:
                continue
            try:
                event_type = json.loads(stripped).get("type")
            except json.JSONDecodeError:
                # Not ours - something printed to the real stdout. Pass it through
                # as a note rather than corrupting the stream.
                yield _line({"type": "noise", "text": stripped.decode("utf-8", "replace")})
                continue
            if event_type in ("done", "fatal"):
                saw_terminal_event = True
            yield raw if raw.endswith(b"\n") else raw + b"\n"

        returncode = await proc.wait()
        if not saw_terminal_event:
            stderr_text = (await stderr_task).decode("utf-8", "replace").strip()
            yield _line(
                {
                    "type": "fatal",
                    "kind": "crash",
                    "message": f"the runner exited with code {returncode} before finishing",
                    "traceback": stderr_text[-4000:],
                }
            )

    except asyncio.CancelledError:
        raise
    finally:
        if proc is not None and proc.returncode is None:
            try:
                proc.kill()
                await asyncio.wait_for(proc.wait(), timeout=KILL_GRACE_SECONDS)
            except (ProcessLookupError, asyncio.TimeoutError):
                pass
        if stderr_task is not None and not stderr_task.done():
            stderr_task.cancel()
        shutil.rmtree(workdir, ignore_errors=True)
