# L03.3 — Uniform Banner

**Difficulty:** Medium
**Topics:** Sliding Window, Counting
**Track:** [03 Sliding Window](../README.md) · rung .3 of 6 (standard)

## Problem

A long banner is a row of painted letters, given as a string `s` of uppercase letters
`A`–`Z`. A painter can **repaint at most `k` letters**, changing each one to any letter.

After repainting, the organisers will cut out the longest **contiguous** stretch in
which every letter is the same. Return the length of the longest such stretch they can
get if the painter chooses the repaints well.

## Examples

**Example 1**

```
Input:  s = "XYXY", k = 2
Output: 4
```

Explanation: repaint both `Y`s to `X` (or both `X`s to `Y`) and the whole banner is
uniform.

**Example 2**

```
Input:  s = "PPQPQQP", k = 1
Output: 4
```

Explanation: repaint the `Q` at index 2 to get `PPPP` at indices 0–3, or the `P` at
index 3 to get `QQQQ` at indices 2–5. No stretch of 5 contains only one letter that
differs from the rest.

**Example 3**

```
Input:  s = "ABCDE", k = 1
Output: 2
```

Explanation: any two neighbours, one of them repainted to match the other.

## Constraints

- `0 <= len(s) <= 500_000`
- `s` contains only uppercase letters `A`–`Z`
- `0 <= k <= len(s)`

## Your task

Implement `longest_uniform(s: str, k: int) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py L3.3
```

## Target complexity

**O(n) time, O(1) extra space** (26 counters count as O(1)).

This rules out checking every stretch, which is O(n²) stretches and gets cut off by the
perf cases. Recomputing a stretch's letter counts from scratch for each new end is just
as slow.

Recomputing `max(counts)` over the 26 counters at every step is O(26·n). That counts as
O(n) and passes. The review will mention a way to avoid it.

<details><summary><b>Hint 1</b></summary>

Look at one stretch. How many repaints does it need to become uniform? Which letter
should it be repainted to, and what does that tell you about the counts you need to keep
for the stretch?

</details>

<details><summary><b>Hint 2</b></summary>

A stretch needs `length - (count of its most common letter)` repaints. It is achievable
when that is at most `k`. That rule is monotone: shrinking a stretch never makes it need
more repaints. So for each right end, find the smallest left end that keeps the stretch
achievable, using 26 counters that are updated as letters enter and leave.

</details>

<details><summary><b>Hint 3</b></summary>

Grow the window by one letter on the right. While it needs more than `k` repaints,
remove the left letter and move left forward. Record the window's length. Start with an
empty window, so no input size needs a special case.

For the bonus: you only care about windows **longer** than the best so far. A remembered
"largest count seen" that is never lowered still gives the right answer. Working out why
is the interesting part.

</details>
