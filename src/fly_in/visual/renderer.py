import pygame
from .var import Window, Surface, Color
from importlib.resources import files, as_file
from ..domain import Map, Zone


class Renderer:
    def __init__(
        self,
        window: Window,
        domain: Map
    ) -> None:
        self.__window: Window = window
        self.__load_image()
        self.__domain: Map = domain

        # Domain to window scale
        self.__scale: int = 50
        width, height = self.__window.get_size()
        self.__offset: tuple[int, int] = (
            width // 2,
            height // 2
        )

        # Color data
        self.__colors: dict[str, Color] = pygame.color.THECOLORS

    def __load_image(self) -> None:
        bg = (
            files("fly_in")
            .joinpath("resources", "images", "background.jpg")
        )
        with as_file(bg) as path:
            self.__background: Surface = pygame.image.load(path)
            w_size = self.__window.get_size()
            self.__background = pygame.transform.scale(
                self.__background,
                w_size
            )

    def __positions(self, pos: tuple[int, int]) -> tuple[int, int]:
        x: int = self.__offset[0] + pos[0] * self.__scale
        y: int = self.__offset[1] - pos[1] * self.__scale

        return x, y

    def __get_color(self, name: str | None) -> Color:
        if name is None:
            return self.__colors["lightgray"]
        try:
            return self.__colors[name]
        except KeyError:
            return self.__colors["lightgray"]

    def __render_zones(self, zone: Zone) -> None:
        pos: tuple[int, int] = self.__positions(zone.coordinate)
        color: Color = self.__get_color(zone.metadata.color)

        pygame.draw.circle(
            self.__window,
            color,
            pos,
            10
        )

    def __draw(self) -> None:
        # Zones
        self.__render_zones(self.__domain.start_hub)
        self.__render_zones(self.__domain.end_hub)
        for zone in self.__domain.hubs:
            self.__render_zones(zone)

    def render(self) -> None:
        self.__window.blit(self.__background, (0, 0))
        self.__draw()
        pygame.display.flip()
