from .platform import Platform
from ..graph import State
from .input import Key, MouseButton
from ..cli import Reporter
from ..utils import VisualError, FlyInError
from .renderer import Renderer


class VisualApp:
    def __init__(
        self,
        title: str
    ) -> None:
        self.__reporter: Reporter = Reporter("Visual")
        self.__title: str = title

    def __setup(self) -> None:
        # Platform initialization
        try:
            self.__platform: Platform = Platform(self.__title)
        except VisualError as e:
            self.__reporter.error(str(e))
            raise FlyInError

        # Renderer initialization
        self.__renderer: Renderer = Renderer()

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
            self.__renderer.render()
            self.__platform.swap_buffer()

        self.__reporter.info("Visual terminated")
