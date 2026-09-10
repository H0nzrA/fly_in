from ..utils import VisualError, FlyInError
from ..cli import Reporter
from .platform import Platform
from .input import KeyInput
from .renderer import Renderer
from ..domain import Map
from ..graph import Graph, State
from .visual_data import VisualData


class VisualApp:
    def __init__(self) -> None:
        self.__reporter: Reporter = Reporter("Visual")

    def __setup(
        self,
        domain: Map,
        graph: Graph,
        paths: dict[int, list[State]]
    ) -> None:
        try:
            self.__visual_data: VisualData = VisualData(
                paths,
                graph
            )

            self.__progress: float = 0.0
            self.__duration: float = 0.3

            self.__platform: Platform = Platform()
            self.__renderer: Renderer = Renderer(
                self.__platform.get_windows(),
                domain,
                self.__visual_data
            )
            self.__reporter.info("Successfully initialize visual application")

        except VisualError as e:
            self.__reporter.info(str(e))
            raise FlyInError

    def __update(self) -> None:
        keys: set[KeyInput] = self.__platform.get_keys()
        if KeyInput.Q in keys or KeyInput.ESC in keys:
            self.__platform.terminate()

        if self.__progress > 1:
            if KeyInput.RIGHT in keys:
                self.__visual_data.next()
                self.__progress = 0
            elif KeyInput.LEFT in keys:
                self.__visual_data.previous()
                self.__progress = 0

        else:
            dt = self.__platform.tick() / 1000
            self.__progress += dt / self.__duration

    def run(
        self,
        domain: Map,
        graph: Graph,
        paths: dict[int, list[State]]
    ) -> None:
        self.__setup(
            domain,
            graph,
            paths
        )

        while self.__platform.is_running():
            self.__platform.poll_events()
            self.__update()
            self.__renderer.render(self.__progress)

        self.__platform.close()
        self.__reporter.info("Terminal visual loop")
