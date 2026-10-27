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
| p015 | [Longest Route in a Network](problems/p015-longest-route-in-a-network/README.md) | Medium | Trees, DFS/BFS, Post-order Aggregation | **todo** | — | — |

## Learning path

Roadmap, ladder rules and placement: [learn/README.md](learn/README.md). Statuses are
the same as above. A topic is complete when every rung from its start rung up to `.5` is
`solved`.

**Current topic:** 04 Prefix Sums & Difference Arrays (placed at rung .3) · **Completed topics:** 01 Arrays & Hashing (2026-10-08, incl. optional .6) · 02 Two Pointers (2026-10-13, incl. optional .6) · 03 Sliding Window (2026-10-16, incl. optional .6 on 2026-10-26)

| ID | Exercise | Difficulty | Rung | Status | Your complexity | Solved on |
| -- | -------- | ---------- | ---- | ------ | --------------- | --------- |
| L01.3 | [Group Rearranged Words](learn/01-arrays-and-hashing/01.3-group-rearranged-words/README.md) | Medium | .3 standard | **solved** — 14/14 on attempt 2 (attempt 1 returned a `dict_values` view) | O(n·k log k) time / O(n·k) space ✅ | 2026-10-08 |
| L01.4 | [On-Call Shortlist](learn/01-arrays-and-hashing/01.4-on-call-shortlist/README.md) | Medium | .4 disguised | **solved** — 13/13 on attempt 2 (attempt 1 sorted, O(d log d)) | O(n) time / O(n) space ✅ (read on a `defaultdict` inserts every empty count) | 2026-10-08 |
| L01.5 | [Longest Unbroken Streak](learn/01-arrays-and-hashing/01.5-longest-unbroken-streak/README.md) | Medium | .5 harder variant | **solved** — 15/15 first try, own approach (expand both ways + visited set) | O(n) time / O(n) space ✅ (second set doubles memory) | 2026-10-08 |
| L01.6 | [Smallest Absent Ticket](learn/01-arrays-and-hashing/01.6-smallest-absent-ticket/README.md) | Hard | .6 stretch (optional) | **solved** — 15/15 first try, cycle-following placement with value v at index v | O(n) time / O(1) extra ✅ except `append(0)`, which regrows the backing array (+1 MB at n = 1M) and changes the caller's list length | 2026-10-09 |
| L02.3 | [Balanced Trios](learn/02-two-pointers/02.3-balanced-trios/README.md) | Medium | .3 standard | **solved** — 15/15 first try; no outer duplicate skip, a `set` of trios removes the repeats afterwards | O(n²) time ✅ / extra O(T) for the set, T = number of trios (target O(1)) | 2026-10-12 |
| L02.4 | [Loading Dock Lanes](learn/02-two-pointers/02.4-loading-dock-lanes/README.md) | Medium | .4 disguised | **solved** — 16/16 on attempt 2; rewrote as one-pass three-region partition (attempt 1: two passes, infinite loop + unclassified meeting slot) | O(n) time / O(1) space ✅ | 2026-10-13 |
| L02.5 | [Rescue Rafts](learn/02-two-pointers/02.5-rescue-rafts/README.md) | Medium | .5 combined with 01 | **solved** — 16/16 first try, heaviest-with-lightest greedy (bonus O(n + limit) not attempted) | O(n log n) time / O(1) extra ✅ (post-loop `if lo == hi` patches a `<` that should be `<=`) | 2026-10-13 |
| L02.6 | [Skyline Rainfall](learn/02-two-pointers/02.6-skyline-rainfall/README.md) | Hard | .6 stretch (optional) | **solved** — 18/18 first try, converging running maxima (arrays version left commented out) | O(n) time / O(1) space ✅ (both maxima refreshed every step, ~1.7x constant) | 2026-10-13 |
| L03.3 | [Uniform Banner](learn/03-sliding-window/03.3-uniform-banner/README.md) | Medium | .3 standard | **solved** — attempt 2: one `for` + `while` shrink, empty start, no guard, no fix-up (attempt 1: three inner loops + seeded window) | O(26·n) time / O(1) space ✅ (`max(counts.values())` per pointer move; slowest case 0.53 s, was 1.2 s; never-lowered max-count bonus not taken) | 2026-10-16 |
| L03.4 | [Two-Compartment Courier](learn/03-sliding-window/03.4-two-compartment-courier/README.md) | Medium | .4 disguised | **solved** — 15/15 first try; recognised the window, count dict with delete-at-zero, empty start | O(n) time / O(1) space ✅ (dict ≤ 3 keys; slowest case 0.25 s vs 0.19 s reference; no-dict bonus not taken) | 2026-10-16 |
| L03.5 | [Shuffled Signature](learn/03-sliding-window/03.5-shuffled-signature/README.md) | Medium | .5 combined with 01 | **solved** — 13/13 first try; prefilled fixed window + hand-written dict compare helper | O(26·n) time ✅ / O(n) extra from `stream[size:]` slice copy (target O(1)); 1.23 s on the all-match case, 0.40 s with `==` instead of the helper | 2026-10-16 |
| L03.6 | [Shortest Collage Strip](learn/03-sliding-window/03.6-shortest-collage-strip/README.md) | Hard | .6 stretch (optional) | **solved** — 13/13 first try; `missing` counter, strict `<` for ties, slice once at the end | O(n + m) time / O(1) space ✅ (counts every letter, incl. ones the message never uses: 161 ms vs 83 ms on the far-apart case; `rf is None or lf is None` is half dead) | 2026-10-26 |
| L04.3 | [Farm Plot Ledger](learn/04-prefix-sums/04.3-farm-plot-ledger/README.md) | Medium | .3 standard | **todo** | — | — |

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
  O(n) space → O(1). Watch for this in DP (table vs. rolling state). *L01.5: a second
  `seen` set mirrors information already derivable from the first — 22 MB vs ~8 MB.*
  *Fixed in attempt 3;
  recurred in p008 (prefix array built then walked once — constant-factor cost only there,
  since the hash map is already O(n), but the same habit). Recurred in p014, where it
  costs real complexity: the prefix array is built so it can be shifted 31 times, but the
  per-bit counters are the only state carried forward — O(n) space against an O(1) target.*
