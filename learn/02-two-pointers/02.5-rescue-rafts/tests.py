"""Test cases for L02.5. Run from repo root:  py run.py L2.5

You can also run this file directly:
    py learn/02-two-pointers/02.5-rescue-rafts/tests.py
Feel free to read this file - the big cases are built so their optimum is provable
from a lower bound, not computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import min_rafts  # noqa: E402

import random  # noqa: E402


def _shuffled(items: list, seed: int) -> list:
    random.Random(seed).shuffle(items)
    return items


# ---------------------------------------------------------------- big inputs
#
# Every raft holds at most two people, so ceil(n / 2) is always a lower bound. Each
# case below either meets that bound with an explicit pairing, or adds people who are
# provably forced to ride alone.

LIMIT = 30_000
N = 500_000

# 250_000 complementary pairs (w, LIMIT - w): a perfect pairing exists, so the answer is
# exactly N / 2. Pairing the lightest people together first does far worse here.
PAIRS = _shuffled(
    [v for i in range(N // 2) for v in (1 + i % 14_999, LIMIT - 1 - i % 14_999)], seed=51
)
PAIRS_ANSWER = N // 2

# 200_000 people weighing exactly LIMIT (nobody can join them: everyone weighs >= 1)
# plus 300_000 people weighing at most LIMIT / 2 (any two of them fit together).
# Answer: 200_000 + 150_000.
HEAVY, LIGHT = 200_000, 300_000
FORCED = _shuffled([LIMIT] * HEAVY + [1 + i % (LIMIT // 2) for i in range(LIGHT)], seed=52)
FORCED_ANSWER = HEAVY + LIGHT // 2

# Everyone weighs just over half the limit, so no two people fit together.
NO_PAIRS = [LIMIT // 2 + 1] * N

PERF_TIME_MS = 2000

CASES = [
    Case(name="example 1", args=([3, 2, 2, 1], 3), expected=3),
    Case(
        name="example 2 - lightest-with-lightest is wrong",
        args=([1, 1, 4, 4], 5),
        expected=2,
        note="Pairing the two lightest people first leaves both 4s alone (3 rafts).",
    ),
    Case(
        name="example 3 - exactly at the limit",
        args=([5, 5, 5, 5], 10),
        expected=2,
        note="A pair weighing exactly the limit is allowed: the test is <=, not <.",
    ),
    Case(name="nobody to rescue", args=([], 10), expected=0),
    Case(name="one person", args=([7], 7), expected=1),
    Case(
        name="last person in the middle",
        args=([3, 2, 3], 5),
        expected=2,
        note="After (2, 3) leaves, both pointers sit on the remaining 3. A loop that "
        "stops when the pointers meet forgets them.",
    ),
    Case(name="odd count, all pairable", args=([1, 1, 1], 2), expected=2),
    Case(name="all equal, just over half", args=([6, 6, 6], 10), expected=3),
    Case(
        name="heaviest must go alone",
        args=([2, 3, 8, 9], 10),
        expected=3,
        note="9 cannot share with the lightest (2), so it cannot share with anyone. "
        "Then (8, 2) and 3 alone, or (3, 2) and 8 alone.",
    ),
    Case(
        name="adjacent pairing after sorting is wrong",
        args=([1, 2, 3, 4], 5),
        expected=2,
        note="Sorted neighbours (1, 2) and (3, 4) do not both fit (3 + 4 = 7). "
        "(1, 4) and (2, 3) do.",
    ),
    Case(name="already sorted", args=([1, 2, 3, 4, 5, 6], 7), expected=3),
    Case(name="reverse sorted", args=([6, 5, 4, 3, 2, 1], 7), expected=3),
    Case(
        name="everyone at the limit",
        args=([10, 10, 10], 10),
        expected=3,
    ),
    Case(
        name="perf: 500k people in complementary pairs",
        args=(PAIRS, LIMIT),
        expected=PAIRS_ANSWER,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
        note="A perfect pairing exists. Budget rejects searching for or removing a "
        "partner per person (O(n^2)).",
    ),
    Case(
        name="perf: 200k forced loners, 300k light people",
        args=(FORCED, LIMIT),
        expected=FORCED_ANSWER,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
        note="People at exactly the limit must ride alone; the light ones pair freely.",
    ),
    Case(
        name="perf: 500k people, no two fit together",
        args=(NO_PAIRS, LIMIT),
        expected=N,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
        note="Every raft carries one person. A loop that moves both pointers on a "
        "failed pairing finishes too early.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(run_cases(min_rafts, CASES, title="L02.5 - Rescue Rafts"))
