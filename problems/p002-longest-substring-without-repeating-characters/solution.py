"""P002 - Longest Substring Without Repeating Characters.

Read the problem in README.md, then fill in `length_of_longest_substring` below.
Run the tests from the repo root with:  py run.py 2
"""


def length_of_longest_substring(s: str) -> int:
    """Return the length of the longest substring of `s` with no repeated character.

    Args:
        s: A string of printable ASCII characters. May be empty.

    Returns:
        The length of the longest contiguous substring in which every character
        is distinct, or 0 if `s` is empty.
    """
    if len(s) < 2:
        return len(s)

    i, j = 0, 1
    window = {s[0]: 0}
    maxlen = 1
    while j < len(s):
        if s[j] in window and window[s[j]] >= i:
            i = window[s[j]]+1
        window[s[j]] = j
        j += 1
        maxlen = max(j-i, maxlen)
    return maxlen
