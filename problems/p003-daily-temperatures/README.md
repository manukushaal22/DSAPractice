# P003 — Daily Temperatures

**Difficulty:** Medium
**Topics:** Arrays, Monotonic Stack

## Problem

You are given a list `temperatures`, where `temperatures[i]` is the temperature
recorded on day `i`.

For every day, you want to know how long you have to wait for a **strictly warmer**
day. Return a list `answer` of the same length, where `answer[i]` is the number of
days you must wait after day `i` for a temperature strictly greater than
`temperatures[i]`. If no such day exists, `answer[i]` is `0`.

A temperature that merely *ties* does not count as warmer.

## Examples

**Example 1**

```
Input:  temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
Output: [1, 1, 4, 2, 1, 1, 0, 0]
```

Explanation: day 0 (73°) is beaten the very next day by 74°, so it waits 1. Day 2
(75°) has to wait through 71°, 69°, 72° before 76° on day 6 — that is 4 days. Days 6
and 7 never see anything warmer, so they get 0.

**Example 2**

```
Input:  temperatures = [30, 40, 50, 60]
Output: [1, 1, 1, 0]
```

Explanation: each day is beaten immediately by its successor; the last day has no
successor.

**Example 3**

```
Input:  temperatures = [55, 55, 55]
Output: [0, 0, 0]
```

Explanation: equal is not warmer, so no day is ever satisfied.

## Constraints

- `0 <= len(temperatures) <= 100_000`
- `-100 <= temperatures[i] <= 100`

Note that temperatures are heavily repeated at this scale — only 201 distinct values
are possible across up to 100 000 days — so ties are the common case, not an edge
case.

## Your task

Implement `daily_temperatures(temperatures: List[int]) -> List[int]` in `solution.py`.

Do not modify the input list.

Run the tests from the repo root with:

```powershell
py run.py 3
```

## Target complexity

**O(n) time, O(n) space.**

The naive approach — for each day, scan forward until you find something warmer — is
O(n²) and is exactly what the perf cases are built to reject. Note that O(n) here is
*amortised*: the algorithm contains a nested loop, but each day is handled a bounded
number of times across the entire run.

<details><summary><b>Hint 1</b></summary>

When you are standing on day `i` and looking backwards, which earlier days could
possibly still be waiting for an answer? If day `a` came before day `b` and
`temperatures[a] <= temperatures[b]`, can day `a` ever be resolved *before* day `b` is?

</details>

<details><summary><b>Hint 2</b></summary>

The set of still-unresolved days, read from oldest to newest, is always in decreasing
temperature order — anything that broke that order would already have been resolved by
the day that broke it. So you only ever need to inspect the *most recent* unresolved
day, and if it gets resolved, the one before it, and so on. That is a stack.

</details>

<details><summary><b>Hint 3</b></summary>

Keep a stack of **indices** of days still waiting for an answer, and a result list
pre-filled with zeros. Sweep left to right. For each new day, repeatedly pop from the
stack while the day on top is strictly cooler than today, filling in that day's answer
as the gap between the two indices. Then push today. Anything still on the stack at the
end keeps its zero. Store indices rather than temperatures — you need the index to
compute the wait, and you can always look the temperature back up.

</details>
