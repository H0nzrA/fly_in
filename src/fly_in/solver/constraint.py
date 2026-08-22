from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class VertexConstraint:
    node: int
    time: int


@dataclass(frozen=True)
class EdgeConstraint:
    from_node: int
    to_node: int
    time: int


Constraint = Union[VertexConstraint, EdgeConstraint]
