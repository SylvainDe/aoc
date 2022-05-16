# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections


def get_line_from_str(s):
    return [int(d) for d in s.strip()]


def get_grid_from_file(file_path="day9_input.txt"):
    with open(file_path) as f:
        return [get_line_from_str(l) for l in f]


def points(grid):
    for x, line in enumerate(grid):
        for y, val in enumerate(line):
            yield x, y, val


def neighbours(grid, x, y):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x2, y2 = x + dx, y + dy
        if 0 <= x2 < len(grid):
            l = grid[x2]
            if 0 <= y2 < len(l):
                yield x2, y2, l[y2]


def get_low_points(grid):
    return (
        (x, y, val)
        for x, y, val in points(grid)
        if all(v > val for _, _, v in neighbours(grid, x, y))
    )


def print_point_sets(grid, points):
    for x, line in enumerate(grid):
        print("".join("X" if (x, y) in points else " " for y, val in enumerate(line)))


def part1(grid):
    return sum(val + 1 for x, y, val in get_low_points(grid))


def get_basin_from_low_point(grid, low_point):
    basin = set()
    queue = collections.deque([low_point])
    while queue:
        pos = queue.popleft()
        if pos not in basin:
            basin.add(pos)
            x, y = pos
            val = grid[x][y]
            for x2, y2, v2 in neighbours(grid, x, y):
                if v2 > val and v2 != 9:
                    queue.append((x2, y2))
    return basin


def part2(grid):
    basins = {
        (x, y): get_basin_from_low_point(grid, (x, y))
        for x, y, val in get_low_points(grid)
    }
    # Additional verification that no one asked
    # "all other locations will always be part of exactly one basin"
    if False:
        point_to_basins = dict()
        for low_point, basin in basins.items():
            for point in basin:
                point_to_basins.setdefault(point, []).append(low_point)
        for low_points in point_to_basins.values():
            assert len(low_points) == 1
    basins_len = sorted([len(basin) for basin in basins.values()], reverse=True)
    return basins_len[0] * basins_len[1] * basins_len[2]


def run_tests():
    grid = [
        "2199943210",
        "3987894921",
        "9856789892",
        "8767896789",
        "9899965678",
    ]
    grid = [get_line_from_str(l) for l in grid]
    assert part1(grid) == 15
    assert part2(grid) == 1134


def get_solutions():
    grid = get_grid_from_file()
    print(part1(grid))
    print(part2(grid))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
