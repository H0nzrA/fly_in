"""Parsing of zone definition lines from map files."""

from ..domain import Zone, ZonePrefix, ZoneMetadata
from typing import Any
from pydantic import ValidationError
from .metadata_parser import get_metadata


class ZoneParser:
    """Parses zone lines into Zone domain objects."""

    def __init__(self) -> None:
        """Initialize the map tracking zone names already seen."""
        self.__zone_name: dict[str, Zone] = {}

    def get_zone(self, key: str, value: str, id: int) -> Zone:
        """Parse a zone line into a Zone object.

        Args:
            key (str): Zone prefix key (e.g. `"start_hub"`, `"hub"`).
            value (str): Zone definition, e.g. `"A 0 0 [zone=priority]"`.
            id (int): Node id to assign to the zone.

        Returns:
            Zone: The parsed zone.

        Raises:
            ValueError: If the line is malformed or the zone name is already
                used.
        """
        res: dict[str, Any] = {}
        res["id"] = id
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
            res["metadata"] = get_metadata(prop[3])

        try:
            zone: Zone = Zone(**res)

        except ValidationError as e:
            msg = "; ".join(
                    f"{'.'.join(map(str, err['loc']))}: {err['msg']}"
                    for err in e.errors()
                )
            raise ValueError(msg)

        self.__zone_name[name] = zone

        return zone

    def is_known_zone(self, name: str) -> Zone:
        """Look up a previously parsed zone by name.

        Args:
            name (str): Name of the zone to look up.

        Returns:
            Zone: The matching zone.

        Raises:
            ValueError: If no zone with the given name has been parsed yet.
        """
        if name in self.__zone_name:
            return self.__zone_name[name]

        raise ValueError(f"Unknown Zone {name!r}")

    def update_hub_capacity(self, zone: Zone, capacity: int) -> Zone:
        """Return a copy of a zone with an updated maximum drone capacity.

        Args:
            zone (Zone): Zone to update.
            capacity (int): New maximum drone capacity.

        Returns:
            Zone: A new zone instance with the updated capacity.
        """
        metadata: ZoneMetadata = zone.metadata.model_copy(
            update={"max_drones": capacity}
        )

        return zone.model_copy(
            update={"metadata": metadata}
        )
