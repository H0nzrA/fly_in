from pydantic import BaseModel, ConfigDict, PrivateAttr, ValidationError
from pathlib import Path
from ..domain import (
    Zone,
    ZoneMetadata,
    Connection,
    Map,
    ZonePrefix
)
from typing import Any
from enum import Enum


class ParserError(Exception):
    def __init__(
        self,
        line_num: int,
        msg: str
    ) -> None:
        err: str = f"Parsing Error on [Line {line_num}]: {msg}"
        super().__init__(err)


class Key(Enum):
    NDRONES = "nb_drones"
    CONN = "connection"


class Parser(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: Path

    __zone_name: dict[str, Zone] = PrivateAttr(default_factory=dict)
    __conn_seen: set[frozenset[str]] = PrivateAttr(default_factory=set)

    def __get_file_content(self) -> list[str]:
        return self.path.read_text().split("\n")

    def __parse(self) -> Map:
        lines: list[str] = self.__get_file_content()
        res: dict[str, Any] = {}
        hubs: list[Zone] = []
        conns: list[Connection] = []

        for num, line in enumerate(lines, start=1):
            if line.startswith("#"):
                continue

            if not line.strip():
                continue

            try:
                key, value = line.split(":", 1)

                if key == Key.NDRONES.value:
                    if key in res:
                        raise ValueError(f"Duplicated key: {key!r}")
                    nb = int(value)
                    if nb <= 0:
                        raise ValueError(
                            f"Invalid Number of drones {nb!r}, "
                            "Minimum 1"
                        )
                    res[Key.NDRONES.value] = nb

                elif key in (
                    ZonePrefix.START.value,
                    ZonePrefix.END.value,
                    ZonePrefix.HUB.value,
                ):
                    zone: Zone = self.__zone_parsing(key, value)
                    self.__zone_name[zone.name] = zone

                    if zone.prefix == ZonePrefix.START:
                        if ZonePrefix.START.value in res:
                            raise ValueError(
                                f"Duplicated {ZonePrefix.START.value!r} zone"
                            )
                        res[ZonePrefix.START.value] = zone

                    if zone.prefix == ZonePrefix.END:
                        if ZonePrefix.END.value in res:
                            raise ValueError(
                                f"Duplicated {ZonePrefix.END.value!r} zone"
                            )
                        res[ZonePrefix.END.value] = zone

                    if zone.prefix == ZonePrefix.HUB:
                        hubs.append(zone)

                elif key == Key.CONN.value:
                    conns.append(self.__connection_parsing(value))

                else:
                    raise ValueError(f"Unknown key defined: {key!r}")

            except ValueError as e:
                raise ParserError(num, str(e))

        res["hubs"] = hubs
        res["connections"] = conns

        return self.__evaluation(res)

    def __evaluation(self, res: dict[str, Any]) -> Map:
        nb_drones: int = res["nb_drones"]
        start: Zone = res[ZonePrefix.START.value]
        end: Zone = res[ZonePrefix.END.value]

        if start.metadata.max_drones < nb_drones:
            start = self.__update_hub_capacity(start, nb_drones)
            print(
                f"[Warning]: {start.name!r} zone max drones capacity "
                "inferior capacity inferior to number of drones -- "
                f"Updated to {nb_drones!r}"
            )

        if end.metadata.max_drones < nb_drones:
            end = self.__update_hub_capacity(end, nb_drones)
            print(
                f"[Warning]: {end.name!r} zone max drones capacity "
                "inferior capacity inferior to number of drones -- "
                f"Updated to {nb_drones!r}"
            )

        res[ZonePrefix.START.value] = start
        res[ZonePrefix.END.value] = end

        return Map(**res)

    def __update_hub_capacity(self, zone: Zone, capacity: int) -> Zone:
        metadata: ZoneMetadata = zone.metadata.model_copy(
            update={"max_drones": capacity}
        )

        return zone.model_copy(
            update={"metadata": metadata}
        )

    def __zone_parsing(self, key: str, value: str) -> Zone:
        res: dict[str, Any] = {}
        res["prefix"] = ZonePrefix(key)

        prop: list[str] = value.split(maxsplit=3)
        if len(prop) < 3:
            raise ValueError("Not enough value given for Zone data")
        if len(prop) > 4:
            raise ValueError("Too Many value given for Zone data")

        name: str = prop[0]
        if name in self.__zone_name:
            raise ValueError(f"Zone with the name {name!r} already set")

        res["name"] = name

        x: int = int(prop[1])
        y: int = int(prop[2])
        res["coordinate"] = (x, y)

        if len(prop) == 4:
            res["metadata"] = self.__get_metadata(prop[3])

        try:
            zone: Zone = Zone(**res)

        except ValidationError as e:
            msg = "; ".join(
                    f"{'.'.join(map(str, err['loc']))}: {err['msg']}"
                    for err in e.errors()
                )
            raise ValueError(msg)

        return zone

    def __connection_parsing(self, value: str) -> Connection:
        prop: list[str] = value.split()
        if len(prop) > 2:
            raise ValueError("Too Many value given for Connection data")

        conn: list[str] = prop[0].split("-")
        if len(conn) != 2:
            raise ValueError("Connection must be only between two Zone")

        source: str = conn[0]
        destination: str = conn[1]

        if source not in self.__zone_name:
            raise ValueError(f"Unknown Zone {source!r}")

        if destination not in self.__zone_name:
            raise ValueError(f"Unknown Zone {destination!r}")

        edge: frozenset[str] = frozenset((source, destination))
        if edge in self.__conn_seen:
            raise ValueError(
                f"Duplicated Connection: '{source} - {destination}'"
            )
        self.__conn_seen.add(edge)

        metadata = None
        if len(prop) == 2:
            metadata = self.__get_metadata(prop[1])

        res: dict[str, Any] = {
            "zone_a": self.__zone_name[source],
            "zone_b": self.__zone_name[destination],
        }
        if metadata is not None:
            res["metadata"] = metadata

        try:
            connection: Connection = Connection(**res)

        except ValidationError as e:
            msg = "; ".join(
                    f"{'.'.join(map(str, err['loc']))}: {err['msg']}"
                    for err in e.errors()
                )
            raise ValueError(msg)

        return connection

    def __get_metadata(self, value: str) -> dict[str, Any]:
        if value.startswith("[") and value.endswith("]"):
            content: list[str] = value[1:-1].split()
            res: dict[str, Any] = {}

            for c in content:
                k, v = c.split("=")
                res[k] = v

            return res

        else:
            raise ValueError("Metadata must be enclosed with []")

    def get_map(self) -> Map:
        try:
            res_map: Map = self.__parse()

        except ValidationError as e:
            msg = "; ".join(
                    f"{'.'.join(map(str, err['loc']))}: {err['msg']}"
                    for err in e.errors()
                )
            raise ValueError(msg)

        return res_map
