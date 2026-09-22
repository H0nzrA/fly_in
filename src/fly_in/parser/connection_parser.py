"""Parsing of connection definition lines from map files."""

from ..domain import Connection, Zone
from typing import Any
from .metadata_parser import get_metadata
from pydantic import ValidationError
from collections.abc import Callable


class ConnectionParser:
    """Parses connection lines into Connection domain objects."""

    def __init__(self) -> None:
        """Initialize the set tracking already-seen connections."""
        self.__conn_seen: set[frozenset[str]] = set()

    def get_connection(
        self,
        value: str,
        get_zone: Callable[[str], Zone]
    ) -> Connection:
        """Parse a connection line into a Connection object.

        Args:
            value (str): Connection definition.
            get_zone (Callable[[str], Zone]): Lookup to resolve zone names.

        Returns:
            Connection: The parsed connection.

        Raises:
            ValueError: If the line is malformed, refers to unknown zones, or
                duplicates an existing connection.
        """
        prop: list[str] = value.split(maxsplit=1)
        if len(prop) > 2:
            raise ValueError("Too Many value given for Connection data")
        if len(prop) == 0:
            raise ValueError(
                "Invalid writting. "
                "Expect: <zone>-<zone>"
            )

        conn: list[str] = prop[0].split("-")
        if len(conn) != 2:
            raise ValueError("Connection must be only between two Zone")

        zone_a: Zone = get_zone(conn[0])
        zone_b: Zone = get_zone(conn[1])

        edge: frozenset[str] = frozenset((zone_a.name, zone_b.name))
        if edge in self.__conn_seen:
            raise ValueError(
                f"Duplicated Connection: '{zone_a.name} - {zone_b.name}'"
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
