# 04 — Prefix Sums & Difference Arrays

**Phase:** Linear basics · **Needs:** 01 · **Starts at:** rung .3
**Related drill:** [p008](../../problems/p008-subarrays-with-given-sum/README.md),
[p014](../../problems/p014-total-xor-over-subarrays/README.md)

> **Placement.** In p008 you paired a running prefix sum with a map of earlier totals at
> O(n), and in p014 you used prefix XORs with per-bit counts. Both were first-attempt
> solves, so this topic starts at rung .3. Rungs .1 (range-sum queries) and .2 (balance
> index) are available on request.

## Why it matters

Many interview problems ask about the **sum of a range**: one range, millions of ranges,
every range, or every range with some property. Summing each range from scratch is
O(n) per range. With O(n) of precomputation, a prefix-sum table answers each range in
**O(1)**, and paired with a hash map it counts or finds qualifying ranges in one pass.

Its mirror image, the **difference array**, handles the opposite workload: many
"add v to every element in [l, r]" updates followed by reads. Each update costs O(1)
instead of O(r − l + 1).

It is also the fallback when a sliding window (topic 03) breaks. With negative numbers,
a sum rule isn't monotone, so a window can't shrink safely. A prefix sum doesn't care
about the sign.

## The mental model

> **Store the running total of the first i elements. Any range is the difference of two
> running totals.**

Define `P[0] = 0` and `P[i + 1] = P[i] + nums[i]`, so `P[i]` is the sum of the first `i`
elements and `P` has `n + 1` entries. Then

> `sum(nums[l..r]) = P[r + 1] − P[l]` (both ends inclusive)

The invariant is *`P[i]` is the sum of the **half-open** range `[0, i)`*. The extra
`P[0] = 0` is the empty prefix. It is a real prefix, not a special case, and it is what
makes ranges starting at index 0 work with the same formula.

Two consequences carry the whole topic:

- **"Sum of a range equals k" becomes "two prefixes differ by k".** Scanning left to
  right, a range ending at `j` has sum `k` exactly when some earlier prefix equals
  `P[j + 1] − k`. A hash map of earlier prefixes answers that in O(1) (p008).
- **Prefix and difference are inverses.** If `D[i] = A[i] − A[i − 1]`, then the prefix
  sums of `D` rebuild `A`. Adding `v` to `A[l..r]` changes only two entries of `D`:
  `D[l] += v` and `D[r + 1] −= v`. Do all the updates on `D`, then take one prefix
  pass to read `A`.

Anything you can **undo** works the same way: sums (undo with −), XOR (undo with XOR,
p014), counts, and products when no zeros are involved. `max` and `min` cannot be undone,
so prefix maxima cannot answer "max of an arbitrary range".

## Python toolkit

| Need | Tool | Notes |
| --- | --- | --- |
| Prefix table | `list(itertools.accumulate(nums, initial=0))` | `n + 1` entries, built in C. `initial=` needs 3.8+ |
| Other operations | `accumulate(nums, operator.xor, initial=0)` | Any binary function |
| Each prefix used once, in order | a running integer | No table needed. O(1) space |
| Earlier prefixes → count / first index | `dict`, `defaultdict(int)` | Seed with the empty prefix: `{0: 1}` or `{0: -1}` |
| 2-D table | `[[0] * (C + 1) for _ in range(R + 1)]` | **Not** `[[0] * (C + 1)] * (R + 1)`, which repeats one row object |
| Positive values, "first prefix ≥ x" | `bisect.bisect_left(P, x)` | `P` is sorted only when every value is ≥ 0 |
| Avoid | `sum(nums[l:r + 1])` per query | O(n) copy plus O(n) sum, every time |

## Recognition cues

- Many **range-sum queries** on data that doesn't change → prefix table.
- "Number of subarrays / longest subarray with sum k (or XOR k, or sum divisible by k)"
  → running prefix + hash map of earlier prefixes.
- Contiguous + sum rule + **negative numbers allowed** → prefix sums, not a window.
- "Add v to every element in a range", many times, then report the final state
  (bookings, schedules, paint, overlapping intervals counted per point) → difference
  array.
- "For each position, combine everything to its left and everything to its right"
  → a prefix pass and a suffix pass (worked example below).
- A grid with rectangle queries → the 2-D version of the same idea.

## Worked example: product of all other elements

