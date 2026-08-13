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
    max_drones: int = Field(ge=0, default=1)  # Maximum drones occupied

    @model_validator(mode="after")
    def initialization(self) -> "ZoneMetadata":
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
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: int = Field(ge=0)
    prefix: ZonePrefix
    name: str
    coordinate: tuple[int, int]
    metadata: ZoneMetadata = Field(default_factory=ZoneMetadata)

    @model_validator(mode="after")
    def validation(self) -> "Zone":
        if "-" in self.name or " " in self.name:
            raise ValueError(
                f"Find Dashes on zone name {self.name!r}"
            )
        return self
