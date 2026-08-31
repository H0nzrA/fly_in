from .cli import MapSelector, Reporter
from .parser import Parser
from pathlib import Path
from .domain import Map
from .graph import Graph, State
from .solver import PrioritizedCooperative
from .logger import Output
from .utils import Syntax


class Program:
    def __init__(self) -> None:
        self.introduction()
        self.__reporter: Reporter = Reporter(source="Core")

        self.__reporter.info("Setup environement ...")

        selector: MapSelector = MapSelector()
        path: Path = selector.get_map_path()
        parser: Parser = Parser(path=path)

        self.__map: Map = parser.get_map()
        self.__graph: Graph = Graph(map=self.__map)

        self.__solver: PrioritizedCooperative = PrioritizedCooperative(
            self.__graph
        )

        self.__output: Output = Output(
            self.__graph, "./logs/output.log")

        self.__reporter.info("Setup Done.")

    def introduction(self) -> None:
        intro: str = "\n".join(
            (
                r" _          _   _      ______ _       ",
                r"| |        | | ( )     |  ___| |      ",
                r"| |     ___| |_|/ ___  | |_  | |_   _ ",
                r"| |    / _ \ __| / __| |  _| | | | | |",
                r"| |___|  __/ |_  \__ \ | |   | | |_| |",
                r"\_____/\___|\__| |___/ \_|   |_|\__, |",
                r"                                 __/ |",
                r"                                |___/ "
            )
        )
        print(Syntax.CLEAR)
        print(intro)

    def run(self) -> None:
        try:
            paths: dict[int, list[State]] = self.__solver.compute(
                self.__map.nb_drones
            )

            self.__output.make_output(paths)

        except Exception as e:
            self.__reporter.error(str(e))
