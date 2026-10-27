# L02.4 — Loading Dock Lanes

**Difficulty:** Medium
**Topics:** Two Pointers, In-place Partitioning
**Track:** [02 Two Pointers](../README.md) · rung .4 of 6 (disguised)

## Problem

Parcels arrive at a loading dock as a list of weights. The dock has a **reference
weight**, and the parcels have to be arranged into three lanes, front to back:

1. every parcel **lighter** than the reference
2. every parcel **exactly** the reference weight
3. every parcel **heavier** than the reference

Rearrange `weights` **in place** into that order and return the same list. Inside each
lane, parcels may be in any order. Any lane may be empty; the reference weight need not
appear at all.

The dock has almost no floor space. Apart from the list itself, you may only use a
few variables.

## Examples

**Example 1**

```
Input:  weights = [5, 2, 8, 5, 1, 9, 5], reference = 5
Output: [2, 1, 5, 5, 5, 8, 9]
```

Explanation: `2` and `1` are lighter, the three `5`s are exactly the reference, and `8`
and `9` are heavier. `[1, 2, 5, 5, 5, 9, 8]` would be equally correct.

**Example 2**

```
Input:  weights = [7, 3, 9, 1], reference = 4
Output: [3, 1, 7, 9]
```

Explanation: nothing weighs exactly 4, so the middle lane is empty.

**Example 3**

```
Input:  weights = [6, 6, 6], reference = 6
Output: [6, 6, 6]
```

Explanation: everything belongs in the middle lane.

## Constraints

- `0 <= len(weights) <= 1_000_000`
- `-10^9 <= weights[i], reference <= 10^9` (the dock's scale has an offset, so negative
  readings happen)
- Rearrange `weights` itself and return it
- **O(1) extra space**: no second list, no sorting

## Your task

Implement `arrange_lanes(weights: List[int], reference: int) -> List[int]` in
`solution.py`.

Run the tests from the repo root with:

```powershell
py run.py L2.4
```

## Target complexity

**O(n) time, O(1) extra space.** One pass over the list is possible.

The perf cases use a million parcels with a **1 MB** memory budget. Moving elements
around inside the list allocates nothing, but a helper list (three lane lists joined at
the end, a sorted copy, a `key=` list) costs several MB and gets an `MLE`. Moving
parcels with `pop` / `insert` / `remove` in a loop is O(n²) and gets a `TLE`.

A plain `weights.sort()` **slips past the tests**. It runs as a single C call that blocks
the memory sampler, and in C it is about as fast as a Python loop. It is still O(n log n)
and uses a scratch buffer, and the constraints forbid it. The review will check.

<details><summary><b>Hint 1</b></summary>

Picture the list partway through a solution. Some parcels have already been put in
their lane, and some have not been looked at yet. How many separate regions does the
list have at that moment, and where could each one sit?

</details>

<details><summary><b>Hint 2</b></summary>

Four regions are enough: *lighter (done)*, *reference (done)*, *not yet examined*,
*heavier (done)*. The unexamined region sits between the reference lane and the heavy
lane. Track the three boundaries between the regions with three indices.

Each step looks at the **first** unexamined parcel, and that parcel joins one region.
The unexamined region shrinks by exactly one parcel per step, which gives O(n).

</details>

<details><summary><b>Hint 3</b></summary>

For the first unexamined parcel:

- **lighter:** swap it to the end of the light lane, and move both the light boundary
  and the scan forward. The parcel that comes back from the swap has already been
  examined.
- **reference:** it is already in place, so move the scan forward.
- **heavier:** swap it with the **last** unexamined parcel and move the heavy boundary
  back. Do **not** move the scan forward: the parcel that just arrived has not been
  examined yet.

Stop when the unexamined region is empty. Check whether your loop condition still
examines the very last unexamined parcel.

</details>
