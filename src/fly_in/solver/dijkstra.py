"""Dijkstra shortest-path distances used as a search heuristic."""

from ..graph import Graph
from math import inf


class Dijkstra:
    """Computes shortest-path distances from a source node to all nodes."""

    def compute_distance(
        self,
        graph: Graph,
        source: int,
        goal: int
    ) -> dict[int, float]:
        """Compute the shortest distance from source to every graph node.

        Args:
            graph (Graph): Graph to search.
            source (int): Node id to compute distances from.
            goal (int): Unused target node id, kept for interface symmetry.

        Returns:
            dict[int, float]: Shortest distance from source to each node.
        """
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
                continue

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
        """Pop the unvisited node with the smallest known distance.

        Args:
            unvisited (set[int]): Nodes not yet finalized.
            distances (dict[int, float]): Current best distance per node.

        Returns:
            int: The unvisited node with the smallest distance.
        """
        find: int = min(
            unvisited,
            key=lambda x: distances[x]
        )
        unvisited.remove(find)
        return find
