# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"


def get_steps_from_file(file_path=resource_dir + "year2017_day11_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip().split(",")


# Map directions in diagonale coordinates
#
#      --+      +--             --+(-1,1) +--                _
#         \ n  /                   \     /                   /| y
#      nw  +--+  ne         (-1, 0) +---+ (0, 1)            /
#         /    \                   /     \                 /
#      --+      +-- <==>        --+ (0,0) +--             /
#         \    /                   \     /                \
#      sw  +--+  se         (0, -1) +---+  (1, 0)          \
#         / s  \                   /     \                  \
#      --+      +--             --+ (1,-1)+--               _\| x

coords = {
    "nw": (-1, 0),
    "n": (-1, 1),
    "ne": (0, 1),
    "sw": (0, -1),
    "s": (1, -1),
    "se": (1, 0),
}


def get_path(steps):
    x, y = (0, 0)
    yield (x, y)
    for step in steps:
        dx, dy = coords[step]
        x += dx
        y += dy
        yield (x, y)


def get_final_position(steps):
    return list(get_path(steps))[-1]


assert (0, 0) == get_final_position(c for c in ("n", "s"))
assert (0, 0) == get_final_position(c for c in ("nw", "se"))
assert (0, 0) == get_final_position(c for c in ("ne", "sw"))
assert (0, 0) == get_final_position(c for c in coords)


def get_distance(coord):
    x, y = coord
    return max(abs(x), abs(y))


def get_final_distance(steps):
    return get_distance(get_final_position(steps))


def get_max_distance(steps):
    return max(get_distance(p) for p in get_path(steps))


def run_tests():
    assert get_final_distance("ne,ne,ne".split(",")) == 3
    assert get_final_distance("ne,ne,sw,sw".split(",")) == 0
    assert get_final_distance("ne,ne,s,s".split(",")) == 2
    assert get_final_distance("se,sw,se,sw,sw".split(",")) == 3


def get_solutions():
    steps = get_steps_from_file()
    print(get_final_distance(steps) == 707)
    print(get_max_distance(steps) == 1490)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
