# L03.4 — Two-Compartment Courier

**Difficulty:** Medium
**Topics:** Sliding Window, Hash Map Counting
**Track:** [03 Sliding Window](../README.md) · rung .4 of 6 (disguised)

## Problem

A street has houses in a fixed order. Every house has placed one food order, and
`orders[i]` is the code of the restaurant that house `i` ordered from.

A courier has an insulated bag with **two compartments**. A compartment can hold any
number of orders, but food from different restaurants must never share a compartment.
So one trip can carry orders from **at most two different restaurants**.

The courier picks one **contiguous** block of houses, collects every order for that
block, and delivers to every house in it. Every house in the block must be served.
A house whose restaurant doesn't fit in the bag can't be skipped.

Return the largest number of houses one trip can serve.

## Examples

**Example 1**

```
Input:  orders = [4, 8, 4, 2, 2, 4]
Output: 4
```

Explanation: houses 2–5 ordered `[4, 2, 2, 4]`, which is only restaurants 4 and 2.
Adding house 1 would bring in restaurant 8 as a third.

**Example 2**

```
Input:  orders = [5, 5, 5]
Output: 3
```

Explanation: one restaurant fits easily, and the second compartment stays empty.

**Example 3**

```
Input:  orders = [1, 2, 3, 4, 5]
Output: 2
```

Explanation: every restaurant differs from its neighbours, so any two adjacent houses
is the best possible.

## Constraints

- `0 <= len(orders) <= 500_000`
- `0 <= orders[i] <= 10^9`

## Your task

Implement `max_houses_served(orders: List[int]) -> int` in `solution.py`. Do not modify
`orders`.

Run the tests from the repo root with:

```powershell
py run.py L3.4
```

## Target complexity

**O(n) time, O(1) extra space.** At any moment you only need to track a handful of
restaurants.

This rules out starting a trip at every house and walking forward until a third
restaurant appears. That is O(n·w), where w is the length of a valid block. On the
perf cases w is in the thousands or hundreds of thousands, so it gets a `TLE`.
Rebuilding a `set` of the current block at every step is just as slow.

Restaurant codes go up to 10⁹, so a fixed-size array indexed by code is not an option.

<details><summary><b>Hint 1</b></summary>

If a block of houses can be served, can every shorter block inside it also be served?
Use the answer to decide what happens to the block's start when its end moves one house
to the right.

</details>

<details><summary><b>Hint 2</b></summary>

Keep a count per restaurant for the houses currently in the block. The block is valid
while at most two restaurants have a non-zero count. When a third one arrives, move the
start forward until one restaurant's count drops to zero. Then remove that restaurant
completely, so "how many restaurants are in the block" is just the number of keys.

</details>

<details><summary><b>Hint 3</b></summary>

Start with an empty block. For each house, add its order to the block. While the
block holds more than two restaurants, take out the house at the start and move the
start forward. Then record the block's length.

Bonus, for the review: this can be done without a dictionary. Remember the two
restaurants in the block, plus where the **latest unbroken run** of a single
restaurant began. Work out what the new block is when a third restaurant arrives.

</details>
