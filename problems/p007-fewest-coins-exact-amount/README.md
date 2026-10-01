# P007 — Fewest Coins for an Exact Amount

**Difficulty:** Medium
**Topics:** 1-D Dynamic Programming, Unbounded Knapsack

## Problem

You are given a list of coin denominations and a target `amount`. You have an
**unlimited** supply of every denomination.

Return the smallest number of coins that adds up to exactly `amount`. If no
combination of the given denominations sums to `amount`, return `-1`.

An amount of `0` needs no coins at all, so the answer for it is `0`.

## Examples

**Example 1**

```
Input:  coins = [1, 3, 4], amount = 6
Output: 2
```

Explanation: `3 + 3 = 6` uses two coins. Note that repeatedly grabbing the largest
coin that fits gives `4 + 1 + 1`, which is three — so the obvious greedy strategy is
already wrong on the third example you would ever try.

**Example 2**

```
Input:  coins = [2], amount = 3
Output: -1
```

Explanation: every reachable total is even, so 3 is unreachable.

**Example 3**

```
Input:  coins = [1, 5, 10, 25], amount = 63
Output: 6
```

Explanation: `25 + 25 + 10 + 1 + 1 + 1`. This denomination set happens to be one
where grabbing the largest coin each time *does* give the optimum — which is exactly
why it is a misleading set to reason from.

## Constraints

- `1 <= len(coins) <= 100`
- `1 <= coins[i] <= 1_000_000` — a denomination may be larger than the target, in
  which case it is simply unusable
- `0 <= amount <= 100_000`
- Denominations are not sorted and may contain duplicates
- Do not modify the input list

## Your task

Implement `min_coins(coins: List[int], amount: int) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py 7
```

## Target complexity

**O(amount · len(coins)) time, O(amount) space.**

This rules out searching over combinations, which is exponential — with a 1-unit coin
and a target of 100 000 there are astronomically many ways to reach the total and you
cannot enumerate them.

It also rules out **recursion**, even memoised. A target of 100 000 with a 1-unit
denomination gives a chain of 100 000 nested subproblems, which is far past Python's
recursion limit. Memoisation fixes the *repeated work* but not the *depth*. Build the
answers up from the bottom instead.

<details><summary><b>Hint 1</b></summary>

Greedy fails, so you cannot commit to a coin and never reconsider. But look at what a
single coin choice actually does: if some optimal solution for the target uses a coin
of value `c` at least once, what is left over is a smaller amount — and the coins used
for that leftover must themselves be an optimal solution for it. Why must they be?

</details>

<details><summary><b>Hint 2</b></summary>

That gives a recurrence: the best answer for an amount is one more than the best answer
for `amount - c`, minimised over every denomination `c` that fits. The important part is
the *counting*: every subproblem you will ever need is an amount between 0 and the
target, so there are only `amount + 1` distinct questions, not one per combination.
Solve each exactly once, in increasing order, and every value you need is already
available when you reach it.

</details>

<details><summary><b>Hint 3</b></summary>

Make a table indexed by amount from 0 up to the target. Amount 0 costs zero coins. For
each amount in increasing order, try every denomination that is not larger than it and
take the best already-computed entry for the remainder, plus one.

The detail that breaks most first attempts is how you represent "unreachable". Whatever
sentinel you pick must lose every minimum it takes part in, and adding one to it must
not turn it into a plausible answer — an unreachable remainder plus one coin is still
unreachable, not a cheap solution. Check the final entry against that sentinel to decide
between a real answer and `-1`.

</details>
