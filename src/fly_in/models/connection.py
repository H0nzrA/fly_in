from pydantic import BaseModel, ConfigDict, Field, model_validator
from .zone import Zone


class ConnectionMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    max_link_capacity: int = Field(ge=0, default=1)


class Connection(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source: Zone
    destination: Zone
    metadata: ConnectionMetadata = Field(
        default_factory=ConnectionMetadata
    )

    @model_validator(mode="after")
    def initialization(self) -> "Connection":
        if (
            self.source.name == self.destination.name or
            self.source == self.destination
        ):
            raise ValueError("Self loop connection found")

        return self
