from ..graph import Graph, State
from ..domain import Zone
from .var import Movement


def get_max_time(paths: dict[int, list[State]]) -> int:
    return max(
        state[1]
        for path in paths.values()
        for state in path
    )


class VisualData:
    def __init__(
        self,
        paths: dict[int, list[State]],
        graph: Graph
    ) -> None:
        self.__max_time: int = get_max_time(paths)
        self.__timed_path: dict[
            int,
            dict[int, Movement]
        ] = self.__data_adapter(
            paths,
            graph
        )
        self.current_time: int = 0

    def __data_adapter(
        self,
        paths: dict[int, list[State]],
        graph: Graph
    ) -> dict[int, dict[int, Movement]]:
        simulation: dict[int, dict[int, Movement]] = {
            i: {}
            for i in range(self.__max_time + 1)
        }

        for drone, path in paths.items():
            for i in range(len(path) - 1):
                cnode, ctime = path[i]
                nnode, ntime = path[i + 1]

                czone: Zone = graph.get_zone_by_id(cnode)
                nzone: Zone = graph.get_zone_by_id(nnode)

                if ctime == 0:
                    simulation[ctime][drone] = czone

                delta: int = ntime - ctime
                if delta != 1:
                    for time in range(ctime + 1, ntime):
                        simulation[time][drone] = graph.get_connection(
                            cnode,
                            nnode
                        )
                simulation[ntime][drone] = nzone

                if nnode == graph.end_node():
                    for time in range(ntime + 1, self.__max_time + 1):
                        simulation[time][drone] = nzone

        return simulation

    def next(self) -> None:
        t: int = self.current_time + 1
        if self.__max_time < t:
            return
        self.current_time = t

    def previous(self) -> None:
        t: int = self.current_time - 1
        if t < 0:
            return
        self.current_time = t

    def get_current(self) -> dict[int, Movement]:
        return self.__timed_path[self.current_time]

    def get_movement_position(
        self,
        movement: Movement
    ) -> tuple[int, int]:
        if isinstance(movement, Zone):
            return movement.coordinate

        pos_a: tuple[int, int] = movement.zone_a.coordinate
        pos_b: tuple[int, int] = movement.zone_b.coordinate

        return (
            (pos_a[0] + pos_b[0]) // 2,
            (pos_a[1] + pos_b[1]) // 2,
        )
