"""L02.5 - Rescue Rafts.

Read the problem in README.md, then fill in `min_rafts` below.
Run the tests from the repo root with:  py run.py L2.5
"""

from typing import List


def min_rafts(weights: List[int], limit: int) -> int:
    """Return the fewest two-person rafts needed to carry everyone.

    Args:
        weights: Each person's weight, between 1 and limit. Possibly empty. May be
            reordered in place.
        limit: The most a single raft can carry, in total.

    Returns:
        The minimum number of rafts, each holding one or two people whose combined
        weight is at most limit.
    """
    weights.sort()
    rafts = 0
    lo, hi = 0, len(weights)-1
    while lo < hi:
        if weights[lo] + weights[hi] <= limit:
            lo += 1
        hi -= 1
        rafts += 1
    if lo == hi:
        rafts += 1
    return rafts

