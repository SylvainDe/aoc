# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re

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
            for dx in range(-l, l+1):
                p = (sx+dx, y_arg)
                assert distance(s, p) <= d_b
                points.add(p)
    return len(points - set(b for s, b in sensors))


def get_pos_with_beacons_naive(sensors, val_max):
    sensors_dist = { s: distance(s, b) for s, b in sensors }
    for x in range(val_max+1):
        for y in range(val_max+1):
            p = (x, y)
            for s, d in sensors_dist.items():
                d2 = distance(s, p)
                if d2 <= d:
                    break
            else:
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


def get_solutions():
    sensors = get_sensor_from_file()
    print(get_pos_without_beacons(sensors, y_arg=2000000))
#    print(get_pos_with_beacons_naive(sensors, val_max=4000000))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
