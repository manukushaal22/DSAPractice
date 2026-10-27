# Learning path

A topic-by-topic route through interview DSA. Each topic starts with a **lesson**,
followed by a **ladder** of exercises that get harder one rung at a time.

This track complements [`problems/`](../problems), it does not replace it:

| Track | Purpose | You know the technique going in? |
| --- | --- | --- |
| `learn/` | Learn one technique properly, from easy to hard | **Yes**, the topic tells you |
| `problems/` | Interview simulation and spaced review across topics | **No**, recognising the technique is the test |

Once a topic is complete here, its techniques start appearing unlabelled in `problems/`.

## How a topic works

```
learn/
  NN-topic-slug/
    README.md                 the lesson
    NN.K-exercise-slug/       one exercise: README.md, solution.py, tests.py
```

1. **Read the lesson.** It covers the mental model, the invariant, recognition cues,
   one problem worked through in full (never one of the exercises), the common variants,
   pitfalls (including your own from `PROGRESS.md`) and self-check questions.
2. **Climb the ladder.** The agent writes exercises **one at a time**. The next rung
   only appears after the current one has been reviewed, so its difficulty can adapt.

### The ladder

| Rung | Level | Purpose |
| --- | --- | --- |
| `.1` | Easy | The technique in its simplest form |
| `.2` | Easy | The technique plus one twist |
| `.3` | Medium | The standard interview problem for this technique |
| `.4` | Medium | **Disguised**: the statement does not hint at the technique |
| `.5` | Medium | Combined with an earlier topic, or a harder variant |
| `.6` | Hard | Stretch challenge. Optional |

- **Adaptive siblings.** If a rung ends up `revisit`, the agent adds a sibling at the
  same level (`03.3b`) before moving up. If a rung was clearly easy, it may skip the next one.
- **Placement.** Topics already practised in `problems/` start higher up the ladder,
  shown in the *Starts at* column. Rungs below the start are skipped, but you can still
  ask for them.
- **Completion.** A topic is complete when every rung from its start rung up to `.5` is
  `solved` at the target complexity. A rung counts as solved when it, or one of its
  siblings, is. `.6` is optional. Completed topics then feed into `problems/` as spaced
  review.
- **Order.** Topics are listed in prerequisite order. Jumping ahead is allowed, but
  check the *Needs* column first.

### Commands

```powershell
py run.py L1.3        # one exercise (01.3); L3.3b for an inserted sibling
py run.py L1          # every exercise in topic 01
py run.py learn       # the whole track
py run.py --list      # both tracks, learn/ grouped by topic
```

## Curriculum

<!-- Parsed by solverapp/server/catalog.py: keep one row per topic and keep the column order. -->

