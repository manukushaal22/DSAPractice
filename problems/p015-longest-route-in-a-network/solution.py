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
    adj = [[] for _ in range(n)]
    for a, b, w in links:
        adj[a].append((b, w))
        adj[b].append((a, w))

    def sweep(start):
        dist = [-1] * n
        dist[start] = 0
        stack = [start]
        far, best = start, 0
        while stack:
            u = stack.pop()
            du = dist[u]
            if du > best:
                best, far = du, u
            for v, w in adj[u]:
                if dist[v] < 0:
                    dist[v] = du + w
                    stack.append(v)
        return far, best

    u, _ = sweep(0)
    _, diameter = sweep(u)
    return diameter
