"""Node types for linked-list and binary-tree exercises.

The harness deep-copies every case's arguments before each call. The default
``copy.deepcopy`` recurses once per node, so a plain node class blows the
recursion limit on a few hundred nodes. These classes copy themselves
iteratively, cope with cycles, and print a bounded ``repr`` so a failing case
on a 100k-node input does not flood the terminal.

Tests build inputs with :func:`build_list` / :func:`build_tree` and compare
outputs with ``cmp=`` plus :func:`list_values` / :func:`tree_values`.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Iterable, Optional

REPR_LIMIT = 40


class ListNode:
    """Singly linked list node: ``val`` and ``next``."""

    __slots__ = ("val", "next")

    def __init__(self, val: Any = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next

    def __deepcopy__(self, memo: dict) -> "ListNode":
        import copy

        if id(self) in memo:
            return memo[id(self)]
        head = ListNode(copy.deepcopy(self.val, memo))
        memo[id(self)] = head
        source, tail = self.next, head
        while source is not None:
            existing = memo.get(id(source))
            if existing is not None:  # cycle, or a node already copied elsewhere
                tail.next = existing
                break
            node = ListNode(copy.deepcopy(source.val, memo))
            memo[id(source)] = node
            tail.next = node
            tail, source = node, source.next
        return head

    def __repr__(self) -> str:
        parts, seen, node = [], set(), self
        while node is not None and len(parts) < REPR_LIMIT:
            if id(node) in seen:
                parts.append(f"(cycle back to {node.val!r})")
                break
            seen.add(id(node))
            parts.append(repr(node.val))
            node = node.next
        else:
            if node is not None:
                parts.append("...")
        return "ListNode[" + " -> ".join(parts) + "]"


class TreeNode:
    """Binary tree node: ``val``, ``left`` and ``right``."""

    __slots__ = ("val", "left", "right")

    def __init__(
        self,
        val: Any = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right

    def __deepcopy__(self, memo: dict) -> "TreeNode":
        import copy

        if id(self) in memo:
            return memo[id(self)]
        root = TreeNode(copy.deepcopy(self.val, memo))
        memo[id(self)] = root
        stack = [(self, root)]
        while stack:
            source, target = stack.pop()
            for side in ("left", "right"):
                child = getattr(source, side)
                if child is None:
                    continue
                existing = memo.get(id(child))
                if existing is None:
                    existing = TreeNode(copy.deepcopy(child.val, memo))
                    memo[id(child)] = existing
                    stack.append((child, existing))
                setattr(target, side, existing)
        return root

    def __repr__(self) -> str:
        values = tree_values(self, limit=REPR_LIMIT)
        text = ", ".join("None" if v is None else repr(v) for v in values)
        return f"TreeNode[{text}{', ...' if len(values) >= REPR_LIMIT else ''}]"


def build_list(values: Iterable[Any], cycle_to: Optional[int] = None) -> Optional[ListNode]:
    """Build a linked list from ``values``.

    ``cycle_to`` links the last node back to the node at that index, for cycle
    problems. Returns ``None`` for an empty input.
    """
    head: Optional[ListNode] = None
    tail: Optional[ListNode] = None
    nodes: list[ListNode] = []
    for value in values:
        node = ListNode(value)
        if cycle_to is not None:
            nodes.append(node)
        if tail is None:
            head = node
        else:
            tail.next = node
        tail = node
    if cycle_to is not None and tail is not None:
        tail.next = nodes[cycle_to]
    return head


def list_values(head: Optional[ListNode], limit: Optional[int] = None) -> list[Any]:
    """Values of a linked list in order. Raises ``ValueError`` on a cycle."""
    values: list[Any] = []
    seen: set[int] = set()
    node = head
    while node is not None:
        if limit is not None and len(values) >= limit:
            break
        if id(node) in seen:
            raise ValueError("linked list contains a cycle")
        seen.add(id(node))
        values.append(node.val)
        node = node.next
    return values


def build_tree(values: Iterable[Any]) -> Optional[TreeNode]:
    """Build a binary tree from level-order values, ``None`` marking a gap.

    ``[1, None, 2, 3]`` is 1 with right child 2, whose left child is 3. This is
    the same encoding :func:`tree_values` produces.
    """
    items = list(values)
    if not items or items[0] is None:
        return None
    root = TreeNode(items[0])
    queue = deque([root])
    i = 1
    while queue and i < len(items):
        node = queue.popleft()
        if i < len(items) and items[i] is not None:
            node.left = TreeNode(items[i])
            queue.append(node.left)
        i += 1
        if i < len(items) and items[i] is not None:
            node.right = TreeNode(items[i])
            queue.append(node.right)
        i += 1
    return root


def tree_values(root: Optional[TreeNode], limit: Optional[int] = None) -> list[Any]:
    """Level-order values with ``None`` gaps, trailing ``None``s trimmed."""
    values: list[Any] = []
    queue = deque([root])
    while queue:
        if limit is not None and len(values) >= limit:
            break
        node = queue.popleft()
        if node is None:
            values.append(None)
            continue
        values.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while values and values[-1] is None:
        values.pop()
    return values
