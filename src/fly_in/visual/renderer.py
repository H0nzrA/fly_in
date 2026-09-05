from OpenGL import GL
from ..utils import VisualError


Color = tuple[float, float, float, float]


class Renderer:
    def __init__(self) -> None:
        version: bytes | None = GL.glGetString(GL.GL_VERSION)

        if version is None:
            raise VisualError("OpenGL has no context to work with")

        self.__bg: Color = (
            15 / 255,
            17 / 255,
            23 / 255,
            1.0,
        )
        GL.glClearColor(*self.__bg)

    def render(self) -> None:
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
