State = tuple[int, int]


class WorldState:
    def __init__(self) -> None:
        self.__node_usage: dict[
            tuple[int, int],
            int
        ] = {}
        self.__edge_usage: dict[
            tuple[frozenset[int], int],
            int
        ] = {}

    def reserve_node(self, node: int, time: int) -> None:
        key: tuple[int, int] = (node, time)
        self.__node_usage[key] = self.__node_usage.get(key, 0) + 1

    def reserve_edge(self, a: int, b: int, time: int) -> None:
        key: tuple[frozenset[int], int] = (frozenset((a, b)), time)
        self.__edge_usage[key] = self.__edge_usage.get(key, 0) + 1

    def node_avaliable(self, node: int, time: int, capacity: int) -> bool:
        key: tuple[int, int] = node, time
        return self.__node_usage.get(key, 0) < capacity

    def edge_avaliable(self, a: int, b: int, time: int, capacity: int) -> bool:
        key: tuple[frozenset[int], int] = (frozenset((a, b)), time)
        return self.__edge_usage.get(key, 0) < capacity
