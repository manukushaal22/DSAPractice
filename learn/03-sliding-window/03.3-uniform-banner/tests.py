"""Test cases for L03.3. Run from repo root:  py run.py L3.3

You can also run this file directly:
    py learn/03-sliding-window/03.3-uniform-banner/tests.py
Feel free to read this file - the big banners are built so their answer is known by
construction, not computed, so there is nothing to copy.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import longest_uniform  # noqa: E402

import string  # noqa: E402

N = 500_000

# "ABAB...". A stretch of length L starting on an A holds ceil(L/2) A's and floor(L/2)
# B's, so it needs floor(L/2) repaints. With k = 1000 the best is L = 2k + 1 = 2001.
ALTERNATING = "AB" * (N // 2)
ALTERNATING_K = 1000

# Blocks of 1000 A's separated by single B's. With k = 5 the best stretch covers 6
# whole A-blocks and the 5 B's between them: 6 * 1000 + 5. Reaching a 7th block means a
# 6th B, and one more letter on either side is a B outside the stretch.
BLOCKS = ("A" * 1000 + "B") * (N // 1001)
BLOCKS_ANSWER = 6 * 1000 + 5

# "ABC...Z" repeated, with a run of 5000 Q's inserted between two repeats (after a Z,
# before an A). With k = 0 the answer is that run.
CYCLE = string.ascii_uppercase * ((N - 5000) // 52)
PLANTED = CYCLE + "Q" * 5000 + CYCLE

PERF_TIME_MS = 2500

CASES = [
    Case(name="example 1", args=("XYXY", 2), expected=4),
    Case(name="example 2", args=("PPQPQQP", 1), expected=4),
    Case(name="example 3", args=("ABCDE", 1), expected=2),
    Case(name="empty banner", args=("", 0), expected=0),
    Case(name="single letter, no repaints", args=("M", 0), expected=1),
    Case(name="already uniform", args=("ZZZZ", 0), expected=4),
    Case(
        name="no repaints allowed",
        args=("AABBBCC", 0),
        expected=3,
        note="With k = 0 the answer is the longest run that already exists.",
    ),
    Case(
        name="more repaints than letters",
        args=("ABCD", 10),
        expected=4,
        note="The answer can never exceed the banner's length.",
    ),
    Case(
        name="counts must come from one stretch",
        args=("AABBAABBAA", 1),
        expected=3,
        note="The banner holds six A's in total, but every stretch of 4 is two A's and "
        "two B's. Adding k to the most common letter over the whole banner gives 7.",
    ),
    Case(
        name="best letter changes along the banner",
        args=("CCCADDDDDB", 2),
        expected=7,
        note="The C's lead early, but the best stretch is 'ADDDDDB' (indices 3-9) "
        "with the A and B repainted to D.",
    ),
    Case(
        name="repaint in the middle joins two runs",
        args=("KKKKXKKKK", 1),
        expected=9,
    ),
    Case(name="every letter different", args=(string.ascii_uppercase, 3), expected=4),
    Case(
        name="perf: alternating AB, k = 1000",
        args=(ALTERNATING, ALTERNATING_K),
        expected=2 * ALTERNATING_K + 1,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
        note="Budget rejects checking every stretch (O(n^2)) and recounting each "
        "stretch from scratch.",
    ),
    Case(
        name="perf: blocks of A split by single B's, k = 5",
        args=(BLOCKS, 5),
        expected=BLOCKS_ANSWER,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
    ),
    Case(
        name="perf: cycling alphabet with a planted run, k = 0",
        args=(PLANTED, 0),
        expected=5000,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
    ),
]

if __name__ == "__main__":
    raise SystemExit(run_cases(longest_uniform, CASES, title="L03.3 - Uniform Banner"))
