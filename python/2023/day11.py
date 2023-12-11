# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_grid_from_lines(string):
    return list(string.splitlines())


def get_grid_from_file(file_path=top_dir + "resources/year2023_day11_input.txt"):
    with open(file_path) as f:
        return get_grid_from_lines(f.read())


def get_galaxies(grid):
    return set((i, j) for i, row in enumerate(grid) for j, cell in enumerate(row) if cell == '#')


def show_galaxies(galaxies):
    xs = set(x for x, _ in galaxies)
    ys = set(y for _, y in galaxies)
    for x in range(max(xs) + 1):
         for y in range(max(ys) + 1):
             print("#" if (x, y) in galaxies else ".", end="")
         print()

def get_shift_values(values):
    shift = 0
    for v in range(max(values) + 1):
        yield shift
        if v not in values:
            shift += 1

def expand_galaxies(galaxies):
    xs = set(x for x, _ in galaxies)
    ys = set(y for _, y in galaxies)
    shift_x = list(get_shift_values(xs))
    shift_y = list(get_shift_values(ys))
    return set((i + shift_x[i], j + shift_y[j]) for i, j in galaxies)

def get_expanded_length_sum(grid):
    galaxies = expand_galaxies(get_galaxies(grid))
    return sum(abs(x1 - x2) + abs(y1 - y2) for (x1, y1), (x2, y2) in itertools.combinations(galaxies, 2))

def run_tests():
    grid = get_grid_from_lines(
        """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    )
    assert get_expanded_length_sum(grid) == 374


def get_solutions():
    grid = get_grid_from_file()
    print(get_expanded_length_sum(grid) == 9799681)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
