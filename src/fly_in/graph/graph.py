from pydantic import BaseModel, ConfigDict, PrivateAttr, model_validator
from ..domain import (
    Map,
    Zone,
    ZoneType,
    Connection
)


class NodeNotFoundError(ValueError):
    def __init__(self, id: int) -> None:
        super().__init__(
            f"No zone with id {id!r} found in list"
        )


class Graph(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True
    )

    map: Map
    __adjacency_list: dict[int, set[Connection]] = PrivateAttr(
        default_factory=dict
    )

    @model_validator(mode="after")
    def __adjacency_extraction(self) -> "Graph":
        for conn in self.map.connections:
            self.__adjacency_list.setdefault(
                conn.zone_a.id, set()
            ).add(conn)
            self.__adjacency_list.setdefault(
                conn.zone_b.id, set()
            ).add(conn)

        return self

    def __node_verification(self, id: int) -> None:
        if id not in self.__adjacency_list:
            raise NodeNotFoundError(id)

    def neighbors(self, id: int) -> dict[int, int | None]:
        self.__node_verification(id)

        ngb: dict[int, int | None] = {}

        for conn in self.__adjacency_list[id]:

            if id == conn.zone_a.id:
                ngb[conn.zone_b.id] = self.__zone_weight(id)
            else:
                ngb[conn.zone_a.id] = self.__zone_weight(conn.zone_a.id)

        return ngb

    def __zone_weight(self, id: int) -> int | None:
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
        self.__node_verification(id)

        if id == 0:
            return self.map.start_hub

        if id == self.map.end_hub.id:
            return self.map.end_hub

        for zone in self.map.hubs:
            if id == zone.id:
                return zone

        raise ValueError

    def get_node_position(self, id: int) -> tuple[int, int]:
        return self.get_zone_by_id(id).coordinate

    def get_nodes(self) -> list[int]:
        return [
            self.map.start_hub.id,
            *[m.id for m in self.map.hubs],
            self.map.end_hub.id
        ]

    def start_node(self) -> int:
        return self.map.start_hub.id

    def end_node(self) -> int:
        return self.map.end_hub.id
