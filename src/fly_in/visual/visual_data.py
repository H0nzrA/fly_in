from ..graph import Graph, State
from ..domain import Zone
from .var import Movement


class VisualData:
    def __init__(
        self,
        paths: dict[int, list[State]],
        graph: Graph
    ) -> None:
        self.__timed_path: dict[
            int,
            dict[int, Movement]
        ] = self.__data_adapter(
            paths,
            graph
        )

    def __data_adapter(
        self,
        paths: dict[int, list[State]],
        graph: Graph
    ) -> dict[int, dict[int, Movement]]:
        max_time: int = self.__get_max_time(paths)
        simulation: dict[int, dict[int, Movement]] = {
            i: {}
            for i in range(max_time + 1)
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
                    for time in range(ntime + 1, max_time + 1):
                        simulation[time][drone] = nzone

        return simulation

    def __get_max_time(self, paths: dict[int, list[State]]) -> int:
        return max(
            state[1]
            for path in paths.values()
            for state in path
        )
