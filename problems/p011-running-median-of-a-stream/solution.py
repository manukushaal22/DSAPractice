"""P011 - Running Median of a Stream.

Read the problem in README.md, then fill in `running_medians` below.
Run the tests from the repo root with:  py run.py 11
"""

from typing import List
import heapq


def running_medians(nums: List[int]) -> List[float]:
    """Return the median of every prefix of the stream.

    Entry ``i`` of the result is the median of ``nums[: i + 1]``. With an even
    number of readings the median is the average of the two middle values, so
    the result can hold halves.

    Args:
        nums: The readings in arrival order. May be empty. Must not be modified.

    Returns:
        A list of the same length as ``nums`` holding the running medians.
    """
    low_max, high_min, result = [], [], []
    for ele in nums:
        if len(low_max) == 0:
            # first element
            heapq.heappush(low_max, -ele)
            median = ele/1
            result.append(median)
            continue
        elif len(high_min) == 0:
            # second element
            heapq.heappush(high_min, ele)
            median = (median+ele)/2
            result.append(median)
            continue

        if median is None or ele <= median:
            if len(low_max) == len(high_min):
                heapq.heappush(low_max, -ele)
            elif len(low_max)-1 == len(high_min) :
                pop_low_max = -heapq.heappop(low_max)
                heapq.heappush(high_min, pop_low_max)
                heapq.heappush(low_max, -ele)
            else:
                raise Exception(f"Unexpected state: ele:{ele}, median:{median}, low_max:{low_max}, high_min:{high_min}")
        else:
            if len(low_max) == len(high_min):
                pop_high_min = heapq.heappop(high_min)
                heapq.heappush(low_max, -pop_high_min)
                heapq.heappush(high_min, ele)
            elif len(low_max)-1 == len(high_min) :
                heapq.heappush(high_min, ele)
            else:
                raise Exception(f"Unexpected state: ele:{ele}, median:{median}, low_max:{low_max}, high_min:{high_min}")

        if len(low_max)-1 == len(high_min):
            median = -low_max[0]/1
        else:
            median = (high_min[0]-low_max[0])/2
        result.append(median)
    return result


