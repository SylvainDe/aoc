# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_grid_from_lines(string):
    return list(string.splitlines())


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
                    connections.setdefault(pos2, set()).add(pos)
    for p, lst in connections.items():
        if p == start:
            assert len(lst) == 2
        else:
            assert 1 <= len(lst) <= 4
    return start, connections


def get_distances(start, connections):
    dist = {start: 0}
    prev = {}
    positions = {start}
    while positions:
        new_positions = set()
        for p in positions:
            d = dist[p]
            for p2 in connections.get(p, []):
                if p2 not in dist:
                    dist[p2] = d + 1
                    prev[p2] = p
                    new_positions.add(p2)
        # print(set(dist[p] for p in positions), set(dist[p] for p in new_positions))
        positions = new_positions
    return dist, prev


def get_path(connections, beg, end):
    distances, previous = get_distances(beg, connections)
    assert end in distances
    assert end in previous
    pos = end
    path = [end]
    while pos in previous:
        pos = previous[pos]
        path.append(pos)
    return path


def get_loop(grid):
    start, connections = get_data(grid)
    beg, end = connections[start]
    return [start] + get_path(connections, beg, end)


def get_distance_to_furthest(grid):
    return len(get_loop(grid)) // 2


def get_enclosed_tiles(grid):
    loop = get_loop(grid)

    # Consider vertical boundaries: going to the north or to the south
    # One needs to check the role(s) for the S boundary
    start_i, start_j = loop[0]
    northbounds, southbounds = set("|LJ"), set("|7F")
    neighbours = set([loop[1], loop[-1]])
    for (di, dj), boundaries in zip((N, S), (northbounds, southbounds)):
        if (start_i + di, start_j + dj) in neighbours:
            boundaries.add("S")

    loop = set(loop)
    enclosed = set()
    for i, row in enumerate(grid):
        inside = False
        for j, cell in enumerate(row):
            pos = (i, j)
            if pos in loop:
                if cell in southbounds:
                    inside = not inside
            elif inside:
                enclosed.add(pos)
        assert not inside
    return len(enclosed)

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
    grid = get_grid_from_lines(
        """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""")
    assert get_enclosed_tiles(grid) == 4
    grid = get_grid_from_lines(
        """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""")
    assert get_enclosed_tiles(grid) == 8
    grid = get_grid_from_lines(
        """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""")
    assert get_enclosed_tiles(grid) == 10




def get_solutions():
    grid = get_grid_from_file()
    print(get_distance_to_furthest(grid) == 6979)
    print(get_enclosed_tiles(grid) == 443)

if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