*This is not one of the exercises; it is here to be read in full.*

> Given a list of integers `nums`, return a list `out` where `out[i]` is the product of
> every element **except** `nums[i]`. Do not use division. Use O(1) extra space besides
> the output.

**Brute force.** For each `i`, multiply the other n − 1 values: O(n²).

**Why not divide?** Multiply everything once and divide by `nums[i]`. It fails on
zeros: one zero makes every other answer 0 but needs special handling at its own index,
and two zeros make everything 0. The prefix/suffix route has no special cases.

**The idea.** `out[i]` = (product of everything **before** `i`) × (product of everything
**after** `i`). Both are running products: a prefix pass left to right and a suffix pass
right to left. The suffix pass can multiply straight into `out`, so the only extra
storage is two integers.

```python
def product_of_others(nums: list[int]) -> list[int]:
    out = [1] * len(nums)
    before = 1                              # product of nums[0 .. i-1]
    for i, value in enumerate(nums):
        out[i] = before                     # write first: exclude nums[i] itself
        before *= value
    after = 1                               # product of nums[i+1 .. n-1]
    for i in range(len(nums) - 1, -1, -1):
        out[i] *= after
        after *= nums[i]
    return out
```

Trace with `nums = [2, 3, 0, 4]`:

| pass | i | running product **before** this step | `out` after this step |
| --- | --- | --- | --- |
| forward | 0 | before = 1 | [1, 1, 1, 1] |
| forward | 1 | before = 2 | [1, 2, 1, 1] |
| forward | 2 | before = 6 | [1, 2, 6, 1] |
| forward | 3 | before = 0 | [1, 2, 6, 0] |
| backward | 3 | after = 1 | [1, 2, 6, 0] |
| backward | 2 | after = 4 | [1, 2, 24, 0] |
| backward | 1 | after = 0 | [1, 0, 24, 0] |
| backward | 0 | after = 0 | [0, 0, 24, 0] |

Why each detail is there:

- **Write, then multiply.** `out[i] = before` happens before `before *= value`, so
  `before` is the **exclusive** prefix: everything strictly left of `i`. Swapping the two
  lines includes `nums[i]` in its own answer.
- **Start both runs at 1, the empty product.** That's what makes index 0 (nothing
  before it) and index n − 1 (nothing after it) correct without a branch. It's the same
  role `P[0] = 0` plays for sums.
- **No suffix array.** A suffix-product list would be built and then read once, in
  order. A running scalar carries the same information, so the extra space drops from
  O(n) to O(1).
- **Empty input** gives `[]`. Both loops run zero times, so there's no guard.

O(n) time, O(1) extra space besides the output.

## Variants you will meet

| Shape | Precompute | Per query / step | Seen in |
| --- | --- | --- | --- |
| Range sum, static array | `P`, n + 1 entries | `P[r + 1] − P[l]` | rung .1 |
| Rectangle sum on a grid | 2-D prefix table, (R + 1) × (C + 1) | a few corner lookups | rung .3 |
| Count subarrays with sum k | running prefix, map prefix → count | `count[P − k]` | p008 |
| Longest subarray with sum k | running prefix, map prefix → **first** index | `j − first[P − k]` | |
| Sum divisible by k | map `P mod k` → count | `count[P mod k]` | |
| Range XOR / any undoable operation | prefix XOR | `P[r + 1] ^ P[l]` | p014 |
| Many range updates, read at the end | difference array, n + 1 entries | `D[l] += v; D[r + 1] −= v`, one prefix pass | |
| Everything except position i | prefix pass + suffix pass | — | worked example |

## Pitfalls

- **Off-by-one between inclusive and half-open.** With `P` of length n + 1, the range
  `[l, r]` inclusive is `P[r + 1] − P[l]`. Write the definition of `P[i]` in a comment
  and check it on a one-element range.
- **Forgetting the empty prefix.** In the hash-map variants, the map must start with the
  empty prefix (`{0: 1}` for counts, `{0: -1}` for first index). Without it, every
  qualifying range that starts at index 0 is missed.
- **Insert before querying.** Look up `P − k` *before* adding the current `P` to the map.
  Otherwise, with `k = 0`, the current prefix matches itself and counts an empty range.
- **Difference array one slot short.** `D[r + 1]` with `r = n − 1` needs `D` of length
  n + 1.
