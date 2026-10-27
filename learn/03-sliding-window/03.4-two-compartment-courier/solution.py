"""L03.4 - Two-Compartment Courier.

Read the problem in README.md, then fill in `max_houses_served` below.
Run the tests from the repo root with:  py run.py L3.4
"""

from typing import List


def max_houses_served(orders: List[int]) -> int:
    """Return the most houses one trip can serve with at most two restaurants.

    Args:
        orders: Restaurant code for each house, in street order. May be empty.
            Codes are between 0 and 10**9. Must not be modified.

    Returns:
        The length of the longest contiguous block of houses whose orders come
        from at most two different restaurants.
    """
    compartments, li, max_len = {}, 0, 0
    for ri, restaurant in enumerate(orders):
        compartments[restaurant] = compartments.get(restaurant, 0) + 1
        while len(compartments) > 2:
            to_remove = orders[li]
            compartments[to_remove] -= 1
            if compartments[to_remove] == 0:
                del compartments[to_remove]
            li += 1
        max_len = max(max_len, ri-li+1)
    return max_len

