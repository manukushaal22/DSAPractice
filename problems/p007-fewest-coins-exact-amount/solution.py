"""P007 - Fewest Coins for an Exact Amount.

Read the problem in README.md, then fill in `min_coins` below.
Run the tests from the repo root with:  py run.py 7
"""

from typing import List


def min_coins(coins: List[int], amount: int) -> int:
    """Return the fewest coins that sum to exactly `amount`, or -1 if impossible.

    Every denomination is available in unlimited quantity.

    Args:
        coins: The available denominations. Unsorted, possibly containing
            duplicates. Must not be modified.
        amount: The exact total to reach. May be 0.

    Returns:
        The minimum number of coins summing to `amount`, or -1 if no combination
        of the denominations reaches it exactly.
    """
    dp = [-1] * (amount+1)
    dp[0] = 0
    for i in range(len(dp)):
        if dp[i] == -1: continue
        for c in coins:
            if i+c < len(dp):
                if dp[i+c] == -1: dp[i+c] = dp[i]+1
                else: dp[i+c] = min(dp[i+c],dp[i]+1)
    return dp[amount]

