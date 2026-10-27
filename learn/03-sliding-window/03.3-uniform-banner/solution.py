"""L03.3 - Uniform Banner.

Read the problem in README.md, then fill in `longest_uniform` below.
Run the tests from the repo root with:  py run.py L3.3
"""
def longest_uniform(s: str, k: int) -> int:
    """Return the longest single-letter stretch achievable with at most k repaints.

    Args:
        s: Uppercase letters A-Z. May be empty.
        k: The most letters that may be repainted, between 0 and len(s).

    Returns:
        The length of the longest contiguous stretch that can be made uniform by
        repainting at most k of its letters.
    """
    counts, max_len, li = {}, 0, 0
    for ri in range(len(s)):
        counts[s[ri]] = counts.get(s[ri], 0) + 1
        to_repaint = ri-li+1 - max(counts.values())
        while to_repaint > k:
            counts[s[li]] -= 1
            li += 1
            to_repaint = ri-li+1 - max(counts.values())
        max_len = max(max_len, ri-li+1)
    return max_len
