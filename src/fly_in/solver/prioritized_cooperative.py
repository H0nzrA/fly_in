"""Prioritized planning across multiple drones sharing the same graph."""

from ..graph import Graph, WorldState, State
from .dijkstra import Dijkstra
from .spacetime_astar import SpacetimeAStar
from ..cli import Reporter, loading
from ..utils import SolverError
from math import inf


class PrioritizedCooperative:
    """Sequentially plans conflict-free paths for multiple drones."""

    def __init__(
        self,
        graph: Graph,
    ) -> None:
        """Initialize the solver's heuristic, world state, and search engine.

        Args:
            graph (Graph): Graph the drones will be routed through.
        """
        self.__reporter: Reporter = Reporter("Solver")

        self.__reporter.info("Initialize...")
        self.__world: WorldState = WorldState()
        self.__brain: SpacetimeAStar = SpacetimeAStar(graph)
        self.__heuristic: dict[int, float] = Dijkstra().compute_distance(
            graph,
            graph.end_node(),
            graph.start_node()
        )

        if self.__heuristic[graph.start_node()] == inf:
            raise SolverError("Goal is Unreachable")

        self.__graph: Graph = graph

    def compute(self, nb_agent: int) -> dict[int, list[State]]:
        """Plan a path for each drone, one at a time, in priority order.

        Args:
            nb_agent (int): Number of drones to plan for.

        Returns:
            dict[int, list[State]]: Solved path per drone id.

        Raises:
            SolverError: If a path cannot be found for any drone.
        """
        self.__reporter.info("Start Solving ...\n")
        paths: dict[int, list[State]] = {}

        source: int = self.__graph.start_node()
        goal: int = self.__graph.end_node()
        start_time: int = 0

        for i in range(1, nb_agent + 1):
            loading(i, nb_agent)
            try:
                path: list[State] = self.__brain.solve(
                    self.__world,
                    source,
                    goal,
                    start_time,
                    self.__heuristic
                )

            except ValueError as e:
                self.__reporter.error(f"Agent id{i}: {e}")
                raise SolverError

            self.__commit(path)

            paths[i] = path

        self.__reporter.info("Finished.")
        return paths

    def __commit(self, path: list[State]) -> None:
        """Reserve a drone's path in the shared world state.

        Args:
            path (list[State]): Path to reserve.
        """
        for state in path:
            self.__world.reserve_node(*state)

        for (a, ta), (b, tb) in zip(path, path[1:]):
            if a == b:
                continue
            for time in range(ta, tb):
                self.__world.reserve_edge(a, b, time)
