# L04.3 — Farm Plot Ledger

**Difficulty:** Medium
**Topics:** Prefix Sums (2-D), Inclusion–Exclusion
**Track:** [04 Prefix Sums & Difference Arrays](../README.md) · rung .3 of 6 (standard)

## Problem

A farm is divided into a grid of plots with `R` rows and `C` columns. The season's
ledger records each plot's result: `ledger[r][c]` is that plot's profit, and a loss is
recorded as a negative number.

The owners ask many questions of the form "what was the combined result of the
rectangular block of plots from row `r1` to row `r2` and from column `c1` to column
`c2`?" Both ends are inclusive.

Given the ledger and a list of queries `(r1, c1, r2, c2)`, return a list with the
total for each query, in the same order. Do not modify the ledger.

## Examples

All three examples use this ledger:

```
ledger = [
    [3, -1,  4],
    [1,  5, -9],
    [2,  6,  5],
]
```

**Example 1**

```
Input:  queries = [(0, 0, 2, 2), (1, 1, 2, 2), (0, 2, 1, 2)]
Output: [16, 7, -5]
```

Explanation: the whole farm sums to 16. The bottom-right 2×2 block is
`5 − 9 + 6 + 5 = 7`. Rows 0–1 of column 2 are `4 − 9 = −5`.

**Example 2**

```
Input:  queries = [(2, 0, 2, 0), (0, 1, 0, 1)]
Output: [2, -1]
```

Explanation: a query can be a single plot.

**Example 3**

```
Input:  queries = [(1, 0, 1, 2), (0, 1, 2, 1)]
Output: [-3, 10]
```

Explanation: row 1 across every column is `1 + 5 − 9 = −3`. Column 1 down every row is
`−1 + 5 + 6 = 10`.

## Constraints

- `1 <= R, C <= 500`
- `-10^4 <= ledger[r][c] <= 10^4`
- `0 <= len(queries) <= 200_000`
- `0 <= r1 <= r2 < R` and `0 <= c1 <= c2 < C` for every query

## Your task

Implement `plot_totals(ledger: List[List[int]], queries: List[Tuple[int, int, int, int]]) -> List[int]`
in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py L4.3
```

## Target complexity

**O(R·C + Q) time, O(R·C) extra space**: one pass of precomputation over the grid, then
O(1) per query.

This rules out summing each query's rectangle, which is O(R·C) per query. It also rules
out one prefix-sum list per row, which still costs O(R) per query: about 10⁸ steps on
the perf case, so it gets a `TLE`.

<details><summary><b>Hint 1</b></summary>

Suppose you knew the total of every rectangle whose top-left corner is plot `(0, 0)`.
How could you combine a few of those totals to get any other rectangle?

</details>

<details><summary><b>Hint 2</b></summary>

Precompute `T[i][j]` = the total of every plot in rows `< i` and columns `< j`. Give `T`
an extra row and column of zeros at the start, so `i` and `j` run from 0 to `R` and `C`.

A query's rectangle is the corner rectangle that ends at its bottom-right plot, minus
the strip above it, minus the strip to its left. The top-left piece has now been
subtracted twice, so add it back once.

</details>

<details><summary><b>Hint 3</b></summary>

Build `T` one row at a time. Each entry is its own plot, plus the entry above, plus the
entry to the left, minus the diagonal entry above-left, which both of those already
include. Then each query is four lookups.

Check every `+ 1` by hand on a 1×1 ledger before trusting the formula.

</details>
