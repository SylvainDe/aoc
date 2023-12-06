# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import string
import heapq
import collections


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

def get_maze_from_file(file_path=resource_dir + "year2019_day18_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def is_entrance(c):
    return c == "@"


def is_key(c):
    return c in string.ascii_lowercase


def is_empty(c):
    return c == "."


def is_free(c, keys):
    return c != "#" and (not c.isupper() or c.lower() in keys)
    # return is_empty(c) or is_key(c) or is_entrance(c) or c.lower() in keys


def at(maze, pos):
    x, y = pos
    return maze[x][y]


def find(maze, func):
    for i, l in enumerate(maze):
        for j, c in enumerate(l):
            if func(c):
                yield i, j


def find_entrance(maze):
    entrances = list(find(maze, is_entrance))
    assert len(entrances) == 1
    return entrances[0]


def find_keys(maze):
    return list(find(maze, is_key))


def distances_to_keys(maze, pos, keys):
    # print("distances_to_keys:", keys_to_find)
    # Dijkstra algorithm
    distances = dict()
    queue = collections.deque([(0, pos)])
    neighbours = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
    while queue:
        d, pos = queue.popleft()
        distances[pos] = d
        x, y = pos
        d2 = d + 1
        for dx, dy in neighbours:
            pos2 = x + dx, y + dy
            if pos2 not in distances:
                cell = at(maze, pos2)
                if is_free(cell, keys):
                    queue.append((d2, pos2))
                if is_key(cell) and cell not in keys:
                    yield pos2, d2, cell


def get_all_keys(maze):
    entrance = find_entrance(maze)
    nb_keys_to_find = len(find_keys(maze))
    # Create heap with values
    #  (distance travelled, -nb_keys_found, position, keys_found)
    #                                       ~~~~~~~~~~~~~~~~~~~~ <- enough to provide full state
    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ <- the smaller, the better
    heap = [(0, 0, entrance, frozenset())]
    seen = dict()
    while heap:
        # For each state, check reachables keys and associated distances with Dijsktra
        # add new state to heap
        dist, nb_keys, pos, keys_found = heapq.heappop(heap)
        state = (pos, keys_found)
        state_seen = seen.get(state, None)
        if state_seen:
            assert state_seen <= dist
            continue
        seen[state] = dist
        assert -len(keys_found) == nb_keys
        if len(keys_found) == nb_keys_to_find:
            return dist
        for k_pos, d, new_key in distances_to_keys(maze, pos, keys_found):
            assert new_key not in keys_found
            dist2 = dist + d
            keys_found2 = keys_found | frozenset([new_key])
            heapq.heappush(heap, (dist2, -len(keys_found2), k_pos, keys_found2))
    assert 0


def run_tests():
    maze = [
        "########################",
        "#f.D.E.e.C.b.A.@.a.B.c.#",
        "######################.#",
        "#d.....................#",
        "########################",
    ]
    assert get_all_keys(maze) == 86
    maze = [
        "########################",
        "#...............b.C.D.f#",
        "#.######################",
        "#.....@.a.B.c.d.A.e.F.g#",
        "########################",
    ]
    assert get_all_keys(maze) == 132
    maze = [
        "#################",
        "#i.G..c...e..H.p#",
        "########.########",
        "#j.A..b...f..D.o#",
        "########@########",
        "#k.E..a...g..B.n#",
        "########.########",
        "#l.F..d...h..C.m#",
        "#################",
    ]
    assert get_all_keys(maze) == 136
    maze = [
        "########################",
        "#@..............ac.GI.b#",
        "###d#e#f################",
        "###A#B#C################",
        "###g#h#i################",
        "########################",
    ]
    assert get_all_keys(maze) == 81


def get_solutions():
    _ = get_maze_from_file()
    # Too slow: print(get_all_keys(maze))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
