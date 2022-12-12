# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import heapq
import collections


def get_grid_from_lines(string):
    start = None
    dest = None
    grid = dict()
    for i, l in enumerate(string.splitlines()):
        for j, val in enumerate(l):
            if val == "S":
                start = (i, j)
                val = "a"
            elif val == "E":
                dest = (i, j)
                val = "z"
            grid[(i, j)] = ord(val) - ord('a')
    assert start is not None
    assert dest is not None
    return grid, start, dest


def get_grid_from_file(file_path="../../resources/year2022_day12_input.txt"):
    with open(file_path) as f:
        return get_grid_from_lines(f.read())


def get_path(grid, start, dest):
    pos = start
    distances = dict()
    queue = collections.deque([(0, pos)])
    neighbours = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
    while queue:
        d, pos = queue.popleft()
        if pos in distances and distances[pos] <= d:
            continue
        distances[pos] = d
        if pos == dest:
            return d
        x, y = pos
        val = grid[pos]
        for dx, dy in neighbours:
            pos2 = x + dx, y + dy
            if pos2 in grid:
                val2 = grid[pos2]
                if val2 <= val + 1:
                    queue.append((d+1, pos2))




def run_tests():
    grid, start, dest = get_grid_from_lines("""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""")
    assert get_path(grid, start, dest) == 31

def get_solutions():
    grid, start, dest = get_grid_from_file()
    print(get_path(grid, start, dest) == 423)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
