from pydantic import (
    BaseModel,
    ConfigDict,
    PrivateAttr,
    ValidationError,
    model_validator
)
from pathlib import Path
from ..domain import (
    Zone,
    Connection,
    Map,
    ZonePrefix
)
from typing import Any
from enum import Enum
from .zone_parser import ZoneParser
from .connection_parser import ConnectionParser
from ..cli import Reporter
from ..utils import FlyInError, ParserError


class Key(Enum):
    NDRONES = "nb_drones"
    CONN = "connection"


class Parser(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: Path
    __zparser: ZoneParser = PrivateAttr(default_factory=ZoneParser)
    __cparser: ConnectionParser = PrivateAttr(
        default_factory=ConnectionParser
    )

    @model_validator(mode="after")
    def initializer(self) -> "Parser":
        self.__reporter: Reporter = Reporter("Parser")
        return self

    def __get_file_content(self) -> list[str]:
        try:
            content: list[str] = self.path.read_text().split("\n")
            return content

        except (
            FileNotFoundError,
            OSError,
            IsADirectoryError,
            PermissionError
        ) as e:
            raise FlyInError(e)

    def __parse(self) -> Map:
        self.__reporter.info("Starting parsing ...")

        lines: list[str] = self.__get_file_content()
        res: dict[str, Any] = {}
        hubs: list[Zone] = []
        conns: list[Connection] = []

        first_line: bool = True
        current_id: int = 0

        for num, line in enumerate(lines, start=1):
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            try:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                if first_line and key != Key.NDRONES.value:
                    raise ValueError(
                        f"Key {Key.NDRONES.value!r} expected on "
                        "first line."
                    )

                first_line = False

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
                    zone: Zone = self.__zparser.get_zone(
                        key,
                        value,
                        current_id
                    )

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

                    current_id += 1

                elif key == Key.CONN.value:
                    conns.append(
                        self.__cparser.get_connection(
                            value,
                            self.__zparser.is_known_zone
                        )
                    )

                else:
                    raise ValueError(f"Unknown key defined: {key!r}")

            except ValueError as e:
                raise ParserError(num, str(e))

        res["hubs"] = hubs
        res["connections"] = conns

        return self.__evaluation(res)

    def __evaluation(self, res: dict[str, Any]) -> Map:
        try:
            nb_drones: int = res["nb_drones"]
            start: Zone = res[ZonePrefix.START.value]
            end: Zone = res[ZonePrefix.END.value]

            if start.metadata.max_drones < nb_drones:
                start = self.__zparser.update_hub_capacity(
                    start,
                    nb_drones
                )
                self.__reporter.warning(
                    f"{start.name!r} zone max drones capacity "
                    "inferior to number of drones -- "
                    f"Updated to {nb_drones!r}"
                )

            if end.metadata.max_drones < nb_drones:
                end = self.__zparser.update_hub_capacity(end, nb_drones)
                self.__reporter.warning(
                    f"{end.name!r} zone max drones capacity "
                    "inferior to number of drones -- "
                    f"Updated to {nb_drones!r}"
                )

            res[ZonePrefix.START.value] = start
            res[ZonePrefix.END.value] = end

        except KeyError as e:
            msg: str = f"Parser Error [Evaluation]: Key {e} not defined"
            raise ValueError(msg)

        return Map(**res)

    def get_map(self) -> Map:
        try:
            return self.__parse()

        except ValidationError as e:
            msg = "; ".join(
                    f"{err['msg']}"
                    for err in e.errors()
                )
            raise FlyInError(msg)

        except ParserError as e:
            self.__reporter.error(str(e))
            raise FlyInError
