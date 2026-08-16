from .cli.map_selector import MapSelector
from .parser import Parser
from .domain import Map, Zone, Connection
from .graph import Graph, BFS


class Program:
    def run(self) -> None:
        selector: MapSelector = MapSelector()
        parser: Parser = Parser(path=selector.get_map_path())
        map: Map = parser.get_map()

        # self.__print_zone(maps.start_hub)
        #
        # for hub in maps.hubs:
        #     self.__print_zone(hub)
        #
        # self.__print_zone(maps.end_hub)

        # print()
        #
        # for conn in maps.connections:
        #     self.__print_connection(conn)
        #
        # self.__print_zone(maps.end_hub)

        graph: Graph = Graph(map=map)
        solver: BFS = BFS()
        path_zone: list[int] = solver.solve(graph)

        path: list[str] = [
            graph.get_zone(p).name
            for p in path_zone
        ]
        print(path)

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
