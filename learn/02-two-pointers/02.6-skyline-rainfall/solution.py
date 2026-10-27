"""L02.6 - Skyline Rainfall.

Read the problem in README.md, then fill in `trapped_water` below.
Run the tests from the repo root with:  py run.py L2.6
"""

from typing import List


def trapped_water(heights: List[int]) -> int:
    """Return how much rain water the skyline holds.

    Args:
        heights: Building heights, each one unit wide, side by side. Possibly
            empty. Must not be modified.

    Returns:
        The total trapped water in square units.
    """
    if len(heights) < 3:
        return 0

    lo, hi = 1, len(heights)-2
    left_max, right_max = heights[0], heights[-1]
    total = 0

    while lo <= hi:
        left_max = max(left_max, heights[lo])
        right_max = max(right_max, heights[hi])

        if left_max <= right_max:
            total += left_max - heights[lo]
            lo += 1
        else:
            total += right_max - heights[hi]
            hi -= 1

    return total
    # right_max = [i for i in heights]
    # for i in range(len(heights)-2, -1, -1):
    #     right_max[i] = max(right_max[i+1], right_max[i])

    # left_max = heights[0]
    # total = 0
    # for i in range(1, len(heights)-1):
    #     left_max = max(left_max, heights[i])
    #     total += min(left_max, right_max[i])

    # return total - sum(heights) + heights[0] + heights[-1]
