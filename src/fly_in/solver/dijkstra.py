from ..graph import Graph
from math import inf


class Dijkstra:
    def solve(
        self,
        start: int,
        goal: int,
        graph: Graph
    ) -> tuple[float, list[int]]:
        distances: dict[int, float] = {
            node: inf
            for node in graph.get_nodes()
        }
        parent: dict[int, int | None] = {
            node: None
            for node in graph.get_nodes()
        }
        unvisited: set[int] = set(graph.get_nodes())

        # Initialization of the algorithm
        distances[start] = 0
        parent[start] = None

        # Core of the algorithm
        while unvisited:
            current: int = self.__get_smallest_dist(unvisited, distances)

            if distances[current] == inf:
                raise ValueError("Goal is Unreachable")

            # Updating unvisited stack
            unvisited.remove(current)

            if current == goal:
                return (
                    distances[goal],
                    self.__reconstruct_path(parent, goal, distances)
                )

            for neighbor, weight in graph.neighbors(current).items():
                if weight is None:
                    continue
                if neighbor in unvisited:
                    # Relaxation
                    if distances[current] + weight < distances[neighbor]:
                        distances[neighbor] = distances[current] + weight
                        parent[neighbor] = current

        raise ValueError("Goal is Unreachable")

    def __get_smallest_dist(
        self,
        unvisited: set[int],
        distances: dict[int, float]
    ) -> int:
        return min(unvisited, key=lambda x: distances[x])

    def __reconstruct_path(
        self,
        parent: dict[int, int | None],
        goal: int,
        distances: dict[int, float]
    ) -> list[int]:
        node: int | None = goal
        path: list[int] = []

        while node is not None:
            path.append(node)
            node = parent[node]

        path.reverse()
        return path

    def compute_distances(self, start: int, graph: Graph) -> dict[int, float]:
        distances: dict[int, float] = {
            node: inf
            for node in graph.get_nodes()
        }
        unvisited: set[int] = set(graph.get_nodes())

        # Initialization of the algorithm
        distances[start] = 0

        # Core of the algorithm
        while unvisited:
            current: int = self.__get_smallest_dist(unvisited, distances)

            if distances[current] == inf:
                raise ValueError("Goal is Unreachable")

            # Updating unvisited stack
            unvisited.remove(current)

            for neighbor, weight in graph.neighbors(current).items():
                if weight is None:
                    continue
                if neighbor in unvisited:
                    # Relaxation
                    if distances[current] + weight < distances[neighbor]:
                        distances[neighbor] = distances[current] + weight

        return distances
