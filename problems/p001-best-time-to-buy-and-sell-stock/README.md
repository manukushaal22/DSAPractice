# P001 — Best Time to Buy and Sell Stock

**Difficulty:** Easy
**Topics:** Arrays, Greedy, Running Minimum, Single Pass

---

## Problem

You are given an array `prices` where `prices[i]` is the price of a given stock on day `i`.

You want to maximise your profit by choosing **a single day to buy** one stock and choosing
**a different day in the future to sell** that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any
profit (prices only ever go down), return `0`.

You must buy **before** you sell — selling on the same day or on an earlier day is not allowed.

---

## Examples

**Example 1**

```
Input:  prices = [7, 1, 5, 3, 6, 4]
Output: 5
Explanation: Buy on day 1 (price = 1) and sell on day 4 (price = 6). Profit = 6 - 1 = 5.
             Note that buying on day 1 and selling on day 0 is not allowed.
```

**Example 2**

```
Input:  prices = [7, 6, 4, 3, 1]
Output: 0
Explanation: Prices only fall, so no transaction is made and the max profit is 0.
```

**Example 3**

```
Input:  prices = [2, 4, 1]
Output: 2
Explanation: Buy at 2, sell at 4. The later dip to 1 is useless because there is
             no day after it to sell on.
```

---

## Constraints

- `1 <= len(prices) <= 10^5`
- `0 <= prices[i] <= 10^4`

---

## Your task

Implement `max_profit` in [`solution.py`](./solution.py).

Run the tests from the repo root:

```powershell
py run.py 1
```

---

## Target complexity

Aim for **O(n) time and O(1) extra space**. A brute-force `O(n^2)` pair check will be
correct but will feel slow on the largest test case — the harness prints per-case timings,
so you will see it.

---

<details>
<summary><b>Hint 1</b> (click to expand)</summary>

The brute force is "try every pair `(i, j)` with `i < j`". Ask yourself: for a fixed
*sell* day `j`, which buy day do you actually want? You never care about *all* earlier
days — only one of them.

</details>

<details>
<summary><b>Hint 2</b></summary>

For a fixed sell day `j`, the best buy day is simply the **cheapest day seen so far**
before `j`. So you only need to remember one number as you scan left to right.

</details>

<details>
<summary><b>Hint 3</b></summary>

Sweep once, keeping two running values:

- `min_so_far` — the lowest price seen up to (and including) the current day
- `best` — the largest `price - min_so_far` seen so far

Update `best` before or after updating `min_so_far`? Think about whether buying and
selling on the *same* day can sneak in — and why it turns out to be harmless here.

</details>
