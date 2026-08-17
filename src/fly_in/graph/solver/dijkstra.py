from ..graph import Graph


class Dijkstra:
    def solve(
        self,
        graph: Graph
    ) -> list[int]:
        distance: dict[int, float] = {
            node: float("inf")
            for node in graph.get_nodes()
        }
        parent: dict[int, int | None] = {
            node: None
            for node in graph.get_nodes()
        }
        unvisited: list[int] = [
            node
            for node in graph.get_nodes()
        ]

        # Start of the Dijkstra's algorithm
        source: int = graph.start_node()
        goal: int = graph.end_node()
        distance[source] = 0
        parent[source] = None
        while unvisited:
            current, unvisited = self.__remove_smallest_distance(
                unvisited,
                distance
            )

            if current == goal:
                return self.__reconstruct_path(parent, goal)

            for neighbor, weight in graph.neighbors(current).items():
                if neighbor in unvisited:
                    self.__relax(
                        current,
                        neighbor,
                        weight,
                        parent,
                        distance
                    )

        raise ValueError("Impossible to go to the end")

    def __relax(
        self,
        u: int,
        v: int,
        w: float,
        parent: dict[int, int | None],
        distance: dict[int, float]
    ) -> None:
        if distance[u] + w < distance[v]:
            distance[v] = distance[u] + w
            parent[v] = u

    def __remove_smallest_distance(
        self,
        unvisited: list[int],
        distance: dict[int, float]
    ) -> tuple[int, list[int]]:
        smallest: int = unvisited[0]

        for node in unvisited:
            if distance[node] < distance[smallest]:
                smallest = node

        unvisited.remove(smallest)
        return (smallest, unvisited)

    def __reconstruct_path(
        self,
        parent: dict[int, int | None],
        current: int
    ) -> list[int]:
        node: int | None = current
        path: list[int] = []

        while node is not None:
            path.append(node)
            node = parent[node]

        path.reverse()
        return path
