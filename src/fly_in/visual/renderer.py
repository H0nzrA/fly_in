from OpenGL import GL
from ..utils import VisualError


class Renderer:
    def __init__(self) -> None:
        version: bytes | None = GL.glGetString(GL.GL_VERSION)

        if version is None:
            raise VisualError("OpenGL has no context to work with")

        GL.glClearColor(0.5, 0.8, 0.9, 1.0)

    def render(self) -> None:
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
