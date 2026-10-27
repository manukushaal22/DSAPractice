# L02.3 — Balanced Trios

**Difficulty:** Medium
**Topics:** Two Pointers, Sorting, Deduplication
**Track:** [02 Two Pointers](../README.md) · rung .3 of 6 (standard)

## Problem

You are given a list of integers `nums` and an integer `target`.

A **trio** is a choice of three **different positions** `i`, `j`, `k` in `nums`. It is
**balanced** if `nums[i] + nums[j] + nums[k] == target`.

Return every balanced trio, described by its **values**, with no repeats. Two trios
are the same if they use the same three values: `[-1, 0, 1]` and `[1, -1, 0]` count
once. The same value may appear more than once *within* a trio, as long as it occurs at
that many different positions in `nums`.

Return a list of trios. Each trio is a list (or tuple) of three values. The order of the
trios and the order inside each trio are up to you.

## Examples

**Example 1**

```
Input:  nums = [-3, 1, 2, -1, 0, 1, 2], target = 0
Output: [[-3, 1, 2], [-1, 0, 1]]
```

Explanation: `-3 + 1 + 2 = 0` and `-1 + 0 + 1 = 0`. The list holds two 1s and two 2s,
so `[-3, 1, 2]` can be built from four different sets of positions, but it is listed
once.

**Example 2**

```
Input:  nums = [0, 0, 0, 0], target = 0
Output: [[0, 0, 0]]
```

Explanation: any three of the four zeros work, and they all describe the same trio of
values.

**Example 3**

```
Input:  nums = [1, 2, 3, 4], target = 9
Output: [[2, 3, 4]]
```

Explanation: the target need not be zero. `2 + 3 + 4 = 9` is the only balanced trio.

## Constraints

- `0 <= len(nums) <= 2_000`
- `-10^9 <= nums[i] <= 10^9`
- `-3·10^9 <= target <= 3·10^9`
- You **may** reorder `nums` in place

## Your task

Implement `balanced_trios(nums: List[int], target: int) -> List[List[int]]` in
`solution.py`.

Run the tests from the repo root with:

```powershell
py run.py L2.3
```

## Target complexity

**O(n²) time, O(1) extra space** beyond the output and an in-place sort.

This rules out trying every trio, which is O(n³). That is about 1.3 billion trios at
`n = 2_000`, and a perf case cuts it off. Collecting trios in a set to remove repeats
afterwards does not save it either: you still generate them all.

A hash-set inner loop also gives O(n²) time and passes the tests, but it uses O(n)
extra space. Aim for the two-pointer version. The review will check.

<details><summary><b>Hint 1</b></summary>

Suppose you fix the **smallest** value of the trio. What problem is left on the
remaining values? You have met a version of it before. What property of the input would
let you solve it in one linear pass with no extra memory?

</details>

<details><summary><b>Hint 2</b></summary>

Sort first. Then, for each index `i`, look for pairs in `i + 1 .. n - 1` that sum to
`target - nums[i]`, with one pointer at each end of that range. If the pair's sum is too
small, the left value cannot work with *any* partner up to the right pointer, because
every one of them is at most as large. So the left pointer moves. The mirror argument
moves the right pointer. That is O(n) per `i`, and O(n²) overall.

</details>

<details><summary><b>Hint 3</b></summary>

Repeats come from equal values, and after sorting equal values sit next to each other.
There are two places to skip them:

- **outer:** if `nums[i]` equals the previous first value, every trio it starts has
  already been found
- **inner:** after recording a trio, move *both* pointers past every copy of the
  values they were on

Do not skip so eagerly that you rule out trios like `[-1, -1, 2]`, which legitimately
use one value twice.

An early exit is a nice touch, but the usual one ("stop once `nums[i] > 0`") is only
correct when `target == 0`. Work out the right condition for a general target.

</details>
