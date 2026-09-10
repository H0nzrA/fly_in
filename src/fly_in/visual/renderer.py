import pygame

from .visual_data import VisualData
from .var import Window, Surface, Color, Movement
from importlib.resources import files, as_file
from ..domain import Map, Zone, Connection


def map_center(domain: Map) -> tuple[float, float]:
    coord: list[tuple[float, float]] = [
        zone.coordinate
        for zone in domain.hubs
    ]
    coord.append(domain.start_hub.coordinate)
    coord.append(domain.end_hub.coordinate)

    x_max = max(x for x, y in coord)
    x_min = min(x for x, y in coord)
    y_max = max(y for x, y in coord)
    y_min = min(y for x, y in coord)

    res: tuple[float, float] = (
        (x_max + x_min) // 2,
        (y_max + y_min) // 2
    )

    return res


class Renderer:
    def __init__(
        self,
        window: Window,
        domain: Map,
        visual_data: VisualData
    ) -> None:
        self.__window: Window = window
        self.__load_image()
        self.__domain: Map = domain

        # Domain to window scale
        self.__scale: int = 50
        self.__map_center: tuple[float, float] = map_center(domain)

        # Color data
        self.__colors: dict[str, Color] = pygame.color.THECOLORS

        self.__visual_data: VisualData = visual_data

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

    def __positions(self, pos: tuple[float, float]) -> tuple[float, float]:
        width, height = self.__window.get_size()

        x: float = width / 2 + (pos[0] - self.__map_center[0]) * self.__scale
        y: float = height / 2 - (pos[1] - self.__map_center[1]) * self.__scale

        return x, y

    def __get_color(self, name: str | None) -> Color:
        if name is None:
            return self.__colors["lightgray"]
        try:
            return self.__colors[name]
        except KeyError:
            return self.__colors["lightgray"]

    def __draw_zones(self, zone: Zone) -> None:
        pos: tuple[float, float] = self.__positions(zone.coordinate)
        color: Color = self.__get_color(zone.metadata.color)

        pygame.draw.circle(
            self.__window,
            color,
            pos,
            10
        )

    def __draw_connection(self, conn: Connection) -> None:
        start_pos = self.__positions(conn.zone_a.coordinate)
        end_pos = self.__positions(conn.zone_b.coordinate)

        pygame.draw.line(
            self.__window,
            "red",
            start_pos,
            end_pos,
            width=2
        )

    def __interpolate(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        progress: float
    ) -> tuple[float, float]:
        x: float = start[0] + (end[0] - start[0]) * progress
        y: float = start[1] + (end[1] - start[1]) * progress

        return (round(x), round(y))

    def __draw_drone(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        progress: float
    ) -> None:
        start = self.__positions(start)
        end = self.__positions(end)
        pos: tuple[float, float] = self.__interpolate(start, end, progress)

        pygame.draw.circle(
            self.__window,
            "purple",
            pos,
            5
        )

    def __draw_static(self) -> None:
        # Connection
        for conn in self.__domain.connections:
            self.__draw_connection(conn)

        # Zones
        self.__draw_zones(self.__domain.start_hub)
        self.__draw_zones(self.__domain.end_hub)
        for zone in self.__domain.hubs:
            self.__draw_zones(zone)

    def __draw_dynamic(self, progress: float) -> None:
        current_time: int = self.__visual_data.current_time
        current: dict[int, Movement] = self.__visual_data.get_current()

        if current_time == 0:
            for drone, movement in current.items():
                pos = self.__visual_data.get_movement_position(movement)
                self.__draw_drone(pos, pos, progress)
            return

        previous: dict[int, Movement] = self.__visual_data.get_at(
            current_time - 1
        )
        for drone, movement in current.items():
            p_move: Movement = previous[drone]
            start = self.__visual_data.get_movement_position(p_move)
            end = self.__visual_data.get_movement_position(movement)
            self.__draw_drone(start, end, progress)

    def __draw(self, progress: float) -> None:
        self.__draw_static()
        self.__draw_dynamic(progress)

    def render(self, progress: float) -> None:
        self.__window.blit(self.__background, (0, 0))
        self.__draw(progress)
        pygame.display.flip()
