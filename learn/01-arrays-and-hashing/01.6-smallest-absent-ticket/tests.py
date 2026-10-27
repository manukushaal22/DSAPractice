"""Test cases for L01.6. Run from repo root:  py run.py L1.6

You can also run this file directly:
    py learn/01-arrays-and-hashing/01.6-smallest-absent-ticket/tests.py
Feel free to read this file - the big cases are built so their answers are known by
construction, not computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import smallest_absent  # noqa: E402

import random  # noqa: E402

INT_MIN, INT_MAX = -(2**31), 2**31 - 1


def _shuffled(items: list, seed: int) -> list:
    random.Random(seed).shuffle(items)
    return items


# ---------------------------------------------------------------- big inputs

N = 1_000_000

# Every ticket 1..N exactly once, shuffled. Nothing is free below N + 1.
FULL = _shuffled(list(range(1, N + 1)), seed=21)

# 1..N with ticket 777_777 removed. Its slot holds a duplicate of 1, and 1% of the other
# slots hold junk (non-positive or too large) in place of tickets that are then also
# missing, but only above 777_777. Answer: 777_777.
GAP = 777_777
_tickets = [v for v in range(1, N + 1) if v != GAP]
_rng = random.Random(33)
for _i in range(len(_tickets)):
    if _tickets[_i] > GAP and _rng.random() < 0.01:
        _tickets[_i] = _rng.choice((0, -_tickets[_i], INT_MIN, INT_MAX, N + _tickets[_i]))
MESSY = _shuffled(_tickets + [1], seed=34)

# Big-case budgets. The time limit rejects O(n^2) (e.g. `in` on the list per candidate).
# Memory is NOT a fair O(1)-space check in Python: writing a negated value allocates a
# new int object, so a correct sign-marking solution peaks around 30 MB here, the same
# as a set. The budget only stops runaways; extra space is checked in review.
PERF_TIME_MS = 4000
PERF_MEMORY_MB = 96

CASES = [
    Case(name="example 1", args=([3, 4, -1, 1],), expected=2),
    Case(name="example 2", args=([1, 2, 0],), expected=3),
    Case(name="example 3 - nothing small present", args=([7, 8, 9, 11, 12],), expected=1),
    Case(name="empty list", args=([],), expected=1),
    Case(name="just a 1", args=([1],), expected=2),
    Case(name="just a 2", args=([2],), expected=1),
    Case(
        name="the same ticket four times",
        args=([1, 1, 1, 1],),
        expected=2,
        time_limit_ms=1000,
        note="If you swap values into their home position, a duplicate whose home "
        "already holds the same value must not be swapped again. That swap changes "
        "nothing and loops forever.",
    ),
    Case(
        name="every ticket doubled",
        args=([3, 1, 2, 3, 2, 1],),
        expected=4,
        time_limit_ms=1000,
        note="n = 6, but only 1..3 are present. Duplicates take up slots without "
        "pushing the answer higher.",
    ),
    Case(name="already sorted", args=(list(range(1, 11)),), expected=11),
    Case(name="reverse sorted", args=(list(range(10, 0, -1)),), expected=11),
    Case(name="only junk", args=([-5, 0, -1, 0],), expected=1),
    Case(
        name="values beyond n are irrelevant",
        args=([1, 1000, 2, 999],),
        expected=3,
    ),
    Case(
        name="32-bit extremes",
        args=([INT_MAX, INT_MIN, 1, INT_MIN],),
        expected=2,
        note="Junk at both ends of the 32-bit range. Using a value as a position "
        "without checking its range raises IndexError (or, with negatives, silently "
        "indexes from the end of the list).",
    ),
    Case(
        name="perf: all of 1..1M, shuffled",
        args=(FULL,),
        expected=N + 1,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=PERF_MEMORY_MB,
        note="Budget rejects anything quadratic, such as `in` on the list for each "
        "candidate (~1e12 steps here). It cannot check O(1) extra space, so the "
        "review does.",
    ),
    Case(
        name="perf: 1M with one gap, duplicates and junk",
        args=(MESSY,),
        expected=GAP,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=PERF_MEMORY_MB,
        note="Ticket 777_777 is missing, 1 appears twice, and junk is scattered above "
        "the gap. A swap loop without a duplicate check never terminates here.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(smallest_absent, CASES, title="L01.6 - Smallest Absent Ticket")
    )
