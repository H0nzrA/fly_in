import pygame
from ..utils import VisualError
from importlib.resources import files, as_file
from .var import Sound


class Mixer:
    def __init__(self) -> None:
        pygame.mixer.init()
        if pygame.mixer.get_init() is None:
            raise VisualError("Pygame Mixer not initialized")
        self.__song: Sound = self.__load_sound()

    def __load_sound(self) -> Sound:
        sound = (
            files("fly_in")
            .joinpath("resources", "music", "background.mp3")
        )
        with as_file(sound) as path:
            return Sound(path)

    def play(self) -> None:
        self.__song.play()

    def terminate(self) -> None:
        pygame.mixer.quit()
