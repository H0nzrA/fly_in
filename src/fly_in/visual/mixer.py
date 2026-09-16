"""Background music playback for the visual application."""

import pygame
from ..utils import VisualError
from importlib.resources import files, as_file
from .var import Sound


class Mixer:
    """Wraps pygame's mixer to load and play background music."""

    def __init__(self) -> None:
        """Initialize the pygame mixer and load the background track.

        Raises:
            VisualError: If the pygame mixer fails to initialize.
        """
        pygame.mixer.init()
        if pygame.mixer.get_init() is None:
            raise VisualError("Pygame Mixer not initialized")
        self.__song: Sound = self.__load_sound()

    def __load_sound(self) -> Sound:
        """Load the packaged background music file.

        Returns:
            Sound: The loaded sound, ready to be played.
        """
        sound = (
            files("fly_in")
            .joinpath("resources", "music", "background.mp3")
        )
        with as_file(sound) as path:
            return Sound(path)

    def play(self) -> None:
        """Play the loaded background sound."""
        self.__song.play(-1)

    def terminate(self) -> None:
        """Shut down the pygame mixer."""
        pygame.mixer.quit()
