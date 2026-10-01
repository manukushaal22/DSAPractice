"""Test cases for P012. Run from repo root:  py run.py 12

You can also run this file directly:
    py problems/p012-earliest-full-connection/tests.py

Feel free to read this file - the answers to the big cases follow from how the input
is built, not from a reference solution.
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import earliest_full_connection  # noqa: E402

EXAMPLE_1 = [[20, 1, 2], [5, 0, 1], [70, 2, 3], [30, 4, 5], [65, 3, 4], [10, 0, 2]]

P = 20_000
H = P // 2
NOISE = 3 * H


def _big_case(join: bool, seed: int) -> list:
    """Two long paths, written down with opposite orientation, plus no-op entries.

    Path A covers members 0..H-1 and is written "old, new": link i is
    ``[i + 1, i, i + 1]``.
    Path B covers members H..P-1 and is written "new, old": link j is
    ``[j - H + 1, j + 1, j]``.

    Both paths carry timestamps 1..H-1 and are therefore built in parallel, in
    timestamp order, so every link attaches a fresh singleton to the group grown so
    far - the worst case for a disjoint-set forest that does not balance its links.
    Writing the two paths in opposite order means that whichever of the two roots such
    an implementation keeps, one of the paths degenerates into a structure of depth ~H.

    The no-op entries are what then pay for that depth. A third repeat the pair (0, 1)
    and a third repeat the pair (H, H+1) - the first link of each path, at each path's
    smallest timestamp, so these repeats are always redundant by the time they are
    read - and a third name one member twice. None of them can drop the group count.

    With ``join``, the two paths are finally tied together at timestamp P, which is
    larger than every other timestamp here, so the answer is P. Without it the members
    stay in exactly two groups forever and the answer is -1.
    """
    rng = random.Random(seed)
    logs = [[i + 1, i, i + 1] for i in range(H - 1)]
    logs.extend([j - H + 1, j + 1, j] for j in range(H, P - 1))
    for k in range(NOISE):
        if k % 3 == 0:
            logs.append([rng.randrange(1, P), 0, 1])
        elif k % 3 == 1:
            logs.append([rng.randrange(1, P), H, H + 1])
        else:
            member = rng.randrange(P)
            logs.append([rng.randrange(1, P), member, member])
    if join:
        logs.append([P, 0, P - 1])
    rng.shuffle(logs)
    return logs


CONNECTS = _big_case(join=True, seed=7)
NEVER = _big_case(join=False, seed=13)

CASES = [
    Case(
        name="example 1",
        args=(6, EXAMPLE_1),
        expected=70,
        expected_args=(6, EXAMPLE_1),
        note="Also checks the input list comes back unchanged and unreordered, so "
        "sort a copy rather than sorting in place.",
    ),
    Case(
        name="example 2 - two halves meet",
        args=(4, [[0, 2, 0], [1, 3, 1], [2, 1, 2]]),
        expected=2,
    ),
    Case(
        name="example 3 - never connects",
        args=(4, [[9, 0, 1], [3, 2, 3], [100, 0, 1]]),
        expected=-1,
        note="The entry at 100 repeats an introduction that already happened.",
    ),
    Case(
        name="no entries at all",
        args=(2, []),
        expected=-1,
        note="Two members, nothing ever merges them.",
    ),
    Case(
        name="smallest input that connects",
        args=(2, [[42, 0, 1]]),
        expected=42,
        note="One entry finishes the job; the counter goes straight from 2 to 1.",
    ),
    Case(
        name="answer is timestamp 0",
        args=(2, [[0, 0, 1]]),
        expected=0,
        note="0 is a real answer, not 'no answer'. A falsy-zero check or an "
        "`ans or -1` reports -1 here.",
    ),
    Case(
        name="entries in reverse time order",
        args=(4, [[30, 2, 3], [20, 1, 2], [10, 0, 1]]),
        expected=30,
        note="The completing entry is first in the list. Reading the list as given "
        "reports 30 for the wrong reason - and 10 if you trust arrival order.",
    ),
    Case(
        name="repeated introductions",
        args=(3, [[1, 0, 1], [2, 0, 1], [3, 1, 0], [4, 1, 2]]),
        expected=4,
        note="Entries at 2 and 3 name a pair already in one group, in both orders; "
        "neither may decrement the group count.",
    ),
    Case(
        name="member introduced to themselves",
        args=(3, [[1, 0, 0], [2, 1, 1], [3, 0, 1], [4, 1, 2]]),
        expected=4,
        note="a == b must be a no-op, not a merge.",
    ),
    Case(
        name="shared timestamps",
        args=(4, [[5, 0, 1], [5, 2, 3], [5, 1, 2]]),
        expected=5,
        note="Three entries at the same instant; the answer is that instant.",
    ),
    Case(
        name="entries after everyone is connected",
        args=(3, [[1, 0, 1], [2, 1, 2], [100, 0, 2], [7, 0, 1]]),
        expected=2,
        note="Answer is the earliest moment, not the last entry processed.",
    ),
    Case(
        name="star around one member",
        args=(5, [[3, 0, 2], [1, 0, 4], [4, 0, 1], [2, 0, 3]]),
        expected=4,
        note="One group absorbs singletons, so the surviving root is the same every "
        "time - the mirror image of the chain case.",
    ),
    Case(
        name="one member left out",
        args=(5, [[1, 0, 1], [2, 1, 2], [3, 2, 3], [9, 3, 0]]),
        expected=-1,
        note="Members 0-3 form one group but member 4 is never named.",
    ),
    Case(
        name="perf: 20k members in two long paths, 50k shuffled entries",
        args=(P, CONNECTS),
        expected=P,
        time_limit_ms=3000,
        memory_limit_mb=128,
        note="The joining entry carries the largest timestamp of all, so the answer "
        "is P by construction. The budget rejects an O(m*(n+m)) recount of "
        "connectivity per entry, and also a disjoint-set forest with neither union "
        "by size nor path compression: the two paths are written in opposite order, "
        "so whichever root such an implementation keeps, one path ends up ~10000 "
        "deep and the repeated entries pay that cost on every lookup.",
    ),
    Case(
        name="perf: same size, the two paths never meet",
        args=(P, NEVER),
        expected=-1,
        time_limit_ms=3000,
        memory_limit_mb=128,
        note="Same cost profile, but there is no early exit - every entry must be "
        "processed before -1 can be returned. Catches a solution that falls out of "
        "the loop and reports the last timestamp it saw, and one that stops at two "
        "groups thinking it is done.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(
            earliest_full_connection, CASES, title="P012 - Earliest Full Connection"
        )
    )
