# P008 — Subarrays With a Given Sum

**Difficulty:** Medium
**Topics:** Prefix Sums, Hash Map Counting

## Problem

You are given a list of integers `nums` and a target `k`.

Return the number of **contiguous, non-empty** subarrays whose elements sum to
exactly `k`.

Subarrays are counted by position, not by content: two subarrays occupying different
index ranges are different answers even if they contain the same values. The values
may be negative, positive or zero.

## Examples

**Example 1**

```
Input:  nums = [1, 1, 1], k = 2
Output: 2
```

Explanation: positions 0–1 and positions 1–2. They overlap and they look identical,
but they are two distinct subarrays.

**Example 2**

```
Input:  nums = [1, 2, 3], k = 3
Output: 2
```

Explanation: `[1, 2]` at positions 0–1, and `[3]` at position 2. A single element
counts as a subarray.

**Example 3**

```
Input:  nums = [1, -1, 0], k = 0
Output: 3
```

Explanation: `[1, -1]`, `[1, -1, 0]` and `[0]`. Negative values mean adding another
element to a subarray can *lower* its sum — worth keeping in mind before reaching for
a technique that assumes otherwise.

## Constraints

- `0 <= len(nums) <= 100_000`
- `-1000 <= nums[i] <= 1000`
- `-1_000_000_000 <= k <= 1_000_000_000`
- Do not modify the input list

The answer can be far larger than the input: with 100 000 elements there are about
five billion subarrays, and a degenerate input can make all of them match. Python
integers handle that without comment, but it is worth noticing that in a language with
fixed-width integers this return value would need 64 bits.

## Your task

Implement `count_subarrays(nums: List[int], k: int) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py 8
```

## Target complexity

**O(n) time, O(n) space.**

This rules out the O(n²) approach of fixing each start index and extending a running
sum to the right. At `n = 100_000` that is five billion additions and the perf cases
will not wait for it.

It also rules out a **sliding window**, which is the natural instinct after P002 and is
simply invalid here. A window only works when growing it moves the sum in one direction
and shrinking it moves the sum in the other, so that you know which edge to move. With
negative values present, neither is true, and there is no rule for which edge to advance.

<details><summary><b>Hint 1</b></summary>

First convince yourself the sliding window really is dead: with `nums = [1, -1, 1]` and
a window that is currently over-target, does shrinking from the left necessarily reduce
the sum? If you cannot decide which edge to move, you cannot run the window.

So try a different framing. Write down the running total of the whole array from the
start up to each position. What is the sum of the subarray between two positions, in
terms of just those two running totals?

</details>

<details><summary><b>Hint 2</b></summary>

The sum of the elements strictly after position `i` up to and including position `j` is
`total(j) - total(i)`. So you are counting pairs of positions whose running totals
differ by exactly `k` — and for a fixed `j`, the partner you need is a specific value,
`total(j) - k`, not a range.

That turns the inner scan into a lookup. Sweep left to right and, at each position, ask
how many *earlier* positions had that exact running total. Counting how many times you
have already seen a value is what a hash map is for.

</details>

<details><summary><b>Hint 3</b></summary>

One pass. Carry a running total and a map from running-total value to the number of
times it has occurred so far. At each element, update the running total, add to the
answer however many times `running total - k` has already been recorded, then record the
current running total.

Two details decide whether this is right. The map has to begin already knowing that a
running total of zero has occurred once — otherwise every subarray that starts at index
0 goes uncounted, because no earlier position established that baseline. And you must
read the map *before* writing the current total into it: with `k = 0` those two totals
are the same value, and writing first makes every position match itself, counting an
empty subarray each time.

</details>
