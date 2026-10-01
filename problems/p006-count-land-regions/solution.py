"""P006 - Count Land Regions.

Read the problem in README.md, then fill in `count_regions` below.
Run the tests from the repo root with:  py run.py 6
"""

from typing import List

def explore(grid, i0, j0):
    queue = [(i0,j0)]
    vis = set()
    while len(queue) > 0:
        i, j = queue.pop(0)
        if  i >= len(grid) or  j >= len(grid[0]) or i<0 or j<0 or grid[i][j] == 0 or (i,j) in vis:
            continue
        vis.add((i,j))
        if (i+1, j) not in vis: queue.append((i+1, j))
        if (i-1, j) not in vis: queue.append((i-1, j))
        if (i, j+1) not in vis: queue.append((i, j+1))
        if (i, j-1) not in vis: queue.append((i, j-1))

def count_regions(grid: List[List[int]]) -> int:
    """Count maximally connected regions of land in a grid.

    Cells are connected only up, down, left and right - never diagonally.

    Args:
        grid: A rectangular grid of 0 (water) and 1 (land). May be empty, and may
            contain rows of length zero. Must not be modified.

    Returns:
        The number of distinct land regions.
    """
    val = -1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                explore(grid, i, j)
                val -= 1
    return -val-1
