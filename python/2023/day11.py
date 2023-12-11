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

def get_shift_values(values, expansion_value):
    shift = 0
    for v in range(max(values) + 1):
        yield shift
        if v not in values:
            shift += expansion_value - 1

def manhattan_dist(p1, p2):
    return sum(abs(c2 - c1) for c1, c2 in zip(p1, p2))

def expand_galaxies(galaxies, expansion_value):
    shift_x = list(get_shift_values(set(x for x, _ in galaxies), expansion_value))
    shift_y = list(get_shift_values(set(y for _, y in galaxies), expansion_value))
    return set((i + shift_x[i], j + shift_y[j]) for i, j in galaxies)

def get_expanded_length_sum(grid, expansion_value):
    galaxies = expand_galaxies(get_galaxies(grid), expansion_value)
    pairs = itertools.combinations(galaxies, 2)
    return sum(manhattan_dist(*pair) for pair in pairs)

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
    assert get_expanded_length_sum(grid, 2) == 374
    assert get_expanded_length_sum(grid, 10) == 1030
    assert get_expanded_length_sum(grid, 100) == 8410


def get_solutions():
    grid = get_grid_from_file()
    print(get_expanded_length_sum(grid, 2) == 9799681)
    print(get_expanded_length_sum(grid, 1000000) == 513171773355)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
