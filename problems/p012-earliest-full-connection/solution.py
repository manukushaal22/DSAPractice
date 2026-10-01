"""P012 - Earliest Full Connection.

Read the problem in README.md, then fill in `earliest_full_connection` below.
Run the tests from the repo root with:  py run.py 12
"""

from typing import List

def find_root(parent, x):
    if x >= len(parent):
        raise Exception(f"Invalid index x:{x}, parent:{parent}")
    if x == parent[x]:
        return x
    return find_root(parent, parent[x])

def set_root(parent, groups, ele, root):
    for child in groups[ele]:


def earliest_full_connection(n: int, logs: List[List[int]]) -> int:
    """Return the earliest timestamp at which all members share one group.

    Members are labelled ``0`` to ``n - 1`` and start in groups of their own.
    Each entry ``[timestamp, a, b]`` merges the groups of ``a`` and ``b``.
    Acquaintance is transitive, so groups only ever merge, never split.

    Args:
        n: Number of members, at least 2.
        logs: Entries ``[timestamp, a, b]`` in arbitrary order. May be empty,
            may repeat a pair, may have ``a == b``, and may repeat a
            timestamp. Must not be modified or reordered.

    Returns:
        The smallest timestamp ``T`` such that the entries with timestamp
        ``<= T`` leave every member in a single group, or ``-1`` if no such
        timestamp exists.
    """
    logs.sort(key=lambda x:x[0])
    parent = list(range(n))
    group = {i:{i,} for i in range(n)}
    for arr in logs:
        t, a, b = tuple(arr)
        a_root = find_root(parent, a)
        b_root = find_root(parent, b)
        root = min(a_root, b_root)
        set_root(parent, group, a, root)
        parent[a], parent[b] = root, root
        group[root]
    for
    return -1

