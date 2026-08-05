from pydantic import BaseModel, ConfigDict, Field
from .zone import Zone


class ConnectionMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    max_link_capacity: int = 1  # Maximum drones that can traverse


class Connection(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source: Zone
    destination: Zone
    metadata: ConnectionMetadata = Field(
        default_factory=ConnectionMetadata
    )
