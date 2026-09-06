from ..utils import VisualError


class Orthographic:
    def __init__(
        self,
        left: float | int,
        right: float | int,
        bottom: float | int,
        top: float | int
    ) -> None:
        if right <= left:
            raise VisualError(
                "Orthographic: coordinate right must be greater than left"
            )

        if top <= bottom:
            raise VisualError(
                "Orthographic: coordinate top must be greater than bottom"
            )

        self.left: float = left
        self.right: float = right
        self.bottom: float = bottom
        self.top: float = top

        self.width: float = self.right - self.left
        self.height: float = self.top - self.bottom

    def project(
        self,
        x: float | int,
        y: float | int
    ) -> tuple[float, float]:
        x_ndc: float = (2 * (x - self.left) / self.width) - 1
        y_ndc: float = (2 * (y - self.bottom) / self.height) - 1

        return x_ndc, y_ndc
