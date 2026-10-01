"""Runs one problem's test suite against an arbitrary solution file.

Executed as a subprocess:

    python child_runner.py <problem_dir> <solution_file>

Emits one JSON object per line on stdout, flushed immediately so the server can
relay results while the suite is still running:

    {"type": "start",  "total": 15}
    {"type": "case",   "index": 1, "status": "pass", ...}
    {"type": "done",   "passed": 15, "total": 15, "verdict": "pass", ...}
    {"type": "fatal",  "kind": "syntax", "message": "...", "line": 12}

The interesting part is how ``<solution_file>`` is substituted for the problem's
real ``solution.py`` without touching the repo. Every ``tests.py`` does
``from solution import <fn>``, so this module loads the given file under the
module name ``solution`` and registers it in ``sys.modules`` *before* importing
``tests.py``. The import system finds the entry already present and never
consults the path finder, so ``problems/pNNN-slug/solution.py`` is never read.

``dsakit`` is used as a library and is not modified; the per-case semantics here
mirror ``dsakit.harness.run_cases``.
"""

from __future__ import annotations

import copy
import importlib.util
import io
import json
import os
import sys
import traceback
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any, Callable, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from dsakit.harness import (  # noqa: E402
    DEFAULT_MEMORY_LIMIT_MB,
    DEFAULT_TIME_LIMIT_MS,
    MAX_REPR,
)
from dsakit.limits import MEMORY_SUPPORTED, call_with_limits  # noqa: E402

MAX_STDOUT_CHARS = 8_000

# The NDJSON stream must never be polluted by the solution's own prints - including
# those of a zombie worker thread that outlived a TLE abort and keeps printing after
# its case was scored. So hold the real stdout aside and leave a capture installed as
# sys.stdout for the whole run.
REAL_STDOUT = sys.stdout


class _Capture(io.TextIOBase):
    """sys.stdout stand-in whose sink can be swapped between cases."""

    def __init__(self) -> None:
        self.sink = io.StringIO()

    def write(self, text: str) -> int:  # type: ignore[override]
        return self.sink.write(text)

    def flush(self) -> None:
        pass

    def isatty(self) -> bool:
        return False

    def swap(self) -> str:
        """Return everything written since the last swap and start a fresh sink."""
        text = self.sink.getvalue()
        self.sink = io.StringIO()
        return text


def emit(payload: dict) -> None:
    try:
        REAL_STDOUT.write(json.dumps(payload, default=repr) + "\n")
        REAL_STDOUT.flush()
    except (OSError, ValueError):
        # The reader went away (Stop pressed, page closed). Nothing left to say.
        raise SystemExit(1)


def short(value: Any) -> str:
    """Truncated repr. Perf fixtures hold 100k elements; the browser wants none of it."""
    try:
        text = repr(value)
    except Exception:
        text = f"<unrepresentable {type(value).__name__}>"
    if len(text) > MAX_REPR:
        text = text[: MAX_REPR - 3] + "..."
    return text


def fatal(kind: str, message: str, **extra: Any) -> None:
    emit({"type": "fatal", "kind": kind, "message": message, **extra})
    raise SystemExit(1)


def load_solution_module(solution_file: Path) -> None:
    """Compile and register ``solution_file`` as ``sys.modules["solution"]``."""
    try:
        source = solution_file.read_text(encoding="utf-8")
    except OSError as exc:
        fatal("io", f"could not read the submitted code: {exc}")

    try:
        compile(source, str(solution_file), "exec")
    except SyntaxError as exc:
        fatal(
            "syntax",
            f"{exc.msg}",
            line=exc.lineno,
            column=exc.offset,
            text=(exc.text or "").rstrip(),
        )

    spec = importlib.util.spec_from_file_location("solution", solution_file)
    if spec is None or spec.loader is None:
        fatal("import", "could not build an import spec for the submitted code")

    module = importlib.util.module_from_spec(spec)
    # Register before executing so a self-import inside the file resolves too.
    sys.modules["solution"] = module
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            spec.loader.exec_module(module)
    except BaseException:
        fatal(
            "import",
            "the submitted code raised while being imported",
            traceback="".join(traceback.format_exc()).strip()[-4000:],
        )


