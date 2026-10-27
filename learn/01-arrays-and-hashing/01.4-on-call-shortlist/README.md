# L01.4 — On-Call Shortlist

**Difficulty:** Medium
**Topics:** Hashing, Counting, Selection
**Track:** [01 Arrays & Hashing](../README.md) · rung .4 of 6 (disguised)

## Problem

An incident log records one error code per incident, in the order the incidents
happened. A code can appear in the log any number of times. Codes are integers and can
be negative.

The on-call team can only investigate `k` codes this week. Return the `k` codes with the
**most incidents**.

The log is chosen so the shortlist is never ambiguous. If there are more than `k`
distinct codes, the code ranked `k`-th by incident count has **strictly more**
incidents than the code ranked `(k + 1)`-th. Codes *inside* the shortlist may tie
with each other.

Return the `k` codes as a list in any order.

## Examples

**Example 1**

```
Input:  codes = [404, 500, 404, 503, 500, 404], k = 2
Output: [404, 500]
```

Explanation: `404` has 3 incidents, `500` has 2 and `503` has 1. The two busiest codes
are `404` and `500`.

**Example 2**

```
Input:  codes = [7], k = 1
Output: [7]
```

Explanation: the only code in the log.

**Example 3**

```
Input:  codes = [-1, -1, 0, 2, 2, 2, 0, -1, 9], k = 2
Output: [-1, 2]
```

Explanation: `-1` and `2` have 3 incidents each, `0` has 2 and `9` has 1. The two
shortlisted codes tie with each other, which is fine. What matters is that both beat
`0`.

## Constraints

- `1 <= len(codes) <= 200_000`
- `-10^9 <= codes[i] <= 10^9`
- `1 <= k <=` the number of distinct codes in `codes`
- The shortlist is unique, as described above
- Do not modify the input list

## Your task

Implement `shortlist(codes: List[int], k: int) -> List[int]` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py L1.4
```

## Target complexity

**O(n) time, O(n) space**, where `n = len(codes)`.

The perf cases reject anything that picks the busiest remaining code `k` times
over, which is O(n·k) or O(d·k) for `d` distinct codes. With `k` and `d` both
around 50 000 that is billions of steps.

Ordering the distinct codes by their counts, whether with a full sort or a heap
(`Counter.most_common` uses both internally), is O(d log d) or O(d log k). That
passes the tests, because in Python a C-level sort is hard to tell apart from a linear
pass by timing alone. It **does not meet the target**, and the review will check.
Getting from "sort it" to linear is the point of this rung.

<details><summary><b>Hint 1</b></summary>

Counting each code's incidents is the easy part: one pass, one dictionary. The
question is how to pick the top `k` from those counts **without comparing counts with
each other**.

What is the smallest possible incident count? What is the largest? How many different
values can a count take?

</details>

<details><summary><b>Hint 2</b></summary>

Every count is a whole number between `1` and `n`. When the values you want to order
are small integers from a known range, you do not need to compare them at all. You can
use each one as a **position**, and the positions are already in order.

Note that this applies to the *counts*, not to the codes. The codes span two billion
values and cannot be used as positions.

</details>

<details><summary><b>Hint 3</b></summary>

After counting, make `n + 1` empty lists, one per possible count. Put each code into the
list at its count. Then walk the lists from the highest count down, collecting codes
until you have `k`.

Thanks to the uniqueness guarantee, the cut never falls in the middle of a list. Check
the off-by-one at the top: a single code can account for all `n` incidents. Also make
sure the walk stops early, so you never build the whole ranking.

</details>