- **Stale guards after a rewrite.** `len(prices) < 2` went load-bearing → dead →
  load-bearing-for-a-different-reason across three rewrites, unchanged each time.
  Re-answer "what does this guard defend against?" whenever the body changes.
  *Same family in L02.3/L02.4: the last branch of an if-chain spelled as `elif <the only
  remaining case>` instead of `else`, and (L02.4 attempt 1) range checks that can never fail.*

- **Special-casing the first element, which then forces a boundary guard** (p002). Pre-seeding
  `window = {s[0]: 0}` and starting at index 1 is what made `len(s) < 2` necessary; starting
  from an empty state removes both. Same guard habit as p001 — now the second data point.
  *Avoided in p003/p004/p007/p008; returned in p005 and p009.* Four occurrences. The tell
  is always the same: something is computed **before** the loop, and the guard exists to
  make that pre-computation safe. Fix the ordering, not the guard. *Fifth occurrence in
  p014: `if not nums: return 0` is dead — the empty list already falls straight through
  the `while` and returns 0.* *Sixth, mirrored, in L02.5: `while lo < hi` plus a post-loop
  `if lo == hi: rafts += 1`. The fix-up exists only because the loop condition stops one
  step early; `lo <= hi` absorbs it.* *Seventh in L02.6: seeding both maxima from
  `heights[0]` / `heights[-1]` and starting at 1 / n-2 is what makes `len < 3` necessary.*
  *Eighth in L03.3, despite the lesson calling it out: `counts = {s[0]: 1}` + `len == 0`
  guard, and recording before growing, which forces an `if ri == len(s) - 1` fix-up.*
  *Fixed in L03.3 attempt 2: empty start, grow → shrink → record, no guard.*
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
- **Fixing a symptom after the fact instead of preventing it** (L02.3). Repeated trios
  were removed by a `set` at the end instead of not being generated, which hid a whole
  repeated inner pass per duplicate first value (173 ms vs 0.5 ms on the few-values case).
- **Hand-writing what a builtin already does in C** (L03.5): a 26-key dict compare helper
  that is exactly `dict ==` cost 3.2x on the all-match perf case.

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
- Names now say what maps to what (`code_to_count` / `count_to_code` in L01.4). The
  naming weak spot from p002–p013 hasn't shown up in L01.3 or L01.4.
- Carries review feedback forward: L03.4 used L03.3's empty-start / `enumerate` fixes unprompted.

## Topics still untouched

Linked lists · Backtracking (both scheduled in the learning path: topics 07 and 08)

Linked lists and trees are supported by the harness via `dsakit.ListNode` / `TreeNode`
and the `build_list` / `list_values` / `build_tree` / `tree_values` helpers, which copy
iteratively. A plain node class still breaks: `run_cases` deep-copies every case's args,
and the default `copy.deepcopy` recurses once per node, so 500+ nodes raise
`RecursionError` before the solution is called.
