import glfw
from enum import Enum


class Key(Enum):
    Q = glfw.KEY_Q
    ESC = glfw.KEY_ESCAPE


class MouseButton(Enum):
    RIGHT = glfw.MOUSE_BUTTON_RIGHT
    LEFT = glfw.MOUSE_BUTTON_LEFT
    MIDDLE = glfw.MOUSE_BUTTON_MIDDLE
