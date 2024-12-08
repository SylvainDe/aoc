# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_grid_content_from_lines(string):
    grid = set()
    antennas = dict()
    for i, l in enumerate(string.splitlines()):
        for j, c in enumerate(l):
            pos = i, j
            grid.add(pos)
            if c != ".":
                antennas.setdefault(c, []).append(pos)
    return grid, antennas


def get_grid_content_from_file(file_path=top_dir + "resources/year2024_day8_input.txt"):
    with open(file_path) as f:
        return get_grid_content_from_lines(f.read())


def get_antinodes_for_antennas(pos1, pos2, grid, part1=True):
    (x1, y1), (x2, y2) = pos1, pos2
    dx, dy = x1 - x2, y1 - y2
    if part1:
        for p in [(x1 + dx, y1 + dy), (x2 - dx, y2 - dy)]:
            if p in grid:
                yield p
    else:
        x, y = x1, y1
        while (x, y) in grid:
            yield x, y
            x -= dx
            y -= dy
        x, y = x1 + dx, y1 + dy
        while (x, y) in grid:
            yield x, y
            x += dx
            y += dy


def get_antinodes_locations(grid_content, part1=True):
    grid, antennas = grid_content
    return len(
        set(
            a
            for k, lst in antennas.items()
            for p1, p2 in itertools.combinations(lst, 2)
            for a in get_antinodes_for_antennas(p1, p2, grid, part1)
        )
    )


def run_tests():
    grid_content = get_grid_content_from_lines(
        """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
    )
    assert get_antinodes_locations(grid_content, True) == 14
    assert get_antinodes_locations(grid_content, False) == 34


def get_solutions():
    grid_content = get_grid_content_from_file()
    print(get_antinodes_locations(grid_content, True) == 311)
    print(get_antinodes_locations(grid_content, False) == 1115)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
