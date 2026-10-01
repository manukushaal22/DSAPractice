"""Test cases for P015. Run from repo root:  py run.py 15

You can also run this file directly:
    py problems/p015-longest-route-in-a-network/tests.py

Feel free to read this file - the answers to the big cases follow from how the input
is built, not from a reference solution.
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import longest_route  # noqa: E402

EXAMPLE_1 = [[0, 1, 5], [1, 2, 3], [1, 3, 2]]


def _scramble(links, seed):
    """Shuffle the cables and flip endpoints, so neither the order of the list
    nor which endpoint comes first leaks the shape of the tree."""
    rng = random.Random(seed)
    out = []
    for a, b, w in links:
        out.append([b, a, w] if rng.getrandbits(1) else [a, b, w])
    rng.shuffle(out)
    return out


# --- Perf case A: a spider -------------------------------------------------------
# Station 0 is the hub. L legs hang off it, each a chain of M cables, and every cable
# on leg i costs i + 1. So the tip of leg i is M * (i + 1) away from the hub.
#
# Any route either stays inside one leg - at most M * (i + 1), which is no better than
# leaving the leg - or runs from one tip through the hub to another tip, costing
# M * (i + 1) + M * (j + 1) for two different legs. That is largest for the two
# priciest legs, so the answer is M * (L + (L - 1)), known by construction.
SPIDER_L = 150
SPIDER_M = 120
SPIDER_N = 1 + SPIDER_L * SPIDER_M

_spider = []
for _leg in range(SPIDER_L):
    _w = _leg + 1
    _first = 1 + _leg * SPIDER_M
    _spider.append([0, _first, _w])
    for _k in range(SPIDER_M - 1):
        _spider.append([_first + _k, _first + _k + 1, _w])

SPIDER_LINKS = _scramble(_spider, seed=3)
SPIDER_EXPECTED = SPIDER_M * (SPIDER_L + (SPIDER_L - 1))

# --- Perf case B: one long chain -------------------------------------------------
# Stations 0-1-2-...-(N-1) in a line, cable i costing (i % 7) + 1. In a chain the
# costliest route is the whole chain, so the answer is just the total, accumulated
# here straight from the construction.
CHAIN_N = 20_000
_chain = [[i, i + 1, (i % 7) + 1] for i in range(CHAIN_N - 1)]
CHAIN_LINKS = _scramble(_chain, seed=9)
CHAIN_EXPECTED = sum((i % 7) + 1 for i in range(CHAIN_N - 1))

CASES = [
    Case(
        name="example 1",
        args=(4, EXAMPLE_1),
        expected=8,
        expected_args=(4, EXAMPLE_1),
        note="Also checks the cable list comes back unchanged and unreordered, so "
        "build your own adjacency list rather than sorting or rewriting links.",
    ),
    Case(
        name="example 2 - cost, not hop count",
        args=(6, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 1], [1, 5, 10]]),
        expected=13,
        note="The route with the most cables costs only 4. Counting hops instead of "
        "summing weights reports 4.",
    ),
    Case(
        name="example 3 - answer avoids station 0",
        args=(5, [[0, 1, 1], [1, 2, 4], [1, 3, 4], [3, 4, 1]]),
        expected=9,
        note="Station 0 is a dead end on no costliest route. Measuring only from "
        "station 0 reports 6.",
    ),
    Case(
        name="single station",
        args=(1, []),
        expected=0,
        note="No cables and no pairs. The answer is 0, and nothing should be "
        "indexed out of an empty cable list.",
    ),
    Case(
        name="two stations",
        args=(2, [[0, 1, 7]]),
        expected=7,
        note="Smallest input with a real route: the one cable is the answer.",
    ),
    Case(
        name="all cables free",
        args=(3, [[0, 1, 0], [1, 2, 0]]),
        expected=0,
        note="A latency of 0 is a real answer, not 'no answer'. Distinguishes this "
        "from the single-station case only by how you got there.",
    ),
    Case(
        name="star around station 0",
        args=(4, [[0, 1, 1], [0, 2, 2], [0, 3, 3]]),
        expected=5,
        note="Every route crosses the hub, so the answer is the two priciest "
        "spokes. Taking only the single priciest spoke reports 3.",
    ),
    Case(
        name="chain of three",
        args=(3, [[0, 1, 2], [1, 2, 9]]),
        expected=11,
        note="A station with exactly one child on each side - the 'second best "
        "reach' must not be forced to exist.",
    ),
    Case(
        name="answer sits inside one branch",
        args=(6, [[0, 1, 1], [1, 2, 1], [0, 3, 1], [3, 4, 50], [3, 5, 50]]),
        expected=100,
        note="The costliest route is 4 -> 3 -> 5, which never reaches station 0. "
        "The best route that does pass through station 0 costs only 53, so a "
        "solution that only combines branches at the root reports that instead.",
    ),
    Case(
        name="equal weights throughout",
        args=(5, [[0, 1, 2], [1, 2, 2], [1, 3, 2], [3, 4, 2]]),
        expected=6,
        note="With uniform weights the answer is hop count times the weight; "
        "catches an off-by-one in how cables are counted.",
    ),
    Case(
        name="one heavy cable dominates",
        args=(5, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 9999]]),
        expected=10002,
        note="The whole chain, not just the heavy cable. Returning the single "
        "largest weight reports 9999.",
    ),
    Case(
        name="endpoints listed in reverse",
        args=(4, [[1, 0, 5], [2, 1, 3], [3, 1, 2]]),
        expected=8,
        note="Example 1 with every cable written b-then-a. The adjacency list must "
        "be built in both directions.",
    ),
    Case(
        name="balanced tree, deepest pair",
        args=(
            7,
            [[0, 1, 1], [0, 2, 1], [1, 3, 2], [1, 4, 2], [2, 5, 3], [2, 6, 3]],
        ),
        expected=7,
        note="Longest is 3 -> 1 -> 0 -> 2 -> 5, costing 2 + 1 + 1 + 3. The pair "
        "that looks deepest on one side, 5 -> 2 -> 6, costs only 6.",
    ),
    Case(
        name="deep chain, 800 stations",
        args=(800, _scramble([[i, i + 1, (i % 5) + 1] for i in range(799)], seed=4)),
        expected=sum((i % 5) + 1 for i in range(799)),
        note="Still inside Python's default recursion limit, so a recursive walk "
        "survives here. The perf chain below is 25x deeper and will not.",
    ),
    Case(
        name="perf: spider, 150 legs of 120 cables",
        args=(SPIDER_N, SPIDER_LINKS),
        expected=SPIDER_EXPECTED,
        time_limit_ms=2000,
        memory_limit_mb=192,
        note="Answer is M * (L + L-1) by construction - the two priciest legs end "
        "to end. The budget rejects O(n^2): a traversal from each of the 18001 "
        "stations is over 300 million steps. Only 120 deep, so recursion is safe "
        "here - this case isolates the complexity problem from the depth problem.",
    ),
    Case(
        name="perf: one chain of 20000 stations",
        args=(CHAIN_N, CHAIN_LINKS),
        expected=CHAIN_EXPECTED,
        time_limit_ms=2000,
        memory_limit_mb=192,
        note="In a chain the costliest route is the whole chain, so the answer is "
        "the total of all weights. Same O(n^2) rejection, plus the depth problem on "
        "its own: 20000 deep against a default recursion limit of 1000, so a "
        "recursive walk raises RecursionError rather than timing out.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(longest_route, CASES, title="P015 - Longest Route in a Network")
    )
