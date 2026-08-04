import sys
import questionary
from pathlib import Path
from importlib.resources import files


class MapSelector:
    BACK = "Go BACK"
    EXIT = "EXIT"

    def __select_map(self) -> Path:
        map_root = (
            files("fly_in")
            .joinpath("maps")
        )
        difficulties = [
            d for d in map_root.iterdir()
            if d.is_dir()
        ]

        while True:
            choice = questionary.select(
                "Choose difficuly",
                choices=[
                    *[d.name.capitalize() for d in difficulties],
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
                        *[f.name for f in maps],
                        self.BACK
                    ]
                ).ask()

                if selected is None:
                    raise SystemExit

                if selected == self.BACK:
                    break

                return Path(selected_difficulty / selected)

    def get_map_path(self) -> Path:
        length: int = len(sys.argv) - 1

        if length == 1:
            return Path(sys.argv[1])

        if length > 1:
            raise ValueError("To many argument given")

        return self.__select_map()
