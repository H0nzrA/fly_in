from pydantic import BaseModel, ConfigDict, model_validator, Field
from enum import Enum


class ZonePrefix(str, Enum):
    START = "start_hub"
    END = "end_hub"
    HUB = "hub"


class ZoneType(str, Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class ZoneMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    zone: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1  # Maximum drones occupied


class Zone(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    prefix: ZonePrefix
    name: str
    coordinate: tuple[int, int]
    metadata: ZoneMetadata = Field(default_factory=ZoneMetadata)

    @model_validator(mode="after")
    def validation(self) -> "Zone":
        if "-" in self.name or " " in self.name:
            raise ValueError(
                f"Find Dashes on zone name: {self.name}"
            )
        return self
