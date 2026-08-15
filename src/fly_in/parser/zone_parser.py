from ..domain import Zone, ZonePrefix, ZoneMetadata
from typing import Any
from pydantic import ValidationError
from .metadata_parser import get_metadata


class ZoneParser:

    def __init__(self) -> None:
        self.__zone_name: dict[str, Zone] = {}

    def get_zone(self, key: str, value: str, id: int) -> Zone:
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
        if name in self.__zone_name:
            return self.__zone_name[name]

        raise ValueError(f"Unknown Zone {name!r}")

    def update_hub_capacity(self, zone: Zone, capacity: int) -> Zone:
        metadata: ZoneMetadata = zone.metadata.model_copy(
            update={"max_drones": capacity}
        )

        return zone.model_copy(
            update={"metadata": metadata}
        )
