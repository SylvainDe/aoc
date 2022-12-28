# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_tiles_from_file(file_path="../../resources/year2016_day18_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


traps = set(
    [
        ("^", "^", "."),
        (".", "^", "^"),
        ("^", ".", "."),
        (".", ".", "^"),
    ]
)


def get_next_line(tiles):
    return "".join(
        "^" if val in traps else "." for val in zip("." + tiles, tiles, tiles[1:] + ".")
    )


def get_tiles(tiles, rows):
    yield tiles
    for _ in range(rows - 1):
        tiles = get_next_line(tiles)
        yield tiles


def get_nb_safe_tiles(tiles, rows):
    return "".join(get_tiles(tiles, rows)).count(".")


def run_tests():
    tiles = "..^^."
    tiles = get_next_line(tiles)
    assert tiles == ".^^^^"
    tiles = get_next_line(tiles)
    assert tiles == "^^..^"
    assert get_nb_safe_tiles(".^^.^.^^^^", 10) == 38


def get_solutions():
    tiles = get_tiles_from_file()
    print(get_nb_safe_tiles(tiles, 40) == 1982)
    print(get_nb_safe_tiles(tiles, 400000) == 20005203)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
