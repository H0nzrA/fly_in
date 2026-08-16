from pydantic import BaseModel, ConfigDict, PrivateAttr, model_validator
from ..domain import (
    Map,
    Zone,
    Connection
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

    def neighbors(self, zone_id: int) -> set[int]:
        if zone_id not in self.__adjacency_list:
            raise ValueError(f"No Zone id {zone_id!r} found in list")

        ngb: set[int] = set()

        for conn in self.__adjacency_list[zone_id]:

            if zone_id == conn.zone_a.id:
                ngb.add(conn.zone_b.id)
            else:
                ngb.add(conn.zone_a.id)

        return ngb

    def get_zone(self, id: int) -> Zone:
        if id == 0:
            return self.map.start_hub

        if id == self.map.end_hub.id:
            return self.map.end_hub

        for zone in self.map.hubs:
            if id == zone.id:
                return zone

        raise ValueError(f"No zone with id {id!r} found")

    def start_zone(self) -> int:
        return self.map.start_hub.id

    def end_zone(self) -> int:
        return self.map.end_hub.id
