from ..domain import Connection, Zone
from typing import Any
from .metadata_parser import get_metadata
from pydantic import ValidationError
from collections.abc import Callable


class ConnectionParser:
    def __init__(self) -> None:
        self.__conn_seen: set[frozenset[str]] = set()

    def get_connection(
        self,
        value: str,
        get_zone: Callable[[str], Zone]
    ) -> Connection:
        prop: list[str] = value.split()
        if len(prop) > 2:
            raise ValueError("Too Many value given for Connection data")

        conn: list[str] = prop[0].split("-")
        if len(conn) != 2:
            raise ValueError("Connection must be only between two Zone")

        zone_a: Zone = get_zone(conn[0])
        zone_b: Zone = get_zone(conn[1])

        edge: frozenset[str] = frozenset((zone_a.name, zone_b.name))
        if edge in self.__conn_seen:
            raise ValueError(
                f"Duplicated Connection: '{zone_a} - {zone_b}'"
            )
        self.__conn_seen.add(edge)

        metadata = None
        if len(prop) == 2:
            metadata = get_metadata(prop[1])

        res: dict[str, Any] = {
            "zone_a": zone_a,
            "zone_b": zone_b,
        }
        if metadata is not None:
            res["metadata"] = metadata

        try:
            connection: Connection = Connection(**res)

        except ValidationError as e:
            msg = "; ".join(
                    f"{err['msg']}"
                    for err in e.errors()
                )
            raise ValueError(msg)

        return connection
