# P006 — Count Land Regions

**Difficulty:** Medium
**Topics:** Grids, BFS/DFS, Flood Fill, Connected Components

## Problem

You are given a rectangular `grid` of `0`s and `1`s, where `1` is land and `0` is
water. A **region** is a maximal group of land cells connected to one another.

Two land cells are connected if they are **directly adjacent — up, down, left or
right**. Cells that meet only at a corner are *not* connected.

Return the number of distinct land regions in the grid.

## Examples

**Example 1**

```
Input:
  1 1 0 0 0
  1 1 0 0 0
  0 0 1 0 0
  0 0 0 1 1

Output: 3
```

Explanation: the four `1`s in the top-left corner form one region. The lone cell at
row 2, column 2 is a second. The pair at the bottom right is a third. Note that the
top-left block and the lone cell touch only diagonally, so they stay separate.

**Example 2**

```
Input:
  1 0
  0 1

Output: 2
```

Explanation: the two land cells share only a corner, which does not connect them.

**Example 3**

```
Input:
  1 1 1
  1 0 1
  1 1 1

Output: 1
```

Explanation: a ring of land around a single water cell. You can walk from any land
cell to any other by going around the hole, so it is all one region.

## Constraints

- `0 <= rows`, `0 <= cols`, and `rows * cols <= 250_000`
- Every cell is either `0` or `1`
- The grid may be empty (`[]`), and may contain rows of length zero
- **Do not modify the input grid.** The caller still needs it afterwards, so the
  common trick of overwriting visited land with water is not available to you.
- A single region may span the entire grid — a quarter of a million connected cells.

## Your task

Implement `count_regions(grid: List[List[int]]) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py 6
```

## Target complexity

**O(R·C) time, O(R·C) space**, where `R·C` is the number of cells. Every cell should
be looked at a constant number of times overall — not once per region.

This rules out restarting a fresh search from every land cell, which is O((R·C)²).

It also rules out **recursion**. Python's default recursion limit is around 1000
frames, and the perf cases include a single region covering 250 000 cells; a recursive
flood fill will die with a `RecursionError` long before it finishes. Raising the limit
is not the answer either — you will hit an actual C stack overflow and take the
interpreter down with it. Manage the frontier yourself.

<details><summary><b>Hint 1</b></summary>

Suppose you scan the grid cell by cell and hit a land cell you have never seen before.
What do you now know about the region it belongs to? Could any *earlier* cell in your
scan have belonged to that same region?

</details>

<details><summary><b>Hint 2</b></summary>

Each time your scan meets land you have not already accounted for, that is a brand new
region — so increment the count, then exhaustively claim every cell reachable from it
before continuing the scan. The total work stays linear because a cell is claimed at
most once ever: the outer scan visits each cell once, and the claiming visits each cell
once across the whole run, not once per region.

</details>

<details><summary><b>Hint 3</b></summary>

Outer loop over every cell. On unclaimed land: add one to the counter, then flood fill
from that cell using an explicit stack or queue that you push to and pop from yourself,
rather than recursion.

Two details decide whether this works. First, mark a cell as claimed at the moment you
**push** it, not when you pop it — otherwise the same cell gets pushed many times by
different neighbours and the frontier explodes. Second, bounds-check before you read a
neighbour; in Python a negative index silently wraps to the other end of the row and
quietly joins regions that are nowhere near each other.

</details>
