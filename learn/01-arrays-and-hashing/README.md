# 01 — Arrays & Hashing

**Phase:** Linear basics · **Needs:** nothing · **Starts at:** rung .3
**Related drill:** [p001](../../problems/p001-best-time-to-buy-and-sell-stock/README.md),
[p002](../../problems/p002-longest-substring-without-repeating-characters/README.md),
[p008](../../problems/p008-subarrays-with-given-sum/README.md)

> **Placement.** In p001, p002 and p008 you already used single passes and dictionaries
> fluently, so this topic starts at rung .3. Rungs .1 and .2 are available on request.

## Why it matters

Hashing is the most common speed-up in interviews. Countless O(n²) brute-force answers
turn into O(n) once you see that the inner loop only answers a lookup question: *"have I
seen X?"*, *"how many X so far?"*, *"where was X?"*. A hash table answers each of those
in O(1) on average, so the inner loop disappears.

Almost every later topic relies on this: sliding windows keep counts in a map, prefix-sum
problems store earlier totals in a map, graph searches keep a visited set, and DP memoises
into a dict.

## The mental model

> **Spend memory to avoid repeating a search.** As you scan, record exactly the facts
> about the elements already seen that a future element will need to look up.

That gives the invariant behind nearly every hashing solution:

> *When processing element `i`, the table holds the needed facts about elements `0..i-1`,
> and nothing else.*

Get the **order** of "look up" and "record" right and most edge cases (an element pairing
with itself, duplicates) handle themselves, with no special-case guards.

## Python toolkit

| Need | Tool | Notes |
| --- | --- | --- |
| "Seen it?" | `set` | `x in s` is O(1) average. `x in some_list` is O(n), a classic hidden O(n²) |
| "How many?" | `collections.Counter` | `Counter(s)`; two `Counter`s compare with `==` |
| "Where / what was it?" | `dict` | `d.get(k, default)` reads without inserting |
| "Group these" | `collections.defaultdict(list)` | `groups[key].append(x)` |
| Composite key | `tuple` | `(r, c)`, `tuple(counts)`. Lists are unhashable |
| Order-free set key | `frozenset` | Ignores **multiplicity**, so it is often the wrong key |

Costs to keep in mind:

- Hashing a key of length `k` costs **O(k)**, not O(1). A table of `n` string keys of
  length `k` costs O(n·k) to fill.
- The O(1) figure is an **average**. Adversarial collisions can degrade a single operation
  to O(n). Interviews treat hash operations as O(1); say "average" when you state it.
- A `dict` keeps insertion order. Code that needs sorted order or "nearest key" needs a
  sorted structure or `bisect`, which come in later topics.

## Recognition cues

- The brute force is a nested loop whose inner loop **searches** for a partner or a
  previous occurrence → put what the inner loop searches for into a hash table.
- "Count", "frequency", "most common", "duplicates", "unique" → `Counter` or `set`.
- "Group", "bucket", "classify", "are these equivalent?" → a **canonical key** shared by
  exactly the equivalent items.
- Values bounded by `n`, or "O(1) extra space" alongside hashing-style questions → the
  array itself can act as the table (rung .6).

## Worked example: pair with a target sum

*This is not one of the exercises; it is here to be read in full.*

> Given an unsorted list `nums` and an integer `target`, return the indices `(i, j)`,
> `i < j`, of two **different** positions whose values sum to `target`. Exactly one such
> pair exists.

**Brute force.** Try every pair: O(n²) time, O(1) space.

**Sort + two pointers.** O(n log n), but sorting scrambles the indices, so you have to
carry them along. It works, but it is more complex than needed.

**Hashing.** Look at the brute force's inner loop. For a fixed `j`, it searches the
earlier positions for the value `target - nums[j]`. That is a lookup, so remember the
values already seen:

```python
def pair_with_sum(nums: list[int], target: int) -> tuple[int, int]:
    index_of: dict[int, int] = {}            # value -> an index where it was seen
    for j, value in enumerate(nums):
        i = index_of.get(target - value)     # 1. look up the partner among 0..j-1
        if i is not None:
            return i, j
        index_of[value] = j                  # 2. only then record this element
    raise ValueError("no pair")
```

Trace with `nums = [3, 3, 4]`, `target = 6`:

| j | value | needs | `index_of` before | result |
| --- | --- | --- | --- | --- |
| 0 | 3 | 3 | `{}` | not found, record `3 → 0` |
| 1 | 3 | 3 | `{3: 0}` | found at 0 → `(0, 1)` |

Why the order matters:

