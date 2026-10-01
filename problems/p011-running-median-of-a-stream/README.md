# P011 — Running Median of a Stream

**Difficulty:** Medium
**Topics:** Heaps / Priority Queues, Streaming, Invariant Maintenance

## Problem

Readings arrive one at a time from a sensor. After **each** reading you must report the
median of everything seen so far — not just at the end.

The median of a collection of numbers is the middle value once they are sorted. If the
count is odd there is exactly one middle value. If the count is even there are two, and
the median is their average (so it may land on a half, e.g. the median of `[1, 2]` is
`1.5`).

Given the readings in arrival order, return a list of the same length whose `i`-th entry
is the median of the first `i + 1` readings. An empty stream produces an empty list.

Values may repeat and may be negative. You may not reorder or modify the input.

## Examples

**Example 1**

```
Input:  nums = [2, 1, 5, 7, 2, 0, 5]
Output: [2.0, 1.5, 2.0, 3.5, 2.0, 2.0, 2.0]
```

Explanation: the sorted prefixes are `[2]`, `[1,2]`, `[1,2,5]`, `[1,2,5,7]`,
`[1,2,2,5,7]`, `[0,1,2,2,5,7]`, `[0,1,2,2,5,5,7]`. Their middles are `2`, `(1+2)/2`,
`2`, `(2+5)/2`, `2`, `(2+2)/2`, `2`.

**Example 2**

```
Input:  nums = [1, 2, 3, 4]
Output: [1.0, 1.5, 2.0, 2.5]
```

Explanation: with a sorted stream the median creeps forward by half a step per reading.

**Example 3**

```
Input:  nums = [5, -5]
Output: [5.0, 0.0]
```

Explanation: one reading is its own median; two readings average, and the average of
`5` and `-5` is `0`.

## Constraints

- `0 <= len(nums) <= 200_000`
- `-1_000_000_000 <= nums[i] <= 1_000_000_000`
- Do not modify the input list
- Answers within `1e-9` of the true median are accepted

## Your task

Implement `running_medians(nums: List[int]) -> List[float]` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py 11
```

## Target complexity

**O(n log n) total time, O(n) space.**

That is `O(log n)` amortised work per reading. It rules out two tempting approaches:

- re-sorting the prefix on every reading — `O(n² log n)`;
- keeping one sorted list and inserting each new reading into its place — finding the
  slot is cheap, but the insertion shifts everything after it, so it costs `O(n²)`
  element moves. The perf cases are shaped so the insertion point is never near the end.

Reporting only the *final* median would be an easier problem. The point here is that the
structure you build has to survive from one reading to the next.

<details><summary><b>Hint 1</b></summary>

You never actually need the prefix sorted. You need one or two values out of it — the
ones sitting at the middle — and you need them to still be findable after the next
reading arrives.

So ask a narrower question: what is the cheapest structure that can hand you the
*largest* element of a group in `O(1)` and absorb a new element in `O(log n)`? And what
would you have to arrange so that the element it hands you is the *middle* of the stream
rather than the largest?

</details>

<details><summary><b>Hint 2</b></summary>

Split the readings seen so far into two groups: a **low half** and a **high half**, with
every value in the low half `<=` every value in the high half.

If you keep their sizes equal, or let one of them run exactly one ahead, then the median
is determined entirely by the *boundary* between them: the largest value of the low half
and the smallest value of the high half. Nothing deeper inside either group matters.

A max-heap over the low half and a min-heap over the high half each expose exactly their
boundary element in `O(1)` and accept a new value in `O(log n)`. Python only ships a
min-heap (`heapq`), so the usual trick for the low half is to store negated values.

</details>

<details><summary><b>Hint 3</b></summary>

Per reading: put it into one of the two halves based on how it compares to the current
boundary, then repair the size invariant by moving at most one element across — pop the
top of the oversized half and push it onto the other. One transfer is always enough,
because a single insertion can unbalance the sizes by only one.

Then read the median off the tops: if the halves are uneven it is the top of the bigger
one; if they are equal it is the average of the two tops. Watch the division — you want
a true average, not an integer one.

Do the repair *unconditionally* after every insert rather than enumerating cases, and
check what your code does on the very first reading, when one half is still empty and
has no top to compare against.

</details>
