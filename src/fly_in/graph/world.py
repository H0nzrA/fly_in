"""Shared reservation state tracking node and edge usage over time."""

State = tuple[int, int]


class WorldState:
    """Tracks how many drones occupy each node and edge over time."""

    def __init__(self) -> None:
        """Initialize empty node and edge usage counters."""
        self.__node_usage: dict[
            tuple[int, int],
            int
        ] = {}
        self.__edge_usage: dict[
            tuple[frozenset[int], int],
            int
        ] = {}

    def reserve_node(self, node: int, time: int) -> None:
        """Reserve one drone's occupancy of a node at a given time.

        Args:
            node (int): Node id being reserved.
            time (int): Time step of the reservation.
        """
        key: tuple[int, int] = (node, time)
        self.__node_usage[key] = self.__node_usage.get(key, 0) + 1

    def reserve_edge(self, a: int, b: int, time: int) -> None:
        """Reserve one drone's occupancy of an edge at a given time.

        Args:
            a (int): First node id of the edge.
            b (int): Second node id of the edge.
            time (int): Time step of the reservation.
        """
        key: tuple[frozenset[int], int] = (frozenset((a, b)), time)
        self.__edge_usage[key] = self.__edge_usage.get(key, 0) + 1

    def node_avaliable(self, node: int, time: int, capacity: int) -> bool:
        """Check whether a node has spare capacity at a given time.

        Args:
            node (int): Node id to check.
            time (int): Time step to check.
            capacity (int): Maximum simultaneous occupancy of the node.

        Returns:
            bool: True if the node has not reached capacity.
        """
        key: tuple[int, int] = node, time
        return self.__node_usage.get(key, 0) < capacity

    def edge_avaliable(self, a: int, b: int, time: int, capacity: int) -> bool:
        """Check whether an edge has spare capacity at a given time.

        Args:
            a (int): First node id of the edge.
            b (int): Second node id of the edge.
            time (int): Time step to check.
            capacity (int): Maximum simultaneous occupancy of the edge.

        Returns:
            bool: True if the edge has not reached capacity.
        """
        key: tuple[frozenset[int], int] = (frozenset((a, b)), time)
        return self.__edge_usage.get(key, 0) < capacity
