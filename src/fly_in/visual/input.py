"""Keyboard input mapping for the visual application."""

import pygame
from enum import Enum


class KeyInput(Enum):
    """Keyboard keys recognized by the visual application."""

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
        """Convert a raw pygame key code to a KeyInput member.

        Args:
            key (int): Raw pygame key code.

        Returns:
            KeyInput | None: The matching key, or None if the code is not
                mapped.
        """
        try:
            return cls(key)
        except ValueError:
            return None
