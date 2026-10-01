"""Persisted last-run badges, stored outside the problem folders.

`dsakit.runner.stray_files` flags anything in a problem folder that is not one of
the three allowed files, so app state lives in ``solverapp/.data/state.json``
(gitignored) instead.
"""

from __future__ import annotations

import json
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Optional

DATA_DIR = Path(__file__).resolve().parents[1] / ".data"
STATE_FILE = DATA_DIR / "state.json"

_lock = threading.Lock()


def _empty() -> dict:
    return {"version": 1, "lastRuns": {}}


def _load_unlocked() -> dict:
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _empty()
    if not isinstance(data, dict) or not isinstance(data.get("lastRuns"), dict):
        return _empty()
    return data


def _save_unlocked(data: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    # Write to a temp file in the same directory, then replace: a crash mid-write
    # can never leave a truncated state.json behind.
    handle, temp_name = tempfile.mkstemp(dir=str(DATA_DIR), suffix=".tmp")
    temp_path = Path(temp_name)
    try:
        with open(handle, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        temp_path.replace(STATE_FILE)
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise


def all_last_runs() -> dict[str, Any]:
    with _lock:
        return dict(_load_unlocked()["lastRuns"])


def get_last_run(problem_id: str) -> Optional[dict]:
    return all_last_runs().get(problem_id)


def record_run(problem_id: str, passed: int, total: int, verdict: str) -> dict:
    """Store the outcome of one run. Returns the stored record."""
    record = {
        "passed": passed,
        "total": total,
        "verdict": verdict,
        "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    with _lock:
        data = _load_unlocked()
        data["lastRuns"][problem_id] = record
        _save_unlocked(data)
    return record
