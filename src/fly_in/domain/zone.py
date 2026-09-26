"""Domain model for zones and their metadata."""

from pydantic import BaseModel, ConfigDict, model_validator, Field
from enum import Enum


class ZonePrefix(str, Enum):
    """Prefix identifying the role of a zone (start, end, or hub)."""

    START = "start_hub"
    END = "end_hub"
    HUB = "hub"


class ZoneType(str, Enum):
    """Category describing how a zone affects drone routing."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class ZoneMetadata(BaseModel):
    """Optional attributes describing a zone's behaviour and capacity.

    Attributes:
        zone (ZoneType): Routing category of the zone.
        color (str | None): Optional display color for the zone.
        max_drones (int): Maximum number of drones allowed on the zone at once.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    zone: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = Field(ge=1, default=1)  # Maximum drones occupied

    @model_validator(mode="after")
    def initialization(self) -> "ZoneMetadata":
        """Validate that the color, if set, is a valid alphabetic string.

        Returns:
            ZoneMetadata: The validated metadata instance.

        Raises:
            ValueError: If the color is shorter than 3 characters or contains
                non-alphabetic characters.
        """
        if self.color:
            if len(self.color) < 3:
                raise ValueError(
                    "Color must be a valid string"
                )

            for c in self.color:
                if not c.isalpha():
                    raise ValueError(
                        "Color must be only strings"
                    )
        return self


class Zone(BaseModel):
    """A single point on the map that drones can occupy or pass through.

    Attributes:
        id (int): Unique identifier of the zone.
        prefix (ZonePrefix): Role of the zone (start, end, or hub).
        name (str): Human-readable name of the zone.
        coordinate (tuple[int, int]): Position of the zone on the map grid.
        metadata (ZoneMetadata): Additional routing metadata for the zone.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: int = Field(ge=0)
    prefix: ZonePrefix
    name: str
    coordinate: tuple[int, int]
    metadata: ZoneMetadata = Field(default_factory=ZoneMetadata)

    @model_validator(mode="after")
    def validation(self) -> "Zone":
        """Validate that the zone name contains no dashes or spaces.

        Returns:
            Zone: The validated zone instance.

        Raises:
            ValueError: If the name contains a dash or a space.
        """
        if "-" in self.name or " " in self.name:
            raise ValueError(
                f"Find Dashes on zone name {self.name!r}"
            )
        return self
