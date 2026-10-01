"""Test cases for P005. Run from repo root:  py run.py 5

You can also run this file directly:  py problems/p005-merge-overlapping-intervals/tests.py
Feel free to read this file - the answers to the big cases are constructed, not
computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import merge_intervals  # noqa: E402

N = 100_000
BIG = 1_000_000_000


def same_intervals(actual, expected) -> bool:
    """Compare interval lists without caring whether the pairs are lists or tuples."""
    try:
        return [list(pair) for pair in actual] == [list(pair) for pair in expected]
    except TypeError:
        return False


def shuffled(items):
    """Deterministic permutation: 37 is coprime with 100_000, so i -> 37i mod N is
    a bijection. Used to make sure the input order is not already sorted."""
    return [items[(i * 37) % len(items)] for i in range(len(items))]


# 100_000 strictly nested intervals: [0, BIG] contains [1, BIG-1] contains [2, BIG-2]
# and so on. Every one of them lies inside the first, so the union is exactly one
# interval, [0, BIG], by construction. Presented shuffled so the input is unsorted.
NESTED = shuffled([[i, BIG - i] for i in range(N)])
NESTED_ANSWER = [[0, BIG]]

# 100_000 intervals of width 1, spaced 10_000 apart: [0,1], [10000,10001], ...
# Consecutive intervals are separated by a gap of ~10_000 points, so none of them
# touch and none merge. The answer is therefore the same set in sorted order.
DISJOINT_SORTED = [[10_000 * i, 10_000 * i + 1] for i in range(N)]
DISJOINT = shuffled(DISJOINT_SORTED)

CASES = [
    Case(
        name="example 1",
        args=([[1, 3], [2, 6], [8, 10], [15, 18]],),
        expected=[[1, 6], [8, 10], [15, 18]],
        cmp=same_intervals,
    ),
    Case(
        name="example 2 - touching at a point",
        args=([[1, 4], [4, 5]],),
        expected=[[1, 5]],
        cmp=same_intervals,
        note="Closed intervals sharing exactly one endpoint still overlap. A strict "
        "'<' comparison keeps them apart and returns two intervals.",
    ),
    Case(
        name="example 3 - unsorted input",
        args=([[5, 7], [1, 3], [2, 4]],),
        expected=[[1, 4], [5, 7]],
        cmp=same_intervals,
        expected_args=([[5, 7], [1, 3], [2, 4]],),
        note="The input must come back untouched - sort a copy, not the caller's list.",
    ),
    Case(name="empty input", args=([],), expected=[], cmp=same_intervals),
    Case(name="single interval", args=([[1, 5]],), expected=[[1, 5]], cmp=same_intervals),
    Case(
        name="degenerate point interval",
        args=([[3, 3]],),
        expected=[[3, 3]],
        cmp=same_intervals,
        note="start == end is legal: a single covered point.",
    ),
    Case(
        name="fully nested must not shrink the block",
        args=([[1, 10], [2, 3], [4, 5], [6, 20]],),
        expected=[[1, 20]],
        cmp=same_intervals,
        note="[2,3] sits inside [1,10]. Taking the incoming end instead of the larger "
        "of the two ends closes the block at 3 and splits the answer apart.",
    ),
    Case(
        name="identical duplicates",
        args=([[1, 4], [1, 4], [1, 4]],),
        expected=[[1, 4]],
        cmp=same_intervals,
    ),
    Case(
        name="adjacent but not touching",
        args=([[1, 2], [3, 4]],),
        expected=[[1, 2], [3, 4]],
        cmp=same_intervals,
        note="2 and 3 are distinct points, so these stay separate. A '<=' on the wrong "
        "side of the gap merges them.",
    ),
    Case(
        name="reverse sorted, all disjoint",
        args=([[5, 6], [3, 4], [1, 2]],),
        expected=[[1, 2], [3, 4], [5, 6]],
        cmp=same_intervals,
        note="Nothing merges, but the output still has to come back in start order.",
    ),
    Case(
        name="chain of touching intervals",
        args=([[1, 2], [2, 3], [3, 4], [4, 5]],),
        expected=[[1, 5]],
        cmp=same_intervals,
        note="Each link only touches its neighbour, but the whole chain collapses to one.",
    ),
    Case(
        name="one interval swallows a distant small one",
        args=([[500, 600], [0, BIG]],),
        expected=[[0, BIG]],
        cmp=same_intervals,
        note="Coordinates are large. Anything that walks covered points one at a time "
        "does a billion units of work here.",
    ),
    Case(
        name="mixed merges and gaps",
        args=([[9, 12], [1, 3], [20, 20], [2, 5], [13, 14]],),
        expected=[[1, 5], [9, 12], [13, 14], [20, 20]],
        cmp=same_intervals,
    ),
    Case(
        name="perf: 100k nested, collapses to one",
        args=(NESTED,),
        expected=NESTED_ANSWER,
        cmp=same_intervals,
        time_limit_ms=3000,
        memory_limit_mb=256,
        note="Budget rejects repeated merging passes over the whole list until nothing "
        "changes, and the 1e9 coordinate range rejects marking covered points.",
    ),
    Case(
        name="perf: 100k disjoint, nothing merges",
        args=(DISJOINT,),
        expected=DISJOINT_SORTED,
        cmp=same_intervals,
        time_limit_ms=3000,
        memory_limit_mb=256,
        note="Worst case for output size: the result is as long as the input. Budget "
        "rejects scanning the whole result list to look for an overlap.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(merge_intervals, CASES, title="P005 - Merge Overlapping Intervals")
    )
