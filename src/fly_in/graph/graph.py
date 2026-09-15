"""Adjacency-list graph view over the domain map."""

from pydantic import BaseModel, ConfigDict, PrivateAttr, model_validator
from ..domain import (
    Map,
    Zone,
    ZoneType,
    Connection
)
from ..cli import Reporter
from ..utils import NodeNotFoundError


class Graph(BaseModel):
    """Adjacency-list view of a Map used for pathfinding.

    Attributes:
        map (Map): The underlying domain map.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True
    )

    map: Map
    __adjacency_list: dict[int, set[Connection]] = PrivateAttr(
        default_factory=dict
    )

    @model_validator(mode="after")
    def initializer(self) -> "Graph":
        """Build the adjacency list from the map's connections.

        Returns:
            Graph: The initialized graph instance.
        """
        self.__reporter: Reporter = Reporter("Graph")
        self.__reporter.info("Adjacency list initialization ...")

        self.__adjacency_list = {
            node: set()
            for node in range(len(self.map.hubs) + 2)
        }
        for conn in self.map.connections:
            self.__adjacency_list[conn.zone_a.id].add(conn)
            self.__adjacency_list[conn.zone_b.id].add(conn)

        return self

    def __node_verification(self, id: int) -> None:
        """Ensure a node id exists in the graph.

        Args:
            id (int): Node id to verify.

        Raises:
            ValueError: If no zone with the given id exists.
        """
        if id not in self.get_nodes():
            self.__reporter.error(f"No zone with id {id!r} found in list")
            raise ValueError

    def neighbors(self, id: int) -> dict[int, int | None]:
        """List the reachable neighbors of a node and their travel weights.

        Args:
            id (int): Node id to find neighbors for.

        Returns:
            dict[int, int | None]: Travel weight per neighbor node id, or None
                if the neighbor is blocked.
        """
        self.__node_verification(id)

        ngb: dict[int, int | None] = {}

        for conn in self.__adjacency_list[id]:

            if id == conn.zone_a.id:
                ngb[conn.zone_b.id] = self.__zone_weight(conn.zone_b.id)
            else:
                ngb[conn.zone_a.id] = self.__zone_weight(conn.zone_a.id)

        return ngb

    def __zone_weight(self, id: int) -> int | None:
        """Determine the travel weight of entering a zone.

        Args:
            id (int): Node id of the zone.

        Returns:
            int | None: Travel weight of the zone, or None if it is blocked.
        """
        zone: Zone = self.get_zone_by_id(id)

        ztype: ZoneType = zone.metadata.zone

        if ztype == ZoneType.RESTRICTED:
            return 2
        elif ztype == ZoneType.PRIORITY:
            return 1
        elif ztype == ZoneType.BLOCKED:
            return None

        return 1

    def get_zone_by_id(self, id: int) -> Zone:
        """Look up the zone with the given id.

        Args:
            id (int): Node id to look up.

        Returns:
            Zone: The matching zone.

        Raises:
            ValueError: If no zone with the given id exists.
        """
        self.__node_verification(id)

        if id == self.map.start_hub.id:
            return self.map.start_hub

        if id == self.map.end_hub.id:
            return self.map.end_hub

        for zone in self.map.hubs:
            if id == zone.id:
                return zone

        raise ValueError

    def get_nodes(self) -> list[int]:
        """List every node id in the graph.

        Returns:
            list[int]: The start hub, hubs, and end hub node ids.
        """
        return [
            self.map.start_hub.id,
            *[m.id for m in self.map.hubs],
            self.map.end_hub.id
        ]

    def get_connection(self, a: int, b: int) -> Connection:
        """Find the connection between two nodes.

        Args:
            a (int): First node id.
            b (int): Second node id.

        Returns:
            Connection: The connection linking the two nodes.

        Raises:
            NodeNotFoundError: If no connection links the two nodes.
        """
        self.__node_verification(a)
        self.__node_verification(b)

        for conn in self.__adjacency_list[a]:
            if {conn.zone_a.id, conn.zone_b.id} == {a, b}:
                return conn

        raise NodeNotFoundError(b)

    def is_priority_node(self, id: int) -> bool:
        """Check whether a node is a priority zone.

        Args:
            id (int): Node id to check.

        Returns:
            bool: True if the zone is a priority zone.
        """
        self.__node_verification(id)
        zone: Zone = self.get_zone_by_id(id)

        if zone.metadata.zone == ZoneType.PRIORITY:
            return True
        return False

    def start_node(self) -> int:
        """Return the start hub's node id.

        Returns:
            int: The start hub's node id.
        """
        return self.map.start_hub.id

    def end_node(self) -> int:
        """Return the end hub's node id.

        Returns:
            int: The end hub's node id.
        """
        return self.map.end_hub.id

    def get_node_capacity(self, id: int) -> int:
        """Return the maximum drone capacity of a node.

        Args:
            id (int): Node id to check.

        Returns:
            int: Maximum number of drones allowed on the node at once.
        """
        self.__node_verification(id)
        return self.get_zone_by_id(id).metadata.max_drones

    def get_edge_capacity(self, a: int, b: int) -> int:
        """Return the maximum drone capacity of an edge.

        Args:
            a (int): First node id of the edge.
            b (int): Second node id of the edge.

        Returns:
            int: Maximum number of drones allowed on the edge at once.

        Raises:
            NodeNotFoundError: If no connection links the two nodes.
        """
        self.__node_verification(a)

        for conn in self.__adjacency_list[a]:
            if {conn.zone_a.id, conn.zone_b.id} == {a, b}:
                return conn.metadata.max_link_capacity

        raise NodeNotFoundError(b)
