# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools

STREAM_DIR = {
    '>': 1,
    '<': -1,
}

def get_streams_from_line(string):
    return [c for c in string]

def get_streams_from_file(file_path="../../resources/year2022_day17_input.txt"):
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
            assert c in ('.', '#')
            if c == '#':
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
        print("".join('#' if (x, y) in points else ' ' for y in y_range) + " " + str(x))


def shift_rock(rock, x, y):
    return [(i+x, j+y) for i, j in rock]

def can_take_pos(fallen_rocks, rock, x, y):
    return all(0 <= sr[1] < WIDTH and sr not in fallen_rocks
               for sr in shift_rock(rock, x, y))

def simulate(streams, nb_rocks):
    # Cycle stream and rock - maybe we could find LCM for optimisation
    stream_iter = itertools.cycle(streams)
    rock_iter = itertools.cycle(ROCKS)
    fallen_rocks = set((0, j) for j in range(WIDTH))
    for _, r in zip(range(nb_rocks), rock_iter):
        max_x = max(r[0] for r in fallen_rocks)
        x, y = max_x + 1 + 3, 2
        while True:
            # Stream
            dy = STREAM_DIR[next(stream_iter)]
            if can_take_pos(fallen_rocks, r, x, y + dy):
                y += dy
            # Fall
            if can_take_pos(fallen_rocks, r, x-1, y):
                x += -1
            else:
                for sr in shift_rock(r, x, y):
                    fallen_rocks.add(sr)
                break
    # show(fallen_rocks)
    return max(x for x, y in fallen_rocks)

def run_tests():
    streams = get_streams_from_line(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>")
    assert simulate(streams, 2022) == 3068


def get_solutions():
    streams = get_streams_from_file()
    print(simulate(streams, 2022) == 3175)

if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
