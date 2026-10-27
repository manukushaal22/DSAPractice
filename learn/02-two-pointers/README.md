# 02 — Two Pointers

**Phase:** Linear basics · **Needs:** 01 · **Starts at:** rung .3
**Related drill:** [p009](../../problems/p009-largest-container/README.md),
[p005](../../problems/p005-merge-overlapping-intervals/README.md)

> **Placement.** In p009 you solved the converging-pointer problem at the target
> complexity and justified the discard step yourself, so this topic starts at rung .3.
> Rungs .1 and .2 are available on request.

## Why it matters

Two pointers turn many O(n²) "look at every pair" searches into O(n) passes, with
**O(1) extra space**. That second part is what sets them apart from hashing. Topic 01
bought speed with memory. Two pointers usually buy it with **order**: either the input
is sorted, or you can sort it without losing what the question asks about.

Interviewers like this technique because the code is short and the correctness argument
is not. Expect "why is it safe to move that pointer?" as a follow-up, and have an answer
ready.

## The mental model

> **Two indices that each move only one way. Every move permanently rules something
> out.**

Neither pointer ever goes back, so together they make at most about `n` moves. That is
where O(n) comes from. Everything else is about one question: **what does each move rule
out, and why is that safe?**

The invariant depends on the family (see Variants below), but it always has this shape:

> *Everything outside the pointers is settled: it is either already accounted for, or
> provably unable to contribute to a better answer.*

For converging pointers it reads: *every candidate that could still beat the best answer
lies entirely inside `[lo, hi]`.* That is exactly the argument you made in p009.

## Python toolkit

| Need | Tool | Notes |
| --- | --- | --- |
| Pointers that move independently | `while lo < hi:` with explicit `lo += 1` / `hi -= 1` | A `for` loop only moves one index |
| Sort in place | `nums.sort()` | O(n log n), returns `None`. `sorted(nums)` allocates a copy |
| Sort but remember original positions | `sorted(range(n), key=nums.__getitem__)` | Sorting throws away indices. Carry them if the answer needs them |
| Swap | `a[i], a[j] = a[j], a[i]` | Right side is built first, so this is safe |
| Walk backwards | `range(n - 1, -1, -1)` | Or `reversed(range(n))` |
| Avoid | `nums[lo:hi]` in a loop, `del nums[i]` / `list.remove` in a loop | Slices copy O(k); deleting shifts O(n). Both turn O(n) into O(n²) |

## Recognition cues

- **Sorted input** (or sortable without harm) plus a question about **pairs**: a sum,
  a difference, a closest value → converging pointers.
- **"In place"** or **"O(1) extra space"** with filtering, deduplicating, or partitioning
  → a read pointer and a write pointer moving in the same direction.
