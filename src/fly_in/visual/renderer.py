import pygame
from .var import Window, Surface
from importlib.resources import files, as_file


class Renderer:
    def __init__(self, window: Window) -> None:
        self.__window: Window = window
        self.__load_image()

    def __load_image(self) -> None:
        bg = (
            files("fly_in")
            .joinpath("resources", "images", "background.jpg")
        )
        with as_file(bg) as path:
            self.__background: Surface = pygame.image.load(path)
            w_size = self.__window.get_size()
            self.__background = pygame.transform.scale(
                self.__background,
                w_size
            )

    def render(self) -> None:
        self.__window.blit(self.__background, (0, 0))
        pygame.display.flip()
