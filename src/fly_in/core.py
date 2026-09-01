from .cli import MapSelector, Reporter
from .parser import Parser
from pathlib import Path
from .domain import Map
from .graph import Graph, State
from .solver import PrioritizedCooperative
from .logger import Output, Benchmark
from .utils import Syntax
from collections.abc import Callable


class Program:
    def __init__(self) -> None:
        self.introduction()
        self.__reporter: Reporter = Reporter(source="Core")

        self.__reporter.info("Setup environement ...")

        self.__benchmark: Benchmark = Benchmark(path="./logs/benchmark.log")

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

        self.__setup_benchmark()

        self.__reporter.info("Setup Done.")

    def __setup_benchmark(self) -> None:
        self.__compute_solver: Callable[
            [int],
            dict[int, list[State]]
        ] = self.__benchmark.mark_memory("Solver")(
            self.__solver.compute
        )

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
            paths: dict[int, list[State]] = self.__compute_solver(
                self.__map.nb_drones
            )

            self.__output.make_output(paths)

        except Exception as e:
            self.__reporter.error(str(e))

        finally:
            self.__benchmark.output_benchmark()
