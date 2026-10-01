# P002 — Longest Substring Without Repeating Characters

**Difficulty:** Medium
**Topics:** Strings, Sliding Window, Hash Map

## Problem

You are given a string `s`. A *substring* is a contiguous run of characters taken
from `s` — `"bcd"` is a substring of `"abcde"`, but `"ace"` is not.

Return the length of the longest substring of `s` in which no character appears
more than once.

If `s` is empty, the answer is `0`.

## Examples

**Example 1**

```
Input:  s = "abcabcbb"
Output: 3
```

Explanation: `"abc"` (positions 0–2) has all-distinct characters and length 3.
Extending it to `"abca"` repeats `a`, and no window of length 4 anywhere in the
string is repeat-free.

**Example 2**

```
Input:  s = "bbbbb"
Output: 1
```

Explanation: every character is the same, so the longest repeat-free substring is
a single `"b"`.

**Example 3**

```
Input:  s = "pwwkew"
Output: 3
```

Explanation: the answer is `"wke"` (positions 2–4). Note that `"pwke"` is **not**
valid — it is a subsequence, not a contiguous substring.

## Constraints

- `0 <= len(s) <= 100_000`
- `s` consists of printable ASCII characters: letters, digits, symbols, and spaces.
  Comparison is case-sensitive, so `'a'` and `'A'` are different characters.

## Your task

Implement `length_of_longest_substring(s: str) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py 2
```

## Target complexity

**O(n) time, O(k) space**, where `n = len(s)` and `k` is the number of distinct
characters (bounded by the alphabet size, so effectively O(1)).

This rules out the obvious O(n²) approach — for every start index, walk forward
until you hit a repeat — and the even worse O(n³) one that re-checks each candidate
substring for duplicates from scratch. With `n = 100_000` the perf cases give the
quadratic version no chance.

<details><summary><b>Hint 1</b></summary>

Think about what happens when you slide a window one step to the right and the new
character is already inside the window. You have to shrink the window from the left
until the duplicate is gone — but how far left, exactly? Is there a way to know that
without walking backwards one character at a time?

</details>

<details><summary><b>Hint 2</b></summary>

The window's left edge only ever moves **right**, never left. So the two edges
together take at most `2n` steps over the whole run — that is where the O(n) comes
from. To jump the left edge in a single move, you need to remember, for each
character, the most recent position where you saw it.

</details>

<details><summary><b>Hint 3</b></summary>

Keep a dict mapping character → last index seen, plus a `left` marker for the start of
the current window. Sweep `right` from `0` to `n-1`. If the character at `right` was
seen at an index that is still inside the window (i.e. at or after `left`), move `left`
to just past that index. Then record the current index for that character and update the
best length with the current window size. That "at or after `left`" test is the part
people get wrong — without it, a stale index from before the window drags `left`
backwards.

</details>
