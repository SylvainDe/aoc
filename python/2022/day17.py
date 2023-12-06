# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

STREAM_DIR = {
    ">": 1,
    "<": -1,
}


def get_streams_from_line(string):
    return list(string)


def get_streams_from_file(file_path=resource_dir + "year2022_day17_input.txt"):
    with open(file_path) as f:
        for l in f:
            return get_streams_from_line(l.strip())


WIDTH = 7

ROCKS_STR = [
    """####""",
    """.#.
###
.#.""",
    """..#
..#
###""",
    """#
#
#
#""",
    """##
##""",
]


def convert_str_to_lst(string):
    lst = []
    for i, s in enumerate(reversed(string.splitlines())):
        for j, c in enumerate(s):
            assert c in (".", "#")
            if c == "#":
                lst.append((i, j))
    return lst


ROCKS = [convert_str_to_lst(r) for r in ROCKS_STR]


# |..@@@@.| <= x = 4
# |.......|
# |.......|
# |.......|
# +-------+ <- x = 0
#  ^
#  |_ y = 0
def show(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    assert x_min == 0
    assert y_min == 0
    assert y_max == WIDTH - 1
    x_range = list(range(x_min, x_max + 1))
    y_range = list(range(y_min, y_max + 1))
    for x in reversed(x_range):
        print("".join("#" if (x, y) in points else " " for y in y_range) + " " + str(x))


def shift_rock(rock, x, y):
    return [(i + x, j + y) for i, j in rock]


def can_take_pos(fallen_rocks, rock, x, y):
    return all(
        0 <= sr[1] < WIDTH and sr not in fallen_rocks for sr in shift_rock(rock, x, y)
    )


def simulate(streams, nb_rocks, skip_optim=False):
    # Cycle stream and rock
    stream_iter = itertools.cycle(enumerate(streams))
    rock_iter = itertools.cycle(enumerate(ROCKS))
    fallen_rocks = set((0, j) for j in range(WIDTH))
    stream_idx = None
    indices_seen = {}
    heights = {}
    for i, (rock_idx, r) in zip(range(nb_rocks), rock_iter):
        max_x = max(r[0] for r in fallen_rocks)
        last_level = tuple(
            (x, y) in fallen_rocks
            for y in range(WIDTH)
            for x in range(max_x - 6, max_x)
        )
        indices = (rock_idx, stream_idx, last_level)
        heights[i] = max_x
        if not skip_optim and indices in indices_seen:
            #      i2   i
            # |-----|---|---| ... |---|-|
            #    A    B   B         B  C
            # A: time to reach beginning of cycle
            # B: full cycles
            # C: remaining
            i2 = indices_seen[indices]
            cycle = i - i2
            after_i2 = nb_rocks - i2
            nb_cycles, rem = divmod(after_i2, cycle)
            height_cycle = heights[i] - heights[i2]
            res = nb_cycles * height_cycle + heights[i2 + rem]
            # print("Index", i, "and", i2, "look similar. We have a cycle of length", cycle)
            # print("We have", nb_cycles, "full cycles and", rem, "are remaining")
            # print("A cycle has height", height_cycle, "for a result for ", nb_rocks, "of", res)
            # print()
            return res
        indices_seen[indices] = i
        x, y = max_x + 1 + 3, 2
        while True:
            # Stream
            stream_idx, c = next(stream_iter)
            dy = STREAM_DIR[c]
            if can_take_pos(fallen_rocks, r, x, y + dy):
                y += dy
            # Fall
            if can_take_pos(fallen_rocks, r, x - 1, y):
                x += -1
            else:
                for sr in shift_rock(r, x, y):
                    fallen_rocks.add(sr)
                break
    # show(fallen_rocks)
    return max(x for x, y in fallen_rocks)


def run_tests():
    streams = get_streams_from_line(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>")
    assert simulate(streams, 2022, skip_optim=True) == 3068
    assert simulate(streams, 2022) == 3068
    # Test that optimisation seems to work on arbitrary values
    # for i in (2023, 2050, 2080): #range(2022, 2080):
    #     assert simulate(streams, i) == simulate(streams, i, skip_optim=True)
    assert simulate(streams, 1000000000000) == 1514285714288


def get_solutions():
    streams = get_streams_from_file()
    print(simulate(streams, 2022) == 3175)
    # Test that optimisation seems to work on arbitrary values
    # for i in range(2178, 2230):
    #     assert simulate(streams, i) == simulate(streams, i, skip_optim=True)
    print(simulate(streams, 1000000000000) == 1555113636385)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
