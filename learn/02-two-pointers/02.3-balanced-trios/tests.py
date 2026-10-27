"""Test cases for L02.3. Run from repo root:  py run.py L2.3

You can also run this file directly:
    py learn/02-two-pointers/02.3-balanced-trios/tests.py
Feel free to read this file - the big cases are built so their answers are known by
construction, not computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import balanced_trios  # noqa: E402

import random  # noqa: E402


def same_trios(actual, expected) -> bool:
    """Any order of trios, any order within a trio, and no repeated trio."""
    if not isinstance(actual, list):
        return False
    try:
        normalised = [tuple(sorted(trio)) for trio in actual]
    except TypeError:
        return False
    if any(len(trio) != 3 for trio in normalised):
        return False
    if len(set(normalised)) != len(normalised):
        return False
    return sorted(normalised) == sorted(tuple(sorted(trio)) for trio in expected)


def _shuffled(items: list, seed: int) -> list:
    random.Random(seed).shuffle(items)
    return items


# ---------------------------------------------------------------- big inputs

# 2_000 distinct odd numbers spanning negatives and positives. A sum of three odd
# numbers is odd, so no trio can hit the even target 0: the answer is empty, yet every
# outer value has partners on both sides, so no early exit skips the work.
ODDS = _shuffled(list(range(-1999, 2000, 2)), seed=12)

# 2_000 values drawn from {0, 1, -2} only. The only value-trios summing to 0 are
# (0, 0, 0) and (-2, 1, 1), but each can be formed from ~10^8 position-trios.
FEW_VALUES = _shuffled([0] * 700 + [1] * 650 + [-2] * 650, seed=13)

PERF_TIME_MS = 3000

CASES = [
    Case(
        name="example 1",
        args=([-3, 1, 2, -1, 0, 1, 2], 0),
        expected=[[-3, 1, 2], [-1, 0, 1]],
        cmp=same_trios,
        note="Repeated values in the input must not produce repeated trios.",
    ),
    Case(
        name="example 2 - four zeros",
        args=([0, 0, 0, 0], 0),
        expected=[[0, 0, 0]],
        cmp=same_trios,
    ),
    Case(
        name="example 3 - nonzero target",
        args=([1, 2, 3, 4], 9),
        expected=[[2, 3, 4]],
        cmp=same_trios,
    ),
    Case(name="empty list", args=([], 0), expected=[], cmp=same_trios),
    Case(name="only two values", args=([1, -1], 0), expected=[], cmp=same_trios),
    Case(
        name="exactly three values that balance",
        args=([5, -2, -3], 0),
        expected=[[-3, -2, 5]],
        cmp=same_trios,
    ),
    Case(
        name="exactly three values that do not",
        args=([1, 1, 1], 0),
        expected=[],
        cmp=same_trios,
    ),
    Case(
        name="all equal, target is three of them",
        args=([2, 2, 2, 2, 2, 2], 6),
        expected=[[2, 2, 2]],
        cmp=same_trios,
    ),
    Case(
        name="value used twice within a trio",
        args=([-1, -1, -1, 2, 2], 0),
        expected=[[-1, -1, 2]],
        cmp=same_trios,
        note="(-1, -1, 2) uses -1 twice, which is allowed because -1 sits at several "
        "positions. Skipping duplicates too eagerly loses this trio.",
    ),
    Case(
        name="all negative, negative target",
        args=([-5, -4, -3, -2, -1], -9),
        expected=[[-5, -3, -1], [-4, -3, -2]],
        cmp=same_trios,
        note="An early exit of 'stop once nums[i] > target' fires immediately here "
        "(-5 > -9) and returns nothing. A correct bound has to account for all three "
        "values of the trio.",
    ),
    Case(
        name="positive first value, positive target",
        args=([1, 2, 3, 4], 6),
        expected=[[1, 2, 3]],
        cmp=same_trios,
        note="The smallest value is already positive. 'Stop once nums[i] > 0' returns "
        "nothing here: that exit is only valid for target 0.",
    ),
    Case(
        name="reverse sorted, several trios",
        args=([4, 3, 2, 1, 0, -1, -2], 3),
        expected=[[-2, 1, 4], [-2, 2, 3], [-1, 0, 4], [-1, 1, 3], [0, 1, 2]],
        cmp=same_trios,
    ),
    Case(
        name="extreme values",
        args=([10**9, -(10**9), 0, 10**9, -(10**9)], 0),
        expected=[[-(10**9), 0, 10**9]],
        cmp=same_trios,
    ),
    Case(
        name="perf: 2k distinct odd values, no trio possible",
        args=(ODDS, 0),
        expected=[],
        cmp=same_trios,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
        note="Budget rejects trying every trio (O(n^3) = 1.3e9 here), with or without a "
        "set to remove repeats afterwards.",
    ),
    Case(
        name="perf: 2k values from {0, 1, -2}",
        args=(FEW_VALUES, 0),
        expected=[[0, 0, 0], [-2, 1, 1]],
        cmp=same_trios,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
        note="Only two distinct trios, but about 1e8 position-trios produce them. "
        "Without skipping runs of equal values you list them repeatedly, or slowly.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(run_cases(balanced_trios, CASES, title="L02.3 - Balanced Trios"))
