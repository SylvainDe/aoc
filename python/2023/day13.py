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

def is_horizontal_reflection(grid, line, with_smudge):
    expected_nb_diff = 1 if with_smudge else 0
    nb_diff = 0
    nb_lines = len(grid)
    for i in range(nb_lines):  # TODO: Better range check
        i1, i2 = line - 1 - i, line + i
        if not (0 <= i1 < i2 < nb_lines):
            break
        row1, row2 = grid[i1], grid[i2]
        assert len(row1) == len(row2)
        nb_diff += sum(v != v2 for v, v2 in zip(row1, row2))
        if nb_diff > expected_nb_diff:
            return False
    return nb_diff == expected_nb_diff

def get_horizontal_reflections(grid, with_smudge):
    return [l for l in range(1, len(grid)) if is_horizontal_reflection(grid, l, with_smudge)]

def get_reflection_summary(grid, with_smudge):
    transpose = [*zip(*grid)]
    horizontal_summary = 100 * sum(get_horizontal_reflections(grid, with_smudge))
    vertical_summary = sum(get_horizontal_reflections(transpose, with_smudge))
    assert bool(horizontal_summary) + bool(vertical_summary) == 1
    return horizontal_summary + vertical_summary

def get_reflection_summary_sum(grids, with_smudge):
    return sum(get_reflection_summary(g, with_smudge) for g in grids)

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
    assert get_reflection_summary_sum(grids, with_smudge=False) == 405
    assert get_reflection_summary_sum(grids, with_smudge=True) == 400


def get_solutions():
    grids = get_grids_from_file()
    print(get_reflection_summary_sum(grids, with_smudge=False) == 28651)
    print(get_reflection_summary_sum(grids, with_smudge=True) == 25450)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
