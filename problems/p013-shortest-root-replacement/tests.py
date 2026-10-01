"""Test cases for P013. Run from repo root:  py run.py 13

You can also run this file directly:
    py problems/p013-shortest-root-replacement/tests.py

Feel free to read this file - the answers to the big cases follow from how the input
is built, not from a reference solution.
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import replace_with_shortest_root  # noqa: E402

EXAMPLE_1_ROOTS = ["cat", "bat", "rat"]

# 'z' is deliberately left out: every generated root is built from ALPHA, so a word
# starting with 'z' is guaranteed to be covered by nothing.
ALPHA = "abcdefghijklmnopqrstuvwxy"

N_ROOTS = 20_000
N_WORDS = 7_500
ROOT_LEN = 5
WORD_LEN = 20


def _ident(i: int) -> str:
    """Four-letter base-25 label for ``i``; distinct for every i < 390625."""
    return (
        ALPHA[i // 15625]
        + ALPHA[(i // 625) % 25]
        + ALPHA[(i // 25) % 25]
        + ALPHA[i % 25]
    )


def _filler(seed: int, length: int) -> str:
    return "".join(ALPHA[(seed * 11 + k * 7) % 25] for k in range(length))


# Every root is exactly ROOT_LEN long and starts with its own unique four-letter
# label, so no root is a prefix of another. That makes "the root covering a word" a
# single, obvious string - known by construction, never computed by a solver.
BIG_ROOTS = [_ident(i) + _filler(i, ROOT_LEN - 4) for i in range(N_ROOTS)]

_rng = random.Random(11)
_picks = [_rng.randrange(N_ROOTS) for _ in range(N_WORDS)]

# Perf case A: every word is one of the roots plus 15 characters of padding.
A_SENTENCE = " ".join(
    BIG_ROOTS[i] + _filler(i + 5, WORD_LEN - ROOT_LEN) for i in _picks
)
A_EXPECTED = " ".join(BIG_ROOTS[i] for i in _picks)

# Perf case B: same root count, but 7 words in 8 start with 'z', which no root uses,
# so they are covered by nothing and must come back untouched.
_b_words, _b_expected = [], []
for _k in range(N_WORDS):
    if _k % 8 == 0:
        _i = _picks[_k]
        _b_words.append(BIG_ROOTS[_i] + _filler(_i + 2, WORD_LEN - ROOT_LEN))
        _b_expected.append(BIG_ROOTS[_i])
    else:
        _word = "z" + _filler(_k, WORD_LEN - 1)
        _b_words.append(_word)
        _b_expected.append(_word)

B_SENTENCE = " ".join(_b_words)
B_EXPECTED = " ".join(_b_expected)

CASES = [
    Case(
        name="example 1",
        args=(EXAMPLE_1_ROOTS, "the cattle was rattled by the battery"),
        expected="the cat was rat by the bat",
        expected_args=(EXAMPLE_1_ROOTS, "the cattle was rattled by the battery"),
        note="Also checks the root list comes back unchanged and unreordered, so if "
        "you want the roots sorted, sort a copy.",
    ),
    Case(
        name="example 2 - shortest root wins",
        args=(["a", "aa", "aaa"], "aaaa aa bbb a"),
        expected="a a bbb a",
        note="'aa' is a root but is itself covered by the shorter root 'a', so it "
        "must still be replaced. Matching the longest root, or the first root in "
        "the list, both report 'a aa bbb a'.",
    ),
    Case(
        name="example 3 - prefix, not substring",
        args=(["tar"], "guitar tarnish tar"),
        expected="guitar tar tar",
        note="'guitar' contains the root but does not start with it. An `in` test "
        "instead of a prefix test replaces it.",
    ),
    Case(
        name="empty sentence",
        args=(["a", "b"], ""),
        expected="",
        note="No words at all. Splitting '' on spaces yields [''], so a careless "
        "rebuild returns a stray empty word or crashes on word[0].",
    ),
    Case(
        name="no roots at all",
        args=([], "nothing here changes"),
        expected="nothing here changes",
        note="An empty root list covers nothing; the sentence comes back verbatim.",
    ),
    Case(
        name="single word, root equals it",
        args=(["hello"], "hello"),
        expected="hello",
        note="Smallest interesting input: a root covers the word it equals.",
    ),
    Case(
        name="root longer than the word",
        args=(["abcdef"], "abc abcde abcdef abcdefgh"),
        expected="abc abcde abcdef abcdef",
        note="A word shorter than the root is not covered - the walk must run out "
        "of word, not out of root. Comparing only the characters the word has "
        "replaces 'abc' and 'abcde' too.",
    ),
    Case(
        name="duplicate and nested roots, worst order",
        args=(["cart", "ca", "cart", "c", "ca"], "cartoon carpet cat"),
        expected="c c c",
        note="Duplicates must not confuse anything, and the shortest root 'c' "
        "appears late in the list.",
    ),
    Case(
        name="roots listed longest first",
        args=(["abcd", "abc", "ab", "a"], "abcde abcd abc ab a"),
        expected="a a a a a",
        note="Every word collapses to the single-letter root regardless of the "
        "order the roots were inserted in.",
    ),
    Case(
        name="nothing is covered",
        args=(["x", "qq", "zebra"], "the quick brown fox"),
        expected="the quick brown fox",
        note="'quick' starts with 'q' but the root is 'qq'; 'fox' ends with 'x' but "
        "the root must sit at the front.",
    ),
    Case(
        name="every word is replaced",
        args=(["a", "b"], "apple banana avocado brie"),
        expected="a b a b",
        note="Single-letter roots: the walk must be able to stop after one step.",
    ),
    Case(
        name="repeated word, one letter apart",
        args=(["ab"], "ab a b abab ba"),
        expected="ab a b ab ba",
        note="'a' is a prefix of the root, not the other way round, so it stays. "
        "'ba' contains the root's letters in the wrong order.",
    ),
    Case(
        name="perf: 20k roots, 7.5k words, every word covered",
        args=(BIG_ROOTS, A_SENTENCE),
        expected=A_EXPECTED,
        time_limit_ms=2000,
        memory_limit_mb=192,
        note="Each word is a known root plus padding, so the answer is the list of "
        "roots picked - known by construction. The budget rejects O(W*R): testing "
        "each of the 7500 words against each of the 20000 roots is 150 million "
        "prefix tests, several seconds even though each one is a fast C call. A "
        "prefix tree reads 5 characters per word and stops.",
    ),
    Case(
        name="perf: same roots, 7 words in 8 covered by nothing",
        args=(BIG_ROOTS, B_SENTENCE),
        expected=B_EXPECTED,
        time_limit_ms=2000,
        memory_limit_mb=192,
        note="Most words start with a letter no root uses, so they must come back "
        "untouched. Same O(W*R) rejection as the previous case, plus the property "
        "that matters for the target complexity: a word covered by nothing should "
        "cost one failed lookup, not a walk over the whole word.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(
            replace_with_shortest_root,
            CASES,
            title="P013 - Shortest Root Replacement",
        )
    )
