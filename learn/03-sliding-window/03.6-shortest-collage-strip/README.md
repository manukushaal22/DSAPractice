# L03.6 — Shortest Collage Strip

**Difficulty:** Hard
**Topics:** Sliding Window (variable size), Counting
**Track:** [03 Sliding Window](../README.md) · rung .6 of 6 (stretch, optional)

## Problem

You are making a collage message out of a single line of printed letters. You may cut
**one contiguous strip** out of the line, then cut that strip into single letters and
rearrange them. Letters you don't need are thrown away.

The strip must contain every letter of `message`, **as many times as the message uses
it**. Case matters: `a` and `A` are different letters.

Return the **shortest** such strip, as a string. If several strips are equally short,
return the one that starts **first**. If no strip works, return `""`.

## Examples

**Example 1**

```
Input:  line = "dbacXabdc", message = "abc"
Output: "bac"
```

Explanation: `"bac"` (indices 1–3) holds an `a`, a `b` and a `c`, and nothing shorter
than 3 letters can. `"cXab"` and `"abdc"` also work but are longer.

**Example 2**

```
Input:  line = "aXbaYa", message = "aa"
Output: "aYa"
```

Explanation: the message needs **two** `a`s. `"aXba"` has them in 4 letters; `"aYa"`
(indices 3–5) has them in 3.

**Example 3**

```
Input:  line = "abc", message = "abcc"
Output: ""
```

Explanation: the line has only one `c`, and the message needs two.

## Constraints

- `0 <= len(line) <= 500_000`
- `1 <= len(message) <= 500_000` (it may be longer than the line)
- both strings contain only letters `a`–`z` and `A`–`Z`

## Your task

Implement `shortest_strip(line: str, message: str) -> str` in `solution.py`.

Run the tests from the repo root with:

```powershell
py run.py L3.6
```

## Target complexity

**O(n + m) time, O(1) extra space** besides the returned string. Here n is the line's
length and m is the message's length; 52 counters count as O(1).

Trying every start and walking forward until the strip is complete is O(n·w), where w is
the length of a valid strip. The first perf case gets that a `TLE`.

Unlike L03.5, the second perf case is **designed to reject** checking all 52 counters
every time a pointer moves. That is O(52·n), linear on paper, but about 13x slower than
the intended solution here. Each pointer move must answer "does the window cover the
message yet?" in O(1).

<details><summary><b>Hint 1</b></summary>

If a strip covers the message, does every longer strip containing it also cover it?
So once the window covers the message, which end is worth moving, and for how long?

</details>

<details><summary><b>Hint 2</b></summary>

Grow the right end until the window covers the message. Then move the left end forward
for as long as it **still** covers, recording the window each time. When it stops
covering, go back to growing.

To answer "covers?" in O(1), keep one number: how many of the message's letters,
counting repeats, the window is still **missing**. A letter entering only lowers it if
the window had fewer copies of that letter than the message needs. A letter leaving
only raises it if the window drops below what the message needs.

</details>

<details><summary><b>Hint 3</b></summary>

Count what the message needs, and start with `missing = len(message)` and an empty
window. For each letter entering on the right, update its count and `missing`. While
`missing` is zero: record the window if it is **strictly** shorter than the best so far
(that keeps the earliest of equal-length strips), then take the left letter out, update
`missing`, and move the left end forward.

Store the best strip's start and length, not a slice. Slice once at the end.

</details>
