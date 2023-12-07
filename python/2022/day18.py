# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools
import collections


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

def get_cube_from_line(string):
    return tuple(int(s) for s in string.split(","))


def get_cubes_from_lines(string):
    return set(get_cube_from_line(l) for l in string.splitlines())


def get_cubes_from_file(file_path=top_dir + "resources/year2022_day18_input.txt"):
    with open(file_path) as f:
        return get_cubes_from_lines(f.read())


def get_neighbours(cube):
    x, y, z = cube
    return (
        (x + dx, y + dy, z + dz)
        for dx, dy, dz in (
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (-1, 0, 0),
            (0, -1, 0),
            (0, 0, -1),
        )
    )


def get_surface_area(cubes):
    return 6 * len(cubes) - sum(c2 in cubes for c in cubes for c2 in get_neighbours(c))


def get_exterior_surface_area(cubes):
    xs = set(c[0] for c in cubes)
    ys = set(c[1] for c in cubes)
    zs = set(c[2] for c in cubes)
    # Look if cube can connect to exterior_cube
    x_range = list(range(min(xs) - 1, max(xs) + 1 + 1))
    y_range = list(range(min(ys) - 1, max(ys) + 1 + 1))
    z_range = list(range(min(zs) - 1, max(zs) + 1 + 1))
    universe = set(itertools.product(x_range, y_range, z_range))
    empty = universe - cubes
    reachable = set()
    cubes_deque = collections.deque([(x_range[0], y_range[0], z_range[0])])
    while cubes_deque:
        c = cubes_deque.popleft()
        if c not in reachable:
            reachable.add(c)
            cubes_deque.extend(
                c2 for c2 in get_neighbours(c) if c2 in empty and c2 not in reachable
            )
    return get_surface_area(universe - reachable)


def run_tests():
    cubes = get_cubes_from_lines(
        """1,1,1
    2,1,1"""
    )
    assert get_surface_area(cubes) == 10
    assert get_exterior_surface_area(cubes) == 10

    cubes = get_cubes_from_lines(
        """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""
    )
    assert get_surface_area(cubes) == 64
    assert get_exterior_surface_area(cubes) == 58


def get_solutions():
    cubes = get_cubes_from_file()
    print(get_surface_area(cubes) == 3586)
    print(get_exterior_surface_area(cubes) == 2072)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
