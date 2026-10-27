# L02.5 — Rescue Rafts

**Difficulty:** Medium
**Topics:** Two Pointers, Sorting, Greedy Pairing
**Track:** [02 Two Pointers](../README.md) · rung .5 of 6 (combined with 01)

## Problem

A flood has stranded a group of people. `weights[i]` is the weight of person `i`. Every
rescue raft has the same weight limit, `limit`, and carries **at most two people**. The
people on a raft must weigh `limit` or less in total.

Everyone has to be rescued. Return the **fewest rafts** needed.

Every person weighs at most `limit`, so everyone fits on a raft alone.

## Examples

**Example 1**

```
Input:  weights = [3, 2, 2, 1], limit = 3
Output: 3
```

Explanation: the 3 has to go alone, since nobody weighs 0. The 1 and one of the 2s
share a raft (`1 + 2 = 3`). The other 2 goes alone. Two rafts are impossible: that
would need two pairs, and the 3 cannot be in a pair.

**Example 2**

```
Input:  weights = [1, 1, 4, 4], limit = 5
Output: 2
```

Explanation: `(1, 4)` and `(1, 4)`. Putting the two lightest people together first,
`(1, 1)`, leaves both 4s alone and uses 3 rafts.

**Example 3**

```
Input:  weights = [5, 5, 5, 5], limit = 10
Output: 2
```

Explanation: a pair that weighs **exactly** the limit is allowed.

## Constraints

- `0 <= len(weights) <= 500_000`
- `1 <= weights[i] <= limit <= 30_000`
- You may reorder `weights` in place

## Your task

Implement `min_rafts(weights: List[int], limit: int) -> int` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py L2.5
```

## Target complexity

**O(n log n) time, O(1) extra space** beyond an in-place sort.

This rules out pairing people by searching for a partner for each one. Scanning, or
finding a partner by binary search and then removing them from a list, is O(n²) and
the perf cases cut it off. The difficulty is not the speed, though. It is **which**
pairs to form: several natural greedy rules are wrong, and the small cases check them.

**Bonus, tying back to topic 01:** weights are whole numbers no larger than 30 000.
That is enough to drop the comparison sort and reach **O(n + limit)** time. It is the
same idea that took L01.4 below `n log n`. This is optional; the O(n log n) version
meets the target.

<details><summary><b>Hint 1</b></summary>

Every raft carries one or two people, so the answer is at least `ceil(n / 2)`. The
question is how many pairs you can form. Which person is the **hardest** to pair? Start
with them.

</details>

<details><summary><b>Hint 2</b></summary>

Take the heaviest person. If **anyone** can share their raft, the lightest person can,
because the lightest person weighs no more than anyone else. Pairing the heaviest with
the lightest is never worse than pairing them with someone else. Swap partners in any
optimal plan and check that it stays valid and uses the same number of rafts.

If the lightest person cannot share with the heaviest, nobody can, and the heaviest goes
alone.

</details>

<details><summary><b>Hint 3</b></summary>

Sort. Put one pointer on the lightest remaining person and one on the heaviest. Each
step launches **one** raft carrying the heaviest. The lightest joins if they fit. Move
the pointers to match.

Be careful at the end, when both pointers are on the **same** person: they still need a
raft.

</details>
