# 03 — Sliding Window

**Phase:** Linear basics · **Needs:** 01, 02 · **Starts at:** rung .3
**Related drill:** [p002](../../problems/p002-longest-substring-without-repeating-characters/README.md),
[p001](../../problems/p001-best-time-to-buy-and-sell-stock/README.md)

> **Placement.** In p002 you wrote a variable-size window with a last-seen index map,
> at O(n), on the first attempt, so this topic starts at rung .3. Rungs .1 and .2
> (fixed-size windows) are available on request.

## Why it matters

"Longest / shortest / count of **contiguous** stretches with some property" is one of
the most common interview shapes, and the brute force is always "try every start, try
every end": O(n²) windows, often O(n³) once each window is checked. A sliding window
does it in **O(n)**: each element enters the window once and leaves it once.

It combines the previous two topics. The window's edges are two pointers moving in the
**same** direction (topic 02). The window's contents are summarised in a counter or map
(topic 01), so you never re-scan the window.

## The mental model

> **Keep a window `[left, right]` that always satisfies the rule. Grow it on the right
> one element at a time; when the new element breaks the rule, shrink it from the left
> until the rule holds again.**

The invariant:

> *After processing `right`, the window `[left, right]` is valid, and `left` is the
> smallest start for which it is valid.* (For "longest" problems.)

That last clause is what makes it correct: for each end `right`, you have found the
longest valid window ending there, so the best over all `right` is the answer. And it
is what makes it fast: `left` never moves back, so the total work is O(n).

The technique only works when the rule is **monotone**: if a window is valid, every
window inside it is valid too (or, for "shortest" problems, every window containing it).
That is what lets you shrink from the left without missing anything.

## Python toolkit

| Need | Tool | Notes |
| --- | --- | --- |
| Window contents by value | `collections.Counter` / `dict` | Update on enter and leave: O(1) each. Delete a key when its count hits 0 if you use `len(...)` |
| Small fixed alphabet | `counts = [0] * 26` with `ord(ch) - ord("A")` | Faster than a dict in CPython |
| Last position of each value | `dict` value → index | Lets `left` jump instead of crawl (p002) |
| Window sum | running integer | `total += x` on enter, `total -= nums[left]` on leave |
| Length | `right - left + 1` | Inclusive ends. Pick one convention and keep it |
| Avoid | `s[left:right + 1]`, `sum(nums[left:right + 1])`, `Counter(window)` inside the loop | Each re-scans the window: O(n²) |

## Recognition cues

- **Contiguous** (subarray, substring, consecutive days) **plus** longest / shortest /
  number of → sliding window, unless the rule is not monotone.
- "At most k" of something (distinct values, replacements, zeros) → variable window,
  shrink while the count exceeds k.
- "Exactly k" → usually `atMost(k) - atMost(k - 1)`. A single window cannot track
  "exactly" monotonically.
- Fixed length L → fixed window: add the entering element, remove the leaving one.
- Negative numbers with a **sum** rule → the rule is **not** monotone (adding an element
  can lower the sum). Sliding window fails; think prefix sums (topic 04, and p008).

## Worked example: shortest stretch reaching a target

*This is not one of the exercises; it is here to be read in full.*

> Given a list of **positive** integers `nums` and a target `t`, return the length of
> the shortest contiguous stretch whose sum is at least `t`, or 0 if there is none.

**Brute force.** Every start, every end: O(n²) with a running sum, O(n³) without.

**Why a window works.** All values are positive, so lengthening a stretch only increases
its sum, and shortening it only decreases it. The rule "sum ≥ t" is monotone: if a
window satisfies it, every window containing it does too. So for each end `right`, once
the window's sum reaches `t`, shrink from the left as far as it stays ≥ t. That gives the
shortest valid window ending at `right`.

```python
def shortest_reaching(nums: list[int], t: int) -> int:
    best = len(nums) + 1                 # sentinel: "nothing found yet"
    total = left = 0
    for right, value in enumerate(nums):
        total += value                   # 1. grow on the right
        while total >= t:                # 2. valid: record, then try to shrink
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return best if best <= len(nums) else 0
```

Trace with `nums = [2, 3, 1, 2, 4, 3]`, `t = 7`:

| right | value | total after add | shrinking | best |
| --- | --- | --- | --- | --- |
| 0 | 2 | 2 | — | — |
| 1 | 3 | 5 | — | — |
| 2 | 1 | 6 | — | — |
| 3 | 2 | 8 | [0..3] len 4 → drop 2, total 6 | 4 |
| 4 | 4 | 10 | [1..4] len 4 → drop 3 → [2..4] len 3 → drop 1, total 6 | 3 |
| 5 | 3 | 9 | [3..5] len 3 → drop 2 → [4..5] len 2 → drop 4, total 3 | 2 |

Why each detail is there:

- **Record inside the `while`, before shrinking.** The window is valid at that moment.
  Recording after the loop would see an invalid window.
- **`while`, not `if`.** One new element can make several left elements unnecessary
  (right = 4 drops two).
