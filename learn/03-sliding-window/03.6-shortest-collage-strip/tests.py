"""Test cases for L03.6. Run from repo root:  py run.py L3.6

You can also run this file directly:
    py learn/03-sliding-window/03.6-shortest-collage-strip/tests.py
Feel free to read this file - the long lines are built so their answer is known by
construction, not computed, so there is nothing to copy.
"""

import string
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import shortest_strip  # noqa: E402

# "A", 999 z's, "B", 999 z's, repeated 250 times (500_000 letters). Every strip holding
# an A and a B runs from one to the nearest other, which is exactly 1001 letters. The
# first one is line[0:1001].
GAP = 999
FAR_APART = ("A" + "z" * GAP + "B" + "z" * GAP) * 250
FAR_APART_ANSWER = FAR_APART[: GAP + 2]

# All 52 letters in a fixed order, repeated 9000 times (468_000 letters). The message
# needs 2000 of every letter (104_000 letters). In a 52-periodic line, any 104_000
# letters in a row hold exactly 2000 of each, and no shorter strip has enough letters
# at all. So the answer is the first 104_000 letters.
LETTERS = string.ascii_letters
NEED_EACH = 2000
PERIODIC_LINE = LETTERS * 9000
EVERY_LETTER_MESSAGE = string.ascii_letters[::-1] * NEED_EACH
PERIODIC_ANSWER = PERIODIC_LINE[: len(LETTERS) * NEED_EACH]

PERF_TIME_MS = 1500

CASES = [
    Case(name="example 1", args=("dbacXabdc", "abc"), expected="bac"),
    Case(name="example 2", args=("aXbaYa", "aa"), expected="aYa"),
    Case(name="example 3", args=("abc", "abcc"), expected=""),
    Case(name="empty line", args=("", "a"), expected=""),
    Case(
        name="the whole line is the answer",
        args=("cab", "abc"),
        expected="cab",
    ),
    Case(
        name="case matters",
        args=("aAbB", "AB"),
        expected="AbB",
        note="'a' and 'A' are different letters. The strip must start at the 'A'.",
    ),
    Case(
        name="tie goes to the earlier strip",
        args=("abXba", "ab"),
        expected="ab",
        note="'ab' at index 0 and 'ba' at index 3 are both length 2. Only replace the "
        "best on a strictly shorter strip.",
    ),
    Case(name="one-letter message", args=("zzzyzz", "y"), expected="y"),
    Case(
        name="surplus copies don't count twice",
        args=("aaab", "ab"),
        expected="ab",
        note="The window holds three a's, but the message needs one. The start must keep "
        "moving past the extra a's.",
    ),
    Case(
        name="answer ends on the last letter",
        args=("XXXXabc", "cba"),
        expected="abc",
    ),
    Case(
        name="repeated letters in the message",
        args=("abcabdebac", "abca"),
        expected="abca",
        note="Needs two a's. 'abc' and 'cab' cover the kinds but not the counts.",
    ),
    Case(
        name="perf: required letters far apart",
        args=(FAR_APART, "AB"),
        expected=FAR_APART_ANSWER,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
        note="Every valid strip is 1001 letters. Trying each start and walking forward "
        "is O(n * 1000) and gets cut off.",
    ),
    Case(
        name="perf: every letter needed 2000 times",
        args=(PERIODIC_LINE, EVERY_LETTER_MESSAGE),
        expected=PERIODIC_ANSWER,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
        note="52 different letters needed. Re-checking all 52 counters every time a "
        "pointer moves is O(52 * n) and is designed to miss this budget. Keep one "
        "number that says how much is still missing.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(shortest_strip, CASES, title="L03.6 - Shortest Collage Strip")
    )
