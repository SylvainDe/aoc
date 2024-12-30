# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import heapq

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

directions = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]

directions2 = directions + directions
next_directions = {
    cur: (pre, nex)
    for pre, cur, nex in zip(directions, directions2[1:], directions2[2:])
}

INITIAL_DIRECTION = (0, 1)  # Facing East


def get_map_content_from_lines(string):
    walls = set()
    start, end = None, None
    for i, l in enumerate(string.splitlines()):
        for j, v in enumerate(l):
            pos = i, j
            if v == "#":
                walls.add(pos)
            elif v == "S":
                start = pos
            elif v == "E":
                end = pos
            else:
                assert v == "."
    return start, end, walls


def get_map_content_from_file(file_path=top_dir + "resources/year2024_day16_input.txt"):
    with open(file_path) as f:
        return get_map_content_from_lines(f.read())


def get_path(map_content):
    start, end, walls = map_content
    distances = dict()
    state = (0, start, INITIAL_DIRECTION)
    to_visit = [state]
    while to_visit:
        dist, pos, direct = heapq.heappop(to_visit)
        assert pos not in walls
        state = (pos, direct)
        if state in distances:
            assert distances[state] <= dist
            continue
        distances[state] = dist
        if pos == end:
            break
        x, y = pos
        dx, dy = direct
        pos2 = x + dx, y + dy
        if pos2 not in walls:
            heapq.heappush(to_visit, (dist + 1, pos2, direct))
        for dir2 in next_directions[direct]:
            heapq.heappush(to_visit, (dist + 1000, pos, dir2))
    else:  # no break
        assert False
    # Shortest dist is found, visit backward from here
    shortest_dist = dist
    sits = set([state[0]])
    to_visit2 = set([state])
    while to_visit2:
        pos, direct = to_visit2.pop()
        dist = distances[(pos, direct)]
        x, y = pos
        dx, dy = direct
        pos2 = x - dx, y - dy
        state2 = pos2, direct
        if distances.get(state2, None) == dist - 1:
            to_visit2.add(state2)
            sits.add(pos2)
        for dir2 in next_directions[direct]:
            state2 = pos, dir2
            if distances.get(state2, None) == dist - 1000:
                to_visit2.add(state2)
                sits.add(pos)
    return shortest_dist, len(set(sits))


def run_tests():
    map_content = get_map_content_from_lines(
        """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""
    )
    assert get_path(map_content) == (7036, 45)
    map_content = get_map_content_from_lines(
        """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
    )
    assert get_path(map_content) == (11048, 64)


def get_solutions():
    map_content = get_map_content_from_file()
    dist, sits = get_path(map_content)
    print(dist == 98520)
    print(sits == 609)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
