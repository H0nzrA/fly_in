class FlyInError(Exception):
    pass


class ParserError(Exception):
    def __init__(
        self,
        line_num: int,
        msg: str
    ) -> None:
        err: str = f"Line {line_num}: {msg}"
        super().__init__(err)


class SolverError(FlyInError):
    pass
