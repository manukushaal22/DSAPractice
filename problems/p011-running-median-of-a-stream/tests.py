"""Test cases for P011. Run from repo root:  py run.py 11

You can also run this file directly:  py problems/p011-running-median-of-a-stream/tests.py
Feel free to read this file - the answers to the big cases come from a closed form
that falls out of how the input is built, not from a reference solution.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import running_medians  # noqa: E402

TOL = 1e-9


def medians_match(actual, expected) -> bool:
    """Element-wise comparison with a tolerance, so 2 and 2.0 both pass."""
    try:
        if len(actual) != len(expected):
            return False
        return all(abs(a - b) <= TOL for a, b in zip(actual, expected))
    except TypeError:
        return False


M = 90_000

# Readings arrive alternately at the top and the bottom of the range seen so far:
# 1, -1, 2, -2, ..., M, -M. After an even count 2i the values are exactly
# {-i..-1} u {1..i}, so the two middle values are -1 and 1 and the median is 0.
# After an odd count 2i+1 the extra reading is +(i+1), the largest so far, which
# pushes the single middle value to 1. So the answer alternates 1.0, 0.0 forever.
# Every reading lands at an extreme, so a sorted list has to shift roughly half its
# contents on each insert.
SEESAW = [v for i in range(1, M + 1) for v in (i, -i)]
SEESAW_ANSWER = [1.0 if k % 2 else 0.0 for k in range(1, 2 * M + 1)]

# A strictly decreasing stream: N, N-1, ..., 1. After k readings the values seen are
# exactly {N-k+1, ..., N}, a contiguous block, whose median is the midpoint of its two
# ends: (N-k+1 + N) / 2. Every reading is the new minimum, so it belongs at the front.
N = 120_000
SLIDE = list(range(N, 0, -1))
SLIDE_ANSWER = [(2 * N - k + 1) / 2 for k in range(1, N + 1)]

CASES = [
    Case(
        name="example 1",
        args=([2, 1, 5, 7, 2, 0, 5],),
        expected=[2.0, 1.5, 2.0, 3.5, 2.0, 2.0, 2.0],
        expected_args=([2, 1, 5, 7, 2, 0, 5],),
        cmp=medians_match,
        note="Also checks the input list comes back unchanged and unreordered.",
    ),
    Case(
        name="example 2 - sorted stream",
        args=([1, 2, 3, 4],),
        expected=[1.0, 1.5, 2.0, 2.5],
        cmp=medians_match,
    ),
    Case(
        name="example 3 - average crosses zero",
        args=([5, -5],),
        expected=[5.0, 0.0],
        cmp=medians_match,
    ),
    Case(name="empty stream", args=([],), expected=[], cmp=medians_match),
    Case(
        name="single reading",
        args=([7],),
        expected=[7.0],
        cmp=medians_match,
        note="One value is its own median; the second half is still empty here.",
    ),
    Case(
        name="two readings, descending",
        args=([3, 1],),
        expected=[3.0, 2.0],
        cmp=medians_match,
        note="The second reading is smaller than the first, so it belongs on the "
        "other side of the boundary.",
    ),
    Case(
        name="even count needs a true average",
        args=([7, 8],),
        expected=[7.0, 7.5],
        cmp=medians_match,
        note="Integer division would report 7 here.",
    ),
    Case(
        name="all readings equal",
        args=([4, 4, 4, 4, 4],),
        expected=[4.0, 4.0, 4.0, 4.0, 4.0],
        cmp=medians_match,
        note="Ties must not break the low <= high split.",
    ),
    Case(
        name="duplicates straddling the median",
        args=([2, 2, 2, 1, 3],),
        expected=[2.0, 2.0, 2.0, 2.0, 2.0],
        cmp=medians_match,
    ),
    Case(
        name="ascending run",
        args=([1, 2, 3, 4, 5, 6],),
        expected=[1.0, 1.5, 2.0, 2.5, 3.0, 3.5],
        cmp=medians_match,
        note="Every reading goes to the high side, so the rebalance fires every step.",
    ),
    Case(
        name="descending run",
        args=([6, 5, 4, 3, 2, 1],),
        expected=[6.0, 5.5, 5.0, 4.5, 4.0, 3.5],
        cmp=medians_match,
        note="Mirror of the previous case; every reading goes to the low side.",
    ),
    Case(
        name="all negative",
        args=([-3, -1, -2, -10],),
        expected=[-3.0, -2.0, -2.0, -2.5],
        cmp=medians_match,
    ),
    Case(
        name="extreme magnitudes",
        args=([10**9, -(10**9), 10**9, -(10**9)],),
        expected=[1e9, 0.0, 1e9, 0.0],
        cmp=medians_match,
        note="Averaging the two middles must not overflow or lose precision.",
    ),
    Case(
        name="perf: 180k alternating extremes",
        args=(SEESAW,),
        expected=SEESAW_ANSWER,
        time_limit_ms=1500,
        memory_limit_mb=128,
        note="Answer alternates 1.0 / 0.0. Budget rejects anything quadratic: "
        "re-sorting each prefix, and also the sorted-list-with-insort approach, "
        "since every reading lands at one end and shifts half the list.",
    ),
    Case(
        name="perf: 120k strictly decreasing",
        args=(SLIDE,),
        expected=SLIDE_ANSWER,
        time_limit_ms=1500,
        memory_limit_mb=128,
        note="Each reading is the new minimum, so a sorted list inserts at index 0 "
        "every time - O(n^2) moves. The median slides by half a unit per reading, "
        "which also catches an off-by-one in which half owns the extra element.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(running_medians, CASES, title="P011 - Running Median of a Stream")
    )
