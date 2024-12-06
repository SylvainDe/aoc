# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import math
import itertools


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_int_from_file(file_path=top_dir + "resources/year2017_day3_input.txt"):
    with open(file_path) as f:
        for l in f:
            return int(l)


# Spiral is like:
# 36  35  34  33  32  31
# 17  16  15  14  13  30
# 18   5   4   3  12  29
# 19   6   1   2  11  28
# 20   7   8   9  10  27
# 21  22  23  24  25  26
#
# or more generally:
#
# - if n is even:
# <----------------- n ----------------->
#       n²          ...    n²-(n-1)       ^
#       .                    .            |
#       .                    .            | n
#       .                    .            |
#   n²-3(n-1)       ...    n²-2(n-1)      v
#
#
# - if n is odd:
#
# <----------------- n ----------------->
#    n²-2(n-1)      ...    n²-3(n-1)      ^
#       .                    .            |
#       .                    .            | n
#       .                    .            |
#    n²-(n-1)       ...      n²           v
#
#
#
def distance_to_center(n):
    # Get the size of the smallest square containing the value
    size = 1 + math.isqrt(n - 1)
    # Key points for that square size
    end = size * size
    corner = end - size + 1
    beg = beg = corner - size + 1
    assert beg == (size - 1) ** 2 + 1
    assert beg <= corner <= end
    assert beg <= n <= end
    # Get positions in square
    # Note: by performing rotations of the square, we could get an easier solution without changing the final distance
    q, r = divmod(size, 2)
    if r == 0:
        center = (q - 1, q)
        if n > corner:
            pos = (end - n, 0)
        else:
            pos = (size - 1, corner - n)
    else:
        center = (q, q)
        if n > corner:
            pos = (size - 1, n - corner)
        else:
            pos = (0, corner - n)
    # Compute distance
    return sum(abs(c1 - c2) for c1, c2 in zip(center, pos))


def get_spiral_position():
    x, y = 0, 0
    yield x, y
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    direc = 0
    for step in itertools.count(1):
        for _ in range(2):
            dx, dy = directions[direc]
            for _ in range(step):
                x += dx
                y += dy
                yield x, y
            direc = (direc + 1) % 4


def get_neighbours(point):
    x, y = point
    for dx, dy in itertools.product([-1, 0, 1], repeat=2):
        if (dx, dy) != (0, 0):
            yield x + dx, y + dy


def part2(target):
    values = dict()
    for p in get_spiral_position():
        val = sum(values.get(n, 0) for n in get_neighbours(p)) if values else 1
        if val > target:
            return val
        values[p] = val


def run_tests():
    # Tests provided
    assert distance_to_center(1) == 0
    assert distance_to_center(12) == 3
    assert distance_to_center(23) == 2
    assert distance_to_center(1024) == 31
    assert part2(805) == 806


def get_solutions():
    n = get_int_from_file()
    print(distance_to_center(n) == 326)
    print(part2(n) == 363010)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
