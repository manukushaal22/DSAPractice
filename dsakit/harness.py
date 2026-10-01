"""Minimal test harness for DSA practice problems.

No third-party dependencies. A problem's ``tests.py`` builds a list of
:class:`Case` objects and hands them to :func:`run_cases`.

Every case runs under a time limit and a memory limit, so a runaway solution is
reported as TLE/MLE within seconds instead of being waited on indefinitely.
"""

from __future__ import annotations

import copy
import os
import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Sequence

from .limits import MEMORY_SUPPORTED, call_with_limits

MAX_REPR = 220

DEFAULT_TIME_LIMIT_MS = 5_000
DEFAULT_MEMORY_LIMIT_MB = 512

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_STUB = 2


def _supports_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        return False
    if os.name == "nt":
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            mode = ctypes.c_uint32()
            if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                return False
            kernel32.SetConsoleMode(handle, mode.value | 0x4)  # VT processing
        except Exception:
            return False
    return True


_COLOR = _supports_color()
_CODES = {
    "green": "\033[32m",
    "red": "\033[31m",
    "yellow": "\033[33m",
    "cyan": "\033[36m",
    "magenta": "\033[35m",
    "grey": "\033[90m",
    "bold": "\033[1m",
}


def c(text: str, *styles: str) -> str:
    if not _COLOR:
        return text
    prefix = "".join(_CODES.get(s, "") for s in styles)
    return f"{prefix}{text}\033[0m" if prefix else text


def _short(value: Any) -> str:
    try:
        text = repr(value)
    except Exception:
        text = f"<unrepresentable {type(value).__name__}>"
    if len(text) > MAX_REPR:
        text = text[: MAX_REPR - 3] + "..."
    return text


def _mb(num_bytes: int) -> str:
    return f"{num_bytes / (1024 * 1024):.1f} MB"


def _env_int(name: str) -> Optional[int]:
    raw = os.environ.get(name)
    if not raw:
        return None
    try:
        value = int(raw)
    except ValueError:
        return None
    return max(value, 0)  # 0 means "disabled"


@dataclass
class Case:
    """One test case.

    args
        Positional arguments passed to the solution function.
    expected
        Expected return value.
    kwargs
        Optional keyword arguments.
    name
        Optional short label shown in the output.
    cmp
        Optional custom comparator ``(actual, expected) -> bool``. Use it when
        the answer is not unique (e.g. any valid ordering is acceptable).
    expected_args
        Optional expected state of ``args`` *after* the call. Use it for
        in-place problems where the mutation is the real answer.
    note
        Extra context printed when the case fails.
    time_limit_ms
        Per-case time budget, overriding the suite default. Use a tight value on
        perf cases so a too-slow algorithm is reported quickly.
    memory_limit_mb
        Per-case memory budget, overriding the suite default.
    """

    args: Sequence[Any] = ()
    expected: Any = None
    kwargs: dict = field(default_factory=dict)
    name: Optional[str] = None
    cmp: Optional[Callable[[Any, Any], bool]] = None
    expected_args: Optional[Sequence[Any]] = None
    note: Optional[str] = None
    time_limit_ms: Optional[int] = None
    memory_limit_mb: Optional[int] = None


def _label(index: int, case: Case) -> str:
    base = f"case {index:>2}"
    return f"{base} ({case.name})" if case.name else base


def _resolve(case_value: Optional[int], suite_value: Optional[int], env_name: str) -> Optional[float]:
    """Env override wins, then the per-case value, then the suite default."""
    override = _env_int(env_name)
    if override is not None:
        chosen: Optional[int] = override
    elif case_value is not None:
        chosen = case_value
    else:
        chosen = suite_value
    if chosen is None or chosen <= 0:
        return None
    return float(chosen)


