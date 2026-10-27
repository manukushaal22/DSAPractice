"""L01.3 - Group Rearranged Words.

Read the problem in README.md, then fill in `group_rearranged` below.
Run the tests from the repo root with:  py run.py L1.3
"""

from typing import List


def group_rearranged(words: List[str]) -> List[List[str]]:
    """Group words that are rearrangements of each other.

    Args:
        words: Lowercase words, possibly empty strings, possibly repeated. Must not
            be modified.

    Returns:
        A list of groups, each a list of words. Two words share a group exactly
        when they use the same letters the same number of times. Every input word
        appears exactly once; group order and order within a group are free.
    """
    groups = {}
    for word in words:
        key = "".join(sorted(word))
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    return list(groups.values())
