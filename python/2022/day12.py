# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

def get_grid_from_lines(string):
    start = None
    dest = None
    grid = {}
    for i, l in enumerate(string.splitlines()):
        for j, val in enumerate(l):
            pos = (i, j)
            if val == "S":
                start = pos
                val = "a"
            elif val == "E":
                dest = pos
                val = "z"
            grid[pos] = ord(val) - ord("a")
    assert start is not None
    assert dest is not None
    return grid, start, dest


def get_grid_from_file(file_path=resource_dir + "year2022_day12_input.txt"):
    with open(file_path) as f:
        return get_grid_from_lines(f.read())


def get_neighbours(x, y):
    return ((x + dx, y + dy) for (dx, dy) in ((-1, 0), (+1, 0), (0, -1), (0, +1)))


def get_accessible_neighbours(grid, uphill):
    access = {}
    for pos, val in grid.items():
        d = access.setdefault(pos, {})
        for pos2 in get_neighbours(*pos):
            val2 = grid.get(pos2)
            if val2 is not None and (
                (val2 <= val + 1) if uphill else (val2 + 1 >= val)
            ):
                d[pos2] = 1
    return access


def get_distances(grid, start, uphill):
    distances = {}
    queue = collections.deque([(0, start)])
    neigh = get_accessible_neighbours(grid, uphill)
    while queue:
        d, pos = queue.popleft()
        if pos not in distances or distances[pos] > d:
            distances[pos] = d
            queue.extend((d + d2, pos2) for pos2, d2 in neigh[pos].items())
    return distances


def get_path(grid, start, dest):
    return get_distances(grid, start, uphill=True)[dest]


def get_path2(grid, dest):
    return min(
        d
        for pos, d in get_distances(grid, dest, uphill=False).items()
        if grid[pos] == 0
    )


def run_tests():
    grid, start, dest = get_grid_from_lines(
        """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    )
    assert get_path(grid, start, dest) == 31
    assert get_path2(grid, dest) == 29


def get_solutions():
    grid, start, dest = get_grid_from_file()
    print(get_path(grid, start, dest) == 423)
    print(get_path2(grid, dest) == 416)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
