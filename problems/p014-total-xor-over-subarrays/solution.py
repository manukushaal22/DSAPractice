"""P014 - Total XOR Over Every Subarray.

Read the problem in README.md, then fill in `total_subarray_xor` below.
Run the tests from the repo root with:  py run.py 14
"""

from typing import List


def total_subarray_xor(nums: List[int]) -> int:
    """Return the sum of the bitwise XOR of every subarray of ``nums``.

    Every run of one or more neighbouring elements counts as a subarray, and
    two runs at different positions count separately even if they hold the
    same values.

    Args:
        nums: Non-negative integers below ``2 ** 31``. May be empty. Must not
            be modified or reordered.

    Returns:
        The sum of the XORs of all subarrays, or ``0`` when ``nums`` is empty.
    """
    if not nums: return 0
    prefix = list(nums)
    for i in range(1, len(nums)):
        prefix[i] = prefix[i] ^ prefix[i-1]

    def sub_xor(i, j):
        if not 0 <= i <= j < len(prefix):
            raise Exception(f"invalid index for sub_arr:{i}, {j}, {prefix}")
        if i == 0:
            return prefix[j]
        return prefix[j] ^ prefix[i-1]

    total = 0
    bit = 0
    while prefix.count(0) != len(prefix):
        ones = 0
        for i in range(len(prefix)):
            if prefix[i] & 1 == 1:
                ones += 1
            prefix[i] = prefix[i]>>1
        total += ones * (len(prefix) - ones + 1) * (1 << bit)
        bit += 1

    return total

