"""L02.3 - Balanced Trios.

Read the problem in README.md, then fill in `balanced_trios` below.
Run the tests from the repo root with:  py run.py L2.3
"""

from typing import List


def balanced_trios(nums: List[int], target: int) -> List[List[int]]:
    """Return every distinct trio of values from nums that sums to target.

    Args:
        nums: Integers, possibly empty, with duplicates and negatives. May be
            reordered in place.
        target: The sum each trio must hit.

    Returns:
        A list of trios, each a list (or tuple) of three values taken from three
        different positions of nums, summing to target. No two trios use the same
        multiset of values. Order of trios and order within a trio are free.
    """
    nums.sort()
    trios = list()
    for i in range(len(nums)):
        if i>0 and nums[i] == nums[i-1]:
            continue
        # find j & k between i+1 and n that sum to (target - nums[i])
        lo, hi = i+1, len(nums)-1
        find = target - nums[i]
        while lo < hi:
            added = nums[lo] + nums[hi]
            if added == find:
                trios.append([nums[i], nums[lo], nums[hi]])
                cur = nums[lo]
                while lo < hi and cur == nums[lo]:
                    lo += 1
                cur = nums[hi]
                while lo < hi and cur == nums[hi]:
                    hi -= 1
            elif added > find:
                hi -= 1
            elif added < find:
                lo += 1
    return trios

