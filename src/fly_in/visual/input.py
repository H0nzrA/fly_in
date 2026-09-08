import pygame
from enum import Enum


class KeyInput(Enum):
    Q = pygame.K_q
    ESC = pygame.K_ESCAPE

    @classmethod
    def to_input(cls, key: int) -> "KeyInput | None":
        try:
            return cls(key)
        except ValueError:
            return None
