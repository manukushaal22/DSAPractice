"""Discovery + CLI for running problem test suites in isolated subprocesses.

Two tracks are discovered:

* ``problems/pNNN-slug/``                    -- the mixed interview drill
* ``learn/NN-topic/NN.K-slug/``              -- the topic-by-topic learning path
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Optional

from .harness import c

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS_DIR = ROOT / "problems"
LEARN_DIR = ROOT / "learn"

# learn/03-sliding-window/
TOPIC_RE = re.compile(r"^(\d{2})-[a-z0-9-]+$")
# learn/03-sliding-window/03.4-some-slug/  (03.4b-... for an inserted sibling rung)
EXERCISE_RE = re.compile(r"^(\d{2})\.(\d+)([a-z]?)-[a-z0-9-]+$")
# CLI selectors: L3, L03, L3.4, L03.4b
LEARN_SELECTOR_RE = re.compile(r"^l(\d{1,2})(?:\.(\d+)([a-z]?))?$")

USAGE = """usage: py run.py [selector ...] [options]

selectors
  (none)                  run everything (problems/ and learn/)
  1                       run problem p001
  p001 3                  run problems p001 and p003
  two-sum                 run exercises whose folder name contains 'two-sum'
  L3.4                    run learn exercise 03.4 (L3.4b for an inserted sibling)
  L3                      run every exercise in learn topic 03
  learn | problems        run one whole track

options
  -l, --list              list problems and their status
      --time-limit MS     per-case time budget (default: 5000, 0 disables)
      --memory-limit MB   per-case memory budget (default: 512, 0 disables)
      --no-limits         disable both limits; let a slow solution finish
  -h, --help              show this message

