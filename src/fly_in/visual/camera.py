from ..domain import Map


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
        (x_max + x_min) / 2,
        (y_max + y_min) / 2
    )

    return res


class Camera:
    def __init__(self, domain: Map) -> None:
        x, y = map_center(domain)
        self.__x: float = x
        self.__y: float = y
        self.__speed: float = 5

    def move(self, dx: float, dy: float) -> None:
        self.__x += dx * self.__speed
        self.__y += dy * self.__speed

    def get_position(self) -> tuple[float, float]:
        return self.__x, self.__y
