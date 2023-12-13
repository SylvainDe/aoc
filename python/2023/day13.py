# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_grids_from_lines(string):
    return [list(g.splitlines()) for g in string.split("\n\n")]


def get_grids_from_file(file_path=top_dir + "resources/year2023_day13_input.txt"):
    with open(file_path) as f:
        return get_grids_from_lines(f.read())

def is_horizontal_reflection(grid, line):
    for i, row in enumerate(grid):  # TODO: Better range check
        i2 = 2 * line - i - 1
        if 0 <= i2 < len(grid) and grid[i2] != row:
            return False
    return True

def get_horizontal_reflections(grid):
    # print(grid)
    rows = dict()
    for i, row in enumerate(grid):
        rows.setdefault(row, []).append(i)
    double_rows = set(b for lst in rows.values() for a, b in zip(lst, lst[1:]) if a+1 == b)
    return [l for l in double_rows if is_horizontal_reflection(grid, l)]

def get_reflection_summary(grid):
    transpose = [*zip(*grid)]
    return 100 * sum(get_horizontal_reflections(grid)) + sum(get_horizontal_reflections(transpose))

def get_reflection_summary_sum(grids):
    return sum(get_reflection_summary(g) for g in grids)

def run_tests():
    grids = get_grids_from_lines(
        """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    )
    assert get_reflection_summary_sum(grids) == 405


def get_solutions():
    grids = get_grids_from_file()
    print(get_reflection_summary_sum(grids) == 28651)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
