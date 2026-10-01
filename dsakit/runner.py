"""Discovery + CLI for running problem test suites in isolated subprocesses."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

from .harness import c

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS_DIR = ROOT / "problems"

USAGE = """usage: py run.py [selector ...] [options]

selectors
  (none)                  run every problem
  1                       run problem p001
  p001 3                  run problems p001 and p003
  two-sum                 run problems whose folder name contains 'two-sum'

options
  -l, --list              list problems and their status
      --time-limit MS     per-case time budget (default: 5000, 0 disables)
      --memory-limit MB   per-case memory budget (default: 512, 0 disables)
      --no-limits         disable both limits; let a slow solution finish
  -h, --help              show this message

Cases that blow a budget are reported as TLE / MLE and aborted, so you never
wait on a runaway solution.
"""


def discover() -> list[Path]:
    if not PROBLEMS_DIR.is_dir():
        return []
    return sorted(
        p for p in PROBLEMS_DIR.iterdir() if p.is_dir() and (p / "tests.py").is_file()
    )


def matches(problem: Path, selector: str) -> bool:
    name = problem.name.lower()
    token = selector.strip().lower()
    if not token:
        return False
    if token.isdigit():
        return name.startswith(f"p{int(token):03d}")
    return token in name


def select(problems: Iterable[Path], selectors: list[str]) -> list[Path]:
    problems = list(problems)
    if not selectors:
        return problems
    chosen: list[Path] = []
    for problem in problems:
        if any(matches(problem, s) for s in selectors) and problem not in chosen:
            chosen.append(problem)
    return chosen


def is_stub(problem: Path) -> bool:
    solution = problem / "solution.py"
    if not solution.is_file():
        return True
    text = solution.read_text(encoding="utf-8")
    return bool(re.search(r"^\s*raise NotImplementedError", text, re.M))


ALLOWED_FILES = {"README.md", "solution.py", "tests.py"}


def stray_files(problem: Path) -> list[str]:
    """Files a problem folder should not contain. Reviews belong in chat, not on disk."""
    return sorted(
        item.name
        for item in problem.iterdir()
        if item.is_file() and item.name not in ALLOWED_FILES
    )


def list_problems(problems: list[Path]) -> int:
    if not problems:
        print(c("No problems yet. Ask the agent for one.", "yellow"))
        return 0
    print(c(f"{len(problems)} problem(s)", "bold", "cyan"))
    strays: list[str] = []
    for problem in problems:
        status = c("todo", "yellow") if is_stub(problem) else c("attempted", "green")
        print(f"  {problem.name:<52} {status}")
        strays += [f"{problem.name}/{name}" for name in stray_files(problem)]
    if strays:
        print()
        print(c("unexpected files (a problem folder holds only README.md,", "yellow"))
        print(c("solution.py and tests.py - reviews stay in chat):", "yellow"))
        for path in strays:
            print(c(f"  {path}", "yellow"))
    return 0


def run_problem(problem: Path, env: dict) -> int:
    print(c("=" * 72, "grey"))
    print(c(problem.name, "bold"))
    sys.stdout.flush()
    result = subprocess.run(
        [sys.executable, str(problem / "tests.py")], cwd=str(problem), env=env
    )
    return result.returncode


class ArgError(ValueError):
    pass


def _take_value(argv: list[str], index: int, flag: str) -> tuple[int, int]:
    """Read ``--flag N`` or ``--flag=N``; returns (value, index_of_last_token)."""
    token = argv[index]
    if "=" in token:
        raw = token.split("=", 1)[1]
    else:
        if index + 1 >= len(argv):
            raise ArgError(f"{flag} needs a value")
        raw = argv[index + 1]
        index += 1
    try:
        value = int(raw)
    except ValueError:
        raise ArgError(f"{flag} needs an integer, got {raw!r}") from None
    if value < 0:
        raise ArgError(f"{flag} must be >= 0")
    return value, index


def parse_args(argv: list[str]) -> tuple[list[str], bool, dict]:
    """Returns (selectors, want_list, env_overrides)."""
    selectors: list[str] = []
    want_list = False
    overrides: dict = {}

    i = 0
    while i < len(argv):
        token = argv[i]
        head = token.split("=", 1)[0]
        if head in ("-l", "--list"):
            want_list = True
        elif head == "--no-limits":
            overrides["DSAKIT_TIME_LIMIT_MS"] = "0"
            overrides["DSAKIT_MEMORY_LIMIT_MB"] = "0"
        elif head == "--time-limit":
            value, i = _take_value(argv, i, "--time-limit")
            overrides["DSAKIT_TIME_LIMIT_MS"] = str(value)
        elif head == "--memory-limit":
            value, i = _take_value(argv, i, "--memory-limit")
            overrides["DSAKIT_MEMORY_LIMIT_MB"] = str(value)
        elif token.startswith("-"):
            raise ArgError(f"unknown option {token!r}")
        else:
            selectors.append(token)
        i += 1

    return selectors, want_list, overrides


def _describe(overrides: dict) -> str:
    parts = []
    time_ms = overrides.get("DSAKIT_TIME_LIMIT_MS")
    mem_mb = overrides.get("DSAKIT_MEMORY_LIMIT_MB")
    if time_ms == "0":
        parts.append("time limit off")
    elif time_ms is not None:
        parts.append(f"time limit {time_ms} ms")
    if mem_mb == "0":
        parts.append("memory limit off")
    elif mem_mb is not None:
        parts.append(f"memory limit {mem_mb} MB")
    return ", ".join(parts)


def main(argv: list[str]) -> int:
    if any(a in ("-h", "--help") for a in argv):
        print(USAGE)
        return 0

    try:
        selectors, want_list, overrides = parse_args(argv)
    except ArgError as exc:
        print(c(f"error: {exc}", "red"))
        print()
        print(USAGE)
        return 2

    problems = select(discover(), selectors)

    if want_list:
        return list_problems(problems)

    if not problems:
        if selectors:
            print(c(f"No problem matched: {' '.join(selectors)}", "red"))
        else:
            print(c("No problems found under problems/. Ask the agent for one.", "yellow"))
        return 1

    env = {**os.environ, **overrides}
    if overrides:
        print(c("limits: " + _describe(overrides), "grey"))

    codes = {problem.name: run_problem(problem, env) for problem in problems}

    if len(codes) > 1:
        print(c("=" * 72, "grey"))
        print(c("overall", "bold"))
        for name, code in codes.items():
            tag = {0: c("PASS", "green"), 2: c("TODO", "yellow")}.get(code, c("FAIL", "red"))
            print(f"  {tag}  {name}")

    return 0 if all(code == 0 for code in codes.values()) else 1
