# P009 — Largest Container

**Difficulty:** Medium
**Topics:** Two Pointers, Greedy Exchange Argument

## Problem

A row of vertical posts stands on a flat surface. `heights[i]` is the height of the
post at position `i`, and consecutive posts are exactly one unit apart.

Choose **two** posts to act as the walls of a container. The container has no bottom
and no other walls, so the water it holds is limited by the shorter of the two posts:

```
capacity = (distance between the two posts) × (height of the shorter post)
```

Return the largest capacity achievable. If there are fewer than two posts, no
container can be formed, so return `0`.

The posts between the two you choose are ignored — they neither help nor hinder.

## Examples

**Example 1**

```
Input:  heights = [1, 8, 6, 2, 5, 4, 8, 3, 7]
Output: 49
```

Explanation: the posts at positions 1 and 8, of heights 8 and 7. They are 7 apart and
the shorter is 7, giving `7 × 7 = 49`. The two 8s at positions 1 and 6 are taller on
average but only 5 apart, giving 40.

**Example 2**

```
Input:  heights = [1, 1]
Output: 1
```

Explanation: the only possible pair — 1 unit apart, shorter post 1.

**Example 3**

```
Input:  heights = [4, 3, 2, 1, 4]
Output: 16
```

Explanation: the two 4s at the ends. They are 4 apart and equally tall, so `4 × 4`.
The short posts sagging in the middle are irrelevant.

## Constraints

- `0 <= len(heights) <= 100_000`
- `0 <= heights[i] <= 1_000_000_000`
- Do not modify the input list

Capacities can reach roughly 10¹⁴, so this is another problem where the answer needs
64 bits in a language that cares.

## Your task

Implement `max_capacity(heights: List[int]) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py 9
```

## Target complexity

**O(n) time, O(1) space.**

This rules out checking all pairs, which is O(n²) — five billion pairs at
`n = 100_000`.

The efficient solution is short, but its *correctness is the hard part*. It works by
discarding candidate posts without examining the pairs they belong to, and the whole
problem is being able to justify why that is safe. Aim to be able to state the argument
out loud, not just to make the tests pass.

<details><summary><b>Hint 1</b></summary>

Start from the widest container possible: the two posts at either end. Every other pair
is strictly narrower, so any pair that beats it has to make up for lost width with extra
height.

Now look at that starting pair and ask which post is actually limiting you. If you keep
both and move inward from either side, what happens to the width? What would have to
happen to the height for the trade to be worth it?

</details>

<details><summary><b>Hint 2</b></summary>

The capacity is capped by the shorter of the two walls, so the taller one is currently
doing nothing — lowering it would change nothing until it dropped below the other.

Consider every remaining pair that still uses that shorter wall. All of them are
narrower than the current pair, and none of them can be taller than the shorter wall,
because that wall caps them too. So every one of them has capacity at or below what you
have already recorded.

That means the shorter wall cannot appear in any *better* pair than the one you just
measured, and can be discarded outright — not just skipped, but eliminated from all
future consideration.

</details>

<details><summary><b>Hint 3</b></summary>

Put one marker at each end and keep a running best. At each step, measure the pair the
two markers describe, then move the marker sitting on the shorter post one step inward.
When the two heights are equal, either marker may move — the argument above applies to
both. Stop when the markers meet.

Every step permanently removes one post from consideration, so there are at most `n`
steps and nothing needs to be stored.

Be careful to measure the current pair *before* moving a marker, and note that the
width is the gap between the two positions, not the number of posts between them.

</details>
