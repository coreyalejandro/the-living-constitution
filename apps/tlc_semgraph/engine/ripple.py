from __future__ import annotations

from collections import deque


def ripple_bfs(
    edges: dict[str, set[str]],
    start_nodes: set[str],
    *,
    max_depth: int = 2,
    hub_degree_threshold: int = 250,
) -> set[str]:
    if max_depth < 0:
        return set()

    visited: set[str] = set()
    q: deque[tuple[str, int]] = deque()

    for n in start_nodes:
        visited.add(n)
        q.append((n, 0))

    while q:
        node, depth = q.popleft()
        if depth >= max_depth:
            continue

        neighbors = edges.get(node, set())
        if len(neighbors) >= hub_degree_threshold:
            continue

        for nxt in neighbors:
            if nxt in visited:
                continue
            visited.add(nxt)
            q.append((nxt, depth + 1))

    return visited

