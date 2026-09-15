"""Domain model for connections (edges) between zones."""

from pydantic import BaseModel, ConfigDict, Field, model_validator
from .zone import Zone


class ConnectionMetadata(BaseModel):
    """Optional attributes describing a connection's capacity.

    Attributes:
        max_link_capacity (int): Maximum number of drones allowed on the
            connection at once.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    max_link_capacity: int = Field(ge=0, default=1)


class Connection(BaseModel):
    """An edge linking two zones that drones can travel along.

    Attributes:
        zone_a (Zone): First zone of the connection.
        zone_b (Zone): Second zone of the connection.
        metadata (ConnectionMetadata): Additional routing metadata for the
            connection.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    zone_a: Zone
    zone_b: Zone
    metadata: ConnectionMetadata = Field(
        default_factory=ConnectionMetadata
    )

    @model_validator(mode="after")
    def initialization(self) -> "Connection":
        """Validate that the connection does not link a zone to itself.

        Returns:
            Connection: The validated connection instance.

        Raises:
            ValueError: If both endpoints refer to the same zone.
        """
        if (
            self.zone_a.name == self.zone_b.name or
            self.zone_a == self.zone_b
        ):
            raise ValueError("Self loop connection found")

        return self