def run_cases(
    func: Callable[..., Any],
    cases: Sequence[Case],
    title: str = "",
    time_limit_ms: Optional[int] = DEFAULT_TIME_LIMIT_MS,
    memory_limit_mb: Optional[int] = DEFAULT_MEMORY_LIMIT_MB,
) -> int:
    """Run ``cases`` against ``func``. Returns a process exit code (0 == pass)."""

    if title:
        print(c(title, "bold", "cyan"))

    passed = 0
    failures: list[str] = []
    total_ms = 0.0
    slowest = 0.0
    peak_bytes = 0
    zombies = 0
    limit_hits = 0

    for i, case in enumerate(cases, start=1):
        label = _label(i, case)
        call_args = copy.deepcopy(list(case.args))
        call_kwargs = copy.deepcopy(case.kwargs)

        time_limit_s = _resolve(case.time_limit_ms, time_limit_ms, "DSAKIT_TIME_LIMIT_MS")
        if time_limit_s is not None:
            time_limit_s /= 1000.0
        mem_limit_mb = _resolve(case.memory_limit_mb, memory_limit_mb, "DSAKIT_MEMORY_LIMIT_MB")
        mem_limit_b = int(mem_limit_mb * 1024 * 1024) if mem_limit_mb is not None else None
        if not MEMORY_SUPPORTED:
            mem_limit_b = None

        outcome = call_with_limits(func, call_args, call_kwargs, time_limit_s, mem_limit_b)

        total_ms += outcome.elapsed_ms
        peak_bytes = max(peak_bytes, outcome.peak_bytes)
        if outcome.zombie:
            zombies += 1

        if outcome.status == "stub":
            print(c("  solution.py is still a stub - implement the function first.", "yellow"))
            return EXIT_STUB

        if outcome.status == "timeout":
            limit_hits += 1
            budget = int(time_limit_s * 1000) if time_limit_s else 0
            print(f"{c('TLE ', 'magenta', 'bold')}  {label}")
            print(c(f"    exceeded the {budget} ms budget - aborted after {outcome.elapsed_ms:.0f} ms", "magenta"))
            print(c(f"    input    : {_short(tuple(case.args))}", "grey"))
            print(c("    Too slow for this input size. Re-read 'Target complexity' in README.md.", "yellow"))
            if case.note:
                print(c(f"    note     : {case.note}", "yellow"))
            failures.append(label)
            continue

        if outcome.status == "memory":
            limit_hits += 1
            budget = f"{mem_limit_mb:.0f}" if mem_limit_mb else "?"
            print(f"{c('MLE ', 'magenta', 'bold')}  {label}")
            print(c(f"    exceeded the {budget} MB budget - peaked at {_mb(outcome.peak_bytes)}", "magenta"))
            print(c(f"    input    : {_short(tuple(case.args))}", "grey"))
            print(c("    Allocating far more than the input warrants - look for copies,", "yellow"))
            print(c("    slices, or tables built inside a loop.", "yellow"))
            if case.note:
                print(c(f"    note     : {case.note}", "yellow"))
            failures.append(label)
            continue

        if outcome.status == "error":
            print(f"{c('ERR ', 'red', 'bold')}  {label}  {c('raised an exception', 'red')}")
            print(c(f"    input    : {_short(tuple(case.args))}", "grey"))
            for line in (outcome.error or "").strip().splitlines()[-3:]:
                print(c("    " + line.strip(), "grey"))
            failures.append(label)
            continue

        slowest = max(slowest, outcome.elapsed_ms)
        actual = outcome.value

        ok = case.cmp(actual, case.expected) if case.cmp else actual == case.expected
        mutation_ok = True
        if case.expected_args is not None:
            mutation_ok = list(call_args) == list(case.expected_args)

        if ok and mutation_ok:
            passed += 1
            detail = f"{outcome.elapsed_ms:8.2f} ms"
            if outcome.peak_bytes >= 1024 * 1024:
                detail += f"  {_mb(outcome.peak_bytes):>9}"
            print(f"{c('PASS', 'green')}  {label}  {c(detail, 'grey')}")
            continue

        print(f"{c('FAIL', 'red', 'bold')}  {label}")
        print(c(f"    input    : {_short(tuple(case.args))}", "grey"))
        if not ok:
            print(f"    expected : {c(_short(case.expected), 'green')}")
            print(f"    actual   : {c(_short(actual), 'red')}")
        if not mutation_ok:
            print(f"    expected args after call : {c(_short(tuple(case.expected_args)), 'green')}")
            print(f"    actual args after call   : {c(_short(tuple(call_args)), 'red')}")
        if case.note:
            print(c(f"    note     : {case.note}", "yellow"))
        failures.append(label)

    total = len(cases)
    print()

    if zombies:
        print(
            c(
                f"note: {zombies} aborted case(s) did not stop immediately (stuck inside a long\n"
                "      C-level call). They are abandoned and die with this process.",
                "yellow",
            )
        )

    summary = f"{passed}/{total} passed  |  total {total_ms:.2f} ms  |  slowest completed case {slowest:.2f} ms"
    if peak_bytes >= 1024 * 1024:
        summary += f"  |  peak {_mb(peak_bytes)}"

    if failures:
        print(c(summary, "red", "bold"))
        print(c("failed: " + ", ".join(failures), "red"))
        if limit_hits:
            print(c("tip: `py run.py N --no-limits` lets a slow solution run to completion.", "grey"))
        return EXIT_FAIL

    print(c(summary, "green", "bold"))
    return EXIT_OK