- **Look up before recording.** With the steps the other way round, `nums = [3]`,
  `target = 6` would pair index 0 with itself. The invariant ("the table holds only
  `0..j-1`") is what rules that out. No `i != j` guard is needed.
- **Duplicates come for free.** The second 3 finds the first because the first was
  recorded before the second was examined.
- **No empty-input guard.** An empty list never enters the loop.

O(n) time, O(n) space. The trade-off is explicit: n extra entries buy back a factor of n
in time.

## Variants you will meet

| Pattern | What the table stores | Typical question |
| --- | --- | --- |
| Membership | `set` of values | "Any duplicates?", "is the complement present?" |
| Counting | value → count | "Are these two the same multiset?", "majority element" |
| Index lookup | value → index | Pair / complement problems like the worked example |
| Canonical-key grouping | key → list of items | "Bucket items that are equivalent under some rule" |
| Bucketing by count | count → values (list indexed by count) | "Top-k by frequency" without sorting |
| Array as its own table | marks written into the input | O(1) extra space when values lie in `1..n` |

### Canonical keys, in general

To group items by an equivalence ("these two count as the same"), find a function `key`
such that:

> `key(a) == key(b)` **if and only if** `a` and `b` are equivalent.

Both directions matter. *Only if* stops unrelated items being merged. *If* stops related
items being split. Then grouping is one pass: `groups[key(item)].append(item)`.

An example that is not on the ladder: e-mail addresses where case does not matter and dots
in the local part are ignored. A suitable key lower-cases the address and deletes the dots
before the `@`. Then `A.Lice@x.com` and `alice@x.com` land in the same bucket, while
`alice@y.com` does not.

## Pitfalls

- **Unhashable keys.** `d[[1, 2]]` raises `TypeError`. Convert to `tuple(...)` first.
- **Ambiguous keys.** If you build a key by joining numbers into a string, use a separator.
  The counts `[1, 11]` and `[11, 1]` both join to `"111"`. A tuple never has this problem.
- **`frozenset` drops multiplicity.** `frozenset("aab") == frozenset("ab")`.
- **`defaultdict` inserts on read.** `if groups[k]:` creates `k`. Use `k in groups` or
  `groups.get(k)` when you only want to look.
- **`x in list` inside a loop** is O(n) per check, so the whole thing is quietly O(n²).
- **From your own history:**
  - *A guard before the loop* (p001, p002, p005, p009, p014). If you find yourself
    writing `if not words: return ...`, check whether starting from an empty table already
    handles it. It almost always does.
  - *State that outlives the call* (p010). `def f(xs, seen=set())` shares one set
    across every call. Create the table inside the function.
  - *Names describe the quantity.* `groups`, `index_of`, `count_of`, not `d`, `hm`,
    `res`.

## Complexity cheat sheet

| Operation | Average | Notes |
| --- | --- | --- |
| `set` / `dict` insert, lookup, delete | O(1) | Plus O(k) to hash a key of length `k` |
| Build `Counter` of `n` items | O(n) | |
| `sorted` on `k` items | O(k log k) | |
| `x in list`, `list.count`, `list.index` | O(n) | Avoid inside loops |
| `list.pop(0)`, `list.insert(0, x)` | O(n) | Use `collections.deque` |

## Self-check

<details><summary><b>Why does the worked example look up before it records?</b></summary>

So the table only ever holds earlier elements. Recording first would let an element pair
with itself when `2 * value == target`, and the fix would be an extra guard. Getting the
order right removes the need for the guard.

</details>

<details><summary><b>You compute a key as a Python list. What goes wrong, and what is the fix?</b></summary>

A list is mutable, so it is unhashable and `dict` rejects it with a `TypeError`. Convert
it with `tuple(...)`. If the list holds numbers, joining them into a string without
separators is **not** a safe fix, because different lists can then collide.

</details>

<details><summary><b>You build a key of length k for each of n strings. What does that cost overall?</b></summary>

At least O(n·k): every character is read once, and hashing the key reads it again. If
building the key sorts the characters, it is O(n·k log k). Either way, report it in terms
of both `n` and `k`.

</details>

<details><summary><b>"Any duplicates?" with a set versus by sorting: what is the trade-off?</b></summary>

Set: O(n) time, O(n) extra space. Sorting: O(n log n) time, O(1) extra space if you may
sort in place, but that mutates the input. If the problem forbids extra memory or modifying
the input, those constraints decide it.

</details>

<details><summary><b>When is a hash table the wrong tool?</b></summary>

When you need **order**: the smallest key, the next key above `x`, every key in a range.
A hash table cannot answer those faster than a full scan, so use sorting, `bisect`, a heap
or a balanced tree instead. It is also wrong when memory is the binding constraint.

</details>

## The ladder

| Rung | Exercise | Level | |
| --- | --- | --- | --- |
| .1 | Detect a duplicate | Easy | skipped by placement, ask if you want it |
| .2 | Same letters, different order | Easy | skipped by placement, ask if you want it |
| .3 | [Group Rearranged Words](01.3-group-rearranged-words/README.md) | Medium | solved |
| .4 | [On-Call Shortlist](01.4-on-call-shortlist/README.md) | Medium | solved |
| .5 | [Longest Unbroken Streak](01.5-longest-unbroken-streak/README.md) | Medium | solved. **Topic complete** |
| .6 | [Smallest Absent Ticket](01.6-smallest-absent-ticket/README.md) | Hard | solved |
