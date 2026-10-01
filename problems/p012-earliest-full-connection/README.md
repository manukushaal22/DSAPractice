# P012 — Earliest Full Connection

**Difficulty:** Medium
**Topics:** Union-Find / Disjoint Set Union, Graphs, Sorting

## Problem

A club has `n` members, labelled `0` to `n - 1`. Over time, pairs of members are
introduced to each other, and each introduction is written down as a log entry
`[timestamp, a, b]`.

Acquaintance spreads: if `a` knows `b` and `b` knows `c`, then `a`, `b` and `c` all
belong to the same **group**. Every member starts out in a group of their own, and
groups only ever merge.

The log entries are handed to you in **arbitrary order**, not by time. Return the
earliest timestamp `T` such that, counting only the introductions that happened at time
`T` or earlier, all `n` members belong to a single group. If that never happens, return
`-1`.

A pair may be introduced more than once, and a log entry may name the same member twice
(`a == b`); both are harmless no-ops. Several entries may share a timestamp. You may not
modify or reorder the input list.

## Examples

**Example 1**

```
Input:  n = 6, logs = [[20,1,2], [5,0,1], [70,2,3], [30,4,5], [65,3,4], [10,0,2]]
Output: 70
```

Explanation: in time order the groups are `{0,1}` at 5, `{0,1,2}` at 10, unchanged at 20
(1 and 2 already share a group), `{4,5}` at 30, `{3,4,5}` at 65, and finally at 70 the
`{0,1,2}` and `{3,4,5}` groups merge into one.

**Example 2**

```
Input:  n = 4, logs = [[0,2,0], [1,3,1], [2,1,2]]
Output: 2
```

Explanation: `{0,2}` forms at 0 and `{1,3}` at 1. The entry at 2 joins those two halves,
so 2 is the first moment all four are together.

**Example 3**

```
Input:  n = 4, logs = [[9,0,1], [3,2,3], [100,0,1]]
Output: -1
```

Explanation: `{0,1}` and `{2,3}` never meet. The entry at 100 repeats an introduction
that already happened, so it merges nothing.

## Constraints

- `2 <= n <= 100_000`
- `0 <= len(logs) <= 200_000`
- `0 <= timestamp <= 1_000_000_000`, and timestamps may repeat
- `0 <= a, b < n`, and `a == b` is allowed
- Do not modify the input list

## Your task

Implement `earliest_full_connection(n: int, logs: List[List[int]]) -> int` in
`solution.py`.

Run the tests from the repo root with:

```powershell
py run.py 12
```

## Target complexity

**O(m log m + (n + m)·α(n)) time, O(n) space**, where `m = len(logs)` and `α` is the
inverse Ackermann function — effectively a constant below 5 for any input you will ever
see. In other words: the sort dominates, and everything after it is near-linear.

That rules out two things:

- **Recomputing connectivity from scratch** after each log entry — a BFS/DFS or a
  component recount per entry is `O(m · (n + m))`, which the perf cases will not finish.
- **A disjoint-set structure that is allowed to grow tall.** Merging groups is the easy
  part; keeping the lookup cheap after tens of thousands of merges is the actual lesson.
  The perf cases are shaped so a structure that degenerates into a long chain is just as
  slow as the naive recount.

<details><summary><b>Hint 1</b></summary>

The entries arrive shuffled, but the question is about *time*. Fix that first — once the
entries are in time order you can process them one at a time and never look back, because
groups only ever merge and never split.

Now the narrower question: after processing an entry, how do you decide whether you are
done? Scanning all `n` members to check is what makes the naive approach quadratic. Is
there a single number you could carry along that tells you the same thing for free?

</details>

<details><summary><b>Hint 2</b></summary>

Keep a counter of how many groups currently exist. It starts at `n`.

Each entry in time order does exactly one of two things: it names two members who are
*already* in the same group, and changes nothing, or it names two members in *different*
groups, and merges them — dropping the counter by exactly one. So the counter reaches `1`
at the very first entry that completes the connection, and that entry's timestamp is the
answer. If you run out of entries with the counter above `1`, the answer is `-1`.

Everything now rests on one operation: given a member, say **which group they are in**,
cheaply, after arbitrarily many merges.

</details>

<details><summary><b>Hint 3</b></summary>

Represent each group as a tree and store only a `parent` array: a member points at
another member, and the root of the tree is the group's identity. "Which group?" means
"follow parent links to the root". Merging two groups is then one assignment — point one
root at the other.

Done naively that is a trap: merging a long run of members in order can build a tree that
is essentially a linked list, and every lookup walks the whole thing. Two standard repairs
turn it into near-constant time, and they compose well:

- **Union by size/rank** — when linking two roots, always hang the smaller tree under the
  larger one, so depth grows logarithmically at worst.
- **Path compression** — while walking to the root, re-point the nodes you passed
  (directly, or at their grandparent) so the next lookup is short.

Note that with union by size you no longer control *which* of the two roots survives, so
never assume the surviving root is the smaller label, the first argument, or anything but
whatever the structure hands back.

</details>
