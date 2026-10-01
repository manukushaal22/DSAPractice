# Progress

Cross-session memory. The agent updates this; statuses are `todo`, `solved`, `revisit`.

| #    | Problem | Difficulty | Topics | Status | Your complexity | Solved on |
| ---- | ------- | ---------- | ------ | ------ | --------------- | --------- |
| p001 | [Best Time to Buy and Sell Stock](problems/p001-best-time-to-buy-and-sell-stock/README.md) | Easy | Arrays, Greedy, Single Pass | **solved** — 14/14, target met | O(n) time / O(1) space ✅ | 2026-08-26 |
| p002 | [Longest Substring Without Repeating Characters](problems/p002-longest-substring-without-repeating-characters/README.md) | Medium | Strings, Sliding Window, Hash Map | **solved** — 15/15, target met | O(n) time / O(k) space ✅ | 2026-08-26 |
| p003 | [Daily Temperatures](problems/p003-daily-temperatures/README.md) | Medium | Arrays, Monotonic Stack | **solved** — 15/15, target met | O(n) amortised time / O(n) space ✅ | 2026-08-26 |
| p004 | [Minimum Processing Rate](problems/p004-minimum-processing-rate/README.md) | Medium | Binary Search on Answer, Arrays | **solved** — 15/15 on attempt 2, target met | O(n log M) time / O(n) space (target O(1)) | 2026-08-27 |
| p005 | [Merge Overlapping Intervals](problems/p005-merge-overlapping-intervals/README.md) | Medium | Sorting, Intervals, Sweep | **solved** — 15/15, target met | O(n log n) time / O(n) space ✅ (~10x constant factor) | 2026-08-28 |
| p006 | [Count Land Regions](problems/p006-count-land-regions/README.md) | Medium | Grids, BFS/DFS, Flood Fill, Connected Components | **revisit** — 10/15, not reviewed yet | — | — |
| p007 | [Fewest Coins for an Exact Amount](problems/p007-fewest-coins-exact-amount/README.md) | Medium | 1-D Dynamic Programming, Unbounded Knapsack | **solved** — 15/15, target met | O(amount·coins) time / O(amount) space ✅ | 2026-09-08 |
| p008 | [Subarrays With a Given Sum](problems/p008-subarrays-with-given-sum/README.md) | Medium | Prefix Sums, Hash Map Counting | **solved** — 15/15, target met | O(n) time / O(n) space ✅ (~1.8x constant factor) | 2026-09-09 |
| p009 | [Largest Container](problems/p009-largest-container/README.md) | Medium | Two Pointers, Greedy Exchange Argument | **solved** — 15/15, target met | O(n) time / O(1) space ✅ (up to 3.5x constant factor) | 2026-09-09 |
| p010 | [Longest Common Subsequence](problems/p010-longest-common-subsequence/README.md) | Medium | 2-D Dynamic Programming, Strings | **revisit** — 7/15, recurrence right, memo shared across calls + recursion depth | O(n·m) time / O(n·m) space (target O(min(n,m))) | — |
| p011 | [Running Median of a Stream](problems/p011-running-median-of-a-stream/README.md) | Medium | Heaps / Priority Queues, Streaming, Invariant Maintenance | **revisit** — 13/15, heap ordering fails during initialization and between boundaries | O(n log n) time / O(n) space ✅ (correctness pending) | — |
| p012 | [Earliest Full Connection](problems/p012-earliest-full-connection/README.md) | Medium | Union-Find / Disjoint Set Union, Graphs, Sorting | **todo** | — | — |
| p013 | [Shortest Root Replacement](problems/p013-shortest-root-replacement/README.md) | Medium | Tries / Prefix Trees, Strings | **solved** — 14/14, target met | O(R + S) time / O(26·R) space (target O(R)) | 2026-09-29 |
| p014 | [Total XOR Over Every Subarray](problems/p014-total-xor-over-subarrays/README.md) | Medium | Bit Manipulation, Prefix XOR, Counting | **solved** — 15/15, time target met | O(n·B) time / O(n) space (target O(B)) | 2026-10-01 |

