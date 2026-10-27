# L03.5 — Shuffled Signature

**Difficulty:** Medium
**Topics:** Sliding Window (fixed size), Counting, Hashing
**Track:** [03 Sliding Window](../README.md) · rung .5 of 6 (combined with 01)

## Problem

A monitoring tool scans a stream of lowercase letters for a known **signature**.
Attackers have learned to dodge exact matching by **shuffling** the signature's letters
before sending it.

Report every position where the stream contains a rearrangement of the signature. That
is, return every index `i` such that `stream[i : i + len(signature)]` uses exactly the
same letters as `signature`, each the same number of times. The signature itself, unshuffled,
also counts.

Return the indices in increasing order. Occurrences may overlap.

## Examples

**Example 1**

```
Input:  stream = "tacocatbat", signature = "act"
Output: [0, 4]
```

Explanation: `"tac"` at index 0 and `"cat"` at index 4 are both rearrangements of
`"act"`. `"bat"` at index 7 has a `b` where the signature has a `c`.

**Example 2**

```
Input:  stream = "abab", signature = "ab"
Output: [0, 1, 2]
```

Explanation: `"ab"`, `"ba"`, `"ab"`. The occurrences overlap, and each one is reported.

**Example 3**

```
Input:  stream = "abbab", signature = "aab"
Output: []
```

Explanation: every 3-letter stretch has the right *kinds* of letter, but each one has
two `b`s and one `a`. The signature needs two `a`s.

## Constraints

- `0 <= len(stream) <= 600_000`
- `1 <= len(signature) <= 600_000` (it may be longer than the stream)
- both strings contain only lowercase letters `a`–`z`

## Your task

Implement `find_shuffled(stream: str, signature: str) -> List[int]` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py L3.5
```

## Target complexity

**O(n + m) time, O(1) extra space** besides the returned list. Here n is the stream's
length and m is the signature's length; 26 counters count as O(1).

This rules out checking each position from scratch. Sorting every stretch, or building a
`Counter` for every stretch, is O(n·m). The perf cases use signatures of 50_000+ letters,
so that gets a `TLE`.

Comparing two 26-entry count lists at every position is O(26·n). That counts as O(n) and
passes. The review will mention how to make each step O(1).

<details><summary><b>Hint 1</b></summary>

Compare the stretch starting at `i` with the one starting at `i + 1`. How many letters
differ between them? What does that mean for any counts you kept for the first one?

</details>

<details><summary><b>Hint 2</b></summary>

Every candidate stretch has the same length, m. So the window is a **fixed** size: there
is no shrink decision. Each step adds one letter on the right and removes one on the
left. Keep 26 counters for the window and 26 for the signature. A position matches
exactly when the two sets of counters are equal.

</details>

<details><summary><b>Hint 3</b></summary>

Count the signature. Fill the window with the first m letters of the stream, then
alternate: check for a match, then slide one step. Make sure the stretch that ends on the
stream's very last letter gets checked, and that a signature longer than the stream
falls through with nothing found, without a special case.

Bonus: instead of comparing all 26 counters, keep one number, "how many letters
currently have exactly the right count". A slide changes at most two counters, so only
those two letters can change that number.

</details>
