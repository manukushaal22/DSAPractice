"""Test cases for P006. Run from repo root:  py run.py 6

You can also run this file directly:  py problems/p006-count-land-regions/tests.py
Feel free to read this file - the answers to the big cases are constructed, not
computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import count_regions  # noqa: E402

SIDE = 500  # 500 * 500 == 250_000 cells

# Every cell is land, so the whole grid is a single region. This is also the deepest
# possible flood fill: one region spanning 250_000 cells.
ALL_LAND = [[1] * SIDE for _ in range(SIDE)]
ALL_LAND_ANSWER = 1

# Checkerboard: land exactly where (row + col) is even. All four neighbours of such a
# cell have the opposite parity and are therefore water, so every land cell is its own
# region. On a 500x500 board exactly half the cells qualify: 125_000 regions.
CHECKERBOARD = [[1 if (r + c) % 2 == 0 else 0 for c in range(SIDE)] for r in range(SIDE)]
CHECKERBOARD_ANSWER = SIDE * SIDE // 2

# Serpentine corridor: every even row is solid land; every odd row has a single land
# cell, at the right edge when row % 4 == 1 and at the left edge when row % 4 == 3.
# Each of those single cells bridges the solid row above it to the solid row below, so
# the even rows are chained together into one long snake: 1 region.
SNAKE = [[0] * SIDE for _ in range(SIDE)]
for _r in range(SIDE):
    if _r % 2 == 0:
        SNAKE[_r] = [1] * SIDE
    elif _r % 4 == 1:
        SNAKE[_r][SIDE - 1] = 1
    else:
        SNAKE[_r][0] = 1
SNAKE_ANSWER = 1

EXAMPLE_1 = [
    [1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1],
]

CASES = [
    Case(name="example 1", args=(EXAMPLE_1,), expected=3),
    Case(
        name="example 2 - diagonals do not connect",
        args=([[1, 0], [0, 1]],),
        expected=2,
        note="Corner contact is not adjacency. Including the four diagonal neighbours "
        "merges these into 1.",
    ),
    Case(
        name="example 3 - ring around a hole",
        args=([[1, 1, 1], [1, 0, 1], [1, 1, 1]],),
        expected=1,
        note="The water cell in the middle does not split the ring.",
    ),
    Case(name="empty grid", args=([],), expected=0),
    Case(
        name="rows with no columns",
        args=([[], []],),
        expected=0,
        note="Two rows, zero columns. Anything that reads grid[0][0] to find the width "
        "raises here.",
    ),
    Case(name="single land cell", args=([[1]],), expected=1),
    Case(name="single water cell", args=([[0]],), expected=0),
    Case(
        name="single row",
        args=([[1, 0, 1, 0, 1]],),
        expected=3,
        note="One row, five columns. Swapping the row and column loops raises here.",
    ),
    Case(
        name="single column",
        args=([[1], [0], [1]],),
        expected=2,
        note="Three rows, one column - the transpose of the previous shape.",
    ),
    Case(name="all water", args=([[0, 0, 0], [0, 0, 0], [0, 0, 0]],), expected=0),
    Case(
        name="land at every corner and edge",
        args=([[1, 0, 1], [0, 0, 0], [1, 0, 1]],),
        expected=4,
        note="Four isolated corners. If a negative index wraps around a row, opposite "
        "corners appear adjacent and the count drops.",
    ),
    Case(
        name="grid must not be modified",
        args=(EXAMPLE_1,),
        expected=3,
        expected_args=(
            [
                [1, 1, 0, 0, 0],
                [1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 1, 1],
            ],
        ),
        note="Sinking visited land by writing 0 into the grid is the usual trick, and "
        "it is not allowed here - track visited cells separately.",
    ),
    Case(
        name="perf: 500x500 all land, one region",
        args=(ALL_LAND,),
        expected=ALL_LAND_ANSWER,
        time_limit_ms=4000,
        memory_limit_mb=256,
        note="A single region of 250_000 cells. Recursive flood fill dies with "
        "RecursionError long before the time budget matters.",
    ),
    Case(
        name="perf: 500x500 checkerboard, 125k regions",
        args=(CHECKERBOARD,),
        expected=CHECKERBOARD_ANSWER,
        time_limit_ms=4000,
        memory_limit_mb=256,
        note="Worst case for region count: 125_000 separate one-cell fills. Budget "
        "rejects anything that rescans the grid per region.",
    ),
    Case(
        name="perf: 500x500 serpentine corridor, one region",
        args=(SNAKE,),
        expected=SNAKE_ANSWER,
        time_limit_ms=4000,
        memory_limit_mb=256,
        note="One region of ~125_000 cells shaped as a single winding path, so the "
        "frontier stays deep no matter which order neighbours are explored in.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(run_cases(count_regions, CASES, title="P006 - Count Land Regions"))
