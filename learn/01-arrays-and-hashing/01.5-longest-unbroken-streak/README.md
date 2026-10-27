# L01.5 — Longest Unbroken Streak

**Difficulty:** Medium
**Topics:** Hashing, Sets, Amortised Analysis
**Track:** [01 Arrays & Hashing](../README.md) · rung .5 of 6 (harder variant)

## Problem

You are given a list of integers in no particular order. The list may contain
duplicates and negative numbers.

A **streak** of length `L` is a run of consecutive values `x, x + 1, ..., x + L - 1`
that **all** occur somewhere in the list. Positions do not matter, only whether each
value is present. A value present several times still counts once.

Return the length of the longest streak. An empty list has no streak, so return `0`.

## Examples

**Example 1**

```
Input:  nums = [100, 4, 200, 1, 3, 2]
Output: 4
```

Explanation: `1, 2, 3, 4` are all present. `100` and `200` are streaks of length 1.

**Example 2**

```
Input:  nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
Output: 9
```

Explanation: every value from `0` to `8` is present. The second `0` adds nothing.

**Example 3**

```
Input:  nums = [-2, -1, 1, 2, 3]
Output: 3
```

Explanation: `1, 2, 3` is the longest streak. `-2, -1` would join it, but `0` is
missing, so the two runs stay separate.

## Constraints

- `0 <= len(nums) <= 200_000`
- `-10^9 <= nums[i] <= 10^9`
- Do not modify the input list

## Your task

Implement `longest_streak(nums: List[int]) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py L1.5
```

## Target complexity

**O(n) time, O(n) space.**

The perf cases reject approaches that rescan a long streak many times. One example is
walking upward from **every** value: on a single streak of 200 000 values, that is
about 2·10¹⁰ steps. Watch the duplicates too. A fast approach can become quadratic
again if a value that occurs 100 000 times triggers 100 000 walks.

Sorting first gives O(n log n). That passes the tests, for the same reason as in L01.4
(a C-level sort is hard to tell apart from a linear pass by timing). It **does not meet
the target**, and the review will check. The values span two billion, so an array
indexed by value is not an option either.

<details><summary><b>Hint 1</b></summary>

With a set, "is `x + 1` present?" costs O(1). Starting at any value and stepping
upward while the next value is present finds the streak above it.

Now count the work. If you do that from every value in a single streak of length `L`,
how many steps is it in total? Which of those walks was actually needed?

</details>

<details><summary><b>Hint 2</b></summary>

Only one walk per streak is needed: the one that starts at the streak's **lowest**
value. You can recognise that value in O(1) by asking a single question about its
neighbour.

Starting walks only there means every value is stepped over at most once across all
walks combined. That is what makes the total linear, even though a single walk can be
long.

</details>

<details><summary><b>Hint 3</b></summary>

Build a set of the values. Go through each **distinct** value. If its predecessor is
absent, it starts a streak: step upward while the next value is present, then compare
the streak's length with the best so far. Otherwise, skip it.

Loop over the distinct values, not the raw list. Otherwise a repeated streak start
repeats the whole walk. An empty input should give `0` with no special case.

</details>
