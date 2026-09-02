from .platform import Platform
from ..graph import State


class VisualApp:
    def __init__(
        self,
        width: int,
        height: int,
        title: str
    ) -> None:
        self.__platform: Platform = Platform(
            width,
            height,
            title
        )

    def run(
        self,
        paths: dict[int, list[State]]
    ) -> None:
        self.__platform.run()
