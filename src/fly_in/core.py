from .cli.map_selector import MapSelector
from .parser import Parser
from .domain import Map, Zone, Connection
from .graph import Graph
from .solver import SpaceTimeAStar, VertexConstraint


class Program:
    def run(self) -> None:
        selector: MapSelector = MapSelector()
        parser: Parser = Parser(path=selector.get_map_path())
        map: Map = parser.get_map()

        graph: Graph = Graph(map=map)
        stas: SpaceTimeAStar = SpaceTimeAStar(graph)

        # path_stas: list[int] = stas.solve(
        #     graph.start_node(),
        #     graph.end_node(),
        #     constraints=set()
        # )
        # path_stas: list[int] = stas.solve(
        #     graph.start_node(),
        #     graph.end_node(),
        #     constraints={
        #         VertexConstraint(
        #             node=2,
        #             time=2
        #         )
        #     }
        # )
        path_stas: list[int] = stas.solve(
            graph.start_node(),
            graph.end_node(),
            constraints={
                VertexConstraint(2, 2),
            }
        )

        path = [
            graph.get_zone_by_id(p).name
            for p in path_stas
        ]

        print(" - ".join(path))

    def __print_zone(self, zone: Zone) -> None:
        res: str = ""

        res += zone.name + f" {zone.id} : "
        res += str(zone.coordinate) + " "
        res += zone.metadata.zone + " "
        res += str(zone.metadata.color) + " "
        res += str(zone.metadata.max_drones) + " "

        print(res)

    def __print_connection(
        self,
        connection: Connection
    ) -> None:
        res: str = ""

        res += connection.zone_a.name + " - "
        res += connection.zone_b.name
        res += f" [{connection.metadata.max_link_capacity}]"

        print(res)
