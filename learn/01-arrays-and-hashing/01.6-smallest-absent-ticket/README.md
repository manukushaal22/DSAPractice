# L01.6 — Smallest Absent Ticket

**Difficulty:** Hard
**Topics:** Arrays, In-place Hashing, Index Arithmetic
**Track:** [01 Arrays & Hashing](../README.md) · rung .6 of 6 (stretch, optional)

## Problem

A raffle hands out tickets numbered `1, 2, 3, ...`. You are given a list of numbers read
off a pile of slips. Some are real ticket numbers, some are duplicates, and some are junk:
zero, negative, or far too large.

Return the **smallest positive integer that does not appear in the list**. That is the
lowest ticket number still free.

You are allowed to **rearrange or overwrite the list**. Its contents after your function
returns do not matter.

## Examples

**Example 1**

```
Input:  nums = [3, 4, -1, 1]
Output: 2
```

Explanation: `1` is present, `2` is not. The `-1` is junk and `3` and `4` are irrelevant.

**Example 2**

```
Input:  nums = [1, 2, 0]
Output: 3
```

Explanation: `1` and `2` are both present, so the first free number is `3`.

**Example 3**

```
Input:  nums = [7, 8, 9, 11, 12]
Output: 1
```

Explanation: nothing small is present, so `1` is free.

## Constraints

- `0 <= len(nums) <= 1_000_000`
- `-2^31 <= nums[i] <= 2^31 - 1`
- You may modify `nums` in place
- **O(1) extra space**: a few integer variables, no extra structure that grows with `n`

## Your task

Implement `smallest_absent(nums: List[int]) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py L1.6
```

## Target complexity

**O(n) time, O(1) extra space.**

A set of the values, or a `seen` list indexed by value, solves this in O(n) time and is
the right first answer in an interview. The follow-up question is always "now do it
without the extra memory", and this rung is that follow-up. A set, a list of flags, a
`bytearray`, a sorted copy, and an in-place `sort()` all fail the constraint. The last
one fails because it is O(n log n) and Python's sort allocates a scratch buffer of up
to `n/2` slots.

**What the tests can check:** the perf cases use a million numbers and reject anything
quadratic, such as trying `1, 2, 3, ...` with `in` on the list (`TLE`). **What they
cannot check is the O(1) space.** In Python every integer is an object, so even a
correct in-place solution that writes new values (for example negated ones) allocates
new int objects. That can show up as much memory as a set. Space is therefore checked
in the review: a solution that passes the tests by building any structure that grows
with `n` is not done.

What is left is to use the input list itself as the lookup table.

<details><summary><b>Hint 1</b></summary>

If the list has `n` numbers, what is the **largest** value the answer could possibly
be? Which numbers in the list can therefore never matter?

</details>

<details><summary><b>Hint 2</b></summary>

The answer lies in `1 .. n + 1`, so only values in `1 .. n` matter. There are `n` of
those values and `n` positions in the list. Each relevant value `v` has a natural
"home": position `v - 1`.

If every relevant value could be put at its home, or its presence recorded *at* its
home, one final scan would reveal the first position that is not occupied correctly.
The list itself becomes the hash table, with the value as the key and its home
position as the bucket.

</details>

<details><summary><b>Hint 3</b></summary>

One shape: for each position, while the value there is in `1 .. n` and is **not
already** at its home, swap it into its home. Each swap places at least one value
permanently, so the total number of swaps is at most `n`. Then scan for the first
position `i` that does not hold `i + 1`.

Duplicates are the trap. If the home already holds the same value, swapping again
changes nothing and loops forever, so check the destination, not just the source.

Another shape skips swapping altogether. Make the junk values harmless first, then
record "value `v` is present" by changing the **sign** of whatever sits at position
`v - 1`. Read values through `abs()` so the marks do not corrupt them.

</details>
