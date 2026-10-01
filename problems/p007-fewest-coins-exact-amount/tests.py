"""Test cases for P007. Run from repo root:  py run.py 7

You can also run this file directly:  py problems/p007-fewest-coins-exact-amount/tests.py
Feel free to read this file - the answers to the big cases are constructed, not
computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import min_coins  # noqa: E402

BIG_AMOUNT = 100_000

# With only a 1-unit coin the answer is forced: exactly BIG_AMOUNT coins. This is also
# the longest possible chain of dependent subproblems, which is what makes recursion
# (memoised or not) run out of stack here.
ONES_ANSWER = BIG_AMOUNT

# coins = [1, 6, 7], amount = 100_000.
# Lower bound: the largest coin is 7, so any solution needs at least
# ceil(100_000 / 7) = 14_286 coins.
# That bound is achievable: 14_284 sevens and 2 sixes give
# 99_988 + 12 = 100_000, using exactly 14_286 coins.
# So the answer is 14_286 by construction.
# Grabbing the largest coin first gives 14_285 sevens (99_995) plus 5 ones = 14_290,
# so this case also rejects a greedy strategy at scale.
GREEDY_TRAP_ANSWER = 14_286

# coins = [7, 14], amount = 100_000. Both denominations are multiples of 7, so every
# reachable total is a multiple of 7. 100_000 = 7 * 14_285 + 5, so it is unreachable
# and the answer is -1. Nothing short-circuits, so the whole table gets built.
UNREACHABLE_ANSWER = -1

CASES = [
    Case(
        name="example 1 - greedy is wrong",
        args=([1, 3, 4], 6),
        expected=2,
        note="3 + 3 beats the greedy 4 + 1 + 1. If this returns 3, the approach is "
        "taking the largest coin that fits and never reconsidering.",
    ),
    Case(name="example 2 - unreachable parity", args=([2], 3), expected=-1),
    Case(name="example 3 - canonical coin system", args=([1, 5, 10, 25], 63), expected=6),
    Case(
        name="amount is zero",
        args=([1, 2, 5], 0),
        expected=0,
        note="Zero coins make zero. This must not fall through to -1.",
    ),
    Case(name="single coin, exact match", args=([5], 5), expected=1),
    Case(
        name="only coin is larger than the amount",
        args=([10], 5),
        expected=-1,
        note="A denomination bigger than the target is unusable, not an error.",
    ),
    Case(name="a coin equals the amount", args=([1, 7, 10], 7), expected=1),
    Case(
        name="greedy trap, larger",
        args=([1, 7, 10], 14),
        expected=2,
        note="7 + 7 beats the greedy 10 + 1 + 1 + 1 + 1.",
    ),
    Case(
        name="duplicate denominations",
        args=([2, 2, 3], 5),
        expected=2,
        note="A repeated denomination adds nothing; it must not be double-counted.",
    ),
    Case(
        name="unsorted denominations",
        args=([5, 1, 3], 7),
        expected=3,
        expected_args=([5, 1, 3], 7),
        note="Order must not matter, and the input list must come back unsorted - "
        "sort a copy if you want one.",
    ),
    Case(
        name="no unit coin, largest unreachable total",
        args=([6, 9, 20], 43),
        expected=-1,
        note="43 is the largest amount not representable with 6, 9 and 20. Every "
        "amount above it is reachable, so an off-by-one in the table shows up here.",
    ),
    Case(name="exact division by the largest coin", args=([1, 2, 5], 100), expected=20),
    Case(
        name="perf: only a 1-unit coin, amount 100k",
        args=([1], BIG_AMOUNT),
        expected=ONES_ANSWER,
        time_limit_ms=2000,
        memory_limit_mb=64,
        note="100_000 nested subproblems. Recursion - even memoised - hits Python's "
        "recursion limit here; only a bottom-up table survives.",
    ),
    Case(
        name="perf: greedy trap at scale, amount 100k",
        args=([1, 6, 7], BIG_AMOUNT),
        expected=GREEDY_TRAP_ANSWER,
        time_limit_ms=2000,
        memory_limit_mb=64,
        note="Greedy returns 14_290 here instead of 14_286, and enumerating "
        "combinations is exponential. Budget rejects both.",
    ),
    Case(
        name="perf: unreachable at scale, amount 100k",
        args=([7, 14], BIG_AMOUNT),
        expected=UNREACHABLE_ANSWER,
        time_limit_ms=2000,
        memory_limit_mb=64,
        note="Worst case for the sentinel: most entries stay unreachable, and adding "
        "one coin to an unreachable remainder must not create a fake answer.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(min_coins, CASES, title="P007 - Fewest Coins for an Exact Amount")
    )
