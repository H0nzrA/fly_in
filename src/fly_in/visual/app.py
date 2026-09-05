from .platform import Platform
from ..graph import State
import pyautogui
from .input import Key, MouseButton
from ..cli import Reporter
from ..utils import VisualError, FlyInError


def get_window_size(width: int, height: int, factor: int) -> tuple[int, int]:
    w_minus: int = width - (width // factor)
    h_minus: int = height - (height // factor)

    return w_minus, h_minus


class VisualApp:
    def __init__(
        self,
        title: str
    ) -> None:
        self.__reporter: Reporter = Reporter("Visual")
        self.__title: str = title

    def __setup(self) -> None:
        screen_width, screen_height = pyautogui.size()
        window_width, window_height = get_window_size(
            screen_width, screen_height,
            6
        )
        try:
            self.__platform: Platform = Platform(
                window_width,
                window_height,
                self.__title
            )
        except VisualError as e:
            self.__reporter.error(str(e))
            raise FlyInError
        self.__reporter.info("Successfully initialize")

    def __update(self) -> None:
        if (
            self.__platform.is_key_pressed(Key.Q) or
            self.__platform.is_key_pressed(Key.ESC)
        ):
            self.__platform.close_window()

        if self.__platform.is_mouse_button_pressed(MouseButton.RIGHT):
            print("r")
        if self.__platform.is_mouse_button_pressed(MouseButton.LEFT):
            print("l")
        if self.__platform.is_mouse_button_pressed(MouseButton.MIDDLE):
            print("m")

    def run(
        self,
        paths: dict[int, list[State]]
    ) -> None:
        self.__setup()
        while not self.__platform.should_close():
            self.__platform.poll_events()
            self.__update()

            # TODO: Adding rendering
        self.__reporter.info("Visual terminated")
