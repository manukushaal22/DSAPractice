"""Test cases for L02.4. Run from repo root:  py run.py L2.4

You can also run this file directly:
    py learn/02-two-pointers/02.4-loading-dock-lanes/tests.py
Feel free to read this file - every input is built from a known multiset, so the
checker only verifies lane order and that nothing was lost or invented.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import arrange_lanes  # noqa: E402

import random  # noqa: E402


def lanes_ok(actual, expected) -> bool:
    """expected = (the input's values in ascending order, reference).

    The answer must be a list holding exactly those values, arranged as
    lighter < reference, then == reference, then > reference.
    """
    values_sorted, reference = expected
    if not isinstance(actual, list) or len(actual) != len(values_sorted):
        return False
    try:
        lane = 0
        for weight in actual:
            current = 0 if weight < reference else (1 if weight == reference else 2)
            if current < lane:
                return False
            lane = current
        return sorted(actual) == values_sorted
    except TypeError:
        return False


def case(name, weights, reference, **extra):
    return Case(
        name=name,
        args=(weights, reference),
        expected=(sorted(weights), reference),
        cmp=lanes_ok,
        **extra,
    )


def _shuffled(items: list, seed: int) -> list:
    random.Random(seed).shuffle(items)
    return items


# ---------------------------------------------------------------- big inputs

N = 1_000_000

# A third lighter, a third exactly the reference, a third heavier, shuffled.
MIXED = _shuffled(
    [-(10**9) + 1999 * i for i in range(N // 3)]
    + [0] * (N // 3)
    + [10**9 - 1999 * i for i in range(N - 2 * (N // 3))],
    seed=24,
)

# Exactly backwards: every heavy parcel first, then the reference ones, then the light
# ones. Every heavy parcel has to travel to the back and every light one to the front.
BACKWARDS = (
    [501 + i % 1000 for i in range(N // 2)]
    + [500] * 1000
    + [i % 500 for i in range(N // 2 - 1000)]
)

PERF_TIME_MS = 3000
PERF_MEMORY_MB = 1

CASES = [
    case("example 1", [5, 2, 8, 5, 1, 9, 5], 5),
    case("example 2 - reference absent", [7, 3, 9, 1], 4),
    case("example 3 - everything matches", [6, 6, 6], 6),
    case("empty list", [], 0),
    case("single parcel, heavier", [9], 3),
    case("all lighter", [1, 2, 3], 10),
    case("all heavier", [11, 12, 13], 10),
    case("already in lane order", [1, 2, 5, 5, 8, 9], 5),
    case("exactly backwards", [9, 8, 5, 5, 2, 1], 5),
    case(
        "heavy swap brings back a light parcel",
        [1, 2, 0],
        1,
        note="After the 2 is swapped to the back, the 0 lands where the 2 was and has "
        "not been examined. Moving the scan forward without examining it leaves "
        "[1, 0, 2].",
    ),
    case(
        "last unexamined parcel",
        [1, 0],
        1,
        note="The 0 is the last unexamined parcel, at the same position as the heavy "
        "boundary. A loop that stops one step early never looks at it.",
    ),
    case("classic three values", [2, 0, 2, 1, 1, 0], 1),
    case("negative weights and reference", [-3, 4, -7, -5, 0, -5], -5),
    case("extreme values", [10**9, -(10**9), 0, 10**9, -(10**9)], 0),
    case(
        "perf: 1M parcels, a third in each lane",
        MIXED,
        0,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=PERF_MEMORY_MB,
        note="MLE means a helper list, sorted copy, or key list. TLE means "
        "pop / insert / remove in a loop (O(n^2)).",
    ),
    case(
        "perf: 1M parcels, exactly backwards",
        BACKWARDS,
        500,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=PERF_MEMORY_MB,
        note="Every parcel is in the wrong lane, so a correct one-pass solution swaps "
        "almost every element. Same budget: O(n) time, O(1) extra space.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(run_cases(arrange_lanes, CASES, title="L02.4 - Loading Dock Lanes"))
