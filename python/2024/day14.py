# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re
import collections
import itertools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


input_re = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"


def get_robot_from_line(string):
    match = re.match(input_re, string)
    return [int(v) for v in match.groups()]


def get_robots_from_lines(string):
    return [get_robot_from_line(l) for l in string.splitlines()]


def get_robots_from_file(file_path=top_dir + "resources/year2024_day14_input.txt"):
    with open(file_path) as f:
        return get_robots_from_lines(f.read())


def get_pos_robot(time, robot, grid):
    x, y, dx, dy = robot
    wid, hei = grid
    return (x + time * dx) % wid, (y + time * dy) % hei


def safety_factor(time, robots, grid):
    wid, hei = grid
    w2, h2 = wid // 2, hei // 2
    quadrants = collections.Counter()
    for x, y in (get_pos_robot(time, r, grid) for r in robots):
        if x != w2 and y != h2:
            quadrants[(x < w2, y < h2)] += 1
    res = 1
    for a, b in itertools.product([True, False], repeat=2):
        res *= quadrants[(a, b)]
    return res


def has_pattern(t, robots, grid):
    wid, hei = grid
    s = set(get_pos_robot(t, r, grid) for r in robots)
    lines = [
        "".join("#" if (x, y) in s else " " for x in range(wid)) for y in range(hei)
    ]
    found = any("#######" in l for l in lines)
    if found:
        print(t)
        print("\n".join(lines))
    return found


def find_easter_egg(robots, grid):
    for t in range(10000):
        if has_pattern(t, robots, grid):
            return t


def run_tests():
    robots = get_robots_from_lines(
        """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    )
    assert safety_factor(100, robots, (11, 7)) == 12


def get_solutions():
    grid = (101, 103)
    robots = get_robots_from_file()
    print(safety_factor(100, robots, grid) == 222062148)
    # print(find_easter_egg(robots, grid) == 7520)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
