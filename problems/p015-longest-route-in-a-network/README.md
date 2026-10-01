# P015 — Longest Route in a Network

**Difficulty:** Medium
**Topics:** Trees, DFS/BFS, Post-order Aggregation

## Problem

A network has `n` relay stations, labelled `0` to `n - 1`, joined by exactly `n - 1`
cables. Every station can reach every other station, and because there are `n - 1` cables
holding `n` stations together there is **exactly one** route between any two stations —
the network is a tree.

Each cable `[a, b, w]` joins stations `a` and `b` and takes `w` milliseconds to cross.
The **latency** between two stations is the total weight of the one route joining them.

Return the largest latency between any pair of stations. With a single station there are
no pairs, so the answer is `0`.

The cables are given in arbitrary order, and `a` and `b` may be listed in either order.
The input must not be modified.

## Examples

**Example 1**

```
Input:  n = 4, links = [[0,1,5], [1,2,3], [1,3,2]]
Output: 8
```

Explanation: station `1` sits in the middle with three neighbours. The costliest route is
`0 → 1 → 2`, costing `5 + 3 = 8`. Note `0 → 1 → 3` costs only `5 + 2 = 7`.

**Example 2**

```
Input:  n = 6, links = [[0,1,1], [1,2,1], [2,3,1], [3,4,1], [1,5,10]]
Output: 13
```

Explanation: stations `0..4` form a chain of cheap cables, and station `5` hangs off
station `1` behind one expensive cable. The costliest route is `5 → 1 → 2 → 3 → 4`,
costing `10 + 1 + 1 + 1 = 13`. The longest route by *number of cables* is
`0 → 1 → 2 → 3 → 4`, but it only costs `4` — hop count is not the answer.

**Example 3**

```
Input:  n = 5, links = [[0,1,1], [1,2,4], [1,3,4], [3,4,1]]
Output: 9
```

Explanation: the costliest route is `2 → 1 → 3 → 4`, costing `4 + 4 + 1 = 9`. Station `0`
is a dead end that no costliest route touches — the answer need not involve station `0`,
and need not start anywhere in particular.

## Constraints

- `1 <= n <= 100_000`
- `len(links) == n - 1`, and the cables always form a single connected tree
- `0 <= a, b < n` and `a != b`
- `0 <= w <= 10_000` — a cable may be free, so a latency of `0` is a real answer
- The tree may be any shape, **including one long chain of `n` stations**
- Do not modify the input list

## Your task

Implement `longest_route(n: int, links: List[List[int]]) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py 15
```

## Target complexity

**O(n) time, O(n) space.** You get to look at each station and each cable a constant
number of times.

That rules out **measuring outward from every station** — a traversal per station is
`O(n²)`, which at the perf sizes is hundreds of millions of steps, and the budget will cut
it off. One traversal gives you the distances from *one* station; the whole point is that
you do not need the other `n - 1`.

One more thing, flagged up front rather than left as a trap: **the constraints allow the
network to be a single chain of 100 000 stations**, and one of the perf cases is exactly
that. Python's default recursion limit is 1000, so a plainly recursive traversal raises
`RecursionError` long before it gets there. That is a property of the input shape, not a
bug in your idea — but you do have to decide what to do about it, and the two natural
approaches to this problem differ in how much they care.

<details><summary><b>Hint 1</b></summary>

Measuring from all `n` stations is wasteful because the answer is a single route, and that
route has just two endpoints. So the real question is: **can you find one of those two
endpoints without already knowing the answer?**

Try it by hand on Example 2. Pick any station you like — say station `3`. Walk to whichever
station is costliest to reach from it. Now do the same thing again, starting from where you
landed. Try it from a different starting station. Does it keep landing on the same pair?

Separately, a completely different angle on the same problem: pin the tree down by calling
some station the top, so every other station hangs below it. Now every route has a single
highest point. If you knew, for each station, how far down it can reach, could you work
out the best route whose highest point is that station?

</details>

<details><summary><b>Hint 2</b></summary>

Both angles work, and they have different strengths.

**The two-sweep idea.** From *any* starting station, the station that is costliest to reach
is always an endpoint of some costliest route. (Sketch of why: suppose it were not. The
route from your start meets the true costliest route somewhere; swapping the tail you took
for the tail of the true route cannot make things shorter, so the station you landed on is
at least as far as a real endpoint — so it is one.) So: sweep once from anywhere to find a
station `u`, then sweep once more from `u`, and the largest distance you see is the answer.
Two traversals, and **neither one needs recursion** — a stack or queue carries the state.

**The hanging-down idea.** Root the tree anywhere. For each station define *reach* = the
cost of the most expensive downward-only route starting there. A station with no children
has reach `0`. Otherwise, reach is the best of `cable weight + that child's reach` over its
children. Now the costliest route whose highest point is this station is the **sum of its
two best** such child values — and when a station has only one child, the second best counts
as `0`, because the route can simply stop there. The answer is the largest such sum over all
stations.

Notice the shape of that second one: what you *return* from a station (one reach) is not what
you are *looking for* (two reaches combined). That split — return one thing, record another —
is the reusable part, and it shows up all over tree problems.

</details>

<details><summary><b>Hint 3</b></summary>

Build an adjacency list first: for each station, the list of `(neighbour, weight)` pairs.
Both approaches need it, and building it is one pass over the cables.

For the two-sweep version, write one helper that takes a start station and returns the
distances to everything — an explicit stack or queue, popping a station and pushing its
unvisited neighbours with the running total. Call it from station `0`, take the station with
the largest distance, call it again from there, and return the largest distance from the
second call. Track visited by remembering the station you came from, or with a visited
array. Because the traversal is iterative, the 100 000-station chain is not a problem.

For the hanging-down version, you need children processed before their parent. Done with
plain recursion that is a post-order walk, and it is the clearer code — but on a chain it
will hit the recursion limit, so you would need to either raise that limit or flatten the
walk into an explicit stack. Flattening a post-order is the fiddly part: a common way is to
first produce an ordering of the stations by a simple iterative sweep from the root, then
process that ordering backwards, which guarantees every child is finished before its parent.

Whichever you pick, remember `n = 1`: no cables, no pairs, answer `0`.

</details>
