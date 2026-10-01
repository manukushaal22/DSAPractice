# P005 — Merge Overlapping Intervals

**Difficulty:** Medium
**Topics:** Sorting, Intervals, Sweep

## Problem

You are given a list of intervals, where each interval is a two-element list
`[start, end]` with `start <= end`. The intervals are **closed** — an interval
covers both of its endpoints and everything between them — and they arrive in no
particular order.

Merge every group of intervals that overlap, and return the resulting list of
non-overlapping intervals, **sorted by start**, that covers exactly the same points
as the input.

Two intervals overlap if they share at least one point. In particular `[1, 4]` and
`[4, 5]` overlap, because they both contain 4, and merge into `[1, 5]`. But `[1, 2]`
and `[3, 4]` do not — 2 and 3 are distinct points with nothing joining them.

## Examples

**Example 1**

```
Input:  [[1, 3], [2, 6], [8, 10], [15, 18]]
Output: [[1, 6], [8, 10], [15, 18]]
```

Explanation: `[1, 3]` and `[2, 6]` share the points 2 and 3, so they collapse into
`[1, 6]`. Nothing else touches, and `[8, 10]` and `[15, 18]` survive unchanged.

**Example 2**

```
Input:  [[1, 4], [4, 5]]
Output: [[1, 5]]
```

Explanation: the intervals meet at the single point 4. That still counts as an
overlap, so they merge.

**Example 3**

```
Input:  [[5, 7], [1, 3], [2, 4]]
Output: [[1, 4], [5, 7]]
```

Explanation: the input is unsorted. `[1, 3]` and `[2, 4]` merge into `[1, 4]`; the
gap between 4 and 5 is real, so `[5, 7]` stays separate. The output is ordered by
start regardless of the input order.

## Constraints

- `0 <= len(intervals) <= 100_000`
- `0 <= start <= end <= 1_000_000_000`
- Endpoints are integers, but coordinates are large — the number of *points* covered
  can be a billion even when there are only a handful of intervals.

Return a list of two-element `[start, end]` lists. **Do not modify the input list**,
and do not modify the interval lists inside it.

## Your task

Implement `merge_intervals(intervals: List[List[int]]) -> List[List[int]]` in
`solution.py`.

Run the tests from the repo root with:

```powershell
py run.py 5
```

## Target complexity

**O(n log n) time, O(n) space**, dominated by a single sort.

This rules out two things. First, the O(n²) approach of holding a result list and
scanning all of it for an overlap on every new interval. Second — and the constraints
are chosen specifically to kill this — any approach that works point by point, such as
marking covered coordinates in a set or boolean array. With coordinates up to a
billion, that is a billion units of work and memory for an input of 100 000 intervals.

<details><summary><b>Hint 1</b></summary>

In the given order, an interval might overlap something far away in the list, so you
have no idea which pairs to compare without checking all of them. Is there an ordering
in which an interval can only ever overlap things *adjacent* to it? What would you have
to sort by to get that property?

</details>

<details><summary><b>Hint 2</b></summary>

Sort by start. Now walk left to right, carrying the merged block you are currently
building. When you reach an interval whose start is past the end of that block, you can
close the block permanently — every interval still to come has a start at least as
large, so nothing later can reach back into it either. That "nothing can reach back" is
what buys you a single pass instead of repeated re-scanning.

</details>

<details><summary><b>Hint 3</b></summary>

Sort by start, seed the output with the first interval, then for each subsequent one:
if its start is at or before the current block's end, the block absorbs it — and the
block's new end is the **larger** of the two ends, never simply the incoming one. If its
start is past the block's end, the block is finished; append a fresh block and carry on.

The larger-of-the-two detail is the whole problem. A short interval sitting entirely
inside a long one must not drag the block's end backwards.

Note also that sorting the caller's list in place would violate the "do not modify the
input" rule — take a sorted copy.

</details>
