"""P008 - Subarrays With a Given Sum.

Read the problem in README.md, then fill in `count_subarrays` below.
Run the tests from the repo root with:  py run.py 8
"""

from typing import List


def count_subarrays(nums: List[int], k: int) -> int:
    """Count contiguous non-empty subarrays of `nums` that sum to exactly `k`.

    Args:
        nums: The values. May be empty, and may contain negatives and zeros.
            Must not be modified.
        k: The target sum. May be negative or zero.

    Returns:
        How many contiguous non-empty subarrays sum to exactly `k`. Subarrays at
        different index ranges count separately even if their contents match.
    """
    prefix = [0, *nums]
    for i in range(1, len(prefix)):
        prefix[i] += prefix[i-1]

    hm = {}
    count = 0
    for i in prefix:
        count += hm.get(i - k, 0)
        hm[i] =  hm.get(i, 0) + 1
    return count
