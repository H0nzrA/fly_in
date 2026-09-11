import pygame
from enum import Enum


class KeyInput(Enum):
    Q = pygame.K_q
    A = pygame.K_a
    R = pygame.K_r
    ESC = pygame.K_ESCAPE
    RIGHT = pygame.K_RIGHT
    LEFT = pygame.K_LEFT
    SPACE = pygame.K_SPACE

    @classmethod
    def to_input(cls, key: int) -> "KeyInput | None":
        try:
            return cls(key)
        except ValueError:
            return None
