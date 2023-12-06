# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"


def get_number_from_file(file_path=resource_dir + "year2016_day13_input.txt"):
    with open(file_path) as f:
        for l in f:
            return int(l.strip())


def is_open(point, number):
    x, y = point
    return (
        x >= 0
        and y >= 0
        and (bin(x * x + 3 * x + 2 * x * y + y + y * y + number).count("1") % 2 == 0)
    )


neigh = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def neighbours(point, number):
    x, y = point
    for dx, dy in neigh:
        p = (x + dx, y + dy)
        if is_open(p, number):
            yield p


def show_distances(number, distances):
    max_d = max(distances.values())
    width = len(str(max_d)) + 2

    def point_str(p):
        if p in distances:
            return str(distances[p]).center(width, " ")
        if is_open(p, number):
            return "#" * width
        return " " * width

    x_vals = [x for x, _ in distances.keys()]
    y_vals = [y for _, y in distances.keys()]
    x_range = list(range(min(x_vals), 1 + max(x_vals)))
    y_range = list(range(min(y_vals), 1 + max(y_vals)))
    for y in y_range:
        print("".join(point_str((x, y)) for x in x_range))
    print()


def shortest_path(start, end, number):
    distances = dict()
    assert is_open(start, number)
    assert is_open(end, number)
    points = collections.deque([(start, 0)])
    while points:
        p, d = points.popleft()
        if p in distances:
            assert d == distances[p]
            continue
        distances[p] = d
        if p == end:
            return distances[end]
        points.extend((n, d + 1) for n in neighbours(p, number) if n not in distances)
    assert False


def reachable(start, number, steps):
    distances = dict()
    assert is_open(start, number)
    points = collections.deque([(start, 0)])
    while points:
        p, d = points.popleft()
        if d > steps:
            break
        if p in distances:
            assert d == distances[p]
            continue
        distances[p] = d
        points.extend((n, d + 1) for n in neighbours(p, number) if n not in distances)
    return distances


def run_tests():
    number = 10
    assert shortest_path((1, 1), (7, 4), number) == 11


def get_solutions():
    number = get_number_from_file()
    print(shortest_path((1, 1), (31, 39), number) == 92)
    print(len(reachable((1, 1), number, 50)) == 124)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
