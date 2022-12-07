# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import math


def get_grid_from_file(file_path="../../resources/year2019_day10_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def get_asteroids(grid):
    for i, line in enumerate(grid):
        for j, val in enumerate(line):
            if val == "#":
                yield j, i


def integer_path(a, b):
    (xa, ya), (xb, yb) = a, b
    dx, dy = xa - xb, ya - yb
    if (dx, dy) == (0, 0):
        return
    elif dx == 0:
        steps = abs(dy)
    elif dy == 0:
        steps = abs(dx)
    else:
        steps = math.gcd(dx, dy)
    assert steps
    udx, udy = dx // steps, dy // steps
    assert dx % steps == 0
    assert dy % steps == 0
    for s in range(1, steps):
        x, y = xa - s * udx, ya - s * udy
        assert (x, y) != a
        assert (x, y) != b
        yield x, y


def visible(a, b, asteroids):
    return not any(p in asteroids for p in integer_path(a, b))


def get_best_asteroid_count(grid):
    asteroids = set(get_asteroids(grid))
    return max(
        (sum(a != b and visible(a, b, asteroids) for b in asteroids), a)
        for a in asteroids
    )


def vaporise(grid, ref, index):
    xo, yo = ref
    asteroids = set(get_asteroids(grid))
    angles = dict()
    for p in asteroids:
        x, y = p
        dx, dy = x - xo, y - yo
        # Compute tuple emulating some kind of angle
        #  - first value is: 0 for up axis, 1 for right side, 2 for down axis, 3 for left side
        #  - second value is dy/dx (or 0 if undefined)
        if dx > 0:
            angle = (1, dy / dx)
            dist = abs(dx)
        elif dx < 0:
            angle = (3, dy / dx)
            dist = abs(dx)
        else:
            dist = abs(dy)
            if dy > 0:
                angle = (2, 0)
            elif dy < 0:
                angle = (0, 0)
            else:
                continue
        angles.setdefault(angle, []).append((dist, p))
    for l in angles.values():
        l.sort()
    vaporised = []
    while angles:
        for a in list(sorted(angles)):
            l = angles[a]
            dist, p = l.pop(0)
            vaporised.append(p)
            if not l:
                del angles[a]
    x, y = vaporised[index - 1]
    return 100 * x + y


def run_tests():
    grid1 = [
        ".#..#",
        ".....",
        "#####",
        "....#",
        "...##",
    ]
    assert get_best_asteroid_count(grid1)[0] == 8
    grid2 = [
        ".#..##.###...#######",
        "##.############..##.",
        ".#.######.########.#",
        ".###.#######.####.#.",
        "#####.##.#.##.###.##",
        "..#####..#.#########",
        "####################",
        "#.####....###.#.#.##",
        "##.#################",
        "#####.##.###..####..",
        "..######..##.#######",
        "####.##.####...##..#",
        ".#####..#.######.###",
        "##...#.##########...",
        "#.##########.#######",
        ".####.#.###.###.#.##",
        "....##.##.###..#####",
        ".#.#.###########.###",
        "#.#.#.#####.####.###",
        "###.##.####.##.#..##",
    ]
    count2, p2 = get_best_asteroid_count(grid2)
    assert count2 == 210
    assert p2 == (11, 13)
    assert vaporise(grid2, p2, 200) == 802


def get_solutions():
    grid = get_grid_from_file()
    count, p = get_best_asteroid_count(grid)
    print(count == 256)
    print(vaporise(grid, p, 200) == 1707)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
