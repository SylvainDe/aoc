# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections


def get_directions_from_file(file_path="../../resources/year2020_day24_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def sum_elementwise(it1, it2):
    return tuple(sum(x) for x in zip(it1, it2))


# https://www.redblobgames.com/grids/hexagons/#coordinates
DIRECTIONS = {
    "e": (1, 0),
    "w": (-1, 0),
    "se": (1, 1),
    "sw": (0, 1),
    "ne": (0, -1),
    "nw": (-1, -1),
}


assert DIRECTIONS["nw"] == tuple(sum_elementwise(DIRECTIONS["ne"], DIRECTIONS["w"]))
assert DIRECTIONS["ne"] == tuple(sum_elementwise(DIRECTIONS["nw"], DIRECTIONS["e"]))
assert DIRECTIONS["sw"] == tuple(sum_elementwise(DIRECTIONS["se"], DIRECTIONS["w"]))
assert DIRECTIONS["se"] == tuple(sum_elementwise(DIRECTIONS["sw"], DIRECTIONS["e"]))


def get_tile_from_direction_string(s):
    dirs = list()
    prev = ""
    for c in s:
        pair = prev + c
        direct = DIRECTIONS.get(pair, None)
        if direct is not None:
            dirs.append(direct)
            prev = ""
        else:
            prev = c
    assert prev == ""
    return tuple(sum(x) for x in zip(*dirs))


def get_tiles_flipped(strings):
    c = collections.Counter(get_tile_from_direction_string(s) for s in strings)
    return set(tile for tile, count in c.items() if count % 2)


def one_day(tiles):
    c = collections.Counter(
        sum_elementwise(t, n) for t in tiles for n in DIRECTIONS.values()
    )
    return set(
        tile
        for tile, count in c.items()
        if count in ((1, 2) if tile in tiles else (2,))
    )


def n_days(tiles, n):
    for _ in range(n):
        tiles = one_day(tiles)
    return len(tiles)


def run_tests():
    get_tile_from_direction_string("esew") == (1, 1)
    get_tile_from_direction_string("nwwswee") == (0, 0)
    example1 = [
        "sesenwnenenewseeswwswswwnenewsewsw",
        "neeenesenwnwwswnenewnwwsewnenwseswesw",
        "seswneswswsenwwnwse",
        "nwnwneseeswswnenewneswwnewseswneseene",
        "swweswneswnenwsewnwneneseenw",
        "eesenwseswswnenwswnwnwsewwnwsene",
        "sewnenenenesenwsewnenwwwse",
        "wenwwweseeeweswwwnwwe",
        "wsweesenenewnwwnwsenewsenwwsesesenwne",
        "neeswseenwwswnwswswnw",
        "nenwswwsewswnenenewsenwsenwnesesenew",
        "enewnwewneswsewnwswenweswnenwsenwsw",
        "sweneswneswneneenwnewenewwneswswnese",
        "swwesenesewenwneswnwwneseswwne",
        "enesenwswwswneneswsenwnewswseenwsese",
        "wnwnesenesenenwwnenwsewesewsesesew",
        "nenewswnwewswnenesenwnesewesw",
        "eneswnwswnwsenenwnwnwwseeswneewsenese",
        "neswnwewnwnwseenwseesewsenwsweewe",
        "wseweeenwnesenwwwswnew",
    ]
    tiles = get_tiles_flipped(example1)
    assert len(tiles) == 10
    assert n_days(tiles, 100) == 2208


def get_solutions():
    directions = get_directions_from_file()
    tiles = get_tiles_flipped(directions)
    print(len(tiles) == 282)
    print(n_days(tiles, 100) == 3445)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
