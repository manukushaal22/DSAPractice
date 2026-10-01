# P004 — Minimum Processing Rate

**Difficulty:** Medium
**Topics:** Binary Search on Answer, Arrays

## Problem

You are draining log data off a fleet of servers. `logs[i]` is the number of
gigabytes sitting on server `i`, and you have `h` hours before the maintenance
window closes.

You pick a single integer processing rate `r`, in gigabytes per hour, and it applies
to every hour of work. Within any one hour you may only touch **one** server: you
process up to `r` GB from it, and if that server has fewer than `r` GB left you
finish it and the rest of that hour is wasted — you cannot start another server with
the leftover time.

Return the smallest integer `r` that lets you clear every server within `h` hours.

Since `h` is at least the number of servers, some rate always works.

## Examples

**Example 1**

```
Input:  logs = [3, 6, 7, 11], h = 8
Output: 4
```

Explanation: at `r = 4` the servers take 1, 2, 2 and 3 hours, totalling exactly 8.
At `r = 3` they take 1, 2, 3 and 4 hours — 10 in total, which overruns.

**Example 2**

```
Input:  logs = [30, 11, 23, 4, 20], h = 5
Output: 30
```

Explanation: there are 5 servers and 5 hours, so every server must be cleared in a
single hour. That forces `r` up to the largest server.

**Example 3**

```
Input:  logs = [30, 11, 23, 4, 20], h = 6
Output: 23
```

Explanation: one extra hour buys enough slack for the 30 GB server to take two hours
(2 + 1 + 1 + 1 + 1 = 6). At `r = 22` the 23 GB server also spills into a second hour
and the total becomes 7.

## Constraints

- `1 <= len(logs) <= 100_000`
- `1 <= logs[i] <= 1_000_000_000`
- `len(logs) <= h <= 1_000_000_000`

Do not modify the input list.

## Your task

Implement `min_processing_rate(logs: List[int], h: int) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py 4
```

## Target complexity

**O(n log M) time, O(1) extra space**, where `n = len(logs)` and `M = max(logs)`.

The naive approach — try `r = 1`, then `2`, then `3`, until one fits — is O(n · M).
With answers in the hundreds of millions that is hopeless, and the perf cases are
sized to prove it. Note that this problem is not solved by scanning the input
cleverly; the thing you search over is not the array.

<details><summary><b>Hint 1</b></summary>

Suppose you have checked some rate `r` and it is too slow to finish in time. What can
you immediately say about `r - 1`? And if `r` *does* finish in time, what about
`r + 1`? Write down the sequence of yes/no answers for `r = 1, 2, 3, ...` and look at
its shape.

</details>

<details><summary><b>Hint 2</b></summary>

The yes/no sequence is all "no"s followed by all "yes"s — it flips exactly once, and
you want the position of the flip. That is a boundary you can bisect for, provided you
can answer "does rate `r` fit in `h` hours?" cheaply for any single `r`. You can: it is
one pass over the servers.

You also need a starting range. The lower end is 1. For the upper end, ask what rate is
so large that it can never be beaten — what is the fewest hours any server can possibly
take?

</details>

<details><summary><b>Hint 3</b></summary>

Binary search `r` over `[1, max(logs)]`. For a candidate `r`, the hours needed for one
server are its size divided by `r`, **rounded up** — a server with any remainder still
occupies one more whole hour. Sum that over all servers and compare against `h`. If it
fits, the answer is `r` or something smaller, so keep `r` as your best and search the
lower half; if it does not fit, search the upper half. Use integer ceiling division
rather than float division — at a billion GB, floating point will round the wrong way.

</details>
