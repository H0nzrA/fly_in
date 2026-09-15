"""Pygame window, event, and clock management."""

import pygame
from ..utils import VisualError
from .input import KeyInput
from .var import Window, Clock, Event


class Platform:
    """Manages the pygame window, input events, and frame timing."""

    def __init__(self) -> None:
        """Initialize pygame and create the application window.

        Raises:
            VisualError: If pygame fails to initialize.
        """
        _, failed = pygame.init()
        if failed:
            raise VisualError("Failed to initialize pygame")

        self.__window: Window = self.__create_window()
        self.__clock: Clock = Clock()
        self.__running: bool = True

        self.__key: set[KeyInput] = set()
        self.__pressed: set[KeyInput] = set()

    def __create_window(self) -> Window:
        """Create a window sized relative to the desktop resolution.

        Returns:
            Window: The created pygame window surface.
        """
        screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
        window_size: tuple[int, int] = (
            screen_width - screen_width // 7,
            screen_height - screen_height // 7
        )
        window: Window = pygame.display.set_mode(window_size)

        return window

    def __handle_key_event(self, event: Event) -> None:
        """Update the held and pressed key sets from a keyboard event.

        Args:
            event (Event): The pygame keyboard event to process.
        """
        key: KeyInput | None = KeyInput.to_input(event.key)
        if key is None:
            return

        if event.type == pygame.KEYDOWN:
            self.__key.add(key)
            self.__pressed.add(key)
        elif event.type == pygame.KEYUP:
            self.__key.discard(key)

    def poll_events(self) -> None:
        """Process pending pygame events and update input/running state."""
        self.__pressed.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type in {pygame.KEYDOWN, pygame.KEYUP}:
                self.__handle_key_event(event)

    def get_keys(self) -> set[KeyInput]:
        """Return the keys currently held down.

        Returns:
            set[KeyInput]: Copy of the currently held keys.
        """
        return self.__key.copy()

    def get_pressed(self) -> set[KeyInput]:
        """Return the keys pressed during the current frame.

        Returns:
            set[KeyInput]: Copy of the keys pressed this frame.
        """
        return self.__pressed.copy()

    def get_mouse_position(self) -> tuple[int, int]:
        """Return the current mouse position.

        Returns:
            tuple[int, int]: The (x, y) position of the mouse cursor.
        """
        return pygame.mouse.get_pos()

    def terminate(self) -> None:
        """Signal that the application loop should stop."""
        self.__running = False

    def close(self) -> None:
        """Shut down pygame."""
        pygame.quit()

    def is_running(self) -> bool:
        """Return whether the application loop should keep running.

        Returns:
            bool: True if the platform is still running.
        """
        return self.__running

    def tick(self, fps: int = 60) -> float:
        """Advance the clock and cap the frame rate.

        Args:
            fps (int): Target frames per second. Defaults to 60.

        Returns:
            float: Milliseconds elapsed since the previous tick.
        """
        return self.__clock.tick(fps)

    def get_windows(self) -> Window:
        """Return the application window.

        Returns:
            Window: The active pygame window surface.

        Raises:
            VisualError: If the window has not been created.
        """
        if not self.__window:
            raise VisualError("Window is not created")
        return self.__window
