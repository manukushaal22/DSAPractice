# P010 — Longest Common Subsequence

**Difficulty:** Medium
**Topics:** 2-D Dynamic Programming, Strings

## Problem

A **subsequence** of a string is what remains after deleting zero or more characters
without reordering the survivors. `"ace"` is a subsequence of `"abcde"`; `"aec"` is
not, because the order changed.

Given two strings `a` and `b`, return the **length** of the longest string that is a
subsequence of both.

If they share nothing, the answer is `0`.

## Examples

**Example 1**

```
Input:  a = "abcde", b = "ace"
Output: 3
```

Explanation: `"ace"` is a subsequence of both — it *is* `b`, and it survives in `a`
after deleting `b` and `d`.

**Example 2**

```
Input:  a = "abcbdab", b = "bdcaba"
Output: 4
```

Explanation: `"bcba"` appears in order in both. Several other length-4 answers exist,
such as `"bdab"`. Only the length is asked for, so ties do not matter.

**Example 3**

```
Input:  a = "abc", b = "cba"
Output: 1
```

Explanation: the two strings use the same three characters but in opposite orders, so
no common subsequence can be longer than a single character.

## Constraints

- `0 <= len(a) <= 1000` and `0 <= len(b) <= 1000`
- Both strings consist of ASCII letters; comparison is case-sensitive
- Either string may be empty

## Your task

Implement `lcs_length(a: str, b: str) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py 10
```

## Target complexity

**O(n · m) time, O(min(n, m)) space**, where `n` and `m` are the two lengths.

The time bound rules out exploring subsequences directly — a 1000-character string has
2¹⁰⁰⁰ of them — and it rules out plain recursion on the two indices, which revisits the
same pair of positions an exponential number of times.

Memoising that recursion fixes the repeated work but not the **depth**: at these lengths
the chain of nested calls is a thousand deep or more, past Python's recursion limit. I
have confirmed that both the plain and the `lru_cache`d recursive versions die on the
perf cases. Build the table iteratively.

The space bound is the more interesting half. The natural formulation builds a full
`(n+1) × (m+1)` table, which is a million cells at these limits. **The tests will not
fail you for building the full table** — a million cells still fits in memory — but the
target is `O(min(n, m))` and reaching it is the point of the exercise. Ask what each cell
actually depends on.

<details><summary><b>Hint 1</b></summary>

Compare the last character of `a` with the last character of `b`.

If they are the same character, is there any reason *not* to pair them up? Convince
yourself that some optimal answer uses that pairing, so you lose nothing by committing
to it.

If they differ, then at least one of those two characters cannot be part of the answer —
but you do not know which. What does that leave you to do?

</details>

<details><summary><b>Hint 2</b></summary>

The state is two-dimensional: the answer for the first `i` characters of `a` against the
first `j` characters of `b`.

When the two characters at the front of that boundary match, the answer is one more than
the answer for `(i-1, j-1)`. When they do not, it is the better of `(i-1, j)` and
`(i, j-1)` — you discard one character or the other and take whichever leaves you better
off.

There are only `(n+1) × (m+1)` such states, so solve each once in an order where the
three it depends on are already known.

</details>

<details><summary><b>Hint 3</b></summary>

Build a table with a row per prefix of `a` and a column per prefix of `b`. Row 0 and
column 0 are all zeros: an empty string shares nothing with anything.

Fill it row by row, left to right. Now look at what a cell reads: the cell diagonally
above-left, the one directly above, and the one immediately to its left. Nothing from two
rows back, and nothing from further right. So the moment a row is finished, every row
above it is dead — two rows of storage are enough, and with care, one row plus a single
saved value.

Two details. Roll over whichever dimension is *shorter* if you want `O(min(n, m))` rather
than `O(max(n, m))`. And if you compress to a single row, the diagonal value you need is
the one that lived in the cell you are about to overwrite — save it before you clobber it.

</details>
