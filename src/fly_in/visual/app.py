from .platform import Platform
from ..graph import State
import pyautogui


def get_window_size(width: int, height: int, factor: int) -> tuple[int, int]:
    w_minus: int = width - (width // factor)
    h_minus: int = height - (height // factor)

    return w_minus, h_minus


class VisualApp:
    def __init__(
        self,
        title: str
    ) -> None:
        screen_width, screen_height = pyautogui.size()
        window_width, window_height = get_window_size(
            screen_width, screen_height,
            6
        )
        self.__platform: Platform = Platform(
            window_width,
            window_height,
            title
        )

    def run(
        self,
        paths: dict[int, list[State]]
    ) -> None:
        while not self.__platform.should_close():
            self.__platform.pool_events()

            # TODO: Adding rendering
