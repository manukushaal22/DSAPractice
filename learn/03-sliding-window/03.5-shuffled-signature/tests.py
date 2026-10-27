"""Test cases for L03.5. Run from repo root:  py run.py L3.5

You can also run this file directly:
    py learn/03-sliding-window/03.5-shuffled-signature/tests.py
Feel free to read this file - the long streams are built so their answer is known by
construction, not computed, so there is nothing to copy.
"""

import string
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import find_shuffled  # noqa: E402

# "abc...z" repeated 23_000 times (598_000 letters). The signature is a fixed shuffle of
# the alphabet repeated 2000 times (52_000 letters, 2000 of each letter). Any stretch of
# 52_000 = 26 * 2000 letters in a 26-periodic stream also holds 2000 of each letter, so
# every start position matches.
ALPHABET_REPEATS = 23_000
SIG_REPEATS = 2000
CYCLE_STREAM = string.ascii_lowercase * ALPHABET_REPEATS
CYCLE_SIGNATURE = "qwertyuiopasdfghjklzxcvbnm" * SIG_REPEATS
CYCLE_ANSWER = list(range(len(CYCLE_STREAM) - len(CYCLE_SIGNATURE) + 1))

# "abab..." (600_000 letters). Any even-length stretch holds equally many a's and b's.
# The signature has one more a than b, so no stretch can match.
HALF = 50_000
AB_STREAM = "ab" * 300_000
LOPSIDED_SIGNATURE = "a" * (HALF + 1) + "b" * (HALF - 1)

PERF_TIME_MS = 3000

CASES = [
    Case(name="example 1", args=("tacocatbat", "act"), expected=[0, 4]),
    Case(name="example 2", args=("abab", "ab"), expected=[0, 1, 2]),
    Case(
        name="example 3",
        args=("abbab", "aab"),
        expected=[],
        note="Same kinds of letter, wrong counts. Checking only which letters appear "
        "reports every position.",
    ),
    Case(name="empty stream", args=("", "a"), expected=[]),
    Case(
        name="signature longer than the stream",
        args=("ab", "abc"),
        expected=[],
    ),
    Case(
        name="same length, a match",
        args=("listen", "silent"),
        expected=[0],
        note="Exactly one stretch fits, and it covers the whole stream.",
    ),
    Case(name="same length, a near miss", args=("abcd", "abce"), expected=[]),
    Case(
        name="one-letter signature",
        args=("banana", "a"),
        expected=[1, 3, 5],
        note="A window of size 1 still slides: add one letter, remove one letter.",
    ),
    Case(
        name="all one letter",
        args=("aaaaa", "aa"),
        expected=[0, 1, 2, 3],
    ),
    Case(
        name="match on the last stretch",
        args=("xyzzyx", "xy"),
        expected=[0, 4],
        note="The stretch at index 4 ends on the stream's last letter. Stopping the "
        "slide one step early misses it.",
    ),
    Case(
        name="signature with repeated letters",
        args=("bacaabca", "aabc"),
        expected=[0, 2, 3, 4],
        note="'baca' yes, 'acaa' no (three a's), then 'caab', 'aabc', 'abca'. Each "
        "match needs two a's, one b, one c.",
    ),
    Case(
        name="perf: every position matches",
        args=(CYCLE_STREAM, CYCLE_SIGNATURE),
        expected=CYCLE_ANSWER,
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=128,
        note="546_001 matches with a 52_000-letter signature. Re-counting or sorting "
        "each stretch is O(n*m) and gets cut off.",
    ),
    Case(
        name="perf: no position matches",
        args=(AB_STREAM, LOPSIDED_SIGNATURE),
        expected=[],
        time_limit_ms=PERF_TIME_MS,
        memory_limit_mb=64,
        note="100_000-letter signature, 500_001 candidate stretches, none valid. "
        "O(n*m) work here is about 5e10 steps.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(run_cases(find_shuffled, CASES, title="L03.5 - Shuffled Signature"))
