import pygame
from .var import Window, Surface, Color
from importlib.resources import files, as_file
from ..domain import Map, Zone, Connection


def map_center(domain: Map) -> tuple[int, int]:
    coord: list[tuple[int, int]] = [
        zone.coordinate
        for zone in domain.hubs
    ]
    coord.append(domain.start_hub.coordinate)
    coord.append(domain.end_hub.coordinate)

    x_max = max(x for x, y in coord)
    x_min = min(x for x, y in coord)
    y_max = max(y for x, y in coord)
    y_min = min(y for x, y in coord)


    res: tuple[int, int] = (
        (x_max + x_min) // 2,
        (y_max + y_min) // 2
    )

    return res


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
        self.__map_center: tuple[int, int] = map_center(domain)

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
        width, height = self.__window.get_size()

        x: int = width // 2 + (pos[0] - self.__map_center[0]) * self.__scale
        y: int = height // 2 - (pos[1] - self.__map_center[1]) * self.__scale

        return x, y

    def __get_color(self, name: str | None) -> Color:
        if name is None:
            return self.__colors["lightgray"]
        try:
            return self.__colors[name]
        except KeyError:
            return self.__colors["lightgray"]

    def __draw_zones(self, zone: Zone) -> None:
        pos: tuple[int, int] = self.__positions(zone.coordinate)
        color: Color = self.__get_color(zone.metadata.color)

        pygame.draw.circle(
            self.__window,
            color,
            pos,
            10
        )

    def __draw_connection(self, conn: Connection) -> None:
        start_pos: tuple[int, int] = self.__positions(conn.zone_a.coordinate)
        end_pos: tuple[int, int] = self.__positions(conn.zone_b.coordinate)

        pygame.draw.line(
            self.__window,
            "red",
            start_pos,
            end_pos,
            width=2
        )

    def __draw(self) -> None:
        # Zones
        self.__draw_zones(self.__domain.start_hub)
        self.__draw_zones(self.__domain.end_hub)
        for zone in self.__domain.hubs:
            self.__draw_zones(zone)

        # Connection
        for conn in self.__domain.connections:
            self.__draw_connection(conn)

    def render(self) -> None:
        self.__window.blit(self.__background, (0, 0))
        self.__draw()
        pygame.display.flip()
