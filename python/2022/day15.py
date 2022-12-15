# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import itertools

# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
sensors_re = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

def get_sensor_from_line(string):
    sx, sy, bx, by = [int(s) for s in sensors_re.match(string).groups()]
    return (sx, sy), (bx, by)

def get_sensor_from_lines(string):
    return [get_sensor_from_line(l) for l in string.splitlines()]

def get_sensor_from_file(file_path="../../resources/year2022_day15_input.txt"):
    with open(file_path) as f:
        return get_sensor_from_lines(f.read())

def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

def get_pos_without_beacons(sensors, y_arg):
    points = set()
    for s, b in sensors:
        sx, sy = s
        closest = (sx, y_arg)
        d_b = distance(s, b)
        d_closest = distance(s, closest)
        l = d_b - d_closest
        if l >= 0:
            new_points = [(sx+dx, y_arg) for dx in range(-l, l+1)]
            # for p in new_points:
            #     assert distance(s, p) <= d_b
            points.update(new_points)
    return len(points - set(b for s, b in sensors))


def get_pos_with_beacons_naive(sensors, val_max):
    sensors_dist = { s: distance(s, b) for s, b in sensors }
    for p in itertools.product(range(val_max+1), repeat=2):
        if all(distance(s, p) > d for s, d in sensors_dist.items()):
            x, y = p
            return x * 4000000 + y


def get_manhattan_circle(center, radius):
    x, y = center
    points = set()
    for i in range(radius+1):
       # Note: tiny overlap which could probably be optimised with better code
       points.add((i+x, y+radius-i))  # upper-right
       points.add((i+x, y-radius+i))  # upper-left
       points.add((i+x-radius, y+i))  # lower-right
       points.add((i+x-radius, y-i))  # lower-left
    # for p in points:
    #     assert distance(center, p) == radius
    return points


def get_pos_with_beacons(sensors, val_max):
    # Assume we'll be at the intersection of at least 3 squares/circles
    sensors_dist = { s: distance(s, b) for s, b in sensors }
    points = dict()
    for s, d in sensors_dist.items():
        for p in get_manhattan_circle(s, d+1):
            points.setdefault(p, set()).add(s)
    for pos, lst in points.items():
        x, y = pos
        if 0 <= x <= val_max and 0 <= y <= val_max and len(lst) >= 3:
            if all(distance(s, pos) > d for s, d in sensors_dist.items()):
                return x * 4000000 + y


def run_tests():
    sensors = get_sensor_from_lines("""Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""")
    assert get_pos_without_beacons(sensors, y_arg=10) == 26
    assert get_pos_with_beacons_naive(sensors, val_max=20) == 56000011
    assert get_manhattan_circle((100, 200), 5) == set([(95, 200), (96, 199), (96, 201), (97, 198), (97, 202), (98, 197), (98, 203), (99, 196), (99, 204), (100, 195), (100, 205), (101, 196), (101, 204), (102, 197), (102, 203), (103, 198), (103, 202), (104, 199), (104, 201), (105, 200)])
    assert get_pos_with_beacons(sensors, val_max=20) == 56000011


def get_solutions():
    sensors = get_sensor_from_file()
    print(get_pos_without_beacons(sensors, y_arg=2000000) == 4811413)
    # print(get_pos_with_beacons(sensors, val_max=4000000) == 13171855019123) # Still a bit slow :(


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
