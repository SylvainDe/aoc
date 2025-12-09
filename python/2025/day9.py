# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools
import math

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_tile_from_line(string):
    return tuple(int(s) for s in string.split(","))


def get_tiles_from_lines(string):
    return [get_tile_from_line(l) for l in string.splitlines()]


def get_tiles_from_file(file_path=top_dir + "resources/year2025_day9_input.txt"):
    with open(file_path) as f:
        return get_tiles_from_lines(f.read())


def get_rect_size(t1, t2):
    return math.prod(1 + abs(c1 - c2) for c1, c2 in zip(t1, t2))


def get_max_rect(tiles, is_valid):
    return max(get_rect_size(t1, t2) for t1, t2 in itertools.combinations(tiles, 2) if is_valid(t1, t2, tiles))


def is_valid_part1(t1, t2, tiles):
    return True


def is_inside(t, tiles):
    for t1, t2 in zip(tiles, tiles[1:] + [tiles[0]]):
        pass
        # TODO
        # x, y = tuple((c1 - c2) for c1, c2 in zip(t1, t2))
        # perp = (-y, x)
        # to_tile = tuple((c1 - c2) for c1, c2 in zip(t1, t))
        # dot_prod = sum(c1 * c2 for c1, c2 in zip(to_tile, perp))
        # signs.append(math.copysign(1, dot_prod))
    return True


def is_valid_part2(t1, t2, tiles):
    return is_inside(t1, tiles) and is_inside(t2, tiles)


def run_tests():
    tiles = get_tiles_from_lines(
        """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
    )
    assert get_max_rect(tiles, is_valid_part1) == 50
    print(get_max_rect(tiles, is_valid_part2)) # TODO


def get_solutions():
    tiles = get_tiles_from_file()
    print(get_max_rect(tiles, is_valid_part1) == 4748985168)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
