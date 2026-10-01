"""Test cases for P003. Run from repo root:  py run.py 3

You can also run this file directly:  py problems/p003-daily-temperatures/tests.py
Feel free to read this file - the answers to the big cases are constructed, not
computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import daily_temperatures  # noqa: E402

# 100_000 days that step down from 100 to -99 in flat runs of 500. The sequence is
# non-increasing, so no day is ever followed by a strictly warmer one: every answer
# is 0 by construction. This is also the worst case for stack depth - nothing is
# ever resolved, so every day accumulates.
NON_INCREASING = [100 - (i // 500) for i in range(100_000)]
NON_INCREASING_ANSWER = [0] * 100_000

# The block [10, 20, 30] repeated 33_333 times. Inside a block, 10 is beaten by the
# 20 next to it and 20 by the 30 next to it, so both wait 1. A 30 is the maximum of
# the whole list, and nothing after it is strictly warmer, so it waits 0 - including
# the very last one. The answer is therefore [1, 1, 0] repeated.
PERIODIC = [10, 20, 30] * 33_333
PERIODIC_ANSWER = [1, 1, 0] * 33_333

CASES = [
    Case(
        name="example 1",
        args=([73, 74, 75, 71, 69, 72, 76, 73],),
        expected=[1, 1, 4, 2, 1, 1, 0, 0],
    ),
    Case(name="example 2 - strictly increasing", args=([30, 40, 50, 60],), expected=[1, 1, 1, 0]),
    Case(
        name="example 3 - all equal",
        args=([55, 55, 55],),
        expected=[0, 0, 0],
        note="Equal is not warmer. A >= comparison resolves these and returns [1, 1, 0].",
    ),
    Case(name="empty input", args=([],), expected=[]),
    Case(name="single day", args=([42],), expected=[0]),
    Case(name="two days, warmer", args=([1, 2],), expected=[1, 0]),
    Case(name="two days, cooler", args=([2, 1],), expected=[0, 0]),
    Case(name="strictly decreasing", args=([5, 4, 3, 2, 1],), expected=[0, 0, 0, 0, 0]),
    Case(
        name="plateau then a rise",
        args=([70, 70, 70, 71],),
        expected=[3, 2, 1, 0],
        note="All three 70s are resolved by the same day. Ties must not cancel each "
        "other out on the way there.",
    ),
    Case(
        name="negative temperatures",
        args=([-5, -10, -3, -3, 0],),
        expected=[2, 1, 2, 1, 0],
        note="Day 1 (-10) is resolved before day 0 (-5), by the same day 2.",
    ),
    Case(
        name="hot day first, never beaten",
        args=([100, 1, 2, 3, 4],),
        expected=[0, 1, 1, 1, 0],
        note="Day 0 is the maximum, so it stays unresolved while everything after it "
        "is resolved quickly.",
    ),
    Case(
        name="one late spike resolves everything",
        args=([3, 3, 3, 3, 4],),
        expected=[4, 3, 2, 1, 0],
        note="A single day clears four pending days at once.",
    ),
    Case(
        name="input must not be mutated",
        args=([73, 74, 75, 71, 69, 72, 76, 73],),
        expected=[1, 1, 4, 2, 1, 1, 0, 0],
        expected_args=([73, 74, 75, 71, 69, 72, 76, 73],),
        note="The input list has to come back unchanged - build a separate result list.",
    ),
    Case(
        name="perf: 100k non-increasing",
        args=(NON_INCREASING,),
        expected=NON_INCREASING_ANSWER,
        time_limit_ms=1500,
        memory_limit_mb=96,
        note="Budget rejects O(n^2): nothing is ever resolved, so a forward scan per "
        "day walks the whole tail every time - about 5e9 comparisons.",
    ),
    Case(
        name="perf: 100k periodic blocks of [10, 20, 30]",
        args=(PERIODIC,),
        expected=PERIODIC_ANSWER,
        time_limit_ms=1500,
        memory_limit_mb=96,
        note="Budget rejects anything worse than amortised O(n). Every third day is a "
        "maximum that is never resolved, so a naive scan still degrades to O(n^2).",
    ),
]

if __name__ == "__main__":
    raise SystemExit(run_cases(daily_temperatures, CASES, title="P003 - Daily Temperatures"))
