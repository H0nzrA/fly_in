from .cli import MapSelector, Reporter, argument_parser
from .parser import Parser
from pathlib import Path
from .domain import Map
from .graph import Graph, State
from .solver import PrioritizedCooperative
from .logger import Output, Benchmark
from .utils import Syntax, FlyInError
from argparse import Namespace
from .visual import VisualApp


class Program:
    def __init__(self) -> None:
        self.introduction()
        self.__reporter: Reporter = Reporter(source="Core")

    def setup(self) -> None:
        self.__reporter.info("Setup environement ...")

        arguments: Namespace = argument_parser()

        selector: MapSelector = MapSelector()
        path: Path = selector.get_map_path(arguments.input)
        parser: Parser = Parser(path=path)

        self.__map: Map = parser.get_map()
        self.__graph: Graph = Graph(map=self.__map)

        self.__solver: PrioritizedCooperative = PrioritizedCooperative(
            self.__graph
        )

        self.__benchmark: Benchmark = Benchmark(
            arguments.benchmark,
            self.__map,
            path
        )

        self.__output: Output = Output(
            self.__graph,
            arguments.output
        )

        self.__visual: VisualApp = VisualApp(self.__map)

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
            self.setup()
            paths: dict[int, list[State]] = self.__benchmark.run(
                "Solver",
                self.__solver.compute,
                self.__map.nb_drones
            )
            self.__output.make_output(paths)

            self.__benchmark.run(
                "Visual",
                self.__visual.run
            )
            self.__benchmark.output_benchmark()

        except FlyInError as e:
            self.__reporter.error(str(e))
            return
