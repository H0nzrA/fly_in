from fly_in import Parser, Map


def test_path1() -> None:
    path = "src/fly_in/maps/hard/03_ultimate_challenge.txt"
    parser = Parser(path=path)

    fmap: Map = parser.get_map()

def test_path2() -> None:
    path = "src/fly_in/maps/easy/03_basic_capacity.txt"
    parser = Parser(path=path)

    fmap: Map = parser.get_map()

def test_path3() -> None:
    path = "src/fly_in/maps/challenger/01_the_impossible_dream.txt"
    parser = Parser(path=path)

    fmap: Map = parser.get_map()

def test_path4() -> None:
    path = "src/fly_in/maps/medium/02_circular_loop.txt"
    parser = Parser(path=path)

    fmap: Map = parser.get_map()

