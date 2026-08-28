from .graph import Graph
from pydantic import BaseModel, PrivateAttr, ConfigDict, model_validator


class NodeState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    total_capacity: int

    __current_occupancy: int = PrivateAttr(default=0)

    def add_agent(self, nb_agent: int) -> None:
        if self.__current_occupancy + nb_agent > self.total_capacity:
            raise ValueError("Max Capacity Reach")

        self.__current_occupancy += nb_agent

    def remove_agent(self, nb_agent: int) -> None:
        self.__current_occupancy -= nb_agent

    def avaliable_capacity(self) -> int:
        return self.total_capacity - self.__current_occupancy


class WorldState(BaseModel):
    graph: Graph

    __nodes: dict[int, NodeState] = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def intialization(self) -> "WorldState":
        self.__nodes = {
            node: NodeState(
                id=node,
                total_capacity=self.graph.get_node_capacity(node)
            )
            for node in self.graph.get_nodes()
        }

        return self

    def get_node_avaliable_capacity(self, id: int) -> int:
        return self.__nodes[id].avaliable_capacity()

    def add_agent_to_node(self, id: int, nb_agent: int) -> None:
        self.__nodes[id].add_agent(nb_agent)

    def remove_agent_to_node(self, id: int, nb_agent: int) -> None:
        self.__nodes[id].remove_agent(nb_agent)

    def node_have_room(self, id: int, nb_agent: int) -> bool:
        nstate: NodeState = self.__nodes[id]

        return nstate.avaliable_capacity() >= nb_agent
