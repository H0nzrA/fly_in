"""Domain model for the overall drone-delivery map."""

from pydantic import BaseModel, ConfigDict, Field, model_validator
from .zone import Zone, ZoneType
from .connection import Connection


class Map(BaseModel):
    """Immutable domain model describing a complete drone delivery map.

    Attributes:
        nb_drones (int): Number of drones to route across the map.
        start_hub (Zone): Zone where every drone starts.
        end_hub (Zone): Zone where every drone must arrive.
        hubs (list[Zone]): Intermediate zones connecting start and end.
        connections (list[Connection]): Edges linking zones together.
    """

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
        """Validate that neither hub is a blocked zone.

        Returns:
            Map: The validated map instance.

        Raises:
            ValueError: If the start or end hub is a blocked zone.
        """
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
