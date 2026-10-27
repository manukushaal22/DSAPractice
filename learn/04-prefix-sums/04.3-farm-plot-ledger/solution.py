"""L04.3 - Farm Plot Ledger.

Read the problem in README.md, then fill in `plot_totals` below.
Run the tests from the repo root with:  py run.py L4.3
"""

from typing import List, Tuple


def plot_totals(
    ledger: List[List[int]], queries: List[Tuple[int, int, int, int]]
) -> List[int]:
    """Return the total of each rectangular block of plots.

    Args:
        ledger: R x C grid of plot results (R, C >= 1). Must not be modified.
        queries: (r1, c1, r2, c2) tuples, inclusive on both ends, with
            r1 <= r2 and c1 <= c2. May be empty.

    Returns:
        One total per query, in query order.
    """
    # TODO: implement me
    raise NotImplementedError
