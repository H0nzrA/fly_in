import pygame
from enum import Enum


class KeyInput(Enum):
    Q = pygame.K_q
    A = pygame.K_a
    R = pygame.K_r
    ESC = pygame.K_ESCAPE
    SPACE = pygame.K_SPACE
    RIGHT = pygame.K_RIGHT
    LEFT = pygame.K_LEFT
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN

    @classmethod
    def to_input(cls, key: int) -> "KeyInput | None":
        try:
            return cls(key)
        except ValueError:
            return None
