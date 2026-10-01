"""Test cases for P004. Run from repo root:  py run.py 4

You can also run this file directly:  py problems/p004-minimum-processing-rate/tests.py
Feel free to read this file - the answers to the big cases are constructed, not
computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import min_processing_rate  # noqa: E402

BIG = 1_000_000_000

# 100_000 identical servers, each holding BIG GB.
# With h == n every server gets exactly one hour, so the rate must clear the whole
# server in a single hour: the answer is BIG. At BIG - 1 every server spills into a
# second hour and the total doubles to 2n.
UNIFORM = [BIG] * 100_000
UNIFORM_H_TIGHT = 100_000
UNIFORM_TIGHT_ANSWER = BIG

# Same fleet, twice the hours. Every server now gets exactly two hours, so the rate
# only has to halve each one: the answer is BIG // 2. One below that leaves a
# remainder, pushing every server to three hours and the total to 3n.
UNIFORM_H_DOUBLE = 200_000
UNIFORM_DOUBLE_ANSWER = BIG // 2

# 500 servers of 6 GB and 500 of 1 GB, with 1500 hours. The 1 GB servers cost one
# hour each at any rate, using 500 hours and leaving 1000 for the 6 GB ones - two
# hours apiece. Clearing 6 GB in two hours needs rate 3; at rate 2 it takes three
# hours and the total becomes 2000.
MIXED = [6] * 500 + [1] * 500
MIXED_H = 1500
MIXED_ANSWER = 3

CASES = [
    Case(name="example 1", args=([3, 6, 7, 11], 8), expected=4),
    Case(name="example 2 - h equals server count", args=([30, 11, 23, 4, 20], 5), expected=30),
    Case(
        name="example 3 - one hour of slack",
        args=([30, 11, 23, 4, 20], 6),
        expected=23,
        expected_args=([30, 11, 23, 4, 20], 6),
        note="The input list must come back unchanged - sorting it in place is not needed "
        "and is not allowed.",
    ),
    Case(name="minimum size input", args=([1], 1), expected=1),
    Case(name="single server, single hour", args=([7], 1), expected=7),
    Case(
        name="ceiling, not floor",
        args=([9], 2),
        expected=5,
        note="9 GB in 2 hours needs rate 5, not 4. Rate 4 leaves 1 GB over and takes a "
        "third hour. Truncating division gives 4.",
    ),
    Case(
        name="abundant time",
        args=([1, 1, 1], 1000),
        expected=1,
        note="The rate can never drop below 1, however much time is available.",
    ),
    Case(name="all equal, h equals server count", args=([5, 5, 5], 3), expected=5),
    Case(
        name="h is exactly twice the server count",
        args=([10, 10], 4),
        expected=5,
        note="Two hours per server, so each rate only has to halve a server.",
    ),
    Case(name="already sorted", args=([1, 2, 3, 4], 4), expected=4),
    Case(
        name="reverse sorted",
        args=([4, 3, 2, 1], 4),
        expected=4,
        note="Same multiset as the previous case - the order of the servers is irrelevant.",
    ),
    Case(
        name="tiny input, enormous answer",
        args=([BIG], 2),
        expected=BIG // 2,
        time_limit_ms=1000,
        memory_limit_mb=64,
        note="One server, but the answer is 500 million. Budget rejects walking the "
        "candidate rates upward from 1, even though n is 1.",
    ),
    Case(name="mixed sizes, 1000 servers", args=(MIXED, MIXED_H), expected=MIXED_ANSWER),
    Case(
        name="perf: 100k servers, h equals server count",
        args=(UNIFORM, UNIFORM_H_TIGHT),
        expected=UNIFORM_TIGHT_ANSWER,
        time_limit_ms=2500,
        memory_limit_mb=96,
        note="Budget rejects O(n * M). The answer sits at the very top of the search "
        "range, so a search that creeps upward never arrives.",
    ),
    Case(
        name="perf: 100k servers, double the hours",
        args=(UNIFORM, UNIFORM_H_DOUBLE),
        expected=UNIFORM_DOUBLE_ANSWER,
        time_limit_ms=2500,
        memory_limit_mb=96,
        note="Budget rejects O(n * M) and anything that rebuilds or copies the fleet "
        "per candidate rate. O(n log M) needs about 30 passes over the list.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(run_cases(min_processing_rate, CASES, title="P004 - Minimum Processing Rate"))
