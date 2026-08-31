from ..graph import Graph, State
from ..domain import Zone, Map


class Output:
    def __init__(self, graph: Graph) -> None:
        self.__graph: Graph = graph

    def drones_paths(
        self,
        paths: dict[int, list[State]],
    ) -> dict[int, list[str]]:
        total_turn: int = self.get_total_turn(paths)
        turns: dict[int, list[str]] = {
            i: []
            for i in range(1, total_turn + 1)
        }

        for drone_id, path in paths.items():
            has_started: bool = False
            for i in range(len(path) - 1):
                current_node, current_time = path[i]
                next_node, next_time = path[i + 1]

                if next_time <= current_time:
                    continue

                if current_node == next_node:
                    if (
                        current_node == self.__graph.start_node()
                        and not has_started
                    ):
                        continue
                    has_started = True


                delta: int = next_time - current_time
                drone: str = f"D{drone_id}"
                czone: str = self.__graph.get_zone_by_id(current_node).name
                nzone: str = self.__graph.get_zone_by_id(next_node).name

                on_zone: str = "-".join([drone, nzone])
                on_connection = "-".join([drone, czone, nzone])

                if delta != 1:

                    for time in range(current_time + 1, next_time):
                        turns[time].append(on_connection)
                        if time + 1 == next_time:
                            turns[time + 1].append(on_zone)

                else:
                    turns[next_time].append(on_zone)

        if len(turns) != total_turn:
            raise ValueError(
                f"Extracted turns have not total turn = {total_turn}"
            )

        return turns

    def get_total_turn(self, paths: dict[int, list[State]]) -> int:
        return max(
            state[1]
            for path in paths.values()
            for state in path
        )
