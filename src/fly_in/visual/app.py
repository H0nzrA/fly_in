import pygame
from ..utils import VisualError
from ..cli import Reporter


class VisualApp:
    def __init__(self) -> None:
        self.__reporter: Reporter = Reporter("Visual")

    def setup(self) -> None:
        _, failed = pygame.init()
        if failed:
            self.__reporter.error("Failed to fully initialize pygame")
            raise VisualError

        # Window
        width, height = pygame.display.get_desktop_sizes()[0]
        window_size = (width - width // 8, height - height // 8)
        self.__window = pygame.display.set_mode(window_size)

        self.__clock = pygame.time.Clock()
        self.__running = True

        self.__reporter.info("Visual application initialized")

    def __poll_events(self) -> None:
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in {pygame.K_ESCAPE, pygame.K_q}:
                    self.__running = False

    def __update(self) -> None:
        ...

    def __render(self) -> None:
        self.__window.fill("purple")
        pygame.display.flip()

    def run(self) -> None:
        self.setup()
        while self.__running:
            self.__poll_events()
            self.__update()
            self.__render()
            self.__clock.tick(60)

        pygame.quit()
        self.__reporter.info("Visual application terminated")
