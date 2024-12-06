# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_position_from_string(string):
    return tuple(int(s) for s in string.split(","))


def get_brick_from_line(string):
    return tuple(get_position_from_string(s) for s in string.split("~"))


def get_bricks_from_lines(string):
    return [get_brick_from_line(l) for l in string.splitlines()]


def get_bricks_from_file(file_path=top_dir + "resources/year2023_day22_input.txt"):
    with open(file_path) as f:
        return get_bricks_from_lines(f.read())


def get_full_brick(brick_ends):
    return set(
        itertools.product(
            *(range(min(pair), max(pair) + 1) for pair in zip(*brick_ends))
        )
    )


def get_nb_disintegrable_bricks(bricks):
    ...  # TODO


def run_tests():
    full_bricks = {
        "0,0,10~1,0,10": [(0, 0, 10), (1, 0, 10)],
        "1,0,10~0,0,10": [(0, 0, 10), (1, 0, 10)],
        "2,2,2~2,2,2": [(2, 2, 2)],
        "0,0,1~0,0,10": [(0, 0, i) for i in range(1, 10 + 1)],
    }
    for s, b in full_bricks.items():
        assert get_full_brick(get_brick_from_line(s)) == set(b)
    bricks = get_bricks_from_lines(
        """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
    )
    print(get_nb_disintegrable_bricks(bricks), 5)


def get_solutions():
    bricks = get_bricks_from_file()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
