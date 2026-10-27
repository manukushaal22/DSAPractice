# L02.6 — Skyline Rainfall

**Difficulty:** Hard
**Topics:** Two Pointers, Running Maxima
**Track:** [02 Two Pointers](../README.md) · rung .6 of 6 (stretch, optional)

## Problem

A skyline is drawn as a row of buildings, each one unit wide. `heights[i]` is the
height of building `i`, and the buildings stand side by side with no gaps. A height of
`0` is an empty lot.

After heavy rain, water settles on top of the skyline. It can collect in any dip
between taller buildings, and runs off both open ends of the row. Return the **total
amount of water** held, in square units.

## Examples

**Example 1**

```
Input:  heights = [5, 1, 3, 0, 4]
Output: 8
```

Explanation: the outer buildings are 5 and 4, so water between them can rise to height
4. Above the 1 that is 3 units, above the 3 it is 1 unit, and above the empty lot it is
4 units: `3 + 1 + 4 = 8`.

```
#
#~~~#
#~#~#
#~#~#
###~#
```

(`#` is building, `~` is water.)

**Example 2**

```
Input:  heights = [2, 0, 2]
Output: 2
```

Explanation: two buildings of height 2 with an empty lot between them hold 2 units.

**Example 3**

```
Input:  heights = [1, 2, 3, 2, 1]
Output: 0
```

Explanation: the skyline rises and then falls, so every drop of rain runs off an end.

## Constraints

- `0 <= len(heights) <= 1_000_000`
- `0 <= heights[i] <= 100_000`
- Do not modify `heights`

## Your task

Implement `trapped_water(heights: List[int]) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py L2.6
```

## Target complexity

**O(n) time, O(1) extra space.**

This rules out finding the walls separately for every building: scanning left and
right from each one is O(n²), and the perf cases cut it off.

The standard O(n) answer stores, for every position, the tallest building to its left
and to its right. That is two extra lists of length `n`. A stack-based method is also
O(n) time, but its stack can hold every building. Both are good first answers in an
interview. Here they exceed the perf cases' **2 MB** memory budget and get an `MLE`.
The rung is about removing that memory.

<details><summary><b>Hint 1</b></summary>

Look at one building in isolation. How high can the water above it rise? It depends on
exactly two numbers, and neither of them is a height of an adjacent building.

</details>

<details><summary><b>Hint 2</b></summary>

Water above building `i` rises to `min(tallest on the left, tallest on the right)`, and
the building occupies `heights[i]` of that. Two arrays of maxima make it O(n) time.

To drop the arrays, notice that you only need the **smaller** of the two maxima. Walk
in from both ends while keeping the tallest building seen so far from each side. If the
left side's tallest so far is lower than the right side's tallest so far, what do you
know about the building at the left pointer, even though you have not seen everything
to its right?

</details>

<details><summary><b>Hint 3</b></summary>

If the left running maximum is no taller than the right running maximum, then the true
tallest building to the right of the left pointer is **at least** the right running
maximum. So the left running maximum is the smaller wall, and the water at the left
pointer is decided. Add it and move the left pointer inward. The mirror case does the
same on the right.

Update each running maximum **before** using it, so a building taller than everything
before it holds zero water rather than a negative amount.

</details>
