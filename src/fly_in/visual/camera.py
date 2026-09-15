"""Camera positioning and panning for the map view."""

from ..domain import Map


def map_center(domain: Map) -> tuple[float, float]:
    """Compute the geometric center of every zone on the map.

    Args:
        domain (Map): Map whose zones are used to compute the center.

    Returns:
        tuple[float, float]: The (x, y) coordinate of the map's center.
    """
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
        (x_max + x_min) / 2,
        (y_max + y_min) / 2
    )

    return res


class Camera:
    """Tracks the viewport position used to render the map."""

    def __init__(self, domain: Map) -> None:
        """Initialize the camera centered on the given map.

        Args:
            domain (Map): Map used to compute the initial camera position.
        """
        x, y = map_center(domain)
        self.__x: float = x
        self.__y: float = y
        self.__speed: float = 5

    def move(self, dx: float, dy: float) -> None:
        """Pan the camera by a delta, scaled by its speed.

        Args:
            dx (float): Horizontal movement direction.
            dy (float): Vertical movement direction.
        """
        self.__x += dx * self.__speed
        self.__y += dy * self.__speed

    def get_position(self) -> tuple[float, float]:
        """Return the current camera position.

        Returns:
            tuple[float, float]: The (x, y) position of the camera.
        """
        return self.__x, self.__y
