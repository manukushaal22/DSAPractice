"""Test cases for P002. Run from repo root:  py run.py 2

You can also run this file directly:  py problems/p002-.../tests.py
Feel free to read this file - the answers to the big cases are constructed, not
computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import length_of_longest_substring  # noqa: E402

# 100_000 copies of the same character: every window of length 2 repeats, so the
# answer is 1 by construction.
ALL_SAME = "a" * 100_000

# "abcdefghij" repeated 10_000 times (100_000 chars). The block has 10 distinct
# characters, so a window of length 10 aligned to a block is repeat-free, and any
# window of length 11 must span a block boundary and therefore repeat. Answer: 10.
PERIODIC = "abcdefghij" * 10_000

CASES = [
    Case(name="example 1", args=("abcabcbb",), expected=3),
    Case(name="example 2 - all identical", args=("bbbbb",), expected=1),
    Case(name="example 3 - substring not subsequence", args=("pwwkew",), expected=3),
    Case(name="empty string", args=("",), expected=0),
    Case(name="single character", args=("a",), expected=1),
    Case(name="two identical characters", args=("aa",), expected=1),
    Case(name="everything distinct", args=("abcdef",), expected=6),
    Case(
        name="abba - left edge must not rewind",
        args=("abba",),
        expected=2,
        note="After the window shrinks past the first 'a', its old index is stale. "
        "Reusing it moves the left edge backwards and inflates the answer to 3.",
    ),
    Case(
        name="tmmzuxt - duplicate outside the window",
        args=("tmmzuxt",),
        expected=5,
        note="The final 't' was last seen at index 0, which is already left of the "
        "window. It must not shrink anything. The answer is 'mzuxt'.",
    ),
    Case(name="dvdf", args=("dvdf",), expected=3),
    Case(
        name="case sensitive",
        args=("AaBbAa",),
        expected=4,
        note="'A' and 'a' are different characters. Folding case gives 2.",
    ),
    Case(
        name="spaces and symbols count",
        args=("a b!a b",),
        expected=4,
        note="The space is an ordinary character and can be the duplicate that "
        "closes a window.",
    ),
    Case(
        name="best window is the last one",
        args=("1231234",),
        expected=4,
        note="'1234' only completes at the final index - the answer must keep being "
        "updated to the very end.",
    ),
    Case(
        name="perf: 100k identical characters",
        args=(ALL_SAME,),
        expected=1,
        time_limit_ms=1500,
        memory_limit_mb=64,
        note="Budget rejects O(n^2): the window closes on every step, so a solution "
        "that rescans or rebuilds a set per start index does ~5e9 operations.",
    ),
    Case(
        name="perf: 100k periodic, 10 distinct per block",
        args=(PERIODIC,),
        expected=10,
        time_limit_ms=1500,
        memory_limit_mb=64,
        note="Budget rejects anything worse than O(n). The intended sweep needs a few "
        "tens of ms here; an O(n^2) scan needs minutes.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(
            length_of_longest_substring,
            CASES,
            title="P002 - Longest Substring Without Repeating Characters",
        )
    )
