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

    fmap: Map
    __adjacency_list: dict[Zone, set[Connection]] = PrivateAttr(
        default_factory=dict
    )

    @model_validator(mode="after")
    def __adjacency_extraction(self) -> "Graph":
        for conn in self.fmap.connections:
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

    def start_zone(self) -> Zone:
        return self.fmap.start_hub

    def end_zone(self) -> Zone:
        return self.fmap.end_hub
