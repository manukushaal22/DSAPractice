"""Test cases for P001. Run from repo root:  py run.py 1

You can also run this file directly:  py problems/p001-.../tests.py
Feel free to read this file - but the answers to the big cases are constructed,
not computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import max_profit  # noqa: E402

# 100_000 values of (i * 37) % 1001. 37 is coprime with 1001, so every value in
# 0..1000 appears inside each 1001-long cycle. A 0 shows up in the first cycle and
# a 1000 shows up in a later cycle, so the best transaction is exactly 1000.
SAWTOOTH = [(i * 37) % 1001 for i in range(100_000)]

# Strictly decreasing: no profitable transaction exists at all.
DESCENDING = list(range(50_000, 0, -1))

CASES = [
    Case(name="example 1", args=([7, 1, 5, 3, 6, 4],), expected=5),
    Case(name="example 2 - only falls", args=([7, 6, 4, 3, 1],), expected=0),
    Case(name="example 3 - dip too late", args=([2, 4, 1],), expected=2),
    Case(name="single day", args=([1],), expected=0),
    Case(name="two days, up", args=([1, 2],), expected=1),
    Case(name="two days, down", args=([2, 1],), expected=0),
    Case(name="flat prices", args=([5, 5, 5, 5],), expected=0),
    Case(name="zeros allowed", args=([0, 0],), expected=0),
    Case(name="peak comes early", args=([1, 7, 2, 3],), expected=6),
    Case(name="dip then recovery", args=([3, 3, 5, 0, 0, 3, 1, 4],), expected=4),
    Case(name="repeated dips", args=([2, 1, 2, 1, 0, 1, 2],), expected=2),
    Case(
        name="min just before the end",
        args=([9, 8, 7, 6, 5, 4, 10],),
        expected=6,
        note="The cheapest day is day 5; the only sell day after it is day 6.",
    ),
    Case(
        name="perf: 50k strictly decreasing",
        args=(DESCENDING,),
        expected=0,
        time_limit_ms=1000,
        memory_limit_mb=64,
        note="An O(n^2) solution will blow the 1s budget here.",
    ),
    Case(
        name="perf: 100k sawtooth",
        args=(SAWTOOTH,),
        expected=1000,
        time_limit_ms=1000,
        memory_limit_mb=64,
        note="O(n) needs ~10 ms here. O(n^2) needs ~50 s.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(run_cases(max_profit, CASES, title="P001 - Best Time to Buy and Sell Stock"))
