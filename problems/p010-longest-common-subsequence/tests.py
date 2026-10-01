"""Test cases for P010. Run from repo root:  py run.py 10

You can also run this file directly:  py problems/p010-longest-common-subsequence/tests.py
Feel free to read this file - the answers to the big cases are constructed, not
computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import lcs_length  # noqa: E402

# Two identical 1000-character strings. A string is a subsequence of itself and nothing
# longer than either input is possible, so the answer is exactly 1000.
IDENTICAL = "ABCDEFGHIJ" * 100

# Disjoint alphabets: no character of one appears in the other, so no common
# subsequence of any length exists and the answer is 0. Worst case in the sense that
# every cell of the table must still be visited to establish it.
DISJOINT_A = "X" * 1000
DISJOINT_B = "Y" * 1000

# "ABAB...AB" against "BABA...BA", 1000 characters each.
# Dropping the leading 'A' from the first gives a 999-character alternating string that
# starts and ends with 'B' - which is exactly the first 999 characters of the second.
# So a common subsequence of length 999 exists. Length 1000 would require the two
# strings to be equal, and they differ at position 0, so the answer is exactly 999.
SHIFTED_A = "AB" * 500
SHIFTED_B = "BA" * 500

CASES = [
    Case(name="example 1", args=("abcde", "ace"), expected=3),
    Case(
        name="example 2 - several optimal answers",
        args=("abcbdab", "bdcaba"),
        expected=4,
        note="'bcba' and 'bdab' both work. Only the length is compared.",
    ),
    Case(
        name="example 3 - reversed order",
        args=("abc", "cba"),
        expected=1,
        note="Same characters, opposite order. Anything above 1 means order is being "
        "ignored - that would be a common substring-set, not a subsequence.",
    ),
    Case(name="both empty", args=("", ""), expected=0),
    Case(name="first empty", args=("", "abc"), expected=0),
    Case(name="second empty", args=("abc", ""), expected=0),
    Case(name="single character, match", args=("a", "a"), expected=1),
    Case(name="single character, no match", args=("a", "b"), expected=0),
    Case(name="no shared characters", args=("abc", "def"), expected=0),
    Case(
        name="subsequence, not substring",
        args=("abcdefg", "aeg"),
        expected=3,
        note="'aeg' is scattered through the first string. A longest-common-substring "
        "solution returns 1 here.",
    ),
    Case(
        name="repeated characters",
        args=("aaa", "aa"),
        expected=2,
        note="Capped by the shorter string, not by the count of distinct characters.",
    ),
    Case(
        name="case sensitivity",
        args=("AbC", "abc"),
        expected=1,
        note="Only 'b' matches across the two; 'A'/'a' and 'C'/'c' differ in case. "
        "Folding case returns 3.",
    ),
    Case(
        name="perf: 1000x1000 identical",
        args=(IDENTICAL, IDENTICAL),
        expected=1000,
        time_limit_ms=4000,
        memory_limit_mb=128,
        note="One million table cells, every one of them a match. Budget rejects "
        "recursion without memoisation, which is exponential here.",
    ),
    Case(
        name="perf: 1000x1000 disjoint alphabets",
        args=(DISJOINT_A, DISJOINT_B),
        expected=0,
        time_limit_ms=4000,
        memory_limit_mb=128,
        note="Every cell must be computed to prove the answer is 0 - nothing "
        "short-circuits.",
    ),
    Case(
        name="perf: 1000x1000 alternating, off by one",
        args=(SHIFTED_A, SHIFTED_B),
        expected=999,
        time_limit_ms=4000,
        memory_limit_mb=128,
        note="Almost the same string, shifted by one character. An off-by-one in the "
        "table indices shows up as 998 or 1000 rather than as garbage.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(lcs_length, CASES, title="P010 - Longest Common Subsequence")
    )
