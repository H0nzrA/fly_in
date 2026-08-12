from pydantic import BaseModel, ConfigDict, Field
from .zone import Zone
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
