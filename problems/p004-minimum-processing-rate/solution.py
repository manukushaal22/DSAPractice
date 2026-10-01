"""P004 - Minimum Processing Rate.

Read the problem in README.md, then fill in `min_processing_rate` below.
Run the tests from the repo root with:  py run.py 4
"""

from typing import List
import math

def can_clear(logs, h, r):
    return sum([int(math.ceil(i/r)) for i in logs])<= h

def min_processing_rate(logs: List[int], h: int) -> int:
    """Return the smallest integer rate that clears every server within `h` hours.

    Args:
        logs: logs[i] is the number of gigabytes on server i. Must not be modified.
        h: The number of hours available. Guaranteed to be at least len(logs).

    Returns:
        The minimum integer gigabytes-per-hour rate that finishes in time.
    """
    l, r = 1, max(logs)
    while l < r:
        md = l + (r-l)//2
        if can_clear(logs,h,md):
            r = md
        else:
            l = md+1
    return r
