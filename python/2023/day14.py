# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import copy

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_grid_from_lines(string):
    return list(string.splitlines())


def get_grid_from_file(file_path=top_dir + "resources/year2023_day14_input.txt"):
    with open(file_path) as f:
        return get_grid_from_lines(f.read())

ROUND = "O"
EMPTY = "."
CUBE = "#"

def extracts_rounds(grid):
    rounds = set()
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if value == ROUND:
                rounds.add((i, j))
                row[j] = EMPTY
    return rounds

N = (-1, 0)

def find_destination(grid, pos, direction):
    dx, dy = direction
    x, y = pos
    assert grid[x][y] == EMPTY
    while True:
        next_x, next_y = x + dx, y + dy
        if 0 <= next_x < len(grid):
            row = grid[next_x]
            if 0 <= next_y < len(row):
                c = row[next_y]
                if c == EMPTY:
                    x, y = next_x, next_y
                    continue
        return x, y

def tilt_north(grid):
    grid = [list(s) for s in grid]
    for pos in sorted(extracts_rounds(grid), key=lambda p: p[0]):
        x, y = find_destination(grid, pos, N)
        grid[x][y] = ROUND
    return grid

def get_load_after_tilt(grid):
    grid = tilt_north(grid)
    return sum(i * sum(c == ROUND for c in row)
               for i, row in enumerate(reversed(grid), start=1))

def run_tests():
    grid = get_grid_from_lines(
        """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
    )
    print(get_load_after_tilt(grid) == 136)


def get_solutions():
    grid = get_grid_from_file()
    print(get_load_after_tilt(grid) == 103614)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
