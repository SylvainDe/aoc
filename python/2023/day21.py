# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_garden_from_lines(string):
    grid = set()
    start = None
    for i, row in enumerate(string.splitlines()):
        for j, val in enumerate(row):
            if val != "#":
                pos = (i, j)
                grid.add(pos)
                if val == "S":
                    start = pos
    return grid, start


def get_garden_from_file(file_path=top_dir + "resources/year2023_day21_input.txt"):
    with open(file_path) as f:
        return get_garden_from_lines(f.read())

neighbours = [(-1, 0), (+1, 0), (0, -1), (0, +1)]

def get_nb_plots(garden_plot, nb_steps):
    grid, start = garden_plot
    # TODO: Future optimisation, consider only
    # non-visited plots and check parity of manhattan distance
    positions = set([start])
    for i in range(1, nb_steps + 1):
        new_positions = set()
        for i, j in positions:
            for di, dj in neighbours:
                pos2 = (i+di, j+dj)
                if pos2 in grid:
                    new_positions.add(pos2)
        positions = new_positions
    # print(len(positions))
    return len(positions)

def run_tests():
    garden = get_garden_from_lines(
        """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
    )
    assert get_nb_plots(garden, 1) == 2
    assert get_nb_plots(garden, 2) == 4
    assert get_nb_plots(garden, 3) == 6
    assert get_nb_plots(garden, 6) == 16

def get_solutions():
    garden = get_garden_from_file()
    print(get_nb_plots(garden, 64) == 3671)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
