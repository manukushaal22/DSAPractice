"""L02.4 - Loading Dock Lanes.

Read the problem in README.md, then fill in `arrange_lanes` below.
Run the tests from the repo root with:  py run.py L2.4
"""

from typing import List


def arrange_lanes(weights: List[int], reference: int) -> List[int]:
    """Rearrange weights in place into lighter / equal / heavier lanes.

    Args:
        weights: Parcel weights, possibly empty, with duplicates and negatives.
            Rearranged in place.
        reference: The reference weight separating the lanes.

    Returns:
        The same list object, now holding every parcel lighter than reference,
        then every parcel equal to it, then every parcel heavier. Order within a
        lane is free.
    """
    less_end, equal_end, unexp_end = 0, 0, len(weights)
    while equal_end < unexp_end:
        to_place = weights[equal_end]
        if to_place == reference:
            equal_end += 1
        elif to_place > reference:
            weights[equal_end], weights[unexp_end-1] = weights[unexp_end-1], weights[equal_end]
            unexp_end -= 1
        elif to_place < reference:
            weights[less_end], weights[equal_end] = weights[equal_end], weights[less_end]
            less_end += 1
            equal_end += 1
    return weights




