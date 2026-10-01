"""Test cases for P014. Run from repo root:  py run.py 14

You can also run this file directly:
    py problems/p014-total-xor-over-subarrays/tests.py

Feel free to read this file - the answers to the big cases follow from how the input
is built, not from a reference solution.
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsakit import Case, run_cases  # noqa: E402
from solution import total_subarray_xor  # noqa: E402

EXAMPLE_1 = [1, 3]

N = 10_000

# Both perf cases are built backwards: pick the prefix-XOR values first, then derive
# the list from them with nums[i] = P[i + 1] ^ P[i]. P[0] must be 0, since it stands
# for the XOR of no elements at all.
#
# The point of choosing the prefix values from a small closed set is that the answer
# follows from counting how many land in each class, and XORing one representative
# per pair of classes - a plain pairing argument, with no bit arithmetic and no
# reference solution anywhere in this file.


def _nums_from_prefixes(prefixes):
    return [prefixes[i + 1] ^ prefixes[i] for i in range(len(prefixes) - 1)]


# --- Perf case A: prefix values are drawn from {0, V} -----------------------------
# Every pair of prefix values XORs to 0 (same class) or to V (different class), so
# the total is simply "number of cross pairs" * V.
V = 0b1011010110101101011010110101101

_rng = random.Random(5)
_pa = [0] + [V if _rng.getrandbits(1) else 0 for _ in range(N)]
A_NUMS = _nums_from_prefixes(_pa)
_a0 = _pa.count(0)
A_EXPECTED = _a0 * (len(_pa) - _a0) * V

# --- Perf case B: prefix values are drawn from {0, X, Y, Z} with Z = X ^ Y --------
# Those four values are closed under XOR, so every pair falls into one of six cross
# classes: (0,X) and (Y,Z) both give X, (0,Y) and (X,Z) both give Y, and (0,Z) and
# (X,Y) both give Z. Same-class pairs give 0.
X = 0b1100110011001100110011001100110
Y = 0b0110011001100110011001100110011
Z = X ^ Y

_rng_b = random.Random(17)
_choices = (0, X, Y, Z)
_pb = [0] + [_choices[_rng_b.getrandbits(2)] for _ in range(N)]
B_NUMS = _nums_from_prefixes(_pb)
_n0, _nx, _ny, _nz = (_pb.count(v) for v in _choices)
B_EXPECTED = (
    (_n0 * _nx + _ny * _nz) * X
    + (_n0 * _ny + _nx * _nz) * Y
    + (_n0 * _nz + _nx * _ny) * Z
)

CASES = [
    Case(
        name="example 1",
        args=(EXAMPLE_1,),
        expected=6,
        expected_args=(EXAMPLE_1,),
        note="Also checks the input list comes back unchanged, so do not build the "
        "prefix XORs in place over nums.",
    ),
    Case(
        name="example 2",
        args=([5, 2, 5],),
        expected=28,
    ),
    Case(
        name="example 3 - repeats cancel",
        args=([4, 4, 4],),
        expected=16,
        note="The two adjacent pairs XOR to 0 and contribute nothing. A solution "
        "that assumes longer subarrays add more gets this wrong.",
    ),
    Case(
        name="empty list",
        args=([],),
        expected=0,
        note="No subarrays at all. The prefix value 0 still exists but there is no "
        "second one to pair it with.",
    ),
    Case(
        name="single zero",
        args=([0],),
        expected=0,
        note="One subarray, worth 0. Distinguishes 'no answer' from 'answer is 0'.",
    ),
    Case(
        name="single element",
        args=([7],),
        expected=7,
        note="Smallest non-trivial input: the only subarray is the whole list.",
    ),
    Case(
        name="all zeros",
        args=([0, 0, 0, 0],),
        expected=0,
        note="Ten subarrays, every one worth 0.",
    ),
    Case(
        name="two identical elements",
        args=([9, 9],),
        expected=18,
        note="9 + 9 + (9 ^ 9) = 18. The pair contributes nothing.",
    ),
    Case(
        name="largest allowed value, alone",
        args=([2**31 - 1],),
        expected=2**31 - 1,
        note="Every bit position up to 30 is in play at once.",
    ),
    Case(
        name="high bit, cancelling",
        args=([2**30, 2**30],),
        expected=2**31,
        note="The answer exceeds any single element and does not fit in 31 bits. "
        "Catches a solution that masks the running total.",
    ),
    Case(
        name="mixed small values",
        args=([1, 2, 3],),
        expected=10,
        note="1 + 2 + 3 + 3 + 1 + 0. The whole-list XOR is 0, which is easy to lose "
        "if the empty prefix is not counted.",
    ),
    Case(
        name="zeros around a value",
        args=([0, 5, 0],),
        expected=20,
        note="Four of the six subarrays contain the 5. Leading and trailing zeros "
        "extend subarrays without changing their XOR.",
    ),
    Case(
        name="distinct powers of two",
        args=([1, 2, 4, 8],),
        expected=72,
        note="No two subarrays share a value here, so nothing cancels - the "
        "opposite regime to the all-zeros case.",
    ),
    Case(
        name="perf: 10k elements, prefix XORs take two values",
        args=(A_NUMS,),
        expected=A_EXPECTED,
        time_limit_ms=1500,
        memory_limit_mb=128,
        note="The answer is (number of cross pairs) * V, known by construction. The "
        "budget rejects O(n^2): walking a running XOR outward from each of the "
        "10000 starts is 50 million iterations. V has bit 30 set, so bounding the "
        "bit loop by the largest value saves nothing.",
    ),
    Case(
        name="perf: 10k elements, prefix XORs take four values",
        args=(B_NUMS,),
        expected=B_EXPECTED,
        time_limit_ms=1500,
        memory_limit_mb=128,
        note="Same size, but the prefix values form a four-element set closed under "
        "XOR, so the six cross classes are counted independently - a stricter check "
        "that no bit position is dropped or double counted. Same O(n^2) rejection.",
    ),
]

if __name__ == "__main__":
    raise SystemExit(
        run_cases(
            total_subarray_xor, CASES, title="P014 - Total XOR Over Every Subarray"
        )
    )
