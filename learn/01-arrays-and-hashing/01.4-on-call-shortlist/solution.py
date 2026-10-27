"""L01.4 - On-Call Shortlist.

Read the problem in README.md, then fill in `shortlist` below.
Run the tests from the repo root with:  py run.py L1.4
"""

from typing import List
from collections import Counter, defaultdict


def shortlist(codes: List[int], k: int) -> List[int]:
    """Return the k codes with the most incidents in the log.

    Args:
        codes: Error codes, one per incident. Non-empty; may contain negatives and
            repeats. Must not be modified.
        k: How many codes to shortlist, between 1 and the number of distinct codes.
            The k-th busiest code is guaranteed to have strictly more incidents than
            the (k + 1)-th, so the answer is unique.

    Returns:
        The k busiest codes, in any order.
    """
    code_to_count = Counter(codes)
    count_to_code = defaultdict(list)
    for code, count in code_to_count.items():
        count_to_code[count].append(code)
    result = []
    for count in range(len(codes), -1, -1):
        result += count_to_code[count]
        if len(result) == k:
            return result
        if len(result) > k:
            raise Exception("Not possible")
    return result
