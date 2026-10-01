"""Test cases for P008. Run from repo root:  py run.py 8

You can also run this file directly:  py problems/p008-subarrays-with-given-sum/tests.py
Feel free to read this file - the answers to the big cases are constructed, not
computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import count_subarrays  # noqa: E402

N = 100_000

# 100_000 zeros with k = 0. Every one of the n*(n+1)/2 subarrays sums to zero, so the
# answer is 100_000 * 100_001 / 2 = 5_000_050_000 by construction. Also the worst case
# for the answer's magnitude.
ZEROS = [0] * N
ZEROS_ANSWER = N * (N + 1) // 2

# [1, -1] repeated 50_000 times, k = 0. The running totals go 0,1,0,1,...,0 - so of the
# 100_001 prefix positions, the 50_001 even ones all hold 0 and the 50_000 odd ones all
# hold 1. Every pair of positions sharing a value is one zero-sum subarray, giving
# C(50_001, 2) + C(50_000, 2) = 1_250_025_000 + 1_249_975_000 = 2_500_000_000.
ALTERNATING = [1, -1] * (N // 2)
ALTERNATING_ANSWER = (50_001 * 50_000) // 2 + (50_000 * 49_999) // 2

# 100_000 ones with k = 1. The running totals are 0,1,2,...,100_000 - all distinct, so
# the map holds 100_001 separate keys and only the single-element subarrays match.
# The answer is exactly N.
ONES = [1] * N
ONES_ANSWER = N

CASES = [
    Case(
        name="example 1 - overlapping duplicates",
        args=([1, 1, 1], 2),
        expected=2,
        note="Positions 0-1 and 1-2 are two different subarrays even though they look "
        "the same and overlap.",
    ),
    Case(name="example 2", args=([1, 2, 3], 3), expected=2),
    Case(
        name="example 3 - negatives present",
        args=([1, -1, 0], 0),
        expected=3,
        expected_args=([1, -1, 0], 0),
        note="[1,-1], [1,-1,0] and [0]. Also checks the input list comes back unchanged.",
    ),
    Case(name="empty list", args=([], 5), expected=0),
    Case(name="single element matches", args=([5], 5), expected=1),
    Case(name="single element does not match", args=([5], 3), expected=0),
    Case(
        name="target unreachable",
        args=([1, 2, 3], 0),
        expected=0,
        note="No subarray sums to 0 here, so this must return 0. Recording the current "
        "running total before reading the map makes every position match itself and "
        "returns 3.",
    ),
    Case(
        name="all zeros, small",
        args=([0, 0, 0], 0),
        expected=6,
        note="All 6 subarrays qualify. Reading the map after recording the current "
        "running total counts the empty subarray too and returns 9.",
    ),
    Case(name="negative target", args=([-1, -1, 1], -2), expected=1),
    Case(
        name="whole array, starting at index 0",
        args=([1, 2, 3], 6),
        expected=1,
        note="The only match starts at index 0. Without seeding the map with a zero "
        "running total, nothing establishes that baseline and this returns 0.",
    ),
    Case(
        name="repeatedly cancelling pairs",
        args=([1, -1, 1, -1], 0),
        expected=4,
        note="Four zero-sum subarrays: two short, one of length 4, one spanning the "
        "middle. A window cannot find these.",
    ),
    Case(name="all identical negatives", args=([-2, -2, -2], -4), expected=2),
    Case(
        name="perf: 100k zeros, every subarray matches",
        args=(ZEROS, 0),
        expected=ZEROS_ANSWER,
        time_limit_ms=1500,
        memory_limit_mb=64,
        note="Five billion matching subarrays. Anything that enumerates them rather "
        "than counting them arithmetically cannot finish.",
    ),
    Case(
        name="perf: 100k alternating +1/-1",
        args=(ALTERNATING, 0),
        expected=ALTERNATING_ANSWER,
        time_limit_ms=1500,
        memory_limit_mb=64,
        note="Negatives throughout, so a sliding window is invalid regardless of speed. "
        "Budget rejects the O(n^2) start-index scan.",
    ),
    Case(
        name="perf: 100k ones, 100k distinct running totals",
        args=(ONES, 1),
        expected=ONES_ANSWER,
        time_limit_ms=1500,
        memory_limit_mb=64,
        note="Every running total is distinct, so the map grows to 100_001 keys - the "
        "worst case for its memory rather than for the answer.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(count_subarrays, CASES, title="P008 - Subarrays With a Given Sum")
    )
