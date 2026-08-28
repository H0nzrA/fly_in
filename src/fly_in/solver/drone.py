from pydantic import BaseModel, ConfigDict, PrivateAttr

class Drone(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True
    )
    id: int

    __position: int = PrivateAttr()


    def set_position(self, pos: int) -> None:
        self.__position = pos

    def get_position(self) -> int:
        return self.__position
