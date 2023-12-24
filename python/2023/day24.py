# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_coord(string):
    return tuple(int(s) for s in string.split(", "))

def get_hailstone_from_line(string):
    sep = " @ "
    pos, mid, vel = string.partition(sep)
    assert mid == sep
    return get_coord(pos), get_coord(vel)


def get_hailstones_from_lines(string):
    return [get_hailstone_from_line(l) for l in string.splitlines()]


def get_hailstones_from_file(file_path=top_dir + "resources/year2023_day24_input.txt"):
    with open(file_path) as f:
        return get_hailstones_from_lines(f.read())

def check_intersection(h1, h2, coord_min, coord_max):
    (xi1, yi1, zi1), (vx1, vy1, vz1) = h1
    (xi2, yi2, zi2), (vx2, vy2, vz2) = h2
    # p(t) = pi + t * v
    # x(t) = xi + t * vx
    # y(t) = yi + t * vy
    #      = yi + (x(t) - xi) * (vy / vx)
    # y(x) = yi + (x - xi) * (vy / vx)
    #      = x * (vy / vx) + yi - xi * (vy / vx)
    # Path intersection:
    # y1(x) = y2(x)
    # x * (vy1 / vx1) + yi1 - xi1 * (vy1 / vx1) = x * (vy2 / vx2) + yi2 - xi2 * (vy2 / vx2)
    # x * (vy1 / vx1 - vy2 / vx2) = yi2 - yi1 + xi1 * (vy1 / vx1)- xi2 * (vy2 / vx2)
    # x = [yi2 - yi1 + xi1 * (vy1 / vx1) - xi2 * (vy2 / vx2)] / (vy1 / vx1 - vy2 / vx2)
    #   = ((yi2 - yi1) * vx2 * vx1 + xi1 * vy1 * vx2 - xi2 * vy2 * vx1) / (vy1 * vx2 - vy2 * vx1)
    try:
        x = ((yi2 - yi1) * vx2 * vx1 + xi1 * vy1 * vx2 - xi2 * vy2 * vx1) / (vy1 * vx2 - vy2 * vx1)
        t1 = (x - xi1) / vx1
        t2 = (x - xi2) / vx2
        y1 = x * (vy1 / vx1) + yi1 - xi1 * (vy1 / vx1)
        y2 = x * (vy2 / vx2) + yi2 - xi2 * (vy2 / vx2)
        is_ok = t1 >= 0 and t2 >= 0 and coord_min <= x <= coord_max and coord_min <= y1 <= coord_max
        # print(h1, h2, x, y1, y2, t1, t2, is_ok)
        return is_ok
    except ZeroDivisionError:
        return False

def get_nb_intersect(hailstones, coord_min, coord_max):
    return sum(check_intersection(h1, h2, coord_min, coord_max)
               for h1, h2 in itertools.combinations(hailstones, 2))

def run_tests():
    hailstones = get_hailstones_from_lines(
        """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
    )
    assert get_nb_intersect(hailstones, 7, 27) == 2


def get_solutions():
    hailstones = get_hailstones_from_file()
    print(get_nb_intersect(hailstones, 200000000000000, 400000000000000) == 16665)

if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
