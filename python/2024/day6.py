# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


directions = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1),
}

FREE = 0
WALL = 1

def get_grid_content_from_lines(string):
    guard = None
    grid = dict()
    for i, l in enumerate(string.splitlines()):
        for j, c in enumerate(l):
            pos = (i, j)
            if c == '#':
                grid[pos] = WALL
            else:
                grid[pos] = FREE
                if c in directions:
                    guard = (pos, directions[c])
                else:
                    assert c == '.'
    return grid, guard


def get_grid_content_from_file(file_path=top_dir + "resources/year2024_day6_input.txt"):
    with open(file_path) as f:
        return get_grid_content_from_lines(f.read())


def run_tests():
    grid, guard = get_grid_content_from_lines(
        """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
    )



def get_solutions():
    grid, guard = get_grid_content_from_file()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
