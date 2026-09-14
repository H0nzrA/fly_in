import pygame
from ..utils import VisualError
from .input import KeyInput
from .var import Window, Clock, Event


class Platform:
    def __init__(self) -> None:
        _, failed = pygame.init()
        if failed:
            raise VisualError("Failed to initialize pygame")

        self.__window: Window = self.__create_window()
        self.__clock: Clock = Clock()
        self.__running: bool = True

        self.__key: set[KeyInput] = set()
        self.__pressed: set[KeyInput] = set()

    def __create_window(self) -> Window:
        screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
        window_size: tuple[int, int] = (
            screen_width - screen_width // 7,
            screen_height - screen_height // 7
        )
        window: Window = pygame.display.set_mode(window_size)

        return window

    def __handle_key_event(self, event: Event) -> None:
        key: KeyInput | None = KeyInput.to_input(event.key)
        if key is None:
            return

        if event.type == pygame.KEYDOWN:
            self.__key.add(key)
            self.__pressed.add(key)
        elif event.type == pygame.KEYUP:
            self.__key.discard(key)

    def poll_events(self) -> None:
        self.__pressed.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type in {pygame.KEYDOWN, pygame.KEYUP}:
                self.__handle_key_event(event)

    def get_keys(self) -> set[KeyInput]:
        return self.__key.copy()

    def get_pressed(self) -> set[KeyInput]:
        return self.__pressed.copy()

    def get_mouse_position(self) -> tuple[int, int]:
        return pygame.mouse.get_pos()

    def terminate(self) -> None:
        self.__running = False

    def close(self) -> None:
        pygame.quit()

    def is_running(self) -> bool:
        return self.__running

    def tick(self, fps: int = 60) -> float:
        return self.__clock.tick(fps)

    def get_windows(self) -> Window:
        if not self.__window:
            raise VisualError("Window is not created")
        return self.__window
