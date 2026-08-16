from ..graph import Graph
from collections import deque
from typing import Deque


class BFS:
    def __reconstruct_path(
        self,
        parent: dict[int, int | None],
        goal: int
    ) -> list[int]:
        node: int | None = goal
        path: list[int] = []

        while node is not None:
            path.append(node)
            node = parent[node]

        path.reverse()
        return path

    def solve(
        self,
        graph: Graph
    ) -> list[int]:
        visited: set[int] = set()
        parent: dict[int, int | None] = {}
        queue: Deque[int] = deque()

        # Start of the BFS Algorithm
        start: int = graph.start_zone()
        goal: int = graph.end_zone()
        visited.add(start)
        parent[start] = None
        queue.append(start)

        while queue:
            current = queue.popleft()

            if current == goal:
                return self.__reconstruct_path(parent, goal)

            for neighbor in graph.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        raise ValueError("Impossible to go to the end")
