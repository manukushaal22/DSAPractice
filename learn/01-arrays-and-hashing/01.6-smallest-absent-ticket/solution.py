"""L01.6 - Smallest Absent Ticket.

Read the problem in README.md, then fill in `smallest_absent` below.
Run the tests from the repo root with:  py run.py L1.6
"""

from typing import List


def smallest_absent(nums: List[int]) -> int:
    """Return the smallest positive integer missing from nums.

    Args:
        nums: Integers, possibly empty, with duplicates, zeros, negatives and values
            larger than len(nums). May be rearranged or overwritten in place.

    Returns:
        The smallest integer >= 1 that does not occur in nums.
    """
    nums.append(0)
    for i in range(len(nums)-1):
        tmp = nums[i]
        while 0 < tmp < len(nums) and nums[tmp] != tmp:
            nums[tmp], tmp = tmp, nums[tmp]
    for i in range(1, len(nums)):
        if nums[i] != i:
            return i
    return len(nums)
