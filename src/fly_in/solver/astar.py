from ..graph import Graph, WorldState
from math import inf


class AStar:
    def solve(
        self,
        graph: Graph,
        world: WorldState,
        source: int,
        goal: int,
        heuristic: dict[int, float]
    ) -> list[int]:
        open_set: set[int] = set()
        parents: dict[int, int | None] = {}
        distances: dict[int, float] = {}
        f_score: dict[int, float] = {}

        # Initialization of data
        distances = {
            node: inf
            for node in graph.get_nodes()
        }
        parents = {
            node: None
            for node in graph.get_nodes()
        }
        f_score = {
            node: inf
            for node in graph.get_nodes()
        }

        # Start of the A* algorithm
        distances[source] = 0
        open_set.add(source)
        f_score[source] = distances[source] + heuristic[source]

        while open_set:
            open_set, current = self.__remove_smallest_f(open_set, f_score)

            if current == goal:
                return self.__reconstruct_path(parents, goal)

            for neighbor, weight in graph.neighbors(current).items():
                if weight is None:
                    continue

                if not self.__is_avaliable_node(neighbor, world):
                    continue

                tentative_g: float = distances[current] + weight
                if tentative_g < distances[neighbor]:
                    distances[neighbor] = tentative_g
                    parents[neighbor] = current
                    f = tentative_g + heuristic[neighbor]
                    f_score[neighbor] = f
                    open_set.add(neighbor)

        return []
        # raise ValueError("Goal is Unreachable")

    def __remove_smallest_f(
        self,
        open_set: set[int],
        f_score: dict[int, float]
    ) -> tuple[set[int], int]:
        current: int = min(
            open_set,
            key=lambda x: f_score[x]
        )
        open_set.remove(current)

        return open_set, current

    def __reconstruct_path(
        self,
        parents: dict[int, int | None],
        current: int
    ) -> list[int]:
        node: int | None = current
        path: list[int] = []

        while node is not None:
            path.append(node)
            node = parents[node]

        path.reverse()
        return path

    def __is_avaliable_node(
        self,
        node: int,
        world: WorldState
    ) -> bool:
        if world.get_node_avaliable_capacity(node) <= 0:
            return False
        return True
