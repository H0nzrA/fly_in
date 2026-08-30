from ..graph import Graph, WorldState, State
from math import inf


Cost = tuple[float, int]  # turn, -priority


class SpacetimeAStar:
    def __init__(self, graph: Graph) -> None:
        self.__graph: Graph = graph

    def __data_init(self, time: int) -> tuple[
        set[State],
        dict[State, State | None],
        dict[State, Cost],
        dict[State, Cost]
    ]:
        open_set: set[State] = set()
        parent: dict[State, State | None] = {
            (node, time): None
            for node in self.__graph.get_nodes()
        }
        distances: dict[State, Cost] = {
            (node, time): (inf, 0)
            for node in self.__graph.get_nodes()
        }
        f_scores: dict[State, Cost] = {
            (node, time): (inf, 0)
            for node in self.__graph.get_nodes()
        }

        return open_set, parent, distances, f_scores

    def solve(
        self,
        world: WorldState,
        source: int,
        goal: int,
        time: int,
        heuristic: dict[int, float]
    ) -> list[State]:
        open_set, parent, distances, f_scores = self.__data_init(time)

        # Start consideration
        start_state: State = (source, time)
        parent[start_state] = None
        distances[start_state] = (0, 0)
        f_scores[start_state] = (heuristic[source], 0)
        open_set.add(start_state)

        while open_set:
            current_state: State = self.__remove_smallest_f(
                open_set,
                f_scores
            )
            c_node: int = current_state[0]
            c_time: int = current_state[1]
            c_g, c_cost = distances[current_state]

            if c_node == goal:
                return self.__reconstruct_path(
                    parent,
                    current_state
                )

            neighbors: dict[int, int | None] = self.__graph.neighbors(c_node)
            neighbors[c_node] = 1

            for neighbor, weight in neighbors.items():
                if weight is None:
                    continue

                next_time: int = c_time + weight
                next_state: State = (neighbor, next_time)

                if not self.__is_avaliable(
                    current_state,
                    next_state,
                    world
                ):
                    continue

                # Relaxation
                tentative_weight: float = c_g + weight
                tentative_cost: int = c_cost - self.__priority_cost(
                    c_node,
                    neighbor
                )
                tentative_g: Cost = (tentative_weight, tentative_cost)
                if tentative_g < distances.get(next_state, (inf, 0)):
                    distances[next_state] = tentative_g
                    parent[next_state] = current_state
                    open_set.add(next_state)
                    f_scores[next_state] = (
                        tentative_weight + heuristic[neighbor],
                        tentative_cost
                    )

        raise ValueError("Goal is Unreachable")

    def __is_avaliable(
        self,
        current_state: State,
        next_state: State,
        world: WorldState
    ) -> bool:
        c_node, c_time = current_state
        neighbor, next_time = next_state

        if not world.node_avaliable(
            neighbor,
            next_time,
            self.__graph.get_node_capacity(neighbor)
        ):
            return False

        if c_node == neighbor:
            return True

        for time in range(c_time, next_time):
            if not world.edge_avaliable(
                c_node,
                neighbor,
                time,
                self.__graph.get_edge_capacity(c_node, neighbor)
            ):
                return False

        return True

    def __remove_smallest_f(
        self,
        open_set: set[State],
        f_scores: dict[State, Cost]
    ) -> State:
        min_state: State = min(
            open_set,
            key=lambda state: f_scores[state]
        )
        open_set.remove(min_state)
        return min_state

    def __priority_cost(self, c_node: int, neighbor: int) -> int:
        if c_node == neighbor:
            return 0

        return 1 if self.__graph.is_priority_node(neighbor) else 0

    def __reconstruct_path(
        self,
        parent: dict[State, State | None],
        state: State
    ) -> list[State]:
        node_state: State | None = state
        path: list[State] = []

        while node_state is not None:
            path.append(node_state)
            node_state = parent[node_state]

        path.reverse()
        return path