- **Two sorted sequences** to merge, intersect, or compare → one pointer per sequence.
- **Palindromes / symmetry** → converging from both ends.
- An objective over **pairs of positions** where one side is clearly the bottleneck
  (p009's shorter wall) → converging pointers plus an exchange argument, even when the
  input is not sorted.
- A **k-tuple** version (triples, quadruples) of a pair problem → fix the outer items
  in loops and run two pointers on the rest. Expect O(n^(k-1)).

## Worked example: squares of a sorted list

*This is not one of the exercises; it is here to be read in full.*

> Given `nums` sorted in non-decreasing order (it may contain negatives), return the
> squares of its elements, also sorted in non-decreasing order.

**Obvious answer.** Square everything, then sort: O(n log n). It works, but it throws
away the fact that the input was already sorted.

**The observation.** Squaring breaks the order only because of negatives:
`[-4, -1, 0, 3, 10]` squares to `[16, 1, 0, 9, 100]`. In a sorted list, though, the
element with the **largest absolute value** is always at one of the two **ends**. So the
largest remaining square is always `nums[lo]²` or `nums[hi]²`. Take it, write it at the
**back** of the output, and move that pointer inward:

```python
def sorted_squares(nums: list[int]) -> list[int]:
    result = [0] * len(nums)
    lo, hi = 0, len(nums) - 1
    for write in range(len(nums) - 1, -1, -1):   # fill from the largest square down
        if abs(nums[lo]) > abs(nums[hi]):
            result[write] = nums[lo] * nums[lo]
            lo += 1
        else:
            result[write] = nums[hi] * nums[hi]
            hi -= 1
    return result
```

Trace with `nums = [-4, -1, 0, 3, 10]`:

| write | lo | hi | compare | writes | move |
| --- | --- | --- | --- | --- | --- |
| 4 | 0 (−4) | 4 (10) | 4 vs 10 | 100 | hi → 3 |
| 3 | 0 (−4) | 3 (3) | 4 vs 3 | 16 | lo → 1 |
| 2 | 1 (−1) | 3 (3) | 1 vs 3 | 9 | hi → 2 |
| 1 | 1 (−1) | 2 (0) | 1 vs 0 | 1 | lo → 2 |
| 0 | 2 (0) | 2 (0) | 0 vs 0 | 0 | hi → 1 |

Result: `[0, 1, 9, 16, 100]`.

Why each detail is there:

- **Why write from the back?** We always know the *largest* remaining square, because
  it is at an end. We do not know the smallest, which sits somewhere near the zero
  crossing. So the output is filled in the only order we can justify.
- **Why it is safe to move the pointer.** The element at that end has just been placed in
  its final slot and will never be needed again. That is the "every move settles
  something permanently" rule.
- **Loop control.** The loop runs exactly `n` times, once per output slot, so no
  `lo <= hi` bookkeeping is needed. On the last step `lo == hi`, and both branches do the
  right thing.
- **No empty-input guard.** With `n = 0` the `range` is empty, so `nums[lo]` is never
  read.

O(n) time, O(n) space for the output, which the problem requires. Extra space is O(1).

## Variants you will meet

| Family | Pointers | Invariant | Typical problems |
| --- | --- | --- | --- |
| **Converging** | `lo` from the left, `hi` from the right | Better answers lie only inside `[lo, hi]` | Pair with target in sorted data, palindromes, p009, trapped water |
| **k-sum reduction** | Loop over the first `k - 2` items, converging pair on the rest | As above, per fixed prefix | Triples or quadruples hitting a target |
| **Read / write** (same direction) | `read` scans everything, `write` marks the end of the kept prefix | `nums[:write]` is exactly the answer for `nums[:read]` | Remove values in place, dedupe a sorted list, move zeros |
| **Partition** | Three regions grown from both ends | Each region holds one class | Three-way partition (Dutch flag), quicksort partition |
| **Two sequences** | One pointer per sorted sequence | Everything behind both pointers has been merged | Merge, intersect, "is `a` a subsequence of `b`" |
| **Fast / slow** | Same start, different speeds | Comes in topic 07 | Cycle detection, middle of a linked list |

Sliding windows (topic 03) are a close relative: two same-direction pointers where the
**range between them** is the object of interest.

## Pitfalls

- **`lo < hi` vs `lo <= hi`.** Pairs need two different indices, so use `lo < hi`.
  Processing every element once, as in the worked example, may need `lo == hi` to be
  included. Decide which one applies before writing the loop.
- **Moving a pointer without a reason.** Every `lo += 1` must be backed by an argument
  that `nums[lo]` cannot be part of any *better* answer. If you cannot state it, the
  move is a guess. Moving *both* pointers needs a separate argument for each.
- **Duplicates.** Sorted input puts equal values next to each other. If the answer must
  be distinct *values*, you need to skip runs of equal values. Skip in the wrong place
  and you either print duplicates or wrongly forbid using two equal values together.
- **Sorting destroys positions.** If the question asks for indices, sort indices (see
  the toolkit) or use a hash map (topic 01) instead.
- **O(n²) hidden in "in place".** `del nums[i]`, `nums.remove(x)` and `nums.insert(0, x)`
  inside a loop each cost O(n). Use a write pointer and truncate once at the end.
- **From your own history:**
  - *A guard before the loop* (p001, p002, p005, **p009**, p014). In p009 you measured the
    first pair before the loop and again after every move inside it. A loop body that
    *measures, then moves* handles the first pair and the empty input without any
    code before the loop.
  - *Names describe the quantity* (p004's `r`). Use `lo` / `hi`, `read` / `write`, not
    `i` / `j` / `k` when three indices are in play.
  - *Dead branches* (L01.4's `raise Exception("Not possible")`). With two pointers the
    loop condition usually makes the "impossible" branch truly impossible, so leave it out.

## Complexity cheat sheet

| Pattern | Time | Extra space |
| --- | --- | --- |
| Converging pair on sorted input | O(n) | O(1) |
| Sort, then converging pair | O(n log n) | O(1) with `.sort()` in place* |
| k-sum by fixing `k - 2` items | O(n^(k-1)) | O(1) plus output |
| Read / write compaction | O(n) | O(1) |
| Merge two sorted lists | O(n + m) | O(n + m) for the output |

\* CPython's sort can allocate up to `n/2` slots of scratch space. Interviews still call
in-place sorting O(1), but say "plus the sort" if pressed.

## Self-check

<details><summary><b>Converging pointers on n elements: why at most n − 1 moves?</b></summary>

Each move shrinks the gap `hi − lo` by at least 1, the gap starts at `n − 1`, and the
loop stops when it reaches 0. Neither pointer ever moves back, so no position is
re-examined.

</details>

<details><summary><b>In the worked example, why is filling the output from the front not possible?</b></summary>

From the front you would need the *smallest* remaining square, which sits at the zero
crossing, somewhere in the middle and not at a pointer. The two ends only ever tell you
the largest. A two-pointer scheme fills the output in whichever order the pointers can
justify.

</details>

<details><summary><b>Two pointers or a hash set for "is there a pair summing to t"? What decides it?</b></summary>

Unsorted input, and positions needed in the answer: use a hash map, O(n) time and O(n)
space. Already sorted, or memory is tight: use two pointers, O(n) time (O(n log n) with
the sort) and O(1) space. Two pointers also list *all* pairs in sorted order, which makes
skipping duplicates easy.

</details>

<details><summary><b>Removing every 0 from a list in place: why is <code>del</code> in a loop O(n²), and what is O(n)?</b></summary>

Each `del` shifts every later element left by one. With k deletions that is O(k·n). A
`write` pointer instead copies each kept element forward exactly once, then a single
`del nums[write:]` truncates. Every element moves at most once: O(n).

</details>

<details><summary><b>When is sorting first the wrong move?</b></summary>

When the answer depends on the original **order** or **positions**: "the earliest
pair", "return indices", "subarray" (contiguous) questions. Also when a hash-based O(n)
solution exists and the sort's O(n log n) is the bottleneck.

</details>

## The ladder

| Rung | Exercise | Level | |
| --- | --- | --- | --- |
| .1 | Palindrome check skipping non-letters | Easy | skipped by placement, ask if you want it |
| .2 | Pair with a target sum in sorted input | Easy | skipped by placement, ask if you want it |
| .3 | [Balanced Trios](02.3-balanced-trios/README.md) | Medium | solved |
| .4 | [Loading Dock Lanes](02.4-loading-dock-lanes/README.md) | Medium | solved |
| .5 | [Rescue Rafts](02.5-rescue-rafts/README.md) | Medium | solved. **Topic complete** |
| .6 | [Skyline Rainfall](02.6-skyline-rainfall/README.md) | Hard | solved |
