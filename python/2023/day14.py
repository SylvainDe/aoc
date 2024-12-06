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

N = (-1, 0)
S = (+1, 0)
W = (0, -1)
E = (0, +1)


def extracts_rounds(grid):
    rounds = set()
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if value == ROUND:
                rounds.add((i, j))
                row[j] = EMPTY
    return rounds


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


def tilt_direction(grid, direction):
    dx, dy = direction
    grid = [list(s) for s in grid]
    for pos in sorted(
        extracts_rounds(grid), key=lambda p: dx * p[0] + dy * p[1], reverse=True
    ):
        x, y = find_destination(grid, pos, direction)
        grid[x][y] = ROUND
    return grid


def get_load_for_grid(grid):
    return sum(
        i * sum(c == ROUND for c in row)
        for i, row in enumerate(reversed(grid), start=1)
    )


def get_load_after_tilt(grid):
    return get_load_for_grid(tilt_direction(grid, N))


def get_load_after_cycles(grid, nb_cycle):
    seen = dict()
    for i in range(nb_cycle):
        for direc in (N, W, S, E):
            grid = tilt_direction(grid, direc)
        hashable = tuple(tuple(row) for row in grid)
        if hashable in seen:
            last_seen = seen[hashable]
            period = i - last_seen
            if (nb_cycle - i - 1) % period == 0:
                break
        seen[hashable] = i
    # print("\n".join("".join(row) for row in grid))
    return get_load_for_grid(grid)


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
    assert get_load_after_tilt(grid) == 136
    grid_after_1_cycle = get_grid_from_lines(
        """.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#...."""
    )
    grid_after_2_cycle = get_grid_from_lines(
        """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O"""
    )
    grid_after_3_cycle = get_grid_from_lines(
        """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O"""
    )
    assert get_load_after_cycles(grid, 1) == get_load_for_grid(grid_after_1_cycle)
    assert get_load_after_cycles(grid, 2) == get_load_for_grid(grid_after_2_cycle)
    assert get_load_after_cycles(grid, 3) == get_load_for_grid(grid_after_3_cycle)
    assert get_load_after_cycles(grid, 1000000000) == 64


def get_solutions():
    grid = get_grid_from_file()
    print(get_load_after_tilt(grid) == 103614)
    print(get_load_after_cycles(grid, 1000000000) == 83790)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
