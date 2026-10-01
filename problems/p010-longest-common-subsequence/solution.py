"""P010 - Longest Common Subsequence.

Read the problem in README.md, then fill in `lcs_length` below.
Run the tests from the repo root with:  py run.py 10
"""


def lcs_length(a: str, b: str) -> int:
    """Return the length of the longest subsequence common to `a` and `b`.

    A subsequence keeps the original order but may skip characters.

    Args:
        a: First string. May be empty.
        b: Second string. May be empty.

    Returns:
        The length of the longest common subsequence, or 0 if there is none.
    """

    return dp(a,b,len(a),len(b))

def dp(a, b, ai, bi, hm={}):
    '''
    dp() gives lcs until ai, bi such that subseq includes ai, bi
    '''
    if ai==0 or bi==0: return 0
    if (ai,bi) in hm: return hm[(ai,bi)]
    if a[ai-1] == b[bi-1]:
        ans = 1+dp(a,b,ai-1,bi-1, hm)
    else:
        ans = max(dp(a,b,ai-1,bi, hm), dp(a,b,ai,bi-1, hm))
    hm[(ai,bi)] = ans
    return ans



