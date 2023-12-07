# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

size = 5


def make_point(i, j):
    return (i, j)


def make_point3d(i, j):
    return (i, j, 0)


def get_bugs_from_lines(lines, make_point_func=make_point):
    for i, line in enumerate(lines):
        for j, val in enumerate(line):
            if val == "#":
                yield make_point_func(i, j)


def get_bugs_from_file(
    file_path=top_dir + "resources/year2019_day24_input.txt", make_point_func=make_point
):
    with open(file_path) as f:
        return set(get_bugs_from_lines(f, make_point_func))


def show_bugs(bugs):
    i_range = list(range(size))
    j_range = list(range(size))
    for i in i_range:
        print("".join("#" if (i, j) in bugs else "." for j in j_range))


def show_bugs3d(bugs):
    k_vals = [k for _, _, k in bugs]
    k_range = list(range(min(k_vals), max(k_vals) + 1))
    i_range = list(range(size))
    j_range = list(range(size))
    for k in k_range:
        print("Depth", k, ":")
        for i in i_range:
            print("".join("#" if (i, j, k) in bugs else "." for j in j_range))


def neighbours(pos):
    i, j = pos
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        i2, j2 = i + di, j + dj
        if 0 <= i2 < size and 0 <= j2 < size:
            yield i2, j2


def neighbours3d(pos):
    i, j, k = pos
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        i2, j2 = i + di, j + dj
        if (i2, j2) == (2, 2):  # Neighbour with the middle
            assert 0 in (di, dj) and (di, dj) != (0, 0)
            if di == 0:
                for i2 in range(size):
                    yield i2, j - dj, k + 1
            if dj == 0:
                for j2 in range(size):
                    yield i - di, j2, k + 1
        elif not (0 <= i2 < size):  # Neighbour with border
            assert 0 <= j2 < size
            yield i - di, 2, k - 1
        elif not (0 <= j2 < size):  # Neighbour with border
            assert 0 <= i2 < size
            yield 2, j - dj, k - 1
        else:
            yield i2, j2, k


def next_gen(bugs, neigh_func):
    neigh_count = collections.Counter(n for b in bugs for n in neigh_func(b))
    next_bugs = set()
    for b, count in neigh_count.items():
        if count == 1 and b in bugs:
            next_bugs.add(b)
        elif count in (1, 2) and b not in bugs:
            next_bugs.add(b)
    return next_bugs


def first_repeated_layout(bugs, neigh_func=neighbours):
    seen = set()
    bugs = tuple(bugs)
    while bugs not in seen:
        seen.add(bugs)
        bugs = tuple(next_gen(bugs, neigh_func))
    return sum(2 ** (i * size + j) for i, j in bugs)


def get_bugs_after_n_generations(bugs, n, neigh_func=neighbours):
    for _ in range(n):
        bugs = next_gen(bugs, neigh_func)
    return bugs


def run_tests_part1():
    assert sorted(neighbours((2, 3))) == [
        (1, 3),
        (2, 2),
        (2, 4),
        (3, 3),
    ]
    assert sorted(neighbours((0, 0))) == [(0, 1), (1, 0)]
    bugs = [
        "....#",
        "#..#.",
        "#..##",
        "..#..",
        "#....",
    ]
    bugs = set(get_bugs_from_lines(bugs))
    assert first_repeated_layout(bugs) == 2129920
    assert len(get_bugs_after_n_generations(bugs, 2)) == 12
    assert len(get_bugs_after_n_generations(bugs, 3)) == 13
    assert len(get_bugs_after_n_generations(bugs, 4)) == 10


def run_tests_part2():
    # Tile 19
    assert sorted(neighbours3d((3, 3, 0))) == [
        (2, 3, 0),
        (3, 2, 0),
        (3, 4, 0),
        (4, 3, 0),
    ]
    # Tile G
    assert sorted(neighbours3d((1, 1, 0))) == [
        (0, 1, 0),
        (1, 0, 0),
        (1, 2, 0),
        (2, 1, 0),
    ]
    # Tile D
    assert sorted(neighbours3d((0, 3, 0))) == [
        (0, 2, 0),
        (0, 4, 0),
        (1, 2, -1),
        (1, 3, 0),
    ]
    # Tile E
    assert sorted(neighbours3d((0, 4, 0))) == [
        (0, 3, 0),
        (1, 2, -1),
        (1, 4, 0),
        (2, 3, -1),
    ]
    # Tile 14/N
    assert sorted(neighbours3d((2, 3, 0))) == [
        (0, 4, 1),
        (1, 3, 0),
        (1, 4, 1),
        (2, 4, 0),
        (2, 4, 1),
        (3, 3, 0),
        (3, 4, 1),
        (4, 4, 1),
    ]
    bugs = [
        "....#",
        "#..#.",
        "#..##",
        "..#..",
        "#....",
    ]
    bugs = set(get_bugs_from_lines(bugs, make_point3d))
    assert len(get_bugs_after_n_generations(bugs, 10, neighbours3d)) == 99


def run_tests():
    run_tests_part1()
    run_tests_part2()


def get_solutions():
    # Part 1
    bugs = get_bugs_from_file()
    print(first_repeated_layout(bugs) == 32506911)
    # Part 2
    bugs = get_bugs_from_file(make_point_func=make_point3d)
    print(len(get_bugs_after_n_generations(bugs, 200, neighbours3d)) == 2025)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
