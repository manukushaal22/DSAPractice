"""L01.5 - Longest Unbroken Streak.

Read the problem in README.md, then fill in `longest_streak` below.
Run the tests from the repo root with:  py run.py L1.5
"""

from typing import List


def longest_streak(nums: List[int]) -> int:
    """Return the length of the longest run of consecutive values present in nums.

    Args:
        nums: Integers in any order, possibly empty, possibly with duplicates and
            negatives. Must not be modified.

    Returns:
        The largest L such that x, x + 1, ..., x + L - 1 all occur in nums for
        some x, or 0 if nums is empty.
    """
    numset = set(nums)
    max_streak = 0
    for num in numset:
        if num-1 in numset:
            continue
        current = num
        while current in numset:
            current += 1
        max_streak = max(max_streak, current-num)
    return max_streak
