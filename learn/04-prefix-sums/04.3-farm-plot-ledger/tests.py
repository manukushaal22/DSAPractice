"""Test cases for L04.3. Run from repo root:  py run.py L4.3

You can also run this file directly:
    py learn/04-prefix-sums/04.3-farm-plot-ledger/tests.py
Feel free to read this file - the big ledger's answers come from a closed-form formula
for its values, not from a reference solution, so there is nothing to copy.
"""

import copy
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import plot_totals  # noqa: E402

LEDGER = [
    [3, -1, 4],
    [1, 5, -9],
    [2, 6, 5],
]

# 3 x 4 ledger used to probe the last row and the last column.
EDGE_LEDGER = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

UNTOUCHED = [[4, -2], [7, 1]]
UNTOUCHED_QUERIES = [(0, 0, 1, 1), (1, 0, 1, 1)]

# 500 x 500 ledger with plot (r, c) = 20 * (r - c), so values span -9980..9980.
# A block of h rows (r1..r2) and w columns (c1..c2) sums to
#     20 * (w * (r1 + ... + r2) - h * (c1 + ... + c2)),
# and each of those is an arithmetic series.
SIZE = 500
BIG = [[20 * (r - c) for c in range(SIZE)] for r in range(SIZE)]


def _block_total(r1: int, c1: int, r2: int, c2: int) -> int:
    h, w = r2 - r1 + 1, c2 - c1 + 1
    return 20 * (w * (r1 + r2) * h // 2 - h * (c1 + c2) * w // 2)


_rng = random.Random(43)
BIG_QUERIES = [
    (
        _rng.randrange(0, 50),
        _rng.randrange(0, 50),
        _rng.randrange(450, SIZE),
        _rng.randrange(450, SIZE),
    )
    for _ in range(200_000)
]
BIG_ANSWER = [_block_total(*q) for q in BIG_QUERIES]

PERF_TIME_MS = 2000

CASES = [
    Case(
        name="example 1",
        args=(LEDGER, [(0, 0, 2, 2), (1, 1, 2, 2), (0, 2, 1, 2)]),
        expected=[16, 7, -5],
    ),
    Case(
        name="example 2",
        args=(LEDGER, [(2, 0, 2, 0), (0, 1, 0, 1)]),
        expected=[2, -1],
    ),
    Case(
        name="example 3",
        args=(LEDGER, [(1, 0, 1, 2), (0, 1, 2, 1)]),
        expected=[-3, 10],
    ),
    Case(name="1 x 1 ledger", args=([[7]], [(0, 0, 0, 0)]), expected=[7]),
    Case(
        name="single row",
        args=([[1, 2, 3, 4, 5]], [(0, 0, 0, 4), (0, 1, 0, 3), (0, 4, 0, 4)]),
        expected=[15, 9, 5],
    ),
    Case(
        name="single column",
        args=([[1], [2], [3], [4]], [(0, 0, 3, 0), (1, 0, 2, 0)]),
        expected=[10, 5],
    ),
    Case(name="no queries", args=(LEDGER, []), expected=[]),
    Case(
        name="blocks touching the last row and column",
        args=(EDGE_LEDGER, [(2, 3, 2, 3), (1, 2, 2, 3), (0, 3, 2, 3), (2, 0, 2, 3)]),
        expected=[12, 38, 24, 42],
        note="Off-by-one probe: every query ends on row R-1 or column C-1, where a "
        "table without the extra zero row/column runs out of bounds.",
    ),
    Case(
        name="repeated identical queries",
        args=(LEDGER, [(0, 0, 1, 1)] * 3),
        expected=[8, 8, 8],
    ),
    Case(
        name="every plot a loss",
        args=([[-3, -1], [-4, -1]], [(0, 0, 1, 1), (0, 1, 1, 1), (1, 0, 1, 0)]),
        expected=[-9, -2, -4],
    ),
    Case(
        name="gains and losses cancel",
        args=([[1, -1, 1], [-1, 1, -1]], [(0, 0, 1, 1), (0, 0, 1, 2), (0, 0, 0, 2)]),
        expected=[0, 0, 1],
        note="A total of 0 is a real answer, not 'missing'.",
    ),
    Case(
        name="ledger is not modified",
        args=(UNTOUCHED, UNTOUCHED_QUERIES),
        expected=[10, 8],
        expected_args=(copy.deepcopy(UNTOUCHED), list(UNTOUCHED_QUERIES)),
        note="Building the running totals inside the ledger itself changes the "
        "caller's data.",
    ),
    Case(
        name="perf: 500 x 500 ledger, 200_000 large blocks",
        args=(BIG, BIG_QUERIES),
        expected=BIG_ANSWER,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=96,
        note="Each block covers 400+ rows. Summing each block is O(R*C) per query, and "
        "one prefix list per row is O(R) per query (~10^8 steps). Both get cut off.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(run_cases(plot_totals, CASES, title="L04.3 - Farm Plot Ledger"))