| # | Topic | Folder | Phase | Needs | Starts at | Related drill |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | [Arrays & Hashing](01-arrays-and-hashing/README.md) | `01-arrays-and-hashing` | Linear basics | — | .3 | p001 |
| 02 | [Two Pointers](02-two-pointers/README.md) | `02-two-pointers` | Linear basics | 01 | .3 | p009 |
| 03 | [Sliding Window](03-sliding-window/README.md) | `03-sliding-window` | Linear basics | 01, 02 | .3 | p002 |
| 04 | [Prefix Sums & Difference Arrays](04-prefix-sums/README.md) | `04-prefix-sums` | Linear basics | 01 | .3 | p008, p014 |
| 05 | Stacks & Monotonic Stacks | `05-stacks` | Linear basics | 01 | .3 | p003 |
| 06 | Binary Search | `06-binary-search` | Linear basics | 02 | .3 | p004 |
| 07 | Linked Lists | `07-linked-lists` | Recursion & structure | 02 | .1 | — |
| 08 | Recursion & Backtracking | `08-recursion-and-backtracking` | Recursion & structure | 01 | .1 | — |
| 09 | Sorting, Intervals & Sweep Line | `09-sorting-and-intervals` | Recursion & structure | 02, 08 | .2 | p005 |
| 10 | Binary Trees | `10-binary-trees` | Trees & graphs | 08 | .1 | p015 |
| 11 | Binary Search Trees | `11-binary-search-trees` | Trees & graphs | 06, 10 | .1 | — |
| 12 | Heaps & Priority Queues | `12-heaps` | Trees & graphs | 09 | .1 | p011 |
| 13 | Graph Traversal (BFS / DFS / grids) | `13-graph-traversal` | Trees & graphs | 08, 10 | .1 | p006 |
| 14 | Topological Sort | `14-topological-sort` | Trees & graphs | 13 | .1 | — |
| 15 | Union-Find & MST | `15-union-find` | Trees & graphs | 13 | .1 | p012 |
| 16 | Shortest Paths | `16-shortest-paths` | Trees & graphs | 12, 13 | .1 | — |
| 17 | Tries | `17-tries` | Trees & graphs | 10 | .3 | p013 |
| 18 | 1-D Dynamic Programming | `18-dp-1d` | Dynamic programming | 08 | .2 | p007 |
| 19 | 2-D & String DP | `19-dp-2d` | Dynamic programming | 18 | .1 | p010 |
| 20 | Knapsack & Subset DP | `20-dp-knapsack` | Dynamic programming | 18 | .2 | p007 |
| 21 | Advanced DP (tree, state machine, interval, bitmask) | `21-dp-advanced` | Dynamic programming | 10, 19, 20 | .1 | — |
| 22 | Greedy & Exchange Arguments | `22-greedy` | Finishers | 09 | .2 | p001, p009 |
| 23 | Bit Manipulation | `23-bit-manipulation` | Finishers | 01 | .3 | p014 |
| 24 | Fenwick & Segment Trees | `24-range-query-trees` | Stretch | 04, 10 | .1 | — |
| 25 | String Algorithms (KMP, rolling hash) | `25-string-algorithms` | Stretch | 01, 03 | .1 | — |

Topics 24–25 are **stretch** topics: they rarely come up in interviews and are only
scheduled if you ask.

## Planned ladders

These are rung themes, not final problems. The agent rewrites every statement in its
own words, may retitle it, and adapts the ladder to how earlier rungs went. None of these
repeat a problem already in `problems/`.

**01 Arrays & Hashing**: .1 detect a duplicate (set membership) · .2 same letters,
different order (frequency counting) · .3 group words by their letters (canonical keys) ·
.4 k most frequent values in linear time (bucketing by count) · .5 longest run of
consecutive integers (set + run starts) · .6 smallest missing positive in O(1) extra space
(the array as its own hash table)

**02 Two Pointers**: .1 palindrome check skipping non-letters · .2 pair with target sum
in a sorted array · .3 all unique zero-sum triples · .4 three-way partition in place
(Dutch flag) · .5 fewest boats with a weight limit (sort + greedy pairing) · .6 trapped
rainwater

**03 Sliding Window**: .1 best fixed-size window sum · .2 fixed window with a running
count · .3 longest window after at most k replacements · .4 at most two kinds of item,
disguised · .5 every anagram occurrence in a text (window + counting) · .6 smallest window
containing all required characters

**04 Prefix Sums & Difference Arrays**: .1 range-sum queries · .2 balance index ·
.3 2-D range-sum queries · .4 range-increment bookings (difference array, disguised) ·
.5 longest subarray with equal 0s and 1s (prefix + hash) · .6 submatrices summing to a
target

**05 Stacks & Monotonic Stacks**: .1 balanced brackets · .2 stack with O(1) minimum ·
.3 streaming price span · .4 smallest number after removing k digits (disguised) ·
.5 sliding-window maximum (monotonic deque) · .6 largest rectangle in a histogram

**06 Binary Search**: .1 classic search · .2 first and last occurrence (lower/upper
bound) · .3 search a rotated sorted array · .4 a peak or rotation point (disguised
predicate) · .5 kth smallest in a sorted matrix (search on value + counting) · .6 median
of two sorted arrays

**07 Linked Lists**: .1 reverse a list · .2 merge two sorted lists · .3 cycle entry
point (fast/slow pointers) · .4 reorder by interleaving halves · .5 least-recently-used
cache (hash map + doubly linked list) · .6 reverse in groups of k

**08 Recursion & Backtracking**: .1 all subsets · .2 all permutations · .3 combinations
summing to a target · .4 word search in a grid · .5 palindrome partitioning · .6 count
N-queens placements

