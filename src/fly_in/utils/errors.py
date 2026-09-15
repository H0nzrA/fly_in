"""Exception types used throughout the application."""


class FlyInError(Exception):
    """Base exception for all application-specific errors."""

    pass


class ParserError(FlyInError):
    """Raised when a map file fails to parse."""

    def __init__(
        self,
        line_num: int,
        msg: str
    ) -> None:
        """Initialize the error with the offending line number and message.

        Args:
            line_num (int): Line number where the error occurred.
            msg (str): Description of the parsing error.
        """
        err: str = f"Line {line_num}: {msg}"
        super().__init__(err)


class SolverError(FlyInError):
    """Raised when the pathfinding solver cannot find a solution."""

    pass


class NodeNotFoundError(SolverError):
    """Raised when a requested node id does not exist in the graph."""

    def __init__(self, id: int) -> None:
        """Initialize the error with the missing node id.

        Args:
            id (int): Node id that could not be found.
        """
        super().__init__(
            f"No zone with id {id!r} found in list"
        )


class VisualError(FlyInError):
    """Raised when the visual application fails."""

    pass
