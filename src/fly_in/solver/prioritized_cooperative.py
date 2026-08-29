from ..graph import Graph, WorldState, State
from .dijkstra import Dijkstra
from .spacetime_astar import SpacetimeAStar


class Agent:
    def __init__(self, id: int) -> None:
        self.id: int = id

    def __repr__(self) -> str:
        return f"D{self.id}"


class PrioritizedCooperative:
    def __init__(
        self,
        graph: Graph,
    ) -> None:
        self.__world: WorldState = WorldState()
        self.__brain: SpacetimeAStar = SpacetimeAStar(graph)
        self.__heuristic: dict[int, float] = Dijkstra().compute_distance(
            graph,
            graph.end_node(),
            graph.start_node()
        )

        self.__graph: Graph = graph

    def compute(self, nb_agent: int) -> dict[int, list[int]]:
        agents: list[Agent] = sorted(
            [
                Agent(id=i)
                for i in range(1, nb_agent + 1)
            ],
            key=lambda a: a.id
        )
        paths: dict[Agent, list[State]] = {}

        source: int = self.__graph.start_node()
        goal: int = self.__graph.end_node()
        start_time: int = 0

        for agent in agents:
            try:
                path: list[State] = self.__brain.solve(
                    self.__world,
                    source,
                    goal,
                    start_time,
                    self.__heuristic
                )

            except ValueError as e:
                raise ValueError(f"Agent {agent}: {e}")

            self.__commit(path)
            print(f"Agent {agent}: {path}")

            paths[agent] = path

        return self.__construct_agents_path(paths)

    def __commit(self, path: list[State]) -> None:
        for state in path:
            self.__world.reserve_node(*state)

        for (a, ta), (b, tb) in zip(path, path[1:]):
            if a == b:
                continue
            for time in range(ta, tb):
                self.__world.reserve_edge(a, b, time)

    def __construct_agents_path(
        self,
        paths: dict[Agent, list[State]]
    ) -> dict[int, list[int]]:
        return {}
