import glfw
from ..utils import VisualError
from typing import Any
from .input import Key, MouseButton


class Platform:
    def __init__(self, title: str) -> None:
        # Initialization
        if not glfw.init():
            raise VisualError("Failed to initialize GLFW")

        self.__key_state: set[Key] = set()
        self.__mouse_state: set[MouseButton] = set()

        # Windows and key event handling
        self.__create_window(title)
        self.__set_callback()

        # Renderer context
        glfw.make_context_current(self.__window)

    def __create_window(self, title: str) -> None:
        monitor = glfw.get_primary_monitor()
        if monitor is None:
            raise VisualError("Failed to get primary monitor")

        mode = glfw.get_video_mode(monitor)
        if mode is None:
            raise VisualError("Failed to get monitor video mode")

        screen_width: int = mode.size.width
        screen_height: int = mode.size.height

        width = screen_width - screen_width // 6
        height = screen_height - screen_height // 6

        self.__window: Any = glfw.create_window(
            width=width,
            height=height,
            title=title,
            monitor=None,
            share=None
        )

        if self.__window is None:
            self.__terminate()
            raise VisualError("Failed to create window")

    def __terminate(self) -> None:
        if self.__window is not None:
            glfw.destroy_window(self.__window)
        glfw.terminate()

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
        try:
            v_key: Key = Key(key)
        except ValueError:
            return

        if action == glfw.PRESS:
            self.__key_state.add(v_key)
        elif action == glfw.RELEASE:
            self.__key_state.discard(v_key)

    def __on_mouse(
        self,
        window: Any,
        button: int,
        action: int,
        mods: int
    ) -> None:
        try:
            v_button: MouseButton = MouseButton(button)
        except ValueError:
            return

        if action == glfw.PRESS:
            self.__mouse_state.add(v_button)
        elif action == glfw.RELEASE:
            self.__mouse_state.discard(v_button)

    def poll_events(self) -> None:
        glfw.poll_events()

    def should_close(self) -> bool:
        return bool(glfw.window_should_close(self.__window))

    def close_window(self) -> None:
        glfw.set_window_should_close(self.__window, True)

    def swap_buffer(self) -> None:
        glfw.swap_buffers(self.__window)

    def is_key_pressed(self, key: Key) -> bool:
        return key in self.__key_state

    def is_mouse_button_pressed(self, button: MouseButton) -> bool:
        return button in self.__mouse_state
