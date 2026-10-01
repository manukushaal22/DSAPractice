"""P013 - Shortest Root Replacement.

Read the problem in README.md, then fill in `replace_with_shortest_root` below.
Run the tests from the repo root with:  py run.py 13
"""

from typing import List

class TrieNode:
    def __init__(self):
        self.children = [None for _ in range(26)]
        self.word = False

    def insert(self, word):
        cur = self
        for ch in word:
            edgeidx = ord(ch)-ord('a')
            if cur.children[edgeidx] is None:
                cur.children[edgeidx] = TrieNode()
            cur = cur.children[edgeidx]
        cur.word = True

    def get_shortest_prefix(self, word):
        cur = self
        prefix = ""
        for ch in word:
            edgeidx = ord(ch)-ord('a')
            if cur.children[edgeidx] is None:
                return word
            cur = cur.children[edgeidx]
            prefix += ch
            if cur.word: return prefix
        return word




def replace_with_shortest_root(roots: List[str], sentence: str) -> str:
    """Replace every word covered by a root with the shortest root covering it.

    A root covers a word when the word starts with that root; a root covers a
    word equal to it as well. Words covered by no root are left unchanged.

    Args:
        roots: Lowercase root strings, possibly empty, possibly with duplicates.
            Must not be modified or reordered.
        sentence: Either ``""`` or lowercase words joined by single spaces, with
            no leading or trailing space. Must not be modified.

    Returns:
        The rewritten sentence, words in their original order joined by single
        spaces.
    """
    trie = TrieNode()
    for root in roots:
        trie.insert(root)
    return " ".join(list(map(trie.get_shortest_prefix, sentence.split())))
