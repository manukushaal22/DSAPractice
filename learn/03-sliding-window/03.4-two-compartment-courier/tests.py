"""Test cases for L03.4. Run from repo root:  py run.py L3.4

You can also run this file directly:
    py learn/03-sliding-window/03.4-two-compartment-courier/tests.py
Feel free to read this file - the long streets are built so their answer is known by
construction, not computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import max_houses_served  # noqa: E402

BLOCK = 1000
HALF_BLOCKS = 250
PLANTED_PAIRS = 1500

# 250 blocks of 1000 houses, each block one restaurant, all codes different (near
# 10^9). Then 3000 houses alternating restaurants 7 and 11, then 250 more blocks.
# Two neighbouring blocks give 2000 houses. The planted stretch gives 3000, and it can't
# grow: the house on either side belongs to a third restaurant.
BLOCKS_WITH_PLANT = (
    [10**9 - i for i in range(HALF_BLOCKS) for _ in range(BLOCK)]
    + [7, 11] * PLANTED_PAIRS
    + [10**9 - HALF_BLOCKS - i for i in range(HALF_BLOCKS) for _ in range(BLOCK)]
)
BLOCKS_WITH_PLANT_ANSWER = 2 * PLANTED_PAIRS

# Restaurants 0/1 alternating for 250_000 houses, one order from restaurant 2, then 0/1
# alternating for 249_998 more. Restaurant 2 cuts the street in two. Around it, the
# best is [1, 2] or [2, 0], so the answer is the longer side.
SPLIT_LEFT = 125_000
ONE_INTRUDER = [0, 1] * SPLIT_LEFT + [2] + [0, 1] * (SPLIT_LEFT - 1)
ONE_INTRUDER_ANSWER = 2 * SPLIT_LEFT

# Every house a different restaurant, codes up to 999_998_000.
ALL_DIFFERENT = [i * 2000 for i in range(500_000)]

PERF_TIME_MS = 2000

CASES = [
    Case(name="example 1", args=([4, 8, 4, 2, 2, 4],), expected=4),
    Case(name="example 2", args=([5, 5, 5],), expected=3),
    Case(name="example 3", args=([1, 2, 3, 4, 5],), expected=2),
    Case(name="empty street", args=([],), expected=0),
    Case(name="single house", args=([42],), expected=1),
    Case(
        name="two restaurants the whole way",
        args=([3, 9, 9, 3, 9, 3],),
        expected=6,
    ),
    Case(
        name="strictly decreasing codes",
        args=([50, 40, 30, 20, 10],),
        expected=2,
    ),
    Case(
        name="latest run is longer than one house",
        args=([5, 6, 6, 7, 7, 6],),
        expected=5,
        note="When 7 arrives, the new block keeps both 6's: [6, 6, 7, 7, 6]. Restarting "
        "from just the previous house drops one of them and gives 4.",
    ),
    Case(
        name="drop the restaurant seen least recently",
        args=([1, 2, 1, 1, 3, 1, 1],),
        expected=5,
        note="When 3 arrives, 1 appeared first but 2 was seen least recently. Dropping "
        "2 gives [1, 1, 3, 1, 1].",
    ),
    Case(
        name="a restaurant fully leaves the block",
        args=([1, 2, 3, 2, 2],),
        expected=4,
        note="Once 1 leaves, it must stop counting as a restaurant in the block. A count "
        "left at zero still looks like a third restaurant.",
    ),
    Case(
        name="best block ends at the last house",
        args=([9, 8, 7, 7, 8, 7, 8],),
        expected=6,
        note="The best block is houses 1-6. It is only complete after the last house "
        "is added.",
    ),
    Case(
        name="codes 0 and 10^9 are ordinary restaurants",
        args=([0, 10**9, 0, 10**9, 999_999_999],),
        expected=4,
        note="0 is a real code, so it can't mean 'no restaurant yet'. Codes reach 10^9, "
        "so a list indexed by code won't fit.",
    ),
    Case(
        name="perf: one-restaurant blocks with a planted pair",
        args=(BLOCKS_WITH_PLANT,),
        expected=BLOCKS_WITH_PLANT_ANSWER,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
        note="Valid blocks are ~2000 long, so walking forward from every house is "
        "O(n * 2000) and gets cut off.",
    ),
    Case(
        name="perf: one intruder splits a two-restaurant street",
        args=(ONE_INTRUDER,),
        expected=ONE_INTRUDER_ANSWER,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
        note="Valid blocks are up to 250_000 long. Any per-start walk or per-step set "
        "rebuild is O(n^2) here.",
    ),
    Case(
        name="perf: every house a different restaurant",
        args=(ALL_DIFFERENT,),
        expected=2,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
        note="The counts must shrink as restaurants leave. Keeping one key per "
        "restaurant ever seen grows to 500_000 entries.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(max_houses_served, CASES, title="L03.4 - Two-Compartment Courier")
    )
