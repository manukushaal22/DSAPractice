# P013 — Shortest Root Replacement

**Difficulty:** Medium
**Topics:** Tries / Prefix Trees, Strings

## Problem

You are given a list of **roots** and a **sentence**. The sentence is a run of lowercase
words separated by single spaces.

A root *covers* a word when the word **starts with** that root — the root has to sit at
the front of the word, not somewhere in the middle. A root covers a word that is equal to
it, too.

Rewrite the sentence: every word covered by at least one root is replaced by the
**shortest** root that covers it. Words that no root covers are left exactly as they are.
Return the rewritten sentence, words joined by single spaces in their original order.

The root list may contain duplicates and may be empty. The sentence may be empty. Neither
input may be modified.

## Examples

**Example 1**

```
Input:  roots = ["cat", "bat", "rat"], sentence = "the cattle was rattled by the battery"
Output: "the cat was rat by the bat"
```

Explanation: `cattle` starts with `cat`, `rattled` with `rat`, `battery` with `bat`. The
words `the`, `was` and `by` are covered by nothing and survive untouched.

**Example 2**

```
Input:  roots = ["a", "aa", "aaa"], sentence = "aaaa aa bbb a"
Output: "a a bbb a"
```

Explanation: `aaaa` is covered by all three roots, and the shortest wins. `aa` is covered
by `a` and by `aa`; again the shortest wins, so it becomes `a` rather than staying `aa`.
`bbb` is covered by nothing. `a` is covered by the root `a`, which equals it.

**Example 3**

```
Input:  roots = ["tar"], sentence = "guitar tarnish tar"
Output: "guitar tar tar"
```

Explanation: `guitar` contains `tar` but does not *start* with it, so it is untouched.
`tarnish` starts with it and is replaced; `tar` equals it and is replaced by itself.

## Constraints

- `0 <= len(roots) <= 20_000`
- `1 <= len(root) <= 100`, lowercase English letters, duplicates allowed
- The sentence is either `""` or lowercase words joined by exactly one space, with no
  leading or trailing space
- `1 <= len(word) <= 100` and `len(sentence) <= 1_000_000`
- Do not modify either input

## Your task

Implement `replace_with_shortest_root(roots: List[str], sentence: str) -> str` in
`solution.py`.

Run the tests from the repo root with:

```powershell
py run.py 13
```

## Target complexity

**O(R + S) time, O(R) space**, where `R` is the total number of characters across all
roots and `S` is the length of the sentence. Every character of every root is touched
once while you prepare, and every character of the sentence is touched at most once —
in fact usually far fewer, because a word stops being interesting the moment it stops
looking like any root at all.

What the perf cases reject is **testing each word against every root**, `O(W · R)`. With
20 000 roots and 7 500 words that is 150 million prefix tests; they are each a fast C
call, and it is still several seconds. The tell is that it re-asks the same question
about the same leading characters thousands of times per word.

One alternative deserves a mention because it is genuinely decent: put the roots in a
set and look up `word[:1]`, `word[:2]`, … until one hits. It passes here — slicing and
hashing are C-speed — but its cost per word is bounded by the **longest root in the
list**, not by how much of the word actually resembles a root. A single 100-character
root makes every uncovered word 100 lookups deep, while the structure below settles the
same word in one. That gap is the point of the exercise.

<details><summary><b>Hint 1</b></summary>

Take the roots `care`, `cart`, `cat` and the word `cartoon`. How many times does a
root-by-root scan look at the letter `c` at the front of that word? At the `a` after it?

The roots overlap, and the work you are repeating is exactly the overlap. That suggests
storing the roots in a shape where a shared prefix is stored — and therefore examined —
only once.

Separately: you want the *shortest* covering root. If you walked the word one letter at
a time, in which order would candidate roots finish?

</details>

<details><summary><b>Hint 2</b></summary>

Arrange the roots into a tree whose **edges are letters**, so that the path from the root
of the tree down to some node spells out a prefix, and every root in your list is spelled
out by exactly one such path. Nodes where a root *ends* get a flag.

Now a word is checked by one walk: start at the top and follow the letters of the word
while there is an edge to follow. Two things can happen. You step onto a flagged node —
you have found a covering root, and because you walked letter by letter it is necessarily
the **shortest** one, so stop immediately. Or you run out of edges — no root covers this
word, and you stop there too, having read only as many letters as the roots had in common
with it.

Notice what that second case buys you: a word beginning with a letter no root begins with
costs you exactly one lookup.

</details>

<details><summary><b>Hint 3</b></summary>

The tree needs no node class — a dict per node is enough, mapping a letter to a child
dict, with one reserved key (something that can never be a letter) marking "a root ends
here".

Build: for each root, walk from the top creating missing children as you go, then set the
end marker on the final node. Inserting a root costs one step per character, so the whole
build is `O(R)`.

Query: for each word, keep a cursor node and a counter of how many letters you have
consumed. Step while the next letter has a child; the moment the current node carries the
end marker, the answer is that prefix of the word. If the walk dies first, the answer is
the word itself.

Collect the per-word results and join them with spaces at the end — do not build the
output by repeated string concatenation, which quietly turns an `O(S)` algorithm into an
`O(S²)` one.

</details>
