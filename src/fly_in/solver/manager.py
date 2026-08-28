from ..graph import Graph, WorldState
from .dijkstra import Dijkstra
from .astar import AStar
from .drone import Drone


class Manager:
    def __init__(
        self,
        graph: Graph,
        nb_agent: int
    ) -> None:
        self.__graph: Graph = graph
        self.__world: WorldState = WorldState(
            graph=self.__graph
        )
        self.__agents: list[Drone] = [
            Drone(id=i)
            for i in range(1, nb_agent + 1)
        ]

        for agent in self.__agents:
            agent.set_position(self.__graph.start_node())

        dijkstra: Dijkstra = Dijkstra()
        self.__heuristic: dict[int, float] = dijkstra.compute_distance(
            self.__graph,
            self.__graph.end_node(),
            self.__graph.start_node()
        )

        self.__solver: AStar = AStar()

    def compute_drones(self) -> dict[int, list[int]]:
        paths: dict[int, list[int]] = {
            agent.id: []
            for agent in self.__agents
        }
        turn: int = 1

        # print("All agent position before start")
        # for agent in self.__agents:
        #     print(f"{agent.id} - {agent.get_position()}")

        while True:
            if not self.__agents:
                break

            for agent in self.__agents[:]:
                path: list[int] = self.__solver.solve(
                    self.__graph,
                    self.__world,
                    agent.get_position(),
                    self.__graph.end_node(),
                    self.__heuristic
                )
                # print(
                #     f"turn={turn} "
                #     f"D{agent.id} "
                #     f"pos={agent.get_position()} "
                #     f"J_capacity={self.__world.get_node_avaliable_capacity(13)} "
                #     f"path={path}"
                # )
                if not path:
                    paths[agent.id].append(agent.get_position())
                    continue

                if len(path) == 1:
                    self.__agents.remove(agent)
                    continue

                next_pos: int = path[1]

                if not self.__world.node_have_room(next_pos, 1):
                    paths[agent.id].append(agent.get_position())
                    continue

                self.__world.add_agent_to_node(next_pos, 1)
                self.__world.remove_agent_to_node(agent.get_position(), 1)
                agent.set_position(next_pos)
                paths[agent.id].append(next_pos)

                if next_pos == self.__graph.end_node():
                    self.__agents.remove(agent)

            turn += 1

        return paths
