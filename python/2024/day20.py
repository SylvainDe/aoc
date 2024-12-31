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


def between(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def find_shortcuts(grid_info, cheat_len=2):
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
    for pos1, dist1 in distances.items():
        for pos2, dist2 in distances.items():
            dist = between(pos1, pos2)
            if dist <= cheat_len:
                diff_dist = dist2 - dist1 - dist
                if diff_dist > 0:
                    shortcuts[diff_dist] += 1
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
    shortcuts = {k: v for k, v in find_shortcuts(grid_info, 20).items() if k >= 50}
    assert shortcuts == {
        50: 32,
        52: 31,
        54: 29,
        56: 39,
        58: 25,
        60: 23,
        62: 20,
        64: 19,
        66: 12,
        68: 14,
        70: 12,
        72: 22,
        74: 4,
        76: 3,
    }


def get_solutions():
    grid_info = get_grid_info_from_file()
    shortcuts = {k: v for k, v in find_shortcuts(grid_info).items() if k >= 100}
    print(sum(shortcuts.values()) == 1445)
    shortcuts = {k: v for k, v in find_shortcuts(grid_info, 20).items() if k >= 100}
    print(sum(shortcuts.values()) == 1008040)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
