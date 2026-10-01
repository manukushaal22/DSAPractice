"""Test cases for P009. Run from repo root:  py run.py 9

You can also run this file directly:  py problems/p009-largest-container/tests.py
Feel free to read this file - the answers to the big cases are constructed, not
computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import max_capacity  # noqa: E402

N = 100_000
BIG = 1_000_000_000

# 100_000 posts of identical height 1000. The shorter post is always 1000 whichever
# pair you pick, so capacity is decided purely by width and the answer is the widest
# pair: 1000 * (N - 1).
PLATEAU = [1000] * N
PLATEAU_ANSWER = 1000 * (N - 1)

# Heights 1, 2, 3, ..., N. For a pair (i, j) with i < j the shorter post is always
# heights[i] = i + 1, so capacity is (i + 1) * (j - i), which for a fixed i is largest
# at j = N - 1. That leaves (i + 1) * (N - 1 - i), a downward parabola maximised where
# i + 1 = N / 2 = 50_000, giving 50_000 * 50_000 = 2_500_000_000.
# The optimum is deep in the interior, so "just use the two ends" scores 100_000 here.
RAMP = list(range(1, N + 1))
RAMP_ANSWER = 50_000 * 50_000

# Two maximal posts at the ends with nothing but zero-height posts between them. Any
# pair involving a zero post holds nothing, so the only non-zero capacity is the pair
# of end posts: BIG * (N - 1).
TOWERS = [BIG] + [0] * (N - 2) + [BIG]
TOWERS_ANSWER = BIG * (N - 1)

CASES = [
    Case(
        name="example 1",
        args=([1, 8, 6, 2, 5, 4, 8, 3, 7],),
        expected=49,
        expected_args=([1, 8, 6, 2, 5, 4, 8, 3, 7],),
        note="Positions 1 and 8, heights 8 and 7, width 7. Also checks the input list "
        "comes back unchanged.",
    ),
    Case(name="example 2 - smallest real container", args=([1, 1],), expected=1),
    Case(
        name="example 3 - tall ends, sagging middle",
        args=([4, 3, 2, 1, 4],),
        expected=16,
        note="Posts between the chosen pair are irrelevant; only the two walls matter.",
    ),
    Case(name="empty input", args=([],), expected=0),
    Case(
        name="single post",
        args=([5],),
        expected=0,
        note="One post cannot form a container.",
    ),
    Case(name="all zero heights", args=([0, 0, 0],), expected=0),
    Case(
        name="strictly decreasing",
        args=([5, 4, 3, 2, 1],),
        expected=6,
        note="Best is positions 0-2 or 0-3, both giving 6. Neither end pair wins.",
    ),
    Case(
        name="strictly increasing",
        args=([1, 2, 3, 4, 5],),
        expected=6,
        note="Mirror image of the previous case, so the answer must match it.",
    ),
    Case(name="tall ends with a flat valley", args=([100, 1, 1, 1, 100],), expected=400),
    Case(
        name="isolated tall post is useless",
        args=([1, 100, 1],),
        expected=2,
        note="The tall middle post is capped by whichever short post it pairs with. "
        "The answer comes from the two 1s, width 2.",
    ),
    Case(name="uniform plateau", args=([3, 3, 3, 3],), expected=9),
    Case(
        name="maximum heights, minimum width",
        args=([BIG, BIG],),
        expected=BIG,
        note="Width 1, height 1e9. Capacities are large enough to need 64 bits.",
    ),
    Case(
        name="perf: 100k equal heights",
        args=(PLATEAU,),
        expected=PLATEAU_ANSWER,
        time_limit_ms=1500,
        memory_limit_mb=64,
        note="Every pair ties on height, so only width matters. Budget rejects the "
        "O(n^2) all-pairs scan.",
    ),
    Case(
        name="perf: 100k ascending ramp, interior optimum",
        args=(RAMP,),
        expected=RAMP_ANSWER,
        time_limit_ms=1500,
        memory_limit_mb=64,
        note="The best pair is at positions 49_999 and 99_999, nowhere near both ends. "
        "Simply measuring the two end posts returns 99_999 here, and moving the taller "
        "marker inward instead of the shorter one also fails.",
    ),
    Case(
        name="perf: 100k towers separated by a zero valley",
        args=(TOWERS,),
        expected=TOWERS_ANSWER,
        time_limit_ms=1500,
        memory_limit_mb=64,
        note="Answer is about 1e14, and it comes from the very first pair examined. "
        "Catches an off-by-one in the width, which is the gap between the two "
        "positions, not the number of posts between them.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(run_cases(max_capacity, CASES, title="P009 - Largest Container"))
