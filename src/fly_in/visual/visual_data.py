"""Time-indexed drone movement data derived from solved paths."""

from ..graph import Graph, State
from ..domain import Zone
from .var import Movement
from ..utils import VisualError


def get_max_time(paths: dict[int, list[State]]) -> int:
    """Find the latest time step reached across all drone paths.

    Args:
        paths (dict[int, list[State]]): Solved path per drone id.

    Returns:
        int: The maximum time step found across all paths.
    """
    return max(
        state[1]
        for path in paths.values()
        for state in path
    )


class VisualData:
    """Adapts solved drone paths into per-turn positions for rendering."""

    def __init__(
        self,
        paths: dict[int, list[State]],
        graph: Graph
    ) -> None:
        """Build the timed movement data from solved paths.

        Args:
            paths (dict[int, list[State]]): Solved path per drone id.
            graph (Graph): Graph used to resolve node ids to zones/connections.
        """
        self.__nb_drones: int = len(paths)
        self.__max_time: int = get_max_time(paths) + 1
        self.__timed_path: dict[
            int,
            dict[int, Movement]
        ] = self.__data_adapter(
            paths,
            graph
        )
        self.__time: int = 0

    def __data_adapter(
        self,
        paths: dict[int, list[State]],
        graph: Graph
    ) -> dict[int, dict[int, Movement]]:
        """Expand solved paths into a movement per drone for every time step.

        Args:
            paths (dict[int, list[State]]): Solved path per drone id.
            graph (Graph): Graph used to resolve node ids to zones/connections.

        Returns:
            dict[int, dict[int, Movement]]: Movement of each drone, indexed by
                time step then drone id.
        """
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
        """Advance the current time step by one, if possible."""
        t: int = self.__time + 1
        if self.__max_time < t:
            return
        self.__time = t

    def previous(self) -> None:
        """Move the current time step back by one, if possible."""
        t: int = self.__time - 1
        if t < 0:
            return
        self.__time = t

    def get_current(self) -> dict[int, Movement]:
        """Return the movement of every drone at the current time step.

        Returns:
            dict[int, Movement]: Movement of each drone at the current time.
        """
        return self.__timed_path[self.__time]

    def get_at(self, time: int) -> dict[int, Movement]:
        """Return the movement of every drone at a given time step.

        Args:
            time (int): Time step to look up.

        Returns:
            dict[int, Movement]: Movement of each drone at the given time.

        Raises:
            VisualError: If no data exists for the requested time step.
        """
        if self.__time == 0:
            return self.get_current()
        if self.__time >= self.__max_time:
            return self.__timed_path[self.__max_time]

        if time not in self.__timed_path:
            raise VisualError(f"No path/position found at time {time}")

        return self.__timed_path[time]

    def get_movement_position(
        self,
        movement: Movement
    ) -> tuple[float, float]:
        """Compute the world position represented by a movement.

        Args:
            movement (Movement): Zone or connection to locate.

        Returns:
            tuple[float, float]: World coordinate of the movement, using the
                midpoint of the two zones if it is a connection.
        """
        if isinstance(movement, Zone):
            coordinate = movement.coordinate
            return float(coordinate[0]), float(coordinate[1])

        pos_a: tuple[int, int] = movement.zone_a.coordinate
        pos_b: tuple[int, int] = movement.zone_b.coordinate

        return (
            (pos_a[0] + pos_b[0]) / 2,
            (pos_a[1] + pos_b[1]) / 2,
        )

    @property
    def current_time(self) -> int:
        """int: The current time step."""
        return self.__time

    @property
    def last_time(self) -> int:
        """int: The final time step across all drone paths."""
        return self.__max_time

    @property
    def nb_drones(self) -> int:
        """int: The number of drones being tracked."""
        return self.__nb_drones

    def reset_time(self) -> None:
        """Reset the current time step back to zero."""
        self.__time = 0
