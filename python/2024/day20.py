# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import heapq
import collections

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_xxx_from_line(string):
    return string


def get_grid_info_from_lines(string):
    start, end = None, None
    walls = set()
    for i, l in enumerate(string.splitlines()):
        for j, v in enumerate(l):
            pos = i, j
            if v == "S":
                start = pos
            elif v == "E":
                end = pos
            elif v == "#":
                walls.add(pos)
            else:
                assert v == "."
    return start, end, walls


def get_grid_info_from_file(file_path=top_dir + "resources/year2024_day20_input.txt"):
    with open(file_path) as f:
        return get_grid_info_from_lines(f.read())


neighbours = ((1, 0), (-1, 0), (0, -1), (0, 1))
oriented_neigh = ((1, 0), (0, 1))


def get_neighbours(pos):
    x, y = pos
    for dx, dy in neighbours:
        yield x + dx, y + dy


def find_shortcuts(grid_info):
    start, end, walls = grid_info
    distances = dict()
    to_visit = [(0, start)]
    while to_visit:
        dist, pos = heapq.heappop(to_visit)
        if pos in distances:
            assert distances[pos] <= dist
            continue
        distances[pos] = dist
        if pos == end:
            break
        for pos2 in get_neighbours(pos):
            if pos2 not in walls:
                heapq.heappush(to_visit, (dist + 1, pos2))
    shortcuts = collections.Counter()
    for x, y in walls:
        for dx, dy in oriented_neigh:
            dist1, dist2 = [
                distances.get((x + s * dx, y + s * dy), None) for s in (-1, 1)
            ]
            if dist1 is not None and dist2 is not None:
                shortcuts[abs(dist1 - dist2) - 2] += 1
    return shortcuts


def run_tests():
    grid_info = get_grid_info_from_lines(
        """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
    )
    assert find_shortcuts(grid_info) == {
        2: 14,
        4: 14,
        8: 4,
        12: 3,
        6: 2,
        10: 2,
        36: 1,
        20: 1,
        38: 1,
        64: 1,
        40: 1,
    }


def get_solutions():
    grid_info = get_grid_info_from_file()
    print(sum(c for d, c in find_shortcuts(grid_info).items() if d >= 100) == 1445)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
