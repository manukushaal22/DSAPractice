"""Test cases for L02.6. Run from repo root:  py run.py L2.6

You can also run this file directly:
    py learn/02-two-pointers/02.6-skyline-rainfall/tests.py
Feel free to read this file - the big skylines are built so their water is known by
construction, not computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import trapped_water  # noqa: E402

N = 1_000_000
H = 100_000

# Two full-height walls around empty lots: every lot fills to H.
BASIN = [H] + [0] * (N - 2) + [H]
BASIN_WATER = H * (N - 2)

# The block [10, 2, 7, 2] repeated, closed with a final 10. Every interior building has
# a 10 on both sides, so it holds 10 - height: 8 + 3 + 8 = 19 per block.
BLOCKS = N // 4
COMB = [10, 2, 7, 2] * BLOCKS + [10]
COMB_WATER = 19 * BLOCKS

# Non-increasing staircase from H down to 1, ten buildings per step: everything runs
# off the right end. Answer 0. A stack-based method keeps every building on its stack.
STAIRS_DOWN = [H - i // 10 for i in range(N)]

# A ramp up to a central peak, then a lake bounded by a lower right wall:
#   0, 1, ..., P - 1, P, 0 x M, W      with W < P.
# The ramp holds nothing (each building is taller than all before it). The lake fills
# to W. Answer: W * M. "Water level = min(first, last)" gets 0 here.
P, W = 100_000, 60_000
M = N - P - 2
RAMP_LAKE = list(range(P)) + [P] + [0] * M + [W]
RAMP_LAKE_WATER = W * M

PERF_TIME_MS = 3000
PERF_MEMORY_MB = 2

CASES = [
    Case(
        name="example 1",
        args=([5, 1, 3, 0, 4],),
        expected=8,
        expected_args=([5, 1, 3, 0, 4],),
        note="Also checks the input list comes back unchanged.",
    ),
    Case(name="example 2", args=([2, 0, 2],), expected=2),
    Case(name="example 3 - rise and fall", args=([1, 2, 3, 2, 1],), expected=0),
    Case(name="no buildings", args=([],), expected=0),
    Case(name="one building", args=([7],), expected=0),
    Case(name="two buildings", args=([3, 9],), expected=0),
    Case(name="flat", args=([4, 4, 4, 4],), expected=0),
    Case(name="strictly increasing", args=([0, 1, 2, 3, 4],), expected=0),
    Case(name="strictly decreasing", args=([4, 3, 2, 1, 0],), expected=0),
    Case(name="V shape", args=([3, 1, 0, 1, 3],), expected=7),
    Case(
        name="unequal walls",
        args=([5, 0, 0, 2],),
        expected=4,
        note="The lower wall (2) decides the level. Using the taller one gives 10.",
    ),
    Case(
        name="neighbours are not the walls",
        args=([3, 0, 1, 0, 3],),
        expected=8,
        note="The water above each lot is set by the tallest buildings on each side, "
        "not by its immediate neighbours. Neighbour-based answers give 2.",
    ),
    Case(
        name="interior bumps under one level",
        args=([5, 2, 1, 2, 1, 5],),
        expected=14,
    ),
    Case(
        name="several pools",
        args=([4, 1, 4, 0, 2, 0, 4, 2, 3],),
        expected=3 + 4 + 2 + 4 + 1,
        note="Pools at levels 4, 4 and 3. The last pool is bounded by the 4 and the "
        "closing 3.",
    ),
    Case(
        name="perf: 1M lots between two walls",
        args=(BASIN,),
        expected=BASIN_WATER,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=PERF_MEMORY_MB,
        note="Budget rejects scanning outward from every building (O(n^2)).",
    ),
    Case(
        name="perf: 1M buildings in a repeating comb",
        args=(COMB,),
        expected=COMB_WATER,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=PERF_MEMORY_MB,
        note="MLE means arrays of left/right maxima (O(n) extra). The target is O(1).",
    ),
    Case(
        name="perf: 1M buildings, non-increasing staircase",
        args=(STAIRS_DOWN,),
        expected=0,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=PERF_MEMORY_MB,
        note="No water at all. A stack-based method holds every building on its stack "
        "here (O(n) extra) and gets MLE.",
    ),
    Case(
        name="perf: 1M ramp, peak, and a lake",
        args=(RAMP_LAKE,),
        expected=RAMP_LAKE_WATER,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=PERF_MEMORY_MB,
        note="The tallest building is in the middle, not at an end. A single water "
        "level taken from the two ends of the row (min(0, 60_000) = 0) gets 0.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(run_cases(trapped_water, CASES, title="L02.6 - Skyline Rainfall"))
