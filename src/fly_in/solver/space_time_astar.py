from ..graph import Graph
from .dijkstra import Dijkstra
from math import inf
from .constraint import Constraint, VertexConstraint, EdgeConstraint


class SpaceTimeAStar:
    def __init__(self, graph: Graph) -> None:
        self.__heuristic: dict[int, float] = Dijkstra().compute_distances(
            graph.end_node(),
            graph
        )
        self.__graph: Graph = graph

    def solve(
        self,
        start: int,
        goal: int,
        constraints: set[Constraint]
    ) -> list[int]:
        open_set: set[tuple[int, int]] = set()
        distances: dict[tuple[int, int], float] = {}
        parent: dict[tuple[int, int], tuple[int, int] | None] = {}

        # Start of the STA Algorithm
        start_stat: tuple[int, int] = (start, 0)
        distances[start_stat] = 0
        parent[start_stat] = None
        open_set.add(start_stat)

        while open_set:
            current_state: tuple[int, int] = self.__get_min(
                open_set,
                distances
            )
            current: int = current_state[0]
            current_t: int = current_state[1]
            current_g: float = distances[current_state]

            if current == goal:
                return self.__reconstruct_path(parent, current_state)

            # Move state
            neighbors: dict[
                int,
                int | None
            ] = self.__graph.neighbors(current).copy()
            # Wait state
            neighbors[current] = 1
            for neighbor, weight in neighbors.items():
                if weight is None:
                    continue

                next_t: int = current_t + weight
                next_state: tuple[int, int] = (neighbor, next_t)

                if self.__vertex_constraint(next_state, constraints):
                    continue
                if neighbor != current and self.__edge_constraint(
                    current,
                    neighbor,
                    next_t,
                    constraints
                ):
                    continue

                tentative_g: float = current_g + weight

                # Relaxation
                if tentative_g < distances.get(next_state, inf):
                    distances[next_state] = tentative_g
                    parent[next_state] = current_state
                    open_set.add(next_state)

        raise ValueError("Goal is Unreachable")

    def __vertex_constraint(
        self,
        state: tuple[int, int],
        constraints: set[Constraint]
    ) -> bool:
        vertex: VertexConstraint = VertexConstraint(
            node=state[0],
            time=state[1]
        )

        if vertex in constraints:
            return True

        return False

    def __edge_constraint(
        self,
        current_node: int,
        next_node: int,
        time: int,
        constraints: set[Constraint]
    ) -> bool:
        edge: EdgeConstraint = EdgeConstraint(
            from_node=current_node,
            to_node=next_node,
            time=time
        )

        if edge in constraints:
            return True

        return False

    def __get_min(
        self,
        open_set: set[tuple[int, int]],
        distances: dict[tuple[int, int], float]
    ) -> tuple[int, int]:
        m, mt = min(
            open_set,
            key=lambda state: (
                distances[state] +
                self.__heuristic[state[0]]
            )
        )

        open_set.remove((m, mt))

        return (m, mt)

    def __reconstruct_path(
        self,
        parent: dict[tuple[int, int], tuple[int, int] | None],
        current: tuple[int, int]
    ) -> list[int]:
        node: tuple[int, int] | None = current
        path: list[int] = []

        while node is not None:
            path.append(node[0])
            node = parent[node]

        path.reverse()
        return path
