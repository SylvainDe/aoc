# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_grid_from_lines(string):
    return [l for l in string.splitlines()]


def get_grid_from_file(file_path=top_dir + "resources/year2023_day10_input.txt"):
    with open(file_path) as f:
        return get_grid_from_lines(f.read())

N = (-1, 0)
S = (+1, 0)
W = (0, -1)
E = (0, +1)

connectors = {
    "|": [N, S],  # a vertical pipe connecting north and south.
    "-": [W, E],  # a horizontal pipe connecting east and west.
    "L": [N, E],  # a 90-degree bend connecting north and east.
    "J": [N, W],  # a 90-degree bend connecting north and west.
    "7": [S, W],  # a 90-degree bend connecting south and west.
    "F": [S, E],  # a 90-degree bend connecting south and east.
    ".": [],      # ground; there is no pipe in this tile."
}

def get_data(grid):
    start = None
    connections = dict()
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            pos = (i, j)
            if cell == "S":
                start = pos
            else:
                for di, dj in connectors[cell]:
                    pos2 = (i+di, j+dj)
                    # connections.setdefault(pos, set()).add(pos2)
                    connections.setdefault(pos2, set()).add(pos)
    for p, lst in connections.items():
        # print(p, len(lst))
        if p == start:
            assert len(lst) == 2
        else:
            assert 1 <= len(lst) <= 4
    return start, connections

def get_distances(start, connections):
    dist = {start: 0}
    positions = {start}
    while positions:
        new_positions = set()
        for p in positions:
            d = dist[p]
            for p2 in connections.get(p, []):
                if p2 not in dist:
                    dist[p2] = d + 1
                    new_positions.add(p2)
        # print(set(dist[p] for p in positions), set(dist[p] for p in new_positions))
        positions = new_positions
    return dist


def get_distance_to_furthest(grid):
    start, connections = get_data(grid)
    beg, end = connections[start]
    dist = get_distances(beg, connections)
    return 1 + dist[end] // 2

def run_tests():
    grid = get_grid_from_lines(
        """.....
.S-7.
.|.|.
.L-J.
....."""
    )
    assert get_distance_to_furthest(grid) == 4
    grid = get_grid_from_lines(
        """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
    )
    assert get_distance_to_furthest(grid) == 8



def get_solutions():
    grid = get_grid_from_file()
    print(get_distance_to_furthest(grid) == 6979)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