- **O(n) despite the nested loop.** `left` only moves forward and never passes `n`, so
  the inner loop runs at most `n` times **in total**, not per `right`.
- **Sentinel instead of a guard.** `best = n + 1` means "not found" without special-casing
  empty input or an unreachable target.

O(n) time, O(1) space.

## Variants you will meet

| Shape | Window state | Shrink when | Answer recorded |
| --- | --- | --- | --- |
| Fixed size L | sum / counts | always, once size exceeds L | after each step once size is L |
| Longest, "at most k" | counts / number of bad elements | rule broken | after shrinking (window valid) |
| Shortest, "at least" | sum / counts | while still valid | inside the shrink loop |
| Count of windows, "at most k" | counts | rule broken | add `right - left + 1` each step |
| "Exactly k" | — | — | `atMost(k) - atMost(k - 1)` |
| Last-seen jump (p002) | value → last index | duplicate inside window | `left` jumps to `last[x] + 1` |

## Pitfalls

- **Slicing or re-counting the window inside the loop.** `Counter(s[left:right + 1])` or
  `sum(nums[left:right + 1])` turns O(n) into O(n²). The whole point is to update the
  summary by one element at a time.
- **Off-by-one in the length.** With inclusive `[left, right]` it is `right - left + 1`.
  Mixing conventions within one solution is the usual source of wrong answers.
- **`if` where `while` is needed** (or the reverse). Some formulations shrink at most one
  step per iteration on purpose; know which one you are writing.
- **Non-monotone rules.** Sums with negative numbers, "exactly k", "the window's median":
  shrinking can skip the answer. Check monotonicity before reaching for a window.
- **Stale entries.** In a `dict` of counts, a key with count 0 still counts towards
  `len(counts)`. Delete it, or track the number of distinct values separately.
- **From your own history:**
  - *Seeding the window before the loop* (**p002**, then p005, p009, p014, L02.5, L02.6).
    In p002 you started with `window = {s[0]: 0}`, `j = 1`, which then needed the
    `len(s) < 2` guard. A window that starts empty (`left = 0`, nothing added) and grows
    in the loop handles every input size with no guard. This is the topic where that
    habit costs the most, because every window problem starts from an empty window.
  - *Fix-ups after the loop* (L02.5's `if lo == hi`). If you need to "also check the last
    window" after the loop, the recording step is in the wrong place inside it.

## Complexity cheat sheet

| Pattern | Time | Extra space |
| --- | --- | --- |
| Fixed or variable window, O(1) update | O(n) | O(1) |
| Window with a counter over an alphabet of size Σ | O(n) | O(Σ) |
| Same, but recomputing `max(counts)` each step | O(n·Σ) | O(Σ) |
| "Exactly k" via two "at most" passes | O(n) | O(Σ) |
| Brute force over all windows | O(n²) to O(n³) | O(1) |

## Self-check

<details><summary><b>The worked example has a <code>while</code> inside a <code>for</code>. Why is it O(n) and not O(n²)?</b></summary>

Count moves of `left` over the whole run, not per iteration. `left` starts at 0, only
increases, and never exceeds `n`, so the inner loop's body runs at most `n` times in
total. The outer loop runs `n` times. Together: O(n).

</details>

<details><summary><b>Why does the worked example fail if <code>nums</code> may contain negative numbers?</b></summary>

Shrinking assumes that removing an element from the left lowers the sum. With negatives,
removing one can *raise* it, so a shorter valid window might exist that the shrinking
step already moved past. The rule is no longer monotone. Prefix sums with a sorted
structure or a deque (later topics) handle that case.

</details>

<details><summary><b>"Longest window with at most k distinct values": where do you record the answer, and why there?</b></summary>

After the shrinking step, at the end of each iteration. At that point the window is
valid and is the longest valid window ending at `right`. Recording before shrinking
could record an invalid window.

</details>

<details><summary><b>How do you count windows with <em>exactly</em> k distinct values?</b></summary>

`atMost(k) - atMost(k - 1)`. Windows with "at most k" form a monotone family; "exactly k"
does not. For each `right` in an "at most" pass, every start from `left` to `right` is
valid, which adds `right - left + 1` windows.

</details>

<details><summary><b>When is a fixed-size window the right tool instead of a variable one?</b></summary>

When the length is given ("every 7-day stretch", "k consecutive elements"). Then there
is no shrink decision: each step adds the element entering on the right and removes the
one leaving on the left.

</details>

## The ladder

| Rung | Exercise | Level | |
| --- | --- | --- | --- |
| .1 | Best fixed-size window sum | Easy | skipped by placement, ask if you want it |
| .2 | Fixed window with a running count | Easy | skipped by placement, ask if you want it |
| .3 | [Uniform Banner](03.3-uniform-banner/README.md) | Medium | solved |
| .4 | [Two-Compartment Courier](03.4-two-compartment-courier/README.md) | Medium | solved |
| .5 | [Shuffled Signature](03.5-shuffled-signature/README.md) | Medium | solved. **Topic complete** |
| .6 | [Shortest Collage Strip](03.6-shortest-collage-strip/README.md) | Hard | solved |
