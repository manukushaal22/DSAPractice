# P014 — Total XOR Over Every Subarray

**Difficulty:** Medium
**Topics:** Bit Manipulation, Prefix XOR, Counting

## Problem

You are given a list of non-negative integers `nums`.

A **subarray** is any run of one or more neighbouring elements. For a list of length `n`
there are `n · (n + 1) / 2` of them, counting each starting and ending position
separately even when two subarrays happen to hold the same values.

Take the bitwise XOR of every subarray, then add all of those XORs together. Return that
total.

The list may be empty, in which case there are no subarrays and the total is `0`. The
input must not be modified.

## Examples

**Example 1**

```
Input:  nums = [1, 3]
Output: 6
```

Explanation: the subarrays are `[1]` → `1`, `[3]` → `3` and `[1, 3]` → `1 ^ 3 = 2`.
Total `1 + 3 + 2 = 6`.

**Example 2**

```
Input:  nums = [5, 2, 5]
Output: 28
```

Explanation: `[5]` → `5`, `[2]` → `2`, `[5]` → `5`, `[5,2]` → `7`, `[2,5]` → `7`,
`[5,2,5]` → `2`. Total `5 + 2 + 5 + 7 + 7 + 2 = 28`.

**Example 3**

```
Input:  nums = [4, 4, 4]
Output: 16
```

Explanation: the three single elements give `4` each, the two adjacent pairs give
`4 ^ 4 = 0` each, and the whole list gives `4`. Total `12 + 0 + 4 = 16`. Repeated values
cancel, so a longer list does not mean a larger total.

## Constraints

- `0 <= len(nums) <= 100_000`
- `0 <= nums[i] < 2^31`
- The total can be far larger than any single element — Python integers are unbounded, so
  there is nothing to guard against, but do not expect it to fit in 32 bits
- Do not modify the input list

## Your task

Implement `total_subarray_xor(nums: List[int]) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py 14
```

## Target complexity

**O(n · B) time, O(B) space**, where `B` is the number of bit positions in play (31 here).
Since `B` is a constant fixed by the value range, that is linear time and constant space.

That rules out **visiting the subarrays at all**. There are `n · (n + 1) / 2` of them, so
even the tidy version — walking a running XOR outward from each start, never recomputing
anything — is `O(n²)`, and at the perf sizes that is tens of millions of iterations. The
budget will cut it off.

The answer is a *sum*, and a sum does not care how its terms were grouped. So the question
to sit with is not "how do I XOR each subarray faster" but "how much does each subarray
contribute, and can I total those contributions without ever forming a subarray".

<details><summary><b>Hint 1</b></summary>

Two independent observations; you need both.

First: in p008 you turned "the sum of a subarray" into a difference of two precomputed
running totals, so any subarray's value came from two numbers instead of a walk. XOR is
its own inverse — `x ^ y ^ y == x` — which is exactly the property that made subtraction
work for sums. What is the XOR analogue of a prefix sum, and what does a subarray's XOR
become once you have it?

Second: bits do not talk to each other. Bit 5 of `a ^ b` depends only on bit 5 of `a` and
bit 5 of `b`, and nothing else. So the total you want can be split into 31 completely
separate, much simpler questions.

</details>

<details><summary><b>Hint 2</b></summary>

Let `P[0] = 0` and `P[i] = nums[0] ^ nums[1] ^ … ^ nums[i-1]`. Then the XOR of the
subarray spanning positions `l` through `r-1` is exactly `P[r] ^ P[l]`.

Every subarray corresponds to one pair `l < r`, and every pair corresponds to one
subarray. So the whole problem is now: **given the `n + 1` values `P[0] … P[n]`, sum
`P[i] ^ P[j]` over all pairs `i < j`.** The subarrays are gone.

Now apply the second observation. For one bit position `b`, `P[i] ^ P[j]` has that bit set
precisely when `P[i]` and `P[j]` **differ** there — one has it, the other does not. So for
bit `b` you do not need the pairs, only two counts: how many of the prefix values have
bit `b` set, and how many do not. How many differing pairs does that give you, and what is
each one worth?

</details>

<details><summary><b>Hint 3</b></summary>

For bit `b`, let `c` be how many of the `n + 1` prefix values have that bit set. Every set
one pairs with every unset one, and no other pair contributes, so bit `b` adds
`c · (n + 1 − c) · 2^b` to the answer. Sum that over all 31 bit positions and you are done.

The shape: walk the list once keeping a rolling XOR, starting at `0` and counting that
starting `0` as a prefix value too — forgetting it drops every subarray that begins at
position 0. For each prefix value you see, bump a counter for each bit it has set. That is
an array of 31 counters, nothing more. Then one short loop over the bits assembles the
total.

Note what you do **not** need: the prefix values themselves. The counters are the only
thing carried forward, so there is no array to build — the same fusing that turned p001's
suffix-max array into a scalar.

</details>