- **Prefix of something you can't undo.** Prefix maxima cannot give the max of `[l, r]`.
  That needs a sparse table or a segment tree (later topics).
- **Aliased 2-D rows.** `[[0] * C] * R` is R references to one list. Writing one cell
  writes the whole column.
- **Prefixing the input in place** (`nums[i] += nums[i - 1]`) when the caller still needs
  `nums`. It saves memory only if the problem allows it.
- **From your own history:**
  - *Materialising a table that is read once in order* (p008, p014, and p001 before it).
    In p008 you built the full prefix list and then walked it once; in p014 you kept an
    O(n) prefix array when per-bit counters were all that carried forward. Build a table
    only when you need **random access** to old prefixes (range queries). For a single
    left-to-right scan, keep a running scalar. The worked example's suffix pass is the
    same move.
  - *Seeding before the loop* (p002 and seven more). The empty prefix `P[0] = 0`, or
    `{0: 1}` in the map, is **not** that habit. It's the correct state for "nothing
    processed yet", and it removes boundary cases instead of creating them. Seeding with
    `nums[0]` and starting the loop at 1 is still the habit.
  - *Recomputing an aggregate from scratch inside a loop* (p001). `sum(nums[l:r + 1])`
    per query is the same smell; prefix sums are the standard cure.

## Complexity cheat sheet

| Pattern | Precompute | Per query | Extra space |
| --- | --- | --- | --- |
| 1-D range sum | O(n) | O(1) | O(n) |
| 2-D rectangle sum | O(R·C) | O(1) | O(R·C) |
| Prefix + hash map, one pass | — | O(1) per element | O(n) for the map |
| Running prefix only, one pass | — | O(1) per element | O(1) |
| Difference array, U updates then one read-out | O(n) | O(1) per update | O(n) |
| Summing each range from scratch | — | O(range length) | O(1) |

## Self-check

<details><summary><b>Why does <code>P</code> have n + 1 entries, and what is <code>P[0]</code> for?</b></summary>

`P[i]` is the sum of the first `i` elements, for `i` from 0 to n, which is n + 1 values.
`P[0] = 0` is the sum of no elements. It lets `sum(nums[0..r]) = P[r + 1] − P[0]` use
the same formula as every other range, with no special case for ranges at the start.

</details>

<details><summary><b>Prefix XOR works for "XOR of a range". Why can't a prefix maximum give "max of a range"?</b></summary>

`P[r + 1] − P[l]` works because subtraction undoes addition, and XOR undoes itself. There
is no operation that removes `max(nums[0..l−1])` from `max(nums[0..r])`. Once a large
value has been absorbed, the information about the smaller ones is gone.

</details>

<details><summary><b>Counting subarrays with sum k, you seed the map with <code>{0: 1}</code>. Isn't that the "seeding before the loop" habit?</b></summary>

No. The habit is pre-processing the **first element** outside the loop, which then
needs a guard for inputs too small to have one. `{0: 1}` records the **empty prefix**,
which exists for every input including the empty one. It *removes* the boundary case
(subarrays starting at index 0) instead of creating one.

</details>

<details><summary><b>A sum rule over contiguous ranges: when do you need prefix sums instead of a sliding window?</b></summary>

When values can be negative (or zero, for some rules). Then extending a range can lower
its sum, so the rule isn't monotone and a window can't shrink safely. Prefix sums don't
rely on monotonicity: they compare every pair of prefixes, using a hash map so it stays
O(n).

</details>

<details><summary><b>Range updates and point reads arrive interleaved, not all updates first. Does a difference array still work?</b></summary>

Not efficiently. Reading `A[i]` from `D` is a prefix sum over `D[0..i]`, which is O(n) if
you redo it after every update. Interleaved updates and queries need a Fenwick tree or a
segment tree, at O(log n) each (later topics).

</details>

## The ladder

| Rung | Exercise | Level | |
| --- | --- | --- | --- |
| .1 | Range-sum queries | Easy | skipped by placement, ask if you want it |
| .2 | Balance index | Easy | skipped by placement, ask if you want it |
| .3 | [Farm Plot Ledger](04.3-farm-plot-ledger/README.md) | Medium | **start here** |
| .4 | Range-increment bookings | Medium | |
| .5 | Longest stretch with equal 0s and 1s | Medium | |
| .6 | Submatrices summing to a target | Hard | optional |
