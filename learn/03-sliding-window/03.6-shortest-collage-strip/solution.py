"""L03.6 - Shortest Collage Strip.

Read the problem in README.md, then fill in `shortest_strip` below.
Run the tests from the repo root with:  py run.py L3.6
"""

def shortest_strip(line: str, message: str) -> str:
    """Return the shortest strip of line that holds every letter the message needs.

    Args:
        line: Upper- and lowercase letters. May be empty.
        message: Upper- and lowercase letters, at least one letter. Case matters.

    Returns:
        The shortest contiguous piece of line whose letter counts cover the
        message's letter counts. If several are equally short, the one that
        starts first. An empty string if no piece works.
    """
    msg_map = {}
    for ch in message:
        msg_map[ch] = msg_map.get(ch, 0) + 1

    li = 0
    strip = {}
    missing = len(message)
    rf, lf = None, None
    for ri, ch in enumerate(line):
        strip[ch] = strip.get(ch, 0) + 1
        if ch in msg_map and strip[ch] <= msg_map[ch]:
            missing -= 1

        while missing == 0:
            if rf is None or lf is None or ri - li < rf - lf:
                lf, rf = li, ri
            remove_ch = line[li]
            if remove_ch in msg_map and strip[remove_ch] <= msg_map[remove_ch]:
                missing += 1
            strip[remove_ch] -= 1
            if strip[remove_ch] == 0:
                del strip[remove_ch]
            li += 1

    if rf is None or lf is None:
        return ""
    return line[lf:rf+1]

