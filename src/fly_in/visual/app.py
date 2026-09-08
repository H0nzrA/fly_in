from ..utils import VisualError, FlyInError
from ..cli import Reporter
from .platform import Platform
from .input import KeyInput
from .renderer import Renderer


class VisualApp:
    def __init__(self) -> None:
        self.__reporter: Reporter = Reporter("Visual")

    def __setup(self) -> None:
        try:
            self.__platform: Platform = Platform()
            self.__renderer: Renderer = Renderer(self.__platform.get_windows())
            self.__reporter.info("Successfully initialize visual application")

        except VisualError as e:
            self.__reporter.info(str(e))
            raise FlyInError

    def __update(self) -> None:
        keys: set[KeyInput] = self.__platform.get_keys()
        if KeyInput.Q in keys or KeyInput.ESC in keys:
            self.__platform.terminate()

        self.__platform.tick(60)

    def run(self) -> None:
        self.__setup()

        while self.__platform.is_running():
            self.__platform.poll_events()
            self.__update()
            self.__renderer.render()

        self.__platform.close()
        self.__reporter.info("Terminal visual loop")
