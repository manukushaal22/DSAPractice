"""Test cases for L01.3. Run from repo root:  py run.py L1.3

You can also run this file directly:
    py learn/01-arrays-and-hashing/01.3-group-rearranged-words/tests.py
Feel free to read this file - the big cases are built so their groups are known by
construction, not computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import group_rearranged  # noqa: E402

import random  # noqa: E402
from itertools import permutations  # noqa: E402


def _canon(groups):
    return sorted(sorted(group) for group in groups)


def same_groups(actual, expected) -> bool:
    """Groups and the words inside them may come in any order."""
    if not isinstance(actual, list) or not all(isinstance(g, list) for g in actual):
        return False
    try:
        return _canon(actual) == _canon(expected)
    except TypeError:
        return False


# ---------------------------------------------------------------- big inputs
#
# A word is described by a "signature" s in [0, 4**9): its base-4 digits are how many
# times each of the letters b..j occurs, and every word also carries one 'a'. Distinct
# signatures have distinct letter counts, so words built from different signatures are
# never rearrangements of each other. Rotating a word keeps its letter counts, so
# rotations of one word always are. The groups are therefore known by construction.

LETTERS = "bcdefghij"
SIGNATURES = 4 ** len(LETTERS)  # 262_144


def word_for(signature: int) -> str:
    counts = []
    for _ in LETTERS:
        signature, digit = divmod(signature, 4)
        counts.append(digit)
    # Start the letter order at a signature-dependent offset so words are not
    # already in alphabetical order.
    start = sum(counts) % len(LETTERS)
    order = range(start, start + len(LETTERS))
    body = "".join(LETTERS[i % 9] * counts[i % 9] for i in order)
    return body[: len(body) // 2] + "a" + body[len(body) // 2 :]


def rotations(word: str, how_many: int) -> list:
    return [word[r % len(word) :] + word[: r % len(word)] for r in range(how_many)]


# 2_000 groups x 50 rotations = 100_000 words, shuffled together. Multiplying by an odd
# number is a bijection modulo 2**18, so the 2_000 signatures are distinct.
GROUPED_EXPECTED = [rotations(word_for(i * 131 % SIGNATURES), 50) for i in range(2_000)]
GROUPED = [word for group in GROUPED_EXPECTED for word in group]
random.Random(13).shuffle(GROUPED)

# 100_000 words with pairwise-distinct signatures: every group is a singleton, so any
# approach that compares a word against each existing group does ~n^2 / 2 comparisons.
SINGLE_WORDS = [word_for(i * 2_654_435_761 % SIGNATURES) for i in range(100_000)]
SINGLE_EXPECTED = [[word] for word in SINGLE_WORDS]

FOUR_LETTER_PERMS = ["".join(p) for p in permutations("abcd")]

CASES = [
    Case(
        name="example 1",
        args=(["listen", "silent", "google", "enlist", "gogole", "cat"],),
        expected=[["listen", "silent", "enlist"], ["google", "gogole"], ["cat"]],
        cmp=same_groups,
        expected_args=(["listen", "silent", "google", "enlist", "gogole", "cat"],),
        note="Also checks the input list comes back unchanged.",
    ),
    Case(
        name="example 2 - empty strings and a duplicate",
        args=(["", "a", ""],),
        expected=[["", ""], ["a"]],
        cmp=same_groups,
        note="Empty strings are rearrangements of each other, and duplicates are kept.",
    ),
    Case(
        name="example 3 - same letters, different counts",
        args=(["ab", "aab", "ba", "abb"],),
        expected=[["ab", "ba"], ["aab"], ["abb"]],
        cmp=same_groups,
        note="A key that records only WHICH letters occur (a set) merges all four.",
    ),
    Case(name="no words", args=([],), expected=[], cmp=same_groups),
    Case(name="single word", args=(["zebra"],), expected=[["zebra"]], cmp=same_groups),
    Case(
        name="the same word four times",
        args=(["abc", "abc", "abc", "abc"],),
        expected=[["abc", "abc", "abc", "abc"]],
        cmp=same_groups,
    ),
    Case(
        name="nothing related",
        args=(["abc", "abd", "abe", "xyz"],),
        expected=[["abc"], ["abd"], ["abe"], ["xyz"]],
        cmp=same_groups,
    ),
    Case(
        name="all 24 orderings of four letters",
        args=(FOUR_LETTER_PERMS,),
        expected=[FOUR_LETTER_PERMS],
        cmp=same_groups,
    ),
    Case(
        name="one letter, different lengths",
        args=(["a", "aa", "aaa", "a"],),
        expected=[["a", "a"], ["aa"], ["aaa"]],
        cmp=same_groups,
    ),
    Case(
        name="doubled letters are a different group",
        args=(["abc", "aabbcc", "cba", "ccbbaa"],),
        expected=[["abc", "cba"], ["aabbcc", "ccbbaa"]],
        cmp=same_groups,
    ),
    Case(
        name="ambiguous count key: 1 and 11 vs 11 and 1",
        args=(["a" + "b" * 11, "a" * 11 + "b", "b" * 11 + "a"],),
        expected=[["a" + "b" * 11, "b" * 11 + "a"], ["a" * 11 + "b"]],
        cmp=same_groups,
        note="Counts (a=1, b=11) and (a=11, b=1) both read '111' when the digits are "
        "glued together without a separator. The key must be unambiguous.",
    ),
    Case(
        name="whole alphabet, forwards and backwards",
        args=(["abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba", "z" * 26],),
        expected=[["abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba"], ["z" * 26]],
        cmp=same_groups,
    ),
    Case(
        name="perf: 100k words in 2k groups of 50",
        args=(GROUPED,),
        expected=GROUPED_EXPECTED,
        cmp=same_groups,
        time_limit_ms=2500,
        memory_limit_mb=384,
        note="Budget rejects comparing words against each other (O(n^2 k)) and "
        "comparing each word with one representative per group (O(n g k)).",
    ),
    Case(
        name="perf: 100k words, all unrelated",
        args=(SINGLE_WORDS,),
        expected=SINGLE_EXPECTED,
        cmp=same_groups,
        time_limit_ms=2500,
        memory_limit_mb=384,
        note="Every word is its own group, so g = n. A scan over existing groups per "
        "word is ~5e9 comparisons here. Budget allows O(n k) or O(n k log k) only.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(group_rearranged, CASES, title="L01.3 - Group Rearranged Words")
    )
