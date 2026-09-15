"""Shared pygame type aliases used across the visual package."""

import pygame
import time

from .visual_data import VisualData
from .var import Font, Window, Surface, Color, Movement, Rect
from importlib.resources import files, as_file
from ..domain import Map, Zone, Connection, ZoneType
from .camera import Camera


class Renderer:
    """Draws the map, drones, tooltips, and dashboard each frame."""

    def __init__(
        self,
        window: Window,
        domain: Map,
        camera: Camera,
        visual_data: VisualData
    ) -> None:
        """Initialize rendering resources for the given map and window.

        Args:
            window (Window): Window surface to render onto.
            domain (Map): Map being visualized.
            camera (Camera): Camera used to convert world coordinates.
            visual_data (VisualData): Timed drone movement data to render.
        """
        self.__window: Window = window
        self.__domain: Map = domain

        # Domain to window scale
        self.__scale: int = 75
        self.__camera: Camera = camera

        self.__visual_data: VisualData = visual_data
        self.__font: Font = Font(None, 12)
        self.__font_header: Font = Font(None, 18)

        # Animation Setup
        self.__drone_frames: list[Surface] = []
        self.__animation_speed: float = 8.0
        self.__start_time: float = time.time()
        self.__marker_colors = {
            ZoneType.NORMAL: Color("white"),
            ZoneType.PRIORITY: Color("cyan"),
            ZoneType.RESTRICTED: Color("orange"),
            ZoneType.BLOCKED: Color("dimgray"),
        }

        self.__load_image()
        self.__dark_overlay: Surface = pygame.Surface(
            self.__window.get_size(),
            pygame.SRCALPHA
        )
        self.__dark_overlay.fill((0, 0, 0, 180))

    def __load_image(self) -> None:
        """Load and prepare the background image and drone sprite frames."""
        # Background loading
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

        # Drone Sprite Sheet loading and slicing
        drone_sheet_path = (
            files("fly_in")
            .joinpath("resources", "images", "drone.png")
        )
        with as_file(drone_sheet_path) as path:
            sprite_sheet: Surface = pygame.image.load(path).convert_alpha()

            sheet_width, sheet_height = sprite_sheet.get_size()
            num_frames = 4
            frame_width = sheet_width // num_frames
            frame_height = sheet_height

            target_drone_size = (38, 38)

            for i in range(num_frames):
                rect = pygame.Rect(
                    i * frame_width,
                    0,
                    frame_width, frame_height
                )
                frame_surface = sprite_sheet.subsurface(rect)

                scaled_frame = pygame.transform.scale(
                    frame_surface,
                    target_drone_size
                )
                self.__drone_frames.append(scaled_frame)

    def __positions(self, pos: tuple[float, float]) -> tuple[float, float]:
        """Convert a world coordinate to a screen coordinate.

        Args:
            pos (tuple[float, float]): World-space coordinate.

        Returns:
            tuple[float, float]: Corresponding screen-space coordinate.
        """
        width, height = self.__window.get_size()
        cam_x, cam_y = self.__camera.get_position()

        x: float = width / 2 + (pos[0] - cam_x) * self.__scale
        y: float = height / 2 - (pos[1] - cam_y) * self.__scale

        return x, y

    def __get_color(self, name: str | None) -> Color:
        """Resolve a color name to a pygame Color, with a fallback.

        Args:
            name (str | None): Color name, or None for the default color.

        Returns:
            Color: The resolved color, or light gray if invalid.
        """
        if name is None:
            return Color("lightgray")
        try:
            return Color(name)
        except ValueError:
            return Color("lightgray")

    def __draw_zones(self, zone: Zone) -> None:
        """Draw a zone marker and its capacity/type indicator.

        Args:
            zone (Zone): Zone to draw.
        """
        pos: tuple[float, float] = self.__positions(zone.coordinate)
        color: Color = self.__get_color(zone.metadata.color)
        color.a = 70
        radius = 20
        surface: Surface = pygame.Surface(
            (radius * 2, radius * 2),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            surface,
            color,
            (radius, radius),
            radius
        )
        self.__window.blit(
            surface,
            (pos[0] - radius, pos[1] - radius)
        )

        type_color: Color = self.__marker_colors[zone.metadata.zone]
        pygame.draw.circle(
            self.__window,
            type_color,
            pos,
            radius / 3
        )

    def __draw_connection(self, conn: Connection) -> None:
        """Draw a line between the two zones of a connection.

        Args:
            conn (Connection): Connection to draw.
        """
        start_pos = self.__positions(conn.zone_a.coordinate)
        end_pos = self.__positions(conn.zone_b.coordinate)

        pygame.draw.line(
            self.__window,
            (60, 70, 90),
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
        """Linearly interpolate between two points.

        Args:
            start (tuple[float, float]): Starting point.
            end (tuple[float, float]): Ending point.
            progress (float): Interpolation factor between 0 and 1.

        Returns:
            tuple[float, float]: The interpolated, rounded point.
        """
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
        """Draw an animated drone sprite moving between two points.

        Args:
            start (tuple[float, float]): Starting world position.
            end (tuple[float, float]): Ending world position.
            progress (float): Animation progress between 0 and 1.
            drone (int | None): Drone identifier to label, if any.
        """
        start = self.__positions(start)
        end = self.__positions(end)
        pos: tuple[float, float] = self.__interpolate(start, end, progress)

        elapsed_time = time.time() - self.__start_time
        frame_index = (
            int(elapsed_time * self.__animation_speed) %
            len(self.__drone_frames)
        )
        active_drone_sprite = self.__drone_frames[frame_index]

        sprite_rect = active_drone_sprite.get_rect(center=pos)
        self.__window.blit(active_drone_sprite, sprite_rect)

        if drone is not None:
            text: Surface = self.__font.render(
                str(drone),
                True,
                "white"
            )
            text_rect: Rect = text.get_rect(center=pos)
            self.__window.blit(text, text_rect)

    def __draw_static(self) -> None:
        """Draw all zones and connections that do not change over time."""
        # Connection
        for conn in self.__domain.connections:
            self.__draw_connection(conn)

        # Zones
        self.__draw_zones(self.__domain.start_hub)
        self.__draw_zones(self.__domain.end_hub)
        for zone in self.__domain.hubs:
            self.__draw_zones(zone)

    def __draw_dynamic(self, progress: float) -> None:
        """Draw drones at their interpolated positions for the current turn.

        Args:
            progress (float): Animation progress between 0 and 1.
        """
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
        """Draw the static map elements followed by the moving drones.

        Args:
            progress (float): Animation progress between 0 and 1.
        """
        self.__draw_static()
        self.__draw_dynamic(progress)

    def __all_zones(self) -> list[Zone]:
        """Return every zone on the map.

        Returns:
            list[Zone]: The start hub, end hub, and all intermediate hubs.
        """
        return [
            self.__domain.start_hub,
            self.__domain.end_hub,
            *self.__domain.hubs,
        ]

    @staticmethod
    def __point_segment_distance(
        p: tuple[float, float],
        a: tuple[float, float],
        b: tuple[float, float]
    ) -> float:
        """Compute the shortest distance from a point to a line segment.

        Args:
            p (tuple[float, float]): Point to measure from.
            a (tuple[float, float]): First endpoint of the segment.
            b (tuple[float, float]): Second endpoint of the segment.

        Returns:
            float: The shortest distance between the point and the segment.
        """
        px, py = p
        ax, ay = a
        bx, by = b

        dx, dy = bx - ax, by - ay
        if dx == 0 and dy == 0:
            return float(((px - ax) ** 2 + (py - ay) ** 2) ** 0.5)

        t: float = max(
            0.0,
            min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy))
        )
        proj_x, proj_y = ax + t * dx, ay + t * dy

        return float(((px - proj_x) ** 2 + (py - proj_y) ** 2) ** 0.5)

    def __hit_test(self, mouse_pos: tuple[int, int]) -> Movement | None:
        """Find the zone or connection under the mouse cursor, if any.

        Args:
            mouse_pos (tuple[int, int]): Current mouse position.

        Returns:
            Movement | None: The zone or connection under the cursor, or
                None if nothing is hovered.
        """
        mx, my = mouse_pos
        radius = 20

        for zone in self.__all_zones():
            zx, zy = self.__positions(zone.coordinate)
            if (zx - mx) ** 2 + (zy - my) ** 2 <= radius ** 2:
                return zone

        threshold = 6.0
        for conn in self.__domain.connections:
            a = self.__positions(conn.zone_a.coordinate)
            b = self.__positions(conn.zone_b.coordinate)
            if self.__point_segment_distance(mouse_pos, a, b) <= threshold:
                return conn

        return None

    def __tooltip_lines(self, target: Movement) -> list[str]:
        """Build the tooltip text lines describing a zone or connection.

        Args:
            target (Movement): Zone or connection to describe.

        Returns:
            list[str]: Lines of text to display in the tooltip.
        """
        if isinstance(target, Zone):
            return [
                f"Zone: {target.name}",
                f"Type: {target.metadata.zone.value}",
                f"Capacity: {target.metadata.max_drones}",
                f"Coord: {target.coordinate}",
            ]

        return [
            f"Connection: {target.zone_a.name} - {target.zone_b.name}",
            f"Link capacity: {target.metadata.max_link_capacity}",
        ]

    def __draw_tooltip(
        self,
        mouse_pos: tuple[int, int],
        target: Movement
    ) -> None:
        """Draw a tooltip box near the mouse describing the hovered target.

        Args:
            mouse_pos (tuple[int, int]): Current mouse position.
            target (Movement): Zone or connection being hovered.
        """
        lines: list[str] = self.__tooltip_lines(target)

        padding = 6
        line_height = 14
        width = max(
            self.__font.size(line)[0] for line in lines
        ) + padding * 2
        height = line_height * len(lines) + padding * 2

        win_w, win_h = self.__window.get_size()
        x = min(mouse_pos[0] + 16, win_w - width - 4)
        y = min(mouse_pos[1] + 16, win_h - height - 4)

        box: Surface = pygame.Surface((width, height), pygame.SRCALPHA)
        box.fill((20, 20, 30, 220))
        pygame.draw.rect(box, (120, 120, 160, 255), box.get_rect(), width=1)

        for i, line in enumerate(lines):
            text: Surface = self.__font.render(line, True, "white")
            box.blit(text, (padding, padding + i * line_height))

        self.__window.blit(box, (x, y))

    def __draw_dashboard(self, playing: bool) -> None:
        """Draw the status dashboard showing turn count and delivery progress.

        Args:
            playing (bool): Whether the simulation is currently playing.
        """
        current: dict[int, Movement] = self.__visual_data.get_current()
        delivered: int = sum(
            1
            for movement in current.values()
            if isinstance(movement, Zone)
            and movement.name == self.__domain.end_hub.name
        )
        current_time: int = self.__visual_data.current_time
        simulation_time: int = current_time - 1 if current_time > 0 else 0

        lines: list[str] = [
            "Fly-in \u2014 Drone Routing Simulation",
            f"Turn: {simulation_time} / "
            f"{self.__visual_data.last_time - 1}",
            f"Delivered: {delivered} / {self.__visual_data.nb_drones}",
            f"Status: {'Playing' if playing else 'Paused'}",
        ]

        padding = 8
        line_height = 18
        width = max(
            self.__font_header.size(line)[0] for line in lines
        ) + padding * 2
        height = line_height * len(lines) + padding * 2

        box: Surface = pygame.Surface((width, height), pygame.SRCALPHA)
        box.fill((15, 15, 25, 200))
        pygame.draw.rect(box, (120, 120, 160, 255), box.get_rect(), width=1)

        for i, line in enumerate(lines):
            text: Surface = self.__font_header.render(line, True, "white")
            box.blit(text, (padding, padding + i * line_height))

        self.__window.blit(box, (12, 12))

    def render(
        self,
        progress: float,
        mouse_pos: tuple[int, int],
        playing: bool
    ) -> None:
        """Render a complete frame: the map, drones, dashboard, and tooltip.

        Args:
            progress (float): Animation progress between 0 and 1.
            mouse_pos (tuple[int, int]): Current mouse position.
            playing (bool): Whether the simulation is currently playing.
        """
        self.__window.blit(self.__background, (0, 0))
        self.__window.blit(self.__dark_overlay, (0, 0))
        self.__draw(progress)
        self.__draw_dashboard(playing)

        hover: Movement | None = self.__hit_test(mouse_pos)
        if hover is not None:
            self.__draw_tooltip(mouse_pos, hover)

        pygame.display.flip()
