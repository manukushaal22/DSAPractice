"""FastAPI app for the local solver UI.

Read-only over ``problems/`` and ``learn/`` except for one endpoint:
``PUT .../solution``, which is the only thing in this app that ever writes into a
problem or exercise folder, and only when the human presses Save.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import catalog, execute, state

APP_DIR = Path(__file__).resolve().parents[1]
DIST_DIR = APP_DIR / "web" / "dist"

app = FastAPI(title="LCP Solver", version="1.0.0")

# The Vite dev server runs on another origin; in the built/single-command mode the
# frontend is same-origin and this is simply unused.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    code: str = Field(..., description="Editor buffer to execute")


class SaveRequest(BaseModel):
    code: str
    baseMtime: Optional[str] = Field(
        None, description="st_mtime_ns of solution.py when it was loaded, as a string"
    )
    force: bool = Field(False, description="Overwrite even if the file changed on disk")


def _mtime_ns(path: Path) -> Optional[str]:
    # Sent as a string: st_mtime_ns exceeds JavaScript's safe integer range.
    try:
        return str(path.stat().st_mtime_ns)
    except OSError:
        return None


def _existing_newline(path: Path) -> str:
    """Line-ending style already used by the file.

    The browser always sends "\\n"-separated text. This repo's files are CRLF, and
    rewriting every line on Save would be a silent, invisible change to the file.
    """
    try:
        return "\r\n" if b"\r\n" in path.read_bytes() else "\n"
    except OSError:
        return os.linesep


def _require(problem_id: str) -> catalog.Problem:
    problem = catalog.find_problem(problem_id)
    if problem is None:
        raise HTTPException(status_code=404, detail=f"no problem matching {problem_id!r}")
    return problem


def _summary(problem: catalog.Problem, last_runs: dict) -> dict:
    return {**catalog.as_dict(problem), "lastRun": last_runs.get(problem.id)}


@app.get("/api/problems")
def list_problems() -> dict:
    last_runs = state.all_last_runs()
    problems = catalog.load_problems()
    return {"problems": [_summary(p, last_runs) for p in problems]}


@app.get("/api/learn")
def list_topics() -> dict:
    last_runs = state.all_last_runs()
    return {"topics": [catalog.topic_dict(t, last_runs) for t in catalog.load_topics()]}


@app.get("/api/learn/{topic_id}")
def get_topic(topic_id: str) -> dict:
    topic = catalog.find_topic(topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail=f"no learn topic matching {topic_id!r}")
    return {
        **catalog.topic_dict(topic, state.all_last_runs()),
        "lesson": catalog.lesson_text(topic),
    }


@app.get("/api/problems/{problem_id}")
def get_problem(problem_id: str) -> dict:
    problem = _require(problem_id)
    directory = catalog.problem_dir(problem)
    solution_file = directory / "solution.py"

    def read(name: str) -> str:
        try:
            return (directory / name).read_text(encoding="utf-8")
        except OSError:
            return ""

    return {
        **_summary(problem, state.all_last_runs()),
        "readme": read("README.md"),
        "code": read("solution.py"),
        "mtime": _mtime_ns(solution_file),
    }


@app.post("/api/problems/{problem_id}/run")
async def run_problem(problem_id: str, request: RunRequest) -> StreamingResponse:
    problem = _require(problem_id)
    directory = catalog.problem_dir(problem)

    async def generate():
        passed = total = 0
        verdict = "unknown"
        async for line in execute.stream_run(directory, request.code):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                event = {}
            if event.get("type") == "done":
                passed = event.get("passed", 0)
                total = event.get("total", 0)
                verdict = event.get("verdict", "unknown")
            yield line
        if verdict != "unknown":
            state.record_run(problem.id, passed, total, verdict)

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
        },
    )


@app.put("/api/problems/{problem_id}/solution")
def save_solution(problem_id: str, request: SaveRequest) -> dict:
    problem = _require(problem_id)
    solution_file = catalog.problem_dir(problem) / "solution.py"

    current = _mtime_ns(solution_file)
    if not request.force and request.baseMtime is not None and current != request.baseMtime:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "solution.py changed on disk since you opened it",
                "diskCode": solution_file.read_text(encoding="utf-8"),
                "mtime": current,
            },
        )

    newline = _existing_newline(solution_file)
    try:
        solution_file.write_text(request.code, encoding="utf-8", newline=newline)
    except OSError as exc:
        raise HTTPException(status_code=500, detail=f"could not write solution.py: {exc}")

    catalog.load_problems(force=True)  # stub status may have just changed
    return {"saved": True, "mtime": _mtime_ns(solution_file)}


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "repoRoot": str(catalog.ROOT), "frontendBuilt": DIST_DIR.is_dir()}


# --------------------------------------------------------------------------
# built frontend (only when `npm run build` has been run)
# --------------------------------------------------------------------------

if DIST_DIR.is_dir():
    app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def spa(full_path: str):
        """Serve index.html for client-side routes like /p/p009."""
        candidate = (DIST_DIR / full_path).resolve()
        if full_path and candidate.is_file() and DIST_DIR.resolve() in candidate.parents:
            return FileResponse(candidate)
        return FileResponse(DIST_DIR / "index.html")
