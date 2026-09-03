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
        self.__set_callback()

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
        if self.__window is not None:
            glfw.destroy_window(self.__window)
        glfw.terminate()
        self.__reporter.info("GLFW terminated")

    def __set_callback(self) -> None:
        glfw.set_key_callback(self.__window, self.__on_key)
        glfw.set_mouse_button_callback(self.__window, self.__on_mouse)

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

    def __on_mouse(
        self,
        window: Any,
        button: int,
        action: int,
        mods: int
    ) -> None:
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            self.__reporter.info("Left Button pressed")

    def pool_events(self) -> None:
        glfw.poll_events()

    def should_close(self) -> bool:
        return bool(glfw.window_should_close(self.__window))

    def get_window(self) -> Any:
        return self.__window
