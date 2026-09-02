import questionary
from pathlib import Path
from importlib.resources import files
from .reporter import Reporter


class MapSelector:
    BACK = "Go BACK"
    EXIT = "EXIT"

    def __init__(self) -> None:
        self.__reporter: Reporter = Reporter("Map Selector")

    def __select_map(self) -> Path:
        map_root = (
            files("fly_in")
            .joinpath("resources", "mandatory")
        )
        difficulties = [
            d for d in map_root.iterdir()
            if d.is_dir()
        ]

        while True:
            choice = questionary.select(
                "Choose difficuly",
                choices=[
                    *[
                        "Easy",
                        "Medium",
                        "Hard",
                        "Challenger"
                    ],
                    self.EXIT
                ]
            ).ask()

            if choice == self.EXIT or choice is None:
                raise SystemExit

            selected = next(
                d for d in difficulties
                if d.name.capitalize() == choice
            )
            selected_difficulty = map_root / str(selected)

            maps = [
                f for f in selected_difficulty.iterdir()
                if f.is_file()
            ]

            while True:
                selected = questionary.select(
                    "Choose Map",
                    choices=[
                        *sorted([f.name for f in maps]),
                        self.BACK
                    ]
                ).ask()

                if selected is None:
                    raise SystemExit

                if selected == self.BACK:
                    break

                return Path(selected_difficulty / selected)

    def get_map_path(self, _input: str | None) -> Path:
        if _input:
            self.__reporter.warning("Selected map is the given argument.")
            return Path(_input)

        self.__reporter.info("Mandatory map selection ...")
        path: Path = self.__select_map()
        self.__reporter.info("Selection finished.")
        return path
