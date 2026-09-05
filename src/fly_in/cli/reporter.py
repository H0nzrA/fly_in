from ..utils import Syntax
from datetime import datetime


def loading(count: int, total: int) -> None:
    """
    Build a textual progress bar.

    Args:
        count (int): Number of completed task.
        total (int): Total number of tasks.
    """
    block: int = 60
    if total <= 0:
        print("█" * block)
    print(Syntax.CURSOR_UP + Syntax.CLEAR_LINE, end="")

    if count >= total:
        print(Syntax.CLEAR_LINE, end="")
        return

    filled = min(block, max(0, (block * count) // total))

    print(
        (Syntax.DARK_CYAN + "█" + Syntax.RESET) * filled
        + f"{Syntax.DIM}█{Syntax.RESET}" * (block - filled) +
        f" {count/total * 100:.2f}%"
    )


class Reporter:
    def __init__(self, source: str) -> None:
        self.source: str = Syntax.BOLD + Syntax.MAGENTA + f"[{source}]"
        self.minfo: str = Syntax.BOLD + Syntax.BLUE + "[INFO]" + Syntax.RESET
        self.mwarning: str = (
            Syntax.BOLD + Syntax.YELLOW +
            "[WARNING]" + Syntax.RESET
        )
        self.merror: str = Syntax.BOLD + Syntax.RED + "[ERROR]" + Syntax.RESET

    def info(self, msg: str) -> None:
        print(f"--- {self.__time()}{self.source} - {self.minfo} {msg}")

    def warning(self, msg: str) -> None:
        print(f"--- {self.__time()}{self.source} - {self.mwarning} {msg}")

    def error(self, msg: str) -> None:
        print(f"--- {self.__time()}{self.source} - {self.merror} {msg}")

    def __time(self) -> str:
        current_time = datetime.now().time()
        return f"{Syntax.DIM}[{current_time}]{Syntax.RESET}"
