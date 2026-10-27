"""L03.5 - Shuffled Signature.

Read the problem in README.md, then fill in `find_shuffled` below.
Run the tests from the repo root with:  py run.py L3.5
"""

from typing import List


def find_shuffled(stream: str, signature: str) -> List[int]:
    """Return every start index where the stream holds a rearrangement of the signature.

    Args:
        stream: Lowercase letters a-z. May be empty.
        signature: Lowercase letters a-z, at least one letter. May be longer than
            the stream.

    Returns:
        Every index i, in increasing order, such that
        stream[i : i + len(signature)] has exactly the same letter counts as
        signature.
    """
    sign_map, window_map, size = {}, {}, len(signature)

    for ch in signature:
        sign_map[ch] = sign_map.get(ch, 0) + 1

    def is_shuffled_sign(word_map):
        for key, val in sign_map.items():
            if key not in word_map or word_map[key] != val:
                return False
        return len(word_map) == len(sign_map)

    for ch in stream[:size]:
        window_map[ch] = window_map.get(ch, 0) + 1

    li, sign_idxs = 0, []
    if is_shuffled_sign(window_map):
        sign_idxs.append(0)

    for enter in stream[size:]:
        window_map[enter] = window_map.get(enter, 0) + 1

        leave = stream[li]
        li += 1

        window_map[leave] -= 1
        if window_map[leave] == 0:
            del window_map[leave]

        if is_shuffled_sign(window_map):
            sign_idxs.append(li)
    return sign_idxs


