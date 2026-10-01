"""P001 - Best Time to Buy and Sell Stock.

Read the problem in README.md, then fill in `max_profit` below.
Run the tests from the repo root with:  py run.py 1
"""

from typing import List


def max_profit(prices: List[int]) -> int:
    """Return the maximum profit from a single buy-then-sell transaction.

    Args:
        prices: prices[i] is the stock price on day i.

    Returns:
        The best achievable profit, or 0 if no profitable transaction exists.
    """
    if len(prices) < 2:
        return 0

    ans = 0
    nextmax = prices[-1]
    for i in range(len(prices)-2,-1,-1):
        ans = max(nextmax - prices[i], ans)
        nextmax = max(prices[i], nextmax)

    return ans
