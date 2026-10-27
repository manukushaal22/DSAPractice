"""Test cases for L01.5. Run from repo root:  py run.py L1.5

You can also run this file directly:
    py learn/01-arrays-and-hashing/01.5-longest-unbroken-streak/tests.py
Feel free to read this file - the big cases are built so their answers are known by
construction, not computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import longest_streak  # noqa: E402

import random  # noqa: E402


def _shuffled(items: list, seed: int) -> list:
    random.Random(seed).shuffle(items)
    return items


# ---------------------------------------------------------------- big inputs

# One streak of 200_000 values straddling zero, shuffled. Answer: all of it.
ONE_STREAK_LEN = 200_000
ONE_STREAK = _shuffled(list(range(-100_000, 100_000)), seed=3)

# The streak 0..99_999, where its start (0) appears 100_001 times. Answer 100_000.
# Looping over the raw list instead of the distinct values walks it ~1e5 times.
DUP_START = _shuffled([0] * 100_001 + list(range(1, 100_000)), seed=5)
DUP_START_ANSWER = 100_000

# 100_000 streaks of length 2 spread over [-1e9, 1e9): pairs (b, b + 1) with
# b = -1e9 + 19_999 * i, so consecutive pairs are 19_997 apart. Answer 2.
PAIRS = _shuffled(
    [v for i in range(100_000) for v in (-(10**9) + 19_999 * i, -(10**9) + 19_999 * i + 1)],
    seed=9,
)

CASES = [
    Case(
        name="example 1",
        args=([100, 4, 200, 1, 3, 2],),
        expected=4,
        expected_args=([100, 4, 200, 1, 3, 2],),
        note="Also checks the input list comes back unchanged.",
    ),
    Case(name="example 2 - duplicate inside the streak", args=([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],), expected=9),
    Case(
        name="example 3 - missing zero splits two runs",
        args=([-2, -1, 1, 2, 3],),
        expected=3,
    ),
    Case(name="empty list", args=([],), expected=0),
    Case(name="single value", args=([5],), expected=1),
    Case(
        name="all equal",
        args=([7, 7, 7, 7],),
        expected=1,
        note="Repeats of one value are a streak of length 1, not 4.",
    ),
    Case(
        name="heavy duplicates inside a streak",
        args=([1, 2, 2, 3, 3, 3, 4],),
        expected=4,
    ),
    Case(name="already sorted", args=(list(range(1, 11)),), expected=10),
    Case(name="reverse sorted", args=(list(range(10, 0, -1)),), expected=10),
    Case(
        name="every other value",
        args=([1, 3, 5, 7, 9],),
        expected=1,
        note="Gaps of 2 everywhere: no two values are consecutive.",
    ),
    Case(
        name="streak crosses zero",
        args=([1, -1, 0],),
        expected=3,
    ),
    Case(
        name="extreme values",
        args=([10**9, -(10**9), 10**9 - 1, -(10**9) + 1, 0],),
        expected=2,
        note="Values span two billion, so they cannot index an array.",
    ),
    Case(
        name="perf: one shuffled streak of 200k",
        args=(ONE_STREAK,),
        expected=ONE_STREAK_LEN,
        time_limit_ms=1500,
        memory_limit_mb=128,
        note="Budget rejects walking upward from every value (O(n^2) = 2e10 steps "
        "here). Sorting passes the harness but is not the O(n) target.",
    ),
    Case(
        name="perf: streak start repeated 100k times",
        args=(DUP_START,),
        expected=DUP_START_ANSWER,
        time_limit_ms=1500,
        memory_limit_mb=128,
        note="0 starts a 100k-long streak and appears 100_001 times. Starting a walk "
        "once per occurrence instead of once per distinct value is O(n^2) again.",
    ),
    Case(
        name="perf: 100k short streaks spread wide",
        args=(PAIRS,),
        expected=2,
        time_limit_ms=1500,
        memory_limit_mb=128,
        note="Many separate streaks. Each must be measured once and only once.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(longest_streak, CASES, title="L01.5 - Longest Unbroken Streak")
    )
