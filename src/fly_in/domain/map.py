from pydantic import BaseModel, ConfigDict, Field, model_validator
from .zone import Zone, ZoneType
from .connection import Connection


class Map(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True
    )

    nb_drones: int = Field(ge=0)
    start_hub: Zone
    end_hub: Zone
    hubs: list[Zone]

    connections: list[Connection]

    @model_validator(mode="after")
    def initialization(self) -> "Map":
        if self.start_hub.metadata.zone == ZoneType.BLOCKED:
            raise ValueError(
                f"Start zone {self.start_hub.name!r} "
                "is a blocked zone"
            )
        if self.end_hub.metadata.zone == ZoneType.BLOCKED:
            raise ValueError(
                f"End zone {self.end_hub.name!r} "
                "is a blocked zone"
            )

        return self