## Topics covered so far

- Arrays / greedy running-minimum (p001)
- Variable-size sliding window with last-seen index map (p002)
- Monotonic stack of pending indices (p003)
- Binary search on the answer space with a monotone predicate (p004)
- Sorting as a preprocessing step, then a single interval sweep (p005)
- Bottom-up 1-D DP, push/forward formulation with unreachable-state pruning (p007)
- Prefix sums paired with a hash map of previously-seen totals (p008)
- Two pointers converging from both ends, justified by a discard/exchange argument (p009)
- Character-indexed prefix tree, built once and walked per word, stopping at the first
  terminal marker (p013)
- Per-bit counting over prefix XORs: splitting a sum into independent bit positions and
  turning "sum over all pairs" into a product of two counts (p014)

## Recurring weak spots

- **Recomputing an aggregate from scratch inside a loop** (p001 attempt 1). The O(n²)
  smell: `max(prices[i+1:])` re-derives a suffix maximum n times when consecutive
  iterations differ by one element. *Fixed in attempt 2.*
- **Materialising an array that is consumed in a single pass** (p001 attempt 2). Built a
  full suffix-max array, then read it once. Fusing the loops collapses it to a scalar:
  O(n) space → O(1). Watch for this in DP (table vs. rolling state). *Fixed in attempt 3;
  recurred in p008 (prefix array built then walked once — constant-factor cost only there,
  since the hash map is already O(n), but the same habit). Recurred in p014, where it
  costs real complexity: the prefix array is built so it can be shifted 31 times, but the
  per-bit counters are the only state carried forward — O(n) space against an O(1) target.*
- **Stale guards after a rewrite.** `len(prices) < 2` went load-bearing → dead →
  load-bearing-for-a-different-reason across three rewrites, unchanged each time.
  Re-answer "what does this guard defend against?" whenever the body changes.

- **Special-casing the first element, which then forces a boundary guard** (p002). Pre-seeding
  `window = {s[0]: 0}` and starting at index 1 is what made `len(s) < 2` necessary; starting
  from an empty state removes both. Same guard habit as p001 — now the second data point.
  *Avoided in p003/p004/p007/p008; returned in p005 and p009.* Four occurrences. The tell
  is always the same: something is computed **before** the loop, and the guard exists to
  make that pre-computation safe. Fix the ordering, not the guard. *Fifth occurrence in
  p014: `if not nums: return 0` is dead — the empty list already falls straight through
  the `while` and returns 0.*
- **Misleading variable names causing the actual defect** (p002 `window` → dead `del`;
  p003 stack of tuples; p004 `r` meaning both "right bound" and "rate" → `ceil(rate/size)`).
  Three problems running. Name the quantity, not the slot: `lo`/`hi`, `rate`, `size`.
  *Fourth occurrence in p013: `self.word` holds a boolean end-of-root flag, and
  `get_shortest_prefix` returns the whole word on its most common path.*
- **State that outlives the call it belongs to** (p010). `def dp(..., hm={})` binds one dict
  at definition time, shared by every invocation for the life of the process, and the key
  `(ai, bi)` says nothing about *which* strings it describes. Per-call scratch space must be
  created per call. Same family as the p001/p002 guard habit: ask what the lifetime of each
  piece of state actually is.

## Strengths demonstrated

- Handles the strict buy-before-sell ordering correctly without prompting (the read-then-
  update ordering in the fused sweep).
- Iterates on feedback fast and arrives at the optimal form independently once pointed at
  the right idea.
- Chose a push/forward DP over the pull formulation in p007 and got the "all writes to i
  happen before i is read" argument right unprompted — and the unreachable-skip made it
  2.3x faster than the pull reference on sparse inputs.
- Wrote an adaptive termination in p014 (`while` the prefixes are not all zero) rather than
  hardcoding 31 bit positions, which makes it 3x faster than the reference on narrow
  values. Same instinct as the p007 unreachable-skip: let the data bound the work.

## Topics still untouched

Linked lists · Trees & DFS/BFS ·
Backtracking
