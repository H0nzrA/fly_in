import glfw
from ..utils import VisualError
from ..cli import Reporter
from typing import Any


class Platform:
    def __init__(
        self,
        width: int,
        height: int,
        title: str
    ) -> None:
        # Initialization
        self.__reporter: Reporter = Reporter("Platform")
        if not glfw.init():
            self.__reporter.error("Failed to initialize GLFW")
            raise VisualError

        # Windows and key event handling
        self.__create_window(width, height, title)
        glfw.set_key_callback(self.__window, self.__on_key)

        self.__exit_key: set[int] = {
            glfw.KEY_Q,
            glfw.KEY_ESCAPE
        }

        self.__reporter.info("GLFW initialized successfully")

    def __create_window(
        self,
        width: int,
        height: int,
        title: str
    ) -> None:
        self.__window: Any = glfw.create_window(
            width=width,
            height=height,
            title=title,
            monitor=None,
            share=None
        )

        if self.__window is None:
            self.__reporter.error("Failed to create window")
            self.__terminate()
            raise VisualError

        self.__reporter.info("Windows created")

    def __terminate(self) -> None:
        glfw.destroy_window(self.__window)
        glfw.terminate()
        self.__reporter.info("GLFW terminated")

    def __on_key(
        self,
        window: Any,
        key: int,
        scancode: int,
        action: int,
        mods: int
    ) -> None:
        if key in self.__exit_key and action == glfw.PRESS:
            self.__reporter.info("Quitting: Going down now")
            glfw.set_window_should_close(window, True)

    def run(self) -> None:
        while not glfw.window_should_close(self.__window):
            glfw.poll_events()

        self.__terminate()

    def get_window(self) -> Any:
        return self.__window
