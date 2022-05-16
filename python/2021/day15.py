# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import heapq

# Everything looks a lot like AOC 2019 Day 2020


def get_grid_from_file(file_path="day15_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def points_iter(grid):
    for x, line in enumerate(grid):
        for y, val in enumerate(line):
            yield (x, y), int(val)


def neighbours(pos):
    x, y = pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        yield x + dx, y + dy


def build_graph(points):
    return {p: {p2: points[p2] for p2 in neighbours(p) if p2 in points} for p in points}


def shortest_path(points):
    entrance = min(points)
    exit = max(points)
    graph = build_graph(points)
    distances = dict()
    heap = [(0, entrance)]
    while heap:
        d, pos = heapq.heappop(heap)
        if pos == exit:
            return d
        if pos in distances:
            assert d >= distances[pos]
            continue
        distances[pos] = d
        for pos2, d2 in graph[pos].items():
            if pos2 not in distances:
                heapq.heappush(heap, ((d + d2), pos2))
    assert False


def multiply_points(points, n):
    h = 1 + max(p[0] for p in points)
    w = 1 + max(p[1] for p in points)
    points2 = dict()
    for i in range(0, n):
        for j in range(0, n):
            add = i + j
            for (x, y), val in points.items():
                val2 = val + add
                if val2 > 9:
                    val2 -= 9
                points2[(x + i * h, y + j * w)] = val2
    return points2


def run_tests():
    grid = [
        "1163751742",
        "1381373672",
        "2136511328",
        "3694931569",
        "7463417111",
        "1319128137",
        "1359912421",
        "3125421639",
        "1293138521",
        "2311944581",
    ]
    points = dict(points_iter(grid))
    assert shortest_path(points) == 40
    points2 = multiply_points(points, 5)
    assert shortest_path(points2) == 315


def get_solutions():
    grid = get_grid_from_file()
    points = dict(points_iter(grid))
    print(shortest_path(points))
    points2 = multiply_points(points, 5)
    print(shortest_path(points2))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
