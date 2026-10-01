"""P003 - Daily Temperatures.

Read the problem in README.md, then fill in `daily_temperatures` below.
Run the tests from the repo root with:  py run.py 3
"""

from typing import List


def daily_temperatures(temperatures: List[int]) -> List[int]:
    """Return, for each day, the wait until a strictly warmer day.

    Args:
        temperatures: temperatures[i] is the temperature on day i. May be empty.
            Must not be modified.

    Returns:
        A list of the same length where entry i is the number of days after day i
        until a strictly greater temperature occurs, or 0 if there is none.
    """
    ans = [0 for i in temperatures]
    stack = []
    for i in range(len(temperatures)):
        while len(stack) > 0 and temperatures[stack[-1]] < temperatures[i]:
            idx = stack.pop()
            ans[idx] = i - idx
        stack.append(i)
    return ans
