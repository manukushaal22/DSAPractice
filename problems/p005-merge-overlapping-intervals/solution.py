"""P005 - Merge Overlapping Intervals.

Read the problem in README.md, then fill in `merge_intervals` below.
Run the tests from the repo root with:  py run.py 5
"""

from typing import List

class Interval:
    def __init__(self, start: int, end: int):
        self.start, self.end = start, end

    def __str__(self):
        return f"[{self.start}, {self.end}]"

    def is_overlapping(self, other: Interval) -> bool:
        return self.start <= other.start <= self.end or self.start <= other.end <= self.end or (self.start >= other.start and self.end <= other.end)

    def merge(self, other: Interval) -> Interval:
        if not self.is_overlapping(other):
            raise Exception(f"Error: Cannot merge non-overlapping -intervals: {self}, {other}")
        return Interval(min(self.start, other.start), max(self.end, other.end))

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """Merge all overlapping closed intervals.

    Args:
        intervals: A list of [start, end] pairs with start <= end, in arbitrary
            order. Neither the outer list nor the inner lists may be modified.

    Returns:
        The merged, non-overlapping intervals as [start, end] lists, ordered by
        start. Intervals that merely touch at a single point are merged.
    """
    if len(intervals) == 0:
        return intervals
    intervals = [Interval(i[0], i[1]) for i in intervals]
    intervals.sort(key=lambda x: (x.start, x.end))
    merged = [intervals[0]]
    for interval in intervals[1:]:
        if interval.is_overlapping(merged[-1]):
            merged[-1] = interval.merge(merged[-1])
        else:
            merged.append(interval)
    return [[i.start, i.end] for i in merged]
