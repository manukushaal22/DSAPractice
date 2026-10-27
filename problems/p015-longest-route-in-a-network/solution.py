"""P015 - Longest Route in a Network.

Read the problem in README.md, then fill in `longest_route` below.
Run the tests from the repo root with:  py run.py 15
"""

from typing import List


def longest_route(n: int, links: List[List[int]]) -> int:
    """Return the largest latency between any two stations in the network.

    The ``n`` stations and ``n - 1`` cables form a tree, so exactly one route
    joins any pair of stations, and a route's latency is the total weight of
    the cables along it.

    Args:
        n: Number of stations, at least 1.
        links: Cables ``[a, b, w]`` in arbitrary order, with the endpoints in
            either order. Must not be modified or reordered.

    Returns:
        The largest latency over all pairs of stations, or ``0`` when there is
        only one station.
    """
    # TODO: implement me
    raise NotImplementedError