**09 Sorting, Intervals & Sweep Line**: .1 can one person attend every meeting ·
.2 insert an interval · .3 fewest removals to make intervals disjoint · .4 minimum rooms
(sweep line, disguised) · .5 intersections of two interval lists (two pointers) · .6 count
inversions with merge sort

**10 Binary Trees**: .1 maximum depth · .2 mirror / identical trees · .3 level-order
traversal · .4 lowest common ancestor · .5 rebuild a tree from two traversals (hashing) ·
.6 maximum path sum

**11 Binary Search Trees**: .1 search and insert · .2 validate a BST · .3 kth smallest
(in-order) · .4 pair with target sum in a BST (disguised in-order + two pointers) ·
.5 delete a node · .6 repair a BST with two swapped nodes

**12 Heaps & Priority Queues**: .1 kth largest · .2 k closest points · .3 merge k sorted
lists · .4 rearrange so no two neighbours match (disguised) · .5 k smallest pair sums
(frontier expansion) · .6 smallest range covering k lists

**13 Graph Traversal**: .1 flood fill · .2 count friend circles in an adjacency matrix ·
.3 multi-source BFS spread · .4 cells that drain to both oceans (reverse search,
disguised) · .5 shortest word transformation (BFS on an implicit graph) · .6 grid shortest
path with k obstacle removals (BFS over states)

**14 Topological Sort**: .1 can every course be finished · .2 a valid course order ·
.3 fewest semesters with parallel courses (Kahn by levels) · .4 letter order of an alien
alphabet (disguised) · .5 longest increasing path in a matrix (DAG + memo) · .6 sort items
by group with dependencies

**15 Union-Find & MST**: .1 connected components · .2 the redundant edge · .3 merge
accounts by shared email · .4 satisfiable equality equations (disguised) · .5 cheapest way
to connect all points (Kruskal) · .6 earliest time to swim across a grid

**16 Shortest Paths**: .1 signal delay to every node (Dijkstra) · .2 path of minimum
effort on a grid · .3 cheapest flight within k stops · .4 fewest arrow flips to cross a
grid (0-1 BFS, disguised) · .5 most probable path (multiplicative Dijkstra) · .6 shortest
walk visiting every node (BFS + bitmask)

**17 Tries**: .1 implement a trie · .2 longest common prefix · .3 word dictionary with
wildcards · .4 maximum XOR of two numbers (bitwise trie, disguised) · .5 search-as-you-type
suggestions · .6 find every dictionary word in a letter grid (trie + backtracking)

**18 1-D Dynamic Programming**: .1 ways to climb stairs · .2 non-adjacent maximum sum ·
.3 ways to decode a digit string · .4 split a string into dictionary words (disguised) ·
.5 longest increasing subsequence in O(n log n) (binary search) · .6 longest valid
bracket substring

**19 2-D & String DP**: .1 grid paths · .2 minimum path sum · .3 edit distance ·
.4 longest palindromic subsequence (disguised LCS) · .5 largest all-ones square ·
.6 regular-expression matching

**20 Knapsack & Subset DP**: .1 can a subset reach the target · .2 number of ways to make
change · .3 split into two equal-sum halves · .4 assign + and − signs to hit a target
(disguised) · .5 two-resource knapsack · .6 count profitable crime schemes

**21 Advanced DP**: .1 non-adjacent tree sum (tree DP) · .2 trading with a cooldown
(state machine) · .3 cheapest way to cut a stick (interval DP) · .4 partition into k equal
sums (bitmask DP, disguised) · .5 burst balloons · .6 shortest superstring

**22 Greedy & Exchange Arguments**: .1 assign cookies · .2 can you reach the end ·
.3 gas station circuit · .4 partition labels (disguised) · .5 task scheduler with
cooldown · .6 candy distribution (two passes)

**23 Bit Manipulation**: .1 count set bits for 0..n · .2 the single unpaired number ·
.3 single number among triples · .4 fewest bit flips so a OR b equals c (disguised) ·
.5 add two integers without `+` · .6 fewest operations to reach zero (Gray code)
