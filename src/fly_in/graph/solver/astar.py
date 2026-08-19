from ..graph import Graph
from math import inf


class AStar:
    def solve(self, graph: Graph) -> list[int]:
        distances: dict[int, float] = {
            node: inf
            for node in graph.get_nodes()
        }
        parent: dict[int, int | None] = {
            node: None
            for node in graph.get_nodes()
        }
        open_set: set[int] = set()
        f_score: dict[int, float] = {}

        # Start of the AStar algorigthm
        source: int = graph.start_node()
        goal: int = graph.end_node()
        distances[source] = 0
        parent[source] = None
        open_set.add(source)
        f_score[source] = distances[source] + self.__heuristic(
            graph.get_node_position(source),
            graph.get_node_position(goal)
        )

        while open_set:
            open_set, current = self.__remove_smallest_f(open_set, f_score)

            if current == goal:
                return self.__reconstruct_path(parent, goal)

            for neighbor, weight in graph.neighbors(current).items():
                tentative_g: float = distances[current] + weight
                if tentative_g < distances[neighbor]:
                    distances[neighbor] = tentative_g
                    parent[neighbor] = current
                    f = tentative_g + self.__heuristic(
                        graph.get_node_position(neighbor),
                        graph.get_node_position(goal)
                    )
                    f_score[neighbor] = f
                    open_set.add(neighbor)

        raise ValueError("Impossible to go to the end")

    def __remove_smallest_f(
        self,
        open_set: set[int],
        f_score: dict[int, float]
    ) -> tuple[set[int], int]:
        current_min: int = min(
            open_set,
            key=lambda score: f_score[score]
        )
        open_set.remove(current_min)
        return open_set, current_min

    def __heuristic(
        self,
        pos1: tuple[int, int],
        pos2: tuple[int, int]
    ) -> float:
        x1, y1 = pos1
        x2, y2 = pos2
        return (
            abs(x1 - x2) + abs(y1 - y2)
        )

    def __reconstruct_path(
        self,
        parent: dict[int, int | None],
        current: int
    ) -> list[int]:
        node: int | None = current
        path: list[int] = []

        while node is not None:
            path.append(node)
            node = parent[node]

        path.reverse()
        return path
