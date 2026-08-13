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
    __adjacency_list: dict[Zone, set[Connection]] = PrivateAttr(
        default_factory=dict
    )

    @model_validator(mode="after")
    def __adjacency_extraction(self) -> "Graph":
        for conn in self.map.connections:
            self.__adjacency_list.setdefault(
                conn.zone_a, set()
            ).add(conn)
            self.__adjacency_list.setdefault(
                conn.zone_b, set()
            ).add(conn)

        return self

    def neighbors(self, zone: Zone) -> set[Zone]:
        if zone not in self.__adjacency_list:
            raise ValueError(f"No Zone {zone.name} found in list")

        ngb: set[Zone] = set()

        for conn in self.__adjacency_list[zone]:

            if zone == conn.zone_a:
                ngb.add(conn.zone_b)
            else:
                ngb.add(conn.zone_a)

        return ngb

    def connections(self, zone: Zone) -> set[Connection]:
        if zone not in self.__adjacency_list:
            raise ValueError(f"No Zone {zone.name} found in list")

        return self.__adjacency_list[zone].copy()

    def get_zone(self, id: int) -> Zone:
        if id == 0:
            return self.start_zone()

        if id == self.end_zone().id:
            return self.end_zone()

        for zone in self.map.hubs:
            if id == zone.id:
                return zone

        raise ValueError(f"No zone with id {id!r} found")

    def start_zone(self) -> Zone:
        return self.map.start_hub

    def end_zone(self) -> Zone:
        return self.map.end_hub
