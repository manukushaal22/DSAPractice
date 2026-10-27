# L01.3 — Group Rearranged Words

**Difficulty:** Medium
**Topics:** Hashing, Canonical Keys, Strings
**Track:** [01 Arrays & Hashing](../README.md) · rung .3 of 6 (standard)

## Problem

You are given a list of lowercase words. Two words are **rearrangements** of each other
if one can be turned into the other by reordering its letters. That means they use
exactly the same letters, each the same number of times.

Split the words into groups so that two words share a group **if and only if** they are
rearrangements of each other. Return the groups as a list of lists.

- Every input word appears in the output exactly once. If the same word appears twice
  in the input, it appears twice in its group.
- Groups may come in any order, and so may the words within a group.
- The empty string is a word. All empty strings are rearrangements of each other.

## Examples

**Example 1**

```
Input:  words = ["listen", "silent", "google", "enlist", "gogole", "cat"]
Output: [["listen", "silent", "enlist"], ["google", "gogole"], ["cat"]]
```

Explanation: `listen`, `silent` and `enlist` each use e, i, l, n, s, t once. `google`
and `gogole` each use two g's, two o's, one l and one e. `cat` matches nothing.

**Example 2**

```
Input:  words = ["", "a", ""]
Output: [["", ""], ["a"]]
```

Explanation: the two empty strings form one group, and the duplicate is kept rather than
dropped.

**Example 3**

```
Input:  words = ["ab", "aab", "ba", "abb"]
Output: [["ab", "ba"], ["aab"], ["abb"]]
```

Explanation: all four words use only `a` and `b`, but in different amounts. Using the
same letters is not enough; each letter must appear the same number of times.

## Constraints

- `0 <= len(words) <= 100_000`
- `0 <= len(words[i]) <= 40`
- Words contain only lowercase English letters `a`–`z`
- Do not modify the input list
- Return a `list` of `list`s, not a `dict` view or a generator

## Your task

Implement `group_rearranged(words: List[str]) -> List[List[str]]` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py L1.3
```

## Target complexity

**O(n·k) time and O(n·k) space**, where `n` is the number of words and `k` the maximum
word length. A solution within a `log k` factor of that time is also accepted.

This rules out comparing words with each other. Checking every pair is O(n²·k).
Comparing each word against one representative per existing group is O(n·g·k), which
is just as bad when most words are unrelated (`g ≈ n`). The perf cases have 100 000
words.

<details><summary><b>Hint 1</b></summary>

Suppose each word came with a label, computed from that word alone, that is identical
for rearrangements and different otherwise. How would you turn grouping into a single
pass with no word-to-word comparisons?

</details>

<details><summary><b>Hint 2</b></summary>

The label has to throw away the **order** of the letters but keep **how many of each**.
There are two natural ways to describe a word's letters with order removed: put them in a
fixed order, or record how many times each letter occurs. Either can be a hash-table key,
as long as it is hashable and two different words never share it by accident.

</details>

<details><summary><b>Hint 3</b></summary>

One pass: compute the word's key, then append the word to the list stored under that key,
creating the list on first use. At the end, return the stored lists.

If your key records letter counts, store it as a tuple. A list cannot be hashed. Joining the
counts as digits without separators makes `"a" + "b" * 11` and `"a" * 11 + "b"` collide.
Ask yourself what your key costs to build per word, and whether that meets the target.

</details>