def load_tests_module(problem_dir: Path):
    tests_file = problem_dir / "tests.py"
    if not tests_file.is_file():
        fatal("io", f"no tests.py in {problem_dir.name}")

    # tests.py itself does sys.path.insert for the repo root and its own folder.
    # Both are harmless: `solution` is already in sys.modules, and dsakit resolves
    # from the repo root we prepended above.
    spec = importlib.util.spec_from_file_location(
        f"tests_{problem_dir.name.replace('-', '_')}", tests_file
    )
    if spec is None or spec.loader is None:
        fatal("import", f"could not build an import spec for {tests_file}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            spec.loader.exec_module(module)
    except BaseException:
        fatal(
            "import",
            f"{problem_dir.name}/tests.py failed to import",
            traceback="".join(traceback.format_exc()).strip()[-4000:],
        )
    return module


def find_solution_function(tests_module) -> Callable[..., Any]:
    """The function under test is whatever ``tests.py`` imported from ``solution``.

    Names differ per problem and are not exported, so identify it by origin
    rather than by name.
    """
    candidates = [
        value
        for value in vars(tests_module).values()
        if callable(value) and getattr(value, "__module__", None) == "solution"
    ]
    if not candidates:
        fatal(
            "import",
            "tests.py does not import any function from solution.py - has the "
            "function been renamed or removed?",
        )
    return candidates[0]


def env_int(name: str) -> Optional[int]:
    raw = os.environ.get(name)
    if not raw:
        return None
    try:
        return max(int(raw), 0)
    except ValueError:
        return None


def resolve_limit(case_value: Optional[int], suite_value: Optional[int], env_name: str):
    """Env override wins, then the per-case value, then the suite default."""
    override = env_int(env_name)
    chosen = override if override is not None else (case_value if case_value is not None else suite_value)
    if chosen is None or chosen <= 0:
        return None
    return float(chosen)


def describe_case(index: int, case) -> dict:
    return {
        "index": index,
        "name": getattr(case, "name", None) or f"case {index}",
        "isPerf": str(getattr(case, "name", "") or "").lower().startswith("perf"),
        "note": getattr(case, "note", None),
    }


def run(problem_dir: Path, solution_file: Path) -> int:
    load_solution_module(solution_file)
    tests_module = load_tests_module(problem_dir)
    func = find_solution_function(tests_module)

    cases = getattr(tests_module, "CASES", None)
    if not cases:
        fatal("import", "tests.py defines no CASES list")

    emit({"type": "start", "total": len(cases), "function": getattr(func, "__name__", "?")})

    capture = _Capture()
    sys.stdout = capture

    passed = 0
    total_ms = 0.0
    slowest = 0.0
    peak_bytes = 0
    failures: list[str] = []
    stub_seen = False

    for index, case in enumerate(cases, start=1):
        info = describe_case(index, case)
        call_args = copy.deepcopy(list(case.args))
        call_kwargs = copy.deepcopy(case.kwargs)

        time_limit_s = resolve_limit(
            case.time_limit_ms, DEFAULT_TIME_LIMIT_MS, "DSAKIT_TIME_LIMIT_MS"
        )
        if time_limit_s is not None:
            time_limit_s /= 1000.0
        mem_limit_mb = resolve_limit(
            case.memory_limit_mb, DEFAULT_MEMORY_LIMIT_MB, "DSAKIT_MEMORY_LIMIT_MB"
        )
        mem_limit_b = (
            int(mem_limit_mb * 1024 * 1024)
            if mem_limit_mb is not None and MEMORY_SUPPORTED
            else None
        )

        capture.swap()
        outcome = call_with_limits(func, call_args, call_kwargs, time_limit_s, mem_limit_b)
        stdout_text = capture.swap()
        if len(stdout_text) > MAX_STDOUT_CHARS:
            stdout_text = stdout_text[:MAX_STDOUT_CHARS] + "\n... (output truncated)"

        total_ms += outcome.elapsed_ms
        peak_bytes = max(peak_bytes, outcome.peak_bytes)

        event = {
            "type": "case",
            **info,
            "elapsedMs": round(outcome.elapsed_ms, 3),
            "peakBytes": outcome.peak_bytes,
            "stdout": stdout_text,
            "zombie": outcome.zombie,
            "input": short(tuple(case.args)),
        }

        if outcome.status == "stub":
            stub_seen = True
            emit({**event, "status": "stub"})
            break

        if outcome.status in ("timeout", "memory"):
            failures.append(info["name"])
            budget = (
                int(time_limit_s * 1000)
                if outcome.status == "timeout" and time_limit_s
                else (int(mem_limit_mb) if mem_limit_mb else None)
            )
            emit(
                {
                    **event,
                    "status": "tle" if outcome.status == "timeout" else "mle",
                    "budget": budget,
                }
            )
            continue

        if outcome.status == "error":
            failures.append(info["name"])
            emit(
                {
                    **event,
                    "status": "error",
                    "error": (outcome.error or "").strip()[-4000:],
                }
            )
            continue

        slowest = max(slowest, outcome.elapsed_ms)
        actual = outcome.value

        try:
            ok = case.cmp(actual, case.expected) if case.cmp else actual == case.expected
        except Exception:
            ok = False
        mutation_ok = True
        if case.expected_args is not None:
            mutation_ok = list(call_args) == list(case.expected_args)

        if ok and mutation_ok:
            passed += 1
            emit({**event, "status": "pass"})
            continue

        failures.append(info["name"])
        emit(
            {
                **event,
                "status": "fail",
                "expected": short(case.expected),
                "actual": short(actual),
                "comparedByCmp": case.cmp is not None,
                "expectedArgs": short(tuple(case.expected_args))
                if case.expected_args is not None
                else None,
                "actualArgs": short(tuple(call_args))
                if case.expected_args is not None
                else None,
                "mutationOk": mutation_ok,
            }
        )

    verdict = "stub" if stub_seen else ("pass" if not failures else "fail")
    emit(
        {
            "type": "done",
            "verdict": verdict,
            "passed": passed,
            "total": len(cases),
            "failed": failures,
            "totalMs": round(total_ms, 3),
            "slowestMs": round(slowest, 3),
            "peakBytes": peak_bytes,
            "memorySupported": MEMORY_SUPPORTED,
        }
    )
    return 0 if verdict == "pass" else (2 if verdict == "stub" else 1)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        emit(
            {
                "type": "fatal",
                "kind": "usage",
                "message": "usage: child_runner.py <problem_dir> <solution_file>",
            }
        )
        return 2
    return run(Path(argv[0]).resolve(), Path(argv[1]).resolve())


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except SystemExit:
        raise
    except BaseException:
        emit(
            {
                "type": "fatal",
                "kind": "internal",
                "message": "the runner itself crashed",
                "traceback": traceback.format_exc()[-4000:],
            }
        )
        raise SystemExit(1)
