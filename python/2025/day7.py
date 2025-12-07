# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_grid_from_lines(string):
    start = None
    splitters = set()
    for i, l in enumerate(string.splitlines()):
        for j, v in enumerate(l):
            pos = (i, j)
            if v == 'S':
                start = pos
            elif v == '^':
                splitters.add(pos)
            else:
                assert v == '.'
    return start, splitters


def get_grid_from_file(file_path=top_dir + "resources/year2025_day7_input.txt"):
    with open(file_path) as f:
        return get_grid_from_lines(f.read())


def count_splits_and_timelines(grid, count_splits):
    start, splitters = grid
    beams = collections.Counter([start])
    max_x = max(x for x, _ in splitters)
    nb_splits = 0
    while True:
        beams2 = collections.Counter()
        for (x, y), c in beams.items():
            x += 1
            if (x, y) in splitters:
                nb_splits += 1
                beams2[(x, y-1)] += c
                beams2[(x, y+1)] += c
            else:
                beams2[(x, y)] += c
        beams = beams2
        if all(x > max_x for x, _ in beams.keys()):
            return nb_splits if count_splits else beams.total()


def run_tests():
    grid = get_grid_from_lines(
        """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
    )
    assert count_splits_and_timelines(grid, count_splits=True) == 21
    assert count_splits_and_timelines(grid, count_splits=False) == 40


def get_solutions():
    grid = get_grid_from_file()
    print(count_splits_and_timelines(grid, count_splits=True) == 1602)
    print(count_splits_and_timelines(grid, count_splits=False) == 135656430050438)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
