"""Test cases for L01.4. Run from repo root:  py run.py L1.4

You can also run this file directly:
    py learn/01-arrays-and-hashing/01.4-on-call-shortlist/tests.py
Feel free to read this file - the big cases are built so their answers are known by
construction, not computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import shortlist  # noqa: E402

import random  # noqa: E402


def same_codes(actual, expected) -> bool:
    """Any order; exactly the expected codes, each once."""
    if not isinstance(actual, list) or len(actual) != len(expected):
        return False
    try:
        return sorted(actual) == sorted(expected)
    except TypeError:
        return False


def _shuffled(items: list, seed: int) -> list:
    random.Random(seed).shuffle(items)
    return items


# ---------------------------------------------------------------- big inputs

# Staircase: code (7*i - 2000) appears exactly i times, for i = 1..632 (~200k entries).
# The 300 busiest are i = 333..632, and i = 332 is strictly below them.
STAIR_N = 632
STAIR_K = 300
STAIRCASE = _shuffled(
    [7 * i - 2000 for i in range(1, STAIR_N + 1) for _ in range(i)], seed=4
)
STAIR_ANSWER = [7 * i - 2000 for i in range(STAIR_N - STAIR_K + 1, STAIR_N + 1)]

# 50_000 distinct codes spread across [-1e9, 1e9). Even-indexed codes appear 3 times,
# odd-indexed codes once: n = 100_000, k = 25_000, and the cut is 3 vs 1.
SPREAD = [-(10**9) + 39_997 * i for i in range(50_000)]
TWO_TIER_ANSWER = SPREAD[0::2]
TWO_TIER = _shuffled([c for c in TWO_TIER_ANSWER for _ in range(3)] + SPREAD[1::2], seed=7)

# 100_000 distinct codes, each exactly once, k = all of them. No (k+1)-th code exists,
# so the shortlist is the whole set.
ALL_DISTINCT = _shuffled([-(10**9) + 19_997 * i for i in range(100_000)], seed=11)
ALL_DISTINCT_ANSWER = list(ALL_DISTINCT)

CASES = [
    Case(
        name="example 1",
        args=([404, 500, 404, 503, 500, 404], 2),
        expected=[404, 500],
        cmp=same_codes,
        expected_args=([404, 500, 404, 503, 500, 404], 2),
        note="Also checks the input list comes back unchanged.",
    ),
    Case(name="example 2 - single incident", args=([7], 1), expected=[7], cmp=same_codes),
    Case(
        name="example 3 - tie inside the shortlist",
        args=([-1, -1, 0, 2, 2, 2, 0, -1, 9], 2),
        expected=[-1, 2],
        cmp=same_codes,
    ),
    Case(
        name="one code accounts for every incident",
        args=([42] * 1000, 1),
        expected=[42],
        cmp=same_codes,
        note="The count equals n here. If you index anything by count, it needs room "
        "for n itself, not just n - 1.",
    ),
    Case(
        name="all codes tie, k takes them all",
        args=([5, 6, 7, 5, 6, 7], 3),
        expected=[5, 6, 7],
        cmp=same_codes,
    ),
    Case(
        name="already sorted by value",
        args=([1, 1, 1, 2, 2, 3], 2),
        expected=[1, 2],
        cmp=same_codes,
    ),
    Case(
        name="reverse sorted by value",
        args=([3, 2, 2, 1, 1, 1], 1),
        expected=[1],
        cmp=same_codes,
    ),
    Case(
        name="codes look like counts",
        args=([3, 3, 1, 1, 1, 2], 2),
        expected=[1, 3],
        cmp=same_codes,
        note="Code 1 has 3 incidents, code 3 has 2, code 2 has 1. Returning counts "
        "instead of codes, or mixing the two up, gives a plausible-looking wrong answer.",
    ),
    Case(
        name="extreme code values",
        args=([10**9, -(10**9), 10**9, 0], 1),
        expected=[10**9],
        cmp=same_codes,
        note="Codes span two billion values, so they cannot be used as list positions.",
    ),
    Case(
        name="cut falls between adjacent counts",
        args=([0, 0, 0, 1, 1, 2, 2, 2, 2], 2),
        expected=[2, 0],
        cmp=same_codes,
        note="Counts are 4, 3 and 2. The shortlist stops between 3 and 2.",
    ),
    Case(
        name="staircase: code i appears i times, 632 codes",
        args=(STAIRCASE, STAIR_K),
        expected=STAIR_ANSWER,
        cmp=same_codes,
        time_limit_ms=2000,
        memory_limit_mb=128,
    ),
    Case(
        name="perf: 50k codes in two tiers, k = 25k",
        args=(TWO_TIER, len(TWO_TIER_ANSWER)),
        expected=TWO_TIER_ANSWER,
        cmp=same_codes,
        time_limit_ms=1500,
        memory_limit_mb=128,
        note="Budget rejects selecting the busiest remaining code k times (O(d k) = "
        "1.25e9 here). Sorting or a heap passes the harness but is not the target.",
    ),
    Case(
        name="perf: 100k distinct codes, k = all of them",
        args=(ALL_DISTINCT, len(ALL_DISTINCT)),
        expected=ALL_DISTINCT_ANSWER,
        cmp=same_codes,
        time_limit_ms=1500,
        memory_limit_mb=128,
        note="Every count is 1 and k = d = n. Repeated max-selection is O(n^2) = 1e10. "
        "Also catches answers that drop or duplicate codes on a total tie.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(run_cases(shortlist, CASES, title="L01.4 - On-Call Shortlist"))
