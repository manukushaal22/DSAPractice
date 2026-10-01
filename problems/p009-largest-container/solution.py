"""P009 - Largest Container.

Read the problem in README.md, then fill in `max_capacity` below.
Run the tests from the repo root with:  py run.py 9
"""

from typing import List


def max_capacity(heights: List[int]) -> int:
    """Return the largest container capacity formed by two posts.

    The capacity of a pair is the distance between the two posts multiplied by
    the height of the shorter one.

    Args:
        heights: Heights of the posts, one unit apart. May be empty or hold a
            single post. Must not be modified.

    Returns:
        The maximum achievable capacity, or 0 if fewer than two posts are given.
    """
    if not heights: return 0
    li, ri = 0, len(heights)-1
    max_capacity = (ri-li) * min(heights[li], heights[ri])
    while li < ri:
        if heights[li]<heights[ri]:
            li += 1
        else:
            ri -= 1
        max_capacity = max(max_capacity, (ri-li) * min(heights[li], heights[ri]))
    return max_capacity


