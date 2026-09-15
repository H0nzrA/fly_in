"""Top-level visual application loop."""

from ..utils import VisualError, FlyInError
from ..cli import Reporter
from .platform import Platform
from .input import KeyInput
from .renderer import Renderer
from ..domain import Map
from ..graph import Graph, State
from .visual_data import VisualData
from .camera import Camera
from .mixer import Mixer


class VisualApp:
    """Runs the interactive pygame visualization of solved drone paths."""

    def __init__(self) -> None:
        """Initialize the reporter used for visual application logging."""
        self.__reporter: Reporter = Reporter("Visual")

    def __setup(
        self,
        domain: Map,
        graph: Graph,
        paths: dict[int, list[State]]
    ) -> None:
        """Initialize the platform, camera, renderer, mixer, and visual data.

        Args:
            domain (Map): Map being visualized.
            graph (Graph): Graph corresponding to the map.
            paths (dict[int, list[State]]): Solved path per drone id.
        """
        try:
            self.__visual_data: VisualData = VisualData(
                paths,
                graph
            )

            self.__progress: float = 1.0
            self.__duration: float = 0.6
            self.__playing: bool = False

            self.__platform: Platform = Platform()
            self.__camera: Camera = Camera(domain)
            self.__renderer: Renderer = Renderer(
                self.__platform.get_windows(),
                domain,
                self.__camera,
                self.__visual_data
            )
            self.__mixer: Mixer = Mixer()
            self.__reporter.info("Successfully initialize visual application")

        except VisualError as e:
            self.__reporter.error(str(e))
            raise FlyInError

    def __update(self) -> None:
        """Process input and advance visual states."""
        keys: set[KeyInput] = self.__platform.get_keys()
        pressed: set[KeyInput] = self.__platform.get_pressed()

        dt = self.__platform.tick() / 1000

        if KeyInput.Q in keys or KeyInput.ESC in keys:
            self.__platform.terminate()

        # Camera view update
        if KeyInput.LEFT in keys:
            self.__camera.move(-dt, 0)
        elif KeyInput.RIGHT in keys:
            self.__camera.move(dt, 0)
        elif KeyInput.UP in keys:
            self.__camera.move(0, dt)
        elif KeyInput.DOWN in keys:
            self.__camera.move(0, -dt)

        if KeyInput.R in pressed:
            self.__visual_data.reset_time()
            self.__playing = False

        if KeyInput.SPACE in pressed:
            self.__playing = not self.__playing

        if self.__progress < 1.0:

            if self.__playing:
                self.__progress += dt / self.__duration

            if self.__progress >= 1.0:
                self.__progress = 1.0

            return

        if self.__playing:
            old_time: int = self.__visual_data.current_time
            self.__visual_data.next()

            if self.__visual_data.current_time == old_time:
                self.__playing = False
            else:
                self.__progress = 0

            return

    def run(
        self,
        domain: Map,
        graph: Graph,
        paths: dict[int, list[State]]
    ) -> None:
        """Set up and run the visual application loop.

        Args:
            domain (Map): Map being visualized.
            graph (Graph): Graph corresponding to the map.
            paths (dict[int, list[State]]): Solved path per drone id.
        """
        self.__setup(
            domain,
            graph,
            paths
        )

        self.__mixer.play()
        while self.__platform.is_running():
            self.__platform.poll_events()
            self.__update()
            self.__renderer.render(
                self.__progress,
                self.__platform.get_mouse_position(),
                self.__playing
            )

        self.__mixer.terminate()
        self.__platform.close()
        self.__reporter.info("Terminal visual loop")
