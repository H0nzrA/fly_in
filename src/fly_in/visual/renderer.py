import pygame

from .visual_data import VisualData
from .var import Font, Window, Surface, Color, Movement, Rect
from importlib.resources import files, as_file
from ..domain import Map, Zone, Connection
from .camera import Camera


class Renderer:
    def __init__(
        self,
        window: Window,
        domain: Map,
        camera: Camera,
        visual_data: VisualData
    ) -> None:
        self.__window: Window = window
        self.__load_image()
        self.__domain: Map = domain

        # Domain to window scale
        self.__scale: int = 75
        self.__camera: Camera = camera

        # Color data
        self.__colors: dict[str, Color] = pygame.color.THECOLORS

        self.__visual_data: VisualData = visual_data
        self.__font: Font = Font(None, 12)

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
        cam_x, cam_y = self.__camera.get_position()

        x: float = width / 2 + (pos[0] - cam_x) * self.__scale
        y: float = height / 2 - (pos[1] - cam_y) * self.__scale

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
        progress: float,
        drone: int | None = None
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
        if drone is not None:
            text: Surface = self.__font.render(
                str(drone),
                True,
                "white"
            )
            text_rect: Rect = text.get_rect(center=pos)

            self.__window.blit(text, text_rect)

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

        previous: dict[int, Movement] = self.__visual_data.get_at(
            current_time - 1
        )
        for drone, movement in current.items():
            p_move: Movement = previous[drone]
            start = self.__visual_data.get_movement_position(p_move)
            end = self.__visual_data.get_movement_position(movement)

            if current_time == 0:
                self.__draw_drone(start, start, progress)
            elif current_time == self.__visual_data.last_time:
                self.__draw_drone(start, end, progress)
            else:
                self.__draw_drone(start, end, progress, drone)

    def __draw(self, progress: float) -> None:
        self.__draw_static()
        self.__draw_dynamic(progress)

    def render(self, progress: float) -> None:
        self.__window.blit(self.__background, (0, 0))
        self.__draw(progress)
        pygame.display.flip()
