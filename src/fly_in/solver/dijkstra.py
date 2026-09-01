from ..graph import Graph
from math import inf
from ..utils import SolverError


class Dijkstra:
    def compute_distance(
        self,
        graph: Graph,
        source: int,
        goal: int
    ) -> dict[int, float]:
        unvisited: set[int] = set()
        distances: dict[int, float] = {}

        # Initialization of data
        unvisited = set(graph.get_nodes())
        distances = {
            node: inf
            for node in graph.get_nodes()
        }

        # Start of the Dijkstra algorithm
        # Compute every distances from source to goal
        distances[source] = 0

        while unvisited:
            current = self.__remove_smallest_dist(unvisited, distances)

            if distances[current] == inf:
                raise SolverError("Goal is Unreachable")

            for neighbor, weight in graph.neighbors(current).items():
                if neighbor in unvisited:
                    if weight is None:
                        continue

                    # Relaxation
                    if distances[current] + weight < distances[neighbor]:
                        distances[neighbor] = distances[current] + weight

        return distances

    def __remove_smallest_dist(
        self,
        unvisited: set[int],
        distances: dict[int, float]
    ) -> int:
        find: int = min(
            unvisited,
            key=lambda x: distances[x]
        )
        unvisited.remove(find)
        return find