Cases that blow a budget are reported as TLE / MLE and aborted, so you never
wait on a runaway solution.
"""


def discover_problems() -> list[Path]:
    if not PROBLEMS_DIR.is_dir():
        return []
    return sorted(
        p for p in PROBLEMS_DIR.iterdir() if p.is_dir() and (p / "tests.py").is_file()
    )


def learn_topics() -> list[Path]:
    if not LEARN_DIR.is_dir():
        return []
    return sorted(p for p in LEARN_DIR.iterdir() if p.is_dir() and TOPIC_RE.match(p.name))


def _exercise_key(exercise: Path) -> tuple:
    match = EXERCISE_RE.match(exercise.name)
    if not match:
        return (1 << 30, "", exercise.name)
    return (int(match.group(2)), match.group(3), exercise.name)


def learn_exercises(topic: Path) -> list[Path]:
    """Exercise folders of one topic, in rung order (03.2 < 03.3 < 03.3b < 03.10)."""
    found = [
        p
        for p in topic.iterdir()
        if p.is_dir() and EXERCISE_RE.match(p.name) and (p / "tests.py").is_file()
    ]
    return sorted(found, key=_exercise_key)


def discover() -> list[Path]:
    """Every runnable folder: problems/ first, then learn/ in topic and rung order."""
    learn = [exercise for topic in learn_topics() for exercise in learn_exercises(topic)]
    return discover_problems() + learn


def is_learn(problem: Path) -> bool:
    return problem.parent.parent == LEARN_DIR


def exercise_id(problem: Path) -> Optional[str]:
    """``L03.4`` / ``L03.4b`` for a learn exercise, ``None`` otherwise."""
    match = EXERCISE_RE.match(problem.name)
    if not is_learn(problem) or not match:
        return None
    return f"L{match.group(1)}.{match.group(2)}{match.group(3)}"


def display_name(problem: Path) -> str:
    if is_learn(problem):
        return f"{problem.parent.name}/{problem.name}"
    return problem.name


def matches(problem: Path, selector: str) -> bool:
    token = selector.strip().lower()
    if not token:
        return False
    learn = is_learn(problem)
    if token in ("learn", "problems"):
        return learn == (token == "learn")

    learn_selector = LEARN_SELECTOR_RE.match(token)
    if learn_selector:
        if not learn:
            return False
        exercise = EXERCISE_RE.match(problem.name)
        if not exercise or int(exercise.group(1)) != int(learn_selector.group(1)):
            return False
        if learn_selector.group(2) is None:
            return True
        return (
            int(exercise.group(2)) == int(learn_selector.group(2))
            and exercise.group(3) == learn_selector.group(3)
        )

    if token.isdigit():
        return not learn and problem.name.startswith(f"p{int(token):03d}")
    # Substring over "topic/exercise" so a topic folder name selects the whole topic.
    return token in display_name(problem).lower()


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
# learn/README.md is the roadmap; learn/NN-topic/README.md is that topic's lesson.
ALLOWED_LEARN_FILES = {"README.md"}


def stray_files(problem: Path) -> list[str]:
    """Files a problem folder should not contain. Reviews belong in chat, not on disk."""
    return sorted(
        item.name
        for item in problem.iterdir()
        if item.is_file() and item.name not in ALLOWED_FILES
    )


def stray_learn_files() -> list[str]:
    """Unexpected files at the learn/ root or directly inside a topic folder."""
    if not LEARN_DIR.is_dir():
        return []
    strays = [
        f"learn/{item.name}"
        for item in LEARN_DIR.iterdir()
        if item.is_file() and item.name not in ALLOWED_LEARN_FILES
    ]
    for topic in learn_topics():
        strays += [
            f"learn/{topic.name}/{item.name}"
            for item in topic.iterdir()
            if item.is_file() and item.name not in ALLOWED_LEARN_FILES
        ]
    return sorted(strays)


def _status(problem: Path) -> str:
    return c("todo", "yellow") if is_stub(problem) else c("attempted", "green")


def list_problems(problems: list[Path]) -> int:
    if not problems:
        print(c("Nothing to list yet. Ask the agent for a problem or a topic.", "yellow"))
        return 0

    drill = [p for p in problems if not is_learn(p)]
    learn = [p for p in problems if is_learn(p)]
    strays: list[str] = []

    if drill:
        print(c(f"problems/  {len(drill)} problem(s)", "bold", "cyan"))
        for problem in drill:
            print(f"  {problem.name:<52} {_status(problem)}")
            strays += [f"problems/{problem.name}/{name}" for name in stray_files(problem)]

    if learn:
        if drill:
            print()
        print(c(f"learn/  {len(learn)} exercise(s)", "bold", "cyan"))
        topic: Optional[Path] = None
        for problem in learn:
            if problem.parent != topic:
                topic = problem.parent
                print(c(f"  {topic.name}", "bold"))
            label = f"{exercise_id(problem)}  {problem.name}"
            print(f"    {label:<58} {_status(problem)}")
            strays += [f"learn/{display_name(problem)}/{name}" for name in stray_files(problem)]

    strays += stray_learn_files()
    if strays:
        print()
        print(c("unexpected files (an exercise folder holds only README.md, solution.py", "yellow"))
        print(c("and tests.py; a learn topic folder holds only its README.md lesson -", "yellow"))
        print(c("reviews stay in chat):", "yellow"))
        for path in strays:
            print(c(f"  {path}", "yellow"))
    return 0


def run_problem(problem: Path, env: dict) -> int:
    print(c("=" * 72, "grey"))
    print(c(display_name(problem), "bold"))
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
            print(c("Nothing found under problems/ or learn/. Ask the agent for one.", "yellow"))
        return 1

    env = {**os.environ, **overrides}
    if overrides:
        print(c("limits: " + _describe(overrides), "grey"))

    codes = {display_name(problem): run_problem(problem, env) for problem in problems}

    if len(codes) > 1:
        print(c("=" * 72, "grey"))
        print(c("overall", "bold"))
        for name, code in codes.items():
            tag = {0: c("PASS", "green"), 2: c("TODO", "yellow")}.get(code, c("FAIL", "red"))
            print(f"  {tag}  {name}")

    return 0 if all(code == 0 for code in codes.values()) else 1
